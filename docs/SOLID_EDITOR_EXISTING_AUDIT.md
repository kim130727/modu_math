# SolidJS Editor Existing Audit

Date: 2026-07-02

Scope: Phase 0 audit only. No existing editor URL, template, JavaScript, CSS, Django view, DSL compiler, schema, renderer, or CLI behavior was changed.

## Summary

The current editor is served at `/editor/` and its API namespace is `/api/editor/`. It is not only a DSL text editor: it is a PowerPoint-like visual editor that renders server-generated SVG, overlays selection/resize/path handles in the browser, derives layout patches from SVG elements, and sends those patches to Django. Django applies most edits to `problem.dsl.py` using LibCST and falls back to generated editor override files for generated/helper slots.

The canonical pipeline remains:

```text
PNG
-> problem.dsl.py
-> semantic JSON
-> solvable JSON
-> layout JSON
-> renderer JSON
-> SVG
```

For the SolidJS migration, the safest first rendering strategy is Strategy A: keep server-generated SVG as the visual source and implement SolidJS editing overlays on top of it. This preserves text baseline, renderer namespace behavior, viewBox handling, SVG image href rewriting, font/stroke/fill behavior, paths, polygon points, and any renderer-specific output while parity is being established. Layout JSON should be used as structured metadata for slot lists, bounds, region membership, and inspector values, not as a canonical source.

## File Map

