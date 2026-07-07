import { SVG, type Element as SvgElement } from "@svgdotjs/svg.js";
import "@svgdotjs/svg.draggable.js";
import "@svgdotjs/svg.select.js";
import "@svgdotjs/svg.resize.js";
import type { Box } from "../model/geometry";

export interface SvgPathEditPoint {
  index: number;
  x: number;
  y: number;
}

export interface SvgEditEngineCallbacks {
  getSelectionBox(): Box | null;
  getSelectedIds(): string[];
  canResizeSelection(): boolean;
  getPointEditableElement(): SVGElement | null;
  commitPointEdit(slotId: string, element: SVGElement): void;
  getPathEditPoints(): { slotId: string; points: SvgPathEditPoint[] } | null;
  commitPathPoint(slotId: string, pointIndex: number, x: number, y: number): void;
  previewMove(dx: number, dy: number): void;
  clearPreview(): void;
  commitMove(slotIds: string[], dx: number, dy: number): void;
  commitResize(box: Box): void;
}

export class SvgEditEngine {
  private proxy: SvgElement | null = null;
  private pointElement: SvgElement | null = null;
  private pointElementNode: SVGElement | null = null;
  private pathEditGroup: SVGGElement | null = null;
  private pathEditKey = "";
  private pathDrag: { pointerId: number; slotId: string; pointIndex: number; handle: SVGCircleElement } | null = null;
  private dragStart: { box: Box; selectedIds: string[] } | null = null;
  private resizeTimer = 0;
  private resizeEnabled: boolean | null = null;

  constructor(
    private readonly svg: SVGSVGElement,
    private readonly callbacks: SvgEditEngineCallbacks,
  ) {}

  sync(): void {
    const box = this.callbacks.getSelectionBox();
    const selectedIds = this.callbacks.getSelectedIds().filter((slotId) => slotId !== "__canvas__");
    if (!box || !selectedIds.length) {
      this.destroy();
      return;
    }
    this.syncPointEditing();
    this.syncPathEditing();
    if (!this.proxy) {
      this.proxy = SVG(this.svg)
        .rect(Math.max(1, box.width), Math.max(1, box.height))
        .move(box.x, box.y)
        .addClass("svg-edit-drag-proxy")
        .attr({ fill: "rgba(0,0,0,0)", stroke: "none", "pointer-events": "all" });
      this.proxy.draggable();
      this.proxy.select({ createRot: createHiddenHandle, updateRot: noopUpdateHandle });
      this.proxy.resize({ preserveAspectRatio: false, aroundCenter: false, grid: 1, degree: 0.1 });
      this.proxy.on("dragstart.modu", () => this.handleDragStart());
      this.proxy.on("dragmove.modu", (event: Event) => this.handleDragMove(event as CustomEvent));
      this.proxy.on("dragend.modu", (event: Event) => this.handleDragEnd(event as CustomEvent));
      this.proxy.on("resize.modu", (event: Event) => this.handleResize(event as CustomEvent));
    }
    if (!this.dragStart) {
      this.proxy.size(Math.max(1, box.width), Math.max(1, box.height)).move(box.x, box.y);
    }
    const canResize = this.callbacks.canResizeSelection();
    if (this.resizeEnabled !== canResize) {
      this.resizeEnabled = canResize;
      if (canResize) {
        this.proxy.select({ createRot: createHiddenHandle, updateRot: noopUpdateHandle });
        this.proxy.resize({ preserveAspectRatio: false, aroundCenter: false, grid: 1, degree: 0.1 });
      } else {
        this.proxy.resize(false);
        this.proxy.select(false);
      }
    }
  }

  destroy(): void {
    if (this.proxy) {
      try {
        this.proxy.draggable(false);
        this.proxy.resize(false);
        this.proxy.select(false);
        this.proxy.remove();
      } catch {
        // Plugin cleanup is best effort; stale DOM will be replaced on rerender.
      }
    }
    this.proxy = null;
    this.resizeEnabled = null;
    this.clearPointEditing();
    this.clearPathEditing();
    this.dragStart = null;
    if (this.resizeTimer) window.clearTimeout(this.resizeTimer);
    this.resizeTimer = 0;
    this.callbacks.clearPreview();
  }

