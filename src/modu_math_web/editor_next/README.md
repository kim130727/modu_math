# ModuMath Editor Konva

This folder contains the React + TypeScript Konva editor used by `/editor-konva/`.
The legacy Django `modu_math_web.editor` app remains available for its editor API endpoints.

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

## Output

The production bundle is written to:

```text
static/editor_next/konva_assets/
```

The Django template loads that bundle from:

```text
/editor-konva/
```
