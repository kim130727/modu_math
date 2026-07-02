import type { EditorStore } from "../stores/editorStore";

interface EditorToolbarProps {
  store: EditorStore;
}

export function EditorToolbar(props: EditorToolbarProps) {
  return (
    <header class="editor-next-toolbar">
      <div class="toolbar-title">
        <strong>ModuMath Editor Next</strong>
        <span>{props.store.state.problemId ?? "No problem selected"}</span>
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
        <button type="button" onClick={() => void props.store.refreshProblems()} disabled={props.store.state.loading}>
          Refresh
        </button>
        <button
          type="button"
          onClick={() => props.store.state.problemId && void props.store.openProblem(props.store.state.problemId)}
          disabled={!props.store.state.problemId || props.store.state.loading}
        >
          Reload
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
