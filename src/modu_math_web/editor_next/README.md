# ModuMath Editor Konva

This folder contains the React + TypeScript Konva editor used by `/editor-konva/`.
It also contains the teacher/admin learning workspace served by Django at `/teacher/`.
The legacy Django `modu_math_web.editor` app remains available for its editor API endpoints.

## 문제 및 정답 편집

오른쪽 패널의 **정답** 탭을 누르면 편집 화면에서 응답 방식과 정답을 바로 작성할 수 있습니다.
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
npm run build:student
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

## Student app preview

**앱처럼 풀어보기** opens the same student application as `localhost:3000`.
There is one Flutter entry (`apps/mobile/lib/main.dart`) and one deployed bundle
(`static/editor_next/student_app/`). Practice and editor preview share
`StudentProblemBody`, `StudentProblemCanvas`, and `AssignmentAnswerInput`.
The host loads the saved student presentation and grades with the same backend
checker through `/api/editor/problems/<id>/student-preview/`. Preview grading
never creates attempts. Save and build before previewing the latest edits.

Build with `npm run build` and `npm run build:student`. The former development
studio, Flutter layout editing, and separate Flutter editor build are removed.
Run `npm run test:editor-preview` against a static server on port 5189 for the
isolated browser test, or set `MODU_EDITOR_TEST_URL` to its editor bundle URL.
With the local apps running on ports 8000 and 3000, `npm run test:editor-parity`
checks that both serve identical Flutter JavaScript and verifies the highlighted
multiplication example and its answer choices against the real preview API.

`npm run test:answer-capacity` verifies typing `1124`, pasting a longer value,
and grading the saved `P3_1_01_00040_00472` problem. A single box bound to a full
answer uses a uniform 64-character capacity independent of the secret answer.
Explicit `digit` cells always retain their one-digit capacity, including cells
bound to separate fields. Multiple cells bound to one field keep their capacities.
The app applies the same rule to older assignment snapshots. Box width and
automatic font size do not determine input capacity.

`npm run test:carry-input` verifies sequential carry/result input, replacement,
and wrong/correct grading for `P3_1_01_00040_02135`. Explicit answer references
take precedence when mapping fields; a complete unique authored order resolves
legacy copied slot IDs. Numeric glyphs must fit inside the padded cell even when
the authored minimum font size is larger than the available space.
