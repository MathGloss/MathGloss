#!/usr/bin/env python3
"""
Extract a termlist (title,link) from a PDF index (non-LaTeX) by text‑parsing
the index. You can either provide a page range of the index inside a full book
PDF, or simply pass an index‑only PDF and let the script parse all its pages.

Requirements: pdfminer.six (pure Python)

Usage
  # Full book PDF + index page range
  python3 scripts/make_pdf_index_termlist.py \
    --pdf /path/to/topoi_full.pdf \
    --pdf-url https://example.org/topoi_full.pdf \
    --index-start 345 --index-end 372 \
    --out data/topoi.csv \
    [--page-offset 0]

  # Index‑only PDF (no start/end needed)
  python3 scripts/make_pdf_index_termlist.py \
    --pdf /path/to/topoi_index.pdf \
    --pdf-url https://example.org/topoi_full.pdf \
    --out data/topoi.csv \
    [--page-offset 0]

Notes
- --index-start/--index-end are 1-based PDF page numbers for the index section.
- --page-offset lets you adjust anchors if your viewer counts pages differently
  (e.g., to account for front matter).
"""
import argparse
import csv
import os
import re
from collections import OrderedDict
from typing import List, Tuple

from pdfminer.high_level import extract_text


def extract_index_text(pdf_path: str, start: int | None, end: int | None) -> str:
    # pdfminer uses 0-based page_numbers; if no range is provided, parse all pages
    if start is not None and end is not None:
        pages = list(range(max(0, start - 1), max(0, end)))
        return extract_text(pdf_path, page_numbers=pages)
    return extract_text(pdf_path)


def normalize_line(line: str) -> str:
    # Replace leader dots and multiple spaces
    s = re.sub(r"\.{2,}", " ", line)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def parse_index_lines(text: str) -> List[Tuple[str, int]]:
    rows: List[Tuple[str, int]] = []
    for raw in text.splitlines():
        line = normalize_line(raw)
        if not line:
            continue
        # Skip guidance lines
        low = line.lower()
        if low.startswith('see ') or ', see ' in low or 'see also' in low:
            continue
        # Heuristic split: split at the comma before the portion that contains digits
        term = None
        pages_part = None
        m = re.match(r"^(?P<term>.*?),(?P<rest>[^,]*\d.*)$", line)
        if m:
            term = m.group('term').strip(' ,;')
            pages_part = m.group('rest').strip()
        else:
            # fallback: find first digit and split
            d = re.search(r"\d", line)
            if d:
                term = line[:d.start()].strip(' ,;')
                pages_part = line[d.start():]
        if not term or not pages_part:
            continue
        # Pick first integer page
        pm = re.search(r"(\d{1,4})", pages_part)
        if not pm:
            continue
        try:
            page = int(pm.group(1))
        except ValueError:
            continue
        # Clean term of trailing commas
        term = term.strip(' ,;')
        if term:
            rows.append((term, page))
    return rows


def first_pages(entries: List[Tuple[str, int]]) -> OrderedDict:
    seen: OrderedDict[str, int] = OrderedDict()
    for term, page in entries:
        key = term.lower()
        if key not in seen:
            seen[key] = page
    # Map back to original casing (first occurrence)
    out: OrderedDict[str, int] = OrderedDict()
    for key, page in seen.items():
        for term, p in entries:
            if term.lower() == key:
                out[term] = page
                break
    return out


def main():
    ap = argparse.ArgumentParser(description='Extract termlist (title,link) from a PDF index page range.')
    ap.add_argument('--pdf', required=True, help='Path to PDF file')
    ap.add_argument('--pdf-url', required=True, help='Base URL to the PDF (used for #page= links)')
    ap.add_argument('--index-start', type=int, required=False, help='1-based start page of the index (omit for index-only PDFs)')
    ap.add_argument('--index-end', type=int, required=False, help='1-based end page (inclusive) of the index (omit for index-only PDFs)')
    ap.add_argument('--out', required=True, help='Output CSV path (title,link)')
    ap.add_argument('--page-offset', type=int, default=0, help='Offset to add to page numbers for the URL anchor')
    args = ap.parse_args()

    text = extract_index_text(args.pdf, args.index_start, args.index_end)
    entries = parse_index_lines(text)
    first = first_pages(entries)

    os.makedirs(os.path.dirname(args.out) or '.', exist_ok=True)
    with open(args.out, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['title', 'link'])
        for title, page in first.items():
            link = f"{args.pdf_url}#page={page + args.page_offset}"
            w.writerow([title, link])
    print(f"Wrote {args.out} with {len(first)} terms (parsed {len(entries)} entries)")


if __name__ == '__main__':
    main()
