<p align="center"><a href="../README.md"><img src="readme/hardening-en.svg" width="100%" alt="Security by design"></a></p>

<p align="center"><a href="SECURITY.he.md"><img src="readme/lang-he.svg" height="44" alt="לגרסה בעברית"></a></p>

## What LeakLens promises

1. **A password is never stored.** There is no database. The password lives in memory only for the length of one request.
2. **A password is never logged.** It is kept in a Pydantic `SecretStr`, which prints as `**********`, and the Docker image runs Uvicorn with access logs off.
3. **A password is never sent.** For breach checks it is hashed with SHA-1 and only the first 5 hex characters go to [Have I Been Pwned](https://haveibeenpwned.com/API/v3#PwnedPasswords).
4. **A password is never echoed back.** Responses contain scores and tips, never the input.

## k-anonymity in short

| Step | Who sees what |
|---|---|
| Hash the password with SHA-1 | Only LeakLens (or your browser in the playground) |
| Send the first 5 characters, for example `5BAA6` | HIBP sees a prefix shared by hundreds of passwords |
| HIBP returns every suffix with that prefix, plus random padding rows | Anyone watching sees a response of a similar size every time |
| Compare the remaining 35 characters locally | Only LeakLens knows the result |

For even more privacy, `POST /v1/pwned/hash` accepts a SHA-1 hash made on the client, so the API never sees the password.

## Protecting the API itself

| Threat | Defense | Code |
|---|---|---|
| Brute force, scraping | Sliding window rate limit per IP, `429` + `Retry-After` | `app/security.py` |
| Memory abuse | Body size cap (4 KB), password length cap (256) | `app/security.py`, `app/main.py` |
| Caching of results | `Cache-Control: no-store` on `/v1` routes | `app/security.py` |
| Clickjacking, MIME sniffing, leaking referrers | `X-Frame-Options: DENY`, `nosniff`, `no-referrer`, strict CSP | `app/security.py` |
| Unwanted browser callers | CORS closed unless `CORS_ORIGINS` is set | `app/main.py` |
| Weak randomness | Python `secrets` and the browser's `crypto.getRandomValues` with rejection sampling | `app/generator.py`, `docs/index.html` |
| Container escape impact | Non-root user, slim base image | `Dockerfile` |

## Honest limits

* The rate limiter lives in memory, so it resets on restart and is per instance. A shared store such as Redis would be the next step for several servers.
* The strength score is a heuristic. A password that scores 4 can still be unsafe if it was reused or leaked, which is why `/v1/check` combines strength with the breach check.
* SHA-1 is used only because the HIBP protocol requires it. It is never used to store anything.

## Reporting a problem

Found a security issue? Please open a [private security advisory](https://github.com/NoyaAdivi/LeakLens/security/advisories/new) instead of a public issue.
