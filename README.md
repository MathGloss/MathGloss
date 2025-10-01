# MathGloss

MathGloss is a scriptable toolkit for aligning mathematical knowledge sources
with Wikidata, producing a unified glossary that powers static sites, data
releases, and graph experiments. The project centers on small, composable
"agents"—Python scripts that each own one step of the pipeline and exchange
well-defined CSV artifacts.

## Key Capabilities
- Ingest term lists from textbooks, wikis, lecture notes, and generated
  contexts into a consistent `title,link[,suggestion]` format.
- Map those terms to Wikidata QIDs using a local index or layered label sets,
  then merge the results into a canonical database for consumption by the UI.
- Prune, enrich, and export the database with Wikipedia sitelinks, cached
  labels, and curated filters.
- Generate derived relationship data (e.g., Mathlib extends graphs, Wikidata
  relation edges) and load the concepts into Neo4j for exploratory analysis.

## Repository Overview
- `AGENTS.md` — reference guide for every automation script and how they hand
  work off to each other.
- `data/` — canonical CSVs (`database*.csv`, per-source term lists, alignments,
  relation caches).
  - `data/alignments/` — mapper outputs per source.
  - `data/cache/` — Wikidata label/pruning caches.
  - `data/relations/` — graph exports and LLM-assisted relation caches.
- `scripts/` — Python agents grouped by responsibility.
  - `scripts/other/` — termlist ingest helpers, map tester, utilities.
  - `scripts/building/` — mappers, database builder, label enrichment, pruning.
  - `scripts/graphing/` — graph-oriented tooling (relation fetchers, Neo4j
    loaders, Mathlib extends extraction).
- `layers/` — SPARQL-generated layer CSVs plus the builder script used by the
  experimental mapper.
- `web/` — static user interface that reads the merged/pruned database.

## Setup
1. Use Python 3.10 or newer.
2. Create and activate a virtual environment (`python -m venv .venv && source
   .venv/bin/activate`).
3. Install the core dependencies: `python -m pip install -r requirements.txt`.
   - The list includes `requests` for Wikidata/API calls, the Neo4j Python
     driver for graph loaders, and `ollama` for optional local LLM inference.
