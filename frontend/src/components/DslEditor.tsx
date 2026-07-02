import { Show } from "solid-js";
import type { EditorDocument } from "../editor-core/model/editorDocument";

interface DslEditorProps {
  document: EditorDocument | null;
}

export function DslEditor(props: DslEditorProps) {
  return (
    <section class="dsl-section">
      <div class="pane-heading">DSL</div>
      <Show when={props.document} fallback={<div class="empty-state compact">No DSL loaded.</div>}>
        {(document) => <textarea readOnly value={document().dslSource} />}
      </Show>
    </section>
  );
}

