#!/usr/bin/env python3
"""Infer semantic relationships between Chicago-linked concepts via LLM APIs.

This script iterates over every MathGloss entry that includes a Chicago
definition, locates the markdown file for that definition, and inspects the
linked Chicago concepts within the text.  For each (source concept, linked
concept) pair it queries a configurable language model backend (Ollama by
default, with optional support for Mistral's API) to classify their
relationship, choosing from the restricted relation set described in the prompt
(for example, ``instance_of``, ``subclass_of``, ``has_property``, ``has_part`` or
the explicit ``no_relation`` opt-out).

Results are streamed into a CSV for downstream graph loading, while responses
are cached in a JSON sidecar to avoid repeated LLM calls across runs (use
``--no-cache`` to disable).  Existing CSV rows are merged in-place so reruns do
not discard previous results.  Ollama
requests use the official Python client, and Mistral calls use the REST API, so
either backend can be targeted without further code changes.
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
import time
from functools import partial
from dataclasses import dataclass
from pathlib import Path
from string import Template
from typing import Callable, Dict, Iterable, Iterator, List, Optional, Tuple

try:
    from ollama import Client as OllamaClient
    from ollama import RequestError, ResponseError
except ImportError as exc:  # pragma: no cover
    raise SystemExit("The 'ollama' package is required. Install it via 'pip install ollama'.") from exc

try:  # pragma: no cover - lazily used when requests is installed
    import requests
except ImportError as exc:  # pragma: no cover
    requests = None  # type: ignore[assignment]


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

from scripts.graphing.concept_extractor import extract_links


DEFAULT_DATABASE = Path("data/database.csv")
DEFAULT_CHICAGO_DIR = Path("chicago")
DEFAULT_OUTPUT = Path("data/chicago_llm_relations.csv")
DEFAULT_CACHE = Path("data/chicago_relation_cache.json")
DEFAULT_PROVIDER = "ollama"
DEFAULT_OLLAMA_MODEL = "deepseek-v3.1:671b-cloud"
DEFAULT_MISTRAL_MODEL = "mistral-large-latest"
DEFAULT_HOST = os.environ.get("OLLAMA_HOST", os.environ.get("OLLAMA_API_BASE", "https://ollama.com"))
DEFAULT_MISTRAL_BASE = os.environ.get("MISTRAL_API_BASE", "https://api.mistral.ai")
DEFAULT_TIMEOUT = 120
STANDARD_RELATIONS = ("instance_of", "subclass_of", "has_property", "has_part")
LABEL_PATTERN = re.compile(r"\blabel\b\s*[:=]\s*['\"]?([A-Za-z0-9_\- ]+)", re.IGNORECASE)
CONFIDENCE_PATTERN = re.compile(r"\bconfidence\b\s*[:=]\s*([0-9]*\.?[0-9]+)", re.IGNORECASE)


class UsageLimitExceeded(RuntimeError):
    """Raised when the selected LLM service reports a usage limit hit."""

PROMPT_TEMPLATE = Template("""You are an expert classifier of semantic relations in mathematical text.
Your job is to decide how a MAIN concept and a LINKED concept are related,
using only the DEFINITION of the MAIN concept provided.

### Allowed relation labels
- instance_of: MAIN is a single instance/individual of class LINKED.
- subclass_of: Every MAIN is a kind of LINKED (MAIN is a subclass of LINKED).
- has_property: MAIN has the adjectival predicate LINKED (e.g. "abelian", "commutative").
- has_part: LINKED is a constituent part-type of MAIN (e.g. "a Lie algebra has a bracket").
- none: none of the above apply.

### Typing rules
- Type each concept as one of:
  * individual (a specific entity)
  * class (a kind of thing)
  * property (an adjectival predicate)
  * part-type (a constituent part)
  * unknown
- The relation label must match the types:
  * individual → class  ⇒ instance_of
  * class → class       ⇒ subclass_of
  * any → property      ⇒ has_property
  * any → part-type     ⇒ has_part
  * otherwise           ⇒ none

