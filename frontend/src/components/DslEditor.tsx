import { Show } from "solid-js";
import type { EditorStore } from "../stores/editorStore";

interface DslEditorProps {
  store: EditorStore;
}

export function DslEditor(props: DslEditorProps) {
  return (
    <section class="dsl-section">
      <div class="pane-heading dsl-heading">
        <span>DSL</span>
        <div>
          <button
            type="button"
            onClick={() => void props.store.saveDslDraft()}
            disabled={!props.store.state.problemId || props.store.state.saving || props.store.state.loading}
          >
            Save
          </button>
          <button
            type="button"
            onClick={() => void props.store.formatDslDraft()}
            disabled={!props.store.state.problemId || props.store.state.formatting || props.store.state.loading}
          >
            Format
          </button>
          <button
            type="button"
            onClick={() => void props.store.buildCurrentProblem()}
            disabled={!props.store.state.problemId || props.store.state.building || props.store.state.loading}
          >
            Build
          </button>
        </div>
      </div>
      <Show when={props.store.state.document} fallback={<div class="empty-state compact">No DSL loaded.</div>}>
        <textarea
          value={props.store.state.dslDraft}
          disabled={props.store.state.saving || props.store.state.formatting}
          onInput={(event) => props.store.setDslDraft(event.currentTarget.value)}
        />
      </Show>
    </section>
  );
}
