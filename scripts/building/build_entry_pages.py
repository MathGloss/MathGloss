#!/usr/bin/env python3
"""Generate static HTML entry pages from a pruned MathGloss database CSV."""

import argparse
import csv
import html
import re
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

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
    <script>
      window.MathJax = {{
        tex: {{inlineMath: [['$', '$'], ['\\(', '\\)']], displayMath: [['$$', '$$'], ['\\[', '\\]']] }},
        svg: {{ fontCache: 'global' }}
      }};
    </script>
    <script src=\"https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js\" async></script>
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


def extract_chicago_slug(url: str) -> Optional[str]:
    if not url:
        return None
    prefixes = [
        'https://mathgloss.github.io/MathGloss/chicago/',
        'http://mathgloss.github.io/MathGloss/chicago/',
        '/chicago/',
    ]
    slug = None
    for prefix in prefixes:
        if url.startswith(prefix):
            slug = url[len(prefix):]
            break
    if slug is None:
        return None
    slug = slug.strip('/')
    if not slug:
        return None
    slug = slug.split('#', 1)[0]
    slug = slug.split('?', 1)[0]
    return slug or None


def parse_chicago_markdown(md_path: Path, slug_to_qid: Dict[str, str]) -> str:
    text = md_path.read_text(encoding='utf-8')
    lines = text.splitlines()
    # Strip YAML front matter if present
    if lines and lines[0].strip() == '---':
        # find next '---'
        try:
            second = lines[1:].index('---') + 1
            lines = lines[second + 1 :]
        except ValueError:
            lines = lines[1:]
    # Drop trailing wikidata id lines
    lines = [line.rstrip() for line in lines]
    lines = [line for line in lines if not line.strip().startswith('Wikidata ID:')]

    def convert_inline(text: str) -> str:
        escaped = html.escape(text, quote=False)

        def repl_bold(match: re.Match) -> str:
            return f"<strong>{match.group(1)}</strong>"

        def repl_link(match: re.Match) -> str:
            label = match.group(1)
            url_raw = match.group(2)
            slug = extract_chicago_slug(url_raw)
            if slug and slug in slug_to_qid:
                target = f"../entries/{slug_to_qid[slug]}.html"
            else:
                target = url_raw
            url = html.escape(target, quote=True)
            return f'<a href="{url}" target="_blank" rel="noopener">{label}</a>'

        escaped = re.sub(r'\*\*(.+?)\*\*', repl_bold, escaped)
        escaped = re.sub(r'\[(.+?)\]\((https?://[^)]+)\)', repl_link, escaped)
        return escaped

    blocks: List[str] = []
    paragraph: List[str] = []
    bullet_items: List[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            text = ' '.join(s.strip() for s in paragraph if s.strip())
            if text:
                blocks.append(f'<p>{convert_inline(text)}</p>')
        paragraph = []

    def flush_list() -> None:
        nonlocal bullet_items
        if bullet_items:
            items_html = '\n'.join(f'<li>{convert_inline(item)}</li>' for item in bullet_items)
            blocks.append(f'<ul>\n{items_html}\n</ul>')
        bullet_items = []

    for raw_line in lines:
        stripped = raw_line.strip()
        if not stripped:
            flush_paragraph()
            flush_list()
            continue
        if stripped.startswith('- '):
            flush_paragraph()
            bullet_items.append(stripped[2:].strip())
        else:
            flush_list()
            paragraph.append(raw_line)

    flush_paragraph()
    flush_list()

    return '\n'.join(blocks)


def load_chicago_definitions(chicago_dir: Path, slug_to_qid: Dict[str, str]) -> Dict[str, str]:
    definitions: Dict[str, str] = {}
    if not chicago_dir.exists():
        return definitions
    for md_path in chicago_dir.glob('*.md'):
        slug = md_path.stem
        try:
            definitions[slug] = parse_chicago_markdown(md_path, slug_to_qid)
        except Exception:
            continue
    return definitions


def get_chicago_html(link: str, definitions: Dict[str, str]) -> Optional[str]:
    if not link:
        return None
    prefix = 'https://mathgloss.github.io/MathGloss/chicago/'
    if link.startswith(prefix):
        slug = link[len(prefix):]
    elif link.startswith('/chicago/'):
        slug = link.split('/chicago/', 1)[1]
    else:
        return None
    slug = slug.strip('/')
    if not slug:
        return None
    return definitions.get(slug)


def build_chicago_slug_to_qid(database_path: Path) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    if not database_path.exists():
        return mapping
    with database_path.open('r', newline='', encoding='utf-8') as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            qid = (row.get('Wikidata ID') or '').strip()
            link = (row.get('Chicago Link') or '').strip()
            slug = extract_chicago_slug(link)
            if qid and slug and slug not in mapping:
                mapping[slug] = qid
    return mapping


def generate_pages(database_path: Path, out_dir: Path, clean: bool, chicago_defs: Dict[str, str]) -> int:
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
        chicago_pair = None
        for pair in source_pairs:
            if pair[0].lower() == 'chicago':
                chicago_pair = pair
                break
        reduced_pairs = [p for p in source_pairs if p != chicago_pair]

        count = 0
        for row in reader:
            qid = (row.get('Wikidata ID') or '').strip()
            if not qid:
                continue
            label = (row.get('Wikidata Label') or qid).strip()
            mathgloss_block = ''
            if chicago_pair is not None:
                chicago_link = (row.get(chicago_pair[2]) or '').strip()
                html_snippet = get_chicago_html(chicago_link, chicago_defs)
                if html_snippet:
                    mathgloss_block = (
                        '    <section class="mathgloss-definition">\n'
                        '      <h2>MathGloss Definition</h2>\n'
                        f'{html_snippet}\n'
                        '    </section>\n'
                    )
            sources_block = build_sources_block(row, reduced_pairs)
            page_html = PAGE_TEMPLATE.format(
                title=html_escape(label),
                qid=html_escape(qid),
                label=html_escape(label),
                sources_block=(mathgloss_block + sources_block)
                if (mathgloss_block or sources_block)
                else '<p>No linked sources yet.</p>',
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
    parser.add_argument('--chicago-dir', default='chicago', help='Path to local Chicago markdown directory')
    args = parser.parse_args()

    db_path = Path(args.database)
    if not db_path.exists():
        raise FileNotFoundError(f'Database CSV not found: {db_path}')

    slug_to_qid = build_chicago_slug_to_qid(db_path)
    chicago_defs = load_chicago_definitions(Path(args.chicago_dir), slug_to_qid)

    out_dir = Path(args.out_dir)
    count = generate_pages(db_path, out_dir, clean=args.clean, chicago_defs=chicago_defs)
    print(f'Generated {count} pages in {out_dir}')


if __name__ == '__main__':
    main()