| File path | Role | Main functions/classes | Depends on | Calls API |
| --- | --- | --- | --- | --- |
| `src/modu_math_web/urls.py` | Project routes. Redirects `/` to `/editor/`, mounts editor page and API. | `urlpatterns` | `modu_math_web.editor.views`, `modu_math_web.editor.urls` | N/A |
| `src/modu_math_web/editor/urls.py` | Editor API routes under `/api/editor/`. | `urlpatterns` | `views` | N/A |
| `src/modu_math_web/editor/views.py` | Django HTML/API views. JSON body parsing, error payloads, list/detail/assets/save/format/build/layout patch endpoints. | `editor_index`, `problems_list`, `problem_detail`, `problem_asset`, `save_dsl`, `format_dsl`, `build_problem`, `layout_patch`, `layout_patch_and_build` | `services.problems`, `services.dsl_patch`, `services.build` | N/A |
| `src/modu_math_web/editor/templates/editor/index.html` | Existing editor template. PowerPoint-like shell, SVG sprite icons, problem tree, ribbon, dialogs, inspector, DSL/artifact panes. | Static IDs used by JS: `svgPreview`, `dslEditor`, `problemTree`, buttons/dialogs/inputs. | `editor.css`, `editor-app.js` | JS only |
| `src/modu_math_web/editor/static/editor/css/editor.css` | Existing editor styling. | PowerPoint shell, stage, inspector, dialogs, handles, inline text editor, swatches. | HTML class/ID contract | None |
| `src/modu_math_web/editor/static/editor/js/editor-api.js` | Browser API adapter and error categorization. | `requestJson`, `listProblems`, `loadProblem`, `saveDsl`, `formatDsl`, `buildProblem`, `applyLayoutPatches`, `applyLayoutPatchesAndBuild`, `classifyApiError` | Fetch API, CSRF cookie | All `/api/editor/...` endpoints |
| `src/modu_math_web/editor/static/editor/js/editor-state.js` | Small module state store. Main app also keeps local variables. | `getState`, `setState`, `subscribe`, `resetState`; state includes problem, DSL, selected IDs, zoom, pan, statuses, artifacts. | None | None |
| `src/modu_math_web/editor/static/editor/js/editor-commands.js` | Generic command history helper. Main app uses its own richer history arrays for visual edits. | `executeCommand`, `undo`, `redo`, `clearHistory`, `createLayoutPatchCommand` | None | None |
| `src/modu_math_web/editor/static/editor/js/editor-canvas.js` | SVG/canvas primitives. Renders SVG string, handles marquee box, drawing preview, pointer capture, path/polygon transforms, hit proxies, coordinate conversion, selection overlay, resize/path/table handles, line rotation math. | `renderSvgContainer`, `beginMarqueeBox`, `finishMarqueeBox`, `svgPoint`, `selectedIdsFromSlots`, `ensureSelectionOverlay`, `updateSelectionOverlay`, `renderTableAdjustmentHandles`, `renderPathPointHandles`, `adjustedBBox`, `linePatchFromEndpoint`, `linePatchFromRotation`, `pointToSegmentDistance` | Browser SVG DOM | None |
| `src/modu_math_web/editor/static/editor/js/editor-properties.js` | Minimal property binding helper. | `initProperties`, `bindCommitInputs` | DOM | None |
| `src/modu_math_web/editor/static/editor/js/editor-app.js` | Main existing editor application. Owns problem loading, SVG rendering, selection, drag, resize, text editing, insertion, formatting, layer/order, history, keyboard shortcuts, status, API calls. | More than 100 local helpers; key state variables: `currentProblemId`, `dragState`, `resizeState`, `selectedSlots`, `undoStack`, `redoStack`, `pickMode`, `marqueeState`, `pendingDrawShape`, `drawState`, `inlineTextEditState`, caches, `snapEnabled`. | All static JS modules, template IDs, SVG DOM, API adapter | All `/api/editor/...` endpoints |
| `src/modu_math_web/editor/state.py` | Server-side dataclass snapshot, currently not central to request handling. | `PanState`, `ArtifactsState`, `EditorState` | dataclasses | None |
| `src/modu_math_web/editor/services/problems.py` | Problem discovery, path validation, artifact reads, asset href rewriting, raw DSL save/format. | `validate_problem_id`, `resolve_problem_paths`, `list_problem_directories`, `read_problem_detail`, `save_problem_dsl`, `format_problem_dsl`, `read_artifacts` | Django settings, `format_dsl_source` | N/A |
| `src/modu_math_web/editor/services/dsl_format.py` | Optional DSL formatter wrapper. | `format_dsl_source` | `black` if installed | N/A |
| `src/modu_math_web/editor/services/build.py` | In-process build used by editor. Loads DSL module, compiles semantic/layout/renderer/SVG, applies editor overrides, validates schemas, writes artifacts. | `BuildResult`, `run_problem_build`, `build_with_artifacts`, `_build_problem_artifacts` | `modu_math.dsl`, layout overrides, renderer, schema validators | N/A |
| `src/modu_math_web/editor/services/dsl_patch.py` | LibCST DSL patch engine and editor override fallback. Supports slot update/add/delete/layer/canvas/group/helper patches. | `SUPPORTED_SLOTS`, `SLOT_KIND_TO_CTOR`, `SlotUpdater`, `CanvasUpdater`, `SlotAddTransformer`, `SlotDeleteTransformer`, `GeneratedHelperSlotOverrideUpdater`, group move transformers, `apply_layout_patches` | `libcst`, `ast`, editor problem paths, formatter | N/A |
| `src/modu_math/layout/editor_overrides.py` | Applies `*.editor_overrides.json` to generated layout before renderer build. | `apply_editor_overrides` | Layout documents | N/A |
| `tests/web/test_editor_api.py` | Existing API and static editor regression baseline. | 46 tests covering routes, path traversal, static assets, build, layout patch, add/delete/group/helper/canvas behaviors. | Django test client | `/editor/`, `/api/editor/...`, static files |

## Feature Inventory

