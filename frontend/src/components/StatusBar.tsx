import { Show } from "solid-js";
import type { EditorState } from "../stores/editorStore";

interface StatusBarProps {
  state: EditorState;
}

export function StatusBar(props: StatusBarProps) {
  return (
    <footer class="editor-next-status ppt-statusbar">
      <span class={props.state.error ? "err" : "ok"}>{statusText(props.state)}</span>
      <span>{props.state.statusMessage}</span>
      <span>{props.state.problems.length} problems</span>
      <span>{props.state.document?.slots.length ?? 0} slots</span>
      <span>{props.state.dirty ? "dirty" : "saved"}</span>
      <span>{props.state.history.undoStack.length} undo</span>
      <span>{props.state.history.redoStack.length} redo</span>
      <Show when={props.state.error}>
        {(error) => <strong class="err">{error().category}: {error().message}</strong>}
      </Show>
    </footer>
  );
}

function statusText(state: EditorState): string {
  if (state.loading) return "Loading";
  if (state.saving) return "Saving";
  if (state.formatting) return "Formatting";
  if (state.building) return "Building";
  return "Ready";
}
