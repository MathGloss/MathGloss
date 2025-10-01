#!/usr/bin/env python3
"""Infer semantic relationships between Chicago-linked concepts using Ollama Cloud.

This script iterates over every MathGloss entry that includes a Chicago
definition, locates the markdown file for that definition, and inspects the
linked Chicago concepts within the text.  For each (source concept, linked
concept) pair it queries an Ollama-hosted language model (default:
``deepseek-v3.1:671b-cloud``) to classify their relationship.  The model is
asked to choose among three structural relations only: ``instance_of``,
``subclass_of``, or ``part_of``.

Results are streamed into a CSV for downstream graph loading, while responses
are cached in a JSON sidecar to avoid repeated LLM calls across runs.  The
script talks to Ollama via the official Python client, so any OpenAI-compatible
endpoint (cloud or self-hosted) can be targeted by supplying ``--host`` or the
``OLLAMA_HOST`` environment variable.
"""
from __future__ import annotations

import argparse
import csv
import itertools
import json
import logging
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional, Tuple

try:
    from ollama import Client as OllamaClient
    from ollama import RequestError, ResponseError
except ImportError as exc:  # pragma: no cover
    raise SystemExit("The 'ollama' package is required. Install it via 'pip install ollama'.") from exc


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

from scripts.graphing.concept_extractor import extract_links


DEFAULT_DATABASE = Path("data/database.csv")
DEFAULT_CHICAGO_DIR = Path("chicago")
DEFAULT_OUTPUT = Path("data/chicago_llm_relations.csv")
DEFAULT_CACHE = Path("data/chicago_relation_cache.json")
DEFAULT_MODEL = "deepseek-v3.1:671b-cloud"
DEFAULT_HOST = os.environ.get("OLLAMA_HOST", os.environ.get("OLLAMA_API_BASE", "https://ollama.com"))
DEFAULT_TIMEOUT = 120
STANDARD_RELATIONS = ("instance_of","subclass_of","has_property","has_part")
PROMPT_TEMPLATE = """You are an ontology assistant helping to build a knowledge graph.

Analyse the provided MathGloss excerpt to determine how the linked concept
relates to the main concept.

The relationship "instance_of" means that the main concept is itself an instance of the linked concept.
The relationship "subclass_of" means that every instance of the main concept is an instance of the linked concept.
The relationship "has_property" means that the main concept has the linked concept as a property. 
The relationship "has_part" means that the main concept has the linked concept as a part.

Main concept:
- Label: {source_label}

Linked concept:
- Label: {target_label}

Definition of main concept:
"""

PROMPT_SUFFIX = """
Pick the single best relationship from the allowed options below. You must
choose exactly one of: instance_of, subclass_of, has_property, has_part. Do not invent other
relation names.

Return a compact JSON object with these keys:
- relation (string)
- confidence (float 0-1, or null if you cannot judge)
- rationale (short English justification)

Respond with JSON only.
"""


@dataclass(frozen=True)
class ConceptPair:
    source_qid: str
    source_label: str
    source_slug: str
    target_qid: str
    target_label: str
    target_slug: str
    context: str
    source_url: str
    target_url: str

    @property
    def cache_key(self) -> str:
        return f"{self.source_qid or self.source_slug}→{self.target_qid or self.target_slug}"


@dataclass
class InferenceResult:
    relation: str
    confidence: Optional[float]
    rationale: str
    raw_response: str
    model: str
    cache_hit: bool = False

    def as_row(self, pair: ConceptPair) -> Dict[str, str]:
        return {
            "parent_qid": pair.source_qid,
            "parent_label": pair.source_label,
            "child_qid": pair.target_qid,
            "child_label": pair.target_label,
            "relation": self.relation,
            "confidence": "" if self.confidence is None else f"{self.confidence:.3f}",
            "rationale": self.rationale,
            "source_url": pair.source_url,
            "target_url": pair.target_url,
            "context": pair.context,
            "model": self.model,
            "cache_hit": "yes" if self.cache_hit else "no",
        }


