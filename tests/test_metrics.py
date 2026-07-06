from skillvitals.metrics import trigger_metrics, efficacy_metrics


def test_trigger_perfect():
    r = [{"should_fire": True, "fired": True}, {"should_fire": False, "fired": False}]
    m = trigger_metrics(r)
    assert m["recall"] == 1.0 and m["false_fire_rate"] == 0.0 and m["f1"] == 1.0


def test_trigger_misses_and_false_fires():
    r = [
        {"should_fire": True, "fired": False},   # miss
        {"should_fire": True, "fired": True},    # hit
        {"should_fire": False, "fired": True},   # false fire
        {"should_fire": False, "fired": False},  # correct quiet
    ]
    m = trigger_metrics(r)
    assert m["recall"] == 0.5
    assert m["false_fire_rate"] == 0.5
    assert m["precision"] == 0.5


def test_efficacy_delta():
    pairs = [{"with": 8, "without": 5}, {"with": 6, "without": 6}, {"with": 4, "without": 7}]
    m = efficacy_metrics(pairs)
    assert m["n"] == 3
    assert m["win_rate"] == round(1 / 3, 3)
    assert m["tie_rate"] == round(1 / 3, 3)
    assert m["avg_delta"] == round((3 + 0 + -3) / 3, 3)


def test_efficacy_empty():
    assert efficacy_metrics([])["n"] == 0
