# Codex Skills

Personal Codex skill repository for reusable workflows, domain instructions, scripts, references, and assets.

## Layout

```text
skills/
  example-skill/
    SKILL.md
    agents/openai.yaml
    references/
    scripts/
    assets/
```

Each skill is a self-contained directory. `SKILL.md` is required; bundled resources are optional and should only be added when they directly support the skill.

## Add A Skill

1. Copy `skills/example-skill` to `skills/<your-skill-name>`.
2. Update `SKILL.md` frontmatter:
   - `name`: stable machine-readable skill name.
   - `description`: clear trigger conditions for when Codex should use the skill.
3. Keep the main instructions concise. Put detailed docs in `references/`, deterministic helpers in `scripts/`, and reusable files in `assets/`.
4. Update `agents/openai.yaml` so the skill list has useful display text.

## Skills

- `api-import-doc-writer`: Generate import-ready API reference docs from source handlers and route code.
- `netease-lyrics-vocab`: Build vocabulary study tables from NetEase Cloud Music playlist lyrics.
- `example-skill`: Minimal starter template for future skills.

## Install Locally

From another machine or Codex environment:

```bash
npx skills install github:Honeylemonade/codex-skills
```

For a single skill path, use:

```bash
npx skills install github:Honeylemonade/codex-skills/tree/main/skills/example-skill
```
