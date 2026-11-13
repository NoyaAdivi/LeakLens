"""Password strength analysis. Pure Python, no network, no storage."""

from __future__ import annotations

import math
import re
import string
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from .messages import LABELS, TIME_UNITS, t

GUESSES_PER_SECOND = 1e10  # an offline attacker with a GPU rig and a fast hash
KEYBOARD_ROWS = ("qwertyuiop", "asdfghjkl", "zxcvbnm", "1234567890", "1qaz2wsx3edc")
LEET = str.maketrans({"@": "a", "4": "a", "3": "e", "1": "i", "!": "i", "0": "o", "$": "s", "5": "s", "7": "t"})


@lru_cache(maxsize=1)
def common_passwords() -> frozenset[str]:
    path = Path(__file__).parent / "data" / "common.txt"
    return frozenset(line.strip().lower() for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


@dataclass
class StrengthResult:
    score: int
    label: str
    entropy_bits: float
    crack_time_seconds: float
    crack_time_display: str
    length: int
    checks: dict[str, bool]
    feedback: list[str] = field(default_factory=list)


def pool_size(pw: str) -> int:
    pool = 0
    if any(c in string.ascii_lowercase for c in pw):
        pool += 26
    if any(c in string.ascii_uppercase for c in pw):
        pool += 26
    if any(c.isdigit() for c in pw):
        pool += 10
    if any(c in string.punctuation or c == " " for c in pw):
        pool += 33
    if any(ord(c) > 127 for c in pw):  # Hebrew and other non-ASCII letters
        pool += 40
    return pool


def _has_sequence(pw: str, run: int = 3) -> bool:
    low = pw.lower()
    for i in range(len(low) - run + 1):
        chunk = low[i : i + run]
        if all(c.isalnum() for c in chunk):
            diffs = {ord(chunk[j + 1]) - ord(chunk[j]) for j in range(run - 1)}
            if diffs in ({1}, {-1}):
                return True
    return False


def _has_keyboard_pattern(pw: str, run: int = 4) -> bool:
    low = pw.lower()
    for row in KEYBOARD_ROWS:
        for i in range(len(row) - run + 1):
            piece = row[i : i + run]
            if piece in low or piece[::-1] in low:
                return True
    return False


def is_common(pw: str) -> bool:
    low = pw.lower()
    stripped = re.sub(r"[\d!@#$%^&*.]+$", "", low)  # "Password123!" -> "password"
    return any(x in common_passwords() for x in {low, stripped, low.translate(LEET), stripped.translate(LEET)})


def crack_time_display(seconds: float, lang: str = "en") -> str:
    units = TIME_UNITS.get(lang, TIME_UNITS["en"])
    if seconds < 1:
        return units[0]
    steps = [(60, 1, 1), (3600, 2, 60), (86400, 3, 3600), (31_536_000, 4, 86400), (3_153_600_000, 5, 31_536_000)]
    for limit, idx, div in steps:
        if seconds < limit:
            return f"{int(seconds // div)} {units[idx]}"
    return units[6]


def analyze(pw: str, lang: str = "en") -> StrengthResult:
    checks = {
        "length_12": len(pw) >= 12,
        "upper": any(c.isupper() for c in pw),
        "lower": any(c.islower() for c in pw),
        "digit": any(c.isdigit() for c in pw),
        "symbol": any(not c.isalnum() for c in pw),
        "not_common": not is_common(pw),
        "no_repeats": not re.search(r"(.)\1\1", pw),
        "no_sequences": not _has_sequence(pw),
        "no_keyboard": not _has_keyboard_pattern(pw),
        "no_years": not re.search(r"(19|20)\d\d", pw),
    }

    pool = pool_size(pw)
    bits = len(pw) * math.log2(pool) if pool else 0.0
    penalty = 0.0
    if not checks["no_repeats"]:
        penalty += 8
    if not checks["no_sequences"]:
        penalty += 8
    if not checks["no_keyboard"]:
        penalty += 12
    if not checks["no_years"]:
        penalty += 6
    bits = max(0.0, bits - penalty)
    if not checks["not_common"]:
        bits = min(bits, 10.0)

    if bits < 28:
        score = 0
    elif bits < 40:
        score = 1
    elif bits < 60:
        score = 2
    elif bits < 80:
        score = 3
    else:
        score = 4
    if not checks["not_common"]:
        score = 0

    seconds = (2 ** min(bits, 1000)) / 2 / GUESSES_PER_SECOND  # cap keeps the float finite

    feedback: list[str] = []
    order = [
        ("not_common", "common"), ("length_12", "too_short"), ("upper", "add_upper"), ("lower", "add_lower"),
        ("digit", "add_digit"), ("symbol", "add_symbol"), ("no_repeats", "repeat"),
        ("no_sequences", "sequence"), ("no_keyboard", "keyboard"), ("no_years", "year"),
    ]
    for key, code in order:
        if not checks[key]:
            feedback.append(t(code, lang))
    if score < 3:
        feedback.append(t("passphrase_tip", lang))

    return StrengthResult(
        score=score,
        label=LABELS[score].get(lang, LABELS[score]["en"]),
        entropy_bits=round(bits, 1),
        crack_time_seconds=seconds,
        crack_time_display=crack_time_display(seconds, lang),
        length=len(pw),
        checks=checks,
        feedback=feedback,
    )
