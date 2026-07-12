import { For, Show, createMemo, createSignal, createEffect, onCleanup, onMount } from "solid-js";
import { boxesIntersect, normalizeBox, unionBoxes, type Box, type Point } from "../editor-core/model/geometry";
import {
  matchSlotIdFromSvgElement,
  slotIdFromElement,
  isDraggableSlotElement,
} from "../editor-core/selection/selectionManager";
import { slotBounds } from "../editor-core/transform/bounds";
import { SvgEditEngine, type SvgPathEditPoint } from "../editor-core/svg-engine/svgEditEngine";
import { clientPointToCanvasPoint } from "../editor-core/transform/coordinateTransform";
import type { EditorStore, TableDividerAxis } from "../stores/editorStore";
import type { LayoutSlot } from "../types/layout";
import { LayoutSvgPreview } from "./LayoutSvgPreview";
import { SvgContent } from "./SvgContent";

interface CanvasViewportProps {
  store: EditorStore;
}

type CanvasInteraction =
  | { kind: "marquee"; pointerId: number; start: Point; current: Point; moved: boolean }
  | { kind: "pan"; pointerId: number; startClient: Point; startPan: Point }
  | { kind: "draw"; pointerId: number; start: Point; current: Point; points: Point[]; moved: boolean }
  | { kind: "table-divider"; pointerId: number; start: Point; current: Point; base: string; axis: TableDividerAxis; index: number; moved: boolean };

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
      points.push({ x: vals[0], y: vals[1] }, { x: vals[2], y: vals[3] }, { x: vals[4], y: vals[5] });
    } else if (cmd === "S" || cmd === "Q") {
      points.push({ x: vals[0], y: vals[1] }, { x: vals[2], y: vals[3] });
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

interface EditablePathPoint extends Point {
  index: number;
  xToken: number;
  yToken: number;
}

function editablePathPoints(d: string): EditablePathPoint[] {
  const tokens = pathTokens(d);
  const points: EditablePathPoint[] = [];
  let i = 0;
  let cmd = "";
  let pointIndex = 0;
  const isCommand = (token: string) => /^[a-zA-Z]$/.test(token);
  const num = (token: string) => Number(token);
  const addPoint = (xToken: number, yToken: number) => {
    const x = num(tokens[xToken]);
    const y = num(tokens[yToken]);
    if (Number.isFinite(x) && Number.isFinite(y)) points.push({ index: pointIndex, xToken, yToken, x, y });
    pointIndex += 1;
  };

  while (i < tokens.length) {
    if (isCommand(tokens[i])) {
      cmd = tokens[i];
      i += 1;
      if (cmd.toUpperCase() === "Z") continue;
    }
    const upper = cmd.toUpperCase();
    const relative = cmd !== upper;
    if (relative) {
      const count = PATH_PARAM_COUNTS[upper];
      if (!count) break;
      while (i < tokens.length && !isCommand(tokens[i])) i += count;
      continue;
    }
    if (upper === "M" || upper === "L" || upper === "T") {
      while (i + 1 < tokens.length && !isCommand(tokens[i])) {
        addPoint(i, i + 1);
        i += 2;
      }
    } else if (upper === "C") {
      while (i + 5 < tokens.length && !isCommand(tokens[i])) {
        addPoint(i, i + 1);
        addPoint(i + 2, i + 3);
        addPoint(i + 4, i + 5);
        i += 6;
      }
    } else if (upper === "S" || upper === "Q") {
      while (i + 3 < tokens.length && !isCommand(tokens[i])) {
        addPoint(i, i + 1);
        addPoint(i + 2, i + 3);
        i += 4;
      }
    } else if (upper === "A") {
      while (i + 6 < tokens.length && !isCommand(tokens[i])) {
        addPoint(i + 5, i + 6);
        i += 7;
      }
    } else {
      const count = PATH_PARAM_COUNTS[upper];
      if (!count) break;
      while (i < tokens.length && !isCommand(tokens[i])) i += count;
    }
  }
  return points;
}

function updateEditablePathPoint(d: string, pointIndex: number, point: Point): string | null {
  const tokens = pathTokens(d);
  const editable = editablePathPoints(d).find((candidate) => candidate.index === pointIndex);
  if (!editable) return null;
  tokens[editable.xToken] = String(Math.round(point.x * 100) / 100);
  tokens[editable.yToken] = String(Math.round(point.y * 100) / 100);
  return tokens.join(" ");
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

const SHAPE_FILL_SWATCHES = ["#ffffff", "#f8fafc", "#fef3c7", "#fed7aa", "#fecaca", "#bfdbfe", "#bbf7d0", "#ddd6fe", "#111827", "#6b7280", "#dc2626", "#2563eb", "#16a34a", "#7c3aed", "#f59e0b", "none"];

export function CanvasViewport(props: CanvasViewportProps) {
  const [interaction, setInteraction] = createSignal<CanvasInteraction | null>(null);
  const [suppressClick, setSuppressClick] = createSignal(false);
  const [slotStripOpen, setSlotStripOpen] = createSignal(false);
  const [shapeFormatMenu, setShapeFormatMenu] = createSignal<{ x: number; y: number; slotId: string; kind: LayoutSlot["kind"]; tableCell: boolean } | null>(null);
  const [selectedSvgElements, setSelectedSvgElements] = createSignal<Element[]>([]);
  const [inlineTextEdit, setInlineTextEdit] = createSignal<{
    slotId: string;
    originalText: string;
    rect: { left: number; top: number; width: number; height: number; fontSize: number; fontFamily: string };
  } | null>(null);
  let surfaceRef!: HTMLDivElement;
  let inlineInputRef: HTMLInputElement | undefined;
  let lastDeleteRequestAt = 0;
  let transformedDragElements: SVGElement[] = [];
  let svgEditEngine: SvgEditEngine | null = null;

  onMount(() => {
    const handleNativeDeletePointer = (event: PointerEvent | MouseEvent) => {
      const target = event.target instanceof Element ? event.target : null;
      if (!target?.closest(".selection-delete-button")) return;
      requestDeleteSelected(event);
    };
    const handleNativeDeleteKey = (event: KeyboardEvent) => {
      if (event.key !== "Delete" && event.key !== "Backspace") return;
      const target = event.target instanceof HTMLElement ? event.target : null;
      if (target) {
        const tagName = target.tagName.toLowerCase();
        if (tagName === "input" || tagName === "textarea" || tagName === "select" || target.isContentEditable) return;
      }
      if (!props.store.state.selectedIds.length) return;
      requestDeleteSelected(event);
    };
    document.addEventListener("pointerdown", handleNativeDeletePointer, true);
    document.addEventListener("mousedown", handleNativeDeletePointer, true);
    document.addEventListener("click", handleNativeDeletePointer, true);
    document.addEventListener("keydown", handleNativeDeleteKey, true);
    onCleanup(() => {
      document.removeEventListener("pointerdown", handleNativeDeletePointer, true);
      document.removeEventListener("mousedown", handleNativeDeletePointer, true);
      document.removeEventListener("click", handleNativeDeletePointer, true);
      document.removeEventListener("keydown", handleNativeDeleteKey, true);
    });
  });

  createEffect(() => {
    if (!inlineTextEdit()) return;
    const handleOutsidePointerDown = (event: PointerEvent) => {
      const target = event.target instanceof Node ? event.target : null;
      if (target && inlineInputRef?.contains(target)) return;
      closeInlineTextEditor(true);
    };
    document.addEventListener("pointerdown", handleOutsidePointerDown, true);
    onCleanup(() => document.removeEventListener("pointerdown", handleOutsidePointerDown, true));
  });

  function handleDoubleClick(event: MouseEvent): void {
    const target = event.target instanceof Element ? event.target : null;
    const slotId = target ? textSlotIdFromEventTarget(target, event.clientX, event.clientY) : null;
    if (!slotId) return;
    openInlineTextEditor(slotId, target);

    event.preventDefault();
    event.stopPropagation();
  }

  function textSlotIdFromEventTarget(target: Element, clientX: number, clientY: number): string | null {
    const el = findDraggableSlotAncestor(target);
    if (el?.tagName.toLowerCase() === "text") {
      const slotId = slotIdFromElement(
        el,
        props.store.state.document?.detail.layout ?? null,
        props.store.state.document?.detail.renderer ?? null,
        props.store.state.dslDraft
      );
      const slot = slotId ? props.store.state.document?.slots.find((candidate) => candidate.id === slotId) : null;
      if (slot?.kind === "text" || slot?.kind === "text_box") return slotId;
    }
    const surface = target.closest<HTMLElement>(".canvas-surface");
    const svg = surface?.querySelector("svg");
    if (!svg) return null;
    const matched = matchingSlotElementAtPoint(svg, clientX, clientY);
    if (!matched) return null;
    const slotId = slotIdFromElement(
      matched,
      props.store.state.document?.detail.layout ?? null,
      props.store.state.document?.detail.renderer ?? null,
      props.store.state.dslDraft
    );
    const slot = slotId ? props.store.state.document?.slots.find((candidate) => candidate.id === slotId) : null;
    return slot?.kind === "text" || slot?.kind === "text_box" ? slotId : null;
  }

  function openInlineTextEditor(slotId: string, element: Element | null): boolean {
    const slot = props.store.state.document?.slots.find((candidate) => candidate.id === slotId);
    if (!slot || (slot.kind !== "text" && slot.kind !== "text_box")) return false;
    const targetElement = element ? findDraggableSlotAncestor(element) : null;
    const textElement = targetElement?.tagName.toLowerCase() === "text" ? targetElement : textElementForSlotId(slotId, surfaceRef);
    if (!textElement) return false;

    const rect = textElement.getBoundingClientRect();
    const surface = textElement.closest(".canvas-surface");
    const containerRect = surface?.getBoundingClientRect() ?? { left: 0, top: 0 };
    const scale = props.store.state.zoom;
    const fontSize = Number(textElement.getAttribute("font-size") || slot.content.font_size || 28) * scale;

    setInlineTextEdit({
      slotId,
      originalText: textElement.textContent || String(slot.content.text ?? ""),
      rect: {
        left: rect.left - containerRect.left - 2,
        top: rect.top - containerRect.top - 2,
        width: Math.max(48, rect.width + 12),
        height: Math.max(24, rect.height + 8),
        fontSize: Math.max(12, fontSize),
        fontFamily: textElement.getAttribute("font-family") || '"Segoe UI", "Pretendard", sans-serif',
      },
    });
    props.store.setStatusMessage(`Editing ${slotId}.`);
    return true;
  }

  function closeInlineTextEditor(save: boolean): void {
    const edit = inlineTextEdit();
    if (!edit) return;
    const text = inlineInputRef?.value ?? edit.originalText;
    setInlineTextEdit(null);
    inlineInputRef = undefined;
    if (save && text !== edit.originalText) {
      void props.store.updateSlotProperties(edit.slotId, { text });
    }
  }

  function textElementForSlotId(slotId: string, surface: HTMLElement | null): Element | null {
    const svg = surface?.querySelector("svg");
    if (!svg) return null;
    for (const node of draggableSlotElements(svg)) {
      if (node.tagName.toLowerCase() !== "text") continue;
      const matched = slotIdFromElement(
        node,
        props.store.state.document?.detail.layout ?? null,
        props.store.state.document?.detail.renderer ?? null,
        props.store.state.dslDraft
      );
      if (matched === slotId) return node;
    }
    return null;
  }

  function requestDeleteSelected(event: Event): void {
    event.preventDefault();
    event.stopPropagation();
    const now = performance.now();
    if (now - lastDeleteRequestAt < 250) return;
    lastDeleteRequestAt = now;
    void props.store.deleteSelectedSlots();
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
    const pickMode = props.store.state.pickMode;
    props.store.state.document?.detail.svg;

    const svg = surfaceRef?.querySelector("svg");
    if (!svg) return;

    const elements = draggableSlotElements(svg);
    const nextSelectedElements: Element[] = [];
    for (const el of elements) {
      const slotId = slotIdFromElement(
        el,
        props.store.state.document?.detail.layout ?? null,
        props.store.state.document?.detail.renderer ?? null,
        props.store.state.dslDraft
      );
      if (selectedIds.includes(slotId)) {
        el.classList.add("slot-selected");
        nextSelectedElements.push(el);
      } else {
        el.classList.remove("slot-selected");
      }
      const slot = props.store.state.document?.slots.find((candidate) => candidate.id === slotId);
      if (slot && pickMode !== "all" && !matchesPickMode(slot)) {
        el.classList.add("pick-disabled");
      } else {
        el.classList.remove("pick-disabled");
      }
    }
    setSelectedSvgElements(nextSelectedElements);
  });

  createEffect(() => {
    props.store.state.document?.detail.svg;
    props.store.state.zoom;
    props.store.state.selectedIds.join("|");
    const current = interaction();
    if (current?.kind === "draw" || current?.kind === "pan" || current?.kind === "marquee") {
      removeSvgEditEngine();
      return;
    }
    syncSvgEditEngine();
  });

  onCleanup(() => removeSvgEditEngine());

  function removeSvgEditEngine(): void {
    svgEditEngine?.destroy();
    svgEditEngine = null;
  }

  function syncSvgEditEngine(): void {
    const svg = surfaceRef?.querySelector("svg");
    if (!svg || props.store.state.activeTool !== "select") {
      removeSvgEditEngine();
      return;
    }
    if (!svgEditEngine) {
      svgEditEngine = new SvgEditEngine(svg, {
        getSelectionBox: () => {
          const selected = props.store.state.selectedIds.filter((slotId) => slotId !== "__canvas__");
          return selectedSvgBoundsForIds(selected) ?? slotBoundsForIds(selected);
        },
        getSelectedIds: () => [...props.store.state.selectedIds],
        canResizeSelection: () => {
          if (props.store.state.selectedIds.length !== 1) return false;
          const slot = props.store.state.document?.slots.find((candidate) => candidate.id === props.store.state.selectedIds[0]);
          return !!slot && ["rect", "circle", "line", "image", "text_box"].includes(slot.kind);
        },
        getPointEditableElement: () => pointEditableSvgElement(),
        commitPointEdit: (slotId, element) => {
          const patch = pointEditPatchFromElement(element);
          if (patch) void props.store.updateSlotProperties(slotId, patch);
        },
        getPathEditPoints: () => pathEditPointsForEngine(),
        commitPathPoint: (slotId, pointIndex, x, y) => {
          const slot = props.store.state.document?.slots.find((candidate) => candidate.id === slotId);
          const content = slot?.content as Record<string, unknown> | undefined;
          const d = typeof content?.d === "string" ? content.d : "";
          const next = updateEditablePathPoint(d, pointIndex, { x, y });
          if (next) void props.store.updateSlotProperties(slotId, { d: next });
        },
        previewMove: applyEngineDragPreview,
        clearPreview: clearEngineDragPreview,
        commitMove: (slotIds, dx, dy) => {
          void props.store.moveSlots(slotIds, dx, dy, "SVG move");
        },
        commitResize: (box) => {
          void props.store.updateSelectedBounds(box);
        },
      });
    }
    svgEditEngine.sync();
  }

  function applyEngineDragPreview(dx: number, dy: number): void {
    const elements = selectedSvgElements().filter((el): el is SVGElement => el instanceof SVGElement);
    transformedDragElements = elements;
    for (const el of elements) {
      if (!(el instanceof SVGElement)) continue;
      el.style.transform = `translate(${roundedDelta(dx)}px, ${roundedDelta(dy)}px)`;
      el.style.transformBox = "fill-box";
      el.style.transformOrigin = "0 0";
    }
  }

  function clearEngineDragPreview(): void {
    const elements = transformedDragElements.length ? transformedDragElements : selectedSvgElements();
    for (const el of elements) {
      if (!(el instanceof SVGElement)) continue;
      el.style.transform = "";
      el.style.transformBox = "";
      el.style.transformOrigin = "";
    }
    transformedDragElements = [];
  }

  function pointEditableSvgElement(): SVGElement | null {
    if (props.store.state.selectedIds.length !== 1) return null;
    const slotId = props.store.state.selectedIds[0];
    const slot = props.store.state.document?.slots.find((candidate) => candidate.id === slotId);
    if (!slot || (slot.kind !== "polygon" && slot.kind !== "line")) return null;
    const svg = surfaceRef?.querySelector("svg");
    if (!svg) return null;
    for (const node of draggableSlotElements(svg)) {
      if (!(node instanceof SVGElement)) continue;
      const matched = slotIdFromElement(
        node,
        props.store.state.document?.detail.layout ?? null,
        props.store.state.document?.detail.renderer ?? null,
        props.store.state.dslDraft,
      );
      if (matched === slotId) return node;
    }
    return null;
  }

  function pathEditPointsForEngine(): { slotId: string; points: SvgPathEditPoint[] } | null {
    if (props.store.state.selectedIds.length !== 1) return null;
    const slotId = props.store.state.selectedIds[0];
    const slot = props.store.state.document?.slots.find((candidate) => candidate.id === slotId);
    const content = slot?.content as Record<string, unknown> | undefined;
    const d = typeof content?.d === "string" ? content.d : "";
    if (!slot || slot.kind !== "path" || !d || typeof content?.transform === "string") return null;
    const points = editablePathPoints(d).map((point) => ({ index: point.index, x: point.x, y: point.y }));
    return points.length ? { slotId, points } : null;
  }

  function pointEditPatchFromElement(element: SVGElement): Record<string, unknown> | null {
    const tag = element.tagName.toLowerCase();
    if (tag === "line") {
      const x1 = Number(element.getAttribute("x1"));
      const y1 = Number(element.getAttribute("y1"));
      const x2 = Number(element.getAttribute("x2"));
      const y2 = Number(element.getAttribute("y2"));
      return [x1, y1, x2, y2].every(Number.isFinite) ? { x1, y1, x2, y2 } : null;
    }
    if (tag === "polygon" || tag === "polyline") {
      const points = parsePolygonPoints(element.getAttribute("points") ?? "");
      return points.length ? { points } : null;
    }
    return null;
  }

  function selectedSvgBoundsForIds(selected: string[]): Box | null {
    const svg = surfaceRef?.querySelector("svg");
    if (!svg) return null;
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

  function slotBoundsForIds(selectedIds: string[]): Box | null {
    const slots = props.store.state.document?.slots ?? [];
    const selected = slots.filter((slot) => selectedIds.includes(slot.id));
    return unionBoxes(selected.map(slotBounds).filter((box): box is Box => box !== null));
  }

  const selectedBounds = createMemo(() => {
    const svgBounds = selectedSvgBoundsForIds(props.store.state.selectedIds);
    if (svgBounds) return svgBounds;
    return slotBoundsForIds(props.store.state.selectedIds);
  });

  const overlayBounds = createMemo(() => {
    return selectedBounds();
  });

  const canvasWidth = () => svgDimension("width") ?? props.store.state.document?.detail.layout?.canvas?.width ?? 900;
  const canvasHeight = () => svgDimension("height") ?? props.store.state.document?.detail.layout?.canvas?.height ?? 420;
  const isCanvasSelected = () => props.store.state.selectedIds.length === 1 && props.store.state.selectedIds[0] === "__canvas__";

  function svgDimension(attribute: "width" | "height"): number | null {
    const svg = props.store.state.document?.detail.svg;
    const match = svg?.match(new RegExp(`${attribute}="([0-9.]+)"`));
    if (!match) return null;
    const value = Number(match[1]);
    return Number.isFinite(value) ? value : null;
  }

  function selectFromSvg(event: MouseEvent): void {
    if (isSvgEngineElement(event.target)) return;
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

  function handleContextMenu(event: MouseEvent): void {
    const slotId = hitSlotId(event.target) ?? hitSlotIdFromPoint(event);
    if (!slotId) {
      setShapeFormatMenu(null);
      return;
    }
    const slot = props.store.state.document?.slots.find((candidate) => candidate.id === slotId);
    const tableCell = !!tableCellFillSlotId(slotId);
    if (!slot || (!isFormatMenuSlot(slot) && !tableCell)) {
      setShapeFormatMenu(null);
      return;
    }
    event.preventDefault();
    event.stopPropagation();
    props.store.setSelectedSlots([slotId]);
    setShapeFormatMenu({ x: event.clientX, y: event.clientY, slotId, kind: slot.kind, tableCell });
  }

  const marqueeBox = createMemo(() => {
    const current = interaction();
    return current?.kind === "marquee" ? normalizeBox(current.start, current.current) : null;
  });

  const tableSelectionBoxes = createMemo(() => {
    const slots = props.store.state.document?.slots ?? [];
    const byId = new Map(slots.map((slot) => [slot.id, slot]));
    const seen = new Set<string>();
    const boxes: { id: string; box: Box }[] = [];
    for (const slotId of props.store.state.selectedIds) {
      const fillSlotId = tableCellFillSlotId(slotId);
      if (!fillSlotId || seen.has(fillSlotId)) continue;
      const slot = byId.get(fillSlotId) ?? byId.get(slotId);
      const box = slot ? slotBounds(slot) : null;
      if (!box) continue;
      seen.add(fillSlotId);
      boxes.push({ id: fillSlotId, box });
    }
    return boxes;
  });

  const tableDividerHandles = createMemo(() => {
    const base = selectedTableBase();
    if (!base) return [];
    const current = interaction();
    const slots = props.store.state.document?.slots ?? [];
    return slots
      .map((slot) => {
        const match = slot.id.match(new RegExp(`^${escapeRegExp(base)}\\.([vh])(\\d+)$`));
        if (!match) return null;
        const box = slotBounds(slot);
        if (!box) return null;
        const axis = match[1] as TableDividerAxis;
        const index = Number(match[2]);
        if (!Number.isFinite(index)) return null;
        const offset = current?.kind === "table-divider" && current.base === base && current.axis === axis && current.index === index ? snappedDelta(current.start, current.current) : { x: 0, y: 0 };
        return {
          base,
          axis,
          index,
          x: axis === "v" ? box.x + offset.x : box.x,
          y: axis === "h" ? box.y + offset.y : box.y,
          width: box.width,
          height: box.height,
        };
      })
      .filter((handle): handle is { base: string; axis: TableDividerAxis; index: number; x: number; y: number; width: number; height: number } => handle !== null);
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

  function isFormatMenuSlot(slot: LayoutSlot): boolean {
    return ["rect", "circle", "line", "polygon", "path", "text_box"].includes(slot.kind);
  }

  function beginCanvasPointer(event: PointerEvent): void {
    if (!props.store.state.document) return;
    if (isSvgEngineElement(event.target)) return;
    const shouldPan = props.store.state.activeTool === "pan" || event.button === 1 || event.altKey;
    const surface = event.currentTarget instanceof HTMLElement ? event.currentTarget : null;
    if (!surface) return;
    setShapeFormatMenu(null);

    if (shouldPan) {
      event.preventDefault();
      surface.setPointerCapture(event.pointerId);
      setInteraction({
        kind: "pan",
        pointerId: event.pointerId,
        startClient: { x: event.clientX, y: event.clientY },
        startPan: { x: props.store.state.panX, y: props.store.state.panY },
      });
      props.store.setStatusMessage("Panning canvas...");
      return;
    }

    if (event.button !== 0) return;

    if (props.store.state.pendingDrawShape) {
      event.preventDefault();
      surface.setPointerCapture(event.pointerId);
      const start = clientPointToCanvasPoint(surface, event.clientX, event.clientY, props.store.state.zoom);
      setInteraction({ kind: "draw", pointerId: event.pointerId, start, current: start, points: [start], moved: false });
      props.store.setStatusMessage(`Drawing ${props.store.state.pendingDrawShape.label}...`);
      return;
    }

    const slotId = hitSlotId(event.target) ?? hitSlotIdFromPoint(event);
    if (slotId && props.store.state.activeTool === "select") {
      event.preventDefault();
      surface.focus();
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
      props.store.setStatusMessage(`Selected ${selectedIds.length} slot${selectedIds.length === 1 ? "" : "s"}. Drag the selection box to move.`);
      return;
    }
    if (slotId) return;

    event.preventDefault();
    surface.setPointerCapture(event.pointerId);
    const start = clientPointToCanvasPoint(surface, event.clientX, event.clientY, props.store.state.zoom);
    setInteraction({ kind: "marquee", pointerId: event.pointerId, start, current: start, moved: false });
    props.store.setStatusMessage("Marquee selecting...");
  }

  function isSvgEngineElement(target: EventTarget | null): boolean {
    return target instanceof Element && !!target.closest(".svg-edit-drag-proxy, .svg-edit-path-layer");
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
    if (current.kind === "draw") {
      const last = current.points[current.points.length - 1] ?? current.start;
      const points = Math.hypot(point.x - last.x, point.y - last.y) >= 3 ? [...current.points, point] : current.points;
      setInteraction({ ...current, current: point, points, moved });
      return;
    }
    setInteraction({ ...current, current: point, moved });
  }

  function tableCellFillSlotId(slotId: string): string | null {
    const fillMatch = slotId.match(/^(slot\.table(?:_\d+)?\.r\d+c\d+)\.fill$/);
    if (fillMatch) return slotId;
    const textMatch = slotId.match(/^(slot\.table(?:_\d+)?\.r\d+c\d+)$/);
    if (textMatch) return `${textMatch[1]}.fill`;
    return null;
  }

  function selectedTableBase(): string | null {
    for (const slotId of props.store.state.selectedIds) {
      const match = slotId.match(/^(slot\.table(?:_\d+)?)(?:\.|$)/);
      if (match) return match[1];
    }
    return null;
  }

  function escapeRegExp(value: string): string {
    return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
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
    if (current.kind === "draw") {
      const definition = props.store.state.pendingDrawShape;
      if (definition && current.moved) {
        void props.store.insertDrawnShape(definition, [...current.points, current.current]);
      } else {
        props.store.cancelDrawShape();
      }
      setSuppressClick(true);
    }
    if (current.kind === "table-divider" && current.moved) {
      const point = snappedPoint(current.current);
      void props.store.updateTableDivider(current.base, current.axis, current.index, current.axis === "v" ? point.x : point.y);
      setSuppressClick(true);
    }
    if (current.kind === "pan") props.store.setStatusMessage("Pan finished.");
    if (current.kind !== "pan" && !current.moved && current.kind === "marquee") props.store.setStatusMessage("No marquee selection.");
    if (current.kind !== "pan" && !current.moved && current.kind === "table-divider") props.store.setStatusMessage("Table divider resize canceled.");
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

  function drawPreviewPath(): string | null {
    const current = interaction();
    const definition = props.store.state.pendingDrawShape;
    if (!current || current.kind !== "draw" || !definition) return null;
    const start = snappedPoint(current.start);
    const end = snappedPoint(current.current);
    if (definition.kind === "line") return `M ${start.x} ${start.y} L ${end.x} ${end.y}`;
    if (definition.id === "elbow") return `M ${start.x} ${start.y} L ${end.x} ${start.y} L ${end.x} ${end.y}`;
    if (definition.id === "freeform") {
      const points = [...current.points, current.current].map(snappedPoint);
      const [first, ...rest] = points;
      return first ? [`M ${first.x} ${first.y}`, ...rest.map((point) => `L ${point.x} ${point.y}`)].join(" ") : null;
    }
    const dx = end.x - start.x;
    const dy = end.y - start.y;
    const c1 = { x: snapNumber(start.x + dx * 0.25), y: snapNumber(start.y - Math.max(20, Math.abs(dy) * 0.6)) };
    const c2 = { x: snapNumber(start.x + dx * 0.75), y: snapNumber(end.y + Math.max(20, Math.abs(dy) * 0.6)) };
    return `M ${start.x} ${start.y} C ${c1.x} ${c1.y}, ${c2.x} ${c2.y}, ${end.x} ${end.y}`;
  }

  function beginTableDividerResize(handle: { base: string; axis: TableDividerAxis; index: number }, event: PointerEvent): void {
    event.preventDefault();
    event.stopPropagation();
    const surface = event.currentTarget instanceof HTMLElement ? event.currentTarget.closest<HTMLElement>(".canvas-surface") : null;
    if (!surface || props.store.state.loading) return;
    surface.setPointerCapture(event.pointerId);
    const start = clientPointToCanvasPoint(surface, event.clientX, event.clientY, props.store.state.zoom);
    setInteraction({ kind: "table-divider", pointerId: event.pointerId, start, current: start, base: handle.base, axis: handle.axis, index: handle.index, moved: false });
    props.store.setStatusMessage(`Resizing table ${handle.axis === "v" ? "column" : "row"} divider...`);
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
        <Show when={props.store.state.pendingDrawShape} fallback={<div>{props.store.state.selectedIds.length} selected</div>}>
          {(shape) => (
            <div class="draw-mode-status">
              <span>Draw {shape().label}</span>
              <button type="button" onClick={() => props.store.cancelDrawShape()}>
                Cancel
              </button>
            </div>
          )}
        </Show>
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
              "is-drawing": !!props.store.state.pendingDrawShape,
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
            onContextMenu={handleContextMenu}
            onDblClick={handleDoubleClick}
            tabIndex={0}
          >
            {props.store.state.document?.detail.svg ? (
              <SvgContent svg={props.store.state.document?.detail.svg ?? ""} />
            ) : props.store.state.document?.detail.layout ? (
              <LayoutSvgPreview layout={props.store.state.document.detail.layout} />
            ) : (
              <div class="empty-state">No SVG or layout output.</div>
            )}
            <Show when={isCanvasSelected()}>
              <div
                class="canvas-guide"
                aria-hidden="true"
                style={{
                  left: "0px",
                  top: "0px",
                  width: `${canvasWidth()}px`,
                  height: `${canvasHeight()}px`,
                }}
              />
            </Show>
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
            <Show when={drawPreviewPath()}>
              {(path) => (
                <svg class="draw-preview-svg" viewBox={`0 0 ${canvasWidth()} ${canvasHeight()}`} aria-hidden="true">
                  <path d={path()} />
                </svg>
              )}
            </Show>
            <For each={tableSelectionBoxes()}>
              {(item) => (
                <div
                  class="table-cell-selected"
                  aria-hidden="true"
                  style={{
                    left: `${item.box.x}px`,
                    top: `${item.box.y}px`,
                    width: `${item.box.width}px`,
                    height: `${item.box.height}px`,
                  }}
                />
              )}
            </For>
            <For each={tableDividerHandles()}>
              {(handle) => (
                <div
                  class={`table-adjust-handle table-adjust-handle-${handle.axis}`}
                  aria-hidden="true"
                  onPointerDown={(event) => beginTableDividerResize(handle, event)}
                  style={{
                    left: `${handle.axis === "v" ? handle.x : handle.x + handle.width / 2}px`,
                    top: `${handle.axis === "h" ? handle.y : handle.y + handle.height / 2}px`,
                    width: `${handle.axis === "h" ? handle.width : 14}px`,
                    height: `${handle.axis === "v" ? handle.height : 14}px`,
                  }}
                />
              )}
            </For>
            <Show when={overlayBounds()}>
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
                  <button
                    type="button"
                    class="selection-delete-button"
                    aria-label="Delete selected slot"
                    title="Delete"
                    onPointerDown={requestDeleteSelected}
                    onMouseDown={requestDeleteSelected}
                    onClick={requestDeleteSelected}
                    style={{
                      left: `${box().x + box().width + 8}px`,
                      top: `${Math.max(0, box().y - 8)}px`,
                    }}
                  >
                    Del
                  </button>
                </>
              )}
            </Show>
            <Show when={inlineTextEdit()}>
              {(edit) => {
                setTimeout(() => {
                  inlineInputRef?.focus();
                  inlineInputRef?.select();
                }, 20);

                const handleKeyDown = (e: KeyboardEvent) => {
                  if (e.key === "Enter") {
                    e.preventDefault();
                    closeInlineTextEditor(true);
                  } else if (e.key === "Escape") {
                    e.preventDefault();
                    closeInlineTextEditor(false);
                  }
                };

                return (
                  <input
                    ref={inlineInputRef}
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
                    onBlur={() => closeInlineTextEditor(true)}
                  />
                );
              }}
            </Show>
          </div>
        </Show>
        <Show when={shapeFormatMenu()}>
          {(menu) => (
            <div
              class="shape-format-menu open"
              style={{ left: `${menu().x}px`, top: `${menu().y}px` }}
              onPointerDown={(event) => event.stopPropagation()}
              onClick={(event) => event.stopPropagation()}
            >
              <div class="shape-format-title">{menu().tableCell ? "Table Cell" : "Shape Format"}</div>
              <div class="shape-format-swatches">
                <For each={SHAPE_FILL_SWATCHES}>
                  {(color) => (
                    <button
                      type="button"
                      classList={{ "shape-swatch": true, transparent: color === "none" }}
                      style={color === "none" ? undefined : { background: color }}
                      title={color}
                      disabled={props.store.state.loading || (!menu().tableCell && menu().kind === "line")}
                      onClick={() => {
                        if (menu().tableCell) void props.store.applySelectedTableCellFill(color);
                        else void props.store.applyShapeFill(color);
                        setShapeFormatMenu(null);
                      }}
                    />
                  )}
                </For>
              </div>
              <Show when={!menu().tableCell}>
                <div class="shape-format-row">
                  <button type="button" class="shape-format-btn" disabled={props.store.state.loading} onClick={() => { void props.store.applyShapeStroke("#111827"); setShapeFormatMenu(null); }}>
                    Stroke
                  </button>
                  <button type="button" class="shape-format-btn" disabled={props.store.state.loading} onClick={() => { void props.store.applyShapeStroke("none"); setShapeFormatMenu(null); }}>
                    No Border
                  </button>
                </div>
                <div class="shape-format-row">
                  <button type="button" class="shape-format-btn" disabled={props.store.state.loading} onClick={() => { void props.store.applyShapeDash(""); setShapeFormatMenu(null); }}>
                    Solid
                  </button>
                  <button type="button" class="shape-format-btn" disabled={props.store.state.loading} onClick={() => { void props.store.applyShapeDash("4 3"); setShapeFormatMenu(null); }}>
                    Dash
                  </button>
                  <button type="button" class="shape-format-btn" disabled={props.store.state.loading} onClick={() => { void props.store.applyShapeDash("2 5"); setShapeFormatMenu(null); }}>
                    Dot
                  </button>
                </div>
              </Show>
            </div>
          )}
        </Show>
      </div>
      <div class="slot-strip" classList={{ open: slotStripOpen() }}>
        <button
          type="button"
          class="slot-strip-toggle"
          aria-expanded={slotStripOpen()}
          onClick={() => setSlotStripOpen((open) => !open)}
        >
          <span>Slots ({props.store.state.document?.slots.length ?? 0})</span>
          <small>{props.store.state.selectedIds.length ? props.store.state.selectedIds.join(", ") : "none selected"}</small>
        </button>
        <Show when={slotStripOpen()}>
          <div class="slot-strip-list">
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
        </Show>
      </div>
    </section>
  );
}
