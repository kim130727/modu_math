import { For, Show, createMemo, createSignal } from "solid-js";
import { boxesIntersect, normalizeBox, unionBoxes, type Box, type Point } from "../editor-core/model/geometry";
import { matchSlotIdFromSvgElement } from "../editor-core/selection/selectionManager";
import { slotBounds } from "../editor-core/transform/bounds";
import { clientPointToCanvasPoint } from "../editor-core/transform/coordinateTransform";
import type { EditorStore } from "../stores/editorStore";
import type { LayoutSlot } from "../types/layout";
import { LayoutSvgPreview } from "./LayoutSvgPreview";
import { SvgContent } from "./SvgContent";

interface CanvasViewportProps {
  store: EditorStore;
}

type CanvasInteraction =
  | { kind: "marquee"; pointerId: number; start: Point; current: Point; moved: boolean }
  | { kind: "pan"; pointerId: number; startClient: Point; startPan: Point };

const RESIZE_HANDLES = [
  { key: "nw", x: 0, y: 0 },
  { key: "n", x: 0.5, y: 0 },
  { key: "ne", x: 1, y: 0 },
  { key: "e", x: 1, y: 0.5 },
  { key: "se", x: 1, y: 1 },
  { key: "s", x: 0.5, y: 1 },
  { key: "sw", x: 0, y: 1 },
  { key: "w", x: 0, y: 0.5 },
] as const;