### Output format
Return only valid JSON with this schema:
{"label": "instance_of | subclass_of | has_property | has_part | none",
 "type_main": "individual | class | property | part-type | unknown",
 "type_linked": "individual | class | property | part-type | unknown",
 "evidence_spans": ["quote phrases from DEFINITION that support your choice"],
 "confidence": float between 0.0 and 1.0}

---

### Few-shot examples

Example 1
MAIN: "SL₂(ℝ)"
LINKED: "Lie group"
DEFINITION(main): "SL₂(ℝ) is the group of 2×2 real matrices with determinant 1, forming a Lie group."

Output:
{"label": "instance_of", "type_main": "individual", "type_linked": "class", "evidence_spans": ["forming a Lie group"], "confidence": 0.95}

---

Example 2
MAIN: "Abelian group"
LINKED: "group"
DEFINITION(main): "An abelian group is a group in which the group operation is commutative."

Output:
{"label": "subclass_of", "type_main": "class", "type_linked": "class", "evidence_spans": ["An abelian group is a group"], "confidence": 0.9}

---

Example 3
MAIN: "Abelian group"
LINKED: "commutative"
DEFINITION(main): "An abelian group is a group in which the group operation is commutative."

Output:
{"label": "has_property", "type_main": "class", "type_linked": "property", "evidence_spans": ["operation is commutative"], "confidence": 0.9}

---

Example 4
MAIN: "Lie algebra"
LINKED: "bracket"
DEFINITION(main): "A Lie algebra is a vector space together with a bilinear bracket operation satisfying antisymmetry and the Jacobi identity."

Output:
{"label": "has_part", "type_main": "class", "type_linked": "part-type", "evidence_spans": ["together with a bilinear bracket operation"], "confidence": 0.88}

---

Example 5
MAIN: "Hilbert space"
LINKED: "inner product"
DEFINITION(main): "A Hilbert space is a complete inner product space, meaning it is a vector space with an inner product where every Cauchy sequence converges."

Output:
{"label": "has_part", "type_main": "class", "type_linked": "part-type", "evidence_spans": ["vector space with an inner product"], "confidence": 0.92}

---

Example 6
MAIN: "Lebesgue integral"
LINKED: "measure theory"
DEFINITION(main): "The Lebesgue integral is a method of integration based on measure theory, extending the Riemann integral to a broader class of functions."

Output:
{"label": "none", "type_main": "class", "type_linked": "class", "evidence_spans": ["based on measure theory"], "confidence": 0.6}

---

### Task
MAIN: "${source_label}"
LINKED: "${target_label}"
MAIN_WIKIDATA: ${source_qid}
LINKED_WIKIDATA: ${target_qid}
DEFINITION(main):
""")

PROMPT_SUFFIX = """
Respond with the JSON only, no extra text.
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
    raw_response: str
    model: str
    rationale: Optional[str] = None
    cache_hit: bool = False

    def as_row(self, pair: ConceptPair) -> Dict[str, str]:
        return {
            "parent_qid": pair.source_qid,
            "parent_label": pair.source_label,
            "child_qid": pair.target_qid,
            "child_label": pair.target_label,
            "relation": self.relation,
            "confidence": "" if self.confidence is None else f"{self.confidence:.3f}",
            "source_url": pair.source_url,
            "target_url": pair.target_url,
            "context": pair.context,
            "model": self.model,
            "rationale": self.rationale or "",
            "cache_hit": "yes" if self.cache_hit else "no",
            "raw_response": self.raw_response,
        }


LLMCaller = Callable[[str, List[Dict[str, str]]], str]


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


