# tcs-macro-pulse 🌏

> **Real-time macro signal pipeline** — L1-L3 data fetchers for global markets.  
> Built by [TCS-PLATFORM](https://github.com/TCS-PLATFORM-OFFICIAL) · MIT License

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![⭐ Star this repo](https://img.shields.io/badge/%E2%AD%90_Star-for_Pro_Trial-gold)](https://github.com/TCS-PLATFORM-OFFICIAL/tcs-macro-pulse/issues/new?template=trial-request.md)

---

## What is this?

`tcs-macro-pulse` is the **open-source L1-L3 macro data pipeline** powering [TCS-PLATFORM](https://tcs-platform-rust.vercel.app) — a Vietnamese investment intelligence system.

We open-source the data collection layer (L1-L3) so the community can:
- Build their own macro dashboards
- Contribute new data sources
- Research macro-market correlations

**What stays private**: Our L4-L9 proprietary analysis engine (Thái Ất / TCI scoring system) — that's our IP.

---

## Features (L1-L3 Open Source)

| Layer | Source | What it fetches |
|---|---|---|
| **L1 Macro** | FRED (US Federal Reserve) | GDP, CPI, Fed Funds Rate, Unemployment, M2 |
| **L1 Macro** | World Bank | Global GDP growth, Inflation by country |
| **L2 News** | GDACS | Natural disasters + severity scores |
| **L2 News** | ACLED | Conflict/protest events by country |
| **L2 News** | ReliefWeb | Humanitarian crisis updates |
| **L3 Social** | RSS feeds | Curated financial news sentiment (keyword-based) |

---

## Quick Start

```bash
# Install
pip install tcs-macro-pulse

# Or from source
git clone https://github.com/TCS-PLATFORM-OFFICIAL/tcs-macro-pulse
cd tcs-macro-pulse
pip install -e .

# Fetch FRED macro data (no API key needed for basic indicators)
python -m tcs_macro_pulse.fetchers.fred --output macro_data.json

# Fetch GDACS disaster events
python -m tcs_macro_pulse.fetchers.gdacs --days 30 --output disasters.json

# Full pipeline
python examples/full_pipeline.py
```

---

## ⭐ Get 30-Day Pro Trial

**Star this repo + open a [Trial Request issue](https://github.com/TCS-PLATFORM-OFFICIAL/tcs-macro-pulse/issues/new?title=Pro+Trial+Request&body=GitHub+username%3A+%0AEmail%3A+) → 30 days TCS-PLATFORM Pro free** (worth $29)

Live demo: [tcs-platform-rust.vercel.app](https://tcs-platform-rust.vercel.app)

Pro tier includes:
- L4-L9 TCI scoring (our proprietary engine)
- 10 VN stocks + 5 global assets tracked daily
- AI Quân Sư chatbot access
- Risk alerts via Telegram/Zalo

---

## Architecture

```
tcs-macro-pulse (OSS — this repo)
├── L1: Macro data (FRED, World Bank, IMF)
├── L2: News/events (GDACS, ACLED, ReliefWeb)  
└── L3: Social signals (RSS, keyword sentiment)

TCS-PLATFORM (Private — our SaaS)
├── L4: Technical analysis
├── L5: Sentiment scoring
├── L6: Fundamental analysis
├── L7: Thái Ất / Thiên Cơ Sách (PROPRIETARY — NOT in this repo)
├── L8: Macro synthesis
└── L9: Final signal generation
```

---

## Usage Examples

### Fetch FRED data
```python
from tcs_macro_pulse.fetchers.fred import FREDFetcher

fetcher = FREDFetcher()
data = fetcher.fetch_key_indicators()
print(data)
# {'fed_funds_rate': 5.33, 'cpi_yoy': 3.4, 'unemployment': 3.9, 'gdp_growth': 2.8}
```

### Fetch GDACS disasters
```python
from tcs_macro_pulse.fetchers.gdacs import GDACSSentinel

sentinel = GDACSSentinel()
events = sentinel.fetch_recent(days=7)
for e in events:
    print(f"{e['type']} · {e['country']} · severity {e['alert_level']}")
```

### Keyword-based news sentiment
```python
from tcs_macro_pulse.analysis.keyword_sentiment import KeywordSentiment

analyzer = KeywordSentiment()
result = analyzer.analyze_headlines(headlines=[
    "Fed signals rate cut in September",
    "China PMI falls below 50",
    "VN-Index hits 1300 resistance",
])
print(result)
# {'overall': 'NEUTRAL', 'bullish': 1, 'bearish': 1, 'neutral': 1, 'score': 0.0}
```

---

## Contributing

1. Fork → branch `feat/your-feature`
2. Add a new fetcher in `tcs_macro_pulse/fetchers/`
3. Add tests in `tests/`
4. PR with description of data source + license confirmation

**Contribution ideas**:
- IMF World Economic Outlook fetcher
- Eurostat GDP fetcher
- Twitter/X financial sentiment (requires API key)
- Crypto Fear & Greed Index
- VN macro data (GSO, SBV)

---

## License

MIT © 2026 TCS-PLATFORM. See [LICENSE](LICENSE).

Data sources have their own terms of use — see each fetcher's docstring.

---

## Disclaimer

This is a data collection tool only. No investment advice. Past data does not guarantee future results.
