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
  | { kind: "pan"; pointerId: number; startClient: Point; startPan: Point }
  | { kind: "drag"; pointerId: number; start: Point; current: Point; selectedIds: string[]; moved: boolean }
  | { kind: "resize"; pointerId: number; start: Point; current: Point; handle: ResizeHandleKey; slotId: string; startBox: Box; moved: boolean };

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
type ResizeHandleKey = (typeof RESIZE_HANDLES)[number]["key"];

const MIN_RESIZE_SIZE = 4;
const SNAP_SIZE = 5;

export function CanvasViewport(props: CanvasViewportProps) {
  const [interaction, setInteraction] = createSignal<CanvasInteraction | null>(null);
  const [suppressClick, setSuppressClick] = createSignal(false);

  const selectedBounds = createMemo(() => {
    const slots = props.store.state.document?.slots ?? [];
    const selected = slots.filter((slot) => props.store.state.selectedIds.includes(slot.id));
    return unionBoxes(selected.map(slotBounds).filter((box): box is Box => box !== null));
  });

  const overlayBounds = createMemo(() => {
    const current = interaction();
    if (current?.kind === "resize") {
      return resizeBoxFromHandle(current.handle, current.startBox, snappedPoint(current.current));
    }
    return selectedBounds();
  });

  const dragOffset = createMemo(() => {
    const current = interaction();
    if (current?.kind !== "drag") return { x: 0, y: 0 };
    return snappedDelta(current.start, current.current);
  });

  const canvasWidth = () => svgDimension("width") ?? props.store.state.document?.detail.layout?.canvas?.width ?? 900;
  const canvasHeight = () => svgDimension("height") ?? props.store.state.document?.detail.layout?.canvas?.height ?? 420;

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

    if (event.button !== 0) return;

    const slotId = hitSlotId(event.target) ?? hitSlotIdFromPoint(event);
    if (slotId && props.store.state.activeTool === "select") {
      event.preventDefault();
      surface.setPointerCapture(event.pointerId);
      const append = event.shiftKey || event.ctrlKey || event.metaKey;
      const wasSelected = props.store.state.selectedIds.includes(slotId);
      const selectedIds = append
        ? wasSelected
          ? props.store.state.selectedIds.filter((id) => id !== slotId)
          : [...props.store.state.selectedIds, slotId]
        : wasSelected
          ? props.store.state.selectedIds
          : [slotId];
      if (!wasSelected || append) {
        props.store.selectSlot(slotId, append);
      }
      const start = clientPointToCanvasPoint(surface, event.clientX, event.clientY, props.store.state.zoom);
      setInteraction({ kind: "drag", pointerId: event.pointerId, start, current: start, selectedIds, moved: false });
      return;
    }
    if (slotId) return;

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
    if (current.kind === "drag" && current.moved) {
      const { x: dx, y: dy } = snappedDelta(current.start, current.current);
      if (dx !== 0 || dy !== 0) {
        void props.store.moveSlots(current.selectedIds, dx, dy, "Drag move");
      }
      setSuppressClick(true);
    }
    if (current.kind === "resize" && current.moved) {
      const slot = props.store.state.document?.slots.find((candidate) => candidate.id === current.slotId);
      const nextBox = resizeBoxFromHandle(current.handle, current.startBox, snappedPoint(current.current));
      const properties = slot ? resizePropertiesForSlot(slot, nextBox) : null;
      if (properties) {
        void props.store.updateSlotProperties(current.slotId, properties);
      }
      setSuppressClick(true);
    }
    setInteraction(null);
  }

  function roundedDelta(value: number): number {
    return Math.round(value * 100) / 100;
  }

  function snappedDelta(start: Point, current: Point): Point {
    const dx = current.x - start.x;
    const dy = current.y - start.y;
    if (!props.store.state.snapEnabled) return { x: roundedDelta(dx), y: roundedDelta(dy) };
    return { x: snapNumber(dx), y: snapNumber(dy) };
  }

  function snappedPoint(point: Point): Point {
    if (!props.store.state.snapEnabled) return { x: roundedDelta(point.x), y: roundedDelta(point.y) };
    return { x: snapNumber(point.x), y: snapNumber(point.y) };
  }

  function snapNumber(value: number): number {
    return Math.round(value / SNAP_SIZE) * SNAP_SIZE;
  }

  function beginResize(handle: ResizeHandleKey, event: PointerEvent): void {
    event.preventDefault();
    event.stopPropagation();
    if (props.store.state.selectedIds.length !== 1 || props.store.state.loading) return;
    const slotId = props.store.state.selectedIds[0];
    const slot = props.store.state.document?.slots.find((candidate) => candidate.id === slotId);
    const startBox = slot ? slotBounds(slot) : null;
    if (!slot || !startBox || !resizePropertiesForSlot(slot, startBox)) return;
    const surface = event.currentTarget instanceof HTMLElement ? event.currentTarget.closest<HTMLElement>(".canvas-surface") : null;
    if (!surface) return;
    surface.setPointerCapture(event.pointerId);
    const start = clientPointToCanvasPoint(surface, event.clientX, event.clientY, props.store.state.zoom);
    setInteraction({ kind: "resize", pointerId: event.pointerId, start, current: start, handle, slotId, startBox, moved: false });
  }

  function resizeBoxFromHandle(handle: ResizeHandleKey, startBox: Box, current: Point): Box {
    let left = startBox.x;
    let right = startBox.x + startBox.width;
    let top = startBox.y;
    let bottom = startBox.y + startBox.height;

    if (handle.includes("w")) left = current.x;
    if (handle.includes("e")) right = current.x;
    if (handle.includes("n")) top = current.y;
    if (handle.includes("s")) bottom = current.y;

    if (right - left < MIN_RESIZE_SIZE) {
      if (handle.includes("w")) left = right - MIN_RESIZE_SIZE;
      else right = left + MIN_RESIZE_SIZE;
    }
    if (bottom - top < MIN_RESIZE_SIZE) {
      if (handle.includes("n")) top = bottom - MIN_RESIZE_SIZE;
      else bottom = top + MIN_RESIZE_SIZE;
    }

    return {
      x: roundedDelta(left),
      y: roundedDelta(top),
      width: roundedDelta(right - left),
      height: roundedDelta(bottom - top),
    };
  }

  function resizePropertiesForSlot(slot: LayoutSlot, box: Box): Record<string, number> | null {
    switch (slot.kind) {
      case "rect":
      case "text_box":
      case "image":
        return {
          x: box.x,
          y: box.y,
          width: box.width,
          height: box.height,
        };
      case "circle": {
        const diameter = Math.max(box.width, box.height);
        return {
          cx: roundedDelta(box.x + box.width / 2),
          cy: roundedDelta(box.y + box.height / 2),
          r: roundedDelta(diameter / 2),
        };
      }
      default:
        return null;
    }
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
          when={props.store.state.document?.detail.svg ?? props.store.state.document?.detail.layout}
          fallback={<div class="empty-state">Select a problem with SVG output.</div>}
        >
          <div
            class="canvas-surface"
            classList={{
              "is-panning": interaction()?.kind === "pan",
              "is-dragging": interaction()?.kind === "drag",
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
            {props.store.state.document?.detail.svg ? (
              <SvgContent svg={props.store.state.document?.detail.svg ?? ""} />
            ) : props.store.state.document?.detail.layout ? (
              <LayoutSvgPreview layout={props.store.state.document.detail.layout} />
            ) : (
              <div class="empty-state">No SVG or layout output.</div>
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
            <Show when={overlayBounds()}>
              {(box) => (
                <>
                  <div
                    class="selection-box"
                    style={{
                      left: `${box().x + dragOffset().x}px`,
                      top: `${box().y + dragOffset().y}px`,
                      width: `${box().width}px`,
                      height: `${box().height}px`,
                    }}
                  />
                  <For each={RESIZE_HANDLES}>
                    {(handle) => (
                      <div
                        class={`resize-handle resize-handle-${handle.key}`}
                        aria-hidden="true"
                        onPointerDown={(event) => beginResize(handle.key, event)}
                        style={{
                          left: `${box().x + box().width * handle.x + dragOffset().x}px`,
                          top: `${box().y + box().height * handle.y + dragOffset().y}px`,
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