def extract_chicago_slug(url: str) -> Optional[str]:
    if not url:
        return None
    prefixes = (
        "https://mathgloss.github.io/MathGloss/chicago/",
        "http://mathgloss.github.io/MathGloss/chicago/",
        "/chicago/",
    )
    slug: Optional[str] = None
    for prefix in prefixes:
        if url.startswith(prefix):
            slug = url[len(prefix):]
            break
    if slug is None:
        return None
    slug = slug.strip("/")
    if not slug:
        return None
    slug = slug.split("#", 1)[0]
    slug = slug.split("?", 1)[0]
    return slug or None


def load_database_rows(database_path: Path) -> Tuple[List[Dict[str, str]], Dict[str, str]]:
    if not database_path.exists():
        raise FileNotFoundError(f"Database CSV not found: {database_path}")
    rows: List[Dict[str, str]] = []
    label_lookup: Dict[str, str] = {}
    with database_path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            qid = (row.get("Wikidata ID") or "").strip()
            label = (row.get("Wikidata Label") or qid).strip()
            if qid:
                label_lookup[qid] = label
            rows.append(row)
    return rows, label_lookup


def build_chicago_slug_to_qid(rows: Iterable[Dict[str, str]]) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    for row in rows:
        qid = (row.get("Wikidata ID") or "").strip()
        link = (row.get("Chicago Link") or "").strip()
        slug = extract_chicago_slug(link)
        if qid and slug and slug not in mapping:
            mapping[slug] = qid
    return mapping


def strip_front_matter(markdown_text: str) -> str:
    lines = markdown_text.splitlines()
    if lines and lines[0].strip() == "---":
        end_idx = None
        for idx in range(1, len(lines)):
            if lines[idx].strip() == "---":
                end_idx = idx
                break
        if end_idx is not None:
            lines = lines[end_idx + 1 :]
        else:  # ill-formed front matter; drop first line
            lines = lines[1:]
    lines = [line for line in lines if not line.strip().startswith("Wikidata ID:")]
    return "\n".join(lines).strip()


def markdown_to_plain(markdown_text: str) -> str:
    text = markdown_text
    text = re.sub(r"```.+?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", text)
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def sentence_window(text: str, start: int, end: int, window: int = 220) -> str:
    left = max(0, start - window)
    right = min(len(text), end + window)
    snippet = text[left:right]
    return snippet.strip()


def gather_concept_pairs(
    rows: Iterable[Dict[str, str]],
    slug_to_qid: Dict[str, str],
    chicago_dir: Path,
    label_lookup: Dict[str, str],
) -> Iterator[ConceptPair]:
    for row in rows:
        source_qid = (row.get("Wikidata ID") or "").strip()
        chicago_link = (row.get("Chicago Link") or "").strip()
        if not (source_qid and chicago_link):
            continue
        source_slug = extract_chicago_slug(chicago_link)
        if not source_slug:
            continue
        md_path = chicago_dir / f"{source_slug}.md"
        if not md_path.exists():
            logging.warning("Chicago markdown missing for %s (%s)", source_qid, source_slug)
            continue
        raw_markdown = md_path.read_text(encoding="utf-8")
        body_markdown = strip_front_matter(raw_markdown)
        links = extract_links(body_markdown)
        if not links:
            continue
        source_label = label_lookup.get(source_qid, source_qid)
        source_url = chicago_link
        for link in links:
            target_slug = extract_chicago_slug(link.url)
            if not target_slug:
                continue
            target_qid = slug_to_qid.get(target_slug, "")
            target_label = label_lookup.get(target_qid, target_slug) if target_qid else target_slug
            target_url = link.url
            context_markdown = sentence_window(body_markdown, link.start, link.end)
            context_snippet = markdown_to_plain(context_markdown)
            if not context_snippet:
                context_snippet = markdown_to_plain(body_markdown[:280])
            yield ConceptPair(
                source_qid=source_qid,
                source_label=source_label,
                source_slug=source_slug,
                target_qid=target_qid,
                target_label=target_label,
                target_slug=target_slug,
                context=context_snippet,
                source_url=source_url,
                target_url=target_url,
            )


