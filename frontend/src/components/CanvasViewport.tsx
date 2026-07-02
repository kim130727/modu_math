import { For, Show } from "solid-js";
import type { EditorStore } from "../stores/editorStore";
import { SvgContent } from "./SvgContent";

interface CanvasViewportProps {
  store: EditorStore;
}

export function CanvasViewport(props: CanvasViewportProps) {
  return (
    <section class="canvas-section">
      <div class="canvas-header">
        <div>
          <strong>Canvas</strong>
          <span>
            {props.store.state.document?.detail.layout?.canvas?.width ?? "-"} x{" "}
            {props.store.state.document?.detail.layout?.canvas?.height ?? "-"}
          </span>
        </div>
        <div>{props.store.state.selectedIds.length} selected</div>
      </div>
      <div class="canvas-viewport" onClick={() => props.store.clearSelectedSlots()}>
        <Show when={props.store.state.document?.detail.svg} fallback={<div class="empty-state">Select a problem with SVG output.</div>}>
          {(svg) => <SvgContent svg={svg()} />}
        </Show>
      </div>
      <div class="slot-strip">
        <For each={props.store.state.document?.slots ?? []}>
          {(slot) => (
            <button
              type="button"
              classList={{ active: props.store.state.selectedIds.includes(slot.id) }}
              onClick={(event) => {
                event.stopPropagation();
                props.store.selectSlot(slot.id);
              }}
            >
              <span>{slot.id}</span>
              <small>{slot.kind}</small>
            </button>
          )}
        </For>
      </div>
    </section>
  );
}

