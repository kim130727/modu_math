import { For, Show } from "solid-js";
import { formatNumber } from "../editor-core/model/geometry";
import { slotBounds } from "../editor-core/transform/bounds";
import type { EditorStore } from "../stores/editorStore";
import type { LayoutSlot } from "../types/layout";

interface PropertyInspectorProps {
  store: EditorStore;
  selectedSlot: LayoutSlot | null;
}

export function PropertyInspector(props: PropertyInspectorProps) {
  const contentEntries = () => Object.entries(props.selectedSlot?.content ?? {});
  const bounds = () => (props.selectedSlot ? slotBounds(props.selectedSlot) : null);

  return (
    <section class="inspector-section">
      <div class="pane-heading">Inspector</div>
      <Show when={props.selectedSlot} fallback={<p class="muted">Select a slot from the slot list.</p>}>
        {(slot) => (
          <>
            <dl class="property-list">
              <dt>ID</dt>
              <dd>{slot().id}</dd>
              <dt>Kind</dt>
              <dd>{slot().kind}</dd>
              <dt>Bounds</dt>
              <dd>
                <Show when={bounds()} fallback="n/a">
                  {(box) => `${formatNumber(box().x)}, ${formatNumber(box().y)}, ${formatNumber(box().width)}, ${formatNumber(box().height)}`}
                </Show>
              </dd>
            </dl>
            <div class="content-table">
              <For each={contentEntries()}>
                {([key, value]) => (
                  <div>
                    <span>{key}</span>
                    <code>{typeof value === "string" || typeof value === "number" ? String(value) : JSON.stringify(value)}</code>
                  </div>
                )}
              </For>
            </div>
          </>
        )}
      </Show>
    </section>
  );
}

