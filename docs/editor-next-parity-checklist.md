# Editor Next Parity Checklist

Reference implementation: `/editor/`

Target implementation: `/editor-next/`

Scope for this document: inventory the stable editor behavior and compare it against the current editor-next Solid implementation. Do not remove or modify `/editor/`; future implementation should stay in `/editor-next/` unless a shared extraction is demonstrably safe.

Status values:

- implemented: editor-next reproduces the editor behavior closely enough to rely on it.
- partially implemented: editor-next has a related behavior, but it is incomplete or materially different.
- missing: editor-next does not expose the behavior.
- unclear: behavior exists in editor but needs runtime verification or deeper DSL/backend analysis before classifying.

## Source Areas Inspected

- `src/modu_math_web/editor/templates/editor/index.html`
- `src/modu_math_web/editor/static/editor/css/editor.css`
- `src/modu_math_web/editor/static/editor/js/editor-api.js`
- `src/modu_math_web/editor/static/editor/js/editor-app.js`
- `src/modu_math_web/editor/static/editor/js/editor-canvas.js`
- `src/modu_math_web/editor/static/editor/js/editor-commands.js`
- `src/modu_math_web/editor/static/editor/js/editor-properties.js`
- `src/modu_math_web/editor/static/editor/js/editor-state.js`
- `src/modu_math_web/editor/urls.py`
- `src/modu_math_web/editor/views.py`
- `src/modu_math_web/editor_next/`
- `src/modu_math_web/urls.py`

## 1. Toolbar Buttons In Editor

| Item | Editor reference behavior | editor-next status | Notes |
| --- | --- | --- | --- |
| Open | Opens problem path from titlebar input. | implemented | editor-next now has a freeform problem path input with datalist and Open/Enter support. |
| Reload | Reloads current problem. | implemented | Toolbar Reload reopens current problem. |
| Save DSL | Saves DSL textarea. | implemented | Present in DSL panel, not top toolbar. `Ctrl/Cmd+S` also saves in editor-next. |
| Format DSL | Calls format endpoint after saving/using current problem. | implemented | Present in DSL panel, not top toolbar. |
| Build | Calls build endpoint and refreshes output/artifacts. | implemented | Present in DSL panel. |
| Refresh List | Reloads problem list. | implemented | Toolbar Refresh exists. |
| Insert Text Box | Adds text box slot. | implemented | Present as Text Box. |
| Insert Image | File picker and image slot insertion. | implemented | editor-next now reads image files as data URLs and inserts scaled image slots. |
| Insert Table | Dialog with rows/columns and table insertion. | missing | No table insertion UI. |
| Insert Bar Model | Dialog with bars/cells/shading/fill/stroke/dashed options. | missing | No bar model UI. |
| Insert Tick Bar | Dialog with rows/ticks/fill/labels/unit/colors options. | missing | No tick bar UI. |
| Insert Graph Paper | Dialog with columns/rows. | missing | No graph paper insertion UI. |
| Insert Fraction | Dialog for numerator/denominator. | missing | No fraction insertion UI. |
| Insert Mixed Fraction | Dialog for whole/numerator/denominator. | missing | No mixed fraction insertion UI. |
| Shape Gallery | PowerPoint-like categorized gallery of lines, rectangles, shapes, teaching objects, arrows, etc. | partially implemented | editor-next now exposes direct insertion for text box, rect, circle, line, triangle, curve, and image; categorized gallery is still missing. |
| Snap Toggle | Toggle 5px snap with active state. | implemented | Present as Snap 5px. |
| Pick All | Selection filter for all elements. | implemented | Present. |
| Pick Line/Path | Selection filter for lines/paths. | partially implemented | Present, but editor-next matching is simpler than editor's SVG/slot/group logic. |
| Pick Text | Selection filter for text. | partially implemented | Present, but lacks editor's generated/fraction/group handling. |
| Pick Shape | Selection filter for shapes. | partially implemented | Present for rect/circle/polygon/image; no full shape gallery/generated group support. |
| Align Left/Center/Right/Top/Middle/Bottom | Align selected items. | partially implemented | Toolbar has align controls, but only based on layout slot bounds; editor handles groups and SVG-derived selection states more deeply. |
| Bring to Front / Send to Back / Bring Forward / Send Backward | Reorders region slot IDs. | partially implemented | Present; needs verification against editor behavior for grouped/generated selections. |
| Undo / Redo | Patch-backed history. | partially implemented | Present, but history coverage is narrower than editor. |
| Delete Selected | Deletes selected slots. | implemented | Present via toolbar and keyboard. |
| Select/Pan/Zoom controls | Not in editor toolbar except canvas select; editor-next adds Select, Pan, zoom buttons. | implemented | Extra editor-next behavior, not parity blocker. |

