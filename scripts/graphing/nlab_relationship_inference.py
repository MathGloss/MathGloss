#!/usr/bin/env python3
"""Infer semantic relationships between nLab concepts using scraped markdown.

This script mirrors the Chicago relationship pipeline, but operates on the
pre-scraped nLab markdown stored in a JSON file. Each entry in the JSON array
must include the keys ``name`` (nLab title), ``url`` (usually the ``/source/``
view) and ``source`` (the raw markdown content). All internal ``[[link]]``
references are extracted, converted into candidate concept pairs, and analysed
with the same LLM-driven classifier used for the Chicago corpus.

Examples
--------
    python scripts/graphing/nlab_relationship_inference.py \
        --nlab-json secrets/nlab/nlab_scrape.json \
        --database data/database.csv \
        --output data/relations/nlab_llm_relations.csv
"""
from __future__ import annotations

import argparse
import itertools
import json
import logging
import os
import re
import sys
import time
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional, Set, Tuple
from urllib.parse import quote, unquote, urlparse

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

from scripts.graphing.chicago_relationship_inference import (
    ConceptPair,
    UsageLimitExceeded,
    call_mistral,
    call_ollama,
    create_ollama_client,
    infer_relationship,
    load_cache,
    load_database_rows,
    markdown_to_plain,
    save_cache,
    sentence_window,
    write_results,
    DEFAULT_HOST,
    DEFAULT_MISTRAL_BASE,
    DEFAULT_MISTRAL_MODEL,
    DEFAULT_OLLAMA_MODEL,
    DEFAULT_PROVIDER,
    DEFAULT_TIMEOUT,
)

DEFAULT_NLAB_JSON = Path("secrets/nlab/nlab_scrape.json")
DEFAULT_OUTPUT = Path("data/relations/nlab_llm_relations.csv")
DEFAULT_CACHE = Path("data/relations/nlab_relation_cache.json")
DEFAULT_DATABASE = Path("data/database.csv")
NLAB_BASE_URL = "https://ncatlab.org/nlab/show/"


@dataclass(frozen=True)
class NlabLink:
    target: str
    display: str
    start: int
    end: int


def extract_nlab_slug(url: str, *, decode: bool = True) -> Optional[str]:
    if not url:
        return None
    parsed = urlparse(url)
    if parsed.scheme and parsed.netloc:
        path = parsed.path or ""
    else:
        path = url
    path = path.strip()
    prefixes = (
        "/nlab/show/",
        "/nlab/source/",
        "nlab/show/",
        "nlab/source/",
        "show/",
        "source/",
    )
    for prefix in prefixes:
        if path.startswith(prefix):
            path = path[len(prefix):]
            break
    path = path.strip("/")
    if not path:
        return None
    if decode:
        return unquote(path)
    return path


def encode_nlab_slug(value: str) -> str:
    text = value.strip()
    if not text:
        return ""
    encoded = quote(text, safe="/:@")
    return encoded.replace("%20", "+")


def is_nlab_only(row: Dict[str, str]) -> bool:
    other_columns = (
        "BCT Link",
        "Chicago Link",
        "Clowder Link",
        "Context Link",
        "Mathlib Link",
        "PlanetMath Link",
        "Wikipedia Link",
    )
    for column in other_columns:
        value = (row.get(column) or "").strip()
        if value:
            return False
    return True


def build_nlab_slug_to_qid(
    rows: Iterable[Dict[str, str]],
    allowed_qids: Set[str],
) -> Tuple[Dict[str, str], Dict[str, str]]:
    slug_to_qid: Dict[str, str] = {}
    lower_slug_to_qid: Dict[str, str] = {}
    for row in rows:
        qid = (row.get("Wikidata ID") or "").strip()
        if qid not in allowed_qids:
            continue
        link = (row.get("nLab Link") or "").strip()
        if not link:
            continue
        raw_slug = extract_nlab_slug(link, decode=False)
        decoded_slug = extract_nlab_slug(link, decode=True)
        for candidate in {raw_slug, decoded_slug}:
            if candidate and candidate not in slug_to_qid:
                slug_to_qid[candidate] = qid
        if decoded_slug:
            lower = decoded_slug.lower()
            if lower and lower not in lower_slug_to_qid:
                lower_slug_to_qid[lower] = qid
    return slug_to_qid, lower_slug_to_qid


