# Agent Rules (Project)

## Encoding

- Always read/write source files as UTF-8.
- For Korean text, use direct Korean literals.
- Do not introduce unicode escapes like `\uXXXX` or `\xNN` in source files unless explicitly requested.

## Commit Safety

- Respect pre-commit checks configured in `.githooks/pre-commit`.
- Do not bypass checks with `--no-verify` except emergency cases documented in `README.md`.

## Editing Principle

- Prefer minimal, targeted edits.
- Do not rewrite working DSL build code when only comments/docs are requested.
