from __future__ import annotations
import argparse
import json
import pathlib
import sys
from skillvitals.skill import parse_skill
from skillvitals.run import run_trigger, run_efficacy, heuristic_trigger
from skillvitals.report import render_human, render_json


def _load_yaml(path):
    import yaml
    return yaml.safe_load(pathlib.Path(path).read_text())


def _skill(args):
    return parse_skill(pathlib.Path(args.skill).read_text())


def _trigger_fn(args):
    if args.model:
        from skillvitals.llm import OpenAIModel, make_trigger_fn
        return make_trigger_fn(OpenAIModel(args.model, args.base_url))
    return heuristic_trigger


def _cmd_trigger(args) -> int:
    skill = _skill(args)
    cases = _load_yaml(args.cases)["cases"]
    metrics, _ = run_trigger(skill, cases, _trigger_fn(args))
    print(render_json(trigger=metrics) if args.json else render_human(trigger=metrics))
    if args.min_recall is not None and metrics["recall"] < args.min_recall:
        print(f"FAIL: recall {metrics['recall']:.0%} below --min-recall {args.min_recall:.0%}", file=sys.stderr)
        return 1
    return 0


def _cmd_efficacy(args) -> int:
    from skillvitals.llm import OpenAIModel, make_task_fn, make_judge_fn
    if not args.model:
        print("efficacy needs --model (it runs the task with and without the skill)", file=sys.stderr)
        return 2
    skill = _skill(args)
    tasks = _load_yaml(args.tasks)["tasks"]
    m = OpenAIModel(args.model, args.base_url)
    metrics, _ = run_efficacy(skill, tasks, make_task_fn(m), make_judge_fn(m))
    print(render_json(efficacy=metrics) if args.json else render_human(efficacy=metrics))
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="skillvitals", description="Vital signs for your agent skills.")
    sub = p.add_subparsers(dest="cmd", required=True)

    t = sub.add_parser("trigger", help="does the skill fire when it should?")
    t.add_argument("skill")
    t.add_argument("--cases", required=True, help="yaml with a 'cases' list of {prompt, should_fire}")
    t.add_argument("--model", help="OpenAI-compatible model id (omit for the zero-cost heuristic)")
    t.add_argument("--base-url", help="OpenAI-compatible base url (for local/cheap models)")
    t.add_argument("--json", action="store_true")
    t.add_argument("--min-recall", type=float, help="exit non-zero if recall falls below this (CI gate)")

    e = sub.add_parser("efficacy", help="does the skill actually help? (needs a model)")
    e.add_argument("skill")
    e.add_argument("--tasks", required=True, help="yaml with a 'tasks' list of {prompt}")
    e.add_argument("--model", help="OpenAI-compatible model id")
    e.add_argument("--base-url")
    e.add_argument("--json", action="store_true")

    args = p.parse_args(argv)
    return _cmd_trigger(args) if args.cmd == "trigger" else _cmd_efficacy(args)


if __name__ == "__main__":
    sys.exit(main())
