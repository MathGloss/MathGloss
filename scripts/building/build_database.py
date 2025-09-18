#!/usr/bin/env python3
"""
Merge per-source alignment CSVs into a single database CSV.

Accepted input alignment formats (one file per source):
1) Preferred (three columns):
   Wikidata ID,<SourceName>,<SourceName link>
   - Example: "[Q181296](https://www.wikidata.org/wiki/Q181296),abelian group,https://.../abelian_group"

2) Legacy (two columns):
   Wikidata ID,<SourceName>
   - Value may be plain text, plain URL, or markdown "[Name](URL)" and will be split
     into Name/Link internally.

Output columns (merged database.csv):
   Wikidata ID, Wikidata Label, <Source1 Name>, <Source1 Link>, <Source2 Name>, <Source2 Link>, ...

Label population options:
- Local index: provide --db to read Wikipedia titles from a local SQLite index (wikimapper-style).
- Online API: provide --online-labels to resolve labels from Wikidata (optionally cached via --cache).
  Online mode prefers the English Wikipedia sitelink title when available, otherwise falls back to
  the Wikidata English label.

Usage:
    python scripts/build_database.py --alignments data/alignments --out data/database.csv [--online-labels [--cache data/cache/wd_labels.json]]
    python scripts/build_database.py --alignments data/alignments --out data/database.csv [--db /path/to/index.db]
"""
import argparse
import csv
import json
import os
from collections import defaultdict, OrderedDict
import re
import urllib.parse
import urllib.request
from typing import Dict, Optional
import time
import sys

# Reuse the mapper class for id_to_titles if available
try:
    from scripts.building.mapper import WikiMapper  # type: ignore
except Exception:  # pragma: no cover
    WikiMapper = None  # fallback handled at runtime

def _normalize_wikidata_id(raw: str) -> str:
    raw = (raw or '').strip()
    m = re.search(r"Q\d+", raw)
    return m.group(0) if m else raw


SOURCE_NAME_ALIASES = {
    'bct': 'BCT',
    'chicago': 'Chicago',
    'clowder': 'Clowder',
    'context': 'Context',
    'mathlib': 'Mathlib',
    'nlab': 'nLab',
    'planetmath': 'PlanetMath',
}

SOURCE_SUFFIXES = (
    '_layer_compiled',
    '_layer_matches',
    '_layer_misses_wikimapper',
    '_layer_misses',
    '_mappings',
)


def _infer_source_name(path: str, fallback: str) -> str:
    stem = os.path.splitext(os.path.basename(path))[0]
    for suffix in SOURCE_SUFFIXES:
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
            break
    normalized = stem.strip().lower()
    if not normalized:
        return fallback
    if normalized in SOURCE_NAME_ALIASES:
        return SOURCE_NAME_ALIASES[normalized]
    pretty = stem.replace('_', ' ').strip()
    return pretty.title() if pretty else fallback


def read_alignment(path):
    rows = []  # list of tuples: (key, name, link)
    labels = {}  # key -> label
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        if len(headers) < 2 or headers[0] != 'Wikidata ID':
            raise ValueError(f"Invalid alignment format in {path}")
        raw_second = headers[1]
        # normalize source base, e.g., "Chicago Name" -> "Chicago", or keep "Chicago"
        source_name = raw_second.replace(' Name', '').strip()
        if source_name.lower() in {'title', 'titles', ''}:
            source_name = _infer_source_name(path, fallback='Title')
        three_col = len(headers) >= 3
        header_map = {h.strip().lower(): idx for idx, h in enumerate(headers)}
        label_idx = None
        for key in ('label', 'wikidata label'):
            if key in header_map:
                label_idx = header_map[key]
                break
        for r in reader:
            if not r or not r[0].strip():
                continue
            key = _normalize_wikidata_id(r[0])
            if three_col:
                name = r[1].strip() if len(r) > 1 else ''
                link = r[2].strip() if len(r) > 2 else ''
            else:
                value = r[1].strip() if len(r) > 1 else ''
                name, link = split_name_link(value)
            rows.append((key, name, link))
            if label_idx is not None and len(r) > label_idx:
                lbl = r[label_idx].strip()
                if lbl and key not in labels:
                    labels[key] = lbl
    return source_name, rows, labels

