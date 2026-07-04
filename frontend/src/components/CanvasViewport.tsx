import { For, Show, createMemo, createSignal, createEffect } from "solid-js";
import { boxesIntersect, normalizeBox, unionBoxes, type Box, type Point } from "../editor-core/model/geometry";
import {
  matchSlotIdFromSvgElement,
  slotIdFromElement,
  isDraggableSlotElement,
} from "../editor-core/selection/selectionManager";
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

function pointToSegmentDistance(point: Point, a: Point, b: Point): number {
  const dx = b.x - a.x;
  const dy = b.y - a.y;
  const len2 = dx * dx + dy * dy;
  if (!len2) return Math.hypot(point.x - a.x, point.y - a.y);
  const t = Math.max(0, Math.min(1, ((point.x - a.x) * dx + (point.y - a.y) * dy) / len2));
  return Math.hypot(point.x - (a.x + dx * t), point.y - (a.y + dy * t));
}

function pointToBoxDistance(point: Point, box: Box): number {
  const insideX = point.x >= box.x && point.x <= box.x + box.width;
  const insideY = point.y >= box.y && point.y <= box.y + box.height;
  if (insideX && insideY) return 0;
  const cx = Math.max(box.x, Math.min(box.x + box.width, point.x));
  const cy = Math.max(box.y, Math.min(box.y + box.height, point.y));
  return Math.hypot(point.x - cx, point.y - cy);
}

function inflateHitBox(box: Box | null, pad: number): Box | null {
  if (!box) return null;
  return {
    x: box.x - pad,
    y: box.y - pad,
    width: box.width + pad * 2,
    height: box.height + pad * 2,
  };
}

function parsePolygonPoints(raw: string): [number, number][] {
  return (raw || "")
    .trim()
    .split(/\s+/)
    .filter(Boolean)
    .map((pair) => {
      const [x, y] = pair.split(",");
      return [Number(x), Number(y)] as [number, number];
    })
    .filter(([x, y]) => Number.isFinite(x) && Number.isFinite(y));
}

function pathTokens(d: string): string[] {
  return (d || "").match(/[a-zA-Z]|-?\d*\.?\d+(?:e[-+]?\d+)?/g) || [];
}

const PATH_PARAM_COUNTS: Record<string, number> = { M: 2, L: 2, T: 2, H: 1, V: 1, C: 6, S: 4, Q: 4, A: 7 };

function pathAnchorPoints(d: string): Point[] {
  const tokens = pathTokens(d);
  const points: Point[] = [];
  let i = 0;
  let cmd: string | null = null;
  const isCommand = (token: string) => /^[a-zA-Z]$/.test(token);
  const num = (token: string) => Number(token);

  while (i < tokens.length) {
    if (isCommand(tokens[i])) {
      cmd = tokens[i].toUpperCase();
      i += 1;
      if (cmd === "Z") continue;
    }
    if (!cmd) break;
    const count = PATH_PARAM_COUNTS[cmd];
    if (!count || i + count > tokens.length) break;
    const vals = tokens.slice(i, i + count).map(num);
    if (vals.some((v) => !Number.isFinite(v))) break;
    if (cmd === "M" || cmd === "L" || cmd === "T") {
      points.push({ x: vals[0], y: vals[1] });
    } else if (cmd === "H" && points.length) {
      points.push({ x: vals[0], y: points[points.length - 1].y });
    } else if (cmd === "V" && points.length) {
      points.push({ x: points[points.length - 1].x, y: vals[0] });
    } else if (cmd === "C") {
      points.push({ x: vals[4], y: vals[5] });
    } else if (cmd === "S" || cmd === "Q") {
      points.push({ x: vals[vals.length - 2], y: vals[vals.length - 1] });
    } else if (cmd === "A") {
      points.push({ x: vals[5], y: vals[6] });
    }
    i += count;
  }
  return points;
}