## 2. Canvas Interactions

| Item | Editor reference behavior | editor-next status | Notes |
| --- | --- | --- | --- |
| Render built SVG in canvas frame. | Injects SVG into `.svg-box`, centers/scales via CSS, preserves interactive IDs. | partially implemented | editor-next renders sanitized SVG inside `.canvas-surface`; adds pan/zoom not present in editor. Visual sizing differs. |
| Fallback layout preview when SVG absent. | Mostly expects artifact SVG. | implemented | editor-next has `LayoutSvgPreview`; this is extra capability. |
| Click select SVG slot elements. | Selects via SVG IDs, renderer refs, DSL IDs, fractions, grouped objects. | partially implemented | Basic slot ID matching exists; advanced editor grouping is incomplete. |
| Multi-select with Shift/Ctrl/Cmd. | Supported. | implemented | Both support appended/toggled selection. |
| Marquee select. | Drag blank canvas shows `.marquee` and selects intersecting slots. | partially implemented | editor-next has `.marquee-box`; uses layout slot bounds, not all SVG-derived/group bounds. |
| Blank click clears selection. | Supported. | implemented | editor-next clears selection on empty click. |
| Pan canvas. | Not a reference behavior. | implemented | editor-next supports pan by tool, middle button, or Alt. |
| Zoom canvas. | Not a reference behavior. | implemented | editor-next supports zoom/reset. |
| Context menu shape formatting. | Right-click or context behavior opens shape format menu for shapes. | missing | No context menu/shape format menu in editor-next. |
| Draw-to-place shapes. | Some line/path/freeform shape types are drawn by pointer. | missing | editor-next inserts centered rect/text only. |
| Canvas selection. | Select canvas, show canvas guide, edit W/H. | partially implemented | editor-next now edits canvas W/H in inspector; explicit canvas selection/guide is still missing. |

## 3. SVG Rendering Behavior

| Item | Editor reference behavior | editor-next status | Notes |
| --- | --- | --- | --- |
| Raw SVG artifact display. | `innerHTML` inserts SVG plus overlays. | partially implemented | editor-next sanitizes SVG and inserts it; sanitization may alter valid renderer output and should be verified. |
| Remove dangerous scripts/events. | No explicit sanitizer in reference. | implemented | editor-next sanitizes script/foreignObject/event handlers. This is safer but not exact parity. |
| Preserve text hit behavior. | Adds text hit proxies and `pointer-events: bounding-box`. | partially implemented | editor-next uses hit tests/fallback geometry, but no text-hit proxy elements. |
| Preserve line/path hit behavior. | Adds thick invisible stroke proxies for thin strokes. | partially implemented | editor-next has distance-based fallback but no actual SVG hit proxies. |
| Selection overlay inside SVG. | SVG overlay group with bounds, line handles, rotate handle, path handles, table handles. | partially implemented | editor-next uses absolutely positioned HTML selection box and 8 resize handles only. |
| Selected visual class. | `.slot-selected` drop shadow on selected SVG elements. | implemented | editor-next toggles `slot-selected` and now includes matching CSS. |
| Pick disabled visual class. | `.pick-disabled` dims non-pickable elements. | missing | No equivalent class/behavior observed. |

