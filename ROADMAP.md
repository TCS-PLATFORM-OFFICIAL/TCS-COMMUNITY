# Roadmap

> Public roadmap for the **L1–L3 open-source layer** of TCS-PLATFORM.
> Items related to L4–L9 (TCI, Thái Ất, signals) are tracked in the private SaaS, not here.

Status legend: 🟢 Done · 🟡 In progress · 🔵 Planned · ⚪ Idea (community input welcome)

## L1 — Macro Fetchers

- 🟢 FRED (US Fed) — GDP, CPI, Fed Funds Rate, M2, unemployment
- 🟢 World Bank — country GDP/CPI
- 🔵 IMF World Economic Outlook (WEO)
- 🔵 Eurostat (EU GDP, inflation)
- ⚪ GSO Vietnam (Tổng cục Thống kê) — VN macro
- ⚪ SBV (Ngân hàng Nhà nước) — VN policy rates, FX reserves
- ⚪ China NBS (National Bureau of Statistics)
- ⚪ Bank of Japan (BoJ) policy rate

## L2 — Event / News Fetchers

- 🟢 GDACS — global natural disasters
- 🟢 ACLED — conflict / protest events
- 🟢 ReliefWeb — humanitarian crisis updates
- 🔵 USGS earthquake feed
- 🔵 NOAA tropical storm feed
- ⚪ EU Sanctions list updates
- ⚪ OFAC sanctions feed

## L3 — Sentiment / Social

- 🟢 Keyword-based RSS sentiment
- 🔵 Reddit r/wallstreetbets ticker mentions (read-only API)
- ⚪ Crypto Fear & Greed Index integration
- ⚪ HackerNews top-N ticker mentions
- ⚪ Google Trends momentum

## Quality / DX

- 🟡 Async fetchers (`httpx` + `asyncio`)
- 🔵 SQLite cache layer (avoid repeated API hits)
- 🔵 CLI tool `tcs-macro fetch <source>` instead of `python -m ...`
- 🔵 Docker image for one-command deployment
- ⚪ Streamlit demo dashboard
- ⚪ TypeScript port of fetchers (npm package)

## How to influence this roadmap

1. **Vote** on a 🔵 or ⚪ item — open a Discussion thread or thumbs-up an existing one
2. **Propose new** items via [Feature Request issue](https://github.com/TCS-PLATFORM-OFFICIAL/TCS-COMMUNITY/issues/new?template=feature_request.yml)
3. **Build** an item — open a PR; we'll prioritize merging community-built fetchers
