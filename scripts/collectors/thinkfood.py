"""식품음료신문 (thinkfood.co.kr) RSS collector — F&B category.

Confirmed working RSS feed as of 2026-09-28; the most reliable source in the
project's source list (see README) since it needs no scraping/headless browser.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import feedparser

from .base import CollectedItem, save_items

SOURCE_ID = "thinkfood"
SOURCE_NAME = "식품음료신문"
CATEGORY = "fnb"
FEED_URL = "https://www.thinkfood.co.kr/rss/allArticle.xml"
LOOKBACK_DAYS = 7


def collect(lookback_days: int = LOOKBACK_DAYS) -> list[CollectedItem]:
    feed = feedparser.parse(FEED_URL)
    cutoff = datetime.now(timezone.utc) - timedelta(days=lookback_days)

    items: list[CollectedItem] = []
    for entry in feed.entries:
        if not getattr(entry, "published_parsed", None):
            continue
        published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        if published < cutoff:
            continue
        items.append(
            CollectedItem(
                title=entry.title.strip(),
                link=entry.link,
                published=published.isoformat(),
                source=SOURCE_NAME,
                category=CATEGORY,
            )
        )
    return items


def run(out_dir: Path) -> Path:
    return save_items(collect(), out_dir, SOURCE_ID)


if __name__ == "__main__":
    result_path = run(Path("data/raw/latest"))
    print(f"Saved {result_path}")
