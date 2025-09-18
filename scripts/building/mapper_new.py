#!/usr/bin/env python3
"""
Match a termlist CSV against layered Wikidata label sets.

The mapper loads the layered catalog (directly from layer CSV/JSON files or
from a pre-built catalog JSON) and runs a staged matching pipeline:

1. Exact letter-only normalization match.
2. Exact "simple" normalization match (alphanumeric words).
3. Token Jaccard similarity (with configurable threshold).

For each term the mapper emits a ranked list of candidates with scores. The
top candidate is accepted when it satisfies the configured score threshold and
is sufficiently separated from the runner-up. The matches/misses CSVs include
diagnostics and alternate candidates to simplify manual review.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Iterable, List, Sequence

try:  # allow execution as standalone script
    from scripts.building.layer_catalog import LayerCatalog, MatchCandidate
    from scripts.building.text_norm import normalize_letters
except ModuleNotFoundError:  # pragma: no cover
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from scripts.building.layer_catalog import LayerCatalog, MatchCandidate
    from scripts.building.text_norm import normalize_letters


def ensure_outdir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Match termlist titles to layered Wikidata labels")
    ap.add_argument("--csv", required=True, help="Input CSV with headers: title,link")
    ap.add_argument(
        "--layers",
        nargs="*",
        default=[
            "experiments/layer1.csv",
            "experiments/layer2.csv",
            "experiments/layer3.csv",
            "experiments/layer4.csv",
        ],
        help="Layer CSV/JSON files (ignored if --catalog is provided)",
    )
    ap.add_argument("--catalog", help="Path to pre-built catalog JSON (from build_layer_catalog.py)")
    ap.add_argument(
        "--outdir",
        default="data/alignments/new",
        help="Output directory (default: data/alignments/new)",
    )
    ap.add_argument("--accept-threshold", type=float, default=0.85, help="Score threshold to auto-accept a candidate")
    ap.add_argument(
        "--min-gap",
        type=float,
        default=0.1,
        help="Minimum score gap between best and second-best to auto-accept (ignored for exact matches)",
    )
    ap.add_argument(
        "--max-candidates",
        type=int,
        default=5,
        help="Maximum candidates to include per term for diagnostics",
    )
    ap.add_argument(
        "--token-threshold",
        type=float,
        default=0.6,
        help="Minimum Jaccard score to keep token-based candidates",
    )
    return ap.parse_args(argv)


def format_candidate(cand: MatchCandidate) -> str:
    return f"{cand.item.qid} ({cand.score:.3f}; {cand.reason}) {cand.item.label} [{cand.item.layer}]"


def format_candidates(cands: Iterable[MatchCandidate], skip: int = 0) -> str:
    items = list(cands)
    if skip:
        items = items[skip:]
    return "; ".join(format_candidate(c) for c in items)


def load_catalog(args: argparse.Namespace) -> LayerCatalog:
    if args.catalog:
        catalog_path = Path(args.catalog)
        if not catalog_path.exists():
            raise FileNotFoundError(f"Catalog not found: {catalog_path}")
        return LayerCatalog.from_catalog(catalog_path)
    layer_paths = [Path(p) for p in args.layers]
    for lp in layer_paths:
        if not lp.exists():
            raise FileNotFoundError(f"Layer file not found: {lp}")
    return LayerCatalog.from_layers(layer_paths)


def load_termlist(csv_path: Path) -> List[dict]:
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or "title" not in reader.fieldnames or "link" not in reader.fieldnames:
            raise ValueError("Input CSV must have headers: title,link")
        return [row for row in reader]


def decide_accept(top: MatchCandidate | None, others: Sequence[MatchCandidate], args: argparse.Namespace) -> bool:
    if top is None:
        return False
    if top.reason.startswith("exact_"):
        return True
    if top.reason.startswith("of_swap"):
        return True
    if top.score < args.accept_threshold:
        return False
    second = others[1] if len(others) > 1 else None
    if not second:
        return True
    return (top.score - second.score) >= args.min_gap


def write_matches(path: Path, rows: List[List[str]]) -> None:
    headers = [
        "Wikidata ID",
        "Title",
        "Link",
        "Label",
        "Layer",
        "Score",
        "Reason",
        "Alternates",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)


def write_misses(path: Path, rows: List[List[str]]) -> None:
    headers = ["Title", "Link", "Normalized", "Candidates"]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)

    csv_path = Path(args.csv)
    if not csv_path.exists():
        raise FileNotFoundError(f"Input CSV not found: {csv_path}")

    catalog = load_catalog(args)
    rows = load_termlist(csv_path)

    matches: List[List[str]] = []
    misses: List[List[str]] = []

    for row in rows:
        title = (row.get("title") or "").strip()
        link = (row.get("link") or "").strip()
        candidates = catalog.find_candidates(
            title,
            max_candidates=max(1, args.max_candidates),
            token_threshold=max(0.0, min(1.0, args.token_threshold)),
        )
        top = candidates[0] if candidates else None
        normalized = normalize_letters(title)
        alternates = format_candidates(candidates, skip=1)
        if decide_accept(top, candidates, args):
            matches.append(
                [
                    top.item.qid,
                    title,
                    link,
                    top.item.label,
                    top.item.layer,
                    f"{top.score:.3f}",
                    top.reason,
                    alternates,
                ]
            )
        else:
            misses.append([
                title,
                link,
                normalized,
                format_candidates(candidates),
            ])

    outdir = Path(args.outdir)
    ensure_outdir(outdir)
    base = csv_path.stem
    matches_path = outdir / f"{base}_layer_matches.csv"
    misses_path = outdir / f"{base}_layer_misses.csv"
    write_matches(matches_path, matches)
    write_misses(misses_path, misses)
    print(
        f"Wrote {matches_path} ({len(matches)} matches), {misses_path} ({len(misses)} misses)."
    )
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
