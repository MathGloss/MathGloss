#!/usr/bin/env python3
"""
Extract an nLab termlist (title,link) from a saved XHTML page that lists all pages.

Inputs
- --xhtml: path to the saved nLab "All pages" XHTML (e.g., nlab.xhtml)
- --out: CSV path to write (title,link)
- Optional: --base-url to resolve root-relative links (default: https://ncatlab.org)
- Optional: --allow-path filters (default: /nlab/show/)

Notes
- Uses only Python stdlib (html.parser, urllib). No network calls.
- Deduplicates by (lowercased title, absolute link).
"""
import argparse
import csv
import os
import re
from html import unescape
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse


class LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links: list[tuple[str, str]] = []  # (href, text)
        self._in_a = False
        self._href: str | None = None
        self._text_parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'a':
            href = dict(attrs).get('href')
            if href:
                self._in_a = True
                self._href = href
                self._text_parts = []

    def handle_endtag(self, tag):
        if tag.lower() == 'a' and self._in_a and self._href is not None:
            text = unescape(''.join(self._text_parts)).strip()
            self.links.append((self._href, text))
            self._in_a = False
            self._href = None
            self._text_parts = []

    def handle_data(self, data):
        if self._in_a:
            self._text_parts.append(data)


def normalize_text(s: str) -> str:
    s = unescape(s or '')
    s = s.replace('\xa0', ' ')
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def should_keep(href: str, allow_paths: set[str]) -> bool:
    if not allow_paths:
        return True
    p = urlparse(href)
    path = p.path or href  # support raw relative
    return any(seg in path for seg in allow_paths)


def main():
    ap = argparse.ArgumentParser(description='Extract (title,link) pairs from nLab "All pages" XHTML.')
    ap.add_argument('--xhtml', required=True, help='Path to saved nLab XHTML (all pages)')
    ap.add_argument('--out', required=True, help='Output CSV path (title,link)')
    ap.add_argument('--base-url', default='https://ncatlab.org', help='Base URL to resolve root-relative links')
    ap.add_argument('--allow-path', action='append', default=['/nlab/show/'], help='Allowed path substring (repeatable). Default: /nlab/show/')
    args = ap.parse_args()

    with open(args.xhtml, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    parser = LinkExtractor()
    parser.feed(html)

    rows: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for href, text in parser.links:
        if not text:
            continue
        if not should_keep(href, set(args.allow_path or [])):
            continue
        title = normalize_text(text)
        link = urljoin(args.base_url, href)
        key = (title.lower(), link)
        if key in seen:
            continue
        seen.add(key)
        rows.append((title, link))

    os.makedirs(os.path.dirname(args.out) or '.', exist_ok=True)
    with open(args.out, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['title', 'link'])
        w.writerows(rows)

    print(f"Wrote {args.out} with {len(rows)} rows (parsed {len(parser.links)} anchors)")


if __name__ == '__main__':
    main()

