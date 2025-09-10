#!/usr/bin/env python3
"""
Extract a Mathlib termlist (title,link) from a saved copy of the
Mathlib Overview page (e.g., https://leanprover-community.github.io/mathlib-overview.html).

Why: The overview’s human-friendly terms (e.g., "vector space") link to the
actual Mathlib docs (often under different names, e.g., modules). We treat
the link text as the user-facing term, and the href as the target doc URL.

Inputs
- --html: path to a saved overview HTML file (download in your browser: Save Page As…)
- --out: CSV path to write (title,link)
- Optional: --base-url to resolve relative links (default autodetect via the HTML’s <base> if present)
- Optional: --allow-path/--allow-domain filters to keep only links to mathlib docs

Workflow
1) Save the overview HTML locally (no network required)
2) Run this script to produce data/mathlib.csv (title,link)
3) Map to Wikidata with scripts/mapper.py --source Mathlib

Notes
- Uses only the Python stdlib (html.parser), no external deps.
"""
import argparse
import csv
import os
import re
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse


class LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []  # list of (href, text)
        self._stack = []
        self._current_href = None
        self._current_text = []
        self._base = None

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'base':
            href = dict(attrs).get('href')
            if href:
                self._base = href
        if tag.lower() == 'a':
            href = dict(attrs).get('href')
            if href:
                self._current_href = href
                self._current_text = []
        self._stack.append(tag.lower())

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == 'a' and self._current_href is not None:
            text = ''.join(self._current_text).strip()
            self.links.append((self._current_href, text))
            self._current_href = None
            self._current_text = []
        if self._stack and self._stack[-1] == tag:
            self._stack.pop()

    def handle_data(self, data):
        if self._current_href is not None:
            self._current_text.append(data)


def normalize_text(s: str) -> str:
    # Collapse whitespace and strip
    return re.sub(r"\s+", " ", s or '').strip()


def should_keep(href: str, text: str, allow_domains, allow_paths) -> bool:
    if not text or len(text) < 2:
        return False
    # Filter by domain/path if provided
    if allow_domains or allow_paths:
        p = urlparse(href)
        dom_ok = (not allow_domains) or (p.netloc in allow_domains)
        path_ok = (not allow_paths) or any(seg in p.path for seg in allow_paths)
        return dom_ok and path_ok
    return True


def resolve_href(href: str, base_url: str | None) -> str:
    if href.startswith('http://') or href.startswith('https://'):
        return href
    if base_url:
        return urljoin(base_url, href)
    return href


def main():
    ap = argparse.ArgumentParser(description='Extract (title,link) pairs from a saved Mathlib overview HTML file.')
    ap.add_argument('--html', required=True, help='Path to saved mathlib-overview HTML file')
    ap.add_argument('--out', required=True, help='Output CSV path (title,link)')
    ap.add_argument('--base-url', required=False, help='Base URL to resolve relative links (optional)')
    ap.add_argument('--allow-domain', action='append', default=[], help='Allowed domain (can repeat). Example: leanprover-community.github.io')
    ap.add_argument('--allow-path', action='append', default=['/mathlib4_docs/'], help='Allowed path substring (can repeat). Default includes /mathlib4_docs/.')
    args = ap.parse_args()

    with open(args.html, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    parser = LinkExtractor()
    parser.feed(html)

    base_url = args.base_url or parser._base

    rows = []
    seen = set()
    for href, text in parser.links:
        text = normalize_text(text)
        href = resolve_href(href, base_url)
        if not should_keep(href, text, set(args.allow_domain or []), set(args.allow_path or [])):
            continue
        key = (text.lower(), href)
        if key in seen:
            continue
        seen.add(key)
        rows.append((text, href))

    os.makedirs(os.path.dirname(args.out) or '.', exist_ok=True)
    with open(args.out, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['title', 'link'])
        w.writerows(rows)

    print(f"Wrote {args.out} with {len(rows)} rows (from {len(parser.links)} links)")


if __name__ == '__main__':
    main()

