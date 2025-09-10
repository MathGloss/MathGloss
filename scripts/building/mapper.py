#!/usr/bin/env python3
"""
Map per-source term lists to Wikidata IDs using a local Wikipedia→Wikidata SQLite index.

Input termlist CSV format:
    title,link[,suggestion]

Output alignment CSV format:
    Wikidata ID,<SourceName> Name,<SourceName> Link
Where <SourceName> is the provided --source.

Notes
- No network calls by default. Optional --check-wikidata will call the Wikidata API
  to filter out disambiguation/people/theorem/etc. types.
  If a suggestion is provided but fails (no match or filtered), the mapper
  falls back to the original title before skipping.
"""
import argparse
import csv
import sqlite3
from typing import List, Optional, Tuple
import re

try:
    import requests  # optional; only used when --check-wikidata is set
except Exception:  # pragma: no cover
    requests = None


# Try general mathematics first, then specific domains (original behavior)
WIKI_CATS = [
    '_(category_theory)', '_(mathematics)', '_(linear_algebra)', '_(algebraic_geometry)',
    '_(algebraic_topology)', '_(commutative_algebra)', '_(field_theory)', '_(game_theory)',
    '_(topology)', '_(differential_geometry)', '_(graph_theory)', '_(group_theory)',
    '_(invariant_theory)', '_(module_theory)', '_(order_theory)', '_(ring_theory)',
    '_(representation_theory)', '_(set_theory)', '_(string_theory)', '_(symplectic geometry)',
    '_(tensor_theory)'
]


class WikiMapper:
    """Query a precomputed Wikipedia→Wikidata SQLite index with table `mapping`.
    Schema expected: mapping(wikipedia_title TEXT, wikidata_id TEXT)
    """
    def __init__(self, path_to_db: str):
        self.conn = sqlite3.connect(path_to_db)

    def title_to_id(self, page_title: str) -> Optional[str]:
        c = self.conn.execute(
            "SELECT wikidata_id FROM mapping WHERE wikipedia_title=?",
            (page_title,)
        )
        row = c.fetchone()
        return row[0] if row and row[0] else None

    # Note: collapsed-key fallback removed for performance and simplicity.

    def id_to_titles(self, wikidata_id: str) -> List[str]:
        c = self.conn.execute(
            "SELECT DISTINCT wikipedia_title FROM mapping WHERE wikidata_id=?",
            (wikidata_id,)
        )
        return [r[0] for r in c.fetchall()]


def _strip_tex_noise(s: str) -> str:
    """Remove simple LaTeX/MathJax adornments from human titles.
    Examples:
    - "$p$-adic number" -> "p-adic number"
    - "\\(x\\)" -> "x"
    - "\\mathbb{R}" -> "R"
    Keeps plain text; aggressively drops $, \\ and braces when used as markup.
    """
    if not s:
        return s
    # Replace math inline $...$ with inner text.
    s = re.sub(r"\$(.*?)\$", r"\1", s)
    # Remove \( ... \) and \[ ... \] wrappers.
    s = re.sub(r"\\\((.*?)\\\)", r"\1", s)
    s = re.sub(r"\\\[(.*?)\\\]", r"\1", s)
    # Replace LaTeX commands with their braced content, if any: \cmd{X} -> X
    s = re.sub(r"\\[A-Za-z]+\{([^}]*)\}", r"\1", s)
    # Drop remaining TeX control sequences like \alpha (keep the name as plain text?)
    # Safer to remove the backslash only: "\\alpha" -> "alpha"
    s = re.sub(r"\\([A-Za-z]+)", r"\1", s)
    # Normalize fancy dashes to ASCII hyphen
    s = s.replace('–', '-').replace('—', '-').replace('−', '-')
    # Remove stray braces and dollar signs if any remain
    s = s.replace('{', '').replace('}', '').replace('$', '')
    # Collapse whitespace
    s = re.sub(r"\s+", " ", s).strip()
    return s