function visualSvgBox(node: Element, svg: SVGSVGElement): Box | null {
  try {
    const rect = node.getBoundingClientRect();
    const ctm = svg.getScreenCTM();
    if (!ctm || rect.width <= 0 || rect.height <= 0) return null;
    const point = svg.createSVGPoint();
    const inverse = ctm.inverse();
    const corners = [
      [rect.left, rect.top],
      [rect.right, rect.top],
      [rect.right, rect.bottom],
      [rect.left, rect.bottom],
    ].map(([x, y]) => {
      point.x = x;
      point.y = y;
      return point.matrixTransform(inverse);
    });
    const xs = corners.map((p) => p.x);
    const ys = corners.map((p) => p.y);
    const minX = Math.min(...xs);
    const minY = Math.min(...ys);
    const maxX = Math.max(...xs);
    const maxY = Math.max(...ys);
    return { x: minX, y: minY, width: maxX - minX, height: maxY - minY };
  } catch (_) {
    return null;
  }
}

function elementHitBox(node: Element, svg: SVGSVGElement | null): Box | null {
  const tag = node.tagName.toLowerCase();
  if (tag === "rect" || tag === "image") {
    const x = Number(node.getAttribute("x") || 0);
    const y = Number(node.getAttribute("y") || 0);
    const width = Number(node.getAttribute("width") || 0);
    const height = Number(node.getAttribute("height") || 0);
    return width > 0 && height > 0 ? { x, y, width, height } : null;
  }
  if (tag === "text") {
    try {
      const bb = (node as SVGGraphicsElement).getBBox();
      return bb ? { x: bb.x, y: bb.y, width: bb.width, height: bb.height } : null;
    } catch (_) {
      return null;
    }
  }
  if (tag === "line") {
    if (svg && node.getAttribute("transform")) {
      const vBox = visualSvgBox(node, svg);
      if (vBox) return inflateHitBox(vBox, 8);
    }
    const x1 = Number(node.getAttribute("x1") || 0);
    const y1 = Number(node.getAttribute("y1") || 0);
    const x2 = Number(node.getAttribute("x2") || 0);
    const y2 = Number(node.getAttribute("y2") || 0);
    const strokeWidth = Number(node.getAttribute("stroke-width") || 1);
    const pad = Math.max(8, strokeWidth * 3);
    return {
      x: Math.min(x1, x2) - pad,
      y: Math.min(y1, y2) - pad,
      width: Math.abs(x2 - x1) + pad * 2,
      height: Math.abs(y2 - y1) + pad * 2,
    };
  }
  if (tag === "circle") {
    if (svg && node.getAttribute("transform")) {
      const vBox = visualSvgBox(node, svg);
      if (vBox) return inflateHitBox(vBox, 8);
    }
    const cx = Number(node.getAttribute("cx") || 0);
    const cy = Number(node.getAttribute("cy") || 0);
    const r = Number(node.getAttribute("r") || 0);
    if (!Number.isFinite(cx) || !Number.isFinite(cy) || !Number.isFinite(r)) return null;
    const strokeWidth = Number(node.getAttribute("stroke-width") || 1);
    const pad = Math.max(8, strokeWidth * 3);
    const rr = Math.max(0, r) + pad;
    return { x: cx - rr, y: cy - rr, width: rr * 2, height: rr * 2 };
  }
  try {
    const bb = (node as SVGGraphicsElement).getBBox();
    if (!bb) return null;
    if (tag === "path" || tag === "polygon") {
      if (svg && node.getAttribute("transform")) {
        const vBox = visualSvgBox(node, svg);
        if (vBox) return inflateHitBox(vBox, 8);
      }
      const strokeWidth = Number(node.getAttribute("stroke-width") || 1);
      const pad = Math.max(8, strokeWidth * 3);
      return { x: bb.x - pad, y: bb.y - pad, width: bb.width + pad * 2, height: bb.height + pad * 2 };
    }
    return { x: bb.x, y: bb.y, width: bb.width, height: bb.height };
  } catch (_) {
    return null;
  }
}

