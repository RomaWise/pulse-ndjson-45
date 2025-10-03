#!/usr/bin/env python3
from __future__ import annotations
import json, hashlib, os
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

def kyiv_tz():
    now = datetime.now(timezone.utc)
    offset = 3 if 3 <= now.month <= 10 else 2   # груба EEST/EET без зовн. API
    return timezone(timedelta(hours=offset), name=f"UTC+{offset}")

def ny_tz():
    now = datetime.now(timezone.utc)
    offset = -4 if 3 <= now.month <= 11 else -5  # груба EDT/EST
    return timezone(timedelta(hours=offset), name=f"UTC{offset}")

def build_event() -> dict:
    now_utc = datetime.now(timezone.utc)
    kyiv = now_utc.astimezone(kyiv_tz())
    ny   = now_utc.astimezone(ny_tz())

    payload = {
        "ts_utc": now_utc.isoformat(timespec="seconds"),
        "unix": int(now_utc.timestamp()),
        "iso_week": int(now_utc.strftime("%V")),
        "weekday": int(now_utc.strftime("%u")),  # 1..7
        "minute": now_utc.minute,
        "hour": now_utc.hour,
        "day_of_year": int(now_utc.strftime("%j")),
        "kyiv": kyiv.isoformat(timespec="seconds"),
        "new_york": ny.isoformat(timespec="seconds"),
        "nonce": hashlib.sha256(os.urandom(16)).hexdigest()[:10],
        "format": "ndjson-pulse-v1"
    }
    # короткий контрольний хеш
    raw = "|".join(str(payload[k]) for k in ("ts_utc","iso_week","weekday","hour","minute"))
    payload["checksum"] = hashlib.sha256(raw.encode()).hexdigest()[:12]
    return payload

def main() -> int:
    now = datetime.now(timezone.utc)
    day_dir = DATA / now.strftime("%Y-%m-%d")
    day_dir.mkdir(parents=True, exist_ok=True)
    outfile = day_dir / "events.ndjson"

    event = build_event()
    with outfile.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

    rel = outfile.relative_to(ROOT)
    print(f"[update.py] appended -> {rel}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
