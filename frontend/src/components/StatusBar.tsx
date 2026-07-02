import { Show } from "solid-js";
import type { EditorState } from "../stores/editorStore";

interface StatusBarProps {
  state: EditorState;
}

export function StatusBar(props: StatusBarProps) {
  return (
    <footer class="editor-next-status">
      <span>{props.state.loading ? "Loading" : "Ready"}</span>
      <span>{props.state.problems.length} problems</span>
      <span>{props.state.document?.slots.length ?? 0} slots</span>
      <Show when={props.state.error}>
        {(error) => <strong>{error().category}: {error().message}</strong>}
      </Show>
    </footer>
  );
}

