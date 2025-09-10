#!/usr/bin/env python3
"""
Create suggestion strings for Clowder rows.

Input CSV headers: title,link
Output CSV headers: title,link,suggestion

Transformation pipeline (on the part after the first colon in title):
- Replace dashes with spaces
- Remove leading articles (a, an, the)
- Singularize simple English plurals (heuristic)
- Capitalize common eponym names (Banach, Tarski, Cauchy, ...)

Usage:
  python scripts/make_clowder_suggestions.py --in data/clowder_title_link.csv --out data/clowder_title_link_suggested.csv
  python scripts/make_clowder_suggestions.py --in data/clowder_title_link.csv --in-place
"""
import argparse
import csv
import os
import re
from typing import List, Dict, Tuple, Any


STOPWORDS = {
    'of', 'and', 'or', 'in', 'on', 'for', 'with', 'to', 'from', 'by',
    'at', 'as', 'via', 'without', 'within', 'between', 'over', 'under',
}


# A lightweight list of common eponym names in mathematics to capitalize
EPONYMS = {
    'banach', 'tarski', 'cauchy', 'lebesgue', 'riemann', 'gauss', 'euler',
    'galois', 'noether', 'hilbert', 'cantor', 'hausdorff', 'borel', 'jordan',
    'zorn', 'sylow', 'abel', 'lie', 'weyl', 'pontryagin', 'chebyshev', 'dirichlet',
    'fourier', 'fubini', 'stokes', 'green', 'lagrange', 'markov', 'kolmogorov',
    'taylor', 'sobolev', 'hadamard', 'hopf', 'kuratowski', 'dehn', 'carathéodory',
    'caratheodory', 'feynman', 'mahler', 'menger', 'nakayama', 'wiener', 'weierstrass',
    'krull', 'artin', 'grothendieck', 'serre', 'schwarz', 'schwartz', 'koch', 'noetherian',
}


def after_colon(title: str) -> str:
    if ':' in title:
        return title.split(':', 1)[1]
    return title


def remove_leading_article(s: str) -> str:
    s = s.strip()
    for art in ("the ", "a ", "an "):
        if s.lower().startswith(art):
            return s[len(art):]
    return s


_re_ies = re.compile(r"([A-Za-z]+)ies$")
_re_es = re.compile(r"([A-Za-z]+)(ches|shes|sses|xes|zes)$")
_re_s = re.compile(r"([A-Za-z]+)s$")


def singularize_token(tok: str) -> str:
    t = tok
    if not t or len(t) <= 2:
        return t
    low = t.lower()
    # Don't touch obvious non-plurals
    if low.endswith('ss') or low.endswith('us') or low.endswith('is'):
        return t
    m = _re_ies.match(low)
    if m:
        return m.group(1) + 'y'
    m = _re_es.match(low)
    if m:
        return m.group(1)
    # -men -> -man
    if low.endswith('men') and len(low) > 3:
        return t[:-3] + 'man'
    # children -> child (rare)
    if low == 'children':
        return 'child'
    # generic -s
    m = _re_s.match(low)
    if m:
        return m.group(1)
    return t


def suggest(raw_title: str) -> str:
    # portion after colon, replace dashes by spaces
    s = after_colon(raw_title or '')
    s = s.replace('-', ' ')
    # drop leading section/subsection markers if present
    s_stripped = s.strip()
    first, rest = (s_stripped.split(None, 1) + [""])[:2] if s_stripped else ("", "")
    if first.lower() in {"section", "subsection"}:
        s = rest
    s = remove_leading_article(s)
    # tokenize on spaces
    tokens = [t for t in re.split(r"\s+", s.strip()) if t]
    if not tokens:
        return ''
    out: List[str] = []
    for idx, tok in enumerate(tokens):
        low = tok.lower()
        # Skip capitalization on stopwords unless it's the first word
        if idx == 0 and low in {'a', 'an', 'the'}:
            # should not happen due to removal, but safe
            continue
        # singularize base token (lowercase for consistency of heuristic)
        base = singularize_token(low)
        # capitalize eponyms
        if base in EPONYMS:
            out.append(base.capitalize())
            continue
        # keep stopwords lowercase, else keep base as-is
        if base in STOPWORDS:
            out.append(base)
        else:
            out.append(base)
    return ' '.join(out).strip()


def process(inp: str, outp: str) -> int:
    with open(inp, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    for r in rows:
        title = (r.get('title') or '').strip()
        r['suggestion'] = suggest(title)
    os.makedirs(os.path.dirname(outp) or '.', exist_ok=True)
    with open(outp, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'link', 'suggestion'])
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def _post_colon_first_token(title: str) -> str:
    s = title.split(':', 1)[1] if ':' in title else title
    s = s.strip().replace('-', ' ')
    return (s.split()[0].lower() if s else '')


def dedupe_by_suggestion(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # Map suggestion -> (row_index, row_dict, starts_with_section)
    chosen: Dict[str, Tuple[int, Dict[str, Any], bool]] = {}
    for idx, r in enumerate(rows):
        s = (r.get('suggestion') or '').strip()
        title = (r.get('title') or '').strip()
        first = _post_colon_first_token(title)
        starts_with_section = first in {'section', 'subsection'}
        if s not in chosen:
            chosen[s] = (idx, r, starts_with_section)
        else:
            prev_idx, prev_row, prev_is_section = chosen[s]
            # Prefer the one that is NOT section/subsection
            if prev_is_section and not starts_with_section:
                chosen[s] = (idx, r, starts_with_section)
            # else keep the previous (stable)
    kept = sorted(chosen.values(), key=lambda t: t[0])
    return [r for _, r, _ in kept]


def main():
    ap = argparse.ArgumentParser(description='Generate suggestion column for Clowder title/link CSV')
    ap.add_argument('--in', dest='inp', required=True, help='Input CSV (headers: title,link)')
    ap.add_argument('--out', dest='out', help='Output CSV path (default: *_suggested.csv or *_suggested_dedup.csv when --dedupe)')
    ap.add_argument('--in-place', action='store_true', help='Overwrite input file with suggestion column added')
    ap.add_argument('--dedupe', action='store_true', help='Deduplicate rows by suggestion, preferring non-section titles')
    args = ap.parse_args()

    if args.in_place and args.out:
        ap.error('Use either --in-place or --out, not both.')
    # Choose default output name depending on --dedupe
    default_out = os.path.splitext(args.inp)[0] + ('_suggested_dedup.csv' if args.dedupe else '_suggested.csv')
    outp = args.inp if args.in_place else (args.out or default_out)

    # Load, suggest, optional dedupe, write
    with open(args.inp, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    for r in rows:
        title = (r.get('title') or '').strip()
        r['suggestion'] = suggest(title)
    if args.dedupe:
        before = len(rows)
        rows = dedupe_by_suggestion(rows)
        after = len(rows)
    else:
        before = after = len(rows)
    os.makedirs(os.path.dirname(outp) or '.', exist_ok=True)
    with open(outp, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'link', 'suggestion'])
        writer.writeheader()
        writer.writerows(rows)
    if args.dedupe:
        print(f'Wrote {outp}: {after} rows with suggestions (deduped from {before})')
    else:
        print(f'Wrote {outp}: {after} rows with suggestions')


if __name__ == '__main__':
    main()
