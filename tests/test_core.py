import asyncio
import hashlib

import pytest

from app.generator import generate_passphrase, generate_password
from app.pwned import RangeCache, count_in_range, lookup_password, sha1_hex, split_hash
from app.security import RateLimiter
from app.strength import analyze, crack_time_display, is_common


# ---------- strength ----------
@pytest.mark.parametrize("pw", ["password", "123456", "P@ssw0rd", "Password123!", "qwerty"])
def test_common_passwords_are_very_weak(pw):
    r = analyze(pw)
    assert r.score == 0
    assert r.checks["not_common"] is False


def test_long_random_password_is_very_strong():
    r = analyze("vT9#qL2!mZ8@wR4$kP7&")
    assert r.score == 4
    assert all(r.checks.values())
    assert r.feedback == []


def test_patterns_are_detected():
    r = analyze("Abcdzzz1990qwer!")
    assert not r.checks["no_sequences"]
    assert not r.checks["no_repeats"]
    assert not r.checks["no_years"]
    assert not r.checks["no_keyboard"]


def test_hebrew_feedback():
    r = analyze("abc", lang="he")
    assert r.label == "חלשה מאוד"
    assert any("12" in f for f in r.feedback)


def test_hebrew_letters_count_as_characters():
    assert analyze("שלוםעולםיפהXy7!").entropy_bits > analyze("abcdXy7!").entropy_bits


def test_crack_time_display():
    assert crack_time_display(0.1) == "instantly"
    assert crack_time_display(120) == "2 minutes"
    assert crack_time_display(10**12) == "centuries"
    assert crack_time_display(120, "he") == "2 דקות"


def test_is_common_handles_leet():
    assert is_common("Tr0ub4dor") is False
    assert is_common("M0nkey") is True


# ---------- pwned (k-anonymity) ----------
def test_sha1_and_split():
    h = sha1_hex("password")
    assert h == hashlib.sha1(b"password").hexdigest().upper()
    assert split_hash(h) == (h[:5], h[5:])
    with pytest.raises(ValueError):
        split_hash("nothex")


def test_count_in_range_ignores_padding():
    body = "AAAA:3\r\n1E4C9B93F3F0682250B6CF8331B7EE68FD8:9545824\r\nBBBB:0"
    assert count_in_range(body, "1e4c9b93f3f0682250b6cf8331b7ee68fd8") == 9545824
    assert count_in_range(body, "BBBB") == 0
    assert count_in_range(body, "CCCC") == 0


def test_only_prefix_leaves_and_cache_is_used():
    sent = []
    h = sha1_hex("password")

    async def fake_fetch(prefix):
        sent.append(prefix)
        return f"{h[5:]}:42"

    cache = RangeCache()
    assert asyncio.run(lookup_password("password", fake_fetch, cache)) == 42
    assert asyncio.run(lookup_password("password", fake_fetch, cache)) == 42
    assert sent == [h[:5]]  # 5 characters, sent once
    assert "password" not in "".join(sent)


# ---------- generator ----------
def test_generated_password_has_every_group():
    pw, bits = generate_password(length=16)
    assert len(pw) == 16
    assert any(c.isupper() for c in pw) and any(c.islower() for c in pw)
    assert any(c.isdigit() for c in pw) and any(not c.isalnum() for c in pw)
    assert bits > 90


def test_generator_excludes_ambiguous_and_validates():
    pw, _ = generate_password(length=64, exclude_ambiguous=True)
    assert not set(pw) & set("Il1O0o")
    with pytest.raises(ValueError):
        generate_password(upper=False, lower=False, digits=False, symbols=False)


def test_generated_passwords_differ():
    assert len({generate_password()[0] for _ in range(50)}) == 50


def test_passphrase():
    phrase, bits = generate_passphrase(words=4, separator=".", add_number=False)
    assert phrase.count(".") == 3
    assert bits > 28


# ---------- rate limiter ----------
def test_rate_limiter_blocks_then_recovers():
    rl = RateLimiter(limit=2, window=60)
    assert rl.check("1.1.1.1", now=0)[0]
    assert rl.check("1.1.1.1", now=1)[0]
    ok, retry = rl.check("1.1.1.1", now=2)
    assert not ok and retry > 0
    assert rl.check("2.2.2.2", now=2)[0]  # other clients are not affected
    assert rl.check("1.1.1.1", now=61)[0]


def test_very_long_password_does_not_overflow():
    r = analyze("Aa1!" * 64)
    assert r.crack_time_display == "centuries"
