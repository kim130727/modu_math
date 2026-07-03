# SolidJS Editor Manual Checklist

Date: 2026-07-03

Use the same problem and same initial DSL when comparing `/editor/` and `/editor-next/`.

## Phase 1 Read Baseline

- [ ] Existing editor still loads at `/editor/`
- [ ] Solid editor loads at `/editor-next/`
- [ ] Problem list loading
- [ ] Problem filtering
- [ ] Problem selection
- [ ] Current problem display
- [ ] DSL display
- [ ] Semantic JSON display
- [ ] Solvable JSON display
- [ ] Layout JSON display
- [ ] Renderer JSON display
- [ ] SVG display
- [ ] Local SVG image assets display
- [ ] Loading state
- [ ] Error recovery
- [ ] Problem switching state reset

## Phase 2 Selection And Canvas

- [ ] Single selection from slot strip
- [ ] Single selection from SVG/canvas
- [ ] Shift multi-selection from slot strip
- [ ] Shift multi-selection from SVG/canvas
- [ ] Ctrl/Cmd multi-selection from slot strip
- [ ] Ctrl/Cmd multi-selection from SVG/canvas
- [ ] Selection clear by empty canvas click
- [ ] Marquee selection
- [ ] Pick mode: all
- [ ] Pick mode: text
- [ ] Pick mode: shape
- [ ] Pick mode: line/path
- [ ] Selection overlay position
- [ ] Multi-object bounding box
- [ ] Resize handles are displayed
- [ ] Zoom in
- [ ] Zoom out
- [ ] Viewport reset
- [ ] Pan tool
- [ ] Alt-drag pan
- [ ] Middle-button pan

## Phase 3 Editing

- [ ] Drag move single selected slot
- [ ] Drag move multiple selected slots
- [ ] Drag move sends one server request on pointerup
- [ ] Drag move refreshes DSL
- [ ] Drag move refreshes layout JSON
- [ ] Drag move refreshes renderer JSON
- [ ] Drag move refreshes SVG
- [ ] Drag move failure displays an error without breaking selection
- [ ] Resize selected slot
- [ ] Move by keyboard arrow keys
- [ ] Shift-arrow coarse movement
- [ ] Snap toggle
- [ ] Shape deletion
- [ ] Shape insertion
- [ ] Color change
- [ ] Property edit
- [ ] Inline text edit

## Later Phases

- [ ] Undo
- [ ] Redo
- [ ] Redo stack clears on new edit
- [ ] DSL save
- [ ] DSL format
- [ ] Manual patch apply
- [ ] Manual patch + build
- [ ] Build
- [ ] Build success refresh
- [ ] Build failure display
- [ ] Existing editor regression after Solid edits
- [ ] Semantic and solvable preservation after save/build
- [ ] Existing `/editor/` remains usable if `/editor-next/` fails
