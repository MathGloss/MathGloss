#!/usr/bin/env python3
"""
Quick CLI to test WikiMapper lookups on terms.

Examples:
  - python scripts/maptest.py --db /path/to/index.db ring "C*-algebra" "p-adic number"
  - python scripts/maptest.py --db /path/to/index.db --collapsed "banachspace"
  - python scripts/maptest.py --db /path/to/index.db --repl
"""
import argparse
from typing import List

from mapper import WikiMapper, lookup, WIKI_CATS, normalize_title

def test_terms(mapper: WikiMapper, terms: List[str]) -> None:
    for t in terms:
        t_disp = t.strip()
        if not t_disp:
            continue
        qid = lookup(mapper, t_disp)
        titles = mapper.id_to_titles(qid) if qid else []  # type: ignore[arg-type]
        print(f"term: {t_disp}")
        print(f"  normalized: {normalize_title(t_disp)}")
        print(f"  qid: {qid or '-'}")
        if titles:
            print("  titles:")
            for tt in titles[:10]:
                print(f"    - {tt}")
            if len(titles) > 10:
                print(f"    (+{len(titles)-10} more)")
        else:
            print("  titles: -")
        print()

def repl(mapper: WikiMapper) -> None:
    print("WikiMapper REPL. Type a term (or :q to quit).")
    while True:
        try:
            s = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not s:
            continue
        if s in {":q", ":quit", ":exit"}:
            break
        test_terms(mapper, [s])


def main():
    ap = argparse.ArgumentParser(description="Test WikiMapper on given terms or in a REPL")
    ap.add_argument("terms", nargs="*", help="Terms to test. If empty and --repl not set, nothing happens.")
    ap.add_argument("--db", required=True, help="Path to Wikipedia→Wikidata SQLite index (table mapping)")
    # --collapsed is deprecated/no-op; kept for CLI compatibility
    ap.add_argument("--collapsed", action="store_true", help="(deprecated/no-op)")
    ap.add_argument("--repl", action="store_true", help="Start interactive prompt")
    args = ap.parse_args()

    mapper = WikiMapper(args.db)
    if args.repl:
        repl(mapper)
    elif args.terms:
        test_terms(mapper, args.terms)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
