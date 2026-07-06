import json
from skillvitals.report import render_human, render_json, badge_endpoint


def test_human_trigger():
    out = render_human(trigger={"recall": 1.0, "false_fire_rate": 0.0, "f1": 1.0, "n": 5})
    assert "trigger" in out and "f1" in out


def test_json_shape():
    data = json.loads(render_json(trigger={"f1": 0.9}, efficacy=None))
    assert data["trigger"]["f1"] == 0.9 and data["efficacy"] is None


def test_badge_color():
    b = badge_endpoint(trigger={"f1": 0.9})
    assert b["label"] == "skill vitals" and b["color"] == "green"
    assert badge_endpoint(trigger={"f1": 0.5})["color"] == "red"
