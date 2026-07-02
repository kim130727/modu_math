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
    </header>
  );
}