function elementVisualBox(node: Element, svg: SVGSVGElement | null): Box | null {
  const tag = node.tagName.toLowerCase();
  if ((tag === "line" || tag === "path" || tag === "polygon" || tag === "circle") && svg && node.getAttribute("transform")) {
    const transformed = visualSvgBox(node, svg);
    if (transformed) return transformed;
  }
  if (tag === "rect" || tag === "image") {
    const x = Number(node.getAttribute("x") || 0);
    const y = Number(node.getAttribute("y") || 0);
    const width = Number(node.getAttribute("width") || 0);
    const height = Number(node.getAttribute("height") || 0);
    return width > 0 && height > 0 ? { x, y, width, height } : null;
  }
  if (tag === "line") {
    const x1 = Number(node.getAttribute("x1") || 0);
    const y1 = Number(node.getAttribute("y1") || 0);
    const x2 = Number(node.getAttribute("x2") || 0);
    const y2 = Number(node.getAttribute("y2") || 0);
    return {
      x: Math.min(x1, x2),
      y: Math.min(y1, y2),
      width: Math.abs(x2 - x1),
      height: Math.abs(y2 - y1),
    };
  }
  if (tag === "circle") {
    const cx = Number(node.getAttribute("cx") || 0);
    const cy = Number(node.getAttribute("cy") || 0);
    const r = Number(node.getAttribute("r") || 0);
    return Number.isFinite(cx) && Number.isFinite(cy) && Number.isFinite(r)
      ? { x: cx - r, y: cy - r, width: r * 2, height: r * 2 }
      : null;
  }
  try {
    const bb = (node as SVGGraphicsElement).getBBox();
    return bb ? { x: bb.x, y: bb.y, width: bb.width, height: bb.height } : null;
  } catch (_) {
    return null;
  }
}

function pointToElementDistance(node: Element, point: Point, box: Box): number {
  const tag = node.tagName.toLowerCase();
  if (node.getAttribute("transform")) return pointToBoxDistance(point, box);
  if (tag === "text") return pointToBoxDistance(point, box);
  if (tag === "line") {
    return pointToSegmentDistance(
      point,
      { x: Number(node.getAttribute("x1") || 0), y: Number(node.getAttribute("y1") || 0) },
      { x: Number(node.getAttribute("x2") || 0), y: Number(node.getAttribute("y2") || 0) }
    );
  }
  if (tag === "circle") {
    const cx = Number(node.getAttribute("cx") || 0);
    const cy = Number(node.getAttribute("cy") || 0);
    const r = Math.max(0, Number(node.getAttribute("r") || 0));
    const fill = String(node.getAttribute("fill") || "").toLowerCase();
    const centerDistance = Math.hypot(point.x - cx, point.y - cy);
    return fill && fill !== "none" ? Math.max(0, centerDistance - r) : Math.abs(centerDistance - r);
  }
  if (tag === "path" || tag === "polygon") {
    const points = tag === "polygon"
      ? parsePolygonPoints(node.getAttribute("points") || "").map(([x, y]) => ({ x, y }))
      : pathAnchorPoints(node.getAttribute("d") || "");
    if (points.length >= 2) {
      let best = Infinity;
      for (let i = 1; i < points.length; i += 1) {
        best = Math.min(best, pointToSegmentDistance(point, points[i - 1], points[i]));
      }
      return best;
    }
  }
  return pointToBoxDistance(point, box);
}

function pickPriority(node: Element): number {
  const tag = node.tagName.toLowerCase();
  if (tag === "text") return 0;
  if (tag === "line" || tag === "path") return 0;
  if (tag === "circle") return 1;
  if (tag === "polygon") return 1;
  if (tag === "image") return 2;
  if (tag === "rect") return 3;
  return 4;
}

