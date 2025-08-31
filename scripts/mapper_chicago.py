#!/usr/bin/env python3
"""
Build a Chicago alignment CSV directly from the markdown files by extracting
the embedded Wikidata ID, title, and permalink.

Output: CSV with columns: Wikidata ID, Chicago, Chicago link

Usage:
  python3 scripts/make_chicago_alignment.py \
    --dir ../chicago \
    --base-url https://mathgloss.github.io/MathGloss \
    --out data/alignments/chicago_mappings.csv
"""
import argparse
import csv
import os
import re
from typing import Optional, Tuple


FRONT_MATTER_RE = re.compile(r"^---\s*$", re.M)
TITLE_RE = re.compile(r"^\s*title:\s*(.+)$", re.M)
PERMALINK_RE = re.compile(r"^\s*permalink:\s*(.+)$", re.M)
QID_RE = re.compile(r"Q\d+")


def parse_front_matter(text: str) -> Tuple[Optional[str], Optional[str]]:
    m = list(FRONT_MATTER_RE.finditer(text))
    if len(m) >= 2 and m[0].start() == 0:
        fm = text[m[0].end():m[1].start()]
        title_m = TITLE_RE.search(fm)
        permalink_m = PERMALINK_RE.search(fm)
        title = title_m.group(1).strip() if title_m else None
        permalink = permalink_m.group(1).strip() if permalink_m else None
        return title, permalink
    return None, None


def extract_qid(text: str) -> Optional[str]:
    # Prefer lines that mention Wikidata ID
    for line in text.splitlines():
        if 'Wikidata' in line:
            q = QID_RE.search(line)
            if q:
                return q.group(0)
    # Fallback: first QID anywhere
    q = QID_RE.search(text)
    return q.group(0) if q else None


def build_url(base_url: str, permalink: Optional[str], slug: str) -> str:
    if permalink:
        if permalink.startswith('http://') or permalink.startswith('https://'):
            return permalink
        # ensure single slash join
        return f"{base_url.rstrip('/')}/{permalink.lstrip('/')}"
    return f"{base_url.rstrip('/')}/chicago/{slug}"


def derive_title_from_filename(filename: str) -> str:
    stem = os.path.splitext(os.path.basename(filename))[0]
    return stem.replace('_', ' ').strip()


def main():
    ap = argparse.ArgumentParser(description='Create Chicago alignment from markdown files with embedded Wikidata ID.')
    ap.add_argument('--dir', required=True, help='Directory containing Chicago .md files')
    ap.add_argument('--base-url', required=True, help='Base site URL (e.g., https://mathgloss.github.io/MathGloss)')
    ap.add_argument('--out', required=True, help='Output CSV path')
    args = ap.parse_args()

    rows = []
    for name in sorted(os.listdir(args.dir)):
        if not name.endswith('.md'):
            continue
        path = os.path.join(args.dir, name)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception:
            continue
        qid = extract_qid(text)
        if not qid:
            continue
        title, permalink = parse_front_matter(text)
        if not title:
            title = derive_title_from_filename(name)
        slug = os.path.splitext(name)[0]
        link = build_url(args.base_url, permalink, slug)
        rows.append((qid, title, link))

    os.makedirs(os.path.dirname(args.out) or '.', exist_ok=True)
    with open(args.out, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['Wikidata ID', 'Chicago', 'Chicago link'])
        for qid, title, link in rows:
            w.writerow([qid, title, link])

    print(f"Wrote {args.out} with {len(rows)} rows")


if __name__ == '__main__':
    main()