def row_cache_key(row: Dict[str, str]) -> str:
    """Build a deterministic key for merging repeated rows."""
    parent = (row.get("parent_qid") or "").strip()
    if not parent:
        parent = extract_chicago_slug(row.get("source_url", "") or "") or (row.get("parent_label") or "").strip()
    child = (row.get("child_qid") or "").strip()
    if not child:
        child = extract_chicago_slug(row.get("target_url", "") or "") or (row.get("child_label") or "").strip()
    parent = parent or "unknown_parent"
    child = child or "unknown_child"
    return f"{parent}→{child}"


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
    text = re.sub(r"__([^_]+)__", r"\1", text)
    text = re.sub(r"\[\[!.*?\]\]", " ", text)
    text = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", text)
    def _replace_double_brackets(match):
        inner = match.group(1)
        if not inner:
            return ""
        inner = inner.strip()
        if not inner or inner.startswith("!"):
            return ""
        if "|" in inner:
            return inner.split("|", 1)[1].strip()
        return inner

    text = re.sub(r"\[\[(.*?)\]\]", _replace_double_brackets, text)
    text = re.sub(r"\[([^\]\[]+)\]\]", r"\1", text)
    text = re.sub(r"\+--\s*\{[^}]*\}", " ", text)
    text = re.sub(r"=--", " ", text)
    text = re.sub(r"\{:\s*[^}]*\}", " ", text)
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
    prompt = PROMPT_TEMPLATE.substitute(
        source_label=pair.source_label,
        source_qid=pair.source_qid or "unknown",
        target_label=pair.target_label,
        target_qid=pair.target_qid or "unknown",
    ) + excerpt + "\n\n" + PROMPT_SUFFIX
    system_instruction = (
        "You are a precise ontology assistant. Always return valid JSON with the keys"
        " 'label', 'type_main', 'type_linked', 'evidence_spans', and 'confidence'."
        " The 'label' must be exactly one of: instance_of, subclass_of, has_property,"
        " has_part, none."
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
    try:
        for part in client.chat(model=model, messages=messages, stream=True):
            chunk = (part.message.content or "") if getattr(part, "message", None) else ""
            if not chunk:
                continue
            if content and chunk.startswith(content):
                chunk = chunk[len(content) :]
            content += chunk
    except ResponseError as exc:
        status = getattr(exc, "status_code", None)
        message = str(exc)
        if status == 402 or " 402" in message or message.strip().startswith("402"):
            raise UsageLimitExceeded(message) from exc
        raise
    return content.strip()


def call_mistral(
    session: "requests.Session",
    base_url: str,
    api_key: Optional[str],
    model: str,
    messages: List[Dict[str, str]],
    timeout: int,
) -> str:
    if requests is None:  # pragma: no cover - handled at runtime
        raise SystemExit("The 'requests' package is required for Mistral support. Install it via 'pip install requests'.")
    if not api_key:
        raise SystemExit("A Mistral API key is required (set --api-key or MISTRAL_API_KEY).")
    url = base_url.rstrip("/") + "/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": messages,
        "response_format": {"type": "json_object"},
    }
    timeout_value = timeout if timeout and timeout > 0 else None
    try:
        response = session.post(url, headers=headers, json=payload, timeout=timeout_value)
    except requests.RequestException as exc:  # pragma: no cover - network errors hard to trigger in tests
        raise RuntimeError(f"Mistral request failed: {exc}") from exc
    if response.status_code in {402, 403, 429}:
        raise UsageLimitExceeded(response.text)
    if response.status_code >= 400:
        raise RuntimeError(f"Mistral request failed ({response.status_code}): {response.text}")
    try:
        data = response.json()
    except ValueError as exc:
        raise RuntimeError("Failed to decode Mistral response as JSON") from exc
    choices = data.get("choices") or []
    if not choices:
        raise RuntimeError("Mistral response contained no choices")
    message = choices[0].get("message") or {}
    content = (message.get("content") or "").strip()
    if not content:
        raise RuntimeError("Mistral response contained no message content")
    return content


