#!/usr/bin/env python3
"""Load harvested Wikidata relations into the MathGloss Neo4j graph.

This script takes the edge list produced by ``fetch_relations.py`` and writes it
into a Neo4j database following the MathGloss v1 graph schema.  Concepts are
stored (or updated) as ``(:Concept {id})`` nodes, while each relation becomes an
``(:Assertion)`` node connected via ``[:SUBJECT]`` and ``[:OBJECT]`` edges.

Example
-------
    python scripts/graphing/load_relations_to_neo4j.py \
        --input data/graph_edges.csv \
        --aura-id abc12345 \
        --user neo4j \
        --password-prompt

The loader is idempotent.  Re-running it will only add missing assertions.
"""
from __future__ import annotations

import argparse
import csv
import getpass
import hashlib
import itertools
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional, Sequence
from urllib.parse import urlparse

try:
    from neo4j import GraphDatabase
except ImportError as exc:  # pragma: no cover
    raise SystemExit("neo4j python driver is required: pip install neo4j") from exc


DEFAULT_INPUT = Path("data/graph_edges.csv")
DEFAULT_BATCH_SIZE = 100
DEFAULT_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
DEFAULT_USER = os.environ.get("NEO4J_USER", "neo4j")
DEFAULT_PASSWORD = os.environ.get("NEO4J_PASSWORD")
DEFAULT_DATABASE = os.environ.get("NEO4J_DATABASE", "neo4j")
DEFAULT_SOURCE_ID = "wikidata"
DEFAULT_SOURCE_NAME = "Wikidata"
DEFAULT_SOURCE_KIND = "kb"
DEFAULT_SOURCE_URL = "https://www.wikidata.org"
PROPERTY_PREDS = {
    "P31": "instance_of",
    "P279": "is_a",
    "P361": "part_of",
    "P460": "said_to_be_the_same_as",
    "P527": "has_part",
    "P138": "named_after",
    "P170": "creator",
    "P1343": "described_by_source",
    "P366": "has_use",
}

CHICAGO_RELATION_PREFIX = "chicago_llm"
NLAB_RELATION_PREFIX = "nlab_llm"


@dataclass
class PreparedRelation:
    source_id: str
    source_label: Optional[str]
    target_id: str
    target_label: Optional[str]
    property_id: str
    property_label: str
    pred: str
    assertion_id: str
    source_name: str
    source_qid: Optional[str]
    target_qid: Optional[str]
    confidence: Optional[float]
    model: Optional[str]

    def to_dict(self) -> Dict[str, Optional[str]]:
        return {
            "source_id": self.source_id,
            "source_label": self.source_label,
            "target_id": self.target_id,
            "target_label": self.target_label,
            "property_id": self.property_id,
            "property_label": self.property_label,
            "pred": self.pred,
            "assertion_id": self.assertion_id,
            "source_name": self.source_name,
            "source_qid": self.source_qid,
            "target_qid": self.target_qid,
            "confidence": self.confidence,
            "model": self.model,
        }


def sanitize_label(value: Optional[str]) -> str:
    if value is None:
        return ""
    value = re.sub(r"\s+", " ", value).strip()
    return value


def slugify(value: str) -> str:
    value = sanitize_label(value)
    if not value:
        return ""
    value = value.lower()
    value = re.sub(r"[^0-9a-z]+", "_", value)
    return value.strip("_")


def slug_from_url(url: Optional[str]) -> Optional[str]:
    if not url:
        return None
    parsed = urlparse(url)
    path = (parsed.path or "").rstrip("/")
    if not path:
        return None
    slug = path.rpartition("/")[2].strip()
    return slug or None


def chicago_identifier(qid: Optional[str], label: Optional[str], url: Optional[str]) -> Optional[str]:
    qid = (qid or "").strip()
    if qid:
        return qid
    slug = slug_from_url(url)
    if slug:
        return f"chicago:{slug}"
    slug = slugify(label or "")
    if slug:
        return f"chicago:{slug}"
    return None


def normalize_chicago_row(row: Dict[str, str]) -> Optional[Dict[str, str]]:
    relation = sanitize_label(row.get("relation"))
    if not relation or relation.lower() in {"none", "no_relation"}:
        return None
    source_label = sanitize_label(row.get("parent_label")) or None
    target_label = sanitize_label(row.get("child_label")) or None
    source_id = chicago_identifier(row.get("parent_qid"), source_label, row.get("source_url"))
    target_id = chicago_identifier(row.get("child_qid"), target_label, row.get("target_url"))
    if not source_id or not target_id:
        return None
    normalized: Dict[str, str] = {
        "source_id": source_id,
        "source_label": source_label or "",
        "target_id": target_id,
        "target_label": target_label or "",
        "property_id": f"{CHICAGO_RELATION_PREFIX}:{relation}",
        "property_label": relation,
    }
    confidence = row.get("confidence")
    if confidence is not None:
        text = str(confidence).strip()
        if text:
            normalized["confidence"] = text
    model = row.get("model")
    if model is not None:
        text = str(model).strip()
        if text:
            normalized["model"] = text
    return normalized


