# SolidJS Editor Parity Matrix

Date: 2026-07-02

Status meanings:

- `Baseline`: Existing editor behavior identified and covered by audit and/or existing tests.
- `Planned`: SolidJS work not implemented yet.
- `Blocked`: Needs implementation or further verification.
- `Pass`: Test/check passed.
- `Not run`: Not executed for SolidJS because Phase 1+ has not been implemented.

Existing test baseline:

```text
uv run pytest -> 110 passed, 1 warning
uv run pytest tests\web\test_editor_api.py -> 46 passed, 1 warning

After Phase 1:
uv run pytest -> 111 passed, 1 warning
uv run pytest tests\web\test_editor_api.py -> 47 passed, 1 warning
npm run typecheck -> passed
npm run build -> passed

After Phase 2 selection, pan, and handle foundation:
uv run pytest -q -> 111 passed, 1 warning
uv run pytest tests\web\test_editor_api.py -q -> 47 passed, 1 warning
npm run typecheck -> passed
npm run build -> passed

After Phase 3 drag, keyboard-move, deletion, inspector-edit, basic resize, insertion, color-edit, and snap foundation:
uv run pytest -q -> 111 passed, 1 warning
uv run pytest tests\web\test_editor_api.py -q -> 47 passed, 1 warning
npm run typecheck -> passed
npm run build -> passed

After Phase 4 undo/redo foundation:
uv run pytest -q -> 111 passed, 1 warning
uv run pytest tests\web\test_editor_api.py -q -> 47 passed, 1 warning
npm run typecheck -> passed
npm run build -> passed

After Phase 5/6 DSL save, format, build, and manual patch foundation:
uv run pytest -q -> 111 passed, 1 warning
uv run pytest tests\web\test_editor_api.py -q -> 47 passed, 1 warning
npm run typecheck -> passed
npm run build -> passed
```

