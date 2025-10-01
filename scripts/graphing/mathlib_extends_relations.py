#!/usr/bin/env python3
"""Derive extends-based relationships between Mathlib declarations.

Given a MathGloss database CSV (e.g. ``data/database_compiled_pruned.csv``)
and a local Mathlib checkout, this script walks each ``Mathlib Link`` entry,
extracts the Lean declaration referenced by the URL, and records the
``extends`` hierarchy discovered in the Lean source. For every ancestor we
try to map back to a MathGloss concept so downstream tooling can surface
relationships such as ``Group`` ⊑ ``Monoid``.

Usage example::

    python scripts/graphing/mathlib_extends_relations.py \
        --database data/database_compiled_pruned.csv \
        --mathlib-dir /path/to/mathlib \
        --out data/relations/mathlib_extends_relations.csv

The script is intentionally heuristic—Lean allows fairly rich declaration
syntax—but it works well for the common ``structure``/``class`` definitions
that make up Mathlib's type hierarchy.
"""

from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Iterable, Optional, Sequence
from urllib.parse import urlparse

MATHLIB_DOC_BASE = "https://leanprover-community.github.io/mathlib4_docs/"

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

from scripts.graphing.mathlib_statement_lookup import (  # type: ignore  # noqa: E402
    extract_signature,
    resolve_mathlib_file,
)


@dataclass(slots=True)
class GlossEntry:
    wikidata_id: str
    label: str
    mathlib_name: str
    mathlib_link: str


@dataclass(slots=True)
class RelationRow:
    child_lean: str
    child_label: str
    child_wikidata: str
    child_link: str
    parent_lean: str
    parent_label: str
    parent_wikidata: str
    parent_link: str
    depth: int
    path: str


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--database",
        type=Path,
        default=Path("data/database_compiled_pruned.csv"),
        help="CSV containing MathGloss entries with Mathlib links.",
    )
    parser.add_argument(
        "--mathlib-dir",
        type=Path,
        required=True,
        help="Path to the local Mathlib checkout (the directory containing Mathlib/).",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("data/relations/mathlib_extends_relations.csv"),
        help="Where to write the derived relations CSV.",
    )
    parser.add_argument(
        "--edges-out",
        type=Path,
        help="Optional path to write canonical subclass edges (for Neo4j ingestion).",
    )
    parser.add_argument(
        "--missing-links-out",
        type=Path,
        help="Optional path to write Mathlib link suggestions for MathGloss concepts lacking them.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional limit on the number of Mathlib entries to process (for debugging).",
    )
    return parser.parse_args(argv)


def load_database(db_path: Path) -> list[dict[str, str]]:
    with db_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return [row for row in reader]


def normalize_label(label: str) -> str:
    return re.sub(r"\s+", " ", label.strip().lower())


def camel_to_words(name: str) -> str:
    parts = re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+", name)
    if not parts:
        return name.lower()
    return " ".join(parts).lower()


def normalize_token(text: str) -> str:
    return re.sub(r"[^0-9a-z]+", "", text.lower())


def fragment_match_score(fragment: str, row: dict[str, str]) -> float:
    lean_norm = normalize_token(fragment)
    if not lean_norm:
        return 1.0
    candidates = []
    for key in (
        "Mathlib Name",
        "Wikidata Label",
        "Chicago Name",
        "nLab Name",
        "BCT Name",
    ):
        value = (row.get(key) or "").strip()
        if value:
            normalized = normalize_token(value)
            if normalized:
                candidates.append(normalized)
    if not candidates:
        return 1.0
    best_ratio = 0.0
    for candidate in candidates:
        if candidate == lean_norm:
            return 0.0
        ratio = SequenceMatcher(None, lean_norm, candidate).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
    return 1.0 - best_ratio if best_ratio else 1.0


