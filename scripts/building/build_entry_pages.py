#!/usr/bin/env python3
"""Generate static HTML entry pages from a pruned MathGloss database CSV."""

import argparse
import csv
import html
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
    <title>{title} — MathGloss</title>
    <link rel=\"stylesheet\" href=\"../web/styles.css\" />
    <style>
      body {{ max-width: 780px; margin: 24px auto; padding: 0 16px; }}
      nav {{ margin-bottom: 20px; }}
      nav a {{ text-decoration: none; font-size: 0.95rem; }}
      .wikidata-meta {{ margin-bottom: 24px; }}
      .wikidata-meta dt {{ font-weight: bold; }}
      .wikidata-meta dd {{ margin: 0 0 8px 0; }}
      .sources h2 {{ margin-top: 32px; }}
      .sources ul {{ list-style: disc; padding-left: 20px; }}
      .sources li {{ margin-bottom: 8px; }}
    </style>
  </head>
  <body>
    <nav><a href=\"../web/\">← Back to index</a></nav>
    <h1>{title}</h1>
    <section class=\"wikidata-meta\">
      <dl>
        <dt>Wikidata ID</dt>
        <dd><a href=\"https://www.wikidata.org/wiki/{qid}\" target=\"_blank\" rel=\"noopener\">{qid}</a></dd>
        <dt>Label</dt>
        <dd>{label}</dd>
      </dl>
    </section>
    {sources_block}
  </body>
</html>
"""

SOURCES_TEMPLATE = """<section class=\"sources\">\n      <h2>Sources</h2>\n      <ul>\n{items}\n      </ul>\n    </section>\n"""

SOURCE_ITEM_TEMPLATE = "        <li><strong>{source}</strong>: <a href=\"{link}\" target=\"_blank\" rel=\"noopener\">{name}</a></li>"


def html_escape(value: str) -> str:
    return html.escape(value or "", quote=True)


def detect_sources(headers: Iterable[str]) -> List[Tuple[str, str, str]]:
    header_set = set(headers)
    pairs: List[Tuple[str, str, str]] = []
    for header in headers:
        if not header.endswith(" Name"):
            continue
        base = header[:-5]
        link_header = f"{base} Link"
        if link_header in header_set:
            pairs.append((base, header, link_header))
    return pairs


def build_sources_block(row: Dict[str, str], source_pairs: List[Tuple[str, str, str]]) -> str:
    items: List[str] = []
    for source, name_key, link_key in source_pairs:
        name = (row.get(name_key) or "").strip()
        link = (row.get(link_key) or "").strip()
        if not (name and link):
            continue
        items.append(
            SOURCE_ITEM_TEMPLATE.format(
                source=html_escape(source),
                name=html_escape(name),
                link=html_escape(link),
            )
        )
    if not items:
        return ""
    return SOURCES_TEMPLATE.format(items="\n".join(items))


def generate_pages(database_path: Path, out_dir: Path, clean: bool) -> int:
    if clean and out_dir.exists():
        for path in out_dir.iterdir():
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                # avoid deleting nested dirs recursively; skip for safety
                continue
    out_dir.mkdir(parents=True, exist_ok=True)

    with database_path.open('r', newline='', encoding='utf-8') as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError('Input CSV is missing headers.')
        source_pairs = detect_sources(reader.fieldnames)

        count = 0
        for row in reader:
            qid = (row.get('Wikidata ID') or '').strip()
            if not qid:
                continue
            label = (row.get('Wikidata Label') or qid).strip()
            sources_block = build_sources_block(row, source_pairs)
            page_html = PAGE_TEMPLATE.format(
                title=html_escape(label),
                qid=html_escape(qid),
                label=html_escape(label),
                sources_block=sources_block or '<p>No linked sources yet.</p>',
            )
            out_path = out_dir / f'{qid}.html'
            out_path.write_text(page_html, encoding='utf-8')
            count += 1
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description='Generate HTML entry pages from a pruned database CSV.')
    parser.add_argument('--database', required=True, help='Path to pruned database CSV')
    parser.add_argument('--out-dir', required=True, help='Directory to write HTML pages into')
    parser.add_argument('--clean', action='store_true', help='Remove existing files in the output directory before generating pages')
    args = parser.parse_args()

    db_path = Path(args.database)
    if not db_path.exists():
        raise FileNotFoundError(f'Database CSV not found: {db_path}')

    out_dir = Path(args.out_dir)
    count = generate_pages(db_path, out_dir, clean=args.clean)
    print(f'Generated {count} pages in {out_dir}')


if __name__ == '__main__':
    main()