def split_name_link(value: str):
    # Parse markdown [Name](URL)
    if value.startswith('[') and '](' in value and value.endswith(')'):
        try:
            name = value.split('[',1)[1].split(']',1)[0]
            link = value.split('](',1)[1][:-1]
            return name.strip(), link.strip()
        except Exception:
            return value, ''
    # If it looks like a URL
    if value.startswith('http://') or value.startswith('https://'):
        return '', value
    # Else plain text
    return value, ''

def merge_alignments(alignments_dir):
    data = defaultdict(dict)  # key -> {f"{source} Name": name, f"{source} Link": link}
    sources = []
    inferred_labels = {}
    for fname in sorted(os.listdir(alignments_dir)):
        if not fname.endswith('.csv'):
            continue
        source, rows, labels = read_alignment(os.path.join(alignments_dir, fname))
        if source not in sources:
            sources.append(source)
        for key, name, link in rows:
            if name:
                data[key][f"{source} Name"] = name
            if link:
                data[key][f"{source} Link"] = link
        for key, lbl in labels.items():
            if lbl and key not in inferred_labels:
                inferred_labels[key] = lbl
    return sources, data, inferred_labels


def _load_cache(path: Optional[str]) -> Dict[str, str]:
    if not path:
        return {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _save_cache(path: Optional[str], cache: Dict[str, str]) -> None:
    if not path:
        return
    try:
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2, sort_keys=True)
    except Exception:
        # best-effort; do not crash build on cache write issues
        pass


def _fetch_wikidata_label_online(qid: str, timeout: float = 10.0, retries: int = 1) -> str:
    """Fetch human-readable label for a Wikidata entity.
    Preference order:
    1) English Wikipedia sitelink title (enwiki)
    2) English Wikidata label
    Returns empty string on error or missing data.
    """
    qid = (qid or '').strip()
    if not qid:
        return ''
    url = f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json"
    # Be a good API citizen; some endpoints are stricter without UA
    headers = {"User-Agent": "MathGloss/1.0 (+https://github.com/lucyhorowitz/MathGloss)"}
    last_err: Optional[Exception] = None
    for attempt in range(max(1, retries)):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode('utf-8'))
            break
        except Exception as e:
            last_err = e
            if attempt + 1 < max(1, retries):
                time.sleep(0.5 * (attempt + 1))
            else:
                return ''
    ent = (data.get('entities') or {}).get(qid) or {}
    # Prefer enwiki sitelink
    sitelinks = ent.get('sitelinks') or {}
    enwiki = sitelinks.get('enwiki') or {}
    title = enwiki.get('title')
    if isinstance(title, str) and title:
        return urllib.parse.unquote(title).replace('_', ' ')
    # Fallback: English label
    labels = ent.get('labels') or {}
    en = labels.get('en') or {}
    lbl = en.get('value')
    if isinstance(lbl, str) and lbl:
        return lbl
    return ''


def _print_progress(prefix: str, idx: int, total: int, a: int, b: int):
    """Write a single-line carriage-return progress update to stderr.
    For online mode, a=cache_hits, b=fetched; for db mode, a=resolved, b=0.
    """
    total = max(total, 1)
    pct = int((idx / total) * 100)
    if prefix == 'online':
        suffix = f"cache {a}, fetched {b}"
    else:
        suffix = f"resolved {a}"
    msg = f"[{prefix}] {idx}/{total} ({pct}%) - {suffix}"
    # pad to clear previous content, stay on same line
    sys.stderr.write('\r' + msg.ljust(80))
    sys.stderr.flush()