def build_entry_indexes(rows: Iterable[dict[str, str]]) -> tuple[
    dict[str, GlossEntry],
    dict[str, GlossEntry],
    dict[str, GlossEntry],
]:
    fragment_map: dict[str, GlossEntry] = {}
    label_map: dict[str, GlossEntry] = {}
    mathlib_name_map: dict[str, GlossEntry] = {}

    for row in rows:
        entry = GlossEntry(
            wikidata_id=row.get("Wikidata ID", "").strip(),
            label=row.get("Wikidata Label", "").strip(),
            mathlib_name=row.get("Mathlib Name", "").strip(),
            mathlib_link=row.get("Mathlib Link", "").strip(),
        )

        if entry.mathlib_link:
            parsed = urlparse(entry.mathlib_link)
            fragment = parsed.fragment.strip()
            if fragment:
                fragment_map.setdefault(fragment, entry)

        if entry.label:
            label_map.setdefault(normalize_label(entry.label), entry)

        if entry.mathlib_name:
            mathlib_name_map.setdefault(normalize_label(entry.mathlib_name), entry)

    return fragment_map, label_map, mathlib_name_map


def compute_fragment_preferences(rows: list[dict[str, str]]) -> dict[str, dict[str, object]]:
    fragment_to_indices: dict[str, list[int]] = defaultdict(list)
    for idx, row in enumerate(rows):
        link = (row.get("Mathlib Link") or "").strip()
        if not link:
            continue
        fragment = urlparse(link).fragment.strip()
        if not fragment:
            continue
        fragment_to_indices[fragment].append(idx)

    preferences: dict[str, dict[str, object]] = {}
    for fragment, indices in fragment_to_indices.items():
        if len(indices) <= 1:
            continue
        best_idx: Optional[int] = None
        best_score = float("inf")
        scores: dict[int, float] = {}
        for idx in indices:
            score = fragment_match_score(fragment, rows[idx])
            scores[idx] = score
            if score < best_score:
                best_score = score
                best_idx = idx
        preferences[fragment] = {"best_index": best_idx, "scores": scores}
    return preferences


def doc_url_for(mathlib_root: Path, file_path: Path, decl_name: str) -> str | None:
    try:
        rel = file_path.relative_to(mathlib_root)
    except ValueError:
        return None
    doc_path = rel.with_suffix(".html")
    url = MATHLIB_DOC_BASE + doc_path.as_posix()
    if decl_name:
        url += f"#{decl_name}"
    return url


def parse_extends(signature: str) -> list[str]:
    match = re.search(r"\bextends\b(.*)", signature, re.DOTALL)
    if not match:
        return []
    tail = match.group(1)
    for stop in (" where", " :=", " deriving"):
        idx = tail.find(stop)
        if idx != -1:
            tail = tail[:idx]
            break
    parts = [segment.strip() for segment in tail.split(",")]
    parents: list[str] = []
    for part in parts:
        if not part:
            continue
        part = part.replace("_root_.", "")
        token = re.match(r"([A-Za-z0-9_\.']+)", part)
        if token:
            parents.append(token.group(1))
    return parents


