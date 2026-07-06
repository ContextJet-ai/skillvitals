import json


def _color(v):
    return "green" if v >= 0.8 else "yellow" if v >= 0.6 else "red"


def render_human(trigger=None, efficacy=None) -> str:
    lines = ["skill vitals", ""]
    if trigger is not None:
        lines += [
            "trigger:",
            f"  fires when it should (recall):     {trigger['recall']:.0%}",
            f"  false-fires when it shouldn't:     {trigger['false_fire_rate']:.0%}",
            f"  f1:                                {trigger['f1']:.2f}  ({trigger['n']} cases)",
            "",
        ]
    if efficacy is not None:
        lines += [
            "efficacy (with skill vs without):",
            f"  win rate:   {efficacy['win_rate']:.0%}",
            f"  avg delta:  {efficacy['avg_delta']:+.2f}  ({efficacy['n']} tasks)",
            "",
        ]
    return "\n".join(lines).rstrip()


def render_json(trigger=None, efficacy=None) -> str:
    return json.dumps({"trigger": trigger, "efficacy": efficacy}, indent=2)


def badge_endpoint(trigger=None, efficacy=None) -> dict:
    if trigger is not None:
        msg, val = f"trigger f1 {trigger['f1']:.2f}", trigger["f1"]
    elif efficacy is not None:
        msg, val = f"help +{efficacy['avg_delta']:.1f}", 1.0 if efficacy["win_rate"] >= 0.6 else 0.5
    else:
        msg, val = "n/a", 0.0
    return {"schemaVersion": 1, "label": "skill vitals", "message": msg, "color": _color(val)}
