"""Breach lookup with Have I Been Pwned's k-anonymity range API.

The password is hashed with SHA-1 on our side. Only the first 5 hex characters
of the hash leave the server, so neither HIBP nor anyone watching the network
ever sees the password or its full hash.
"""

from __future__ import annotations

import hashlib
import re
import time
from typing import Awaitable, Callable

RANGE_URL = "https://api.pwnedpasswords.com/range/{prefix}"
SHA1_RE = re.compile(r"^[0-9A-Fa-f]{40}$")

Fetcher = Callable[[str], Awaitable[str]]


def sha1_hex(password: str) -> str:
    return hashlib.sha1(password.encode("utf-8")).hexdigest().upper()  # noqa: S324 (required by the HIBP protocol)


def split_hash(sha1: str) -> tuple[str, str]:
    sha1 = sha1.upper()
    if not SHA1_RE.match(sha1):
        raise ValueError("sha1 must be 40 hex characters")
    return sha1[:5], sha1[5:]


def count_in_range(body: str, suffix: str) -> int:
    """Find our suffix in a range response. Padding rows have a count of 0."""
    suffix = suffix.upper()
    for line in body.splitlines():
        candidate, _, count = line.strip().partition(":")
        if candidate.upper() == suffix:
            try:
                return int(count)
            except ValueError:
                return 0
    return 0


class RangeCache:
    """Small in-memory TTL cache. It holds only public range data, never passwords."""

    def __init__(self, ttl: float = 3600, max_items: int = 2048) -> None:
        self.ttl, self.max_items = ttl, max_items
        self._items: dict[str, tuple[float, str]] = {}

    def get(self, prefix: str) -> str | None:
        hit = self._items.get(prefix)
        if hit and time.monotonic() - hit[0] < self.ttl:
            return hit[1]
        self._items.pop(prefix, None)
        return None

    def set(self, prefix: str, body: str) -> None:
        if len(self._items) >= self.max_items:
            self._items.pop(next(iter(self._items)))
        self._items[prefix] = (time.monotonic(), body)


async def lookup_hash(sha1: str, fetch: Fetcher, cache: RangeCache | None = None) -> int:
    prefix, suffix = split_hash(sha1)
    body = cache.get(prefix) if cache else None
    if body is None:
        body = await fetch(prefix)
        if cache:
            cache.set(prefix, body)
    return count_in_range(body, suffix)


async def lookup_password(password: str, fetch: Fetcher, cache: RangeCache | None = None) -> int:
    return await lookup_hash(sha1_hex(password), fetch, cache)
