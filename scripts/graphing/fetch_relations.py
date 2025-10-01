#!/usr/bin/env python3
"""Fetch Wikidata relations for concepts included in the pruned MathGloss database.

The script loads every QID from the compiled, pruned database CSV and issues
batched SPARQL queries to wikidata.org in order to discover direct (wdt:)
relations where both the subject and the object appear in the database.  The
resulting edge list is written to a CSV that can be consumed by downstream
visualisation or analysis tools.

Example
-------
    python scripts/graphing/fetch_relations.py \
        --input data/database_compiled_pruned.csv \
        --output data/graph_edges.csv

The script respects Wikidata's usage policy by defaulting to one request per
second and by allowing callers to customise the user agent string.
"""
from __future__ import annotations

import argparse
import csv
import sys
import time
from collections import OrderedDict
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Sequence, Tuple
import hashlib
import json

try:
    import requests
except ImportError as exc:  # pragma: no cover
    raise SystemExit("requests is required to run this script") from exc


DEFAULT_ENDPOINT = "https://query.wikidata.org/sparql"
DEFAULT_USER_AGENT = "MathGlossRelationFetcher/0.1 (+https://mathgloss.github.io)"
DEFAULT_INPUT = Path("data/database_compiled_pruned.csv")
DEFAULT_OUTPUT = Path("data/graph_edges.csv")
DEFAULT_SOURCE_CHUNK = 40
DEFAULT_TARGET_CHUNK = 200
DEFAULT_TIMEOUT = 60
DEFAULT_SLEEP = 0.1
MAX_RETRIES = 5
RETRY_BACKOFF = 2.0


def chunked(items: Sequence[str], size: int) -> Iterator[Sequence[str]]:
    """Yield fixed-size slices from *items* without copying when possible."""
    if size <= 0:
        raise ValueError("chunk size must be positive")
    for start in range(0, len(items), size):
        yield items[start:start + size]


def read_qids(path: Path) -> List[str]:
    """Extract and deduplicate QIDs from the input CSV."""
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or "Wikidata ID" not in reader.fieldnames:
            raise ValueError("input CSV must include a 'Wikidata ID' column")
        qids = [row["Wikidata ID"].strip() for row in reader if row.get("Wikidata ID", "").strip()]
    # Preserve deterministic ordering so that chunking is repeatable.
    seen: OrderedDict[str, None] = OrderedDict((qid, None) for qid in qids)
    return list(seen.keys())


def build_query(sources: Sequence[str], targets: Sequence[str]) -> str:
    """Construct a SPARQL query that discovers direct edges between *sources* and *targets*."""
    source_values = " ".join(f"wd:{qid}" for qid in sources)
    target_values = " ".join(f"wd:{qid}" for qid in targets)
    return f"""
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX bd: <http://www.bigdata.com/rdf#>

SELECT DISTINCT ?source ?sourceLabel ?property ?propertyLabel ?target ?targetLabel WHERE {{
  VALUES ?source {{ {source_values} }}
  VALUES ?target {{ {target_values} }}
  ?source ?prop ?target .
  ?property wikibase:directClaim ?prop .
  FILTER (?source != ?target)
  SERVICE wikibase:label {{
    bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" .
  }}
}}
"""


def perform_request(
    endpoint: str,
    query: str,
    user_agent: str,
    timeout: int,
    sleep_seconds: float,
) -> Dict:
    """Execute the SPARQL query with retries and respectful throttling."""
    headers = {
        "Accept": "application/sparql-results+json",
        "User-Agent": user_agent,
    }
    last_error: Exception | None = None
    for attempt in range(1, MAX_RETRIES + 1):
        if sleep_seconds > 0 and attempt > 1:
            time.sleep(sleep_seconds)
        try:
            response = requests.post(
                endpoint,
                data={"query": query},
                headers=headers,
                timeout=timeout,
            )
            if response.status_code == 429:
                raise requests.HTTPError("Rate limited", response=response)
            response.raise_for_status()
            payload = response.json()
            if sleep_seconds > 0:
                time.sleep(sleep_seconds)
            return payload
        except requests.RequestException as exc:  # pragma: no cover - network dependent
            if attempt == MAX_RETRIES:
                raise
            wait_for = RETRY_BACKOFF ** attempt
            time.sleep(wait_for)
            last_error = exc
    raise SystemExit(f"Failed to fetch data after {MAX_RETRIES} attempts: {last_error}")


