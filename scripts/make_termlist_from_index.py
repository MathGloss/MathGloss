#!/usr/bin/env python3
r"""
Extract terms from a LaTeX index (.idx) and build a termlist CSV (title,link).

Intended for sources like "Category Theory in Context" where you can compile
the TeX and generate an index.

Workflow to produce .idx:
 1) Ensure the preamble includes: \usepackage{makeidx} and \makeindex
 2) Near the end: \printindex
 3) Build: pdflatex context.tex && makeindex context.idx && pdflatex context.tex
 4) The file context.idx (and context.ind) will be in the same directory.

This script parses the .idx (or .ind) entries of form:
   \indexentry{term|...}{42}
   \indexentry{group!abelian}{17}

It maps nested entries like "group!abelian" to a human title like "abelian group"
(one-level inversion). It collects the first page where a term appears and writes
title,link rows where link = <pdf-url>#page=<page+offset>.

Usage
  python scripts/extract_index_terms.py \
    --idx /path/to/context.idx \
    --pdf-url https://example.org/context.pdf \
    --out data/context.csv \
    [--page-offset 0]
"""
import argparse
import csv
import os
import re
from collections import OrderedDict


IDX_ENTRY_RE = re.compile(r"\\indexentry\{(?P<term>.+?)\}\{(?P<page>\d+)\}")
ITEM_RE = re.compile(r"^\s*\\item\s+(.+?),\s*\\hyperpage\{([^}]*)\}")
SUBITEM_RE = re.compile(r"^\s*\\subitem\s+(.+?),\s*\\hyperpage\{([^}]*)\}")
SUBSUBITEM_RE = re.compile(r"^\s*\\subsubitem\s+(.+?),\s*\\hyperpage\{([^}]*)\}")


def clean_term(raw: str) -> str:
    # Strip any |... directives (e.g., |textbf, |hyperpage)
    term = raw.split('|', 1)[0]
    # Handle @ display text: use the portion after '@' if present in each component
    def display_of(s: str) -> str:
        s = s.strip()
        if '@' in s:
            left, right = s.split('@', 1)
            return right.strip() or left.strip()
        return s

    # Handle subentries separated by '!': parent!child
    parts = [display_of(p) for p in term.split('!') if p.strip()]
    if parts:
        if len(parts) >= 2:
            parent = parts[-2]
            child = parts[-1]
            # If child ends with a trailing hyphen marker (e.g., "natural -", "dual -", "graph of -"),
            # reverse order and drop the trailing hyphen.
            if re.search(r"\s*-\s*$", child):
                child_clean = re.sub(r"\s*-\s*$", "", child).strip()
                term = f"{child_clean} {parent}"
            else:
                term = f"{parent} {child}"
        else:
            term = parts[-1]
    else:
        term = term.strip()

    # Remove simple TeX formatting commands like \emph{...}, \textbf{...}
    term = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", term)
    # Remove inline math $...$
    term = re.sub(r"\$(.*?)\$", r"\1", term)
    # Remove braces
    term = term.replace('{', '').replace('}', '')
    # Collapse whitespace
    term = re.sub(r"\s+", " ", term).strip()
    return term


def parse_idx(path: str) -> list[tuple[str, int]]:
    rows: list[tuple[str, int]] = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            m = IDX_ENTRY_RE.search(line)
            if not m:
                continue
            raw = m.group('term')
            page = int(m.group('page'))
            term = clean_term(raw)
            if term:
                rows.append((term, page))
    return rows


def _first_page_number(pages: str) -> int | None:
    # pages may be like '159--164', '100, 101', or roman numerals 'ix'
    m = re.search(r"\d+", pages)
    if m:
        try:
            return int(m.group(0))
        except Exception:
            return None
    return None


def parse_ind(path: str) -> list[tuple[str, int]]:
    rows: list[tuple[str, int]] = []
    current_parent: str | None = None
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.rstrip()
            # Skip section separators
            if line.strip() == '' or line.strip() == '\\indexspace':
                continue
            m_item = ITEM_RE.search(line)
            if m_item:
                raw_term, page_s = m_item.group(1), m_item.group(2)
                term = clean_term(raw_term)
                current_parent = term
                page = _first_page_number(page_s)
                if term and page is not None:
                    rows.append((term, page))
                continue
            m_sub = SUBITEM_RE.search(line) or SUBSUBITEM_RE.search(line)
            if m_sub:
                raw_sub, page_s = m_sub.group(1), m_sub.group(2)
                sub = clean_term(raw_sub)
                page = _first_page_number(page_s)
                if not sub or page is None:
                    continue
                if current_parent:
                    # If sub already mentions parent (case-insensitive substring), keep as-is
                    low_parent = current_parent.lower()
                    low_sub = sub.lower()
                    if low_parent in low_sub:
                        term = sub
                    else:
                        term = f"{sub} {current_parent}"
                else:
                    term = sub
                rows.append((term, page))
                continue
            # ignore other lines (e.g., \hyperindexformat{\see ...})
    return rows


def select_first_pages(entries: list[tuple[str, int]]) -> OrderedDict:
    first: OrderedDict[str, int] = OrderedDict()
    for term, page in entries:
        key = term.lower()
        if key not in first:
            first[key] = page
    # Return with original casing (best-effort): map back lower->original
    result: OrderedDict[str, int] = OrderedDict()
    for key, page in first.items():
        # Find a representative original casing
        for term, p in entries:
            if term.lower() == key:
                result[term] = page
                break
    return result


def main():
    ap = argparse.ArgumentParser(description='Extract termlist (title,link) from LaTeX .idx index file.')
    ap.add_argument('--idx', required=True, help='Path to .idx (or .ind) file')
    ap.add_argument('--pdf-url', required=True, help='Base URL to the compiled PDF (used for #page= links)')
    ap.add_argument('--out', required=True, help='Output CSV path (title,link)')
    ap.add_argument('--page-offset', type=int, default=0, help='Offset to add to index page numbers to match PDF pages (default 0)')
    args = ap.parse_args()

    # Choose parser based on content
    with open(args.idx, 'r', encoding='utf-8', errors='ignore') as _f:
        head = _f.read(4096)
    if '\\indexentry' in head:
        entries = parse_idx(args.idx)
    else:
        entries = parse_ind(args.idx)
    first_pages = select_first_pages(entries)

    os.makedirs(os.path.dirname(args.out) or '.', exist_ok=True)
    with open(args.out, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['title', 'link'])
        for title, page in first_pages.items():
            link = f"{args.pdf_url}#page={page + args.page_offset}"
            w.writerow([title, link])

    print(f"Wrote {args.out} with {len(first_pages)} terms (from {len(entries)} index entries)")


if __name__ == '__main__':
    main()
