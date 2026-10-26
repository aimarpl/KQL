#!/usr/bin/env python3
"""Validate the metadata header on every .kql file in the repository.

Each query must open with a comment block naming its title, platform,
category, tags, description and data sources, so queries stay findable as the
library grows across solutions.

Usage:
    python3 tools/validate-kql-metadata.py [path ...]

Exits 0 when every file passes, 1 when any file fails.
"""

from __future__ import annotations

import pathlib
import re
import sys

REQUIRED_FIELDS = ("Title", "Platform", "Category", "Tags", "Description", "Data sources")

ALLOWED_PLATFORMS = {
    "Microsoft Sentinel / Log Analytics",
    "Microsoft Defender XDR / Advanced Hunting",
    "Azure Data Explorer",
    "Multiple",
}

# Categories group queries by purpose. Add a new one here and in the README
# together, so the two never drift apart.
ALLOWED_CATEGORIES = {
    "Identity - MFA",
    "Identity - Sign-in risk",
    "Identity - Privileged access",
    "Endpoint",
    "Email",
    "Network",
    "Operations",
}

FIELD_PATTERN = re.compile(r"^//\s*([A-Za-z][A-Za-z ]*?)\s*:\s*(.*)$")
TAG_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def parse_header(path: pathlib.Path) -> dict[str, str]:
    """Read the leading comment block as field/value pairs."""
    fields: dict[str, str] = {}
    last_field: str | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line.startswith("//"):
            break

        match = FIELD_PATTERN.match(line)
        if match:
            name, value = match.group(1).strip(), match.group(2).strip()
            fields[name] = value
            last_field = name
        elif last_field:
            # A continuation line keeps the previous field's value readable
            # across several lines.
            fields[last_field] += " " + line.lstrip("/ ").strip()

    return fields


def validate(path: pathlib.Path) -> list[str]:
    """Return a list of problems; empty means the file is valid."""
    problems: list[str] = []
    fields = parse_header(path)

    if not fields:
        return ["no metadata header found (file must start with // comments)"]

    for field in REQUIRED_FIELDS:
        if not fields.get(field):
            problems.append(f"missing or empty // {field}:")

    platform = fields.get("Platform", "")
    if platform and platform not in ALLOWED_PLATFORMS:
        allowed = ", ".join(sorted(ALLOWED_PLATFORMS))
        problems.append(f"Platform '{platform}' is not one of: {allowed}")

    category = fields.get("Category", "")
    if category and category not in ALLOWED_CATEGORIES:
        allowed = ", ".join(sorted(ALLOWED_CATEGORIES))
        problems.append(f"Category '{category}' is not one of: {allowed}")

    tags = fields.get("Tags", "")
    if tags:
        for tag in (item.strip() for item in tags.split(",")):
            if not tag:
                problems.append("Tags contains an empty entry")
            elif not TAG_PATTERN.match(tag):
                problems.append(f"tag '{tag}' must be lowercase kebab-case")

    return problems


def main(argv: list[str]) -> int:
    roots = [pathlib.Path(arg) for arg in argv[1:]] or [pathlib.Path(".")]

    files: list[pathlib.Path] = []
    for root in roots:
        files.extend([root] if root.is_file() else sorted(root.rglob("*.kql")))

    if not files:
        print("No .kql files found.")
        return 0

    failed = 0
    for path in files:
        problems = validate(path)
        if problems:
            failed += 1
            print(f"FAIL {path}")
            for problem in problems:
                print(f"       {problem}")
        else:
            print(f"ok   {path}")

    print(f"\n{len(files) - failed}/{len(files)} file(s) passed.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
