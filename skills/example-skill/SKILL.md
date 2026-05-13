---
name: example-skill
description: Use this starter skill as a template when creating a new personal Codex skill. Trigger when the user wants a minimal example of skill structure, metadata, references, scripts, or assets.
---

# Example Skill

Use this skill as a compact template for personal Codex skills.

## Workflow

1. Read the user request and confirm this skill's scope applies.
2. Load only the specific reference file needed for the task.
3. Prefer scripts for repeatable or fragile operations.
4. Keep generated output focused on the user's requested artifact.

## Resource Guide

- `references/`: Put detailed domain notes or API references here.
- `scripts/`: Put deterministic helpers here.
- `assets/`: Put templates, images, or reusable source files here.

## Quality Bar

- Keep `SKILL.md` concise.
- Avoid duplicating content between `SKILL.md` and references.
- Include only files that directly help Codex perform the skill.
