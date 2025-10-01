#!/usr/bin/env python3
"""Extract Lean declaration signatures from local Mathlib sources via doc URLs."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional
from urllib.parse import unquote, urlparse


def _url_to_module_path(url: str) -> tuple[str, str]:
    parsed = urlparse(url)
    if not parsed.path:
        raise ValueError(f"URL is missing a path component: {url}")
    path = unquote(parsed.path.lstrip("/"))
    if path.startswith("mathlib4_docs/"):
        path = path[len("mathlib4_docs/") :]
    if path.startswith("mathlib_docs/"):
        path = path[len("mathlib_docs/") :]
    if not path:
        raise ValueError(f"URL path resolves to empty: {url}")
    fragment = unquote(parsed.fragment or "")
    if path.endswith(".html"):
        path = path[: -len(".html")]
    path = path.rstrip("/")
    if not path:
        raise ValueError(f"URL path resolves to an invalid module: {url}")
    return path, fragment


def resolve_mathlib_file(mathlib_root: Path, url: str) -> tuple[Path, str]:
    module_path, fragment = _url_to_module_path(url)
    module_variants: list[str] = [module_path]
    if module_path.startswith("Mathlib/"):
        tail = module_path[len("Mathlib/") :]
        if tail:
            module_variants.append(tail)
    if module_path.startswith("Init/"):
        tail = module_path[len("Init/") :]
        if tail:
            module_variants.append(tail)

    seen: set[Path] = set()
    for variant in module_variants:
        variant_path = Path(variant)
        if not variant_path.parts:
            continue
        for candidate_path in (
            (mathlib_root / variant_path).with_suffix(".lean"),
            (mathlib_root / Path(variant.replace(".", "/"))).with_suffix(".lean"),
        ):
            if candidate_path in seen:
                continue
            seen.add(candidate_path)
            if candidate_path.exists():
                return candidate_path, fragment

    raise FileNotFoundError(f"Could not locate Lean source for {url} under {mathlib_root}")


def extract_signature(file_path: Path, qualified_name: str) -> Optional[str]:
    target = qualified_name.split(".")[-1] if qualified_name else ""
    if not target:
        return None

    lines = file_path.read_text(encoding="utf-8").splitlines()
    line_count = len(lines)
    idx = 0
    allowed_keywords = {"structure", "class", "inductive"}

    while idx < line_count:
        stripped = lines[idx].strip()
        if not stripped or stripped.startswith("--"):
            idx += 1
            continue
        tokens = stripped.split()
        if not tokens:
            idx += 1
            continue
        if tokens[0] not in allowed_keywords:
            idx += 1
            continue
        match_index: Optional[int] = None
        for i, token in enumerate(tokens[1:], start=1):
            if token.split(".")[-1] == target:
                match_index = i
                break
        if match_index is None or match_index == 0:
            idx += 1
            continue

        first_line = lines[idx]
        assign_pos = first_line.find(":=")
        if assign_pos != -1:
            return first_line.rstrip()

        collected: list[str] = [first_line.rstrip()]
        idx += 1
        while idx < line_count:
            current = lines[idx]
            stripped_current = current.strip()
            if not stripped_current:
                break
            if not current.startswith((" ", "\t")):
                break
            assign_pos = current.find(":=")
            if assign_pos != -1:
                collected.append(current.rstrip())
                return "\n".join(collected).strip()
            collected.append(current.rstrip())
            idx += 1
        return "\n".join(collected).strip() if collected else None
    return None


def fetch_signature(mathlib_root: Path, url: str) -> str:
    file_path, fragment = resolve_mathlib_file(mathlib_root, url)
    signature = extract_signature(file_path, fragment)
    if not signature:
        raise LookupError(f"Declaration '{fragment}' not found in {file_path}")
    return signature


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mathlib-dir", type=Path, required=True, help="Path to local mathlib checkout")
    parser.add_argument("url", help="Mathlib documentation URL pointing to a declaration")
    return parser


def main(argv: Optional[list[str]] = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)
    mathlib_dir = args.mathlib_dir.expanduser().resolve()
    if not mathlib_dir.exists():
        raise SystemExit(f"Mathlib directory not found: {mathlib_dir}")
    try:
        signature = fetch_signature(mathlib_dir, args.url)
    except Exception as exc:
        raise SystemExit(str(exc)) from exc
    print(signature)


if __name__ == "__main__":  # pragma: no cover
    main()