_NLAB_LINK_PATTERN = re.compile(r"\[\[(.+?)\]\]")


def extract_nlab_links(markdown: str) -> List[NlabLink]:
    links: List[NlabLink] = []
    for match in _NLAB_LINK_PATTERN.finditer(markdown):
        inner = match.group(1).strip()
        if not inner or inner.startswith("!"):
            continue
        if inner.lower().startswith("category:"):
            continue
        if "|" in inner:
            target_raw, display = inner.split("|", 1)
        else:
            target_raw, display = inner, inner
        target = target_raw.strip()
        display = display.strip() or target
        if not target or target.startswith("http://") or target.startswith("https://"):
            continue
        if target.startswith(":"):
            # Skip interwiki or file links like ":Category:".
            continue
        links.append(NlabLink(target=target, display=display, start=match.start(), end=match.end()))
    return links


def format_nlab_url(slug_encoded: str) -> str:
    slug = slug_encoded.strip("/")
    return f"{NLAB_BASE_URL}{slug}" if slug else NLAB_BASE_URL.rstrip("/")


def resolve_nlab_qid(
    slug_to_qid: Dict[str, str],
    lower_slug_to_qid: Dict[str, str],
    target: str,
) -> Optional[str]:
    candidates = []
    encoded = encode_nlab_slug(target)
    if encoded:
        candidates.append(encoded)
    candidates.append(target)
    stripped = target.strip("/")
    if stripped and stripped not in candidates:
        candidates.append(stripped)
    dashed = stripped.replace(" ", "-") if stripped else ""
    if dashed and dashed not in candidates:
        candidates.append(dashed)
    for candidate in candidates:
        if candidate in slug_to_qid:
            return slug_to_qid[candidate]
        if candidate.replace(" ", "+") in slug_to_qid:
            return slug_to_qid[candidate.replace(" ", "+")]
    lowered = stripped.lower() if stripped else target.lower()
    return lower_slug_to_qid.get(lowered)