def load_cache(path: Path) -> Dict[str, Dict[str, object]]:
    if not path.exists():
        return {}
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError as exc:
        logging.warning("Failed to parse cache %s (%s); starting fresh", path, exc)
        return {}


def save_cache(cache: Dict[str, Dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with tmp_path.open("w", encoding="utf-8") as handle:
        json.dump(cache, handle, ensure_ascii=False, indent=2, sort_keys=True)
    tmp_path.replace(path)


def build_messages(pair: ConceptPair) -> List[Dict[str, str]]:
    excerpt = f"{pair.context}"
    prompt = PROMPT_TEMPLATE.format(
        source_label=pair.source_label,
        source_qid=pair.source_qid or "unknown",
        target_label=pair.target_label,
        target_qid=pair.target_qid or "unknown",
    ) + excerpt + "\n\n" + PROMPT_SUFFIX
    system_instruction = (
        "You are a precise ontology assistant. Always return valid JSON with the keys"
        " 'relation', 'confidence', and 'rationale'. The 'relation' value must be exactly"
        " one of: instance_of, subclass_of, part_of."
    )
    return [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": prompt},
    ]


def create_ollama_client(host: str, api_key: Optional[str], timeout: int) -> OllamaClient:
    headers = {"Authorization": api_key} if api_key else None
    timeout_value = timeout if timeout and timeout > 0 else None
    return OllamaClient(host=host, timeout=timeout_value, headers=headers)


def call_ollama(
    client: OllamaClient,
    model: str,
    messages: List[Dict[str, str]],
) -> str:
    content = ""
    for part in client.chat(model=model, messages=messages, stream=True):
        chunk = (part.message.content or "") if getattr(part, "message", None) else ""
        if not chunk:
            continue
        if content and chunk.startswith(content):
            chunk = chunk[len(content) :]
        content += chunk
    return content.strip()


def normalise_relation(label: str) -> str:
    cleaned = label.strip().lower().replace(" ", "_")
    cleaned = re.sub(r"[^a-z0-9_]+", "_", cleaned)
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return cleaned or "unspecified"


def parse_llm_response(raw: str, model: str) -> InferenceResult:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"LLM response is not valid JSON: {raw}") from exc
    relation_raw = str(data.get("relation", "")).strip()
    if not relation_raw:
        raise ValueError(f"LLM response missing 'relation': {raw}")
    relation = normalise_relation(relation_raw)
    if relation not in STANDARD_RELATIONS:
        raise ValueError(
            f"LLM response returned unsupported relation '{relation_raw}'."
            f" Expected one of: {', '.join(STANDARD_RELATIONS)}."
        )
    confidence_value = data.get("confidence")
    confidence: Optional[float]
    if isinstance(confidence_value, (int, float)):
        confidence = max(0.0, min(1.0, float(confidence_value)))
    elif isinstance(confidence_value, str):
        try:
            confidence = float(confidence_value)
            confidence = max(0.0, min(1.0, confidence))
        except ValueError:
            confidence = None
    else:
        confidence = None
    rationale = str(data.get("rationale", "")).strip()
    return InferenceResult(
        relation=relation,
        confidence=confidence,
        rationale=rationale,
        raw_response=raw,
        model=model,
    )


def infer_relationship(
    pair: ConceptPair,
    *,
    model: str,
    client: OllamaClient,
    cache: Dict[str, Dict[str, object]],
    refresh: bool,
) -> InferenceResult:
    key = pair.cache_key
    if not refresh and key in cache:
        cached = cache[key]
        cached_relation = normalise_relation(str(cached.get("relation", "")))
        if cached_relation in STANDARD_RELATIONS:
            return InferenceResult(
                relation=cached_relation,
                confidence=cached.get("confidence"),
                rationale=cached.get("rationale", ""),
                raw_response=cached.get("raw_response", ""),
                model=cached.get("model", model),
                cache_hit=True,
            )
        # Drop stale cache entries that do not satisfy the current policy.
        cache.pop(key, None)
    messages = build_messages(pair)
    raw = call_ollama(client, model, messages)
    result = parse_llm_response(raw, model)
    cache[key] = {
        "relation": result.relation,
        "confidence": result.confidence,
        "rationale": result.rationale,
        "raw_response": result.raw_response,
        "model": result.model,
    }
    return result


def write_results(path: Path, rows: Iterable[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "parent_qid",
        "parent_label",
        "child_qid",
        "child_label",
        "relation",
        "confidence",
        "rationale",
        "source_url",
        "target_url",
        "context",
        "model",
        "cache_hit",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=DEFAULT_DATABASE, help="Path to the MathGloss database CSV")
    parser.add_argument("--chicago-dir", type=Path, default=DEFAULT_CHICAGO_DIR, help="Directory containing Chicago markdown files")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="CSV path to write inferred relations")
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE, help="JSON cache file for LLM responses")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Ollama model identifier to use")
    parser.add_argument(
        "--host",
        dest="host",
        default=None,
        help="Base URL for the Ollama service (defaults to env OLLAMA_HOST or cloud endpoint)",
    )
    parser.add_argument("--api-base", dest="host", help=argparse.SUPPRESS)
    parser.add_argument(
        "--api-key",
        default=os.environ.get("OLLAMA_API_KEY"),
        help="API key for Ollama Cloud (env OLLAMA_API_KEY)",
    )
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="HTTP timeout for Ollama requests")
    parser.add_argument("--limit", type=int, default=0, help="Optional limit on the number of links to process")
    parser.add_argument("--refresh", action="store_true", help="Ignore cached responses and query the LLM again")
    parser.add_argument("--log-level", default="INFO", help="Logging level (default: INFO)")
    args = parser.parse_args(argv)
    if not args.host:
        args.host = DEFAULT_HOST
    return args