def normalise_relation(label: str) -> str:
    cleaned = label.strip().lower().replace(" ", "_")
    cleaned = re.sub(r"[^a-z0-9_]+", "_", cleaned)
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return cleaned or "unspecified"


def escape_invalid_backslashes(text: str) -> str:
    """Ensure lone backslashes become valid JSON escapes."""
    # Valid JSON escapes are \", \\, \/, \b, \f, \n, \r, \t, and \uXXXX.
    pattern = re.compile(r"(?<!\\)\\(?![\"\\/bfnrtu])")
    previous = None
    escaped = text
    while previous != escaped and pattern.search(escaped):
        previous = escaped
        escaped = pattern.sub(r"\\\\", escaped)
    return escaped


def coerce_json_object(raw: str) -> str:
    """Trim LLM output to the JSON object we asked for."""
    candidate = raw.strip()
    # Strip leading/trailing quotes that sometimes wrap the payload
    while candidate.startswith(('"', "'")) and not candidate.startswith('{'):
        candidate = candidate[1:].lstrip()
    while candidate.endswith(('"', "'")) and not candidate.endswith('}'):
        candidate = candidate.rstrip().rstrip('"').rstrip("'")
    if candidate.startswith("```"):
        lines = [line for line in candidate.splitlines() if line.strip() != "```" and not line.strip().startswith("```json")]
        candidate = "\n".join(lines).strip()
    first_brace = candidate.find("{")
    last_brace = candidate.rfind("}")
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        candidate = candidate[first_brace : last_brace + 1]
    else:
        candidate = candidate.strip()
        if not candidate.startswith("{"):
            candidate = "{\n" + candidate
        if not candidate.rstrip().endswith("}"):
            candidate = candidate.rstrip() + "\n}"
    return escape_invalid_backslashes(candidate)


def fallback_parse_fields(raw: str) -> Dict[str, object]:
    """Best-effort parser for semi-structured model output."""
    raw = escape_invalid_backslashes(raw)
    result: Dict[str, object] = {}
    label_match = LABEL_PATTERN.search(raw)
    if label_match:
        result["label"] = label_match.group(1).strip()
    confidence_match = CONFIDENCE_PATTERN.search(raw)
    if confidence_match:
        try:
            result["confidence"] = float(confidence_match.group(1))
        except ValueError:
            pass
    return result


def parse_llm_response(raw: str, model: str) -> InferenceResult:
    try:
        payload = coerce_json_object(raw)
        data = json.loads(payload)
    except json.JSONDecodeError:
        data = fallback_parse_fields(raw)
        payload = raw.strip()
        if "label" not in data:
            raise ValueError(f"LLM response is not valid JSON and missing label: {raw}")
    relation_raw = str(data.get("label", "")).strip()
    if not relation_raw:
        raise ValueError(f"LLM response missing 'label': {raw}")
    relation = normalise_relation(relation_raw)
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
    evidence: Optional[str] = None
    evidence_value = data.get("evidence_spans")
    if isinstance(evidence_value, list):
        cleaned = [str(item).strip() for item in evidence_value if str(item).strip()]
        if cleaned:
            evidence = " | ".join(cleaned)
    elif isinstance(evidence_value, str):
        stripped = evidence_value.strip()
        if stripped:
            evidence = stripped

    if relation in {"none", "no_relation"}:
        # Treat as an explicit signal to omit the edge while keeping the response in cache.
        return InferenceResult(
            relation="no_relation",
            confidence=confidence,
            raw_response=payload,
            model=model,
            rationale=evidence,
        )
    if relation not in STANDARD_RELATIONS:
        raise ValueError(
            f"LLM response returned unsupported relation '{relation_raw}'."
            f" Expected one of: {', '.join(STANDARD_RELATIONS + ('none',))}."
        )
    return InferenceResult(
        relation=relation,
        confidence=confidence,
        raw_response=payload,
        model=model,
        rationale=evidence,
    )


