"""LeakLens: a privacy-first REST API for password strength and breach checks."""

from __future__ import annotations

import os
from contextlib import asynccontextmanager
from typing import Literal

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field, SecretStr

from . import __version__
from .generator import generate_passphrase, generate_password
from .messages import t
from .pwned import RANGE_URL, RangeCache, lookup_hash, lookup_password
from .security import RateLimiter, SecurityMiddleware
from .strength import analyze

RATE_LIMIT = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "").split(",") if o.strip()]
USER_AGENT = f"LeakLens/{__version__} (+https://github.com/NoyaAdivi/LeakLens)"

Lang = Literal["en", "he"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http = httpx.AsyncClient(timeout=5.0, headers={"User-Agent": USER_AGENT, "Add-Padding": "true"})
    app.state.cache = RangeCache()
    yield
    await app.state.http.aclose()


app = FastAPI(
    title="LeakLens",
    version=__version__,
    summary="Password strength and breach checks that never store, log or send your password.",
    lifespan=lifespan,
    license_info={"name": "MIT", "url": "https://github.com/NoyaAdivi/LeakLens/blob/main/LICENSE"},
)
app.add_middleware(SecurityMiddleware, limiter=RateLimiter(RATE_LIMIT))
if CORS_ORIGINS:
    app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGINS, allow_methods=["GET", "POST"], allow_headers=["Content-Type"])


# ---------- models ----------
class PasswordIn(BaseModel):
    password: SecretStr = Field(..., min_length=1, max_length=256, description="Never logged or stored")
    lang: Lang = "en"


class HashIn(BaseModel):
    sha1: str = Field(..., pattern=r"^[0-9A-Fa-f]{40}$", description="SHA-1 of the password, hashed on the client")
    lang: Lang = "en"


class GenerateIn(BaseModel):
    length: int = Field(20, ge=8, le=128)
    upper: bool = True
    lower: bool = True
    digits: bool = True
    symbols: bool = True
    exclude_ambiguous: bool = False


class PassphraseIn(BaseModel):
    words: int = Field(5, ge=3, le=12)
    separator: str = Field("-", max_length=3)
    capitalize: bool = True
    add_number: bool = True


# ---------- helpers ----------
async def fetch_range(request: Request, prefix: str) -> str:
    try:
        res = await request.app.state.http.get(RANGE_URL.format(prefix=prefix))
        res.raise_for_status()
        return res.text
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=503, detail="Breach service is unavailable, try again soon") from exc


def breach_body(count: int, lang: str) -> dict:
    return {"pwned": count > 0, "count": count, "message": t("pwned" if count else "not_pwned", lang)}


# ---------- routes ----------
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/docs")


@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok", "version": __version__}


@app.post("/v1/strength", tags=["passwords"])
def strength(body: PasswordIn):
    """Score a password from 0 to 4, estimate crack time and explain how to improve it."""
    return analyze(body.password.get_secret_value(), body.lang).__dict__


@app.post("/v1/pwned", tags=["breaches"])
async def pwned(body: PasswordIn, request: Request):
    """Check if a password appeared in a data breach, using k-anonymity."""
    count = await lookup_password(body.password.get_secret_value(), lambda p: fetch_range(request, p), request.app.state.cache)
    return breach_body(count, body.lang)


@app.post("/v1/pwned/hash", tags=["breaches"])
async def pwned_hash(body: HashIn, request: Request):
    """Most private option: send only a SHA-1 hash made on your side."""
    count = await lookup_hash(body.sha1, lambda p: fetch_range(request, p), request.app.state.cache)
    return breach_body(count, body.lang)


@app.post("/v1/check", tags=["passwords"])
async def check(body: PasswordIn, request: Request):
    """Strength and breach check in one call, with a final verdict."""
    pw = body.password.get_secret_value()
    result = analyze(pw, body.lang).__dict__
    count = await lookup_password(pw, lambda p: fetch_range(request, p), request.app.state.cache)
    breach = breach_body(count, body.lang)
    safe = result["score"] >= 3 and not breach["pwned"]
    return {"safe": safe, "strength": result, "breach": breach}


@app.post("/v1/generate", tags=["generator"])
def generate(body: GenerateIn):
    """Create a random password with a cryptographically secure generator."""
    try:
        password, bits = generate_password(**body.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {"password": password, "entropy_bits": bits}


@app.post("/v1/passphrase", tags=["generator"])
def passphrase(body: PassphraseIn):
    """Create a memorable passphrase from random words."""
    phrase, bits = generate_passphrase(**body.model_dump())
    return {"passphrase": phrase, "entropy_bits": bits}