| ID | Feature | Existing implementation location | Input event | State change | Server call | Result |
| --- | --- | --- | --- | --- | --- | --- |
| F001 | Editor page load | `urls.py`, `views.editor_index`, `templates/editor/index.html` | Browser opens `/editor/` | Static shell loaded | GET `/editor/` | Existing editor page displayed |
| F002 | Static asset loading | Template, `editor.css`, JS modules | Page load | CSS/JS module graph active | GET `/static/editor/...` | UI and app initialized |
| F003 | Problem list loading | `editor-app.js:loadProblems`, `editor-api.js:listProblems`, `services.problems.list_problem_directories` | Initial load, refresh button | `knownProblems`, datalist/tree | GET `/api/editor/problems/` | Problem tree and count displayed |
| F004 | Problem tree filtering | `editor-app.js:filteredProblemIds`, `renderProblemTree` | Search input `input` | Tree render changes | None | Filtered problem tree |
| F005 | Folder collapse/expand | `editor-app.js:renderTreeNode`, `collapsedProblemFolders` | Folder button click | Folder set toggled | None | Tree branch expands/collapses |
| F006 | Problem selection/open | `editor-app.js:selectProblem`, `editor-api.js:loadProblem`, `views.problem_detail` | Tree click, Open button, Reload button | `currentProblemId`, DSL textarea, artifacts, selection/history reset | GET `/api/editor/problems/{id}/` | DSL, JSON panes, SVG, status updated |
| F007 | Path traversal rejection | `services.problems.validate_problem_id`, `resolve_problem_paths`, `views.problem_asset` | Malicious problem/asset path | None | GET/POST endpoints | 400/404 JSON error |
| F008 | Artifact display | `editor-app.js:renderArtifacts`, `renderJsonView`, `renderSvg` | Problem selection/build/patch | Artifact panes and SVG DOM replaced | GET detail or POST build/patch | semantic/solvable/layout/renderer/SVG visible |
| F009 | Relative SVG image asset rewrite | `services.problems._rewrite_svg_asset_hrefs`, `problem_asset` | Problem detail read | SVG href rewritten | GET detail, GET asset | Local images served via `/api/editor/assets/...` |
| F010 | DSL text editing | Template `dslEditor`, `editor-app.js:saveDsl` | User edits textarea | Dirty/save status | POST `/api/editor/problems/{id}/dsl/` | DSL formatted and saved |
| F011 | DSL format | `editor-app.js:formatDsl`, `views.format_dsl`, `services.dsl_format` | Format button | DSL textarea refreshed | POST `/api/editor/problems/{id}/dsl/format/` | Current DSL formatted by black when available |
| F012 | Build | `editor-app.js:buildProblem`, `views.build_problem`, `services.build` | Build button | `building`, build log, artifacts | POST `/api/editor/problems/{id}/build/` | semantic/layout/renderer/SVG/solvable artifacts written and returned |
| F013 | Build failure reporting | `editor-api.js:requestJson`, `classifyApiError`, `views.build_problem` | Failed build | `error`, status/log | POST build | JSON error with stdout/stderr/artifacts if available |
| F014 | Manual patch | `readPatchPayload`, `patchOnly` | Patch button | DSL/artifacts maybe refreshed | POST `/layout-patch/` | LibCST patch applied, DSL textarea refreshed |
| F015 | Patch + build | `patchAndBuild`, `layout_patch_and_build` | Patch + Build button | DSL/artifacts/log refreshed | POST `/layout-patch-and-build/` | Patch applied then artifacts rebuilt |
| F016 | Single selection | `bindSlotInteractions`, `selectSlotElement`, `selectedSlots` | SVG slot click/pointerdown | `selectedSlots`, selected ID, inspector | None | Selection class and overlay displayed |
| F017 | Multi-selection | `beginSlotPointerDown`, `selectSlotElement` | Shift/Ctrl/Cmd click | `selectedSlots` map appends/toggles | None | Multiple selected slots/group overlays |
| F018 | Marquee selection | `beginMarquee`, `updateMarquee`, `finishMarquee`, canvas helpers | Empty SVG drag | `marqueeState`, selected slots | None | All elements in box selected |
| F019 | Selection clear | `clearSelection`, empty SVG/container click paths | Empty click or mode-specific miss | Selection map cleared | None | Overlay/inspector cleared |
| F020 | Pick modes | `pickMode`, pick buttons, `matchesPickMode` | Pick all/line/text/shape buttons | `pickMode` | None | Click hit testing restricted by type |
| F021 | SVG hit proxies | `appendStrokeHitProxy`, `appendTextHitProxy`, `syncSlotHitProxies` | SVG render/bind | Extra invisible hit targets | None | Thin strokes/text boxes easier to select |
| F022 | Drag move | `dragState`, `applyDragDeltaToSelection`, `buildDragEndPatchSet`, `commitPatches` | Pointer drag selected slot | DOM moved locally; one history entry | POST `/layout-patch-and-build/` by default | DSL patch saved, build artifacts refreshed |
| F023 | Drag throttling | `scheduleDragFrame`, `consumePendingDragDelta` | Pointermove | Local DOM only per frame | None during move | Avoids server calls on every pointermove |
| F024 | Keyboard move | Document `keydown`, arrow logic, `queueKeyboardCommit` | Arrow keys | Local move and delayed commit | POST layout patch/build | 1px move, Shift = 10px |
| F025 | Snap toggle | `snapEnabled`, `snapValue`, `snapPatchValue` | Snap button | Snap on/off | None | 5px snapping applied/removed |
| F026 | Resize handles | `ensureSelectionOverlay`, `beginResizeFromHandle`, `updateResize`, `endResize` | Handle pointerdown/move/up | `resizeState`, DOM preview, history | POST patch/build | Slot/canvas/group resized |
| F027 | Line endpoint edit | `linePatchFromEndpoint`, line-specific resize branch | `p1`/`p2` handle drag | x1/y1/x2/y2 | POST patch/build | Line endpoint changed |
| F028 | Line rotation | `linePatchFromRotation`, `rotationValueFromPointer` | Rotation handle drag | `transform=rotate(...)` | POST patch/build | Line/slot rotated |
| F029 | Path point editing | `editablePathFromD`, `renderPathPointHandles`, `pathPointPatchFromHandle` | Path handle drag | `d` updated | POST patch/build | Path point adjusted |
| F030 | Polygon/path transforms | `parsePolygonPoints`, `formatPolygonPoints`, `transformPathD`, `scalePathD`, `shiftPathD` | Drag/resize | points/d transformed | POST patch/build | Shape path/polygon updated |
| F031 | Canvas selection/resize | Select Canvas button, `CanvasUpdater`, `resizePatchForCanvas` | Button, resize handle | Canvas selected, width/height patch | POST layout patch | `Canvas(width,height)` updated |
| F032 | Property inspector coordinate edit | `commitPropertyPatch`, property inputs | Change/Enter | Local property patch/history | POST patch/build | Slot fields updated |
| F033 | Text inspector edit | `textEditInput`, `commitTextEdit`, `textEditBtn` | Button/Enter | text patch/history | POST patch/build | Text slot content updated |
| F034 | Inline text edit | `beginInlineTextEdit`, `finishInlineTextEdit` | Double click text/hit proxy; Enter/Escape/blur | `inlineTextEditState`, textarea overlay | POST patch/build on commit | Text edited in-place; Escape cancels |
| F035 | Font size controls | `fontDecreaseBtn`, `fontIncreaseBtn`, table font handling | Button click | font size patch/history | POST patch/build | Text/table font changes |
| F036 | Text alignment | `textAlignLeft/Center/Right`, table/text alignment logic | Button click | align or x/max_width patch | POST patch/build | Text/table cell alignment changes |
| F037 | Shape insertion gallery | `SHAPE_CATEGORIES`, `pendingDrawShape`, draw functions | Shape gallery click, canvas drag/click | Draw preview, add patches | POST patch/build | Rect/circle/polygon/path/composite shape inserted |
| F038 | Text box insertion | `insertTextBoxBtn`, `uniqueInsertedSlotId` | Button click | Add patch | POST patch/build | `TextBoxSlot` added in region |
| F039 | Image insertion | File input/change, FileReader, `insertImage` | Image button/file select | Data URL add patch | POST patch/build | `ImageSlot` inserted |
| F040 | Table insertion | Dialog, `tablePatches`, `insertTable` | Button/dialog confirm | Multiple add patches | POST patch/build | Rect/line/text table slots inserted |
| F041 | Graph paper insertion | Dialog, `graphPaperPatches` | Button/dialog confirm | Multiple add patches | POST patch/build | Grid line slots inserted |
| F042 | Bar model insertion | Dialog, `barModelPatches` | Button/dialog confirm | Multiple add patches | POST patch/build | Bar model slots inserted |
| F043 | Tick bar insertion | Dialog, `tickBarPatches` | Button/dialog confirm | Multiple add patches | POST patch/build | Tick bar rows, labels, ticks inserted |
| F044 | Fraction/mixed fraction insertion | Dialog, `fractionPatches` | Button/dialog confirm | Multiple add patches | POST patch/build | Math text/line slots inserted |
| F045 | Shape fill/stroke/dash formatting | Shape format menu, swatches, `applyShapeFormatPatch` | Menu buttons/color inputs | style patch/history | POST patch/build | fill/stroke/stroke_width/stroke_dasharray changed |
| F046 | Delete selection | `deleteSelectedSlots`, `SlotDeleteTransformer` | Delete button, Delete/Backspace | Selection cleared/local nodes removed | POST layout patch/build | Slots removed or `deleted_slots` override recorded |
| F047 | Copy/paste selected slots | `copySelectedSlots`, `pasteCopiedSlots`, `cloneSlotId` | Ctrl/Cmd+C, Ctrl/Cmd+V | `copyBuffer`, `pasteSequence`, add patches | POST patch/build | Duplicate slots inserted with unique IDs |
| F048 | Undo | `pushHistory`, `undoAction`, document Ctrl/Cmd+Z | Button or shortcut | undoStack -> redoStack; historyBusy | POST layout patch/build | Previous slot values restored |
| F049 | Redo | `redoAction`, Ctrl/Cmd+Y or Ctrl/Cmd+Shift+Z | Button or shortcut | redoStack -> undoStack | POST layout patch/build | Next slot values restored |
| F050 | History cap/reset | `pushHistory`, problem selection reset | Edits/problem switch | Max 100 entries; stacks cleared | None | Redo cleared on new action; clean switch |
| F051 | Alignment | `alignSelected` | Align buttons | move patches/history | POST patch/build | Selected objects aligned left/center/right/top/middle/bottom |
| F052 | Layer ordering | `layerSelected`, `reorderLayerIds`, `layer` op | Layer buttons | region slot order override | POST `/layout-patch/` | Render order changes via editor overrides |
| F053 | Table cell selection | `selectedTableCells`, table hit/handles | Table click/handle drag | Selected cells/resize state | POST patch/build | Table cells selected or relayouted |
| F054 | Table divider adjustment | `renderTableAdjustmentHandles`, `tableDividerValuesFromDrag` | Table handle drag | line/text/rect patches | POST patch/build | Column/row dimensions adjusted |
| F055 | Generated/helper group movement | JS group detection plus `dsl_patch.py` group transformers | Drag group | `move_dx/move_dy` patches | POST patch/build | Character, table, figure, graph, paper fold, measurement groups move together |
| F056 | Generated slot override fallback | `GeneratedHelperSlotOverrideUpdater`, `_save_editor_slot_override` | Patch generated slot | `*.editor_overrides.json` | POST layout patch | Layout override saved without regenerating DSL slot |
| F057 | Editor override delete/layer state | `_save_editor_slot_delete`, `_save_editor_region_slot_order`, build apply | Delete/layer generated state | `*.editor_overrides.json` | POST layout patch/build | Generated layout adjusted at build |
| F058 | Supported slot patch fields | `SUPPORTED_SLOTS` | Patch/update/add | Validated by slot type | POST layout patch | Only supported fields applied |
| F059 | Import insertion for added slots | `DslImportEnsurer` | Add patch | DSL import changed minimally | POST layout patch | Missing `modu_math.dsl` constructor import added |
| F060 | Solvable/semantic preservation on build | `services.build` | Build | `SEMANTIC_OVERRIDE`, `SEMANTIC_ANSWER`, `SOLVABLE` merged/validated | POST build | semantic/solvable artifacts preserved when DSL defines them |
| F061 | Local image href inlining on build | `inline_local_image_hrefs` in build | Build | SVG output with image data | POST build | Generated SVG can embed local assets |
| F062 | Error category/status messaging | `withApiErrors`, `userMessageForError`, `setStatus` | Any failed API/action | Status/error state | Any endpoint | User-facing error shown |
| F063 | DSL/artifact slot ID caches | `extractDslSlotIds`, `extractSourceDslSlotIds`, `extractRendererSlotRefs` | Selection/insertion/render | Cache by pane contents | None | Better slot ID mapping and unique ID generation |

