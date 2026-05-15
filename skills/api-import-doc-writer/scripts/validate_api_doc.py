#!/usr/bin/env python3
"""Validate Markdown API docs generated for field import tools."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ALLOWED_TYPES = {"string", "boolean", "integer", "object", "map", "array"}


def iter_import_json_blocks(text: str):
    for index, match in enumerate(
        re.finditer(r"Import JSON:\n\n```json\n(.*?)\n```", text, flags=re.S),
        start=1,
    ):
        yield index, match.group(1)


def walk_import_fields(value: Any, block_index: int, path: str, issues: list[str]) -> None:
    if isinstance(value, list):
        for item in value:
            walk_import_fields(item, block_index, path, issues)
        return

    if not isinstance(value, dict):
        return

    field_name = str(value.get("fieldName", "<anonymous>"))
    field_path = f"{path}.{field_name}" if path else field_name
    field_type = value.get("type")

    if field_type and field_type not in ALLOWED_TYPES:
        issues.append(
            f"JSON block {block_index}: {field_path} uses unsupported type {field_type!r}; "
            f"allowed types are {sorted(ALLOWED_TYPES)}"
        )

    if isinstance(field_name, str) and field_name.startswith("http_query_params:"):
        issues.append(
            f"JSON block {block_index}: {field_path} should keep fieldName as the raw parameter name; "
            "put the http_query_params hint in description"
        )

    if field_type == "object" and not value.get("children"):
        issues.append(f"JSON block {block_index}: object field {field_path} must have non-empty children")

    if field_type == "array":
        children = value.get("children") or []
        if len(children) != 1:
            issues.append(f"JSON block {block_index}: array field {field_path} must have exactly one child named items")
        elif children[0].get("fieldName") != "items":
            issues.append(f"JSON block {block_index}: array field {field_path} child must be named items")

    for child in value.get("children") or []:
        walk_import_fields(child, block_index, field_path, issues)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_api_doc.py <api-reference.md>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")
    issues: list[str] = []
    block_count = 0

    for block_index, block_text in iter_import_json_blocks(text):
        block_count += 1
        try:
            parsed = json.loads(block_text)
        except json.JSONDecodeError as exc:
            issues.append(f"JSON block {block_index}: invalid JSON: {exc}")
            continue
        walk_import_fields(parsed, block_index, "", issues)

    if block_count == 0:
        issues.append("No Import JSON blocks found")

    if issues:
        for issue in issues:
            print(issue, file=sys.stderr)
        return 1

    print(f"OK: {block_count} JSON block(s), import field types are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
