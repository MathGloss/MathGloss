"""Layer catalog construction and lookup utilities."""
from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Set

from scripts.building.text_norm import (
    normalize_letters,
    normalize_simple,
    of_swap_variants,
    tokenize,
)


@dataclass(frozen=True)
class LayerItem:
    qid: str
    label: str
    layer: str
    norm_letters: str
    norm_simple: str
    tokens: frozenset[str]


class LayerCatalog:
    def __init__(self, items: Sequence[LayerItem], layers_meta: Sequence[dict]):
        self.items: List[LayerItem] = list(items)
        self.layers_meta: List[dict] = list(layers_meta)
        self._by_letters: Dict[str, List[int]] = {}
        self._by_simple: Dict[str, List[int]] = {}
        self._token_index: Dict[str, Set[int]] = {}
        for idx, item in enumerate(self.items):
            self._by_letters.setdefault(item.norm_letters, []).append(idx)
            self._by_simple.setdefault(item.norm_simple, []).append(idx)
            for tok in item.tokens:
                self._token_index.setdefault(tok, set()).add(idx)

    @classmethod
    def from_layers(cls, layer_paths: Sequence[Path]) -> "LayerCatalog":
        items: List[LayerItem] = []
        meta: List[dict] = []
        for lp in layer_paths:
            rows = list(_iter_layer_entries(lp))
            meta.append({"path": str(lp), "count": len(rows)})
            items.extend(rows)
        return cls(items, meta)

    @classmethod
    def from_catalog(cls, path: Path) -> "LayerCatalog":
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        entries = data.get("entries", [])
        items = [
            LayerItem(
                qid=e["qid"],
                label=e["label"],
                layer=e["layer"],
                norm_letters=e["norm_letters"],
                norm_simple=e["norm_simple"],
                tokens=frozenset(e.get("tokens", [])),
            )
            for e in entries
        ]
        return cls(items, data.get("layers", []))

    def to_dict(self) -> dict:
        return {
            "layers": self.layers_meta,
            "entries": [
                {
                    "qid": item.qid,
                    "label": item.label,
                    "layer": item.layer,
                    "norm_letters": item.norm_letters,
                    "norm_simple": item.norm_simple,
                    "tokens": sorted(item.tokens),
                }
                for item in self.items
            ],
        }

    def find_candidates(
        self,
        title: str,
        *,
        max_candidates: int = 5,
        token_threshold: float = 0.6,
    ) -> List["MatchCandidate"]:
        norm_letters = normalize_letters(title)
        norm_simple = normalize_simple(title)
        title_lower = title.lower().strip()
        simple_variants = of_swap_variants(norm_simple) if norm_simple else []
        tok_set = set(tokenize(title))

        seen: Dict[str, MatchCandidate] = {}

        def _register(idx: int, score: float, reason: str) -> None:
            item = self.items[idx]
            prev = seen.get(item.qid)
            if prev is None or score > prev.score:
                seen[item.qid] = MatchCandidate(item=item, score=score, reason=reason)

        if norm_letters:
            for idx in self._by_letters.get(norm_letters, []):
                _register(idx, 1.0, "exact_letters")

        if not seen and norm_simple:
            for idx in self._by_simple.get(norm_simple, []):
                _register(idx, 0.9, "exact_simple")

        for variant in simple_variants:
            for idx in self._by_simple.get(variant, []):
                _register(idx, 0.94, f"of_swap:{variant}")

        if tok_set:
            candidate_idxs: Set[int] = set()
            for tok in tok_set:
                candidate_idxs.update(self._token_index.get(tok, set()))
            for idx in candidate_idxs:
                item = self.items[idx]
                score = _token_jaccard(tok_set, item.tokens)
                if score >= token_threshold:
                    blended = 0.6 + 0.4 * score
                    _register(idx, blended, f"token_jaccard={score:.2f}")

        candidates = list(seen.values())
        def _sort_key(c: MatchCandidate) -> tuple:
            exact_label = 0 if title_lower and c.item.label.lower() == title_lower else 1
            exact_simple = 0 if norm_simple and c.item.norm_simple == norm_simple else 1
            return (-c.score, exact_label, exact_simple, c.item.label.lower(), c.item.qid)

        candidates.sort(key=_sort_key)
        return candidates[:max_candidates]


@dataclass(frozen=True)
class MatchCandidate:
    item: LayerItem
    score: float
    reason: str


def _iter_layer_entries(path: Path) -> Iterable[LayerItem]:
    if path.suffix.lower() == ".csv":
        yield from _iter_layer_csv(path)
    elif path.suffix.lower() == ".json":
        yield from _iter_layer_json(path)
    else:
        raise ValueError(f"Unsupported layer extension for {path}")


def _iter_layer_csv(path: Path) -> Iterable[LayerItem]:
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or "qid" not in reader.fieldnames or "label" not in reader.fieldnames:
            raise ValueError(f"Layer CSV must have headers qid,label (in {path})")
        for row in reader:
            qid = (row.get("qid") or "").strip()
            label = (row.get("label") or "").strip()
            if not qid or not label:
                continue
            norm_letters = normalize_letters(label)
            if not norm_letters:
                continue
            yield LayerItem(
                qid=qid,
                label=label,
                layer=path.name,
                norm_letters=norm_letters,
                norm_simple=normalize_simple(label),
                tokens=tokenize(label),
            )


def _iter_layer_json(path: Path) -> Iterable[LayerItem]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    entities = (data or {}).get("entities", {})
    for qid, ent in entities.items():
        label = (ent or {}).get("label") or ""
        if not isinstance(label, str):
            continue
        label = label.strip()
        if not label:
            continue
        norm_letters = normalize_letters(label)
        if not norm_letters:
            continue
        yield LayerItem(
            qid=qid,
            label=label,
            layer=path.name,
            norm_letters=norm_letters,
            norm_simple=normalize_simple(label),
            tokens=tokenize(label),
        )


def _token_jaccard(a: Set[str], b: Set[str] | frozenset[str]) -> float:
    if not a or not b:
        return 0.0
    intersection = len(a & set(b))
    if intersection == 0:
        return 0.0
    union = len(a | set(b))
    if union == 0:
        return 0.0
    return intersection / union
