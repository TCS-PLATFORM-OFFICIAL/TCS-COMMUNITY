"""
L1 Macro Fetcher — FRED (US Federal Reserve Economic Data)
===========================================================
Fetches key macroeconomic indicators from FRED public API.

No API key required for public series.
Optional: set FRED_API_KEY env var for higher rate limits.

Data source: https://fred.stlouisfed.org
Terms of use: https://fred.stlouisfed.org/legal/ (public, free to use)
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Any

import requests

logger = logging.getLogger(__name__)

FRED_BASE = "https://api.stlouisfed.org/fred/series/observations"

# Key indicators — all public FRED series
KEY_INDICATORS: dict[str, str] = {
    "fed_funds_rate":  "FEDFUNDS",      # Federal Funds Rate (%)
    "cpi_yoy":         "CPIAUCSL",      # CPI All Urban (index)
    "unemployment":    "UNRATE",        # Unemployment Rate (%)
    "gdp_growth":      "A191RL1Q225SBEA",  # Real GDP QoQ growth (%)
    "m2_growth":       "M2SL",          # M2 Money Supply (B USD)
    "10y_treasury":    "DGS10",         # 10-Year Treasury Rate (%)
    "2y_treasury":     "DGS2",          # 2-Year Treasury Rate (%)
    "vix":             "VIXCLS",        # VIX Volatility Index
    "sp500":           "SP500",         # S&P 500 index
    "hy_spread":       "BAMLH0A0HYM2",  # High Yield Bond Spread (bps)
}


class FREDFetcher:
    """Fetch key macro indicators from FRED.

    Usage:
        fetcher = FREDFetcher()
        data = fetcher.fetch_key_indicators()
    """

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.environ.get("FRED_API_KEY", "")

    def _fetch_series(self, series_id: str, observation_start: str | None = None) -> list[dict]:
        """Fetch observations for a single FRED series."""
        params: dict[str, Any] = {
            "series_id": series_id,
            "file_type": "json",
            "sort_order": "desc",
            "limit": 5,
        }
        if self.api_key:
            params["api_key"] = self.api_key
        if observation_start:
            params["observation_start"] = observation_start

        try:
            resp = requests.get(FRED_BASE, params=params, timeout=10)
            resp.raise_for_status()
            return resp.json().get("observations", [])
        except requests.RequestException as e:
            logger.warning("FRED fetch failed for %s: %s", series_id, e)
            return []

    def fetch_latest(self, series_id: str) -> dict[str, Any]:
        """Return the latest non-null observation for a series."""
        obs = self._fetch_series(series_id)
        for o in obs:
            if o.get("value") not in (".", None, ""):
                return {
                    "series_id": series_id,
                    "date": o["date"],
                    "value": float(o["value"]),
                }
        return {"series_id": series_id, "date": None, "value": None}

    def fetch_key_indicators(self) -> dict[str, Any]:
        """Fetch all key indicators and return as a flat dict.

        Returns:
            {
                "fed_funds_rate": 5.33,
                "cpi_yoy": 313.1,
                "unemployment": 3.9,
                ...
                "generated_at": "2026-05-05T...",
                "source": "FRED",
            }
        """
        result: dict[str, Any] = {}
        for name, series_id in KEY_INDICATORS.items():
            obs = self.fetch_latest(series_id)
            result[name] = obs["value"]
            result[f"{name}_date"] = obs["date"]
            logger.debug("FRED %s (%s) = %s @ %s", name, series_id, obs["value"], obs["date"])

        result["generated_at"] = datetime.now(timezone.utc).isoformat()
        result["source"] = "FRED (Federal Reserve Bank of St. Louis)"
        return result

    def yield_curve_spread(self) -> float | None:
        """10Y - 2Y spread in basis points. Negative = inverted curve."""
        t10 = self.fetch_latest("DGS10")
        t2 = self.fetch_latest("DGS2")
        if t10["value"] is not None and t2["value"] is not None:
            spread = (t10["value"] - t2["value"]) * 100
            return round(spread, 1)
        return None


if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    fetcher = FREDFetcher()
    data = fetcher.fetch_key_indicators()

    output_path = sys.argv[1] if len(sys.argv) > 1 else None
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Saved to {output_path}")
    else:
        print(json.dumps(data, indent=2, ensure_ascii=False))

    spread = fetcher.yield_curve_spread()
    print(f"\nYield curve (10Y-2Y): {spread} bps")
    if spread is not None and spread < 0:
        print("⚠️  Yield curve inverted — recession risk indicator elevated")
