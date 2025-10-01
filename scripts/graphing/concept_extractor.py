#!/usr/bin/env python3
"""Utilities for extracting concept references from MathGloss markdown."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, Iterator, List, Optional
from urllib.parse import urlparse


_LINK_PATTERN = re.compile(r"\[(?P<text>[^\]]+)\]\((?P<url>[^\)]+)\)")


@dataclass(frozen=True)
class ConceptLink:
    text: str
    url: str
    start: int
    end: int

    @property
    def normalized_url(self) -> str:
        return normalize_url(self.url)


def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    scheme = (parsed.scheme or "https").lower()
    netloc = parsed.netloc.lower()
    path = parsed.path.rstrip('/')
    if path.startswith('/'):
        path = path
    query = f"?{parsed.query}" if parsed.query else ""
    fragment = ""
    return f"{scheme}://{netloc}{path}{query}{fragment}" if netloc else path or url


def extract_links(
    markdown: str,
    *,
    allow_domains: Optional[Iterable[str]] = None,
    allow_path_prefixes: Optional[Iterable[str]] = None,
) -> List[ConceptLink]:
    allowed_domains = {d.lower() for d in allow_domains} if allow_domains else None
    allowed_prefixes = tuple(allow_path_prefixes) if allow_path_prefixes else None

    matches: List[ConceptLink] = []
    for match in _LINK_PATTERN.finditer(markdown):
        url = match.group('url').strip()
        text = match.group('text').strip()
        if not url:
            continue
        parsed = urlparse(url)
        if allowed_domains and parsed.netloc.lower() not in allowed_domains:
            continue
        if allowed_prefixes:
            path = parsed.path
            if not any(path.startswith(prefix) for prefix in allowed_prefixes):
                continue
        matches.append(ConceptLink(text=text, url=url, start=match.start(), end=match.end()))
    return matches


__all__ = ["ConceptLink", "extract_links", "normalize_url"]