## Shortcut Inventory

| Shortcut | Condition | Action | Existing implementation location |
| --- | --- | --- | --- |
| Ctrl/Cmd+Z | Not typing in protected text input/textarea | Undo visual edit | `editor-app.js` document `keydown`, `undoAction` |
| Ctrl/Cmd+Y | Same | Redo visual edit | `editor-app.js` document `keydown`, `redoAction` |
| Ctrl/Cmd+Shift+Z | Same | Redo visual edit | `editor-app.js` document `keydown`, `redoAction` |
| Delete | Selection exists | Delete selected slots | `editor-app.js` document `keydown`, `deleteSelectedSlots` |
| Backspace | Selection exists | Delete selected slots | `editor-app.js` document `keydown`, `deleteSelectedSlots` |
| Arrow keys | Selection exists | Move selected slots by 1px | `editor-app.js` document `keydown`, keyboard move block |
| Shift+Arrow keys | Selection exists | Move selected slots by 10px | `editor-app.js` document `keydown`, keyboard move block |
| Escape | Inline text edit active | Cancel inline edit | `finishInlineTextEdit(false)` |
| Enter | Inline text edit active | Commit inline edit | `finishInlineTextEdit(true)` |
| Enter | Property/patch/dialog inputs | Commit current input/dialog | Input-specific `keydown` handlers |
| Ctrl/Cmd+C | Selection exists | Copy selected slots | `copySelectedSlots` shortcut block |
| Ctrl/Cmd+V | Copy buffer exists | Paste copied slots | `pasteCopiedSlots` shortcut block |

