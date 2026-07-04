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
  let canvasWidthRef!: HTMLInputElement;
  let canvasHeightRef!: HTMLInputElement;

  function commitPrimitiveField(slot: LayoutSlot, key: string, previous: unknown, input: HTMLInputElement): void {
    if (props.store.state.loading) return;
    if (typeof previous === "number") {
      const next = Number(input.value);
      if (!Number.isFinite(next) || next === previous) {
        input.value = String(previous);
        return;
      }
      void props.store.updateSlotProperties(slot.id, { [key]: next });
      return;
    }
    if (typeof previous === "string") {
      const next = input.value;
      if (next === previous) return;
      void props.store.updateSlotProperties(slot.id, { [key]: next });
    }
  }

  function commitOnEnter(event: KeyboardEvent): void {
    if (event.key !== "Enter") return;
    const input = event.currentTarget instanceof HTMLInputElement ? event.currentTarget : null;
    input?.blur();
  }

  function isColorField(key: string, value: unknown): value is string {
    return (key === "fill" || key === "stroke") && typeof value === "string" && /^#[0-9a-f]{6}$/i.test(value);
  }

  function commitCanvasSize(): void {
    const width = Number(canvasWidthRef?.value);
    const height = Number(canvasHeightRef?.value);
    if (!Number.isFinite(width) || !Number.isFinite(height)) {
      const canvas = props.store.state.document?.detail.layout?.canvas;
      if (canvas) {
        canvasWidthRef.value = String(canvas.width);
        canvasHeightRef.value = String(canvas.height);
      }
      return;
    }
    void props.store.updateCanvasSize(width, height);
  }

  return (
    <>
      <section class="inspector-section">
        <div class="pane-heading">Canvas</div>
        <Show when={props.store.state.document?.detail.layout?.canvas} fallback={<p class="muted">No canvas loaded.</p>}>
          {(canvas) => (
            <div class="field-grid">
              <label>
                X
                <input type="number" value="0" readonly />
              </label>
              <label>
                Y
                <input type="number" value="0" readonly />
              </label>
              <label>
                W
                <input
                  ref={canvasWidthRef}
                  type="number"
                  min="20"
                  step="1"
                  value={canvas().width}
                  disabled={props.store.state.loading}
                  onKeyDown={commitOnEnter}
                  onBlur={commitCanvasSize}
                />
              </label>
              <label>
                H
                <input
                  ref={canvasHeightRef}
                  type="number"
                  min="20"
                  step="1"
                  value={canvas().height}
                  disabled={props.store.state.loading}
                  onKeyDown={commitOnEnter}
                  onBlur={commitCanvasSize}
                />
              </label>
            </div>
          )}
        </Show>
      </section>
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
                      <label for={`property-${slot().id}-${key}`}>{key}</label>
                      <Show
                        when={typeof value === "string" || typeof value === "number"}
                        fallback={<code>{JSON.stringify(value)}</code>}
                      >
                        <div classList={{ "color-field": isColorField(key, value) }}>
                          <Show when={isColorField(key, value)}>
                            <input
                              class="color-swatch"
                              aria-label={`${key} color`}
                              type="color"
                              value={String(value)}
                              disabled={props.store.state.loading}
                              onChange={(event) => void props.store.updateSlotProperties(slot().id, { [key]: event.currentTarget.value })}
                            />
                          </Show>
                          <input
                            id={`property-${slot().id}-${key}`}
                            type={typeof value === "number" ? "number" : "text"}
                            step={typeof value === "number" ? "0.1" : undefined}
                            value={String(value)}
                            disabled={props.store.state.loading}
                            onKeyDown={commitOnEnter}
                            onBlur={(event) => commitPrimitiveField(slot(), key, value, event.currentTarget)}
                          />
                        </div>
                      </Show>
                    </div>
                  )}
                </For>
              </div>
            </>
          )}
        </Show>
      </section>
    </>
  );
}