def normalize_title(s: str) -> str:
    # Strip TeX noise then normalize for Wikipedia title lookup
    s = _strip_tex_noise(s)
    s = s.strip().replace(' ', '_')
    if not s:
        return s
    return s[0].upper() + s[1:]


# Note: collapse_key removed (deprecated)


WD_FILTER_IDS = {
    'Q4167410',  # disambiguation page
    'Q5',        # human
    'Q65943',    # theorem
    'Q207505',   # lemma
    'Q108163',   # proposition
    'Q22808320', # human name disambiguation page
    'Q1422068',  # fixed point
    'Q319141',   # conjecture
    'Q1936384',  # branch of science
    'Q13406463', # list of
}


def is_filtered_wikidata_entity(wikidata_id: str) -> bool:
    if requests is None:
        return False
    url = "https://www.wikidata.org/w/api.php"
    params = {"action": "wbgetentities", "ids": wikidata_id, "format": "json"}
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
    except Exception:
        return False
    claims = data.get("entities", {}).get(wikidata_id, {}).get("claims", {})
    for claim in claims.get("P31", []):  # instance of
        val = claim.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("id")
        if val in WD_FILTER_IDS:
            return True
    return False


def get_attempt_terms(row: dict) -> Tuple[str, List[str]]:
    """Return (display_title, attempts) where attempts is [suggestion?, title].
    display_title always uses row['title'] for output markdown link.
    """
    title = (row.get('title') or '').strip()
    suggestion = (row.get('suggestion') or '').strip()
    attempts: List[str] = []
    if suggestion and suggestion != title:
        attempts.append(suggestion)
    attempts.append(title)
    return title, attempts


def lookup(mapper: WikiMapper, term: str) -> Optional[str]:
    """Single-result lookup: try domain-suffixed titles, then exact.
    """
    base = normalize_title(term)
    # try category-suffixed titles first (in configured order)
    for suffix in WIKI_CATS:
        wid = mapper.title_to_id(base + suffix)
        if wid:
            return wid
    # then exact
    wid = mapper.title_to_id(base)
    if wid:
        return wid
    return None


def write_alignment(out_path: str, source_name: str, rows: List[Tuple[str, str, str]]):
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        # Preferred alignment header: Wikidata ID, <SourceName>, <SourceName link>
        w.writerow(['Wikidata ID', f'{source_name}', f'{source_name} link'])
        for qid, name, link in rows:
            # Write plain QID
            w.writerow([qid, name, link])


def main():
    ap = argparse.ArgumentParser(description='Map term list to Wikidata IDs using a local index.')
    ap.add_argument('--db', required=True, help='Path to Wikipedia→Wikidata SQLite index (with table `mapping`).')
    ap.add_argument('--csv', required=True, help='Input termlist CSV (headers: title,link[,suggestion]).')
    ap.add_argument('--source', required=True, help='Source name to use as the alignment column header.')
    ap.add_argument('--out', required=True, help='Output alignment CSV path.')
    ap.add_argument('--check-wikidata', action='store_true', help='Call Wikidata API to filter disambiguations/people/theorems. Optional.')
    args = ap.parse_args()

    mapper = WikiMapper(args.db)

    found: List[Tuple[str, str, str]] = []
    skipped = 0
    with open(args.csv, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        # validate columns
        cols = [c.strip() for c in reader.fieldnames or []]
        if 'title' not in cols or 'link' not in cols:
            raise ValueError('Input CSV must have headers: title,link[,suggestion]')

        for row in reader:
            display_title, attempts = get_attempt_terms(row)
            qid: Optional[str] = None
            for term in attempts:
                if not term:
                    continue
                qid_try = lookup(mapper, term)
                if not qid_try:
                    continue
                if args.check_wikidata and is_filtered_wikidata_entity(qid_try):
                    continue
                qid = qid_try
                break
            if not qid:
                skipped += 1
                continue
            link = (row.get('link') or '').strip()
            found.append((qid, display_title, link))

    write_alignment(args.out, args.source, found)
    print(f"Wrote {args.out}: {len(found)} rows, skipped {skipped}.")


if __name__ == '__main__':
    main()