def nlab_identifier(qid: Optional[str], label: Optional[str], url: Optional[str]) -> Optional[str]:
    qid = (qid or "").strip()
    if qid:
        return qid
    slug = slug_from_url(url)
    if slug:
        return f"nlab:{slug}"
    slug = slugify(label or "")
    if slug:
        return f"nlab:{slug}"
    return None


def normalize_nlab_row(row: Dict[str, str]) -> Optional[Dict[str, str]]:
    relation = sanitize_label(row.get("relation"))
    if not relation or relation.lower() in {"none", "no_relation"}:
        return None
    source_label = sanitize_label(row.get("parent_label")) or None
    target_label = sanitize_label(row.get("child_label")) or None
    source_id = nlab_identifier(row.get("parent_qid"), source_label, row.get("source_url"))
    target_id = nlab_identifier(row.get("child_qid"), target_label, row.get("target_url"))
    if not source_id or not target_id:
        return None
    normalized: Dict[str, str] = {
        "source_id": source_id,
        "source_label": source_label or "",
        "target_id": target_id,
        "target_label": target_label or "",
        "property_id": f"{NLAB_RELATION_PREFIX}:{relation}",
        "property_label": relation,
    }
    confidence = row.get("confidence")
    if confidence is not None:
        text = str(confidence).strip()
        if text:
            normalized["confidence"] = text
    model = row.get("model")
    if model is not None:
        text = str(model).strip()
        if text:
            normalized["model"] = text
    return normalized


def to_predicate(property_id: str, property_label: str) -> str:
    if property_id in PROPERTY_PREDS:
        return PROPERTY_PREDS[property_id]
    label = sanitize_label(property_label or property_id)
    label = label.lower()
    label = re.sub(r"[^0-9a-z]+", "_", label)
    label = re.sub(r"_+", "_", label).strip("_")
    return label or property_id.lower()


def maybe_qid(value: str) -> Optional[str]:
    value = value.strip()
    return value if value.startswith("Q") else None


def assertion_id(dataset: str, source_id: str, property_id: str, target_id: str) -> str:
    digest = hashlib.sha1()
    digest.update(dataset.encode("utf-8"))
    digest.update(b"|")
    digest.update(source_id.encode("utf-8"))
    digest.update(b"|")
    digest.update(property_id.encode("utf-8"))
    digest.update(b"|")
    digest.update(target_id.encode("utf-8"))
    return digest.hexdigest()


def prepare_relation(row: Dict[str, str], source_name: str) -> Optional[PreparedRelation]:
    source_id = row.get("source_id", "").strip()
    target_id = row.get("target_id", "").strip()
    property_id = row.get("property_id", "").strip()
    if not source_id or not target_id or not property_id:
        return None
    source_label = sanitize_label(row.get("source_label", "")) or None
    target_label = sanitize_label(row.get("target_label", "")) or None
    property_label = sanitize_label(row.get("property_label", "")) or property_id
    lower_pid = property_id.lower()
    lower_label = property_label.lower()
    if lower_pid == "no_relation" or lower_label == "no_relation" or lower_pid.endswith(":no_relation"):
        return None
    pred = to_predicate(property_id, property_label)
    confidence_value = row.get("confidence")
    confidence: Optional[float]
    if confidence_value is None:
        confidence = None
    else:
        if isinstance(confidence_value, (int, float)):
            confidence = float(confidence_value)
        else:
            text = str(confidence_value).strip()
            if not text:
                confidence = None
            else:
                try:
                    confidence = float(text)
                except ValueError:
                    confidence = None
    model_value = row.get("model")
    model: Optional[str]
    if model_value is None:
        model = None
    else:
        model_str = str(model_value).strip()
        model = model_str or None
    dataset = source_name or ""
    return PreparedRelation(
        source_id=source_id,
        source_label=source_label,
        target_id=target_id,
        target_label=target_label,
        property_id=property_id,
        property_label=property_label,
        pred=pred,
        assertion_id=assertion_id(dataset, source_id, property_id, target_id),
        source_name=source_name,
        source_qid=maybe_qid(source_id),
        target_qid=maybe_qid(target_id),
        confidence=confidence,
        model=model,
    )