| ID | Feature | Existing Editor | SolidJS | Auto Test | Manual Test | Status |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| F001 | Editor page load at `/editor/`; separate `/editor-next/` page | Yes | Implemented Phase 1 | Existing and next route pass | Not run | Phase 1 implemented |
| F002 | Static CSS/JS asset loading | Yes | Implemented separate Solid assets | Existing and next static pass | Not run | Phase 1 implemented |
| F003 | Problem list loading | Yes | Implemented Phase 1 | Existing pass; Solid build pass | Not run | Phase 1 implemented |
| F004 | Problem tree filtering | Yes | Implemented simple filter | Solid build pass | Not run | Phase 1 implemented |
| F005 | Folder collapse/expand | Yes | Planned Phase 1+ | Not run | Not run | Planned |
| F006 | Problem selection/open | Yes | Implemented Phase 1 | Existing pass; Solid build pass | Not run | Phase 1 implemented |
| F007 | Path traversal rejection | Yes | Reuse server | Existing pass | Not run | Baseline |
| F008 | Artifact display | Yes | Implemented Phase 1 read-only | Existing partial pass; Solid build pass | Not run | Phase 1 implemented |
| F009 | SVG image asset rewrite | Yes | Reuse server | Existing pass | Not run | Baseline |
| F010 | DSL text editing/save | Yes | Implemented editable DSL draft, dirty state, Save button, and Ctrl/Cmd+S through existing `/dsl/` endpoint | Existing pass; Solid build/typecheck pass | Not run | Partial Phase 5 |
| F011 | DSL format | Yes | Implemented Format button that saves first, then calls existing `/dsl/format/` endpoint | Existing pass; Solid build/typecheck pass | Not run | Partial Phase 5 |
| F012 | Build | Yes | Implemented Build button through existing `/build/` endpoint; returned artifacts refresh Solid document/SVG | Existing pass; Solid build/typecheck pass | Not run | Partial Phase 6 |
| F013 | Build failure reporting | Yes | Implemented status/error state plus build stdout/stderr/error display when returned by the server | Existing partial pass; Solid build/typecheck pass | Not run | Partial Phase 6 |
| F014 | Manual layout patch | Yes | Implemented manual slot-id + JSON update patch form through existing `/layout-patch/` endpoint | Existing pass; Solid build/typecheck pass | Not run | Partial Phase 5 |
| F015 | Patch + build | Yes | Implemented manual patch Build action through existing `/layout-patch-and-build/` endpoint | Existing pass; Solid build/typecheck pass | Not run | Partial Phase 5/6 |
| F016 | Single selection | Yes | Implemented for slot strip and SVG element clicks using server SVG element IDs | Solid build/typecheck pass | Not run | Partial Phase 2 |
| F017 | Multi-selection | Yes | Implemented for Shift/Ctrl/Cmd click in slot strip and SVG element clicks | Solid build/typecheck pass | Not run | Partial Phase 2 |
| F018 | Marquee selection | Yes | Implemented for layout-bounds selection from empty-canvas drag | Solid build/typecheck pass | Not run | Partial Phase 2 |
| F019 | Selection clear | Yes | Implemented for empty SVG/canvas click | Solid build/typecheck pass | Not run | Partial Phase 2 |
| F020 | Pick modes | Yes | Basic `all`/`text`/`shape`/`linepath` filters implemented for SVG click and marquee selection | Solid build/typecheck pass | Not run | Partial Phase 2 |
| F021 | SVG hit proxies | Yes | Planned Phase 2 | Existing static symbol check only | Not run | Planned |
| F022 | Drag move | Yes | Implemented basic selected-slot drag using existing `move_dx`/`move_dy` patch-and-build endpoint | Existing server patch pass; Solid build/typecheck pass | Not run | Partial Phase 3 |
| F023 | Drag throttling/local preview | Yes | Overlay-only local drag preview; one server patch/build on pointerup | Solid build/typecheck pass | Not run | Partial Phase 3 |
| F024 | Keyboard move | Yes | Implemented Arrow key movement with Shift+Arrow 10px coarse movement through existing patch-and-build endpoint | Solid build/typecheck pass | Not run | Partial Phase 3 |
| F025 | Snap toggle 5px | Yes | Implemented toolbar toggle for drag delta and resize handle snapping | Solid build/typecheck pass | Not run | Partial Phase 3 |
| F026 | Resize handles | Yes | Implemented basic single-slot resize for `rect`, `text_box`, `image`, and `circle`; other resize modes pending | Existing server patch pass; Solid build/typecheck pass | Not run | Partial Phase 3 |
| F027 | Line endpoint edit | Yes | Planned Phase 3 | Existing server patch pass | Not run | Planned |
| F028 | Line/slot rotation | Yes | Planned Phase 3 | Existing server patch pass | Not run | Planned |
| F029 | Path point editing | Yes | Planned Phase 3 | Existing static symbol check | Not run | Planned |
| F030 | Polygon/path transforms | Yes | Planned Phase 3 | Existing static symbol check | Not run | Planned |
| F031 | Canvas selection/resize | Yes | Planned Phase 3 | Existing pass | Not run | Planned |
| F032 | Property inspector coordinate edit | Yes | Implemented primitive number/string field editing from selected slot layout content | Existing server patch pass; Solid build/typecheck pass | Not run | Partial Phase 3 |
| F033 | Text inspector edit | Yes | Implemented text/string field editing through the same inspector primitive editor | Existing server patch pass; Solid build/typecheck pass | Not run | Partial Phase 3 |
| F034 | Inline text edit | Yes | Planned Phase 3 | Existing static asset check only | Not run | Planned |
| F035 | Font size controls | Yes | Planned Phase 3 | Existing server patch pass | Not run | Planned |
| F036 | Text alignment | Yes | Planned Phase 3 | Not run | Not run | Planned |
| F037 | Shape insertion gallery | Yes | Implemented toolbar rectangle insertion only; full gallery/draw modes pending | Existing add patch pass; Solid build/typecheck pass | Not run | Partial Phase 3 |
| F038 | Text box insertion | Yes | Implemented toolbar text box insertion through existing add patch/build endpoint | Existing add patch pass; Solid build/typecheck pass | Not run | Partial Phase 3 |
| F039 | Image insertion | Yes | Planned Phase 3 | Existing add patch pass | Not run | Planned |
| F040 | Table insertion | Yes | Planned Phase 3 | Existing pass | Not run | Planned |
| F041 | Graph paper insertion | Yes | Planned Phase 3 | Existing pass | Not run | Planned |
| F042 | Bar model insertion | Yes | Planned Phase 3 | Existing server helpers pass | Not run | Planned |
| F043 | Tick bar insertion | Yes | Planned Phase 3 | Existing server helpers pass | Not run | Planned |
| F044 | Fraction/mixed fraction insertion | Yes | Planned Phase 3 | Existing fraction patch pass | Not run | Planned |
| F045 | Shape fill/stroke/dash formatting | Yes | Implemented inspector hex color swatches for `fill`/`stroke`; dash/no-border presets pending | Existing server patch pass; Solid build/typecheck pass | Not run | Partial Phase 3 |
| F046 | Delete selection | Yes | Implemented Delete/Backspace selected-slot removal through existing patch-and-build endpoint | Existing pass; Solid build/typecheck pass | Not run | Partial Phase 3 |
| F047 | Copy/paste selected slots | Yes | Planned Phase 3/4 | Existing add copied slot pass | Not run | Planned |
| F048 | Undo | Yes | Implemented for Solid patch-backed drag, keyboard move, resize, property/color edit, insertion, and deletion | Solid build/typecheck pass | Not run | Partial Phase 4 |
| F049 | Redo | Yes | Implemented for the same patch-backed operations, including Ctrl/Cmd+Y and Ctrl/Cmd+Shift+Z | Solid build/typecheck pass | Not run | Partial Phase 4 |
| F050 | History cap/reset | Yes | Implemented 100-entry undo cap, redo clear on new edit, and history reset on problem switch | Solid build/typecheck pass | Not run | Partial Phase 4 |
| F051 | Alignment | Yes | Planned Phase 3/4 | Not run | Not run | Planned |
| F052 | Layer ordering | Yes | Planned Phase 3/4 | Existing override path partial | Not run | Planned |
| F053 | Table cell selection | Yes | Planned Phase 3 | Not run | Not run | Planned |
| F054 | Table divider adjustment | Yes | Planned Phase 3 | Existing server patch partial | Not run | Planned |
| F055 | Generated/helper group movement | Yes | Planned Phase 3 | Existing pass | Not run | Planned |
| F056 | Generated slot override fallback | Yes | Reuse server | Existing pass | Not run | Baseline |
| F057 | Editor override delete/layer state | Yes | Reuse server | Existing pass | Not run | Baseline |
| F058 | Supported slot field validation | Yes | Reuse server | Existing pass | Not run | Baseline |
| F059 | Import insertion for added slots | Yes | Reuse server | Existing pass | Not run | Baseline |
| F060 | Semantic/solvable preservation on build | Yes | Reuse server | Existing pass | Not run | Baseline |
| F061 | Local image href inlining on build | Yes | Reuse server | Existing partial pass | Not run | Baseline |
| F062 | Error category/status messaging | Yes | Implemented Phase 1 loading/error status | Existing partial pass; Solid build pass | Not run | Phase 1 implemented |
| F063 | DSL/artifact slot ID caches | Yes | Planned typed equivalent | Not run | Not run | Planned |

