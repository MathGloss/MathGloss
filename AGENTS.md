# MathGloss Agents

MathGloss leans on a handful of single-purpose automation scripts. Treat each script as an "agent" that owns a step in the data pipeline. This document summarizes what is available, where it lives, and how the agents hand work off to each other.

## Quick Reference
| Agent | Location | Role | Inputs | Outputs | Network |
| --- | --- | --- | --- | --- | --- |
| Mathlib termlist ingestor | `scripts/other/make_mathlib_termlist_from_overview.py` | Parse a saved Mathlib overview HTML page into a `title,link` CSV | Saved HTML, optional base URL, domain/path filters | `data/mathlib.csv` | No |
| nLab termlist ingestor | `scripts/other/make_nlab_termlist_from_xhtml.py` | Crawl an exported nLab listing and keep `/nlab/show/` pages | Downloaded XHTML export | `data/nlab.csv` | No |
| Chicago termlist ingestor | `scripts/other/make_chicago_termlist.py` | Derive titles from Markdown lecture notes and mint shareable links | Local `chicago/` Markdown tree, base URL | `data/chicago.csv` | No |
| PDF index termlist agent | `scripts/other/make_termlist_from_index.py` | Turn LaTeX/PDF index dumps into `title,link` rows with `#page=` anchors | `.idx/.ind` or PDF-derived text, base URL | `data/context.csv`, `data/bct.csv`, etc. | No |
| Clowder suggestion agent | `scripts/other/make_clowder_suggestions.py` | Enrich termlists with heuristic suggestions for harder Wikidata lookups | `title,link` CSV | `title,link,suggestion` CSV | No |
| Wikidata mapper (index) | `scripts/building/mapper.py` | Resolve human-readable titles to Wikidata QIDs via local SQLite index | Termlist CSV, SQLite index, optional suggestions | Alignment CSV in `data/alignments/` | No (optional API filters) |
| Wikidata mapper (layer sets) | `scripts/building/mapper_new.py` | Match titles to experimental layer label sets using letter-only normalization | Termlist CSV, `experiments/layer*.csv` (or legacy JSON) | Match + miss CSVs in `data/alignments/new/` | No |
| Map tester | `scripts/other/maptest.py` | Spot-check mapper results interactively or for specific terms | SQLite index, test terms | Console diagnostics | No |
| Alignment merger | `scripts/building/build_database.py` | Merge per-source alignments and hydrate labels | Alignment CSV dir, optional index or online labels | `data/database.csv` | Optional (for online labels) |
| Wikipedia linker | `scripts/building/add_enwiki_links.py` | Fetch English sitelinks to add `Wikipedia Link` column | `data/database*.csv` | Updated CSV with link column | Yes |
| Pruner | `scripts/building/prune_database.py` | Drop humans/disambiguations (and optionally nLab-only rows) via P31 types | `data/database.csv` | `data/database_pruned.csv` | Yes |
| Layer builder | `experiments/labels.py` | Generate layered QID/label CSVs from seed concepts via SPARQL | Seed list or layer CSV | `experiments/layer*.csv` | Yes |
| Layer catalog builder | `scripts/building/build_layer_catalog.py` | Pack layer CSVs into a reusable JSON catalog with normalized forms | `experiments/layer*.csv` | `experiments/layer_catalog.json` | No |

## Agent Hand-Offs and Typical Flow
1. **Ingest termlists** using one or more ingest agents. Each writes a `title,link` CSV under `data/`.
2. **Optionally enrich** termlists with the Clowder suggestion agent if you want a third column that nudges the mapper toward alternate spellings.
3. **Map to Wikidata** via the mapper agent best suited to the task:
   - `scripts/building/mapper.py` for the standard pipeline (needs the local SQLite index; use `--check-wikidata` only when you can afford network calls).
   - `scripts/building/mapper_new.py` when experimenting with the layered label sets stored in `experiments/`.
4. **Inspect or debug mappings** with the map tester agent before committing bulk results.
5. **Merge alignments** with `build_database.py` once each source has a `data/alignments/<source>_mappings.csv` file. Supply either `--db` (preferred) or `--online-labels [--cache ...]` if the index is unavailable.
6. **Add Wikipedia sitelinks** via `add_enwiki_links.py` to populate the `Wikipedia Link` column used by the UI.
7. **Prune** the merged database with `prune_database.py` if you want to drop people, disambiguations, or rows that are nLab-only.
8. **Export layers** with `experiments/labels.py` whenever you need refreshed layered label sets to drive the experimental mapper or other analyses.