def iter_relations(path: Path, source_name: str) -> Iterator[PreparedRelation]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = set(reader.fieldnames or [])
        if not fieldnames:
            return
        canonical_required = {"source_id", "target_id", "property_id"}
        chicago_required = {"relation", "parent_label", "child_label"}

        if canonical_required.issubset(fieldnames):
            for raw in reader:
                prepared = prepare_relation(raw, source_name)
                if prepared is not None:
                    yield prepared
            return

        if chicago_required.issubset(fieldnames):
            for raw in reader:
                source_url = raw.get("source_url", "")
                if "ncatlab.org" in source_url:
                    normalized = normalize_nlab_row(raw)
                else:
                    normalized = normalize_chicago_row(raw)
                if normalized is None:
                    continue
                prepared = prepare_relation(normalized, source_name)
                if prepared is not None:
                    yield prepared
            return

        else:
            raise ValueError(
                f"Unrecognised columns in {path}. Expected {sorted(canonical_required)} or chicago_llm schema."
            )


def batched(iterable: Iterable[PreparedRelation], size: int) -> Iterator[List[PreparedRelation]]:
    batch: List[PreparedRelation] = []
    for item in iterable:
        batch.append(item)
        if len(batch) >= size:
            yield batch
            batch = []
    if batch:
        yield batch


def ensure_source_node(session, *, source_id: str, name: str, kind: Optional[str], url_root: Optional[str]) -> None:
    def _tx(tx):
        tx.run(
            """
            MERGE (s:Source {id: $id})
            ON CREATE SET s.name = $name, s.kind = $kind, s.url_root = $url_root
            SET s.name = coalesce(s.name, $name)
            SET s.kind = coalesce(s.kind, $kind)
            SET s.url_root = coalesce(s.url_root, $url_root)
            """,
            id=source_id,
            name=name,
            kind=kind,
            url_root=url_root,
        )

    session.execute_write(_tx)


def write_batch(session, batch: Sequence[PreparedRelation], *, allow_create_concepts: bool) -> None:
    payload = [item.to_dict() for item in batch]

    if allow_create_concepts:

        def _tx(tx):
            tx.run(
                """
                UNWIND $batch AS row
                MERGE (src:Concept {id: row.source_id})
                FOREACH (_ IN CASE WHEN row.source_qid IS NULL THEN [] ELSE [1] END | SET src.qid = coalesce(src.qid, row.source_qid))
                FOREACH (_ IN CASE WHEN row.source_label IS NULL THEN [] ELSE [1] END | SET src.label = coalesce(src.label, row.source_label))
                MERGE (tgt:Concept {id: row.target_id})
                FOREACH (_ IN CASE WHEN row.target_qid IS NULL THEN [] ELSE [1] END | SET tgt.qid = coalesce(tgt.qid, row.target_qid))
                FOREACH (_ IN CASE WHEN row.target_label IS NULL THEN [] ELSE [1] END | SET tgt.label = coalesce(tgt.label, row.target_label))
                MERGE (a:Assertion {id: row.assertion_id})
                ON CREATE SET a.pred = row.pred,
                              a.property_id = row.property_id,
                              a.property_label = row.property_label,
                              a.source_name = row.source_name
                FOREACH (_ IN CASE WHEN a.pred IS NULL THEN [1] ELSE [] END | SET a.pred = row.pred)
                FOREACH (_ IN CASE WHEN a.property_id IS NULL THEN [1] ELSE [] END | SET a.property_id = row.property_id)
                FOREACH (_ IN CASE WHEN a.property_label IS NULL THEN [1] ELSE [] END | SET a.property_label = row.property_label)
                FOREACH (_ IN CASE WHEN a.source_name IS NULL THEN [1] ELSE [] END | SET a.source_name = row.source_name)
                FOREACH (_ IN CASE WHEN row.confidence IS NULL THEN [] ELSE [1] END | SET a.confidence = row.confidence)
                FOREACH (_ IN CASE WHEN row.model IS NULL THEN [] ELSE [1] END | SET a.model = row.model)
                MERGE (a)-[:SUBJECT]->(src)
                MERGE (a)-[:OBJECT]->(tgt)
                """,
                batch=payload,
            )

        session.execute_write(_tx)
        return

    def _tx(tx):
        tx.run(
            """
            UNWIND $batch AS row
            MATCH (src:Concept {id: row.source_id})
            MATCH (tgt:Concept {id: row.target_id})
            MERGE (a:Assertion {id: row.assertion_id})
            ON CREATE SET a.pred = row.pred,
                          a.property_id = row.property_id,
                          a.property_label = row.property_label,
                          a.source_name = row.source_name
            FOREACH (_ IN CASE WHEN a.pred IS NULL THEN [1] ELSE [] END | SET a.pred = row.pred)
            FOREACH (_ IN CASE WHEN a.property_id IS NULL THEN [1] ELSE [] END | SET a.property_id = row.property_id)
            FOREACH (_ IN CASE WHEN a.property_label IS NULL THEN [1] ELSE [] END | SET a.property_label = row.property_label)
            FOREACH (_ IN CASE WHEN a.source_name IS NULL THEN [1] ELSE [] END | SET a.source_name = row.source_name)
            FOREACH (_ IN CASE WHEN row.confidence IS NULL THEN [] ELSE [1] END | SET a.confidence = row.confidence)
            FOREACH (_ IN CASE WHEN row.model IS NULL THEN [] ELSE [1] END | SET a.model = row.model)
            MERGE (a)-[:SUBJECT]->(src)
            MERGE (a)-[:OBJECT]->(tgt)
            """,
            batch=payload,
        )

    session.execute_write(_tx)


