# Contributing to tcs-macro-pulse

Thanks for your interest in improving the open-source data layer of TCS-PLATFORM! This document explains **what we accept**, **what we don't**, and the **legal terms** of contributing.

---

## 1. Scope: What belongs in this repo

✅ **In-scope (L1–L3 — open source)**
- New macro data fetchers (FRED, IMF, World Bank, Eurostat, GSO Vietnam, SBV, …)
- New event/news fetchers (GDACS, ACLED, ReliefWeb, RSS feeds, …)
- New sentiment analyzers based on **public** signals (keyword counts, RSS, public APIs)
- Bug fixes, documentation, tests, examples
- Performance improvements (caching, async, batching)
- New output formats (CSV, Parquet, JSONL)

❌ **Out-of-scope (belongs in private TCS-PLATFORM SaaS)**
- TCI scoring formulas
- Thái Ất / Thiên Cơ Sách logic (L7)
- Trading signal generation
- Portfolio optimization / risk gates
- Anything that calls a paid TCS-PLATFORM API
- Vietnamese stock-specific recommendation logic

If you're unsure, open a **Discussion** before writing code.

---

## 2. Contributor License Grant (READ CAREFULLY)

By submitting a Pull Request, **you irrevocably agree** that:

1. **You own** the code you contribute (or have permission from the owner).
2. Your contribution is licensed to TCS-PLATFORM under the **MIT License** (same as this repo).
3. TCS-PLATFORM may **incorporate your contribution into proprietary derivatives** (the private TCS-PLATFORM SaaS) without further notice or compensation.
4. You waive any claim to royalties, attribution beyond the git history, or veto rights over how the code is used downstream.
5. The data sources you add **have licenses that permit redistribution**, and you confirm this in the PR checklist.

This is a **standard "inbound = MIT" contribution model**, similar to most open-source projects. We do not use a separate CLA document.

---

## 3. Code style

- **Python 3.11+**
- Format with `ruff format` (config in `pyproject.toml`)
- Lint with `ruff check`
- Type hints required for public APIs
- Docstrings (Google-style) for all new fetchers
- Tests with `pytest` — aim for ≥80% coverage on new code

```bash
ruff format .
ruff check .
pytest -q
```

---

## 4. Adding a new fetcher

Template:

```python
# tcs_macro_pulse/fetchers/your_source.py
"""
Fetcher for <Source Name>.

License: <e.g., CC-BY 4.0 — permits redistribution>
Rate limit: <e.g., 60 req/min, no key required>
Docs: <URL to source's official API docs>
"""

from __future__ import annotations
import requests
from typing import Any


class YourSourceFetcher:
    BASE_URL = "https://api.example.com/v1"

    def __init__(self, api_key: str | None = None, timeout: int = 30) -> None:
        self.api_key = api_key
        self.timeout = timeout

    def fetch(self, **params: Any) -> dict[str, Any]:
        """Fetch data. Returns dict with 'data' and 'metadata' keys."""
        ...
```

Add a CLI entrypoint:

```python
if __name__ == "__main__":
    import argparse, json
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="-")
    args = parser.parse_args()
    data = YourSourceFetcher().fetch()
    out = json.dumps(data, indent=2, ensure_ascii=False)
    if args.output == "-":
        print(out)
    else:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out)
```

Add a test:

```python
# tests/test_your_source.py
def test_fetcher_smoke():
    from tcs_macro_pulse.fetchers.your_source import YourSourceFetcher
    # Use mock or VCR.py to avoid real network calls in CI
    ...
```

---

## 5. Workflow

1. **Discuss first** for non-trivial changes — open an Issue or Discussion.
2. Fork → branch `feat/<short-name>` or `fix/<short-name>`.
3. Commit with [Conventional Commits](https://www.conventionalcommits.org/): `feat(fetchers): add IMF WEO fetcher`.
4. Open PR against `main`. Fill in the PR template completely.
5. CI must pass (lint + tests).
6. A maintainer will review within 7 days.

---

## 6. Reporting security issues

**Do NOT open a public issue.** See [SECURITY.md](SECURITY.md).

---

## 7. Code of Conduct

By participating, you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md).

---

## 8. Questions?

- **Open a [Discussion](https://github.com/TCS-PLATFORM-OFFICIAL/tcs-macro-pulse/discussions)** for general questions.
- **Email**: hello@tcs-platform.com (response within 3 business days).
