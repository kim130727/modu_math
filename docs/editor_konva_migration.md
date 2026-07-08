# Editor Konva Migration Notes

## Existing tldraw Editor Structure

- Entry points:
  - React/Vite entry: `src/modu_math_web/editor_next/src/main.tsx`
  - App switch: `src/modu_math_web/editor_next/src/App.tsx`
  - tldraw editor component: `src/modu_math_web/editor_next/src/components/MathProblemEditor.tsx`
  - Django route/template: `/editor-next/tldraw/`, `templates/editor_next/tldraw.html`
- Reusable pieces:
  - Problem API client: `src/api/editorApi.ts`
  - Problem list UI: `src/components/ProblemList.tsx`
  - Problem JSON types: `src/types/problem.ts`
  - DSL patch generation: `src/tldraw/converters/problemJsonToLayoutPatches.ts`
  - Existing shared CSS layout classes such as `math-problem-editor`, `mvp-toolbar`, and `editor-body`
- Strong tldraw dependencies:
  - `MathProblemEditor.tsx` imports `Tldraw`, `Editor`, `createShapeId`, `toRichText`, and tldraw shape ids.
  - `src/components/Toolbar.tsx` accepts a tldraw `Editor`.
  - `src/tldraw/shapes/*` are `ShapeUtil` implementations.
  - `problemJsonToTldraw.ts` and `tldrawToProblemJson.ts` map directly to tldraw store/shape props.

## New Konva Files

- Route/template:
  - `/editor-konva/`
  - `src/modu_math_web/editor_next/templates/editor_next/konva.html`
- Common schema:
  - `src/modu_math_web/editor_next/src/types/editorShape.ts`
- Konva editor:
  - `src/modu_math_web/editor_next/src/konva_editor/EditorKonva.tsx`
  - `KonvaStage.tsx`
  - `ShapeRenderer.tsx`
  - `KonvaToolbar.tsx`
  - `PropertyPanel.tsx`
  - `JsonImportExport.tsx`
  - `converters.ts`
  - `latexRenderer.ts`

## Implemented

- Separate Konva editor route without deleting or overwriting the tldraw editor.
- `ProblemJson -> EditorShapeDocument -> ProblemJson` adapter.
- Konva rendering for `rect`, `circle`, `line`, `text`, `image`.
- `math` shape placeholder with a future `renderLatexToSvgDataUrl` hook.
- Shape add, select, drag, delete, property edits, JSON import/export.
- Konva `Transformer` resize support for rect, image, text, math, and circle radius updates.
- Existing API problem loading and DSL patch saving reused.
- Unsupported base problem objects are preserved during save so the MVP does not accidentally delete shapes it cannot render yet.

## Still Missing

- Full parity for fraction bars, number lines, object groups, tables, paths, speech bubbles, and angle markers.
- Real LaTeX rendering through MathJax or KaTeX.
- Multi-select, z-order controls, copy/paste, keyboard shortcuts, undo/redo.
- Line endpoint editing. Lines currently support move only.
- Direct SVG/Flutter export from the new schema.
- Visual regression tests or Playwright coverage.

## tldraw Dependencies That Remain

- The original tldraw editor remains intact and still owns its custom `ShapeUtil` files.
- The Konva editor reuses `problemJsonToLayoutPatches.ts`, which lives under `src/tldraw/converters` but is actually renderer-agnostic because it consumes `ProblemJson`.
- The Vite bundle still includes both tldraw and Konva because `App.tsx` switches editor implementation by route.

## Advantages of the Konva Path

- Canvas rendering is driven by a small explicit `EditorShape` schema instead of tldraw store records.
- The save format is easier to align with Python DSL, SVG output, and Flutter rendering.
- Shape rendering and shape persistence are separated through adapters.
- Math rendering can be added as a focused `latex -> SVG data URL -> Konva.Image` pipeline.

## Cautions

- Konva has lower-level editor behavior than tldraw, so selection, snapping, history, grouping, text editing, and asset management must be built or adopted separately.
- Transformer updates must always write back to `EditorShape`; otherwise canvas state and exported JSON diverge.
- Unsupported DSL/problem objects should remain preserved until dedicated Konva renderers exist.
- Large images and future MathJax/KaTeX SVG conversion should be cached to avoid slow redraws.

## Next Steps

1. Move `problemJsonToLayoutPatches.ts` out of the `tldraw` folder into a renderer-neutral adapter folder.
2. Add Konva renderers for path, fraction bar, number line, group objects, and table.
3. Add keyboard delete and undo/redo.
4. Replace math placeholder with KaTeX or MathJax SVG conversion in `latexRenderer.ts`.
5. Add Playwright checks for `/editor-next/tldraw/` and `/editor-konva/`.
6. Split the Vite build into separate tldraw and Konva chunks if bundle size becomes an issue.