## API Inventory

| Method | URL | Request | Response | Errors | Called from |
| --- | --- | --- | --- | --- | --- |
| GET | `/editor/` | None | HTML template | Django errors | Browser |
| GET | `/api/editor/problems/` | None | `{problems: ProblemSummary[]}` | 500 JSON error | `editor-api.js:listProblems`, `loadProblems` |
| GET | `/api/editor/problems/{problem_id}/` | Path problem id | Detail with `dsl`, `semantic`, `solvable`, `layout`, `renderer`, `svg` | 400 invalid id, 404 missing, 500 | `loadProblem`, `selectProblem` |
| GET | `/api/editor/assets/{problem_id}/{filename}` | Safe filename only | FileResponse with guessed content type | 400 invalid filename/path, 404 missing, 500 | Rewritten SVG image hrefs |
| POST | `/api/editor/problems/{problem_id}/dsl/` | `{dsl: string}` | `{ok, problem_id, dsl}` | 400 invalid/empty body, 404, 500 | `saveDsl`, Save button |
| POST | `/api/editor/problems/{problem_id}/dsl/format/` | None | `{ok, problem_id, dsl}` | 400/404/500 | `formatDsl`, Format button |
| POST | `/api/editor/problems/{problem_id}/build/` | None | `{ok, problem_id, stdout, stderr, artifacts}` | 400/404; 500 with `error` on build failure | `buildProblem`, Build button |
| POST | `/api/editor/problems/{problem_id}/layout-patch/` | `{patches: Patch[], format?: boolean}` | `{ok, problem_id, applied, dsl}` | `DslPatchError` as 400, 404, 500 | manual patch, drag/resize/edit/insertion/delete/layer |
| POST | `/api/editor/problems/{problem_id}/layout-patch-and-build/` | `{patches: Patch[], format?: boolean}` | Patch response plus `{build, artifacts}` | Patch failure or build 500 | most visual commits |

