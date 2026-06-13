#!/usr/bin/env python3
"""Regenerate index.json (the catalog manifest) from the skills/ tree.

The manifest is the source of truth for "what skills exist" — there is no
directory listing over HTTP, so consumers load this first and lazy-fetch
full skill JSON only for skills they actually apply.

Usage:
    python scripts/generate_index.py          # rewrite index.json if stale
    python scripts/generate_index.py --check  # exit 1 if index.json is stale (CI)

`generated_at` is the consumer-side cache key, so it is only refreshed when
the catalog content actually changes; otherwise the file is left untouched.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.json"
SKILLS_DIR = ROOT / "skills"

MANIFEST_SCHEMA_VERSION = 2


def build_entries() -> list[dict]:
    entries = []
    for latest in sorted(SKILLS_DIR.glob("*/latest.json")):
        slug = latest.parent.name
        skill = json.loads(latest.read_text(encoding="utf-8"))
        entries.append(
            {
                "name": skill["name"],
                "slug": slug,
                "version": skill["version"],
                "description": skill["description"],
                "domains": skill["domains"],
                "review_status": skill["review_status"],
                "path": f"skills/{slug}/latest.json",
            }
        )
    return entries


def main() -> int:
    check_only = "--check" in sys.argv[1:]
    entries = build_entries()

    current = None
    if INDEX.exists():
        current = json.loads(INDEX.read_text(encoding="utf-8"))

    if current is not None and current.get("skills") == entries:
        print(f"index.json is up to date ({len(entries)} skills).")
        return 0

    if check_only:
        print(
            "index.json is stale — run `python scripts/generate_index.py` "
            "and commit the result.",
            file=sys.stderr,
        )
        return 1

    manifest = {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "skills": entries,
    }
    INDEX.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Wrote index.json ({len(entries)} skills).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
