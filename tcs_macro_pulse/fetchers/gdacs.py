"""
L2 News/Events Fetcher — GDACS (Global Disaster Alert and Coordination System)
===============================================================================
Fetches natural disaster events from GDACS public API.

No API key required. Data is public domain.

Data source: https://www.gdacs.org
Terms of use: https://www.gdacs.org/About/usage.aspx (free, with attribution)
"""

from __future__ import annotations

import json
import logging
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from typing import Any

import requests

logger = logging.getLogger(__name__)

GDACS_RSS = "https://www.gdacs.org/xml/rss.xml"
GDACS_API = "https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH"

ALERT_SEVERITY: dict[str, int] = {
    "Red": 3,
    "Orange": 2,
    "Green": 1,
}


class GDACSSentinel:
    """Fetch and score natural disaster events from GDACS.

    Usage:
        sentinel = GDACSSentinel()
        events = sentinel.fetch_recent(days=7)
        risk_score = sentinel.compute_risk_score(events)
    """

    def fetch_recent(self, days: int = 7) -> list[dict[str, Any]]:
        """Fetch recent disaster events from GDACS RSS feed.

        Returns list of event dicts:
            {
                "event_id": "TC1001568",
                "type": "Tropical Cyclone",
                "title": "Cyclone Mocha - Bangladesh",
                "country": "Bangladesh",
                "alert_level": "Red",
                "severity_score": 3,
                "latitude": 22.5,
                "longitude": 91.8,
                "date": "2026-05-04T12:00:00",
                "url": "https://...",
            }
        """
        try:
            resp = requests.get(GDACS_RSS, timeout=15, headers={"User-Agent": "tcs-macro-pulse/0.1"})
            resp.raise_for_status()
            return self._parse_rss(resp.text, days=days)
        except requests.RequestException as e:
            logger.warning("GDACS fetch failed: %s", e)
            return []

    def _parse_rss(self, xml_text: str, days: int = 7) -> list[dict[str, Any]]:
        """Parse GDACS RSS XML."""
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        events: list[dict[str, Any]] = []

        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError as e:
            logger.error("GDACS XML parse error: %s", e)
            return []

        # GDACS uses gdacs: namespace
        ns = {
            "gdacs": "http://www.gdacs.org",
            "geo":   "http://www.w3.org/2003/01/geo/wgs84_pos#",
        }

        channel = root.find("channel")
        if channel is None:
            return []

        for item in channel.findall("item"):
            try:
                pub_date_str = (item.findtext("pubDate") or "").strip()
                # Parse RFC 2822 date
                from email.utils import parsedate_to_datetime
                pub_date = parsedate_to_datetime(pub_date_str).replace(tzinfo=timezone.utc) if pub_date_str else None

                if pub_date and pub_date < cutoff:
                    continue

                alert_level = item.findtext("gdacs:alertlevel", namespaces=ns) or "Green"
                event = {
                    "event_id":      item.findtext("gdacs:eventid", namespaces=ns) or "",
                    "type":          item.findtext("gdacs:eventtype", namespaces=ns) or "Unknown",
                    "title":         item.findtext("title") or "",
                    "country":       item.findtext("gdacs:country", namespaces=ns) or "",
                    "alert_level":   alert_level,
                    "severity_score": ALERT_SEVERITY.get(alert_level, 0),
                    "latitude":      self._safe_float(item.findtext("geo:lat", namespaces=ns)),
                    "longitude":     self._safe_float(item.findtext("geo:long", namespaces=ns)),
                    "date":          pub_date.isoformat() if pub_date else None,
                    "url":           item.findtext("link") or "",
                }
                events.append(event)
            except Exception as e:
                logger.debug("Skip GDACS item due to parse error: %s", e)
                continue

        return events

    def compute_risk_score(self, events: list[dict[str, Any]]) -> dict[str, Any]:
        """Compute overall macro risk score from disaster events.

        Returns:
            {
                "risk_level": "GREEN" | "AMBER" | "RED",
                "risk_score": 0-100,
                "n_red": 2,
                "n_orange": 1,
                "n_total": 8,
                "dominant_types": ["Tropical Cyclone", "Earthquake"],
            }
        """
        if not events:
            return {"risk_level": "GREEN", "risk_score": 0, "n_red": 0, "n_orange": 0, "n_total": 0, "dominant_types": []}

        n_red = sum(1 for e in events if e["alert_level"] == "Red")
        n_orange = sum(1 for e in events if e["alert_level"] == "Orange")
        n_total = len(events)

        # Simple scoring: Red=15pts, Orange=5pts, capped at 100
        raw_score = min(100, n_red * 15 + n_orange * 5)

        if raw_score >= 30:
            risk_level = "RED"
        elif raw_score >= 10:
            risk_level = "AMBER"
        else:
            risk_level = "GREEN"

        # Get dominant event types
        from collections import Counter
        type_counts = Counter(e["type"] for e in events)
        dominant = [t for t, _ in type_counts.most_common(3)]

        return {
            "risk_level": risk_level,
            "risk_score": raw_score,
            "n_red": n_red,
            "n_orange": n_orange,
            "n_total": n_total,
            "dominant_types": dominant,
        }

    @staticmethod
    def _safe_float(val: str | None) -> float | None:
        try:
            return float(val) if val else None
        except (ValueError, TypeError):
            return None


if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    sentinel = GDACSSentinel()
    events = sentinel.fetch_recent(days=14)
    risk = sentinel.compute_risk_score(events)

    print(f"\nGDACS Events (last 14 days): {len(events)}")
    print(f"Risk Score: {risk['risk_score']}/100 ({risk['risk_level']})")
    print(f"Red alerts: {risk['n_red']} · Orange: {risk['n_orange']}")
    print(f"Dominant types: {', '.join(risk['dominant_types'])}\n")

    for e in events[:5]:
        print(f"  [{e['alert_level']}] {e['type']} · {e['country']} · {e['date'][:10]}")
