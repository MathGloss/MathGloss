"""Utility normalization helpers shared across mapping scripts."""
from __future__ import annotations

import re
import unicodedata
from typing import FrozenSet, List

OF_STOPWORDS = {"a", "an", "the"}


def _strip_accents(s: str) -> str:
    if not s:
        return ""
    normalized = unicodedata.normalize("NFKD", s)
    return "".join(ch for ch in normalized if not unicodedata.combining(ch))


def normalize_letters(s: str) -> str:
    """Lowercase string keeping only alphanumeric characters (Unicode-aware)."""
    base = _strip_accents(s)
    allowed = {"∞"}
    return "".join(ch for ch in base.lower() if ch.isalnum() or ch in allowed)


def normalize_simple(s: str) -> str:
    """Lowercase alphanumeric words separated by single spaces."""
    base = _strip_accents(s).lower()
    # Replace any non-alphanumeric character with a space
    base = re.sub(r"[^a-z0-9]+", " ", base)
    base = re.sub(r"\s+", " ", base)
    return base.strip()


def tokenize(s: str) -> FrozenSet[str]:
    """Return a frozenset of normalized tokens."""
    simple = normalize_simple(s)
    if not simple:
        return frozenset()
    return frozenset(simple.split(" "))


def of_swap_variants(simple: str) -> List[str]:
    """Generate variants by swapping the clause after 'of' to the front.

    Example: 'order of a group' -> ['group order']
    """
    tokens = simple.split()
    if not tokens or "of" not in tokens:
        return []
    variants: List[str] = []
    for idx, tok in enumerate(tokens):
        if tok != "of":
            continue
        left = tokens[:idx]
        right = tokens[idx + 1 :]
        if not left or not right:
            continue
        # Drop leading articles in the right side
        while right and right[0] in OF_STOPWORDS:
            right = right[1:]
        if not right:
            continue
        candidate = right + left
        variant = " ".join(candidate)
        if variant and variant not in variants:
            variants.append(variant)
    return variants
