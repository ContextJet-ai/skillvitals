<div align="center">

# skillvitals

**Vital signs for your agent skills. Does it fire when it should, and does it actually help? Measure both, on a cheap model.**

[![tests](https://github.com/ContextJet-ai/skillvitals/actions/workflows/tests.yml/badge.svg)](https://github.com/ContextJet-ai/skillvitals/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)
[![by ContextJet.ai](https://img.shields.io/badge/by-ContextJet.ai-1f6feb)](https://www.contextjetai.com)

</div>

> [!NOTE]
> Agent skills are usually shipped on faith. Two things actually decide whether one works: does its description make the model **trigger** it on the right requests, and once triggered, does it **help** the output. skillvitals measures both, so validating a skill stops being an org-only, big-budget exercise.

## Install

```bash
uv tool install git+https://github.com/ContextJet-ai/skillvitals
# or: pipx install git+https://github.com/ContextJet-ai/skillvitals
```

## 60-second start

Test whether a skill triggers correctly. No API key needed, this uses a zero-cost heuristic:

```bash
skillvitals trigger ./SKILL.md --cases cases.yaml
```

```text
skill vitals

trigger:
  fires when it should (recall):     92%
  false-fires when it shouldn't:     8%
  f1:                                0.91  (25 cases)
```

`cases.yaml` is just labeled prompts:

```yaml
cases:
  - prompt: "help me add evals to my chatbot"
    should_fire: true
  - prompt: "what is the weather today"
    should_fire: false
```

## The two things it measures

**Triggering.** Does the skill's description make a model activate it on prompts that should, and stay quiet on the ones that shouldn't. You get recall, false-fire rate, and F1. This is the cheap axis, so it runs on the free heuristic or any small model.

```bash
skillvitals trigger ./SKILL.md --cases cases.yaml --model gpt-4o-mini
# or a local model:
skillvitals trigger ./SKILL.md --cases cases.yaml --model llama3 --base-url http://localhost:11434/v1
```

**Efficacy.** Does using the skill actually improve the answer. skillvitals runs each task twice, once with the skill and once without, and has a judge score both, then reports the win rate and average delta.

```bash
skillvitals efficacy ./SKILL.md --tasks tasks.yaml --model gpt-4o-mini
```

```text
efficacy (with skill vs without):
  win rate:   78%
  avg delta:  +1.60  (20 tasks)
```

## Works with any model

Point `--model` and `--base-url` at anything OpenAI-compatible: OpenAI, Together, Groq, or a local model via Ollama or LM Studio. The whole idea is that validating a skill should cost cents, not a research budget.

## Why this exists

If you write agent skills, you are guessing at two things: whether the model reliably picks up your skill, and whether it changes the output for the better. This turns both guesses into numbers you can run in CI, on a model you can afford.

Built by [ContextJet.ai](https://www.contextjetai.com). Part of the vitals family alongside [mcpvitals](https://github.com/ContextJet-ai/mcpvitals). MIT licensed.
