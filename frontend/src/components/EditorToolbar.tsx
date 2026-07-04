import type { EditorStore } from "../stores/editorStore";
import { createSignal } from "solid-js";

interface EditorToolbarProps {
  store: EditorStore;
}

export function EditorToolbar(props: EditorToolbarProps) {
  const [problemPath, setProblemPath] = createSignal("");
  let imageInputRef!: HTMLInputElement;
  const hasSelection = () => props.store.state.selectedIds.length > 0;
  const hasMultiSelection = () => props.store.state.selectedIds.length > 1;
  const isBusy = () => props.store.state.loading;
  const currentProblemPath = () => problemPath() || props.store.state.problemId || "";

  return (
    <header class="editor-next-toolbar">
      <div class="toolbar-title">
        <strong>ModuMath Editor Next</strong>
        <span>{props.store.state.problemId ?? "No problem selected"}</span>
        <input
          class="toolbar-problem-input"
          list="editorNextProblemOptions"
          value={currentProblemPath()}
          placeholder="Problem path"
          onInput={(event) => setProblemPath(event.currentTarget.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter") void props.store.openProblem(currentProblemPath());
          }}
          disabled={props.store.state.loading}
        />
        <datalist id="editorNextProblemOptions">
          {props.store.state.problems.map((problem) => (
            <option value={problem.problem_id} />
          ))}
        </datalist>
      </div>
      <div class="toolbar-actions">
        <button
          type="button"
          classList={{ active: props.store.state.activeTool === "select" }}
          onClick={() => props.store.setActiveTool("select")}
          disabled={props.store.state.loading}
        >
          Select
        </button>
        <button
          type="button"
          classList={{ active: props.store.state.activeTool === "pan" }}
          onClick={() => props.store.setActiveTool("pan")}
          disabled={props.store.state.loading}
        >
          Pan
        </button>
        <button
          type="button"
          classList={{ active: props.store.state.snapEnabled }}
          onClick={() => props.store.setSnapEnabled(!props.store.state.snapEnabled)}
          disabled={props.store.state.loading}
        >
          Snap 5px
        </button>
        <button
          type="button"
          onClick={() => void props.store.undo()}
          disabled={props.store.state.loading || props.store.state.history.undoStack.length === 0}
        >
          Undo
        </button>
        <button
          type="button"
          onClick={() => void props.store.redo()}
          disabled={props.store.state.loading || props.store.state.history.redoStack.length === 0}
        >
          Redo
        </button>
        <button type="button" onClick={() => void props.store.refreshProblems()} disabled={props.store.state.loading}>
          Refresh
        </button>
        <button
          type="button"
          onClick={() => void props.store.openProblem(currentProblemPath())}
          disabled={!currentProblemPath().trim() || props.store.state.loading}
        >
          Open
        </button>
        <button
          type="button"
          onClick={() => props.store.state.problemId && void props.store.openProblem(props.store.state.problemId)}
          disabled={!props.store.state.problemId || props.store.state.loading}
        >
          Reload
        </button>
        <button type="button" onClick={() => void props.store.insertShape("text_box")} disabled={!props.store.state.document || props.store.state.loading}>
          Text Box
        </button>
        <button type="button" onClick={() => void props.store.insertShape("rect")} disabled={!props.store.state.document || props.store.state.loading}>
          Rect
        </button>
        <button type="button" onClick={() => void props.store.insertShape("circle")} disabled={!props.store.state.document || props.store.state.loading}>
          Circle
        </button>
        <button type="button" onClick={() => void props.store.insertShape("line")} disabled={!props.store.state.document || props.store.state.loading}>
          Line
        </button>
        <button type="button" onClick={() => void props.store.insertShape("triangle")} disabled={!props.store.state.document || props.store.state.loading}>
          Triangle
        </button>
        <button type="button" onClick={() => void props.store.insertShape("path")} disabled={!props.store.state.document || props.store.state.loading}>
          Curve
        </button>
        <button
          type="button"
          onClick={() => {
            if (!props.store.state.document || props.store.state.loading) return;
            imageInputRef.click();
          }}
          disabled={!props.store.state.document || props.store.state.loading}
        >
          Image
        </button>
        <input
          ref={imageInputRef}
          type="file"
          accept="image/*"
          hidden
          onChange={(event) => {
            const file = event.currentTarget.files?.[0];
            event.currentTarget.value = "";
            if (file) void props.store.insertImageFile(file);
          }}
        />
        <button type="button" onClick={() => void props.store.deleteSelectedSlots()} disabled={isBusy() || !hasSelection()}>
          Delete
        </button>
      </div>
      <div class="toolbar-actions toolbar-align" aria-label="Alignment and layer controls">
        <button type="button" onClick={() => void props.store.alignSelectedSlots("left")} disabled={isBusy() || !hasMultiSelection()}>
          Align L
        </button>
        <button type="button" onClick={() => void props.store.alignSelectedSlots("center")} disabled={isBusy() || !hasMultiSelection()}>
          Align C
        </button>
        <button type="button" onClick={() => void props.store.alignSelectedSlots("right")} disabled={isBusy() || !hasMultiSelection()}>
          Align R
        </button>
        <button type="button" onClick={() => void props.store.alignSelectedSlots("top")} disabled={isBusy() || !hasMultiSelection()}>
          Align T
        </button>
        <button type="button" onClick={() => void props.store.alignSelectedSlots("middle")} disabled={isBusy() || !hasMultiSelection()}>
          Align M
        </button>
        <button type="button" onClick={() => void props.store.alignSelectedSlots("bottom")} disabled={isBusy() || !hasMultiSelection()}>
          Align B
        </button>
        <button type="button" onClick={() => void props.store.layerSelectedSlots("front")} disabled={isBusy() || !hasSelection()}>
          Front
        </button>
        <button type="button" onClick={() => void props.store.layerSelectedSlots("back")} disabled={isBusy() || !hasSelection()}>
          Back
        </button>
        <button type="button" onClick={() => void props.store.layerSelectedSlots("forward")} disabled={isBusy() || !hasSelection()}>
          Forward
        </button>
        <button type="button" onClick={() => void props.store.layerSelectedSlots("backward")} disabled={isBusy() || !hasSelection()}>
          Backward
        </button>
      </div>
      <div class="toolbar-pickmodes" aria-label="Selection target filters">
        <button
          type="button"
          classList={{ active: props.store.state.pickMode === "all" }}
          onClick={() => props.store.setPickMode("all")}
          disabled={props.store.state.loading}
        >
          All
        </button>
        <button
          type="button"
          classList={{ active: props.store.state.pickMode === "text" }}
          onClick={() => props.store.setPickMode("text")}
          disabled={props.store.state.loading}
        >
          Text
        </button>
        <button
          type="button"
          classList={{ active: props.store.state.pickMode === "shape" }}
          onClick={() => props.store.setPickMode("shape")}
          disabled={props.store.state.loading}
        >
          Shape
        </button>
        <button
          type="button"
          classList={{ active: props.store.state.pickMode === "linepath" }}
          onClick={() => props.store.setPickMode("linepath")}
          disabled={props.store.state.loading}
        >
          Line/Path
        </button>
      </div>
    </header>
  );
}