def gather_nlab_pairs(
    pages: Iterable[Dict[str, object]],
    slug_to_qid: Dict[str, str],
    lower_slug_to_qid: Dict[str, str],
    label_lookup: Dict[str, str],
    allowed_qids: Set[str],
    definitions_only: bool = False,
) -> Iterator[ConceptPair]:
    for page in pages:
        raw_markdown = str(page.get("source", ""))
        if not raw_markdown.strip():
            continue
        url = str(page.get("url", ""))
        name = str(page.get("name", ""))
        source_slug_raw = extract_nlab_slug(url, decode=False)
        source_slug_decoded = extract_nlab_slug(url, decode=True)
        source_qid = (
            slug_to_qid.get(source_slug_raw or "")
            or slug_to_qid.get(source_slug_decoded or "")
            or lower_slug_to_qid.get((source_slug_decoded or "").lower())
        )
        if not source_qid or source_qid not in allowed_qids:
            continue
        source_slug_for_pair = (source_slug_raw or encode_nlab_slug(source_slug_decoded or name) or name or "")
        source_url = format_nlab_url(source_slug_for_pair)
        source_label = label_lookup.get(source_qid, name or source_slug_decoded or source_slug_raw or source_slug_for_pair)
        if definitions_only:
            section_marker = "## Definition"
            lower_text = raw_markdown.lower()
            marker_index = lower_text.find(section_marker.lower())
            if marker_index != -1:
                section_text = raw_markdown[marker_index:]
                next_header_index = section_text.find("\n## ", len(section_marker))
                if next_header_index != -1:
                    raw_markdown = section_text[:next_header_index]
                else:
                    raw_markdown = section_text
        links = extract_nlab_links(raw_markdown)
        if not links:
            continue
        fallback_context = markdown_to_plain(raw_markdown[:280])
        for link in links:
            target_text = link.target.strip()
            if not target_text:
                continue
            target_core = target_text.split("#", 1)[0].split("?", 1)[0].strip()
            while target_core.startswith("../"):
                target_core = target_core[3:]
            target_core = target_core.lstrip("./").strip()
            if not target_core:
                continue
            target_slug_encoded = encode_nlab_slug(target_core)
            target_qid = resolve_nlab_qid(slug_to_qid, lower_slug_to_qid, target_core)
            if not target_qid or target_qid not in allowed_qids:
                continue
            if target_slug_encoded and source_slug_for_pair:
                if target_slug_encoded.strip("/").lower() == source_slug_for_pair.strip("/").lower():
                    continue
            if source_qid == target_qid:
                continue
            target_label = label_lookup.get(target_qid, link.display or target_text)
            target_url = format_nlab_url(target_slug_encoded)
            context_markdown = sentence_window(raw_markdown, link.start, link.end)
            context = markdown_to_plain(context_markdown)
            if not context:
                context = fallback_context
            yield ConceptPair(
                source_qid=source_qid or "",
                source_label=source_label,
                source_slug=source_slug_for_pair,
                target_qid=target_qid or "",
                target_label=target_label,
                target_slug=target_slug_encoded or target_text,
                context=context,
                source_url=source_url,
                target_url=target_url,
            )


def parse_pages(path: Path) -> List[Dict[str, object]]:
    if not path.exists():
        raise FileNotFoundError(f"nLab JSON not found: {path}")
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError("Expected a JSON array of page objects")
    return data


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=DEFAULT_DATABASE, help="Path to the MathGloss database CSV")
    parser.add_argument("--nlab-json", type=Path, default=DEFAULT_NLAB_JSON, help="JSON dump of nLab pages")
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
    parser.add_argument("--api-key", default=None, help="API key/token for the selected backend")
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
    parser.add_argument("--definitions-only", action="store_true", help="Restrict context to the Definition section when present")
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
    allowed_qids: Set[str] = set()
    for row in rows:
        qid = (row.get("Wikidata ID") or "").strip()
        if qid and not is_nlab_only(row):
            allowed_qids.add(qid)
    slug_to_qid, lower_slug_to_qid = build_nlab_slug_to_qid(rows, allowed_qids)
    cache = load_cache(args.cache) if args.use_cache else {}

    pages = parse_pages(args.nlab_json)

    if args.provider == "ollama":
        client = create_ollama_client(args.host, args.api_key, args.timeout)
        call_fn = partial(call_ollama, client)
    else:
        import requests  # deferred import to avoid mandatory dependency when unused

        session = requests.Session()
        call_fn = partial(
            call_mistral,
            session,
            args.mistral_base,
            args.api_key,
            timeout=args.timeout,
        )

    pairs_iter = gather_nlab_pairs(
        pages,
        slug_to_qid,
        lower_slug_to_qid,
        label_lookup,
        allowed_qids,
        definitions_only=args.definitions_only,
    )
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
            logging.warning("Usage limit reached after %d pairs: %s", total - 1, exc)
            usage_limit_hit = True
            break
        except Exception:
            logging.exception("Failed to infer relation for %s → %s", pair.source_label, pair.target_label)
            continue
        processed_rows.append(result.as_row(pair))

    if args.use_cache:
        save_cache(cache, args.cache)

    if processed_rows:
        write_results(args.output, processed_rows)
        logging.info("Wrote %d relation rows to %s", len(processed_rows), args.output)
    else:
        logging.info("No relations processed; nothing written.")

    if usage_limit_hit:
        logging.info("Terminated early due to usage limit.")


if __name__ == "__main__":
    main()
