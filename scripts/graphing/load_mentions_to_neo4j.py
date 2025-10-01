#!/usr/bin/env python3
"""Load MathGloss concept and mention nodes into Neo4j."""

from __future__ import annotations

import argparse
import csv
import getpass
import hashlib
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Sequence, Tuple

try:
    from neo4j import GraphDatabase
except ImportError as exc:  # pragma: no cover
    raise SystemExit("neo4j python driver is required: pip install neo4j") from exc


DEFAULT_INPUT = Path("data/database.csv")
DEFAULT_BATCH_SIZE = 200
DEFAULT_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
DEFAULT_USER = os.environ.get("NEO4J_USER", "neo4j")
DEFAULT_PASSWORD = os.environ.get("NEO4J_PASSWORD")
DEFAULT_DATABASE = os.environ.get("NEO4J_DATABASE", "neo4j")


@dataclass(frozen=True)
class SourceConfig:
    base: str
    source_id: str
    name_key: str
    link_key: str
    source_name: str
    source_kind: Optional[str]
    source_url: Optional[str]


SOURCE_CONFIGS: Tuple[SourceConfig, ...] = (
    SourceConfig(
        base="BCT",
        source_id="bct",
        name_key="BCT Name",
        link_key="BCT Link",
        source_name="Basic Category Theory",
        source_kind="book",
        source_url="https://emilyriehl.github.io/files/context.pdf",
    ),
    SourceConfig(
        base="Chicago",
        source_id="chicago",
        name_key="Chicago Name",
        link_key="Chicago Link",
        source_name="Chicago Notes",
        source_kind="notes",
        source_url="https://mathgloss.github.io/MathGloss/chicago",
    ),
    SourceConfig(
        base="Clowder",
        source_id="clowder",
        name_key="Clowder Name",
        link_key="Clowder Link",
        source_name="Clowder",
        source_kind="notes",
        source_url=None,
    ),
    SourceConfig(
        base="Context",
        source_id="context",
        name_key="Context Name",
        link_key="Context Link",
        source_name="Category Theory in Context",
        source_kind="book",
        source_url="https://emilyriehl.github.io/files/context.pdf",
    ),
    SourceConfig(
        base="Mathlib",
        source_id="mathlib",
        name_key="Mathlib Name",
        link_key="Mathlib Link",
        source_name="Mathlib",
        source_kind="formal",
        source_url="https://leanprover-community.github.io/mathlib4_docs",
    ),
    SourceConfig(
        base="nLab",
        source_id="nlab",
        name_key="nLab Name",
        link_key="nLab Link",
        source_name="nLab",
        source_kind="wiki",
        source_url="https://ncatlab.org/nlab",
    ),
    SourceConfig(
        base="PlanetMath",
        source_id="planetmath",
        name_key="PlanetMath Name",
        link_key="PlanetMath Link",
        source_name="PlanetMath",
        source_kind="wiki",
        source_url="https://planetmath.org",
    ),
)


@dataclass(frozen=True)
class ConceptMention:
    concept_id: str
    concept_label: Optional[str]
    mention_id: str
    mention_label: Optional[str]
    mention_url: Optional[str]
    source_id: str
    source_name: str
    source_kind: Optional[str]
    source_url: Optional[str]

    def to_dict(self) -> Dict[str, Optional[str]]:
        return {
            "concept_id": self.concept_id,
            "concept_label": self.concept_label,
            "mention_id": self.mention_id,
            "mention_label": self.mention_label,
            "mention_url": self.mention_url,
            "source_id": self.source_id,
            "source_name": self.source_name,
            "source_kind": self.source_kind,
            "source_url": self.source_url,
        }


def clean_text(value: Optional[str]) -> str:
    if not value:
        return ""
    return " ".join(value.strip().split())


def mention_identifier(concept_id: str, source_id: str, url: Optional[str], label: Optional[str]) -> str:
    digest = hashlib.sha1()
    digest.update(concept_id.encode("utf-8"))
    digest.update(b"|")
    digest.update(source_id.encode("utf-8"))
    digest.update(b"|")
    digest.update((url or "").encode("utf-8"))
    digest.update(b"|")
    digest.update((label or "").encode("utf-8"))
    token = digest.hexdigest()[:20]
    return f"{source_id}:{token}"


def read_mentions(path: Path) -> List[ConceptMention]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        if "Wikidata ID" not in fieldnames:
            raise SystemExit("input CSV must include a 'Wikidata ID' column")
        configs = [cfg for cfg in SOURCE_CONFIGS if cfg.name_key in fieldnames or cfg.link_key in fieldnames]
        mentions: List[ConceptMention] = []
        for row in reader:
            concept_id = clean_text(row.get("Wikidata ID"))
            if not concept_id:
                continue
            concept_label = clean_text(row.get("Wikidata Label")) or None
            for cfg in configs:
                name_value = clean_text(row.get(cfg.name_key))
                link_value = (row.get(cfg.link_key) or "").strip()
                if not name_value and not link_value:
                    continue
                mention_id = mention_identifier(concept_id, cfg.source_id, link_value, name_value)
                mentions.append(
                    ConceptMention(
                        concept_id=concept_id,
                        concept_label=concept_label,
                        mention_id=mention_id,
                        mention_label=name_value or None,
                        mention_url=link_value or None,
                        source_id=cfg.source_id,
                        source_name=cfg.source_name,
                        source_kind=cfg.source_kind,
                        source_url=cfg.source_url,
                    )
                )
        return mentions