def infer_relationship(
    pair: ConceptPair,
    *,
    model: str,
    call_fn: LLMCaller,
    cache: Dict[str, Dict[str, object]],
    refresh: bool,
    use_cache: bool,
) -> InferenceResult:
    key = pair.cache_key
    if use_cache and not refresh and key in cache:
        cached = cache[key]
        cached_model = str(cached.get("model")) if cached.get("model") is not None else None
        if cached_model and cached_model != model:
            cache.pop(key, None)
        else:
            cached_relation = normalise_relation(str(cached.get("relation", "")))
            if cached_relation == "none":
                cached_relation = "no_relation"
            if cached_relation in STANDARD_RELATIONS or cached_relation == "no_relation":
                return InferenceResult(
                    relation=cached_relation,
                    confidence=cached.get("confidence"),
                    raw_response=cached.get("raw_response", ""),
                    model=cached.get("model", model),
                    rationale=cached.get("rationale"),
                    cache_hit=True,
                )
            # Drop stale cache entries that do not satisfy the current policy.
            cache.pop(key, None)
    messages = build_messages(pair)
    raw = call_fn(model, messages)
    try:
        result = parse_llm_response(raw, model)
    except Exception as exc:
        logging.error(
            "Failed to parse response for %s → %s: %s\nRaw output:\n%s",
            pair.source_qid,
            pair.target_qid or pair.target_slug,
            exc,
            raw,
        )
        if use_cache:
            cache.pop(key, None)
        return InferenceResult(
            relation="no_relation",
            confidence=None,
            raw_response=raw,
            model=model,
            rationale=None,
        )
    if use_cache:
        cache[key] = {
            "relation": result.relation,
            "confidence": result.confidence,
            "raw_response": result.raw_response,
            "model": result.model,
            "rationale": result.rationale,
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
        "source_url",
        "target_url",
        "context",
        "model",
        "rationale",
        "cache_hit",
        "raw_response",
    ]
    new_rows = list(rows)
    existing_rows: List[Dict[str, str]] = []
    if path.exists():
        with path.open("r", newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                existing_rows.append(row)
    rows_by_key: Dict[str, Dict[str, str]] = {}
    ordered_keys: List[str] = []
    seen_keys = set()
    for row in existing_rows:
        key = row_cache_key(row)
        rows_by_key[key] = row
        ordered_keys.append(key)
        seen_keys.add(key)
    for row in new_rows:
        key = row_cache_key(row)
        rows_by_key[key] = row
        if key not in seen_keys:
            ordered_keys.append(key)
            seen_keys.add(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for key in ordered_keys:
            writer.writerow(rows_by_key[key])


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=DEFAULT_DATABASE, help="Path to the MathGloss database CSV")
    parser.add_argument("--chicago-dir", type=Path, default=DEFAULT_CHICAGO_DIR, help="Directory containing Chicago markdown files")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="CSV path to write inferred relations")
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE, help="JSON cache file for LLM responses")
    parser.add_argument("--no-cache", action="store_true", help="Disable reading and writing the response cache")
    parser.add_argument("--provider", choices=("ollama", "mistral"), default=DEFAULT_PROVIDER, help="LLM backend to use")
    parser.add_argument("--model", default=None, help="Model identifier for the chosen backend")
    parser.add_argument(
        "--host",
        dest="host",
        default=None,
        help="Base URL for the Ollama service (defaults to env OLLAMA_HOST or cloud endpoint)",
    )
    parser.add_argument("--api-base", dest="host", help=argparse.SUPPRESS)
    parser.add_argument(
        "--api-key",
        default=None,
        help="API key/token for the selected backend (defaults to provider-specific env)",
    )
    parser.add_argument(
        "--mistral-base",
        dest="mistral_base",
        default=None,
        help="Override the base URL for the Mistral API (defaults to https://api.mistral.ai)",
    )
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="HTTP timeout for API requests")
    parser.add_argument("--sleep", type=float, default=0.0, help="Seconds to sleep between uncached LLM calls")
    parser.add_argument("--limit", type=int, default=0, help="Optional limit on the number of links to process")
    parser.add_argument("--refresh", action="store_true", help="Ignore cached responses and query the LLM again")
    parser.add_argument("--log-level", default="INFO", help="Logging level (default: INFO)")
    args = parser.parse_args(argv)
    if args.provider == "ollama":
        if not args.host:
            args.host = DEFAULT_HOST
        if args.api_key is None:
            args.api_key = os.environ.get("OLLAMA_API_KEY")
    else:
        if not args.mistral_base:
            args.mistral_base = DEFAULT_MISTRAL_BASE
        if args.api_key is None:
            args.api_key = os.environ.get("MISTRAL_API_KEY")
    if not args.model:
        args.model = DEFAULT_OLLAMA_MODEL if args.provider == "ollama" else DEFAULT_MISTRAL_MODEL
    args.use_cache = not args.no_cache
    return args