## Phase 2 Progress Notes

Implemented after Phase 1:

- SVG click selection now delegates from the server-rendered SVG and maps element IDs such as `slot.q.text` back to layout slot IDs.
- Shift/Ctrl/Cmd click toggles multi-selection in both the SVG and slot strip.
- Empty SVG/canvas click clears selection.
- A read-only selection bounding box is drawn from layout slot bounds.
- Basic zoom controls were added to the canvas surface. This is a Solid-only convenience foundation; the audit found no complete existing user-facing zoom/pan implementation to match yet.
- Empty-canvas drag creates a marquee rectangle and selects slots whose layout bounds intersect it.
- Pan tool, Alt-drag, and middle-button drag update the viewport pan state locally.
- Type-restricted pick filters (`all`, `text`, `shape`, `linepath`) apply to SVG click selection and marquee selection.
- Display-only resize handles are drawn around the selected bounding box.

Still pending for Phase 2 parity:

- Resize handle interaction.
- Hit proxy parity for thin lines/text.
- Transform-aware/path-aware selection bounds.

## Phase 3 Progress Notes

Implemented after Phase 2:

- Solid API adapter now posts layout patches to the existing `/api/editor/problems/{id}/layout-patch-and-build/` endpoint.
- Solid HTTP requests now include CSRF and JSON content-type headers for POST requests.
- Server SVG is rendered inline after sanitization so element IDs remain part of the editable canvas surface.
- Selected slot drag starts from SVG element hit testing or layout-bound fallback hit testing.
- Multi-selected slots are moved together by sending one `move_dx`/`move_dy` update patch per selected slot.
- Pointermove updates only local overlay state; pointerup commits a single server request and refreshes returned artifacts.
- Snap 5px toolbar toggle applies to drag preview/commit and resize preview/commit.
- Arrow keys move selected slots by 1px; Shift+Arrow moves selected slots by 10px. Input, textarea, select, and contenteditable targets are ignored.
- Delete and Backspace remove selected slots through the existing `delete` patch path, then clear Solid selection after a successful response.
- Inspector number and string fields commit update patches on blur or Enter. Complex fields such as polygon `points` remain display-only.
- Inspector `fill` and `stroke` fields show color swatches when the value is a six-digit hex color.
- Resize handles now preview and commit basic single-slot resize for bbox-based slots and circles.
- Toolbar buttons insert basic text boxes and rectangles into the preferred diagram/absolute layout region, then select the new slot.

