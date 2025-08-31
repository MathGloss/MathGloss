# MathGloss

MathGloss is a small, scriptable toolkit for building a cross‑source glossary of mathematical terms and mapping them to Wikidata. It ships with:

- A simple data pipeline for ingesting term lists from various sources
- A mapper, based on [wikimapper](https://github.com/jcklie/wikimapper) that resolves human‑readable titles to Wikidata IDs via a local index
- A merged, canonical database (`data/database.csv`) suitable for a static UI
- A lightweight web UI (`web/`) to browse, filter, and link out to sources

## Repository Layout
- `data/` — inputs and builds (CSV)
  - `data/alignments/` — per‑source mappings: `Wikidata ID,<Source>,<Source link>`
  - `data/database.csv` — merged table across sources
  - `data/database_pruned.csv` — optional pruned table (see Pruning)
- `scripts/` — CLI utilities (pure Python, no hardcoded paths)
- `web/` — static UI that loads `data/database_pruned.csv` (or `database.csv`)

## Prerequisites
- Python 3.10+
- A local SQLite index mapping Wikipedia page titles to Wikidata IDs (table `mapping(wikipedia_title TEXT, wikidata_id TEXT)`). Can be found [here](https://dumps.wikimedia.org/wikidatawiki/entities/)
- Optional: `pdfminer.six` for extracting terms from PDF indices of textbooks; `requests` for pruning by Wikidata properties.

Install optional deps for features you use:
- `python -m pip install pdfminer.six requests`

## Quick Start
1) Prepare per‑source term lists (`title,link[,suggestion]`). Examples below show how to extract these. Suggestion is optional, and usually refers to different word forms of terms you might use to improve the number of Wikidata hits you get.
2) Map each term list to Wikidata IDs using the local index.
3) Merge alignments into a single database.
4) (Optional) Prune out irrelevant entities using the Wikidata API.
5) Open the UI locally or publish via GitHub Pages.

## Ingest: Make term lists

Making term lists is task that has to be specialized to each source. A summary of the sources currently included in MathGloss:

- Mathlib (data/mathlib.csv): parsed from a saved copy of the [Mathlib Overview page](https://leanprover-community.github.io/mathlib-overview.html). Use `scripts/make_mathlib_termlist_from_overview.py` with `--base-url https://leanprover-community.github.io/` to resolve root‑relative links and keep items under `/mathlib4_docs/`.
- nLab (data/nlab.csv): parsed from [all page titles](https://ncatlab.org/nlab/all_pages) in the nLab. Use `scripts/make_nlab_termlist_from_xhtml.py`; anchors filtered to `/nlab/show/` and resolved to absolute URLs.
- Chicago (data/chicago.csv): generated from the local `chicago/` Markdown corpus, which is a collection of definitions from [Lucy's](https://math.berkeley.edu/~lucy/forest/index/index.xml) undergrad notes. Use `scripts/make_chicago_termlist.py --dir chicago --base-url https://mathgloss.github.io/MathGloss/chicago`.
- Context (data/context.csv): extracted from the index of [Category Theory in Context](https://emilyriehl.github.io/files/context.pdf) by [Emily Riehl](https://emilyriehl.github.io) and linked to PDF pages (via `#page=`). Use either `scripts/make_termlist_from_index.py` for LaTeX `.idx/.ind` or `scripts/make_pdf_index_termlist.py` for text‑parsed indices.
- BCT (data/bct.csv): extracted from the index of [Basic Category Theory](https://arxiv.org/abs/1612.09375) by [Tom Leinster](https://webhomes.maths.ed.ac.uk/~tl/) with arXiv PDF page anchors.
- PlanetMath (data/planetmath.csv): parsed from the [PlanetMath alphabetical index](https://planetmath.org/alphabetical.html), then spaces are added by checking each linked page's title.
- Clowder (data/alignments/clowder_mappings.csv): tags from [Emily de Oliveira Santos's](https://topological-modular-forms.github.io) [Clowder Project](https://www.clowderproject.com).

## Map: Term list → Wikidata IDs

Map a term list using a local SQLite index (no network required):
- `python scripts/mapper.py --db /path/to/index.db --csv data/mathlib.csv --source Mathlib --out data/alignments/mathlib_mappings.csv`

Notes
- The mapper tries common disambiguation suffixes (e.g., `_(mathematics)`), then exact title. This is done to 
- It normalizes light math markup (e.g., `$p$-adic` → `p-adic`).
- Optional filter (network): `--check-wikidata` excludes people, disambiguations, theorem‑like pages.
- The mapper is based on [wikimapper](https://github.com/jcklie/wikimapper) by [Jan-Christoph Klie](https://mrklie.com)

Repeat for each `data/<source>.csv` to produce `data/alignments/<source>_mappings.csv`.

## Merge: Build the database

Combine all per‑source alignments into a canonical table. If you provide the index, labels are populated from Wikipedia titles.

- `python scripts/build_database.py --alignments data/alignments --out data/database.csv --db /path/to/index.db`

Output columns
- `Wikidata ID`, `Wikidata Label`
- For each source `S`: `S Name`, `S Link`

## Prune (optional)

Filter out non‑topic entities via Wikidata API (network):

- `python scripts/prune_database.py --in data/database.csv --out data/database_pruned.csv --batch-size 50 --verbose`

What it drops by default (via P31 “instance of”):
- Humans (Q5), disambiguation pages (Q4167410, Q22808320), theorem/lemma/proposition (Q65943, Q207505, Q108163)

Tip: If rate‑limited, reduce `--batch-size` (e.g., 20).

## Browse the UI

Local preview
- `python -m http.server -d . 8000`
- Open `http://localhost:8000/web/` (the UI loads `data/database_pruned.csv` by default).

View online at https://mathgloss.github.io/MathGloss

## License and citation

This toolkit is open source under the LICENSE included in the repo.

If you use MathGloss in research or a project, please consider citing the preprint:

- MathGloss: Building mathematical glossaries from text (Nov 2023) — https://arxiv.org/abs/2311.12649