def main(argv: Optional[List[str]] = None) -> None:
    args = parse_args(argv)
    logging.basicConfig(level=getattr(logging, args.log_level.upper(), logging.INFO), format="%(levelname)s: %(message)s")

    rows, label_lookup = load_database_rows(args.database)
    slug_to_qid = build_chicago_slug_to_qid(rows)
    cache = load_cache(args.cache) if args.use_cache else {}

    if args.provider == "ollama":
        try:
            client = create_ollama_client(args.host, args.api_key, args.timeout)
        except Exception as exc:  # pragma: no cover - transport setup errors
            raise SystemExit(f"Failed to initialise Ollama client: {exc}") from exc
        call_fn: LLMCaller = partial(call_ollama, client)
    else:
        if requests is None:  # pragma: no cover - handled in call_mistral but caught earlier for clarity
            raise SystemExit("The 'requests' package is required for Mistral support. Install it via 'pip install requests'.")
        session = requests.Session()
        call_fn = partial(
            call_mistral,
            session,
            args.mistral_base,
            args.api_key,
            timeout=args.timeout,
        )

    pairs_iter = gather_concept_pairs(rows, slug_to_qid, args.chicago_dir, label_lookup)
    if args.limit and args.limit > 0:
        pairs_iter = itertools.islice(pairs_iter, args.limit)

    processed_rows: List[Dict[str, str]] = []
    total = 0
    usage_limit_hit = False
    for pair in pairs_iter:
        total += 1
        try:
            result = infer_relationship(
                pair,
                model=args.model,
                call_fn=call_fn,
                cache=cache,
                refresh=args.refresh,
                use_cache=args.use_cache,
            )
            if args.sleep > 0 and not result.cache_hit:
                time.sleep(args.sleep)
        except UsageLimitExceeded as exc:
            logging.warning(
                "Usage limit reached after %d pairs: %s",
                total - 1,
                exc,
            )
            usage_limit_hit = True
            break
        except Exception:
            logging.exception(
                "Failed to infer relation for %s → %s",
                pair.source_qid,
                pair.target_qid or pair.target_slug,
            )
            continue
        if result.relation == "no_relation":
            logging.debug(
                "Skipping %s → %s because model returned no_relation",
                pair.source_qid,
                pair.target_qid or pair.target_slug,
            )
            if result.raw_response:
                logging.debug("Raw response was:\n%s", result.raw_response)
            continue
        processed_rows.append(result.as_row(pair))
        if total % 10 == 0:
            logging.info("Processed %d pairs", total)
    if processed_rows:
        write_results(args.output, processed_rows)
        if args.use_cache:
            save_cache(cache, args.cache)
        logging.info(
            "Wrote %d inferred relations to %s%s",
            len(processed_rows),
            args.output,
            " (partial run; usage limit reached)" if usage_limit_hit else "",
        )
    else:
        logging.warning("No relations inferred; nothing written")


if __name__ == "__main__":  # pragma: no cover
    main()
