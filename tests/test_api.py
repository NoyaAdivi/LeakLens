import pytest

pytest.importorskip("fastapi")
from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402
from app.pwned import sha1_hex  # noqa: E402

LEAKED = "password"


class FakeResponse:
    def __init__(self, text):
        self.text = text

    def raise_for_status(self):
        pass


class FakeHttp:
    def __init__(self):
        self.urls = []

    async def get(self, url):
        self.urls.append(url)
        return FakeResponse(f"{sha1_hex(LEAKED)[5:]}:9545824\r\n0000000000000000000000000000000000A:0")

    async def aclose(self):
        pass


@pytest.fixture
def client():
    with TestClient(app) as c:
        app.state.http = FakeHttp()
        yield c


def test_health(client):
    assert client.get("/health").json()["status"] == "ok"


def test_strength(client):
    r = client.post("/v1/strength", json={"password": "vT9#qL2!mZ8@wR4$kP7&"})
    assert r.status_code == 200
    assert r.json()["score"] == 4


def test_strength_in_hebrew(client):
    r = client.post("/v1/strength", json={"password": "123456", "lang": "he"})
    assert r.json()["label"] == "חלשה מאוד"


def test_pwned_sends_only_prefix(client):
    r = client.post("/v1/pwned", json={"password": LEAKED})
    assert r.json()["pwned"] is True
    url = app.state.http.urls[-1]
    assert url.endswith("/range/" + sha1_hex(LEAKED)[:5])
    assert LEAKED not in url.split("/range/")[1]  # the host name itself contains "password"


def test_pwned_hash(client):
    r = client.post("/v1/pwned/hash", json={"sha1": sha1_hex("something-unique-xyz")})
    assert r.json() == {"pwned": False, "count": 0, "message": "Not found in known data breaches."}


def test_check_verdict(client):
    assert client.post("/v1/check", json={"password": LEAKED}).json()["safe"] is False


def test_generate_and_passphrase(client):
    assert len(client.post("/v1/generate", json={"length": 32}).json()["password"]) == 32
    assert client.post("/v1/passphrase", json={"words": 6}).json()["passphrase"].count("-") == 6


def test_validation(client):
    assert client.post("/v1/strength", json={"password": "x" * 300}).status_code == 422
    assert client.post("/v1/pwned/hash", json={"sha1": "abc"}).status_code == 422


def test_security_headers(client):
    r = client.post("/v1/strength", json={"password": "abc"})
    assert r.headers["cache-control"] == "no-store"
    assert r.headers["x-content-type-options"] == "nosniff"
    assert "default-src 'none'" in r.headers["content-security-policy"]


def test_password_is_not_echoed(client):
    r = client.post("/v1/check", json={"password": "MySecret-Value-123"})
    assert "MySecret-Value-123" not in r.text


def test_body_too_large(client):
    r = client.post("/v1/strength", content="x" * 5000, headers={"content-type": "application/json"})
    assert r.status_code == 413
