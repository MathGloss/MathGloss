#!/usr/bin/env python3
"""Generate a reusable JSON catalog from layer CSV/JSON files."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List

try:  # allow running as standalone script
    from scripts.building.layer_catalog import LayerCatalog
except ModuleNotFoundError:  # pragma: no cover
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from scripts.building.layer_catalog import LayerCatalog


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Build compact catalog JSON from layer files.")
    ap.add_argument(
        "--layers",
        nargs="*",
        default=[
            "experiments/layer1.csv",
            "experiments/layer2.csv",
            "experiments/layer3.csv",
            "experiments/layer4.csv",
        ],
        help="Layer CSV/JSON files to include (default: experiments/layer[1-4].csv)",
    )
    ap.add_argument(
        "--out",
        default="experiments/layer_catalog.json",
        help="Path to write the catalog JSON (default: experiments/layer_catalog.json)",
    )
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    layer_paths: List[Path] = [Path(p) for p in args.layers]
    for lp in layer_paths:
        if not lp.exists():
            raise FileNotFoundError(f"Layer file not found: {lp}")

    catalog = LayerCatalog.from_layers(layer_paths)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(catalog.to_dict(), f, ensure_ascii=False, indent=2, sort_keys=True)
    total_items = len(catalog.items)
    print(f"Wrote {out_path} with {total_items} entries from {len(layer_paths)} layers.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