def batched(items: Sequence[ConceptMention], size: int) -> Iterator[Sequence[ConceptMention]]:
    if size <= 0:
        raise ValueError("batch size must be positive")
    for start in range(0, len(items), size):
        yield items[start:start + size]


def ensure_source_nodes(session, configs: Sequence[SourceConfig]) -> None:
    payload = [
        {
            "id": cfg.source_id,
            "name": cfg.source_name,
            "kind": cfg.source_kind,
            "url_root": cfg.source_url,
        }
        for cfg in configs
    ]

    def _tx(tx):
        tx.run(
            """
            UNWIND $sources AS source
            MERGE (s:Source {id: source.id})
            FOREACH (_ IN CASE WHEN s.name IS NULL THEN [1] ELSE [] END | SET s.name = source.name)
            FOREACH (_ IN CASE WHEN s.kind IS NULL THEN [1] ELSE [] END | SET s.kind = source.kind)
            FOREACH (_ IN CASE WHEN s.url_root IS NULL THEN [1] ELSE [] END | SET s.url_root = source.url_root)
            """,
            sources=payload,
        )

    session.execute_write(_tx)


def write_batch(session, rows: Sequence[ConceptMention]) -> None:
    payload = [row.to_dict() for row in rows]

    def _tx(tx):
        tx.run(
            """
            UNWIND $rows AS row
            MATCH (source:Source {id: row.source_id})
            MERGE (concept:Concept {id: row.concept_id})
            FOREACH (_ IN CASE WHEN concept.qid IS NULL THEN [1] ELSE [] END | SET concept.qid = row.concept_id)
            FOREACH (_ IN CASE WHEN row.concept_label IS NULL THEN [] ELSE [1] END | SET concept.label = coalesce(concept.label, row.concept_label))
            WITH row, source, concept
            MERGE (mention:Mention {id: row.mention_id})
            SET mention.source_id = row.source_id
            FOREACH (_ IN CASE WHEN row.mention_label IS NULL THEN [] ELSE [1] END | SET mention.label = row.mention_label)
            FOREACH (_ IN CASE WHEN row.mention_url IS NULL THEN [] ELSE [1] END | SET mention.url = row.mention_url)
            FOREACH (_ IN CASE WHEN row.source_name IS NULL THEN [] ELSE [1] END | SET mention.source_name = row.source_name)
            FOREACH (_ IN CASE WHEN row.source_kind IS NULL THEN [] ELSE [1] END | SET mention.source_kind = row.source_kind)
            FOREACH (_ IN CASE WHEN row.source_url IS NULL THEN [] ELSE [1] END | SET mention.source_url = row.source_url)
            MERGE (concept)-[hm:HAS_MENTION {source_id: row.source_id}]->(mention)
            FOREACH (_ IN CASE WHEN row.mention_label IS NULL THEN [] ELSE [1] END | SET hm.label = row.mention_label)
            MERGE (mention)-[:FROM_SOURCE]->(source)
            """,
            rows=payload,
        )

    session.execute_write(_tx)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Path to database.csv")
    parser.add_argument("--uri", default=DEFAULT_URI, help="Neo4j bolt URI")
    parser.add_argument("--user", default=DEFAULT_USER, help="Neo4j username")
    parser.add_argument("--password", default=DEFAULT_PASSWORD, help="Neo4j password")
    parser.add_argument("--password-prompt", action="store_true", help="Prompt for the Neo4j password")
    parser.add_argument("--database", default=DEFAULT_DATABASE, help="Neo4j database name")
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE, help="Rows per write batch")
    parser.add_argument("--dry-run", action="store_true", help="Parse the CSV and report counts without writing to Neo4j")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if not args.input.is_file():
        raise SystemExit(f"Input CSV not found: {args.input}")
    mentions = read_mentions(args.input)
    if args.dry_run:
        concepts = {row.concept_id for row in mentions}
        print(f"Would ingest {len(mentions)} mentions covering {len(concepts)} concepts")
        return 0
    if args.password_prompt and not args.password:
        args.password = getpass.getpass("Neo4j password: ")
    if not args.password:
        raise SystemExit("Neo4j password not provided. Use --password or --password-prompt.")
    driver = GraphDatabase.driver(args.uri, auth=(args.user, args.password))
    with driver.session(database=args.database) as session:
        ensure_source_nodes(session, SOURCE_CONFIGS)
        total = len(mentions)
        processed = 0
        for batch in batched(mentions, args.batch_size):
            write_batch(session, batch)
            processed += len(batch)
            print(f"Ingested {processed}/{total} mentions", flush=True)
    driver.close()
    concepts = {row.concept_id for row in mentions}
    print(f"Finished ingestion: {len(mentions)} mentions covering {len(concepts)} concepts")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