def write_database_csv(out_path, sources, data, labels=None):
    expanded = []
    for s in sources:
        expanded.extend([f"{s} Name", f"{s} Link"])
    fieldnames = ['Wikidata ID', 'Wikidata Label'] + expanded
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for key in sorted(data.keys()):
            row = OrderedDict()
            row['Wikidata ID'] = key
            row['Wikidata Label'] = (labels or {}).get(key, '')
            for s in sources:
                row[f"{s} Name"] = data[key].get(f"{s} Name", '')
                row[f"{s} Link"] = data[key].get(f"{s} Link", '')
            writer.writerow(row)

def main():
    ap = argparse.ArgumentParser(description='Build database.csv from per-source alignment CSVs.')
    ap.add_argument('--alignments', required=True, help='Directory containing <source>_mappings.csv files')
    ap.add_argument('--out', required=True, help='Output database.csv path')
    ap.add_argument('--db', required=False, help='Path to Wikipedia→Wikidata SQLite index to populate Wikidata Label (legacy/local)')
    ap.add_argument('--online-labels', action='store_true', help='Fetch labels from Wikidata API (cached if --cache provided)')
    ap.add_argument('--cache', required=False, default='data/cache/wd_labels.json', help='Path to JSON cache for online labels')
    ap.add_argument('--timeout', type=float, default=10.0, help='HTTP timeout (seconds) for online label fetches')
    ap.add_argument('--retries', type=int, default=2, help='HTTP retry attempts for online label fetches')
    args = ap.parse_args()

    sources, data, inferred_labels = merge_alignments(args.alignments)
    os.makedirs(os.path.dirname(args.out) or '.', exist_ok=True)
    labels: Dict[str, str] = dict(inferred_labels)

    # Online mode takes precedence when requested
    if args.online_labels:
        cache = _load_cache(args.cache)
        cache_hits = 0
        fetched = 0
        prefilled = sum(1 for key in data.keys() if key in labels and labels[key])
        keys = list(data.keys())
        total = len(keys)
        # Update roughly every 1% or at least every 10 items
        step = max(10, total // 100)
        for i, key in enumerate(keys, 1):
            if key in labels and labels[key]:
                if i % step == 0 or i == total:
                    _print_progress('online', i, total, cache_hits + prefilled, fetched)
                continue
            if key in cache and cache.get(key):
                labels[key] = cache[key]
                cache_hits += 1
            else:
                lbl = _fetch_wikidata_label_online(key, timeout=args.timeout, retries=args.retries)
                if lbl:
                    labels[key] = lbl
                    cache[key] = lbl
                    fetched += 1
            if i % step == 0 or i == total:
                _print_progress('online', i, total, cache_hits + prefilled, fetched)
        # newline after progress bar
        sys.stderr.write('\n')
        sys.stderr.flush()
        _save_cache(args.cache, cache)
        print(f"Online labels: {prefilled} prefilled, {cache_hits} cache hits, {fetched} fetched, cache path: {args.cache}")
    elif args.db:
        if WikiMapper is None:
            raise RuntimeError('mapper.WikiMapper not available to populate labels; run with --online-labels or ensure scripts are co-located.')
        mapper = WikiMapper(args.db)
        keys = list(data.keys())
        total = len(keys)
        resolved = 0
        prefilled = sum(1 for key in keys if key in labels and labels[key])
        step = max(10, total // 100)
        for i, key in enumerate(keys, 1):
            if key in labels and labels[key]:
                if i % step == 0 or i == total:
                    _print_progress('db', i, total, resolved + prefilled, 0)
                continue
            try:
                titles = mapper.id_to_titles(key)
                if titles:
                    # Choose first title; prettify by unquoting and replacing underscores
                    label = urllib.parse.unquote(titles[0]).replace('_', ' ')
                    labels[key] = label
                    resolved += 1
            except Exception:
                pass
            if i % step == 0 or i == total:
                _print_progress('db', i, total, resolved + prefilled, 0)
        sys.stderr.write('\n')
        sys.stderr.flush()
    write_database_csv(args.out, sources, data, labels)
    print(f"Wrote {args.out} with {len(data)} rows and {len(sources)} sources. Labels populated: {sum(1 for v in labels.values() if v)}")

if __name__ == '__main__':
    main()