def main(argv: Optional[List[str]] = None) -> None:
    args = parse_args(argv)
    logging.basicConfig(level=getattr(logging, args.log_level.upper(), logging.INFO), format="%(levelname)s: %(message)s")

    rows, label_lookup = load_database_rows(args.database)
    slug_to_qid = build_chicago_slug_to_qid(rows)
    cache = load_cache(args.cache)

    try:
        client = create_ollama_client(args.host, args.api_key, args.timeout)
    except Exception as exc:  # pragma: no cover - transport setup errors
        raise SystemExit(f"Failed to initialise Ollama client: {exc}") from exc

    pairs_iter = gather_concept_pairs(rows, slug_to_qid, args.chicago_dir, label_lookup)
    if args.limit and args.limit > 0:
        pairs_iter = itertools.islice(pairs_iter, args.limit)

    processed_rows: List[Dict[str, str]] = []
    total = 0
    for pair in pairs_iter:
        total += 1
        try:
            result = infer_relationship(
                pair,
                model=args.model,
                client=client,
                cache=cache,
                refresh=args.refresh,
            )
        except Exception as exc:
            logging.error("Failed to infer relation for %s → %s: %s", pair.source_qid, pair.target_qid or pair.target_slug, exc)
            continue
        processed_rows.append(result.as_row(pair))
        if total % 10 == 0:
            logging.info("Processed %d pairs", total)
    if processed_rows:
        write_results(args.output, processed_rows)
        save_cache(cache, args.cache)
        logging.info("Wrote %d inferred relations to %s", len(processed_rows), args.output)
    else:
        logging.warning("No relations inferred; nothing written")


if __name__ == "__main__":  # pragma: no cover
    main()