## 4. Slot Selection Behavior

| Item | Editor reference behavior | editor-next status | Notes |
| --- | --- | --- | --- |
| Resolve slot IDs from SVG element IDs. | Uses renderer refs, DSL ID cache, layout cache, fractions, generated groups. | partially implemented | editor-next has renderer ref, DSL source, fraction, and fallback matching, but less coverage. |
| Select fraction as one logical object. | Fraction part IDs map to a prefix and move/update as group. | partially implemented | `parseFractionPartId` exists; resize/edit coverage is limited. |
| Select character/layout/generated/figure/paper-fold/measurement/graph-paper groups. | Group-aware selection and patching. | missing | editor-next treats slots primarily as individual layout slots. |
| Slot list/strip selection. | Editor has problem tree, not slot strip; selection mostly via canvas/inspector. | implemented | editor-next slot strip is extra and supports selection. |
| Pick filters update active button states. | All/Text/Shape/LinePath active state and pointer behavior. | partially implemented | Active states exist; no `.pick-disabled` visual behavior. |

## 5. Drag Behavior

| Item | Editor reference behavior | editor-next status | Notes |
| --- | --- | --- | --- |
| Drag selected slot(s). | Live SVG move, overlay move, patch on pointer up. | partially implemented | editor-next shows overlay offset and commits move patches, but does not live-transform actual SVG elements. |
| Drag multiple selected slots. | Supported with group-specialized patching. | partially implemented | Basic multi-slot move patch exists; group-specific movement is missing. |
| Snap-aware drag. | 5px snap toggle. | implemented | editor-next snaps drag deltas when enabled. |
| Drag line/path/group special cases. | Handles line endpoints, generated groups, fractions, measurements, etc. | missing | editor-next move uses `{move_dx, move_dy}` for selected IDs only. |
| Drag commit throttling/status. | Drag status, queued/debounced patch persistence. | missing | editor-next commits at pointer up and status is generic loading/ready. |

## 6. Resize Behavior

| Item | Editor reference behavior | editor-next status | Notes |
| --- | --- | --- | --- |
| Rect/text/image resize. | Handles all sides/corners with snap. | implemented | editor-next supports rect/text_box/image via content x/y/width/height. |
| Circle resize. | Supported. | implemented | editor-next maps resized box to center/radius. |
| Line endpoint resize. | `p1`/`p2` endpoint handles. | missing | editor-next has only rectangular handles and no line endpoint edit. |
| Line rotation. | `r` rotation handle and angle snapping. | missing | No rotate handle. |
| Generic transform/rotate edit. | Inspector can edit `Rotate` transform string; resize can update transform-aware elements. | missing | No rotate inspector field. |
| Polygon/path resize. | Path/polygon coordinate scaling. | missing | Bounds can be selected, but no resize patch for polygon/path. |
| Path point editing. | Cubic/polyline anchor/control point handles. | missing | No path point handles. |
| Canvas resize. | Select canvas and edit W/H. | partially implemented | Inspector W/H edits are patch-backed; no canvas select overlay/handles yet. |
| Table divider resize. | Table adjustment handles for row/column dividers. | missing | No table editing handles. |
| Group resize. | Figure/graph-paper/group-specific resize support. | missing | No group resize support. |

## 7. Text Editing Behavior

| Item | Editor reference behavior | editor-next status | Notes |
| --- | --- | --- | --- |
| Inspector text input and Update Text. | `textEditInput` plus Update Text button. | partially implemented | editor-next generic inspector edits any primitive `text` field, but lacks dedicated text section/button. |
| Double-click inline text editor. | Opens positioned inline input; Enter commits, Escape cancels, blur commits. | implemented | editor-next has inline editor for SVG `text` elements. |
| Font size increase/decrease buttons. | A-/A+ adjust selected text font size. | missing | No dedicated buttons. Primitive `font_size` can be edited if present. |
| Text alignment left/center/right. | Aligns selected text inside cell/table context. | missing | No dedicated text alignment controls. |
| Enter in inspector text input commits. | Supported. | partially implemented | Generic inspector blurs on Enter; manual text panel absent. |

