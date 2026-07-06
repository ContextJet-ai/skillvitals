"""Real model layer. Builds injectable callables from any OpenAI-compatible endpoint.
Imported lazily so the pure core has no hard openai dependency."""
from __future__ import annotations
import os


class OpenAIModel:
    def __init__(self, model: str, base_url: str | None = None, api_key: str | None = None):
        from openai import OpenAI
        self.model = model
        self.client = OpenAI(base_url=base_url or os.getenv("OPENAI_BASE_URL"),
                             api_key=api_key or os.getenv("OPENAI_API_KEY", "sk-none"))

    def complete(self, system: str, user: str) -> str:
        r = self.client.chat.completions.create(
            model=self.model, temperature=0,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}])
        return r.choices[0].message.content or ""


def make_trigger_fn(model: OpenAIModel):
    def fn(skill, prompt: str) -> bool:
        sys = ("You decide whether a skill should activate for a user request. "
               "Answer with exactly 'yes' or 'no'.")
        user = f"Skill name: {skill.name}\nSkill description: {skill.description}\n\nUser request: {prompt}\n\nShould this skill activate?"
        return model.complete(sys, user).strip().lower().startswith("y")
    return fn


def make_task_fn(model: OpenAIModel):
    def fn(prompt: str, skill_body):
        sys = "You are a helpful assistant."
        if skill_body:
            sys += "\n\nApply this skill if relevant:\n" + skill_body
        return model.complete(sys, prompt)
    return fn


def make_judge_fn(model: OpenAIModel):
    def fn(task: str, output: str) -> float:
        sys = "Score the response to the task from 0 to 10 for how well it accomplishes it. Reply with only the number."
        raw = model.complete(sys, f"Task: {task}\n\nResponse: {output}\n\nScore (0-10):")
        try:
            return float(raw.strip().split()[0])
        except (ValueError, IndexError):
            return 0.0
    return fn
