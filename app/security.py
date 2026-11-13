"""Hardening middleware: security headers, per-IP rate limiting and a body size cap."""

from __future__ import annotations

import json
import time
from collections import defaultdict, deque

API_HEADERS = [
    (b"x-content-type-options", b"nosniff"),
    (b"x-frame-options", b"DENY"),
    (b"referrer-policy", b"no-referrer"),
    (b"permissions-policy", b"camera=(), microphone=(), geolocation=()"),
    (b"cross-origin-opener-policy", b"same-origin"),
    (b"strict-transport-security", b"max-age=63072000; includeSubDomains"),
]
NO_STORE = [(b"cache-control", b"no-store"), (b"content-security-policy", b"default-src 'none'; frame-ancestors 'none'")]


class RateLimiter:
    """Sliding window limiter kept in memory. One deque of timestamps per client."""

    def __init__(self, limit: int, window: float = 60.0) -> None:
        self.limit, self.window = limit, window
        self.hits: dict[str, deque[float]] = defaultdict(deque)

    def check(self, key: str, now: float | None = None) -> tuple[bool, int]:
        now = time.monotonic() if now is None else now
        q = self.hits[key]
        while q and now - q[0] >= self.window:
            q.popleft()
        if len(q) >= self.limit:
            return False, max(1, int(self.window - (now - q[0])) + 1)
        q.append(now)
        return True, 0


class SecurityMiddleware:
    def __init__(self, app, limiter: RateLimiter, max_body: int = 4096) -> None:
        self.app, self.limiter, self.max_body = app, limiter, max_body

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        path: str = scope.get("path", "")
        is_api = path.startswith("/v1/")

        async def send_with_headers(message):
            if message["type"] == "http.response.start":
                message.setdefault("headers", [])
                message["headers"] = list(message["headers"]) + API_HEADERS + (NO_STORE if is_api else [])
            await send(message)

        if is_api:
            client = (scope.get("client") or ("unknown", 0))[0]
            ok, retry = self.limiter.check(client)
            if not ok:
                return await _json(send_with_headers, 429, {"detail": "Too many requests"},
                                   [(b"retry-after", str(retry).encode())])
            headers = dict(scope.get("headers") or [])
            length = headers.get(b"content-length")
            if length and length.isdigit() and int(length) > self.max_body:
                return await _json(send_with_headers, 413, {"detail": "Request body too large"})

        await self.app(scope, receive, send_with_headers)


async def _json(send, status: int, body: dict, extra: list | None = None) -> None:
    data = json.dumps(body).encode()
    await send({"type": "http.response.start", "status": status,
                "headers": [(b"content-type", b"application/json"), (b"content-length", str(len(data)).encode())] + (extra or [])})
    await send({"type": "http.response.body", "body": data})