## 8. Shape Insertion Behavior

| Item | Editor reference behavior | editor-next status | Notes |
| --- | --- | --- | --- |
| Insert text box. | Adds DSL/layout slot and rebuilds. | implemented | editor-next supports `text_box`. |
| Insert rectangle. | Shape gallery rectangle insertion. | implemented | editor-next supports centered `rect`. |
| Insert lines/curves/freeform. | Gallery plus draw-mode for some shapes. | partially implemented | editor-next supports centered line and curve insertion; draw-mode/freeform placement is still missing. |
| Insert common polygons/basic shapes. | Many gallery options. | partially implemented | editor-next supports circle and triangle; broader gallery remains missing. |
| Insert composite teaching objects. | Boy/girl/school/house/playground/etc. | missing | No composite insertion. |
| Shape fill/stroke menu and swatches. | Fill/stroke colors, no border, dash styles. | missing | No shape format UI. |
| Image insertion from file. | Reads image file and inserts image payload. | implemented | editor-next now provides file input and image slot insertion. |

## 9. Table Insertion/Editing Behavior

| Item | Editor reference behavior | editor-next status | Notes |
| --- | --- | --- | --- |
| Table insertion dialog. | Rows/columns with validation and Enter/Escape handling. | missing | No table UI. |
| Table slot creation. | Adds table layout content. | missing | No table insertion store action. |
| Table cell selection. | Shows `.table-cell-selected`. | missing | No table cell selection. |
| Table row/column divider handles. | `.table-adjust-handle` resize controls. | missing | No table divider handles. |
| Table auto-fit/fill editing. | Functions exist in editor for fill/autofit behavior. | missing | No table edit panel. |

## 10. Inspector Panel Fields

| Item | Editor reference behavior | editor-next status | Notes |
| --- | --- | --- | --- |
| Canvas X/Y/W/H. | X/Y readonly, W/H editable. | implemented | Canvas inspector fields are now present and W/H commit patch-backed canvas updates. |
| Select Canvas button. | Selects canvas for resize/edit. | missing | No canvas selection. |
| Slot ID field. | Shows selected slot ID and can be used for patch target. | partially implemented | Inspector shows ID read-only; manual patch panel has editable Slot ID. |
| Position/size X/Y/W/H. | Dedicated numeric fields commit layout patches. | partially implemented | Generic inspector edits primitive content fields if present; no normalized slot X/Y/W/H section yet. |
| Font field. | Dedicated font size numeric field. | partially implemented | Generic primitive `font_size` edit if present. |
| Rotate field. | Dedicated transform/rotate field. | missing | No rotation field. |
| Text edit field and Update Text. | Dedicated text section. | partially implemented | Generic content editor and inline edit only. |
| Font smaller/larger. | A-/A+ buttons. | missing | No controls. |
| Text align left/center/right. | Buttons. | missing | No controls. |
| Patch JSON. | JSON textarea with Patch and Patch + Build. | implemented | editor-next has manual patch Apply and Build. |
| DSL/JSON tabs. | Inspector tabs switch between DSL and artifacts. | partially implemented | editor-next has separate inspector DSL and stage artifact section, not tabs. |
| Artifact textareas. | Separate semantic/solvable/layout/renderer read-only textareas. | implemented | editor-next now renders separate read-only artifact panes. |

## 11. Problem Tree Behavior

