"""
L3 Social/News Fetcher — Keyword-based Sentiment Analyzer
==========================================================
Lightweight keyword-based sentiment scoring for financial headlines.

This is a SIMPLE baseline — for production-grade NLP, install with `[nlp]`
extras and use FinBERT (transformers).
"""

from __future__ import annotations

from typing import Iterable

# Curated keyword dictionaries (can be extended)
BULLISH_KEYWORDS: set[str] = {
    "rally", "surge", "rise", "gain", "jump", "soar", "climb", "rebound",
    "boost", "upbeat", "optimism", "growth", "expand", "beat", "outperform",
    "bullish", "uptrend", "breakout", "all-time high", "record high",
    "rate cut", "stimulus", "easing", "dovish", "buy", "upgrade",
    # Vietnamese
    "tăng", "phục hồi", "khởi sắc", "đột phá", "kỷ lục", "tích cực",
}

BEARISH_KEYWORDS: set[str] = {
    "crash", "plunge", "fall", "drop", "tumble", "slump", "decline", "loss",
    "weak", "worry", "concern", "fear", "panic", "bearish", "downtrend",
    "miss", "underperform", "downgrade", "sell", "recession", "default",
    "rate hike", "tightening", "hawkish", "inflation", "deflation",
    "war", "conflict", "sanction", "crisis", "collapse", "bankruptcy",
    # Vietnamese
    "giảm", "lao dốc", "sụp đổ", "khủng hoảng", "tiêu cực", "rủi ro",
}


class KeywordSentiment:
    """Simple keyword-matching sentiment analyzer.

    Usage:
        analyzer = KeywordSentiment()
        result = analyzer.analyze_headlines([
            "Fed signals rate cut",
            "China PMI falls below 50",
        ])
    """

    def __init__(
        self,
        bullish_words: set[str] | None = None,
        bearish_words: set[str] | None = None,
    ) -> None:
        self.bullish = {w.lower() for w in (bullish_words or BULLISH_KEYWORDS)}
        self.bearish = {w.lower() for w in (bearish_words or BEARISH_KEYWORDS)}

    def classify(self, text: str) -> str:
        """Classify a single text. Returns 'BULLISH', 'BEARISH', or 'NEUTRAL'."""
        if not text:
            return "NEUTRAL"
        text_lower = text.lower()

        bullish_hits = sum(1 for w in self.bullish if w in text_lower)
        bearish_hits = sum(1 for w in self.bearish if w in text_lower)

        if bullish_hits > bearish_hits:
            return "BULLISH"
        if bearish_hits > bullish_hits:
            return "BEARISH"
        return "NEUTRAL"

    def analyze_headlines(self, headlines: Iterable[str]) -> dict[str, object]:
        """Aggregate sentiment over a list of headlines.

        Returns:
            {
                "overall": "BULLISH" | "BEARISH" | "NEUTRAL",
                "bullish": 5,
                "bearish": 2,
                "neutral": 3,
                "total": 10,
                "score": 0.3,   # net score: (bull-bear)/total in [-1, 1]
            }
        """
        counts = {"BULLISH": 0, "BEARISH": 0, "NEUTRAL": 0}
        for h in headlines:
            counts[self.classify(h)] += 1

        total = sum(counts.values())
        if total == 0:
            return {"overall": "NEUTRAL", "bullish": 0, "bearish": 0, "neutral": 0, "total": 0, "score": 0.0}

        score = (counts["BULLISH"] - counts["BEARISH"]) / total
        if score >= 0.2:
            overall = "BULLISH"
        elif score <= -0.2:
            overall = "BEARISH"
        else:
            overall = "NEUTRAL"

        return {
            "overall":  overall,
            "bullish":  counts["BULLISH"],
            "bearish":  counts["BEARISH"],
            "neutral":  counts["NEUTRAL"],
            "total":    total,
            "score":    round(score, 3),
        }


if __name__ == "__main__":
    analyzer = KeywordSentiment()

    sample = [
        "Fed signals rate cut in September meeting",
        "China PMI falls below 50, raising recession fears",
        "VN-Index hits 1300 resistance level",
        "Apple beats Q2 earnings expectations",
        "Oil prices crash on demand concerns",
        "Bitcoin rallies to all-time high above $80,000",
    ]

    print("Headlines analyzed:")
    for h in sample:
        print(f"  [{analyzer.classify(h)}] {h}")

    result = analyzer.analyze_headlines(sample)
    print(f"\nAggregate: {result}")
