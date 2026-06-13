#!/usr/bin/env python3
"""Validate every skill in skills/ against the JSON Schema, plus repo invariants.

Hard failures (exit 1):
  - any skill JSON violates schema/framework-skill.schema.json
  - a skill directory name does not match slugify(skill name)
  - latest.json does not equal the highest vN.json in its directory

Warnings (exit 0):
  - relationships.* entries that do not resolve to an existing skill slug.
    Dangling references are deliberate — they mark skills worth authoring
    (wiki redlinks) and feed WISHLIST.md.

Usage:
    python scripts/validate.py
    python scripts/validate.py --dangling   # only print dangling references
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schema" / "framework-skill.schema.json"
SKILLS_DIR = ROOT / "skills"


def slugify(name: str) -> str:
    # Must match frameworks/library.py:slugify_skill_name in the analyzer
    # and the slugs consumers use to fetch skills/<slug>/latest.json.
    return re.sub(r"[^a-z0-9]+", "-", name.strip().lower()).strip("-")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    dangling_only = "--dangling" in sys.argv[1:]
    validator = Draft202012Validator(load_json(SCHEMA_PATH))
    errors: list[str] = []
    catalog_slugs: set[str] = set()
    skills_by_slug: dict[str, dict] = {}

    for skill_dir in sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()):
        slug = skill_dir.name
        catalog_slugs.add(slug)
        versions = sorted(
            skill_dir.glob("v*.json"),
            key=lambda p: int(p.stem[1:]),
        )
        latest_path = skill_dir / "latest.json"

        if not versions:
            errors.append(f"{slug}: no vN.json files")
            continue
        if not latest_path.exists():
            errors.append(f"{slug}: missing latest.json")
            continue

        for path in [*versions, latest_path]:
            try:
                skill = load_json(path)
            except json.JSONDecodeError as exc:
                errors.append(f"{path.relative_to(ROOT)}: invalid JSON ({exc})")
                continue
            for err in validator.iter_errors(skill):
                where = "/".join(str(x) for x in err.absolute_path) or "<root>"
                errors.append(f"{path.relative_to(ROOT)}: {where}: {err.message}")

        latest = load_json(latest_path)
        highest = load_json(versions[-1])
        if latest != highest:
            errors.append(
                f"{slug}: latest.json differs from {versions[-1].name} "
                "(latest.json must be a copy of the newest version)"
            )
        if slugify(latest.get("name", "")) != slug:
            errors.append(
                f"{slug}: directory does not match slugify({latest.get('name')!r}) "
                f"= {slugify(latest.get('name', ''))!r}"
            )
        skills_by_slug[slug] = latest

    # Dangling relationship references — warn, never fail.
    dangling: dict[str, list[str]] = defaultdict(list)
    for slug, skill in skills_by_slug.items():
        for kind, names in skill.get("relationships", {}).items():
            for name in names:
                if slugify(name) not in catalog_slugs:
                    dangling[name].append(f"{slug}.{kind}")

    if dangling_only:
        for name in sorted(dangling):
            print(f"{name}  (referenced by: {', '.join(sorted(dangling[name]))})")
        return 0

    if dangling:
        print(f"NOTE: {len(dangling)} dangling relationship reference(s) — "
              "candidate skills to author (see WISHLIST.md):")
        for name in sorted(dangling):
            print(f"  - {name}  ({len(dangling[name])} reference(s))")

    if errors:
        print(f"\nFAIL: {len(errors)} error(s):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"\nOK: {len(catalog_slugs)} skills valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
