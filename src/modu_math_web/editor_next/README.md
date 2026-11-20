# ModuMath Editor Konva

This folder contains the React + TypeScript Konva editor used by `/editor-konva/`.
It also contains the teacher/admin learning workspace served by Django at `/teacher/`.
The legacy Django `modu_math_web.editor` app remains available for its editor API endpoints.

## 문제 및 정답 편집

상단의 **정답 설정**을 누르면 편집 화면에서 응답 방식과 정답을 바로 작성할 수 있습니다.
단답형은 정답과 단위를 나누어 입력하고, 여러 답은 **정답 추가**로 늘립니다.
문제 안에 입력칸이 필요하면 **문제 속 빈칸 채우기**를 선택한 뒤 **문제에 정답 빈칸 추가**를 누릅니다.
빈칸과 정답 항목이 자동으로 연결되며, 캔버스에서 위치와 크기를 조절할 수 있습니다.
**정답 저장하고 화면 반영**으로 저장한 뒤 **정답 검수**에서 학생처럼 풀어봅니다.
기존 도구는 **기본 요소**, **수학 교구**, **정답 및 파일**에 모두 있습니다.

Vite 실행 후 `npm run test:editor-browser`로 도구 접근, 정답 작성, 빈칸 연결,
JSON, 힌트, 검수, 화면 크기별 배치를 확인합니다. 실제 문제 파일을 변경하지 않으며
스크린샷은 `.tmp/editor-workspace/`에 저장됩니다.

## 개발 명령

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

The toolbar's **앱처럼 풀어보기** button opens the saved problem in a Flutter
dialog. Unsaved Konva edits stay in the editor and are restored on return.
Use **저장하고 화면 반영** before opening it to try the latest edits. The host
loads the saved semantic, solvable, layout, and renderer together; this preview
does not load a fallback catalog or persist practice attempts. Build both the
React bundle and Flutter editor bundle before serving this feature.

After serving this folder on port 5189, run
`node scripts/editor-student-preview.browser.mjs` to check the real iframe,
answer input, preserved draft, and load failure/retry without changing problems.

Konva remains the editing canvas. The existing Flutter bridge also supports
platform-neutral layout patches (`target`, `op`, and `value`), but the student
preview runs in a fixed solve mode and does not apply editing patches. Rebuild
the embedded Flutter bundle with `npm run build:flutter-editor` after changing
files under `apps/mobile/lib`.