## State Inventory

- Problem/application: `currentProblemId`, `knownProblems`, `collapsedProblemFolders`, `loading`, `saving`, `building`, `saveStatus`, `buildStatus`, `error`, `artifacts`, DSL textarea contents.
- Selection: `selectedSlots: Map`, `selectedSlotId`, `selectedElement`, `selectedIds` in module store, `selectedTableCells`, canvas selection sentinel `__canvas__`.
- Tools and modes: `activeTool`, `pickMode` (`all`, `linepath`, `text`, `shape`), `snapEnabled`, `pendingDrawShape`, `drawState`, `openMenu`, `inlineEditor`.
- Interaction: `dragState`, `resizeState`, `marqueeState`, pointer IDs, `dragFrameRequested`, `resizeFrameRequested`, `pendingResizePoint`, `lastDragStatusAt`.
- History: main app `undoStack`, `redoStack`, `historyBusy`; generic command module has separate `undoStack`/`redoStack`.
- Save queue: `dragCommitTimer`, `dragCommitTask`, `pendingPatchSaves`, `keyboardCommitTimer`.
- Canvas/SVG: SVG DOM in `#svgPreview`, viewBox-derived canvas bounds, zoom/pan fields exist in `editor-state.js` and `state.py` but no complete pan/zoom UI was found in current template/app.
- Caches: `dslSlotIdCache`, `sourceDslSlotIdCache`, `rendererSlotRefCache`, `layoutGroupCache`.
- Clipboard/insertion: `copyBuffer`, `pasteSequence`, insertion dialog fields, `imageInsertInFlight`.
- Server state: `problem.editor_overrides.json` sidecar can hold slot overrides, deleted slots, and region slot order.

## Save And Build Sequence