  private syncPointEditing(): void {
    const node = this.callbacks.getPointEditableElement();
    if (node === this.pointElementNode) return;
    this.clearPointEditing();
    if (!node) return;
    this.pointElementNode = node;
    this.pointElement = SVG(node);
    if ("pointSelect" in this.pointElement) {
      (this.pointElement as SvgElement & { pointSelect: (enable?: boolean) => SvgElement }).pointSelect();
      this.pointElement.on("point.modu", () => {
        const selectedId = this.callbacks.getSelectedIds()[0];
        if (selectedId && this.pointElementNode) this.callbacks.commitPointEdit(selectedId, this.pointElementNode);
      });
    }
  }

  private clearPointEditing(): void {
    if (this.pointElement) {
      try {
        if ("pointSelect" in this.pointElement) {
          (this.pointElement as SvgElement & { pointSelect: (enable: boolean) => SvgElement }).pointSelect(false);
        }
        this.pointElement.off("point.modu");
      } catch {
        // Best effort plugin cleanup.
      }
    }
    this.pointElement = null;
    this.pointElementNode = null;
  }

  private syncPathEditing(): void {
    const edit = this.callbacks.getPathEditPoints();
    const nextKey = edit ? `${edit.slotId}:${edit.points.map((point) => `${point.index}:${round(point.x)},${round(point.y)}`).join("|")}` : "";
    if (nextKey === this.pathEditKey) return;
    this.clearPathEditing();
    this.pathEditKey = nextKey;
    if (!edit || edit.points.length === 0) return;

    this.pathEditGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
    this.pathEditGroup.classList.add("svg-edit-path-layer");
    this.svg.appendChild(this.pathEditGroup);

    const guide = document.createElementNS("http://www.w3.org/2000/svg", "polyline");
    guide.classList.add("svg-edit-path-guide");
    guide.setAttribute("points", edit.points.map((point) => `${point.x},${point.y}`).join(" "));
    this.pathEditGroup.appendChild(guide);

    for (const point of edit.points) {
      const handle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      handle.classList.add("svg-edit-path-handle");
      handle.dataset.slotId = edit.slotId;
      handle.dataset.pointIndex = String(point.index);
      handle.setAttribute("cx", String(point.x));
      handle.setAttribute("cy", String(point.y));
      handle.setAttribute("r", "5");
      handle.addEventListener("pointerdown", this.handlePathPointerDown);
      this.pathEditGroup.appendChild(handle);
    }
  }

  private clearPathEditing(): void {
    if (this.pathEditGroup) {
      for (const handle of this.pathEditGroup.querySelectorAll<SVGCircleElement>(".svg-edit-path-handle")) {
        handle.removeEventListener("pointerdown", this.handlePathPointerDown);
      }
      this.pathEditGroup.remove();
    }
    this.pathEditGroup = null;
    this.pathEditKey = "";
    this.pathDrag = null;
  }

  private readonly handlePathPointerDown = (event: PointerEvent): void => {
    const handle = event.currentTarget instanceof SVGCircleElement ? event.currentTarget : null;
    const slotId = handle?.dataset.slotId;
    const pointIndex = Number(handle?.dataset.pointIndex);
    if (!handle || !slotId || !Number.isFinite(pointIndex)) return;
    event.preventDefault();
    event.stopPropagation();
    handle.setPointerCapture(event.pointerId);
    this.pathDrag = { pointerId: event.pointerId, slotId, pointIndex, handle };
    handle.addEventListener("pointermove", this.handlePathPointerMove);
    handle.addEventListener("pointerup", this.handlePathPointerUp);
    handle.addEventListener("pointercancel", this.handlePathPointerUp);
  };

  private readonly handlePathPointerMove = (event: PointerEvent): void => {
    const drag = this.pathDrag;
    if (!drag || drag.pointerId !== event.pointerId) return;
    event.preventDefault();
    event.stopPropagation();
    const point = clientPointToSvg(this.svg, event.clientX, event.clientY);
    if (!point) return;
    drag.handle.setAttribute("cx", String(round(point.x)));
    drag.handle.setAttribute("cy", String(round(point.y)));
    this.updatePathGuide();
  };