| Item | Editor reference behavior | editor-next status | Notes |
| --- | --- | --- | --- |
| Problem list API. | Loads `/api/editor/problems/`. | implemented | Shared API. |
| Hierarchical tree. | Builds folders/files, collapsible folders, remembers collapsed folders. | implemented | editor-next now renders a collapsible problem tree. |
| Filter by filename/folder. | Filters tree and forces open matching folders. | implemented | Filtered tree forces folders open and matches full problem paths. |
| Count display. | Shows count. | implemented | Shows visible/total count. |
| Active problem highlight. | Active file button. | implemented | Active list button. |
| Problem datalist/freeform input. | Titlebar input with datalist. | implemented | editor-next now has a toolbar problem path input and datalist. |
| Auto-load first problem. | Loads first known problem into input; open action loads. | partially implemented | editor-next auto-opens URL requested problem or first problem with SVG/first problem. |

## 12. DSL Editor Behavior

| Item | Editor reference behavior | editor-next status | Notes |
| --- | --- | --- | --- |
| DSL textarea. | Inspector tab panel textarea. | implemented | Present in inspector. |
| Save. | Calls `/dsl/`, updates DSL and dirty state. | implemented | Present. |
| Format. | Calls `/dsl/format/`, updates DSL. | implemented | Present. |
| Build. | Calls `/build/`, updates artifacts/SVG/log. | implemented | Present. |
| Dirty tracking. | State has dirty flag and body dataset. | partially implemented | editor-next status shows dirty/saved; no body dataset. |
| Disable controls while busy. | Buttons disabled while operations run. | implemented | Present. |
| Save shortcut. | Reference does not show `Ctrl/Cmd+S`; editor-next adds it. | implemented | Extra capability. |

## 13. Artifact Panels

| Item | Editor reference behavior | editor-next status | Notes |
| --- | --- | --- | --- |
| Build log. | Separate notes/log area. | partially implemented | editor-next shows build log in Artifacts section if build output exists. |
| Status box. | Separate status box with success/error messages. | partially implemented | editor-next footer status/error only. |
| Semantic view. | Dedicated read-only textarea. | implemented | Separate pane now exists. |
| Solvable view. | Dedicated read-only textarea. | implemented | Separate pane now exists. |
| Layout view. | Dedicated read-only textarea. | implemented | Separate pane now exists. |
| Renderer view. | Dedicated read-only textarea. | implemented | Separate pane now exists. |
| JSON tab switching. | DSL/JSON tabs in inspector. | missing | No tabs. |

## 14. Build/Save/Format/Patch API Calls

| Item | Editor reference behavior | editor-next status | Notes |
| --- | --- | --- | --- |
| `GET /api/editor/problems/` | List problems. | implemented | Shared endpoint. |
| `GET /api/editor/problems/<problem_id>/` | Load detail. | implemented | Shared endpoint. |
| `POST /api/editor/problems/<problem_id>/dsl/` | Save DSL. | implemented | Shared endpoint. |
| `POST /api/editor/problems/<problem_id>/dsl/format/` | Format DSL. | implemented | Shared endpoint. |
| `POST /api/editor/problems/<problem_id>/build/` | Build artifacts. | implemented | Shared endpoint. |
| `POST /api/editor/problems/<problem_id>/layout-patch/` | Patch only. | implemented | Manual patch uses this. |
| `POST /api/editor/problems/<problem_id>/layout-patch-and-build/` | Patch and build. | implemented | Used for move/edit/insert/delete/history. |
| `GET /api/editor/assets/<problem_id>/<filename>` | Serve problem asset. | unclear | API exists, but editor-next image insertion/display asset use was not verified. |
| CSRF headers. | Reads `csrftoken` for non-GET. | implemented | Shared behavior in TypeScript client. |
| API error classification. | Network/patch/parse/schema/build/unknown. | implemented | Present in TypeScript client. |

## 15. Keyboard Shortcuts

