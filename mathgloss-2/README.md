# MathGloss 2 (Clean Start)

MathGloss 2 is a clean, modular rebuild of the MathGloss project: a cross‑source glossary of mathematical terms mapped to Wikidata.

Goals
- Minimal, scriptable data pipeline (no hardcoded paths)
- One canonical CSV/JSON database as the source of truth
- Simple, static web UI that reads the CSV
- Optional graph export (Neo4j) as a separate, documented step

Structure
- `data/` — inputs and builds (CSV/JSON)
- `scripts/` — ingestion/build utilities (pure Python, CLI args)
- `web/` — static UI consuming `data/database.csv`
- `docs/` — short guides on schema and pipeline

Quick Start
1) Put per‑source alignment CSVs into `data/alignments/`.
   - Preferred format: `Wikidata ID,<SourceName>,<SourceName link>`
   - Legacy format: `Wikidata ID,<SourceName>` with values that may be plain text, URL, or `[Name](URL)`.
2) Build the merged database: `python scripts/build_database.py --alignments data/alignments --out data/database.csv`
3) Open `web/index.html` in a local server and browse the table

Database Schema
- `Wikidata ID`: The canonical key (e.g. `[Q181296](https://www.wikidata.org/wiki/Q181296)`).
- `Wikidata Label`: Optional label (left blank by builder unless you provide it upstream).
- For each source `<S>`: two columns — `<S> Name`, `<S> Link`.
  - If the alignment value is `[Name](URL)`, the builder splits into Name/Link.
  - If it’s a URL, it becomes `<S> Link` only.
  - If it’s plain text, it becomes `<S> Name` only.

Mapper
- Purpose: Convert a termlist (`title,link[,suggestion]`) into an alignment CSV (`Wikidata ID,<SourceName>`)
- Input: local SQLite index mapping Wikipedia titles → Wikidata IDs (table `mapping`)
- Output alignment columns: `Wikidata ID, <SourceName>, <SourceName link>`
- Usage:
  - `python scripts/mapper.py --db /path/to/index.db --csv termlists/chicago.csv --source Chicago --out data/alignments/chicago_mappings.csv`
  - Optional `--check-wikidata` filters disambiguation/person/theorem/etc. via Wikidata API (network).

Build database from alignments
- `python scripts/build_database.py --alignments data/alignments --out data/database.csv`

Notes
- No network calls in the core pipeline. External enrichment (e.g., Wikidata API, Neo4j) lives in optional scripts.
- Keep everything parameterized via CLI flags.