def run_rg_for_decl(mathlib_root: Path, name: str) -> Path | None:
    search_token = name.split(".")[-1]
    pattern = rf"^\s*(?:structure|class)\s+{re.escape(search_token)}\b"
    result = subprocess.run(
        [
            "rg",
            "--pcre2",
            "--no-heading",
            "-n",
            pattern,
            str(mathlib_root),
        ],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode not in (0, 1):
        raise RuntimeError(
            f"ripgrep failed while locating '{name}': {result.stderr.strip()}"
        )
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    if not lines:
        return None
    best_path: Path | None = None
    best_score = float("inf")
    for line in lines:
        path_str, _, content = line.partition(":")
        # ``content`` still includes the line number; split once more to reach the source text.
        _, _, source_text = content.partition(":")
        source_text = source_text.strip()
        candidate = Path(path_str)
        if not candidate.is_absolute():
            candidate = mathlib_root / candidate
        try:
            rel = candidate.relative_to(mathlib_root)
            rel_parts = rel.parts
        except ValueError:
            rel_parts = ()
        root = rel_parts[0] if rel_parts else ""
        priority = {
            "Mathlib": 0,
            "Init": 1,
            "Std": 2,
            "Batteries": 3,
        }.get(root, 10)
        score = priority * 10 + len(rel_parts)

        if source_text:
            lower = source_text.lower()
            name_lower = name.lower()
            idx = lower.find(name_lower)
            if idx != -1:
                after = lower[idx + len(name_lower) : idx + len(name_lower) + 1]
                if after in {"", " ", "(", "["}:
                    score -= 2
                elif after in {".", "_"}:
                    score += 2

        if score < best_score:
            best_score = score
            best_path = candidate
    return best_path


class ExtendsResolver:
    def __init__(self, mathlib_root: Path):
        self.mathlib_root = mathlib_root
        self.decl_to_file: dict[str, Path] = {}
        self.parents_cache: dict[str, list[str]] = {}
        self.doc_urls: dict[str, str] = {}

    def register(self, name: str, file_path: Path, doc_url: str | None = None) -> None:
        self.decl_to_file.setdefault(name, file_path)
        if doc_url:
            self.doc_urls.setdefault(name, doc_url)

    def find_file(self, name: str) -> Path | None:
        if name in self.decl_to_file:
            return self.decl_to_file[name]
        candidate = run_rg_for_decl(self.mathlib_root, name)
        if candidate:
            self.decl_to_file[name] = candidate
        return candidate

    def parents(self, name: str) -> list[str]:
        if name in self.parents_cache:
            return self.parents_cache[name]

        file_path = self.find_file(name)
        if not file_path or not file_path.exists():
            self.parents_cache[name] = []
            return []

        try:
            signature = extract_signature(file_path, name)
        except Exception:
            self.parents_cache[name] = []
            return []

        if not signature:
            self.parents_cache[name] = []
            return []

        parents = parse_extends(signature)
        self.parents_cache[name] = parents

        if name not in self.doc_urls:
            doc_url = doc_url_for(self.mathlib_root, file_path, name)
            if doc_url:
                self.doc_urls[name] = doc_url
        return parents

    def ancestor_paths(self, name: str) -> list[tuple[str, int, list[str]]]:
        """Return (ancestor, depth, path) tuples for ``name``."""

        paths: list[tuple[str, int, list[str]]] = []
        stack: list[str] = []

        def dfs(current: str) -> None:
            stack.append(current)
            for parent in self.parents(current):
                if parent in stack:
                    continue
                path = stack[1:] + [parent]
                paths.append((parent, len(path), path.copy()))
                dfs(parent)
            stack.pop()

        dfs(name)

        best: dict[str, tuple[int, list[str]]] = {}
        for ancestor, depth, path in paths:
            if ancestor not in best or depth < best[ancestor][0]:
                best[ancestor] = (depth, path)

        return [(ancestor, depth, path) for ancestor, (depth, path) in best.items()]


def best_entry_for(
    lean_name: str,
    fragment_map: dict[str, GlossEntry],
    mathlib_name_map: dict[str, GlossEntry],
    label_map: dict[str, GlossEntry],
) -> GlossEntry | None:
    if lean_name in fragment_map:
        return fragment_map[lean_name]

    suffix = lean_name.split(".")[-1]
    if suffix in fragment_map:
        return fragment_map[suffix]

    suffix_norm = normalize_label(suffix)
    if suffix_norm in mathlib_name_map:
        return mathlib_name_map[suffix_norm]

    camel_norm = normalize_label(camel_to_words(suffix))
    if camel_norm in label_map:
        return label_map[camel_norm]

    return None


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)

    mathlib_root = args.mathlib_dir.expanduser().resolve()
    if not mathlib_root.exists():
        print(f"Mathlib directory not found: {mathlib_root}", file=sys.stderr)
        return 1

    rows = load_database(args.database)
    fragment_preferences = compute_fragment_preferences(rows)
    fragment_map, label_map, mathlib_name_map = build_entry_indexes(rows)

    resolver = ExtendsResolver(mathlib_root)

    relations: list[RelationRow] = []
    processed = 0
    link_updates: dict[str, dict[str, str]] = {}

    for row_index, row in enumerate(rows):
        link = (row.get("Mathlib Link", "") or "").strip()
        if not link:
            continue

        if args.limit is not None and processed >= args.limit:
            break

        parsed = urlparse(link)
        fragment = parsed.fragment.strip()
        if not fragment:
            continue

        try:
            file_path, _ = resolve_mathlib_file(mathlib_root, link)
        except FileNotFoundError as exc:
            print(f"[warn] {exc}", file=sys.stderr)
            continue
        except Exception as exc:  # pylint: disable=broad-except
            print(f"[warn] Failed to resolve {link}: {exc}", file=sys.stderr)
            continue

        resolver.register(fragment, file_path, link)

        ancestors = resolver.ancestor_paths(fragment)

        child_entry = best_entry_for(
            fragment,
            fragment_map,
            mathlib_name_map,
            label_map,
        )
        child_label = (row.get("Wikidata Label") or "").strip()
        if not child_label and child_entry:
            child_label = child_entry.label
        child_wikidata = (row.get("Wikidata ID") or "").strip()
        if not child_wikidata and child_entry:
            child_wikidata = child_entry.wikidata_id
        if child_entry and child_wikidata and not child_entry.mathlib_link and link:
            link_updates.setdefault(
                child_wikidata,
                {
                    "wikidata_id": child_wikidata,
                    "label": child_label,
                    "lean_name": fragment,
                    "mathlib_name": child_entry.mathlib_name or fragment,
                    "mathlib_link": link,
                },
            )

        if ancestors:
            for parent, depth, path in ancestors:
                parent_entry = best_entry_for(
                    parent,
                    fragment_map,
                    mathlib_name_map,
                    label_map,
                )

                parent_link = ""
                if parent_entry and parent_entry.mathlib_link:
                    parent_link = parent_entry.mathlib_link
                else:
                    parent_link = resolver.doc_urls.get(parent, "")
                    if parent_entry and parent_entry.wikidata_id and not parent_entry.mathlib_link and parent_link:
                        link_updates.setdefault(
                            parent_entry.wikidata_id,
                            {
                                "wikidata_id": parent_entry.wikidata_id,
                                "label": parent_entry.label,
                                "lean_name": parent,
                                "mathlib_name": parent_entry.mathlib_name or parent,
                                "mathlib_link": parent_link,
                            },
                        )

                relations.append(
                    RelationRow(
                        child_lean=fragment,
                        child_label=child_label,
                        child_wikidata=child_wikidata,
                        child_link=link,
                        parent_lean=parent,
                        parent_label=parent_entry.label if parent_entry else "",
                        parent_wikidata=parent_entry.wikidata_id if parent_entry else "",
                        parent_link=parent_link,
                        depth=depth,
                        path=" > ".join([fragment] + path),
                    )
                )

        preference = fragment_preferences.get(fragment)
        if preference:
            best_index = preference.get("best_index")
            if isinstance(best_index, int) and best_index != row_index:
                parent_row = rows[best_index]
                parent_wikidata = (parent_row.get("Wikidata ID") or "").strip()
                parent_label = (parent_row.get("Wikidata Label") or "").strip()
                if not parent_label:
                    parent_label = (parent_row.get("Mathlib Name") or "").strip()
                if not parent_label and child_entry:
                    parent_label = child_entry.label
                if not parent_wikidata:
                    preferred_entry = best_entry_for(
                        fragment,
                        fragment_map,
                        mathlib_name_map,
                        label_map,
                    )
                    if preferred_entry and preferred_entry.wikidata_id:
                        parent_wikidata = preferred_entry.wikidata_id
                    if preferred_entry and preferred_entry.label and not parent_label:
                        parent_label = preferred_entry.label
                if (
                    parent_wikidata
                    and child_wikidata
                    and parent_wikidata != child_wikidata
                ):
                    parent_link = (parent_row.get("Mathlib Link") or link)
                    alias_child = child_label or child_wikidata or fragment
                    alias_parent = parent_label or parent_wikidata
                    relations.append(
                        RelationRow(
                            child_lean=fragment,
                            child_label=child_label,
                            child_wikidata=child_wikidata,
                            child_link=link,
                            parent_lean=fragment,
                            parent_label=parent_label or "",
                            parent_wikidata=parent_wikidata,
                            parent_link=parent_link,
                            depth=1,
                            path=f"{fragment} ({alias_child}) > {fragment} ({alias_parent})",
                        )
                    )

        processed += 1

    if not relations:
        print("No relations derived; check inputs?", file=sys.stderr)
        return 0

    relations.sort(key=lambda r: (r.child_lean, r.depth, r.parent_lean))

    args.out.parent.mkdir(parents=True, exist_ok=True)

    with args.out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "Child Lean",
                "Child Label",
                "Child Wikidata ID",
                "Child Mathlib Link",
                "Parent Lean",
                "Parent Label",
                "Parent Wikidata ID",
                "Parent Mathlib Link",
                "Depth",
                "Path",
            ]
        )
        for rel in relations:
            writer.writerow(
                [
                    rel.child_lean,
                    rel.child_label,
                    rel.child_wikidata,
                    rel.child_link,
                    rel.parent_lean,
                    rel.parent_label,
                    rel.parent_wikidata,
                    rel.parent_link,
                    rel.depth,
                    rel.path,
                ]
            )

    print(f"Wrote {len(relations)} relations to {args.out}")

    if args.edges_out:
        lean_qid_cache: dict[str, Optional[str]] = {}

        def lean_to_qid(lean_name: str) -> Optional[str]:
            key = lean_name.strip()
            if key in lean_qid_cache:
                return lean_qid_cache[key]
            entry = best_entry_for(key, fragment_map, mathlib_name_map, label_map)
            qid = (entry.wikidata_id.strip() if entry and entry.wikidata_id else "") or None
            lean_qid_cache[key] = qid
            return qid

        edges = []
        for rel in relations:
            if not (rel.child_wikidata and rel.parent_wikidata):
                continue
            child_label = rel.child_label or rel.child_lean
            parent_label = rel.parent_label or rel.parent_lean

            path_parts = [part.strip() for part in rel.path.split(">")]
            intermediate_parts = path_parts[1:-1] if len(path_parts) > 2 else []
            skip_edge = False
            for part in intermediate_parts:
                intermediate_qid = lean_to_qid(part)
                if intermediate_qid and intermediate_qid not in {rel.child_wikidata, rel.parent_wikidata}:
                    skip_edge = True
                    break
            if skip_edge:
                continue

            edges.append(
                {
                    "source_id": rel.child_wikidata,
                    "source_label": child_label,
                    "target_id": rel.parent_wikidata,
                    "target_label": parent_label,
                    "property_id": "P279",
                    "property_label": "subclass of",
                    "source_mathlib_link": rel.child_link,
                    "target_mathlib_link": rel.parent_link,
                    "mathlib_path": rel.path,
                }
            )

        if edges:
            args.edges_out.parent.mkdir(parents=True, exist_ok=True)
            with args.edges_out.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=[
                        "source_id",
                        "source_label",
                        "property_id",
                        "property_label",
                        "target_id",
                        "target_label",
                        "source_mathlib_link",
                        "target_mathlib_link",
                        "mathlib_path",
                    ],
                )
                writer.writeheader()
                writer.writerows(edges)
            print(f"Wrote {len(edges)} subclass edges to {args.edges_out}")
        else:
            print("No subclass edges with Wikidata IDs were found", file=sys.stderr)

    if args.missing_links_out and link_updates:
        args.missing_links_out.parent.mkdir(parents=True, exist_ok=True)
        with args.missing_links_out.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=[
                    "wikidata_id",
                    "label",
                    "lean_name",
                    "mathlib_name",
                    "mathlib_link",
                ],
            )
            writer.writeheader()
            writer.writerows(sorted(link_updates.values(), key=lambda v: v["wikidata_id"]))
        print(f"Wrote {len(link_updates)} Mathlib link suggestions to {args.missing_links_out}")

    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
