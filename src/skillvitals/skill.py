from __future__ import annotations
import re
from dataclasses import dataclass


@dataclass
class Skill:
    name: str
    description: str
    body: str


_FM = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.S)


def _yaml_lite(text: str) -> dict:
    """Parse the tiny subset of YAML used in SKILL.md frontmatter (key: value)."""
    out = {}
    key = None
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            key = m.group(1).strip()
            val = m.group(2).strip()
            out[key] = val.strip('"').strip("'")
        elif key and line.startswith((" ", "\t")):
            out[key] = (out.get(key, "") + " " + line.strip()).strip()
    return out


def parse_skill(text: str) -> Skill:
    m = _FM.match(text.lstrip("﻿"))
    if not m:
        raise ValueError("SKILL.md must start with a YAML frontmatter block (--- ... ---)")
    meta = _yaml_lite(m.group(1))
    if not meta.get("name"):
        raise ValueError("skill frontmatter missing 'name'")
    if not meta.get("description"):
        raise ValueError("skill frontmatter missing 'description'")
    return Skill(name=meta["name"], description=meta["description"], body=m.group(2).strip())
