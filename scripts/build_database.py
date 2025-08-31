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

Notes:
- No external network calls.
- Wikidata labels can be populated if a local Wikipedia→Wikidata index is provided via --db;
  otherwise they are left blank.

Usage:
    python scripts/build_database.py --alignments data/alignments --out data/database.csv [--db /path/to/index.db]
"""
import argparse
import csv
import os
from collections import defaultdict, OrderedDict
import re
import urllib.parse

# Reuse the mapper class for id_to_titles if available
try:
    from mapper import WikiMapper  # type: ignore
except Exception:  # pragma: no cover
    WikiMapper = None  # fallback handled at runtime

def _normalize_wikidata_id(raw: str) -> str:
    raw = (raw or '').strip()
    m = re.search(r"Q\d+", raw)
    return m.group(0) if m else raw


def read_alignment(path):
    rows = []  # list of tuples: (key, name, link)
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        if len(headers) < 2 or headers[0] != 'Wikidata ID':
            raise ValueError(f"Invalid alignment format in {path}")
        raw_second = headers[1]
        # normalize source base, e.g., "Chicago Name" -> "Chicago", or keep "Chicago"
        source_name = raw_second.replace(' Name', '').strip()
        three_col = len(headers) >= 3
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
    return source_name, rows

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
    for fname in sorted(os.listdir(alignments_dir)):
        if not fname.endswith('.csv'):
            continue
        source, rows = read_alignment(os.path.join(alignments_dir, fname))
        if source not in sources:
            sources.append(source)
        for key, name, link in rows:
            if name:
                data[key][f"{source} Name"] = name
            if link:
                data[key][f"{source} Link"] = link
    return sources, data

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
    ap.add_argument('--db', required=False, help='Path to Wikipedia→Wikidata SQLite index to populate Wikidata Label')
    args = ap.parse_args()

    sources, data = merge_alignments(args.alignments)
    os.makedirs(os.path.dirname(args.out) or '.', exist_ok=True)
    labels = {}
    if args.db:
        if WikiMapper is None:
            raise RuntimeError('mapper.WikiMapper not available to populate labels; run without --db or ensure scripts are co-located.')
        mapper = WikiMapper(args.db)
        for key in data.keys():
            try:
                titles = mapper.id_to_titles(key)
                if titles:
                    # Choose first title; prettify by unquoting and replacing underscores
                    label = urllib.parse.unquote(titles[0]).replace('_', ' ')
                    labels[key] = label
            except Exception:
                continue
    write_database_csv(args.out, sources, data, labels)
    print(f"Wrote {args.out} with {len(data)} rows and {len(sources)} sources. Labels populated: {len(labels)}")

if __name__ == '__main__':
    main()