Still pending for Phase 3 parity:

- Underlying SVG element preview movement during drag.
- Snap parity for keyboard movement and future drawing/insertion flows.
- Multi-selection resize, line endpoint resize, path point editing, polygon/path scaling, and transform-aware resize.
- Full shape gallery, drag-to-draw placement, image upload, helper insertions, dash/no-border presets, and non-hex color controls.

## Phase 4 Progress Notes

Implemented after Phase 3:

- Added a typed history manager with undo and redo stacks capped at 100 entries.
- Solid editing actions now record patch-backed history entries for drag move, keyboard move, single-slot resize, primitive inspector edits, hex fill/stroke changes, basic insertion, and deletion.
- Undo applies the stored inverse patch list through the existing `/layout-patch-and-build/` endpoint; redo applies the original patch list through the same endpoint.
- New edits clear the redo stack, and switching problems resets both stacks.
- Toolbar buttons and keyboard shortcuts were added for Undo/Redo: Ctrl/Cmd+Z, Ctrl/Cmd+Shift+Z, and Ctrl/Cmd+Y.
- The status bar now exposes undo/redo stack counts for manual verification.

Current intentional limits:

- History entries cover Solid operations currently implemented in Phase 3/4; pending features such as inline text edit, line endpoint edit, path point edit, full helper insertion, layer ordering, and DSL save/format/build history are not included yet.
- Delete undo reconstructs direct layout slots via an `add` patch. Generated/helper slot restoration still relies on the existing server patch support and needs targeted manual verification.
- Undo/redo refreshes from server artifacts after each operation; there is no local-only rollback preview.

## Phase 5/6 Progress Notes

Implemented after Phase 4:

- Added Solid API calls for the existing DSL save, DSL format, and build endpoints.
- The DSL pane is now editable and tracks a local dirty draft separate from generated artifacts.
- Save writes the draft through `POST /api/editor/problems/{id}/dsl/` and replaces the draft with the server-formatted response.
- Format mirrors the existing editor flow: save the current draft first, then call `POST /dsl/format/`.
- Build calls `POST /build/`, records stdout/stderr/error output, refreshes semantic/layout/renderer/SVG artifacts, and refreshes the problem list status.
- Added Ctrl/Cmd+S for DSL save.
- Added a manual patch panel that mirrors the existing editor's slot id + JSON value flow.
- Manual Apply posts an update patch to `/layout-patch/` and refreshes the DSL draft from the response.
- Manual Build posts the same patch to `/layout-patch-and-build/` and refreshes artifacts/SVG via the shared patch-and-build path.

Current intentional limits:

- Build follows the existing editor behavior and builds the saved DSL file; it does not automatically save an unsaved dirty draft before building.
- DSL save/format/build are not recorded in the visual undo/redo history.
- Manual patch UI currently supports the existing quick update flow only. Full arbitrary patch arrays and add/delete/layer patch authoring remain pending.
- Build output display is intentionally compact and has not yet been manually compared against the existing build log UI.

## Phase 1 Minimum Matrix

These rows must move from `Planned` to implemented and verified before Phase 1 can be considered complete:

| ID | Feature | Existing Editor | SolidJS | Auto Test | Manual Test | Status |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| F001 | Existing `/editor/` still loads and `/editor-next/` is separate | Yes | Implemented | Pass | Pending | Phase 1 implemented |
| F003 | Problem list loading | Yes | Implemented | Build/typecheck pass | Pending | Phase 1 implemented |
| F006 | Problem selection/open | Yes | Implemented | Build/typecheck pass | Pending | Phase 1 implemented |
| F008 | DSL/layout/renderer/SVG artifact read/display | Yes | Implemented | Build/typecheck pass | Pending | Phase 1 implemented |
| F016 | Read-only slot selection/list foundation | Yes | Implemented | Build/typecheck pass | Pending | Phase 1 implemented |
| F062 | Loading/error/status display | Yes | Implemented | Build/typecheck pass | Pending | Phase 1 implemented |
