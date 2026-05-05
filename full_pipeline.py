"""
Full L1-L3 Pipeline Demo
========================
Demonstrates fetching from FRED + GDACS + sentiment analysis.

Run:
    python examples/full_pipeline.py
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone

from tcs_macro_pulse.fetchers.fred import FREDFetcher
from tcs_macro_pulse.fetchers.gdacs import GDACSSentinel
from tcs_macro_pulse.analysis.keyword_sentiment import KeywordSentiment


def main() -> dict:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    print("=" * 60)
    print("  TCS Macro Pulse — Full L1-L3 Pipeline Demo")
    print("=" * 60)

    # L1: Macro from FRED
    print("\n[L1] Fetching FRED macro indicators...")
    fred = FREDFetcher()
    macro = fred.fetch_key_indicators()
    yield_spread = fred.yield_curve_spread()
    print(f"  Fed Funds Rate: {macro.get('fed_funds_rate')}%")
    print(f"  10Y Treasury: {macro.get('10y_treasury')}%")
    print(f"  Yield Curve (10Y-2Y): {yield_spread} bps")
    print(f"  VIX: {macro.get('vix')}")

    # L2: Disaster events from GDACS
    print("\n[L2] Fetching GDACS disaster events (last 14 days)...")
    gdacs = GDACSSentinel()
    events = gdacs.fetch_recent(days=14)
    risk = gdacs.compute_risk_score(events)
    print(f"  Total events: {risk['n_total']}")
    print(f"  Risk Level: {risk['risk_level']} (score {risk['risk_score']}/100)")

    # L3: Sentiment from sample headlines (in real use: pull from RSS)
    print("\n[L3] Analyzing sample headlines...")
    sample_headlines = [
        "Fed signals possible rate cut in September",
        "China PMI falls below 50, raising recession fears",
        "VN-Index breaks resistance at 1300",
        "Bitcoin rallies on ETF inflows",
    ]
    analyzer = KeywordSentiment()
    sentiment = analyzer.analyze_headlines(sample_headlines)
    print(f"  Overall sentiment: {sentiment['overall']}")
    print(f"  Score: {sentiment['score']:+.2f} (bull={sentiment['bullish']}, bear={sentiment['bearish']}, neutral={sentiment['neutral']})")

    # Combine
    snapshot = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "L1_macro":     macro,
        "L1_yield_spread_bps": yield_spread,
        "L2_disaster_risk":    risk,
        "L3_sentiment":        sentiment,
    }

    output_path = "macro_pulse_snapshot.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False, default=str)

    print(f"\n✅ Snapshot saved to {output_path}")
    print("\n→ Want L4-L9 analysis (TCI scoring, AI signals)?")
    print("   ⭐ Star this repo + open a Trial Request issue for 30-day Pro trial:")
    print("      https://github.com/TCS-PLATFORM-OFFICIAL/tcs-macro-pulse/issues/new\n")

    return snapshot


if __name__ == "__main__":
    main()
