import { createEffect, createSignal, For, Show } from "solid-js";
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
  const [textValue, setTextValue] = createSignal("");
  const [fillColor, setFillColor] = createSignal("#ffffff");
  const [strokeColor, setStrokeColor] = createSignal("#111827");
  const [boundsDraft, setBoundsDraft] = createSignal({ x: "", y: "", width: "", height: "" });
  let canvasWidthRef!: HTMLInputElement;
  let canvasHeightRef!: HTMLInputElement;

  createEffect(() => {
    const slot = props.selectedSlot;
    const content = (slot?.content ?? {}) as Record<string, unknown>;
    setTextValue(typeof content.text === "string" ? content.text : "");
    setFillColor(isHexColor(content.fill) ? String(content.fill) : "#ffffff");
    setStrokeColor(isHexColor(content.stroke) ? String(content.stroke) : "#111827");
    const box = bounds();
    setBoundsDraft({
      x: box ? String(formatNumber(box.x)) : "",
      y: box ? String(formatNumber(box.y)) : "",
      width: box ? String(formatNumber(box.width)) : "",
      height: box ? String(formatNumber(box.height)) : "",
    });
  });

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

  function isHexColor(value: unknown): value is string {
    return typeof value === "string" && /^#[0-9a-f]{6}$/i.test(value);
  }

  function isTextLike(slot: LayoutSlot | null): boolean {
    return slot?.kind === "text" || slot?.kind === "text_box";
  }

  function isShapeLike(slot: LayoutSlot | null): boolean {
    return !!slot && ["rect", "circle", "line", "polygon", "path", "text_box"].includes(slot.kind);
  }

  function canEditBounds(slot: LayoutSlot | null): boolean {
    return !!slot && ["rect", "text_box", "image", "text", "circle", "line"].includes(slot.kind);
  }

  function commitBounds(): void {
    if (!canEditBounds(props.selectedSlot)) return;
    const current = bounds();
    if (!current) return;
    const draft = boundsDraft();
    const x = Number(draft.x);
    const y = Number(draft.y);
    const width = Number(draft.width);
    const height = Number(draft.height);
    if (![x, y, width, height].every(Number.isFinite) || width <= 0 || height <= 0) {
      setBoundsDraft({
        x: String(formatNumber(current.x)),
        y: String(formatNumber(current.y)),
        width: String(formatNumber(current.width)),
        height: String(formatNumber(current.height)),
      });
      return;
    }
    if (x === current.x && y === current.y && width === current.width && height === current.height) return;
    void props.store.updateSelectedBounds({ x, y, width, height });
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
              <div class="field-grid slot-bounds-grid">
                <label>
                  X
                  <input
                    type="number"
                    step="0.1"
                    value={boundsDraft().x}
                    disabled={props.store.state.loading || !canEditBounds(slot())}
                    onInput={(event) => setBoundsDraft((draft) => ({ ...draft, x: event.currentTarget.value }))}
                    onKeyDown={commitOnEnter}
                    onBlur={commitBounds}
                  />
                </label>
                <label>
                  Y
                  <input
                    type="number"
                    step="0.1"
                    value={boundsDraft().y}
                    disabled={props.store.state.loading || !canEditBounds(slot())}
                    onInput={(event) => setBoundsDraft((draft) => ({ ...draft, y: event.currentTarget.value }))}
                    onKeyDown={commitOnEnter}
                    onBlur={commitBounds}
                  />
                </label>
                <label>
                  W
                  <input
                    type="number"
                    min="1"
                    step="0.1"
                    value={boundsDraft().width}
                    disabled={props.store.state.loading || !canEditBounds(slot())}
                    onInput={(event) => setBoundsDraft((draft) => ({ ...draft, width: event.currentTarget.value }))}
                    onKeyDown={commitOnEnter}
                    onBlur={commitBounds}
                  />
                </label>
                <label>
                  H
                  <input
                    type="number"
                    min="1"
                    step="0.1"
                    value={boundsDraft().height}
                    disabled={props.store.state.loading || !canEditBounds(slot())}
                    onInput={(event) => setBoundsDraft((draft) => ({ ...draft, height: event.currentTarget.value }))}
                    onKeyDown={commitOnEnter}
                    onBlur={commitBounds}
                  />
                </label>
              </div>
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
      <Show when={isTextLike(props.selectedSlot)}>
        <section class="inspector-section">
          <div class="pane-heading">Text</div>
          <div class="single-field">
            <label>
              Content
              <input
                value={textValue()}
                disabled={props.store.state.loading}
                onInput={(event) => setTextValue(event.currentTarget.value)}
                onKeyDown={(event) => {
                  if (event.key === "Enter") void props.store.updateSelectedText(textValue());
                }}
              />
            </label>
          </div>
          <div class="row mt-8">
            <button type="button" disabled={props.store.state.loading} onClick={() => void props.store.updateSelectedText(textValue())}>
              Update Text
            </button>
          </div>
          <div class="row mt-8">
            <button type="button" disabled={props.store.state.loading} onClick={() => void props.store.nudgeSelectedFontSize(-2)}>
              A-
            </button>
            <button type="button" disabled={props.store.state.loading} onClick={() => void props.store.nudgeSelectedFontSize(2)}>
              A+
            </button>
          </div>
          <div class="row mt-8">
            <button type="button" disabled={props.store.state.loading} onClick={() => void props.store.alignSelectedText("left")}>
              Left
            </button>
            <button type="button" disabled={props.store.state.loading} onClick={() => void props.store.alignSelectedText("center")}>
              Center
            </button>
            <button type="button" disabled={props.store.state.loading} onClick={() => void props.store.alignSelectedText("right")}>
              Right
            </button>
          </div>
        </section>
      </Show>
      <Show when={isShapeLike(props.selectedSlot)}>
        <section class="inspector-section">
          <div class="pane-heading">Shape Format</div>
          <div class="shape-format-row">
            <input class="shape-format-color" type="color" value={fillColor()} disabled={props.store.state.loading || props.selectedSlot?.kind === "line"} onInput={(event) => setFillColor(event.currentTarget.value)} />
            <button type="button" class="shape-format-btn" disabled={props.store.state.loading || props.selectedSlot?.kind === "line"} onClick={() => void props.store.applyShapeFill(fillColor())}>
              Fill
            </button>
          </div>
          <div class="shape-format-row">
            <input class="shape-format-color" type="color" value={strokeColor()} disabled={props.store.state.loading} onInput={(event) => setStrokeColor(event.currentTarget.value)} />
            <button type="button" class="shape-format-btn" disabled={props.store.state.loading} onClick={() => void props.store.applyShapeStroke(strokeColor())}>
              Stroke
            </button>
          </div>
          <div class="shape-format-row wrap-row">
            <button type="button" class="shape-format-btn" disabled={props.store.state.loading} onClick={() => void props.store.applyShapeStroke("none")}>
              No Border
            </button>
            <button type="button" class="shape-format-btn" disabled={props.store.state.loading} onClick={() => void props.store.applyShapeDash("")}>
              Solid
            </button>
            <button type="button" class="shape-format-btn" disabled={props.store.state.loading} onClick={() => void props.store.applyShapeDash("4 3")}>
              Short Dash
            </button>
            <button type="button" class="shape-format-btn" disabled={props.store.state.loading} onClick={() => void props.store.applyShapeDash("10 6")}>
              Dashed
            </button>
            <button type="button" class="shape-format-btn" disabled={props.store.state.loading} onClick={() => void props.store.applyShapeDash("10 4 2 4")}>
              Dot Dash
            </button>
            <button type="button" class="shape-format-btn" disabled={props.store.state.loading} onClick={() => void props.store.applyShapeDash("2 5")}>
              Dotted
            </button>
          </div>
        </section>
      </Show>
    </>
  );
}