def count_rows(path: Path) -> int:
    with path.open(encoding="utf-8") as handle:
        return max(sum(1 for _ in handle) - 1, 0)


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="CSV file produced by fetch_relations.py")
    parser.add_argument("--uri", default=DEFAULT_URI, help="Neo4j URI, e.g. bolt://localhost:7687 or neo4j+s://<id>.databases.neo4j.io")
    parser.add_argument("--aura-id", help="Neo4j Aura database ID; overrides --uri")
    parser.add_argument("--user", default=DEFAULT_USER, help="Neo4j username")
    parser.add_argument("--password", default=DEFAULT_PASSWORD, help="Neo4j password")
    parser.add_argument("--database", default=DEFAULT_DATABASE, help="Neo4j database name")
    parser.add_argument("--password-prompt", action="store_true", help="Prompt for the Neo4j password interactively")
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE, help="rows per write transaction")
    parser.add_argument("--source-id", default=DEFAULT_SOURCE_ID, help="Source.id to use for provenance")
    parser.add_argument("--source-name", default=DEFAULT_SOURCE_NAME, help="Display name for the Source node")
    parser.add_argument("--source-kind", default=DEFAULT_SOURCE_KIND, help="kind attribute for the Source node")
    parser.add_argument("--source-url", default=DEFAULT_SOURCE_URL, help="url_root for the Source node")
    parser.add_argument("--skip-source-merge", action="store_true", help="do not create/update the Source node")
    parser.add_argument("--match-existing", action="store_true", help="only attach relations when Concept nodes already exist")
    parser.add_argument("--dry-run", action="store_true", help="preview the first batch instead of writing")
    parser.add_argument("--no-progress", action="store_true", help="suppress progress output")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)

    if not args.input.is_file():
        raise SystemExit(f"Input CSV not found: {args.input}")
    if args.batch_size <= 0:
        raise SystemExit("batch size must be positive")

    if args.aura_id:
        args.uri = f"neo4j+s://{args.aura_id}.databases.neo4j.io"

    if args.dry_run:
        preview_batch = list(itertools.islice(iter_relations(args.input, args.source_name or args.source_id), args.batch_size))
        if not preview_batch:
            print("No rows to ingest")
            return 0
        print("Preview batch:")
        for item in preview_batch:
            print(item)
        print("Cypher writes (simplified):")
        if args.match_existing:
            print("MATCH (:Concept {id}) … ; MERGE (:Assertion {id}) … ;")
        else:
            print("MERGE (:Concept {id}) … ; MERGE (:Assertion {id}) … ;")
        return 0

    if args.password_prompt and not args.password:
        args.password = getpass.getpass("Neo4j password: ")

    if not args.password:
        raise SystemExit("Neo4j password not provided. Use --password or --password-prompt.")

        if not preview_batch:
            print("No rows to ingest")
            return 0
        print("Preview batch:")
        for item in preview_batch:
            print(item)
        print("Cypher writes (simplified):")
        print(
            "MERGE (:Concept {id}) … ; MERGE (:Assertion {id}) … ;"
        )
        return 0

    relations_iter = iter_relations(args.input, args.source_name or args.source_id)

    total_rows = None if args.no_progress else count_rows(args.input)
    processed = 0

    driver = GraphDatabase.driver(args.uri, auth=(args.user, args.password))
    with driver.session(database=args.database) as session:
        if not args.skip_source_merge:
            ensure_source_node(
                session,
                source_id=args.source_id,
                name=args.source_name,
                kind=args.source_kind,
                url_root=args.source_url,
            )
        for batch in batched(relations_iter, args.batch_size):
            if not batch:
                continue
            write_batch(session, batch, allow_create_concepts=not args.match_existing)
            processed += len(batch)
            if not args.no_progress:
                if total_rows:
                    print(f"Ingested {processed}/{total_rows} rows", flush=True)
                else:
                    print(f"Ingested {processed} rows", flush=True)
    driver.close()
    print(f"Finished ingestion: {processed} rows processed")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
