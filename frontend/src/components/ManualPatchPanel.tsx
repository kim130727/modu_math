import { createEffect, createSignal } from "solid-js";
import type { EditorStore } from "../stores/editorStore";

interface ManualPatchPanelProps {
  store: EditorStore;
}

export function ManualPatchPanel(props: ManualPatchPanelProps) {
  const [target, setTarget] = createSignal("");
  const [value, setValue] = createSignal('{\n  "move_dx": 0,\n  "move_dy": 0\n}');

  createEffect(() => {
    const selectedId = props.store.state.selectedIds[0];
    if (selectedId && !target()) setTarget(selectedId);
  });

  return (
    <section class="manual-patch-section">
      <div class="pane-heading patch-heading">
        <span>Patch</span>
        <div>
          <button
            type="button"
            onClick={() => void props.store.applyManualPatch(target(), value(), false)}
            disabled={!props.store.state.problemId || props.store.state.loading}
          >
            Apply
          </button>
          <button
            type="button"
            onClick={() => void props.store.applyManualPatch(target(), value(), true)}
            disabled={!props.store.state.problemId || props.store.state.loading}
          >
            Build
          </button>
        </div>
      </div>
      <label>
        Slot ID
        <input value={target()} onInput={(event) => setTarget(event.currentTarget.value)} disabled={props.store.state.loading} />
      </label>
      <label>
        Value
        <textarea value={value()} onInput={(event) => setValue(event.currentTarget.value)} disabled={props.store.state.loading} />
      </label>
    </section>
  );
}
