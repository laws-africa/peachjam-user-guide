# AGENTS.md

Guidance for coding/documentation agents working in this repository.

## What This Repository Is

This repo stores GitBook user documentation for Peachjam-based legal information sites.

- Source guides (authoritative): `eng/` and `fra/`
- Generated site variants: `ghalii-eng/`, `kenyalaw-eng/`, `lawlibrary-eng/`, `seylii-eng/`, `tanzlii-eng/`, `ulii-eng/`
- Build config: `peachjam.json` (currently configured for `eng` outputs only)
- Build script: `bin/build.py`
- CI workflow: `.github/workflows/build.yml`

## Golden Rules

- Treat `eng/` and `fra/` as source of truth.
- Never change files in generated variant folders.
- Expect generated folders to be overwritten by `bin/build.py` and by CI.
- Keep changes minimal and targeted; avoid repo-wide formatting churn.

## Documentation Audience and Writing Goals

Write documentation for non-technical legal researchers first.

- Primary persona 1: judges and magistrates doing legal research, often cautious with technology and unlikely to experiment.
- Primary persona 2: students and junior legal practitioners who are more comfortable exploring, but still need clear guidance on capability and process.
- Optimise for confidence: write predictable, explicit steps that reduce uncertainty.
- Explain capability: show what users can do and why it is useful for legal research.

## Tone, Voice, and Language

- Tone: friendly, semi-formal, direct, and simple.
- Use plain language and short sentences.
- Use active voice and action-led instructions.
- Use UK English spelling and conventions consistently.
- Avoid vague/promotional phrasing; prefer concrete outcomes and user benefit.

## Page Openings (Problem-First)

At the start of each page, explain:

- the user problem,
- how the feature solves it, and
- why it matters in legal research.

Do not begin with technical detail alone.

## Procedure Writing Standards

- Use numbered steps for task procedures.
- Keep one clear action per step.
- Keep step sequences short. If a procedure is long, split it into smaller logical sections.
- For complex tasks, guide users with screenshots as they progress.
- For important docs, include video where available.
- Use exact UI labels as shown in the product.

## Troubleshooting Guidance

- Include troubleshooting only when there are known failure points or common user confusion.
- Do not add a troubleshooting section by default if there are no known issues.

## Accessibility and Media

- Add meaningful `alt` text for instructional screenshots.
- Avoid empty `alt=""` for screenshots that carry instructional context.
- Keep screenshot references aligned to the step they support.

## Terminology and Consistency

- Keep terminology consistent across pages.
- Prefer canonical wording for repeated concepts and controls.
- Use consistent casing for feature names and navigation labels.

## File Change Policy (Strict)

- Only change source files (code and docs), such as:
- `eng/**`
- `fra/**`
- `bin/**`
- `_site-images/**`
- `.github/workflows/**`
- `peachjam.json`
- `requirements.txt`
- `README.md`
- Never edit generated directories:
- `ghalii-eng/**`
- `kenyalaw-eng/**`
- `lawlibrary-eng/**`
- `seylii-eng/**`
- `tanzlii-eng/**`
- `ulii-eng/**`
- If a task appears to require edits in generated directories, make the equivalent change in source files and regenerate outputs via build/CI.

## How Variants Are Built

1. GitHub Actions runs on push to `main`.
2. Workflow installs Python 3.10 and `requirements.txt` dependencies.
3. It runs `python bin/build.py`.
4. The workflow commits generated changes with message `Update site variants [nobuild]`.
5. Commits containing `nobuild` are skipped to avoid recursive CI runs.

## Local Build Commands

- Install deps: `pip install -r requirements.txt`
- Build variants: `python bin/build.py`

Run the build after changing source docs, template logic, site config, or shared assets.

## Template Syntax (Jinja with Custom Delimiters)

Markdown source files may contain Jinja templates rendered by `bin/build.py`:

- Variables: `%%VARIABLE%%` (example: `%%APPNAME%%`)
- Control blocks: `(% if ... %) ... (% endif %)`

Important: use these delimiters, not default Jinja `{{ }}` and `{% %}`.

## Available Template Context

From `peachjam.json` and build logic:

- `APPNAME`
- `APPURL`
- `languages`
- `APPCODE` (auto-derived if not set)
- `LANG`

If you add new template variables, ensure they are present in every relevant site config.

## Assets and Image Localisation

Assets live under each source language at `.gitbook/assets`.

Build behavior:

- Markdown image `src` paths to `.gitbook/assets/...` are rewritten to site-prefixed names like `lawlibrary--file.png`.
- Site-specific overrides are sourced from `_site-images/<appcode>/<lang>/`.
- If no override exists, the default `<lang>/.gitbook/assets/<file>` is used.
- The build copies assets into generated variant folders as prefixed names.

When localising screenshots for a specific site, place overrides in `_site-images/<appcode>/<lang>/`.

## Safe Editing Workflow for Agents

1. Confirm task scope (source docs vs generated output).
2. Edit only source files (`eng/`, `fra/`, `peachjam.json`, `bin/build.py`, workflow/config files) as needed.
3. Run `python bin/build.py` when output should change.
4. Check diffs for unintended broad changes.
5. Summarise exactly what changed and why.

## CI/Commit Notes

- CI is configured to auto-commit generated variant updates on `main`.
- If preparing commits manually and you intentionally include generated refreshes, use clear commit messaging.
- Do not remove the `[nobuild]` mechanism unless CI recursion handling is replaced.

## When Unsure

Default to preserving current generation behavior and ask before introducing structural changes to:

- variant folder naming
- template delimiters
- workflow trigger/auto-commit behavior
- asset rewrite rules

For documentation decisions, default to:

- user confidence over completeness,
- clarity over brevity, and
- `eng/` as source of truth with `fra/` catching up through translation.
