"""Shared helpers for source collectors."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class CollectedItem:
    title: str
    link: str
    published: str  # ISO 8601, UTC
    source: str
    category: str  # "fashion" | "beauty" | "fnb" | "media"


def save_items(items: list[CollectedItem], out_dir: Path, source_id: str) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{source_id}.json"
    payload = {
        "source_id": source_id,
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "items": [asdict(item) for item in items],
    }
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_path
