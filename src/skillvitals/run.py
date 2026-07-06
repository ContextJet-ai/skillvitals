"""Orchestration. Takes injected callables so it stays testable without a model."""
import re
from skillvitals.metrics import trigger_metrics, efficacy_metrics


def _trigger_terms(skill):
    quoted = re.findall(r'"([^"]+)"', skill.description)
    name_words = [w for w in skill.name.replace("-", " ").split() if len(w) > 3]
    return [t.lower() for t in quoted] + [w.lower() for w in name_words]


def heuristic_trigger(skill, prompt: str) -> bool:
    """Zero-cost, deterministic trigger baseline: fires if the prompt contains a
    quoted trigger phrase from the description or a word from the skill name."""
    p = prompt.lower()
    return any(term and term in p for term in _trigger_terms(skill))


def run_trigger(skill, cases, trigger_fn):
    results = [{"should_fire": bool(c["should_fire"]), "fired": bool(trigger_fn(skill, c["prompt"]))}
               for c in cases]
    return trigger_metrics(results), results


def run_efficacy(skill, tasks, task_fn, judge_fn):
    pairs = []
    for t in tasks:
        base = task_fn(t["prompt"], None)
        withs = task_fn(t["prompt"], skill.body)
        pairs.append({"without": judge_fn(t["prompt"], base), "with": judge_fn(t["prompt"], withs)})
    return efficacy_metrics(pairs), pairs