export function CanvasViewport(props: CanvasViewportProps) {
  const [interaction, setInteraction] = createSignal<CanvasInteraction | null>(null);
  const [suppressClick, setSuppressClick] = createSignal(false);

  const selectedBounds = createMemo(() => {
    const slots = props.store.state.document?.slots ?? [];
    const selected = slots.filter((slot) => props.store.state.selectedIds.includes(slot.id));
    return unionBoxes(selected.map(slotBounds).filter((box): box is Box => box !== null));
  });

  const canvasWidth = () => props.store.state.document?.detail.layout?.canvas?.width ?? svgDimension("width") ?? 900;
  const canvasHeight = () => props.store.state.document?.detail.layout?.canvas?.height ?? svgDimension("height") ?? 420;

  function svgDimension(attribute: "width" | "height"): number | null {
    const svg = props.store.state.document?.detail.svg;
    const match = svg?.match(new RegExp(`${attribute}="([0-9.]+)"`));
    if (!match) return null;
    const value = Number(match[1]);
    return Number.isFinite(value) ? value : null;
  }

  function selectFromSvg(event: MouseEvent): void {
    if (suppressClick()) {
      event.preventDefault();
      event.stopPropagation();
      setSuppressClick(false);
      return;
    }
    const target = event.target instanceof Element ? event.target : null;
    const svgElement = target?.closest("[id]");
    const slotId = matchSelectableSlotId(svgElement?.getAttribute("id") ?? null) ?? hitSlotIdFromPoint(event);
    if (!slotId) {
      props.store.clearSelectedSlots();
      return;
    }
    props.store.selectSlot(slotId, event.shiftKey || event.ctrlKey || event.metaKey);
  }

  const marqueeBox = createMemo(() => {
    const current = interaction();
    return current?.kind === "marquee" ? normalizeBox(current.start, current.current) : null;
  });

  function hitSlotId(target: EventTarget | null): string | null {
    const element = target instanceof Element ? target : null;
    const svgElement = element?.closest("[id]");
    return matchSelectableSlotId(svgElement?.getAttribute("id") ?? null);
  }

  function hitSlotIdFromPoint(event: MouseEvent | PointerEvent): string | null {
    const surface = event.currentTarget instanceof HTMLElement ? event.currentTarget : null;
    if (!surface) return null;
    const point = clientPointToCanvasPoint(surface, event.clientX, event.clientY, props.store.state.zoom);
    const slots = props.store.state.document?.slots ?? [];
    const matchingSlot = [...slots]
      .reverse()
      .filter((slot) => matchesPickMode(slot))
      .find((slot) => {
        const bounds = slotBounds(slot);
        return bounds ? boxesIntersect({ x: point.x, y: point.y, width: 1, height: 1 }, bounds) : false;
      });
    return matchingSlot?.id ?? null;
  }

  function matchSelectableSlotId(elementId: string | null): string | null {
    const slots = props.store.state.document?.slots ?? [];
    const slotId = matchSlotIdFromSvgElement(
      elementId,
      slots.filter((slot) => matchesPickMode(slot)).map((slot) => slot.id),
    );
    return slotId;
  }

  function matchesPickMode(slot: LayoutSlot): boolean {
    switch (props.store.state.pickMode) {
      case "text":
        return slot.kind === "text" || slot.kind === "text_box";
      case "shape":
        return slot.kind === "rect" || slot.kind === "circle" || slot.kind === "polygon" || slot.kind === "image";
      case "linepath":
        return slot.kind === "line" || slot.kind === "path";
      case "all":
        return true;
    }
  }

  function beginCanvasPointer(event: PointerEvent): void {
    if (!props.store.state.document) return;
    const shouldPan = props.store.state.activeTool === "pan" || event.button === 1 || event.altKey;
    const surface = event.currentTarget instanceof HTMLElement ? event.currentTarget : null;
    if (!surface) return;

    if (shouldPan) {
      event.preventDefault();
      surface.setPointerCapture(event.pointerId);
      setInteraction({
        kind: "pan",
        pointerId: event.pointerId,
        startClient: { x: event.clientX, y: event.clientY },
        startPan: { x: props.store.state.panX, y: props.store.state.panY },
      });
      return;
    }

    if (event.button !== 0 || hitSlotId(event.target) || hitSlotIdFromPoint(event)) return;
    event.preventDefault();
    surface.setPointerCapture(event.pointerId);
    const start = clientPointToCanvasPoint(surface, event.clientX, event.clientY, props.store.state.zoom);
    setInteraction({ kind: "marquee", pointerId: event.pointerId, start, current: start, moved: false });
  }

  function updateCanvasPointer(event: PointerEvent): void {
    const current = interaction();
    if (!current || current.pointerId !== event.pointerId) return;
    const surface = event.currentTarget instanceof HTMLElement ? event.currentTarget : null;
    if (!surface) return;

    if (current.kind === "pan") {
      props.store.setPan(current.startPan.x + event.clientX - current.startClient.x, current.startPan.y + event.clientY - current.startClient.y);
      return;
    }

    const point = clientPointToCanvasPoint(surface, event.clientX, event.clientY, props.store.state.zoom);
    const moved = current.moved || Math.abs(point.x - current.start.x) > 3 || Math.abs(point.y - current.start.y) > 3;
    setInteraction({ ...current, current: point, moved });
  }

  function finishCanvasPointer(event: PointerEvent): void {
    const current = interaction();
    if (!current || current.pointerId !== event.pointerId) return;
    const surface = event.currentTarget instanceof HTMLElement ? event.currentTarget : null;
    surface?.releasePointerCapture(event.pointerId);

    if (current.kind === "marquee" && current.moved) {
      const box = normalizeBox(current.start, current.current);
      const selectedIds = (props.store.state.document?.slots ?? [])
        .filter((slot) => matchesPickMode(slot))
        .filter((slot) => {
          const bounds = slotBounds(slot);
          return bounds ? boxesIntersect(box, bounds) : false;
        })
        .map((slot) => slot.id);
      props.store.setSelectedSlots(selectedIds);
      setSuppressClick(true);
    }
    setInteraction(null);
  }

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
      <div class="canvas-controls" aria-label="Canvas zoom controls">
        <button type="button" onClick={() => props.store.setZoom(props.store.state.zoom - 0.1)} disabled={!props.store.state.document}>
          -
        </button>
        <span>{Math.round(props.store.state.zoom * 100)}%</span>
        <button type="button" onClick={() => props.store.setZoom(props.store.state.zoom + 0.1)} disabled={!props.store.state.document}>
          +
        </button>
        <button type="button" onClick={() => props.store.resetViewport()} disabled={!props.store.state.document}>
          Reset
        </button>
      </div>
      <div class="canvas-viewport">
        <Show
          when={props.store.state.document?.detail.layout ?? props.store.state.document?.detail.svg}
          fallback={<div class="empty-state">Select a problem with SVG output.</div>}
        >
          <div
            class="canvas-surface"
            classList={{
              "is-panning": interaction()?.kind === "pan",
              "pan-tool": props.store.state.activeTool === "pan",
            }}
            style={{
              width: `${canvasWidth()}px`,
              height: `${canvasHeight()}px`,
              transform: `translate(${props.store.state.panX}px, ${props.store.state.panY}px) scale(${props.store.state.zoom})`,
            }}
            onPointerDown={beginCanvasPointer}
            onPointerMove={updateCanvasPointer}
            onPointerUp={finishCanvasPointer}
            onPointerCancel={finishCanvasPointer}
            onClick={selectFromSvg}
          >
            {props.store.state.document?.detail.layout ? (
              <LayoutSvgPreview layout={props.store.state.document.detail.layout} />
            ) : (
              <SvgContent svg={props.store.state.document?.detail.svg ?? ""} />
            )}
            <Show when={marqueeBox()}>
              {(box) => (
                <div
                  class="marquee-box"
                  style={{
                    left: `${box().x}px`,
                    top: `${box().y}px`,
                    width: `${box().width}px`,
                    height: `${box().height}px`,
                  }}
                />
              )}
            </Show>
            <Show when={selectedBounds()}>
              {(box) => (
                <>
                  <div
                    class="selection-box"
                    style={{
                      left: `${box().x}px`,
                      top: `${box().y}px`,
                      width: `${box().width}px`,
                      height: `${box().height}px`,
                    }}
                  />
                  <For each={RESIZE_HANDLES}>
                    {(handle) => (
                      <div
                        class={`resize-handle resize-handle-${handle.key}`}
                        aria-hidden="true"
                        style={{
                          left: `${box().x + box().width * handle.x}px`,
                          top: `${box().y + box().height * handle.y}px`,
                        }}
                      />
                    )}
                  </For>
                </>
              )}
            </Show>
          </div>
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
                props.store.selectSlot(slot.id, event.shiftKey || event.ctrlKey || event.metaKey);
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