### Raw DSL Save

```text
User clicks Save DSL
-> editor-app.js reads #dslEditor.value
-> POST /api/editor/problems/{id}/dsl/ with {dsl}
-> views.save_dsl validates non-empty string
-> services.problems.save_problem_dsl resolves safe path
-> format_dsl_source runs black if available
-> formatted DSL overwrites problem.dsl.py
-> response returns saved DSL
-> frontend updates textarea, save status, dirty=false
```

### Format

```text
User clicks Format
-> frontend first calls saveDsl()
-> POST /api/editor/problems/{id}/dsl/format/
-> server reads current problem.dsl.py
-> format_dsl_source runs black if available
-> file is overwritten with formatted DSL
-> response returns DSL
-> frontend updates textarea/status
```

### Visual Patch

```text
User drags/resizes/edits/inserts/deletes/layers
-> frontend mutates SVG DOM locally for preview
-> pointerup/button commit builds patch list
-> history entry is pushed when applicable
-> POST /layout-patch-and-build/ for most visual edits
   or POST /layout-patch/ for patch-only/layer/manual flows
-> views.layout_patch validates JSON body and format flag
-> dsl_patch.apply_layout_patches parses problem.dsl.py with LibCST
-> add/update/delete/layer/canvas/group/helper-specific transformer applies minimal change
-> unsupported generated/helper fields may be written to problem.editor_overrides.json
-> updated DSL is formatted unless format=false and written to disk
-> for patch-and-build, build_with_artifacts runs immediately
-> frontend receives DSL/artifacts, rerenders SVG/artifact panes
-> previous selection is restored when possible
```

### Build

```text
User clicks Build or visual patch requests build
-> POST /api/editor/problems/{id}/build/
-> services.build.resolve_problem_paths validates path
-> DSL module loaded from problem.dsl.py with unique module name
-> ProblemTemplate obtained from PROBLEM_TEMPLATE or build_problem_template()
-> compile semantic and layout from DSL
-> apply problem.editor_overrides.json if present
-> compile renderer JSON
-> render SVG and inline local image hrefs
-> apply SEMANTIC_OVERRIDE / SEMANTIC_ANSWER
-> load SOLVABLE or build_solvable when present
-> validate semantic/layout/renderer schemas
-> validate semantic/solvable answer match when solvable exists
-> write generated JSON/SVG artifacts
-> return artifacts plus stdout/stderr/error status
-> frontend updates log, artifacts, SVG, problem list status
```

## Hidden Or Easily Missed Features

- Shift/Ctrl/Cmd click appends or toggles multi-selection.
- Empty canvas drag creates marquee selection.
- Thin strokes and text boxes receive invisible hit proxies.
- Pick mode restricts selection target classes.
- Drag/resize uses local DOM preview and commits one server patch at the end.
- Arrow keys move by 1px; Shift+Arrow moves by 10px.
- Snap is a user toggle; default is 5px.
- Undo/redo replays layout patches through the server, not only local DOM state.
- Copy/paste duplicates selected slots with unique IDs and canvas-bounded paste offsets.
- Delete can remove direct DSL slots or record generated-slot deletes in editor overrides.
- Layer changes are stored as region slot order overrides.
- Generated/helper groups include tables, bar/tick/grid figures, graph paper, paper folding helpers, compass/ruler measurement tools, character/speaker groups, fraction groups, and direct layout groups.
- Some helper child edits are rejected; e.g. measurement tool parts must move as a group.
- `format=false` is supported for fast drag saves.
- Build applies editor overrides before renderer compilation.
- Relative image hrefs in existing SVG detail are rewritten to asset endpoints; build can inline local images.
- Added slots automatically ensure missing `modu_math.dsl` imports.
- DSL patch target matching allows normalized and unique-prefix matching.
- Canvas size is patchable through target `__canvas__` or `canvas`.
- Shape formatting supports no border, solid, short dash, long dash, dot-dash, and dotted patterns.
- Table resizing includes divider handles and selected cell text relayout.
- Current code contains zoom/pan state fields, but no complete user-facing zoom/pan implementation was identified in the existing template/app during this audit.

## Existing Tests Baseline

Commands run on 2026-07-02:

