#!/usr/bin/env python3
"""
Prune database.csv by excluding rows whose Wikidata entity is a person,
disambiguation page, or theorem-like page (per-instance-of types).

Uses the Wikidata API (wbgetentities) in batches to check P31 values.

Input:  database.csv (from build_database.py)
Output: database_pruned.csv (same columns, filtered rows)

Usage
  python3 scripts/prune_database.py \
    --in data/database.csv \
    --out data/database_pruned.csv \
    [--batch-size 50]

Notes
- Network required.
- Safe to re-run; only reads/writes local CSVs.
"""
import argparse
import csv
import math
import sys
import time
from typing import Dict, Iterable, List, Set

import requests


# Instance-of (P31) QIDs to EXCLUDE
FILTER_P31: Set[str] = {
    'Q5',         # human
    'Q4167410',   # disambiguation page
    'Q22808320',  # human name disambiguation page
#    'Q65943',     # theorem
#    'Q207505',    # lemma
#    'Q108163',    # proposition
}


def batched(xs: List[str], n: int) -> Iterable[List[str]]:
    for i in range(0, len(xs), n):
        yield xs[i:i + n]


def fetch_p31(ids: List[str], *, retries: int = 3, pause: float = 0.2, verbose: bool = False) -> Dict[str, List[str]]:
    """Return {QID: [P31 ids]} for the given ids using Wikidata API.
    Missing/error entities map to an empty list.
    """
    url = 'https://www.wikidata.org/w/api.php'
    params = {
        'action': 'wbgetentities',
        'ids': '|'.join(ids),
        'props': 'claims',
        'format': 'json',
    }
    headers = {"User-Agent": "MathGloss/2 prune_database (contact: your-email@example.com)"}
    for attempt in range(retries):
        try:
            r = requests.get(url, params=params, timeout=20, headers=headers)
            r.raise_for_status()
            data = r.json()
            if 'error' in data:
                if verbose:
                    print(f"[prune][warn] API error for batch: {data['error']}")
                raise RuntimeError(str(data['error']))
            out: Dict[str, List[str]] = {}
            ents = data.get('entities', {}) or {}
            for qid in ids:
                claims = (ents.get(qid) or {}).get('claims', {}) or {}
                p31s = []
                for c in claims.get('P31', []) or []:
                    val = (((c.get('mainsnak') or {}).get('datavalue') or {}).get('value') or {}).get('id')
                    if val:
                        p31s.append(val)
                out[qid] = p31s
            return out
        except Exception:
            if attempt + 1 >= retries:
                return {qid: [] for qid in ids}
            time.sleep(pause * (attempt + 1))
    return {qid: [] for qid in ids}


def main():
    ap = argparse.ArgumentParser(description='Prune database.csv by excluding humans/disambiguations/theorem-like pages via Wikidata API P31 types.')
    ap.add_argument('--in', dest='inp', required=True, help='Path to input database.csv')
    ap.add_argument('--out', dest='out', required=True, help='Path to output pruned CSV')
    ap.add_argument('--batch-size', type=int, default=50, help='Wikidata API batch size (ids per request)')
    ap.add_argument('--verbose', action='store_true', help='Print extra diagnostics and sample P31s')
    ap.add_argument('--fail-on-empty', action='store_true', help='Exit non-zero if no P31 values were retrieved')
    ap.add_argument('--drop-nlab-only', action='store_true', help='Drop rows that only have nLab data and no other source')
    args = ap.parse_args()

    # Read all rows
    with open(args.inp, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        rows = list(reader)

    qids = [r.get('Wikidata ID', '').strip() for r in rows if r.get('Wikidata ID')]
    qids = [q for q in qids if q.startswith('Q')]
    qids_unique = sorted(set(qids))

    # Fetch P31s in batches
    p31_map: Dict[str, List[str]] = {}
    kept, dropped = 0, 0
    total_batches = max(1, math.ceil(len(qids_unique) / max(1, args.batch_size)))
    for bi, batch in enumerate(batched(qids_unique, args.batch_size), start=1):
        print(f"[prune] Fetching P31 batch {bi}/{total_batches} (size={len(batch)})...", flush=True)
        p31s = fetch_p31(batch, verbose=args.verbose)
        p31_map.update(p31s)
        time.sleep(0.05)
    nonempty = sum(1 for v in p31_map.values() if v)
    print(f"[prune] Finished fetching P31 for {len(p31_map)} unique QIDs; non-empty P31 sets: {nonempty}.", flush=True)
    if nonempty == 0:
        print("[prune][warn] No P31 values retrieved. Check network/firewall or try a smaller --batch-size.", flush=True)
        if args.fail_on_empty:
            sys.exit(2)
    if args.verbose:
        sample = [(q, p31_map[q]) for q in qids_unique[:10]]
        print("[prune] Sample P31s:")
        for q, vs in sample:
            print(f"  {q}: {vs}")

    # Filter rows
    filtered: List[dict] = []
    counts_by_type: Dict[str, int] = {}
    # Discover source columns from headers
    fieldnames_lower = [fn.strip() for fn in fieldnames]
    sources = [fn[:-5] for fn in fieldnames_lower if fn.endswith(' Name')]
    def has_source_data(row: dict, src: str) -> bool:
        return bool((row.get(f"{src} Name", '') or '').strip() or (row.get(f"{src} Link", '') or '').strip())
    drop_nlab_only_count = 0
    for i, r in enumerate(rows, start=1):
        qid = r.get('Wikidata ID', '').strip()
        p31s = set(p31_map.get(qid, []))
        hit = p31s & FILTER_P31
        if hit:
            for t in hit:
                counts_by_type[t] = counts_by_type.get(t, 0) + 1
            dropped += 1
            continue
        if args.drop_nlab_only:
            # Drop if nLab has data but no other source has data
            nlab_has = has_source_data(r, 'nLab')
            others = [s for s in sources if s != 'nLab']
            others_have = any(has_source_data(r, s) for s in others)
            if nlab_has and not others_have:
                dropped += 1
                drop_nlab_only_count += 1
                continue
        kept += 1
        filtered.append(r)
        if i % 500 == 0:
            print(f"[prune] Filtered {i}/{len(rows)} rows — kept {kept}, dropped {dropped}.", flush=True)

    # Write output
    with open(args.out, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in filtered:
            w.writerow(r)

    print(f"Pruned to {kept} rows (dropped {dropped}) from {len(rows)} using P31 filters: {sorted(FILTER_P31)}")
    if counts_by_type:
        print("Dropped counts by P31:")
        for t, c in sorted(counts_by_type.items(), key=lambda x: (-x[1], x[0]))[:10]:
            print(f"  {t}: {c}")
    if args.drop_nlab_only:
        print(f"Dropped nLab-only rows: {drop_nlab_only_count}")


if __name__ == '__main__':
    main()