4. Obtain a wikimapper-style SQLite index with a `mapping(wikipedia_title TEXT,
   wikidata_id TEXT)` table. Build one with
   [wikimapper](https://github.com/jcklie/wikimapper) or reuse an existing
   index. Point mapper scripts to it via `--db`.
5. When running Neo4j loaders, set `NEO4J_URI`, `NEO4J_USER`, and
   `NEO4J_PASSWORD`, or supply them via CLI flags.

## Standard Pipeline
1. **Ingest term lists** with the relevant agent for each source. Each script
   writes a `title,link` CSV in `data/` (optionally `suggestion`).
2. **Optionally enrich** with `scripts/other/make_clowder_suggestions.py` to
   add heuristic alternate spellings.
3. **Map to Wikidata** using `scripts/building/mapper.py` (SQLite index) or
   `scripts/building/mapper_new.py` (layer-based experiments). Inspect tricky
   cases interactively with `scripts/other/maptest.py`.
4. **Merge alignments** via `scripts/building/build_database.py`, drawing
   labels from the index or the Wikidata API (`--online-labels`).
5. **Augment** with `scripts/building/add_enwiki_links.py` to populate a
   `Wikipedia Link` column.
6. **Prune** using `scripts/building/prune_database.py` to drop humans,
   disambiguations, list articles, broad areas, and science awards by default
   (`Q5`, `Q4167410`, `Q22808320`, `Q13406463`, `Q1936384`, `Q11448906`).
   Additional flags (e.g., `--drop-nlab-only`, `--keep-people`) tailor the
   output to project needs.
7. **Publish** the resulting CSVs (`data/database.csv`,
   `data/database_pruned.csv`, or compiled variants) and update the static UI
   or downstream analyses.

For a script-by-script breakdown, see `AGENTS.md`.

## Term List Agents
- **Mathlib:** `scripts/other/make_mathlib_termlist_from_overview.py` parses a
  saved Mathlib overview HTML file. Use `--base-url` to keep links absolute and
  `--allow-domain`/`--allow-path` to filter stray anchors.
- **nLab:** `scripts/other/make_nlab_termlist_from_xhtml.py` processes the
  exported `all_pages` XHTML listing and keeps `/nlab/show/` entries.
- **Chicago:** `scripts/other/make_chicago_termlist.py` scans the local
  `chicago/` markdown tree, taking the first heading as the title and building
  shareable URLs from a provided base.
- **PDF indices:** `scripts/other/make_termlist_from_index.py` converts LaTeX
  `.idx/.ind` files or text dumps into CSV rows with optional `--page-offset`.
- **Clowder suggestions:** `scripts/other/make_clowder_suggestions.py` adds a
  `suggestion` column that normalizes names for better mapper recall.

## Mapping and Quality Control
- **Index-backed mapper:** `scripts/building/mapper.py` uses the SQLite index
  to resolve titles. Supports per-source naming via `--source`, explicit output
  paths via `--out`, and optional network filters with `--check-wikidata`.
- **Layer mapper:** `scripts/building/mapper_new.py` compares normalized titles
  against the `layers/` CSVs or a prebuilt catalog.
- **Layer catalog helper:** `scripts/building/build_layer_catalog.py` speeds up
  repeated layer-based runs by precomputing token indexes.
- **Map tester:** `scripts/other/maptest.py` lets you probe mapper outcomes for
  sample strings before large batch jobs.

## Database Assembly and Post-Processing
- **Merger:** `scripts/building/build_database.py` aggregates per-source
  alignments under `data/alignments/` and hydrates human-readable labels from
  the index or live Wikidata lookups. Caches persist in `data/cache/` when
  `--cache` is provided.
- **Wikipedia linker:** `scripts/building/add_enwiki_links.py` fills the
  `Wikipedia Link` column using batched Wikidata API calls; safe to re-run.
- **Pruner:** `scripts/building/prune_database.py` filters out unwanted QIDs
  and supports additional toggles such as `--drop-nlab-only` and
  `--keep-disambiguations`.

## Relationship and Graph Tooling
- **Wikidata relation fetcher:** `scripts/graphing/fetch_relations.py` issues
  SPARQL queries for pairs of concepts in the compiled database, producing
  `data/relations/graph_edges.csv` and caches to skip repeated calls.
- **Neo4j loaders:**
  - `scripts/graphing/load_mentions_to_neo4j.py` inserts concept and mention
    nodes, batching data from the compiled/pruned database.
  - `scripts/graphing/load_relations_to_neo4j.py` pushes relation edges into
    Neo4j, optionally reading cached results.
- **Mathlib extends extraction:**
  - `scripts/graphing/mathlib_extends_relations.py` walks Mathlib declaration
    URLs to discover Lean `extends` hierarchies and map them back to MathGloss
    entries, writing detailed relations plus optional `*_edges.csv` exports.
  - `scripts/graphing/chicago_relationship_inference.py` and
    `scripts/graphing/nlab_relationship_inference.py` leverage cached LLM
    outputs under `data/relations/` to infer subclass links between non-Mathlib
    sources.
- **Support utilities:** `scripts/graphing/concept_extractor.py` normalizes
  markdown links, and `scripts/graphing/mathlib_statement_lookup.py` resolves
  Mathlib doc URLs to Lean declarations.

## Web UI
Serve the static site locally with `python -m http.server -d . 8000` and open
`http://localhost:8000/web/`. The UI defaults to `data/database_pruned.csv` but
can be pointed at other compiled CSVs by editing `web/index.html`.

## Additional Documentation
- `AGENTS.md` — authoritative agent reference and pipeline hand-off guide.
- `NatFoM slides.pdf` — presentation deck summarizing project goals.
- Source directories (`chicago/`, `entries/`) host the raw content used when
  generating term lists.

## License and Citation

MathGloss is released under the repository's LICENSE. If you draw on MathGloss
in a publication, please cite:

- MathGloss: Building mathematical glossaries from text (Nov 2023).
  https://arxiv.org/abs/2311.12649