| Item | Editor reference behavior | editor-next status | Notes |
| --- | --- | --- | --- |
| Ctrl/Cmd+Z undo. | Supported outside inputs/textareas. | implemented | Present. |
| Ctrl/Cmd+Shift+Z redo. | Supported. | implemented | Present. |
| Ctrl/Cmd+Y redo. | Supported. | implemented | Present. |
| Ctrl/Cmd+C copy selected slots. | Supported. | implemented | editor-next now copies selected layout slots into an internal buffer. |
| Ctrl/Cmd+V paste copied slots. | Supported. | partially implemented | editor-next pastes copied slots with add/delete patch history and offset geometry; advanced group/generated-slot paste remains incomplete. |
| Ctrl/Cmd+S save. | Not in reference. | implemented | Extra editor-next behavior. |
| Delete/Backspace delete selection. | Supported. | implemented | Present. |
| Arrow keys move selection. | 1px, Shift=10px, queued save. | partially implemented | Movement exists, but no queued/debounced save/status and group behavior differs. |
| Escape cancel drawing / close shape UI. | Supported. | partially implemented | Inline editor Escape cancels; no drawing/gallery/format menu to close. |
| Enter commits dialog fields. | Table/graph/bar/tick/math dialogs support Enter. | missing | Dialogs absent. |
| Escape closes dialogs. | Supported in editor dialogs. | missing | Dialogs absent. |

## 16. Error Handling

| Item | Editor reference behavior | editor-next status | Notes |
| --- | --- | --- | --- |
| Network errors. | Wrapped and shown via status/log. | implemented | Classified in `httpClient`, displayed in footer. |
| API error categories. | Classified by message/status. | implemented | Same category family. |
| Build failure output. | Shows stdout/stderr/error and failed status. | partially implemented | Build failure payload is captured; display is less detailed than editor log/status pairing. |
| Invalid manual patch JSON. | Caught and shown. | implemented | editor-next validates JSON object. |
| Empty DSL save. | Backend rejects; UI surfaces error. | implemented | Via API client/footer. |
| Dialog validation. | Clamps table/graph/model inputs. | missing | Dialogs absent. |
| Per-action localized success/error messages. | Editor has specific `setStatus` messages. | missing | editor-next mostly shows generic loading/ready/error. |

## 17. Status Messages

| Item | Editor reference behavior | editor-next status | Notes |
| --- | --- | --- | --- |
| Status text area. | Dedicated status box with operation-specific Korean messages. | partially implemented | Footer status is generic: Loading/Saving/Formatting/Building/Ready. |
| Build log. | Persistent stdout/stderr log. | partially implemented | Present only in artifact section after build output. |
| Status bar hints. | Shows "Drag, resize, align, edit text" and shortcuts. | missing | Footer instead shows counts/history/dirty. |
| Snap toggle message. | Shows enabled/disabled message. | missing | Active state only. |
| Pick mode message. | Shows selected mode message. | missing | Active state only. |
| Drag/keyboard save messages. | Shows movement/save progress. | missing | Generic loading only. |
| Error class styling. | `.err`, `.ok` classes. | partially implemented | Footer error uses `<strong>`; no equivalent ok/error status classes. |

## 18. CSS Classes Required For Visual Parity

