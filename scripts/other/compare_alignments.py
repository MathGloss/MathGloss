#!/usr/bin/env python3
"""
Compare two alignment CSVs and report which items (by link) are in A not B and B not A.

Assumes both have a column ending with ' link' (case-insensitive). Prints a summary and
writes optional CSVs with the differing rows.

Usage:
  python scripts/compare_alignments.py \
    --a data/alignments/source1.csv \
    --b data/alignments/source2.csv \
    --out-dir data/alignments/diffs
"""
import argparse
import csv
import os
from typing import Tuple, List, Dict


def read_by_link(path: str) -> Tuple[List[str], List[Dict[str, str]], Dict[str, Dict[str, str]], str]:
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        link_col = ''
        for h in headers:
            if h.lower().endswith(' link'):
                link_col = h
                break
        if not link_col:
            raise ValueError(f'No link column ending with " link" found in {path}')
        rows = list(reader)
    by_link: Dict[str, Dict[str, str]] = {}
    for r in rows:
        link = (r.get(link_col) or '').strip()
        if link:
            by_link[link] = r
    return headers, rows, by_link, link_col


def main():
    ap = argparse.ArgumentParser(description='Compare two alignment CSVs by link')
    ap.add_argument('--a', required=True, help='Path to CSV A')
    ap.add_argument('--b', required=True, help='Path to CSV B')
    ap.add_argument('--out-dir', required=False, help='Directory to write difference CSVs')
    args = ap.parse_args()

    hA, rowsA, mapA, linkA = read_by_link(args.a)
    hB, rowsB, mapB, linkB = read_by_link(args.b)

    onlyA = sorted(set(mapA.keys()) - set(mapB.keys()))
    onlyB = sorted(set(mapB.keys()) - set(mapA.keys()))

    print(f'A only: {len(onlyA)}')
    print(f'B only: {len(onlyB)}')

    if args.out_dir:
        os.makedirs(args.out_dir, exist_ok=True)
        # Write A-only rows with A headers
        path_A_only = os.path.join(args.out_dir, 'A_only.csv')
        with open(path_A_only, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=hA)
            w.writeheader()
            for link in onlyA:
                w.writerow(mapA[link])
        # Write B-only rows with B headers
        path_B_only = os.path.join(args.out_dir, 'B_only.csv')
        with open(path_B_only, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=hB)
            w.writeheader()
            for link in onlyB:
                w.writerow(mapB[link])
        print(f'Wrote {path_A_only} and {path_B_only}')


if __name__ == '__main__':
    main()

