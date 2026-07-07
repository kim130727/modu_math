# ModuMath editor_next tldraw MVP

This folder contains an experimental React + TypeScript + tldraw editor for math problem objects.

It does not replace the existing Django `editor` app or the current `/editor-next/` Solid editor.
It is available separately at:

```text
/editor-next/tldraw/
```

## Commands

From `src/modu_math_web/editor_next`:

```bash
npm install
npm run typecheck
npm run build
```

For local Vite development:

```bash
npm run dev
```

## Data Model

The source of truth is canonical problem JSON in `src/types/problem.ts`.
tldraw is used only as an editing UI engine.

Current flow:

```text
sample_problem.json
-> canonical ProblemJson
-> tldraw shapes
-> user edits
-> canonical ProblemJson
-> console output on Save JSON
```

## MVP Features

- Load `samples/sample_problem.json`.
- Show the sample on a tldraw canvas.
- Add and move math text.
- Edit selected `MathTextShape` text/latex via a prompt.
- Add basic rectangle and circle shapes.
- Add custom math shapes:
  - `MathTextShape`
  - `FractionBarShape`
  - `NumberLineShape`
  - `GroupObjectsShape`
- Convert current tldraw page back to canonical problem JSON.
- Show canonical JSON in the debug panel.
- Print canonical JSON to the console with Save JSON.

## TODO

- Replace prompt-based MathText editing with a dedicated math input panel.
- Render `MathTextShape.props.latex` with KaTeX or MathJax.
- Add canonical image object import/export through tldraw assets.
- Add automatic JSON refresh via tldraw store listeners.
- Add Python DSL -> canonical problem JSON conversion endpoint.
- Add canonical problem JSON -> Python DSL conversion endpoint.
- Add canonical problem JSON -> SVG/PNG/Flutter asset export.
- Add robust persistence API instead of console-only Save JSON.

## Next Python Integration Files

Suggested next files:

```text
src/modu_math_web/editor_next/services/problem_json.py
src/modu_math_web/editor_next/api.py
tests/web/test_editor_next_problem_json.py
```

These should host the Python DSL <-> canonical problem JSON adapters and HTTP endpoints.
