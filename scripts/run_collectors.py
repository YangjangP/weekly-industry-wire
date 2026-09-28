"""Run all configured collectors and write raw JSON under data/raw/<iso-week>/.

Usage:
    python scripts/run_collectors.py
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from collectors import thinkfood  # noqa: E402

COLLECTORS = [thinkfood]


def main() -> None:
    run_id = datetime.now(timezone.utc).strftime("%G-W%V")
    out_dir = Path("data/raw") / run_id

    for collector in COLLECTORS:
        path = collector.run(out_dir)
        print(f"[{collector.SOURCE_ID}] -> {path}")


if __name__ == "__main__":
    main()
