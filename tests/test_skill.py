import pytest
from skillvitals.skill import parse_skill

GOOD = """---
name: add-llm-evals
description: Use this when adding evaluation to an LLM app. Trigger on "add evals", "test my prompt".
---

# Add evals

Do the thing.
"""


def test_parse_good_skill():
    s = parse_skill(GOOD)
    assert s.name == "add-llm-evals"
    assert "add evals" in s.description
    assert s.body.startswith("# Add evals")


def test_missing_frontmatter_raises():
    with pytest.raises(ValueError):
        parse_skill("# just markdown, no frontmatter")


def test_missing_name_raises():
    with pytest.raises(ValueError):
        parse_skill("---\ndescription: x\n---\nbody")