def parse_bindings(bindings: Iterable[Dict]) -> List[Tuple[str, str, str, str, str, str]]:
    """Convert SPARQL bindings to a normalized edge list tuple."""
    edges: List[Tuple[str, str, str, str, str, str]] = []
    for binding in bindings:
        source = binding["source"]["value"].rpartition("/")[2]
        target = binding["target"]["value"].rpartition("/")[2]
        prop = binding["property"]["value"].rpartition("/")[2]
        source_label = binding.get("sourceLabel", {}).get("value", "")
        target_label = binding.get("targetLabel", {}).get("value", "")
        prop_label = binding.get("propertyLabel", {}).get("value", "")
        edges.append((source, source_label, prop, prop_label, target, target_label))
    return edges


def fetch_relations(
    qids: Sequence[str],
    endpoint: str,
    user_agent: str,
    source_chunk: int,
    target_chunk: int,
    timeout: int,
    sleep_seconds: float,
    progress: bool,
    cache_dir: Path | None,
) -> List[Tuple[str, str, str, str, str, str]]:
    """Gather every direct relation between members of *qids*."""
    edges: Dict[Tuple[str, str, str], Tuple[str, str, str, str, str, str]] = {}
    source_chunks = list(chunked(qids, source_chunk))
    target_chunks = list(chunked(qids, target_chunk))
    total_queries = len(source_chunks) * len(target_chunks)
    queries_done = 0
    if cache_dir is not None:
        cache_dir.mkdir(parents=True, exist_ok=True)
    for src_idx, sources in enumerate(source_chunks, start=1):
        for targets in target_chunks:
            cache_payload: Dict | None = None
            cache_key = None
            cache_path: Path | None = None
            if cache_dir is not None:
                digest = hashlib.sha1()
                digest.update("|".join(sources).encode("utf-8"))
                digest.update(b"||")
                digest.update("|".join(targets).encode("utf-8"))
                cache_key = digest.hexdigest()
                cache_path = cache_dir / f"{cache_key}.json"
                if cache_path.exists():
                    try:
                        cache_payload = json.loads(cache_path.read_text(encoding="utf-8"))
                    except json.JSONDecodeError:
                        cache_payload = None
            query = build_query(sources, targets)
            if cache_payload is None:
                payload = perform_request(
                    endpoint=endpoint,
                    query=query,
                    user_agent=user_agent,
                    timeout=timeout,
                    sleep_seconds=sleep_seconds,
                )
                if cache_path is not None:
                    cache_path.write_text(json.dumps(payload), encoding="utf-8")
            else:
                payload = cache_payload
            bindings = payload.get("results", {}).get("bindings", [])
            for edge in parse_bindings(bindings):
                key = (edge[0], edge[2], edge[4])
                edges[key] = edge
            queries_done += 1
        if progress:
            status = (
                f"Processed source chunk {src_idx}/{len(source_chunks)}; "
                f"queries {queries_done}/{total_queries}; edges found {len(edges)}"
            )
            print(status, flush=True)
    return list(edges.values())


def write_edges(output_path: Path, edges: Sequence[Tuple[str, str, str, str, str, str]]) -> None:
    """Persist the edge list as CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "source_id",
            "source_label",
            "property_id",
            "property_label",
            "target_id",
            "target_label",
        ])
        writer.writerows(edges)


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="path to the pruned database CSV")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="path for the resulting edge CSV")
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT, help="SPARQL endpoint URL")
    parser.add_argument("--user-agent", default=DEFAULT_USER_AGENT, help="User-Agent header for requests")
    parser.add_argument("--source-chunk", type=int, default=DEFAULT_SOURCE_CHUNK, help="number of QIDs per subject batch")
    parser.add_argument("--target-chunk", type=int, default=DEFAULT_TARGET_CHUNK, help="number of QIDs per object batch")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="HTTP timeout for a single request")
    parser.add_argument("--sleep", type=float, default=DEFAULT_SLEEP, help="seconds to sleep before each request (throttling)")
    parser.add_argument("--dry-run", action="store_true", help="print the first query and exit (useful for debugging)")
    parser.add_argument("--no-progress", action="store_true", help="suppress progress updates")
    parser.add_argument("--cache-dir", type=Path, help="optional directory for caching per-query results")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)

    if not args.input.is_file():
        raise SystemExit(f"Input CSV not found: {args.input}")

    qids = read_qids(args.input)
    if not qids:
        raise SystemExit("No QIDs found in the input CSV")

    if args.dry_run:
        preview_query = build_query(
            qids[: min(len(qids), args.source_chunk)],
            qids[: min(len(qids), args.target_chunk)],
        )
        print(preview_query)
        return 0

    edges = fetch_relations(
        qids=qids,
        endpoint=args.endpoint,
        user_agent=args.user_agent,
        source_chunk=args.source_chunk,
        target_chunk=args.target_chunk,
        timeout=args.timeout,
        sleep_seconds=args.sleep,
        progress=not args.no_progress,
        cache_dir=args.cache_dir,
    )

    write_edges(args.output, edges)
    print(f"Wrote {len(edges)} edges to {args.output}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