  private readonly handlePathPointerUp = (event: PointerEvent): void => {
    const drag = this.pathDrag;
    if (!drag || drag.pointerId !== event.pointerId) return;
    event.preventDefault();
    event.stopPropagation();
    drag.handle.removeEventListener("pointermove", this.handlePathPointerMove);
    drag.handle.removeEventListener("pointerup", this.handlePathPointerUp);
    drag.handle.removeEventListener("pointercancel", this.handlePathPointerUp);
    try {
      drag.handle.releasePointerCapture(event.pointerId);
    } catch {
      // Ignore stale pointer capture.
    }
    const x = Number(drag.handle.getAttribute("cx"));
    const y = Number(drag.handle.getAttribute("cy"));
    this.pathDrag = null;
    if (Number.isFinite(x) && Number.isFinite(y)) {
      this.callbacks.commitPathPoint(drag.slotId, drag.pointIndex, x, y);
    }
  };

  private updatePathGuide(): void {
    const group = this.pathEditGroup;
    if (!group) return;
    const guide = group.querySelector<SVGPolylineElement>(".svg-edit-path-guide");
    if (!guide) return;
    const points = [...group.querySelectorAll<SVGCircleElement>(".svg-edit-path-handle")]
      .map((handle) => `${handle.getAttribute("cx") ?? 0},${handle.getAttribute("cy") ?? 0}`)
      .join(" ");
    guide.setAttribute("points", points);
  }

  private handleDragStart(): void {
    const box = this.callbacks.getSelectionBox();
    if (!box) return;
    this.dragStart = { box, selectedIds: this.callbacks.getSelectedIds() };
  }

  private handleDragMove(event: CustomEvent): void {
    const start = this.dragStart;
    const nextBox = eventBox(event) ?? this.proxyBox();
    if (!start || !nextBox) return;
    this.callbacks.previewMove(nextBox.x - start.box.x, nextBox.y - start.box.y);
  }

  private handleDragEnd(event: CustomEvent): void {
    const start = this.dragStart;
    const nextBox = eventBox(event) ?? this.proxyBox();
    this.dragStart = null;
    this.callbacks.clearPreview();
    if (!start || !nextBox) return;
    const dx = round(nextBox.x - start.box.x);
    const dy = round(nextBox.y - start.box.y);
    if (dx || dy) this.callbacks.commitMove(start.selectedIds, dx, dy);
  }

  private handleResize(event: CustomEvent): void {
    if (!this.callbacks.canResizeSelection()) return;
    const box = eventBox(event) ?? this.proxyBox();
    if (!box) return;
    if (this.resizeTimer) window.clearTimeout(this.resizeTimer);
    this.resizeTimer = window.setTimeout(() => {
      this.resizeTimer = 0;
      this.callbacks.commitResize(box);
    }, 180);
  }

  private proxyBox(): Box | null {
    if (!this.proxy) return null;
    try {
      const box = this.proxy.bbox();
      return { x: box.x, y: box.y, width: box.w, height: box.h };
    } catch {
      return null;
    }
  }
}

function eventBox(event: CustomEvent): Box | null {
  const box = (event.detail as { box?: { x?: number; y?: number; w?: number; width?: number; h?: number; height?: number } } | undefined)?.box;
  if (!box || typeof box.x !== "number" || typeof box.y !== "number") return null;
  return {
    x: box.x,
    y: box.y,
    width: Number(box.w ?? box.width ?? 0),
    height: Number(box.h ?? box.height ?? 0),
  };
}

function round(value: number): number {
  return Math.round(value * 100) / 100;
}

function clientPointToSvg(svg: SVGSVGElement, clientX: number, clientY: number): { x: number; y: number } | null {
  const matrix = svg.getScreenCTM();
  if (!matrix) return null;
  const point = svg.createSVGPoint();
  point.x = clientX;
  point.y = clientY;
  const transformed = point.matrixTransform(matrix.inverse());
  return { x: transformed.x, y: transformed.y };
}

function createHiddenHandle(group: SvgElement): SvgElement {
  return (group as any).circle(0).attr({ opacity: 0, "pointer-events": "none" });
}

function noopUpdateHandle(): void {}