| Class/selector | Editor reference behavior | editor-next status | Notes |
| --- | --- | --- | --- |
| `.wrap.powerpoint`, `.ppt-shell`, `.ppt-titlebar`, `.ppt-ribbon`, `.ribbon-group`, `.ribbon-dropdown` | PowerPoint-like shell and ribbon. | missing | editor-next uses `.editor-next-shell` and a different dark toolbar. |
| `.ppt-workspace`, `.ppt-sidebar`, `.ppt-stage`, `.ppt-inspector`, `.ppt-notes`, `.ppt-statusbar` | Three-pane layout with notes/statusbar. | partially implemented | Three-pane layout exists, but dimensions/styling differ and no notes/statusbar parity. |
| `.pane-title`, `.pane-body` | Stable panel headers/bodies. | partially implemented | editor-next uses `.pane-heading`. |
| `.icon-sprite`, `.icon-btn` | SVG icon toolbar buttons. | missing | editor-next uses text buttons. |
| `.svg-box` and nested SVG pointer-event rules | Centered slide frame and interactive SVG hit behavior. | partially implemented | editor-next uses `.canvas-viewport`, `.canvas-surface`, `.svg-content`. |
| `.slot-selected` | Selected SVG drop shadow. | implemented | CSS now exists for editor-next selected SVG elements. |
| `.pick-disabled` | Dim/disable unpickable items. | partially implemented | CSS now exists; behavior that applies the class is still missing. |
| `.canvas-guide` | Canvas selection guide. | missing | No canvas selection. |
| `.selection-overlay`, `.selection-bounds`, `.selection-line`, `.selection-handle` | SVG selection overlay. | missing | editor-next uses HTML `.selection-box` and `.resize-handle`. |
| `.path-edit-guide`, `.path-point-handle` | Path point editing. | missing | No path handles. |
| `.table-adjust-handle`, `.table-cell-selected` | Table editing visuals. | missing | No table editing. |
| `.inline-text-editor` | Inline text input. | partially implemented | Same class exists in editor-next, but CSS differs and is inline-styled. |
| `.marquee` | Marquee selection rectangle. | partially implemented | editor-next uses `.marquee-box`. |
| `.shape-gallery`, `.shape-category-title`, `.shape-grid`, `.shape-choice` | Shape gallery. | missing | No gallery. |
| `.shape-format-menu`, `.shape-format-row`, `.shape-swatch`, `.shape-format-btn` | Shape formatting popup. | missing | No popup. |
| `.table-dialog`, `.table-dialog-panel`, `.table-dialog-fields`, `.table-dialog-actions` | Insertion dialogs. | missing | No dialogs. |
| `.tree`, `.folder`, `.children.collapsed`, `.file-btn`, `.tree-tools`, `.tree-count` | Hierarchical problem tree. | partially implemented | Tree/folder/children/file classes now exist; `tree-tools` naming is still represented by editor-next filter controls rather than exact class parity. |
| `.inspector-section`, `.field-grid`, `.single-field`, `.ppt-tabs`, `.ppt-tab-panel`, `.artifact-grid`, `.log`, `.err`, `.ok` | Inspector, tabs, artifacts, log/status styling. | partially implemented | `.field-grid`, canvas inspector styling, and `.artifact-grid` now exist; tabs/log status classes remain incomplete. |

## Short Technical Plan

1. Establish editor-next parity tests and visual checkpoints before changing behavior. Cover problem loading, SVG rendering, selection, drag, resize, text edit, DSL save/format/build, manual patch, keyboard shortcuts, and artifact display.
2. Bring over the editor shell structure and visual vocabulary in editor-next: ribbon groups, icon buttons, problem tree, inspector sections, notes/log/status areas, DSL/JSON tabs, and required selection/table/path/shape CSS classes.
3. Expand editor-next state and selection model to match editor's slot resolution: renderer refs, DSL IDs, fractions, generated groups, layout groups, figures, paper-fold/measurement/table/graph-paper groups, and pick-disabled visuals.
4. Port interaction behavior feature by feature: live SVG drag, robust multi-select/marquee, keyboard move queueing, line endpoint/rotation handles, path point handles, canvas selection/resize, table cell/divider editing, and group-specific resize/move patches.
5. Port insertion workflows: image, table, graph paper, bar model, tick bar, fraction/mixed fraction, and the full shape gallery with draw-mode placement and shape formatting menu.
6. Normalize inspector and artifact panels to reference behavior: canvas fields, slot ID, position/size/font/rotate fields, dedicated text tools, patch controls, DSL/JSON tabs, and separate semantic/solvable/layout/renderer panes.
7. Keep `/editor/` unchanged throughout. Prefer isolated editor-next TypeScript modules; extract shared code only where tests show behavior is identical and the stable editor surface is unaffected.
