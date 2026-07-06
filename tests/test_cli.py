import json
from skillvitals.cli import main


def test_trigger_offline_heuristic(capsys):
    rc = main(["trigger", "tests/fixtures/sample_skill.md",
               "--cases", "tests/fixtures/cases.yaml", "--json"])
    data = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert data["trigger"]["n"] == 5
    assert data["trigger"]["recall"] >= 0.6  # heuristic catches the quoted-phrase cases


def test_efficacy_requires_model(capsys):
    rc = main(["efficacy", "tests/fixtures/sample_skill.md", "--tasks", "tests/fixtures/cases.yaml"])
    assert rc == 2  # no --model