```text
uv run pytest
-> 110 passed, 1 warning in 3.70s

uv run pytest tests\web\test_editor_api.py
-> 46 passed, 1 warning in 3.54s

After Phase 1 route/static addition:
uv run pytest
-> 111 passed, 1 warning in 3.50s

uv run pytest tests\web\test_editor_api.py
-> 47 passed, 1 warning in 1.91s

npm run typecheck
-> passed

npm run build
-> passed; emitted editor-next.js and editor-next.css

After Phase 2 selection, pan, and handle foundation:
uv run pytest -q
-> 111 passed, 1 warning

uv run pytest tests\web\test_editor_api.py -q
-> 47 passed, 1 warning

npm run typecheck
-> passed

npm run build
-> passed; emitted updated editor-next.js and editor-next.css
```

Warning in both runs: Django `RemovedInDjango50Warning` about future `USE_TZ` default.

## Phase 1 File-Level Implementation Plan

Do not replace `/editor/`. Add `/editor-next/` and, if a new API adapter is needed, add it without changing `/api/editor/` semantics. For Phase 1, prefer reusing existing `/api/editor/` contracts until the SolidJS shell needs a separate namespace.

Proposed file layout:

```text
frontend/
  package.json
  tsconfig.json
  vite.config.ts
  src/
    api/httpClient.ts
    api/editorApi.ts
    types/api.ts
    types/layout.ts
    types/renderer.ts
    editor-core/model/editorDocument.ts
    editor-core/model/editorObject.ts
    editor-core/model/geometry.ts
    editor-core/transform/coordinateTransform.ts
    editor-core/transform/bounds.ts
    editor-core/selection/selectionManager.ts
    editor-core/history/historyManager.ts
    stores/editorStore.ts
    features/problem-list/problemListModel.ts
    features/canvas/svgDocument.ts
    components/EditorPage.tsx
    components/EditorToolbar.tsx
    components/ProblemList.tsx
    components/CanvasViewport.tsx
    components/SvgContent.tsx
    components/PropertyInspector.tsx
    components/DslEditor.tsx
    components/BuildOutput.tsx
    components/StatusBar.tsx
```

Django additions for Phase 1:

```text
src/modu_math_web/editor_next/
  views.py              # render /editor-next/
  urls.py               # optional adapter namespace if needed
  templates/editor_next/index.html
```

Phase 1 behavior target:

- Load problem list.
- Select/reload a problem.
- Display current problem ID.
- Display DSL text read-only or editable with no save parity claim yet.
- Display server SVG exactly as returned.
- Display semantic/solvable/layout/renderer JSON.
- Derive a slot list from layout/renderer for read-only inspector.
- Preserve existing editor behavior and tests.

## Phase 1 Implementation Notes

Implemented after this audit:

- Added separate Django page at `/editor-next/`.
- Added a new `frontend/` SolidJS + TypeScript + Vite workspace.
- Built static assets into `src/modu_math_web/editor_next/static/editor_next/assets/`.
- Reused the existing `/api/editor/` read endpoints for problem list and problem detail.
- Kept `/editor/` and the legacy static assets unchanged.
- Implemented read-only problem list, filter, problem selection, server SVG display, DSL display, artifacts JSON display, slot list, and basic inspector.
- Added a Django regression test proving `/editor-next/` uses `editor_next` assets and does not load legacy `/static/editor/js/editor-app.js`.

## Phase 2 Implementation Notes

Implemented after Phase 1:

- Added Solid selection-state toggling for single and Shift/Ctrl/Cmd multi-selection.
- Added SVG click delegation that maps server-rendered SVG element IDs back to layout slot IDs without mutating the SVG markup.
- Added empty canvas/SVG click selection clearing.
- Added a read-only selection overlay based on layout bounds for selected slots.
- Added basic canvas zoom controls and viewport reset state.
- Added empty-canvas drag marquee selection using layout bounds.
- Added a basic pan tool plus Alt-drag and middle-button drag panning.
- Added type-restricted pick filters (`all`, `text`, `shape`, `linepath`) for SVG click and marquee selection.
- Added display-only resize handles around selected layout bounds.

Current intentional limits:

- No visual edits are written to DSL in this phase.
- Resize handle interaction, drag movement, and hit proxy parity remain pending.
- Selection bounds are layout-derived and do not yet account for path bounds or transformed/rotated geometry.
- Pick filters are layout-kind based and do not yet include the existing editor's invisible hit proxy behavior.
