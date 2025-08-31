#!/usr/bin/env python3
"""
Generate a Chicago termlist CSV (title,link) from the local Chicago corpus of Markdown files.

Strategy
- Title: first H1 in the file ("# ...") if present; otherwise derive from filename by
  replacing underscores/dashes with spaces.
- Link: <base-url>/<slug> where slug is the filename without extension.

Usage
  python scripts/make_chicago_termlist.py \
    --dir /path/to/corpus \
    --base-url https://mathgloss.github.io/MathGloss/chicago \
    --out data/chicago.csv
"""
import argparse
import csv
import os


def derive_title_from_filename(path: str) -> str:
    stem = os.path.splitext(os.path.basename(path))[0]
    return stem.replace('_', ' ').replace('-', ' ').strip()


def extract_h1_title(path: str) -> str | None:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                s = line.strip()
                if s.startswith('#'):
                    # remove leading hashes and whitespace
                    title = s.lstrip('#').strip()
                    return title if title else None
    except Exception:
        return None
    return None


def build_termlist(src_dir: str, base_url: str) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for root, _, files in os.walk(src_dir):
        for name in sorted(files):
            if not name.lower().endswith('.md'):
                continue
            full = os.path.join(root, name)
            slug = os.path.splitext(name)[0]
            link = f"{base_url.rstrip('/')}/{slug}"
            title = extract_h1_title(full) or derive_title_from_filename(full)
            if title:
                rows.append((title, link))
    return rows


def main():
    ap = argparse.ArgumentParser(description='Create a termlist (title,link) from Markdown files.')
    ap.add_argument('--dir', required=True, help='Directory containing .md files')
    ap.add_argument('--base-url', required=True, help='Base URL for links (no trailing slash)')
    ap.add_argument('--out', required=True, help='Output CSV path (title,link)')
    args = ap.parse_args()

    rows = build_termlist(args.dir, args.base_url)
    os.makedirs(os.path.dirname(args.out) or '.', exist_ok=True)
    with open(args.out, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['title', 'link'])
        w.writerows(rows)
    print(f"Wrote {args.out} ({len(rows)} rows)")


if __name__ == '__main__':
    main()