export function CanvasViewport(props: CanvasViewportProps) {
  const [interaction, setInteraction] = createSignal<CanvasInteraction | null>(null);
  const [suppressClick, setSuppressClick] = createSignal(false);
  const [inlineTextEdit, setInlineTextEdit] = createSignal<{
    slotId: string;
    originalText: string;
    rect: { left: number; top: number; width: number; height: number; fontSize: number; fontFamily: string };
  } | null>(null);
  let surfaceRef!: HTMLDivElement;

  function handleDoubleClick(event: MouseEvent): void {
    const target = event.target instanceof Element ? event.target : null;
    if (!target) return;
    const svg = target.closest("svg");
    if (!svg) return;
    const el = findDraggableSlotAncestor(target);
    if (!el || el.tagName.toLowerCase() !== "text") return;

    const slotId = slotIdFromElement(
      el,
      props.store.state.document?.detail.layout ?? null,
      props.store.state.document?.detail.renderer ?? null,
      props.store.state.dslDraft
    );
    if (!slotId) return;

    const rect = el.getBoundingClientRect();
    const surface = svg.closest(".canvas-surface");
    const containerRect = surface?.getBoundingClientRect() ?? { left: 0, top: 0 };
    const scale = props.store.state.zoom;
    const fontSize = Number(el.getAttribute("font-size") || 28) * scale;

    setInlineTextEdit({
      slotId,
      originalText: el.textContent || "",
      rect: {
        left: rect.left - containerRect.left - 2,
        top: rect.top - containerRect.top - 2,
        width: Math.max(48, rect.width + 12),
        height: Math.max(24, rect.height + 8),
        fontSize: Math.max(12, fontSize),
        fontFamily: el.getAttribute("font-family") || '"Segoe UI", "Pretendard", sans-serif',
      },
    });

    event.preventDefault();
    event.stopPropagation();
  }

  function findDraggableSlotAncestor(el: Element | null): Element | null {
    let curr = el;
    while (curr && curr.tagName.toLowerCase() !== "svg") {
      if (curr.getAttribute("id") && isDraggableSlotElement(curr)) {
        return curr;
      }
      curr = curr.parentElement;
    }
    return null;
  }

  function draggableSlotElements(svg: SVGSVGElement): Element[] {
    const layout = props.store.state.document?.detail.layout ?? null;
    const renderer = props.store.state.document?.detail.renderer ?? null;
    const dsl = props.store.state.dslDraft;
    return Array.from(svg.querySelectorAll("[id]")).filter(
      (node) => isDraggableSlotElement(node) && slotIdFromElement(node, layout, renderer, dsl)
    );
  }

  function matchingSlotElementAtPoint(svg: SVGSVGElement, clientX: number, clientY: number): Element | null {
    const seen = new Set<Element>();
    const doc = svg.ownerDocument;

    for (const node of doc.elementsFromPoint(clientX, clientY)) {
      if (!(node instanceof SVGElement) || !svg.contains(node)) continue;
      const slotTarget = findDraggableSlotAncestor(node);
      if (!slotTarget || seen.has(slotTarget)) continue;
      seen.add(slotTarget);
      if (matchSelectableSlotId(slotTarget.getAttribute("id"))) return slotTarget;
    }

    const surface = svg.closest(".canvas-surface");
    if (!surface) return null;
    const point = clientPointToCanvasPoint(surface as HTMLElement, clientX, clientY, props.store.state.zoom);
    const nodes = draggableSlotElements(svg);
    const candidates: { node: Element; priority: number; distance: number; area: number; z: number }[] = [];

    for (let i = nodes.length - 1; i >= 0; i -= 1) {
      const node = nodes[i];
      if (node.getAttribute("id")) {
        const sid = slotIdFromElement(
          node,
          props.store.state.document?.detail.layout ?? null,
          props.store.state.document?.detail.renderer ?? null,
          props.store.state.dslDraft
        );
        const slot = props.store.state.document?.slots.find((s) => s.id === sid);
        if (!slot || !matchesPickMode(slot)) continue;
      }
      const bb = elementHitBox(node, svg);
      if (!bb) continue;
      if (point.x >= bb.x && point.x <= bb.x + bb.width && point.y >= bb.y && point.y <= bb.y + bb.height) {
        const area = Math.max(0, bb.width) * Math.max(0, bb.height);
        const distance = pointToElementDistance(node, point, bb);
        candidates.push({ node, priority: pickPriority(node), distance, area, z: i });
      }
    }

    if (candidates.length) {
      candidates.sort((a, b) => a.distance - b.distance || a.priority - b.priority || a.area - b.area || b.z - a.z);
      return candidates[0].node;
    }
    return null;
  }

  createEffect(() => {
    const selectedIds = props.store.state.selectedIds;
    props.store.state.document?.detail.svg;

    const svg = surfaceRef?.querySelector("svg");
    if (!svg) return;

    const elements = draggableSlotElements(svg);
    for (const el of elements) {
      const slotId = slotIdFromElement(
        el,
        props.store.state.document?.detail.layout ?? null,
        props.store.state.document?.detail.renderer ?? null,
        props.store.state.dslDraft
      );
      if (selectedIds.includes(slotId)) {
        el.classList.add("slot-selected");
      } else {
        el.classList.remove("slot-selected");
      }
    }
  });

  function selectedSvgBounds(): Box | null {
    const svg = surfaceRef?.querySelector("svg");
    if (!svg) return null;
    const selected = props.store.state.selectedIds;
    if (!selected.length) return null;
    const boxes = draggableSlotElements(svg)
      .map((el) => {
        const slotId = slotIdFromElement(
          el,
          props.store.state.document?.detail.layout ?? null,
          props.store.state.document?.detail.renderer ?? null,
          props.store.state.dslDraft
        );
        if (!selected.includes(slotId)) return null;
        return elementVisualBox(el, svg);
      })
      .filter((box): box is Box => box !== null);
    return unionBoxes(boxes);
  }

  const selectedBounds = createMemo(() => {
    const svgBounds = selectedSvgBounds();
    if (svgBounds) return svgBounds;
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
    const slotId = hitSlotId(event.target) ?? hitSlotIdFromPoint(event);
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
    if (!element) return null;
    const slotTarget = findDraggableSlotAncestor(element);
    if (slotTarget && matchesPickModeElement(slotTarget)) {
      return slotIdFromElement(
        slotTarget,
        props.store.state.document?.detail.layout ?? null,
        props.store.state.document?.detail.renderer ?? null,
        props.store.state.dslDraft
      );
    }
    return null;
  }

  function hitSlotIdFromPoint(event: MouseEvent | PointerEvent): string | null {
    const surface = event.currentTarget instanceof HTMLElement ? event.currentTarget : null;
    const svg = surface?.querySelector("svg");
    if (!svg) return null;
    const matched = matchingSlotElementAtPoint(svg, event.clientX, event.clientY);
    if (matched) {
      return slotIdFromElement(
        matched,
        props.store.state.document?.detail.layout ?? null,
        props.store.state.document?.detail.renderer ?? null,
        props.store.state.dslDraft
      );
    }
    return null;
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

  function matchesPickModeElement(el: Element): boolean {
    const tag = el.tagName.toLowerCase();
    switch (props.store.state.pickMode) {
      case "text":
        return tag === "text";
      case "shape":
        return tag === "rect" || tag === "circle" || tag === "polygon" || tag === "image";
      case "linepath":
        return tag === "line" || tag === "path";
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
            ref={surfaceRef}
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
            onDblClick={handleDoubleClick}
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
            <Show when={inlineTextEdit()}>
              {(edit) => {
                let inputRef!: HTMLInputElement;
                setTimeout(() => {
                  inputRef?.focus();
                  inputRef?.select();
                }, 20);

                const handleKeyDown = (e: KeyboardEvent) => {
                  if (e.key === "Enter") {
                    e.preventDefault();
                    const text = inputRef.value;
                    if (text !== edit().originalText) {
                      void props.store.updateSlotProperties(edit().slotId, { text });
                    }
                    setInlineTextEdit(null);
                  } else if (e.key === "Escape") {
                    e.preventDefault();
                    setInlineTextEdit(null);
                  }
                };

                return (
                  <input
                    ref={inputRef}
                    type="text"
                    class="inline-text-editor"
                    value={edit().originalText}
                    style={{
                      position: "absolute",
                      left: `${edit().rect.left}px`,
                      top: `${edit().rect.top}px`,
                      width: `${edit().rect.width}px`,
                      height: `${edit().rect.height}px`,
                      "font-size": `${edit().rect.fontSize}px`,
                      "font-family": edit().rect.fontFamily,
                      display: "block",
                      "z-index": 100,
                    }}
                    onKeyDown={handleKeyDown}
                    onBlur={() => {
                      const text = inputRef.value;
                      if (text !== edit().originalText) {
                        void props.store.updateSlotProperties(edit().slotId, { text });
                      }
                      setInlineTextEdit(null);
                    }}
                  />
                );
              }}
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