## Detailed Notes per Agent
### Termlist Ingestors
- **Mathlib** (`scripts/other/make_mathlib_termlist_from_overview.py`): Run after saving the Mathlib overview HTML locally. `--base-url` keeps generated links absolute; `--allow-domain` / `--allow-path` guard against stray links.
- **nLab** (`scripts/other/make_nlab_termlist_from_xhtml.py`): Expects the XHTML dump produced by https://ncatlab.org/nlab/all_pages. The agent filters to `/nlab/show/` URLs and normalizes whitespace in titles.
- **Chicago** (`scripts/other/make_chicago_termlist.py`): Scans the `chicago/` Markdown corpus, prefers the first `# Heading` as the title, and builds links from the provided `--base-url` plus the file stem.
- **PDF index** (`scripts/other/make_termlist_from_index.py`): Handles `.idx/.ind` or plaintext PDF index exports. Use it for books like Riehl's *Category Theory in Context* or Leinster's *Basic Category Theory*; pass `--page-offset` when page numbers need shifting.
- **Clowder suggestions** (`scripts/other/make_clowder_suggestions.py`): Augments `title,link` CSVs with a heuristic `suggestion` column that strips articles, singularizes plurals, and capitalizes common eponym names—useful fuel for the mapper's alternate lookup pass.

### Mapping and Inspection
- **Mapper (SQLite-backed)** (`scripts/building/mapper.py`): Requires a wikimapper-style SQLite database (`mapping(wikipedia_title TEXT, wikidata_id TEXT)`). It strips light TeX markup and tries category-specific suffixes before exact matches. Use `--source` to name the output columns and `--out` to direct the result under `data/alignments`. Enabling `--check-wikidata` makes best-effort API calls to filter out disambiguations, people, and theorem-like entities.
- **Mapper (Layer experiments)** (`scripts/building/mapper_new.py`): Instead of hitting a SQLite index, this agent compares normalized titles against layered label files (prefer the compact `experiments/layer*.csv`, or load a prebuilt `experiments/layer_catalog.json`). The staged matcher scores candidates (exact letters, simple normalization, token Jaccard, and `of`-phrase swaps) and records alternates, emitting `<base>_layer_matches.csv` plus `<base>_layer_misses.csv`.
- **Layer catalog builder** (`scripts/building/build_layer_catalog.py`): Optional helper that rolls several layer CSV/JSON files into a JSON catalog with precomputed normalizations and token indexes. `mapper_new.py` can reuse this via `--catalog` for faster startups.
- **Mapper test harness** (`scripts/other/maptest.py`): Lightweight REPL/CLI to inspect what `mapper.py` would return for sample terms. Handy before large batch runs.

### Database Assembly and Cleanup
- **Database builder** (`scripts/building/build_database.py`): Consolidates all alignment CSVs and hydrates human-readable labels from either the local SQLite index or the live Wikidata API. Outputs a canonical `data/database.csv` that the web UI and notebooks consume. Supports caching of online labels via `--cache`.
- **Wikipedia link filler** (`scripts/building/add_enwiki_links.py`): Calls the Wikidata API in batches to populate a `Wikipedia Link` column with canonical `https://en.wikipedia.org/wiki/...` URLs. Safe to re-run; preserves any existing values.
- **Pruner** (`scripts/building/prune_database.py`): Filters the merged database by checking each QID's P31 instance-of values. By default it drops humans and disambiguation pages. Flags like `--drop-nlab-only` help trim rows that only appear in nLab.

### Experimental Layers
- **Layer builder** (`experiments/labels.py`): Issues SPARQL queries starting from seed QIDs (defaults: mathematical concept/object/structure) and grows outward layer by layer using P31/P279 relationships. Supports both chained single-layer mode (`--from-csv`) and multi-layer mode (`--layers N`). Outputs compact `qid,label` CSVs under `experiments/` and can optionally use `--transitive` to enable P279* traversals.
- **Layer CSVs** (`experiments/layer1.csv` ... `layer4.csv`): These are snapshots generated by the layer builder. Keep them up to date when refreshing experiments so the layer mapper has consistent inputs.

## Maintenance Tips
- All agents are pure Python and avoid hard-coded paths; run them from the project root or provide explicit paths.
- Network-using agents (`add_enwiki_links.py`, `prune_database.py`, `experiments/labels.py` with SPARQL, and `mapper.py --check-wikidata`) should be throttled responsibly. Batch sizes default to conservative values but can be reduced if rate limits appear.
- Most agents write CSVs in-place; commit results in the order above so downstream steps always see consistent inputs.
- The pipeline is modular—feel free to introduce new agents for additional sources as long as they emit the same `title,link[,suggestion]` shape consumed by the mappers.
