#!/usr/bin/env python3
"""
Populate English Wikipedia links for each QID in a database CSV.

Adds a new column 'Wikipedia Link' containing https://en.wikipedia.org/wiki/<Title>
when the Wikidata entity has an enwiki sitelink. Existing columns are preserved.

Usage:
  python scripts/add_enwiki_links.py --in data/database.csv --out data/database.csv
  python scripts/add_enwiki_links.py --in data/database_pruned.csv --out data/database_pruned.csv
"""
import argparse
import csv
import os
import sys
import time
import urllib.parse
import urllib.request
from typing import Dict, List


def batched(xs: List[str], n: int):
    for i in range(0, len(xs), n):
        yield xs[i:i + n]


def fetch_enwiki_links(qids: List[str], *, batch_size: int = 100, pause: float = 0.1) -> Dict[str, str]:
    """Return {QID: enwiki_title} for given QIDs using Wikidata API (wbgetentities).
    Prints progress to stderr.
    """
    out: Dict[str, str] = {}
    total = len(qids)
    done = 0
    for batch in batched(qids, batch_size):
        params = {
            'action': 'wbgetentities',
            'ids': '|'.join(batch),
            'props': 'sitelinks',
            'sitefilter': 'enwiki',
            'format': 'json',
            'origin': '*',
        }
        url = 'https://www.wikidata.org/w/api.php?' + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={
            'User-Agent': 'MathGloss/add_enwiki_links (contact: your-email@example.com)'
        })
        # best-effort with a couple quick retries
        data = None
        for attempt in range(2):
            try:
                with urllib.request.urlopen(req, timeout=20) as resp:
                    data = resp.read().decode('utf-8', errors='replace')
                break
            except Exception as e:
                if attempt == 1:
                    print(f"[warn] batch failed ({e}); continuing", file=sys.stderr)
                time.sleep(pause)
        if data is None:
            done += len(batch)
            continue
        try:
            import json
            j = json.loads(data)
        except Exception:
            j = {}
        ents = (j.get('entities') or {})
        for q in batch:
            ent = ents.get(q) or {}
            sl = ent.get('sitelinks') or {}
            en = sl.get('enwiki') or {}
            title = en.get('title')
            if isinstance(title, str) and title:
                out[q] = title
        done += len(batch)
        if total:
            pct = int(100 * done / total)
            print(f"[enwiki] {done}/{total} ({pct}%)", file=sys.stderr)
        time.sleep(pause)
    return out


def main():
    ap = argparse.ArgumentParser(description='Add English Wikipedia links to database CSV (via Wikidata sitelinks).')
    ap.add_argument('--in', dest='inp', required=True, help='Input CSV path (database.csv or database_pruned.csv)')
    ap.add_argument('--out', dest='out', required=True, help='Output CSV path (can overwrite input)')
    ap.add_argument('--batch-size', type=int, default=100, help='API batch size (default 100)')
    args = ap.parse_args()

    with open(args.inp, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        rows = list(reader)

    qids = []
    for r in rows:
        q = (r.get('Wikidata ID') or '').strip()
        if q.startswith('Q'):
            qids.append(q)
    qids = sorted(set(qids))
    print(f"Found {len(qids)} unique QIDs", file=sys.stderr)

    # Keep any existing links so re-runs only fill missing
    existing = {}
    link_col = 'Wikipedia Link'
    for r in rows:
        q = (r.get('Wikidata ID') or '').strip()
        link = (r.get(link_col) or '').strip()
        if q and link:
            existing[q] = link

    enwiki = fetch_enwiki_links(qids, batch_size=max(1, args.batch_size))

    if link_col not in headers:
        headers = headers + [link_col]

    filled_before = sum(1 for r in rows if (r.get(link_col) or '').strip())
    for r in rows:
        q = (r.get('Wikidata ID') or '').strip()
        # preserve existing link if present
        if q in existing:
            r[link_col] = existing[q]
            continue
        title = enwiki.get(q)
        if title:
            r[link_col] = 'https://en.wikipedia.org/wiki/' + urllib.parse.quote(title)
        else:
            r[link_col] = ''
    filled_after = sum(1 for r in rows if (r.get(link_col) or '').strip())

    os.makedirs(os.path.dirname(args.out) or '.', exist_ok=True)
    with open(args.out, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {args.out} with column '{link_col}'. Filled: +{filled_after - filled_before} (now {filled_after} total).")


if __name__ == '__main__':
    main()
