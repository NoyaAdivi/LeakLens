"""Cryptographically secure password and passphrase generation (uses `secrets`)."""

from __future__ import annotations

import math
import secrets
import string
from functools import lru_cache
from pathlib import Path

AMBIGUOUS = set("Il1O0o|`'\"")
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.?/~"


@lru_cache(maxsize=1)
def wordlist() -> tuple[str, ...]:
    text = (Path(__file__).parent / "data" / "words.txt").read_text(encoding="utf-8")
    return tuple(sorted(set(text.split())))


def generate_password(
    length: int = 20,
    upper: bool = True,
    lower: bool = True,
    digits: bool = True,
    symbols: bool = True,
    exclude_ambiguous: bool = False,
) -> tuple[str, float]:
    groups = [g for g, on in ((string.ascii_uppercase, upper), (string.ascii_lowercase, lower),
                              (string.digits, digits), (SYMBOLS, symbols)) if on]
    if not groups:
        raise ValueError("choose at least one character group")
    if exclude_ambiguous:
        groups = ["".join(c for c in g if c not in AMBIGUOUS) for g in groups]
    if length < len(groups):
        raise ValueError("length is too short for the chosen groups")

    alphabet = "".join(groups)
    chars = [secrets.choice(g) for g in groups]  # at least one from every group
    chars += [secrets.choice(alphabet) for _ in range(length - len(chars))]
    for i in range(len(chars) - 1, 0, -1):  # Fisher-Yates shuffle with a CSPRNG
        j = secrets.randbelow(i + 1)
        chars[i], chars[j] = chars[j], chars[i]
    return "".join(chars), round(length * math.log2(len(alphabet)), 1)


def generate_passphrase(words: int = 5, separator: str = "-", capitalize: bool = True,
                        add_number: bool = True) -> tuple[str, float]:
    pool = wordlist()
    picked = [secrets.choice(pool) for _ in range(words)]
    if capitalize:
        picked = [w.capitalize() for w in picked]
    bits = words * math.log2(len(pool))
    phrase = separator.join(picked)
    if add_number:
        phrase += separator + str(secrets.randbelow(100))
        bits += math.log2(100)
    return phrase, round(bits, 1)
