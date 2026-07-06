from skillvitals.skill import parse_skill
from skillvitals.run import heuristic_trigger, run_trigger, run_efficacy

SKILL = parse_skill(open("tests/fixtures/sample_skill.md").read())


def test_heuristic_fires_on_trigger_phrase():
    assert heuristic_trigger(SKILL, "help me add evals to my app") is True
    assert heuristic_trigger(SKILL, "what's the weather") is False


def test_run_trigger_metrics():
    cases = [
        {"prompt": "add evals please", "should_fire": True},
        {"prompt": "the weather", "should_fire": False},
    ]
    metrics, results = run_trigger(SKILL, cases, heuristic_trigger)
    assert metrics["recall"] == 1.0
    assert metrics["false_fire_rate"] == 0.0
    assert len(results) == 2


def test_run_efficacy_with_fakes():
    # fake task_fn: returns a longer answer when the skill is applied;
    # fake judge_fn: scores by length -> "with" should win.
    def task_fn(prompt, body):
        return "detailed answer with skill" if body else "short"

    def judge_fn(task, output):
        return float(len(output))

    metrics, pairs = run_efficacy(SKILL, [{"prompt": "q1"}, {"prompt": "q2"}], task_fn, judge_fn)
    assert metrics["win_rate"] == 1.0
    assert metrics["avg_delta"] > 0
