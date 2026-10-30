# ModuMath Editor Konva

This folder contains the React + TypeScript Konva editor used by `/editor-konva/`.
It also contains the teacher/admin learning workspace served by Django at `/teacher/`.
The legacy Django `modu_math_web.editor` app remains available for its editor API endpoints.

## Commands

From `src/modu_math_web/editor_next`:

```bash
npm install
npm run typecheck
npm run build
npm run build:flutter-editor
```

The teacher workspace uses the existing Django `/api/v1/` endpoints on the same
origin. Build with `npm run build`, start Django, then visit `/teacher/`.
Register/create a Django account and grant the teacher role with
`python manage.py set_teacher <username>` from the repository root, or use an
existing administrator account. Tests never create these accounts in your DB.

```bash
npm run test:teacher
npm run test:teacher-browser
```

The browser test requires the repository Python environment and Chrome or
Playwright Chromium. It builds a disposable SQLite fixture and starts its own
server. Set `MODU_TEST_PYTHON` or `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH` to override
the default executables. Screenshots go to ignored `.tmp/teacher-browser/`.
Build the bundles before running the browser test.

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

## Flutter editing surface

The primary canvas is the real Flutter renderer. It sends platform-neutral
layout patches (`target`, `op`, and `value`) to the React host, where the
existing save/build flow persists them as editor overrides. Rebuild the
embedded Flutter bundle with `npm run build:flutter-editor` after changing
files under `apps/mobile/lib`. Konva remains available as an advanced fallback.
