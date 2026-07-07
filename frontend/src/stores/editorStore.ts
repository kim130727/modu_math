import { createStore } from "solid-js/store";
import {
  applyLayoutPatches,
  applyLayoutPatchesAndBuild,
  buildProblem,
  formatDsl,
  loadProblem,
  listProblems,
  saveDsl,
} from "../api/editorApi";
import { EditorApiError } from "../api/httpClient";
import {
  emptyHistory,
  popRedoEntry,
  popUndoEntry,
  pushHistoryEntry,
  type HistorySnapshot,
  type HistoryState,
} from "../editor-core/history/historyManager";
import { createEditorDocument, type EditorDocument } from "../editor-core/model/editorDocument";
import type { Box, Point } from "../editor-core/model/geometry";
import { clearSelection, toggleSelection } from "../editor-core/selection/selectionManager";
import { slotBounds } from "../editor-core/transform/bounds";
import type { BuildOutputState, BuildProblemResponse, EditorError, LayoutPatch, LayoutPatchBuildResponse, ProblemDetailResponse, ProblemSummary } from "../types/api";
import type { LayoutDocument, LayoutSlot } from "../types/layout";
import type { RendererDocument, RendererElement } from "../types/renderer";

export type EditorTool = "select" | "pan";
export type EditorPickMode = "all" | "linepath" | "text" | "shape";
export type InsertableShapeKind = "rect" | "text_box" | "circle" | "line" | "triangle" | "path";
export type GalleryShapeKind = "line" | "rect" | "circle" | "polygon" | "path";
export type GalleryShapeDefinitionKind = GalleryShapeKind | "composite";
export type AlignMode = "left" | "center" | "right" | "top" | "middle" | "bottom";
export type LayerMode = "front" | "back" | "forward" | "backward";
export type TextAlignMode = "left" | "center" | "right";
export type TableDividerAxis = "v" | "h";

export interface GalleryShapeDefinition {
  id: string;
  label: string;
  kind: GalleryShapeDefinitionKind;
  w?: number;
  h?: number;
  r?: number;
  rx?: number;
  ry?: number;
  line?: "horizontal" | "vertical";
  points?: [number, number][];
  d?: string;
  sourceWidth?: number;
  sourceHeight?: number;
  fill?: string;
  stroke?: string;
  stroke_width?: number;
  parts?: GalleryShapePart[];
  drawMode?: boolean;
}

export interface GalleryShapePart {
  id: string;
  kind: GalleryShapeKind;
  x?: number;
  y?: number;
  width?: number;
  height?: number;
  cx?: number;
  cy?: number;
  r?: number;
  rx?: number;
  ry?: number;
  x1?: number;
  y1?: number;
  x2?: number;
  y2?: number;
  points?: [number, number][];
  d?: string;
  fill?: string;
  stroke?: string;
  stroke_width?: number;
}

export interface BarModelOptions {
  bars?: number;
  cells?: number;
  shadedCounts?: string;
  fillColors?: string;
  stroke?: string;
  dashed?: boolean;
}

export interface TickBarOptions {
  rows?: number;
  totalTicks?: number;
  filledTicks?: string;
  majorEvery?: number;
  labels?: string;
  unit?: string;
  showScaleLabels?: boolean;
  showFractionLabel?: boolean;
  axisColor?: string;
  fillColor?: string;
}

export interface FractionInsertOptions {
  mixed?: boolean;
  whole?: string;
  numerator?: string;
  denominator?: string;
}

export interface EditorState {
  problemId: string | null;
  problems: ProblemSummary[];
  document: EditorDocument | null;
  dslDraft: string;
  selectedIds: string[];
  zoom: number;
  panX: number;
  panY: number;
  activeTool: EditorTool;
  pickMode: EditorPickMode;
  snapEnabled: boolean;
  history: HistoryState<LayoutPatch[]>;
  historyBusy: boolean;
  dirty: boolean;
  loading: boolean;
  saving: boolean;
  formatting: boolean;
  building: boolean;
  buildOutput: BuildOutputState | null;
  error: EditorError | null;
  statusMessage: string;
  pendingDrawShape: GalleryShapeDefinition | null;
  hasCopyBuffer: boolean;
}

const initialState: EditorState = {
  problemId: null,
  problems: [],
  document: null,
  dslDraft: "",
  selectedIds: [],
  zoom: 1,
  panX: 0,
  panY: 0,
  activeTool: "select",
  pickMode: "all",
  snapEnabled: true,
  history: emptyHistory<LayoutPatch[]>(),
  historyBusy: false,
  dirty: false,
  loading: false,
  saving: false,
  formatting: false,
  building: false,
  buildOutput: null,
  error: null,
  statusMessage: "Ready",
  pendingDrawShape: null,
  hasCopyBuffer: false,
};

function toEditorError(error: unknown): EditorError {
  if (error instanceof EditorApiError) {
    return { message: error.message, category: error.category, status: error.status };
  }
  return { message: String(error), category: "UNKNOWN_ERROR", status: 0 };
}

export function createEditorStore() {
  const [state, setState] = createStore<EditorState>(initialState);
  let copyBuffer: LayoutSlot[] = [];
  let pasteSequence = 0;

  async function refreshProblems(): Promise<void> {
    setState({ loading: true, error: null, statusMessage: "Loading problem list..." });
    try {
      const response = await listProblems();
      setState({ problems: response.problems, loading: false, statusMessage: `Loaded ${response.problems.length} problems.` });
    } catch (error) {
      setState({ loading: false, error: toEditorError(error), statusMessage: "Could not load problem list." });
    }
  }

  async function openProblem(problemId: string): Promise<void> {
    if (!problemId.trim()) return;
    setState({ loading: true, error: null, selectedIds: clearSelection(), statusMessage: "Opening problem..." });
    try {
      const detail = await loadProblem(problemId.trim());
      setState({
        problemId: detail.problem_id,
        document: createEditorDocument(detail),
        dslDraft: detail.dsl,
        selectedIds: clearSelection(),
        zoom: 1,
        panX: 0,
        panY: 0,
        history: emptyHistory<LayoutPatch[]>(),
        historyBusy: false,
        dirty: false,
        loading: false,
        saving: false,
        formatting: false,
        building: false,
        buildOutput: null,
        statusMessage: "Problem opened.",
      });
      const url = new URL(window.location.href);
      url.searchParams.set("problem", detail.problem_id);
      window.history.replaceState(null, "", url);
    } catch (error) {
      setState({ loading: false, error: toEditorError(error), statusMessage: "Could not open problem." });
    }
  }

  async function patchAndBuild(patches: LayoutPatch[], options: { format?: boolean } = {}): Promise<boolean> {
    if (!state.problemId || patches.length === 0) return false;
    const deletedIds = patches.filter((patch) => patch.op === "delete").map((patch) => patch.target);
    setState({ loading: true, error: null, statusMessage: "Applying changes..." });
    try {
      const response = await applyLayoutPatchesAndBuild(state.problemId, patches, options);
      applyPatchBuildResponse(response, deletedIds);
      setState({ dirty: false, loading: false, statusMessage: "Changes applied." });
      return true;
    } catch (error) {
      if (error instanceof EditorApiError && isPatchBuildResponse(error.payload)) {
        applyPatchBuildResponse(error.payload, deletedIds);
        setState({
          dirty: false,
          loading: false,
          error: toEditorError(error),
          statusMessage: "Changes applied, but build failed.",
        });
        return true;
      }
      setState({ loading: false, error: toEditorError(error), statusMessage: "Could not apply changes." });
      return false;
    }
  }

  async function commitHistoryPatches(
    label: string,
    patches: LayoutPatch[],
    inversePatches: LayoutPatch[],
    options: { format?: boolean } = {},
  ): Promise<boolean> {
    if (patches.length === 0 || inversePatches.length === 0) return false;
    const committed = await patchAndBuild(patches, options);
    if (committed) {
      const entry: HistorySnapshot<LayoutPatch[]> = { label, before: inversePatches, after: patches };
      setState("history", pushHistoryEntry(state.history, entry));
      setState({ statusMessage: `${label} complete.` });
    }
    return committed;
  }

  async function moveSlots(slotIds: string[], dx: number, dy: number, label = "Move"): Promise<boolean> {
    if (slotIds.length === 0 || state.loading) return false;
    const movableIds = expandGeneratedMoveIds(slotIds.map(resolveSlotId)).filter((slotId) => !!findSlot(slotId));
    if (!movableIds.length) return false;
    const patches: LayoutPatch[] = [];
    const inversePatches: LayoutPatch[] = [];
    for (const slotId of movableIds) {
      const slot = findSlot(slotId);
      const value = slot ? movePropertiesForSlot(slot, dx, dy) : null;
      if (!slot || !value) continue;
      patches.push({ target: slotId, op: "update", value });
      inversePatches.push({ target: slotId, op: "update", value: inverseAnyProperties(slot, value) });
    }
    return commitHistoryPatches(label, patches, inversePatches, { format: false });
  }

  async function moveSelectedSlots(dx: number, dy: number): Promise<boolean> {
    if (state.selectedIds.length === 0 || state.loading) return false;
    return moveSlots(state.selectedIds, dx, dy, "Keyboard move");
  }

  async function deleteSelectedSlots(): Promise<boolean> {
    if (state.selectedIds.length === 0) return false;
    const selectedIds = uniqueIds(state.selectedIds.map(resolveSlotId));
    const inversePatches = selectedIds
      .map((slotId) => {
        const slot = findSlot(slotId);
        if (!slot) return null;
        return addPatchForSlot(slot);
      })
      .filter((patch): patch is LayoutPatch => patch !== null);
    const patches: LayoutPatch[] = selectedIds.map((slotId) => ({
      target: slotId,
      op: "delete",
    }));
    optimisticallyRemoveDeletedSlots(selectedIds);
    const deleted = inversePatches.length === patches.length
      ? await commitHistoryPatches("Delete", patches, inversePatches, { format: false })
      : await patchAndBuild(patches, { format: false });
    if (deleted) {
      setState({ selectedIds: clearSelection() });
    }
    return deleted;
  }

  async function updateSlotProperties(slotId: string, properties: Record<string, unknown>): Promise<boolean> {
    if (!slotId || state.loading) return false;
    const slot = findSlot(slotId);
    if (!slot) return false;
    const inverse = inverseProperties(slot, properties);
    if (!Object.keys(inverse).length) return false;
    return commitHistoryPatches(
      "Property edit",
      [{ target: slotId, op: "update", value: properties }],
      [{ target: slotId, op: "update", value: inverse }],
      { format: false },
    );
  }

  async function updateSelectedBounds(box: Box): Promise<boolean> {
    if (state.selectedIds.length !== 1 || state.loading) return false;
    const slot = findSlot(state.selectedIds[0]);
    if (!slot) return false;
    const properties = boundsPropertiesForSlot(slot, box);
    if (!properties) return false;
    return commitSlotPropertyPatch("Bounds edit", slot, properties);
  }

  async function updateSelectedTransform(transform: string): Promise<boolean> {
    if (state.selectedIds.length !== 1 || state.loading) return false;
    const slot = findSlot(state.selectedIds[0]);
    if (!slot) return false;
    return commitSlotPropertyPatch("Transform edit", slot, { transform: transform.trim() });
  }

  async function updateSelectedText(text: string): Promise<boolean> {
    if (state.selectedIds.length !== 1 || state.loading) return false;
    const slot = findSlot(state.selectedIds[0]);
    if (!slot || !isTextLikeSlot(slot)) return false;
    return commitSlotPropertyPatch("Update text", slot, { text });
  }

  async function nudgeSelectedFontSize(delta: number): Promise<boolean> {
    if (state.selectedIds.length !== 1 || state.loading) return false;
    const slot = findSlot(state.selectedIds[0]);
    if (!slot || !isTextLikeSlot(slot)) return false;
    const current = Number((slot.content as Record<string, unknown>).font_size ?? 18);
    const next = Math.max(6, Math.min(96, Math.round(current + delta)));
    return commitSlotPropertyPatch("Font size", slot, { font_size: next });
  }

  async function alignSelectedText(mode: TextAlignMode): Promise<boolean> {
    if (state.selectedIds.length !== 1 || state.loading) return false;
    const slot = findSlot(state.selectedIds[0]);
    if (!slot || !isTextLikeSlot(slot)) return false;
    if (slot.kind === "text_box") return commitSlotPropertyPatch(`Text ${mode}`, slot, { align: mode });
    const anchor = mode === "center" ? "middle" : mode === "right" ? "end" : "start";
    return commitSlotPropertyPatch(`Text ${mode}`, slot, { anchor });
  }

  async function applyShapeFill(fill: string): Promise<boolean> {
    const slots = selectedShapeSlots().filter((slot) => slot.kind !== "line");
    if (!slots.length || state.loading) return false;
    return commitMultiSlotPropertyPatch("Shape fill", slots, { fill });
  }

  async function applyShapeStroke(stroke: string): Promise<boolean> {
    const slots = selectedShapeSlots();
    if (!slots.length || state.loading) return false;
    return commitMultiSlotPropertyPatch("Shape stroke", slots, { stroke, stroke_width: stroke === "none" ? 0 : 1.5 });
  }

  async function applyShapeDash(strokeDasharray: string): Promise<boolean> {
    const slots = selectedShapeSlots();
    if (!slots.length || state.loading) return false;
    const value = strokeDasharray ? { stroke_dasharray: strokeDasharray, stroke_width: 1.5 } : { stroke_dasharray: "" };
    return commitMultiSlotPropertyPatch("Shape dash", slots, value);
  }

  async function applySelectedTableCellFill(fill: string): Promise<boolean> {
    if (!state.selectedIds.length || state.loading) return false;
    const fillSlots = state.selectedIds
      .map((slotId) => tableCellFillSlotId(slotId))
      .filter((slotId): slotId is string => !!slotId)
      .map((slotId) => findSlot(slotId))
      .filter((slot): slot is LayoutSlot => !!slot);
    if (!fillSlots.length) return false;
    return commitMultiSlotPropertyPatch("Table cell fill", fillSlots, { fill });
  }

  async function updateTableDivider(base: string, axis: TableDividerAxis, index: number, position: number): Promise<boolean> {
    if (!state.document || state.loading || !base.startsWith("slot.table")) return false;
    const lineSlot = findSlot(`${base}.${axis}${index}`);
    if (!lineSlot || lineSlot.kind !== "line") return false;
    const nextPosition = roundedDelta(position);
    const patches: LayoutPatch[] = [];
    const inversePatches: LayoutPatch[] = [];
    const addUpdate = (slotId: string, properties: Record<string, unknown>) => {
      const slot = findSlot(slotId);
      if (!slot || !Object.keys(properties).length) return;
      patches.push({ target: slotId, op: "update", value: properties });
      inversePatches.push({ target: slotId, op: "update", value: inverseAnyProperties(slot, properties) });
    };

    if (axis === "v") {
      const rows = tableRowsForBase(base);
      const clamped = clampTableVerticalDivider(base, index, nextPosition, rows);
      addUpdate(lineSlot.id, { x1: clamped, x2: clamped });
      for (const row of rows) {
        const leftFill = findSlot(`${base}.r${row}c${index}.fill`);
        const rightFill = findSlot(`${base}.r${row}c${index + 1}.fill`);
        const leftBox = leftFill ? slotBounds(leftFill) : null;
        const rightBox = rightFill ? slotBounds(rightFill) : null;
        if (!leftFill || !rightFill || !leftBox || !rightBox) continue;
        const rightEdge = rightBox.x + rightBox.width;
        const leftWidth = Math.max(4, roundedDelta(clamped - leftBox.x));
        const rightWidth = Math.max(4, roundedDelta(rightEdge - clamped));
        addUpdate(leftFill.id, { width: leftWidth });
        addUpdate(rightFill.id, { x: clamped, width: rightWidth });
        addUpdate(`${base}.r${row}c${index}`, { x: roundedDelta(leftBox.x + leftWidth / 2), max_width: Math.max(8, roundedDelta(leftWidth - 20)) });
        addUpdate(`${base}.r${row}c${index + 1}`, { x: roundedDelta(clamped + rightWidth / 2), max_width: Math.max(8, roundedDelta(rightWidth - 20)) });
      }
    } else {
      const cols = tableColsForBase(base);
      const clamped = clampTableHorizontalDivider(base, index, nextPosition, cols);
      addUpdate(lineSlot.id, { y1: clamped, y2: clamped });
      for (const col of cols) {
        const topFill = findSlot(`${base}.r${index}c${col}.fill`);
        const bottomFill = findSlot(`${base}.r${index + 1}c${col}.fill`);
        const topBox = topFill ? slotBounds(topFill) : null;
        const bottomBox = bottomFill ? slotBounds(bottomFill) : null;
        if (!topFill || !bottomFill || !topBox || !bottomBox) continue;
        const bottomEdge = bottomBox.y + bottomBox.height;
        const topHeight = Math.max(4, roundedDelta(clamped - topBox.y));
        const bottomHeight = Math.max(4, roundedDelta(bottomEdge - clamped));
        addUpdate(topFill.id, { height: topHeight });
        addUpdate(bottomFill.id, { y: clamped, height: bottomHeight });
        addUpdate(`${base}.r${index}c${col}`, { y: roundedDelta(topBox.y + topHeight / 2 + tableTextBaselineOffset(`${base}.r${index}c${col}`)) });
        addUpdate(`${base}.r${index + 1}c${col}`, { y: roundedDelta(clamped + bottomHeight / 2 + tableTextBaselineOffset(`${base}.r${index + 1}c${col}`)) });
      }
    }
    return commitHistoryPatches("Table divider resize", patches, inversePatches, { format: false });
  }

  async function updateCanvasSize(width: number, height: number): Promise<boolean> {
    if (!state.document || !state.problemId || state.loading) return false;
    const canvas = state.document.detail.layout?.canvas;
    if (!canvas) return false;
    const nextWidth = Math.max(20, Math.round(width));
    const nextHeight = Math.max(20, Math.round(height));
    if (nextWidth === canvas.width && nextHeight === canvas.height) return false;
    return commitHistoryPatches(
      "Canvas resize",
      [{ target: "__canvas__", op: "update", value: { width: nextWidth, height: nextHeight } }],
      [{ target: "__canvas__", op: "update", value: { width: canvas.width, height: canvas.height } }],
      { format: false },
    );
  }

  async function alignSelectedSlots(mode: AlignMode): Promise<boolean> {
    if (!state.document || state.loading || state.selectedIds.length < 2) return false;
    const items = selectedSlotsWithBounds();
    if (items.length < 2) return false;

    const targetMetric = alignmentMetric(mode, items.map((item) => item.bounds));
    const canvasBounds = canvasBox();
    const patches: LayoutPatch[] = [];
    const inversePatches: LayoutPatch[] = [];

    for (const item of items) {
      let dx = 0;
      let dy = 0;
      if (mode === "left") dx = targetMetric - item.bounds.x;
      if (mode === "center") dx = targetMetric - (item.bounds.x + item.bounds.width / 2);
      if (mode === "right") dx = targetMetric - (item.bounds.x + item.bounds.width);
      if (mode === "top") dy = targetMetric - item.bounds.y;
      if (mode === "middle") dy = targetMetric - (item.bounds.y + item.bounds.height / 2);
      if (mode === "bottom") dy = targetMetric - (item.bounds.y + item.bounds.height);

      if (canvasBounds) {
        dx = clampDelta(dx, canvasBounds.x - item.bounds.x, canvasBounds.x + canvasBounds.width - (item.bounds.x + item.bounds.width));
        dy = clampDelta(dy, canvasBounds.y - item.bounds.y, canvasBounds.y + canvasBounds.height - (item.bounds.y + item.bounds.height));
      }

      dx = roundedDelta(dx);
      dy = roundedDelta(dy);
      if (dx === 0 && dy === 0) continue;
      const value = movePropertiesForSlot(item.slot, dx, dy);
      if (!value) continue;
      patches.push({ target: item.slot.id, op: "update", value });
      inversePatches.push({ target: item.slot.id, op: "update", value: inverseAnyProperties(item.slot, value) });
    }

    return commitHistoryPatches(`Align ${mode}`, patches, inversePatches, { format: false });
  }

  async function layerSelectedSlots(mode: LayerMode): Promise<boolean> {
    if (!state.document || state.loading || state.selectedIds.length === 0) return false;
    const layout = state.document.detail.layout;
    const patches: LayoutPatch[] = [];
    const inversePatches: LayoutPatch[] = [];

    for (const region of layout?.regions ?? []) {
      const currentOrder = region.slot_ids ?? [];
      const selectedInRegion = state.selectedIds.filter((slotId) => currentOrder.includes(slotId));
      if (!selectedInRegion.length) continue;
      const nextOrder = reorderLayerIds(currentOrder, selectedInRegion, mode);
      if (sameOrder(currentOrder, nextOrder)) continue;
      const regionId = region.id || "region.stem";
      patches.push({ target: "__layer__", op: "layer", value: { region_id: regionId, slot_ids: nextOrder } });
      inversePatches.push({ target: "__layer__", op: "layer", value: { region_id: regionId, slot_ids: currentOrder } });
    }

    return commitHistoryPatches(`Layer ${mode}`, patches, inversePatches, { format: false });
  }

  async function insertShape(kind: InsertableShapeKind): Promise<boolean> {
    if (!state.document || state.loading) return false;
    const regionId = preferredRegionId();
    if (!regionId) {
      setState({ error: { message: "No layout region is available for insertion.", category: "DSL_PATCH_ERROR", status: 400 } });
      return false;
    }
    const slotId = uniqueSlotId(kind);
    const canvas = state.document.detail.layout?.canvas;
    const content = insertedShapeContent(kind, canvas?.width ?? 900, canvas?.height ?? 420);
    const addPatch: LayoutPatch = {
      target: slotId,
      op: "add",
      value: {
        kind: patchKindForInsert(kind),
        region_id: regionId,
        content,
      },
    };
    const inserted = await commitHistoryPatches("Insert shape", [addPatch], [{ target: slotId, op: "delete" }], { format: false });
    if (inserted) {
      setState({ selectedIds: [slotId], activeTool: "select" });
    }
    return inserted;
  }

  async function insertGalleryShape(definition: GalleryShapeDefinition): Promise<boolean> {
    if (!state.document || state.loading) return false;
    const regionId = preferredRegionId();
    if (!regionId) {
      setState({ error: { message: "No layout region is available for insertion.", category: "DSL_PATCH_ERROR", status: 400 } });
      return false;
    }
    if (definition.kind === "composite") {
      const { patches, selectId } = compositeShapePatches(definition, regionId);
      return insertGeneratedPatches(`Insert ${definition.label}`, patches, selectId);
    }
    const slotId = uniqueSlotId(definition.id);
    const canvas = state.document.detail.layout?.canvas;
    const payload = galleryShapePayload(definition, canvas?.width ?? 900, canvas?.height ?? 420);
    const addPatch: LayoutPatch = {
      target: slotId,
      op: "add",
      value: {
        kind: payload.kind,
        region_id: regionId,
        content: payload.content,
      },
    };
    const inserted = await commitHistoryPatches(`Insert ${definition.label}`, [addPatch], [{ target: slotId, op: "delete" }], { format: false });
    if (inserted) setState({ selectedIds: [slotId], activeTool: "select" });
    return inserted;
  }

  function beginDrawShape(definition: GalleryShapeDefinition): void {
    if (!state.document || state.loading || definition.kind === "composite") return;
    setState({ pendingDrawShape: definition, activeTool: "select", selectedIds: clearSelection(), statusMessage: `Draw ${definition.label}: drag on the canvas.` });
  }

  function cancelDrawShape(): void {
    setState({ pendingDrawShape: null, statusMessage: "Drawing canceled." });
  }

  async function insertDrawnShape(definition: GalleryShapeDefinition, points: Point[]): Promise<boolean> {
    if (!state.document || state.loading || definition.kind === "composite" || points.length < 2) return false;
    const regionId = preferredRegionId();
    if (!regionId) {
      setState({ error: { message: "No layout region is available for insertion.", category: "DSL_PATCH_ERROR", status: 400 }, pendingDrawShape: null });
      return false;
    }
    const content = drawnShapeContent(definition, points);
    if (!content) return false;
    const slotId = uniqueSlotId(definition.id);
    const addPatch: LayoutPatch = {
      target: slotId,
      op: "add",
      value: { kind: content.kind, region_id: regionId, content: content.content },
    };
    const inserted = await commitHistoryPatches(`Draw ${definition.label}`, [addPatch], [{ target: slotId, op: "delete" }], { format: false });
    if (inserted) setState({ selectedIds: [slotId], activeTool: "select", pendingDrawShape: null });
    return inserted;
  }

  async function insertTable(rows: number, cols: number): Promise<boolean> {
    const { base, patches } = tablePatches(rows, cols);
    return insertGeneratedPatches(`Insert table`, patches, `${base}.outer`);
  }

  async function insertGraphPaper(rows: number, cols: number): Promise<boolean> {
    const { base, patches } = graphPaperPatches(rows, cols);
    return insertGeneratedPatches(`Insert graph paper`, patches, `${base}.v0`);
  }

  async function insertBarModel(options: BarModelOptions = {}): Promise<boolean> {
    const { base, patches } = barModelPatches(options);
    return insertGeneratedPatches(`Insert bar model`, patches, `${base}.bar1.outline`);
  }

  async function insertTickBar(options: TickBarOptions = {}): Promise<boolean> {
    const { base, patches } = tickBarPatches(options);
    return insertGeneratedPatches(`Insert tick bar`, patches, `${base}.row1.axis`);
  }

  async function insertFractionExpression(options: FractionInsertOptions = {}): Promise<boolean> {
    const { base, patches } = fractionPatches(options);
    return insertGeneratedPatches(options.mixed ? "Insert mixed fraction" : "Insert fraction", patches, `${base}.num`);
  }

  async function insertGeneratedPatches(label: string, patches: LayoutPatch[], selectId: string): Promise<boolean> {
    if (!state.document || state.loading || patches.length === 0) return false;
    const inversePatches = patches.map((patch) => ({ target: patch.target, op: "delete" }));
    const inserted = await commitHistoryPatches(label, patches, inversePatches, { format: false });
    if (inserted) setState({ selectedIds: [selectId], activeTool: "select" });
    return inserted;
  }

  function copySelectedSlots(): boolean {
    if (!state.document || state.selectedIds.length === 0) return false;
    copyBuffer = uniqueIds(state.selectedIds.map(resolveSlotId))
      .map((slotId) => findSlot(slotId))
      .filter((slot): slot is LayoutSlot => slot !== null)
      .map((slot) => structuredClone(slot));
    pasteSequence = 0;
    setState({
      hasCopyBuffer: copyBuffer.length > 0,
      statusMessage: copyBuffer.length > 0 ? `Copied ${copyBuffer.length} slot${copyBuffer.length === 1 ? "" : "s"}.` : "Nothing selected to copy.",
    });
    return copyBuffer.length > 0;
  }

  async function pasteCopiedSlots(): Promise<boolean> {
    if (!state.document || state.loading) return false;
    if (copyBuffer.length === 0) {
      setState({ statusMessage: "Nothing copied to paste." });
      return false;
    }
    pasteSequence += 1;
    const offset = 20 * pasteSequence;
    const patches: LayoutPatch[] = [];
    const inversePatches: LayoutPatch[] = [];
    const pastedIds: string[] = [];

    for (const slot of copyBuffer) {
      if (slot.kind === "unknown") continue;
      const regionId = regionIdForSlot(slot.id);
      if (!regionId) continue;
      const nextId = uniqueSlotId(slot.kind);
      patches.push({
        target: nextId,
        op: "add",
        value: {
          kind: slot.kind,
          region_id: regionId,
          content: shiftCopiedContent(structuredClone(slot.content), offset, offset),
        },
      });
      inversePatches.push({ target: nextId, op: "delete" });
      pastedIds.push(nextId);
    }

    if (!patches.length) {
      setState({ statusMessage: "No copyable slots in clipboard." });
      return false;
    }
    const pasted = await commitHistoryPatches("Paste", patches, inversePatches, { format: false });
    if (pasted) setState({ selectedIds: pastedIds, activeTool: "select" });
    return pasted;
  }

  async function insertImageFile(file: File): Promise<boolean> {
    if (!state.document || state.loading) return false;
    if (!file.type.startsWith("image/")) {
      setState({ error: { message: "Choose an image file.", category: "DSL_PATCH_ERROR", status: 400 } });
      return false;
    }
    const regionId = preferredRegionId();
    if (!regionId) {
      setState({ error: { message: "No layout region is available for insertion.", category: "DSL_PATCH_ERROR", status: 400 } });
      return false;
    }
    try {
      const href = await readFileAsDataUrl(file);
      const size = await imageSizeFromDataUrl(href);
      const maxWidth = 320;
      const maxHeight = 240;
      const scale = Math.min(1, maxWidth / Math.max(size.width, 1), maxHeight / Math.max(size.height, 1));
      const width = Math.max(24, Math.round(size.width * scale));
      const height = Math.max(24, Math.round(size.height * scale));
      const { x, y } = centeredOrigin(width, height, state.document.detail.layout?.canvas?.width ?? 900, state.document.detail.layout?.canvas?.height ?? 420);
      const slotId = uniqueSlotId("image");
      const addPatch: LayoutPatch = {
        target: slotId,
        op: "add",
        value: {
          kind: "image",
          region_id: regionId,
          content: { href, x, y, width, height, preserve_aspect_ratio: "xMidYMid meet" },
        },
      };
      const inserted = await commitHistoryPatches("Insert image", [addPatch], [{ target: slotId, op: "delete" }], { format: false });
      if (inserted) setState({ selectedIds: [slotId], activeTool: "select" });
      return inserted;
    } catch (error) {
      setState({ error: toEditorError(error) });
      return false;
    }
  }

  async function saveDslDraft(): Promise<boolean> {
    if (!state.problemId || state.saving || state.loading) return false;
    setState({ saving: true, error: null, statusMessage: "Saving DSL..." });
    try {
      const response = await saveDsl(state.problemId, state.dslDraft);
      const current = state.document?.detail;
      if (current) {
        applyProblemDetail({ ...current, problem_id: response.problem_id, dsl: response.dsl });
      }
      setState({ saving: false, dirty: false, statusMessage: "DSL saved." });
      return true;
    } catch (error) {
      setState({ saving: false, error: toEditorError(error), statusMessage: "Could not save DSL." });
      return false;
    }
  }

  async function formatDslDraft(): Promise<boolean> {
    if (!state.problemId || state.formatting || state.loading) return false;
    setState({ formatting: true, error: null, statusMessage: "Formatting DSL..." });
    const saved = await saveDslDraft();
    if (!saved) {
      setState({ formatting: false, statusMessage: "Could not format DSL." });
      return false;
    }
    try {
      const response = await formatDsl(state.problemId);
      const current = state.document?.detail;
      if (current) {
        applyProblemDetail({ ...current, problem_id: response.problem_id, dsl: response.dsl });
      }
      setState({ formatting: false, dirty: false, statusMessage: "DSL formatted." });
      return true;
    } catch (error) {
      setState({ formatting: false, error: toEditorError(error), statusMessage: "Could not format DSL." });
      return false;
    }
  }

  async function buildCurrentProblem(): Promise<boolean> {
    if (!state.problemId || state.building || state.loading) return false;
    setState({ building: true, error: null, buildOutput: null, statusMessage: "Building artifacts..." });
    try {
      const response = await buildProblem(state.problemId);
      applyBuildResponse(response);
      setState({ building: false, statusMessage: response.ok ? "Build complete." : "Build finished with errors." });
      await refreshProblems();
      return true;
    } catch (error) {
      const apiError = toEditorError(error);
      setState({ building: false, error: apiError, statusMessage: "Build failed." });
      if (error instanceof EditorApiError) {
        const payload = error.payload as Partial<BuildProblemResponse> | null;
        if (payload?.stdout !== undefined || payload?.stderr !== undefined || payload?.error) {
          setState({
            buildOutput: {
              ok: false,
              stdout: payload.stdout ?? "",
              stderr: payload.stderr ?? "",
              error: payload.error ?? apiError.message,
            },
          });
        }
      }
      return false;
    }
  }

  async function applyManualPatch(target: string, valueSource: string, build: boolean): Promise<boolean> {
    if (!state.problemId || state.loading) return false;
    const slotId = target.trim();
    if (!slotId) {
      setState({ error: { message: "Slot id is required.", category: "DSL_PATCH_ERROR", status: 400 }, statusMessage: "Patch needs a slot id." });
      return false;
    }
    let value: unknown;
    try {
      value = JSON.parse(valueSource);
    } catch (error) {
      setState({ error: { message: `Invalid patch JSON: ${String(error)}`, category: "DSL_PATCH_ERROR", status: 400 }, statusMessage: "Patch JSON is invalid." });
      return false;
    }
    if (!isRecord(value)) {
      setState({ error: { message: "Patch value must be a JSON object.", category: "DSL_PATCH_ERROR", status: 400 }, statusMessage: "Patch value must be an object." });
      return false;
    }
    const patches: LayoutPatch[] = [{ target: slotId, op: "update", value }];
    if (build) return patchAndBuild(patches, { format: false });

    setState({ loading: true, error: null, statusMessage: "Applying manual patch..." });
    try {
      const response = await applyLayoutPatches(state.problemId, patches, { format: false });
      const current = state.document?.detail;
      if (current) {
        applyProblemDetail({ ...current, problem_id: response.problem_id, dsl: response.dsl });
      }
      setState({
        loading: false,
        dirty: false,
        buildOutput: {
          ok: true,
          stdout: `Applied ${response.applied.length} patch${response.applied.length === 1 ? "" : "es"}.`,
          stderr: "",
        },
      });
      setState({ statusMessage: "Manual patch applied." });
      return true;
    } catch (error) {
      setState({ loading: false, error: toEditorError(error), statusMessage: "Could not apply manual patch." });
      return false;
    }
  }

  async function undo(): Promise<boolean> {
    if (state.loading || state.historyBusy) return false;
    const previousHistory = state.history;
    const { entry, history } = popUndoEntry(state.history);
    if (!entry) return false;
    setState({ history, historyBusy: true, statusMessage: `Undoing ${entry.label}...` });
    const applied = await patchAndBuild(entry.before, { format: false });
    setState({ historyBusy: false });
    if (!applied) {
      setState("history", previousHistory);
      return false;
    }
    setState({ statusMessage: `Undid ${entry.label}.` });
    return true;
  }

  async function redo(): Promise<boolean> {
    if (state.loading || state.historyBusy) return false;
    const previousHistory = state.history;
    const { entry, history } = popRedoEntry(state.history);
    if (!entry) return false;
    setState({ history, historyBusy: true, statusMessage: `Redoing ${entry.label}...` });
    const applied = await patchAndBuild(entry.after, { format: false });
    setState({ historyBusy: false });
    if (!applied) {
      setState("history", previousHistory);
      return false;
    }
    setState({ statusMessage: `Redid ${entry.label}.` });
    return true;
  }

  function findSlot(slotId: string): LayoutSlot | null {
    const resolved = resolveSlotId(slotId);
    return state.document?.slots.find((slot) => slot.id === resolved) ?? null;
  }

  function resolveSlotId(slotId: string): string {
    const slots = state.document?.slots ?? [];
    if (slots.some((slot) => slot.id === slotId)) return slotId;
    const stripped = rendererElementSlotTarget(slotId);
    if (slots.some((slot) => slot.id === stripped)) return stripped;
    const match = [...slots]
      .map((slot) => slot.id)
      .sort((left, right) => right.length - left.length)
      .find((candidate) => slotId.startsWith(`${candidate}.`));
    return match ?? stripped;
  }

  function rendererElementSlotTarget(slotId: string): string {
    return slotId.replace(/\.(text|line|rect|path|polygon|circle|image)$/i, "");
  }

  function uniqueIds(slotIds: string[]): string[] {
    return [...new Set(slotIds.filter(Boolean))];
  }

  function applyProblemDetail(detail: ProblemDetailResponse): void {
    setState({
      problemId: detail.problem_id,
      document: createEditorDocument(detail),
      dslDraft: detail.dsl,
    });
  }

  function optimisticallyRemoveDeletedSlots(deletedIds: string[]): void {
    const current = state.document?.detail;
    if (!current) return;
    applyProblemDetail(applyDeletedSlotsToDetail(current, deletedIds));
    setState({ selectedIds: clearSelection() });
  }

  function applyPatchBuildResponse(response: LayoutPatchBuildResponse, deletedIds: string[] = []): void {
    const current = state.document?.detail;
    const artifacts = response.artifacts ?? {};
    const detail = applyDeletedSlotsToDetail({
      problem_id: response.problem_id,
      base_dir: current?.base_dir ?? "",
      dsl: response.dsl,
      semantic: artifacts.semantic ?? current?.semantic ?? null,
      solvable: artifacts.solvable ?? current?.solvable ?? null,
      layout: artifacts.layout ?? current?.layout ?? null,
      renderer: artifacts.renderer ?? current?.renderer ?? null,
      svg: artifacts.svg ?? current?.svg ?? null,
      svg_url: current?.svg_url ?? null,
    }, deletedIds);
    applyProblemDetail(detail);
  }

  function applyDeletedSlotsToDetail(detail: ProblemDetailResponse, deletedIds: string[]): ProblemDetailResponse {
    const cleanIds = normalizeDeletedSlotIds(deletedIds);
    if (!cleanIds.length) return detail;
    return {
      ...detail,
      layout: removeDeletedSlotsFromLayout(detail.layout, cleanIds),
      renderer: removeDeletedSlotsFromRenderer(detail.renderer, cleanIds),
      svg: removeDeletedSlotsFromSvg(detail.svg, cleanIds),
    };
  }

  function normalizeDeletedSlotIds(deletedIds: string[]): string[] {
    const ids = new Set<string>();
    for (const slotId of deletedIds) {
      if (!slotId || slotId === "__canvas__") continue;
      ids.add(slotId);
      ids.add(slotId.replace(/\.(text|line|rect|path|polygon|circle|image)$/i, ""));
    }
    return [...ids].filter(Boolean);
  }

  function deletedSlotMatches(slotId: unknown, deletedIds: string[]): boolean {
    return typeof slotId === "string" && deletedIds.some((deletedId) => slotId === deletedId || slotId.startsWith(`${deletedId}.`));
  }

  function removeDeletedSlotsFromLayout(layout: LayoutDocument | null, deletedIds: string[]): LayoutDocument | null {
    if (!layout) return layout;
    return {
      ...layout,
      slots: layout.slots?.filter((slot) => !deletedSlotMatches(slot.id, deletedIds)) ?? layout.slots,
      regions: layout.regions?.map((region) => ({
        ...region,
        slot_ids: region.slot_ids?.filter((slotId) => !deletedSlotMatches(slotId, deletedIds)),
      })),
    };
  }

  function removeDeletedSlotsFromRenderer(renderer: RendererDocument | null, deletedIds: string[]): RendererDocument | null {
    if (!renderer) return renderer;
    const filterElements = (elements: RendererElement[] | undefined): RendererElement[] | undefined => {
      if (!elements) return elements;
      return elements
        .filter((element) => !rendererElementMatchesDeletedSlot(element, deletedIds))
        .map((element) => ({ ...element, elements: filterElements(element.elements) }));
    };
    return { ...renderer, elements: filterElements(renderer.elements) };
  }

  function rendererElementMatchesDeletedSlot(element: RendererElement, deletedIds: string[]): boolean {
    return (
      deletedSlotMatches(element.id, deletedIds) ||
      deletedSlotMatches(element.source_ref, deletedIds) ||
      deletedSlotMatches(element.refs?.layout_slot_id, deletedIds) ||
      deletedSlotMatches(element.attributes?.source_ref, deletedIds)
    );
  }

  function removeDeletedSlotsFromSvg(svg: string | null, deletedIds: string[]): string | null {
    if (!svg) return svg;
    try {
      const doc = new DOMParser().parseFromString(svg, "image/svg+xml");
      const root = doc.documentElement;
      if (!root || root.nodeName.toLowerCase() !== "svg") return svg;
      const nodes = Array.from(root.querySelectorAll("[id], [data-slot-id], [data-layout-slot-id]"));
      for (const node of nodes) {
        const id = node.getAttribute("id");
        const slotId = node.getAttribute("data-slot-id") ?? node.getAttribute("data-layout-slot-id");
        if (deletedSlotMatches(id, deletedIds) || deletedSlotMatches(slotId, deletedIds)) {
          node.parentNode?.removeChild(node);
        }
      }
      return new XMLSerializer().serializeToString(root);
    } catch {
      return svg;
    }
  }

  function applyBuildResponse(response: BuildProblemResponse): void {
    const current = state.document?.detail;
    const artifacts = response.artifacts ?? {};
    if (current) {
      applyProblemDetail({
        problem_id: response.problem_id,
        base_dir: current.base_dir,
        dsl: state.dslDraft,
        semantic: artifacts.semantic ?? current.semantic,
        solvable: artifacts.solvable ?? current.solvable,
        layout: artifacts.layout ?? current.layout,
        renderer: artifacts.renderer ?? current.renderer,
        svg: artifacts.svg ?? current.svg,
        svg_url: current.svg_url ?? null,
      });
    }
    setState({
      buildOutput: {
        ok: response.ok,
        stdout: response.stdout,
        stderr: response.stderr,
        error: response.error,
      },
    });
  }

  function setDslDraft(dslDraft: string): void {
    setState({ dslDraft, dirty: dslDraft !== (state.document?.dslSource ?? "") });
  }

  function isRecord(value: unknown): value is Record<string, unknown> {
    return typeof value === "object" && value !== null && !Array.isArray(value);
  }

  function isPatchBuildResponse(value: unknown): value is LayoutPatchBuildResponse {
    return isRecord(value) && typeof value.problem_id === "string" && typeof value.dsl === "string";
  }

  function regionIdForSlot(slotId: string): string | null {
    const resolved = resolveSlotId(slotId);
    const regions = state.document?.detail.layout?.regions ?? [];
    return regions.find((region) => region.slot_ids?.includes(resolved))?.id ?? preferredRegionId();
  }

  function addPatchForSlot(slot: LayoutSlot): LayoutPatch | null {
    const regionId = regionIdForSlot(slot.id);
    if (!regionId) return null;
    return {
      target: slot.id,
      op: "add",
      value: {
        kind: slot.kind,
        region_id: regionId,
        content: structuredClone(slot.content),
      },
    };
  }

  function commitSlotPropertyPatch(label: string, slot: LayoutSlot, properties: Record<string, unknown>): Promise<boolean> {
    return commitMultiSlotPropertyPatch(label, [slot], properties);
  }

  function commitMultiSlotPropertyPatch(label: string, slots: LayoutSlot[], properties: Record<string, unknown>): Promise<boolean> {
    const patches: LayoutPatch[] = [];
    const inversePatches: LayoutPatch[] = [];
    for (const slot of slots) {
      patches.push({ target: slot.id, op: "update", value: properties });
      inversePatches.push({ target: slot.id, op: "update", value: inverseAnyProperties(slot, properties) });
    }
    return commitHistoryPatches(label, patches, inversePatches, { format: false });
  }

  function expandGeneratedMoveIds(slotIds: string[]): string[] {
    const expanded = new Set<string>();
    const slots = state.document?.slots ?? [];
    for (const slotId of slotIds) {
      const base = generatedGroupBase(slotId);
      if (!base) {
        expanded.add(slotId);
        continue;
      }
      const groupIds = slots.filter((slot) => slot.id === base || slot.id.startsWith(`${base}.`)).map((slot) => slot.id);
      if (groupIds.length) groupIds.forEach((id) => expanded.add(id));
      else expanded.add(slotId);
    }
    return [...expanded];
  }

  function generatedGroupBase(slotId: string): string | null {
    const match = slotId.match(/^(slot\.(?:table|graph_paper|bar_model|tick_bar|mixed_fraction|fraction)(?:_\d+)?)(?:\.|$)/);
    return match?.[1] ?? null;
  }

  function generatedSelectionIds(slotId: string): string[] {
    const match = slotId.match(/^(slot\.(?:graph_paper|bar_model|tick_bar|mixed_fraction|fraction)(?:_\d+)?)(?:\.|$)/);
    const base = match?.[1];
    if (!base) return [];
    return (state.document?.slots ?? [])
      .filter((slot) => slot.id === base || slot.id.startsWith(`${base}.`))
      .map((slot) => slot.id);
  }

  function inverseAnyProperties(slot: LayoutSlot, properties: Record<string, unknown>): Record<string, unknown> {
    const inverse: Record<string, unknown> = {};
    const content = slot.content as Record<string, unknown>;
    for (const key of Object.keys(properties)) {
      const previous = content[key];
      inverse[key] = previous ?? defaultInverseValue(key);
    }
    return inverse;
  }

  function defaultInverseValue(key: string): string | number {
    if (key === "stroke_width" || key === "font_size") return 0;
    return "";
  }

  function inverseProperties(slot: LayoutSlot, properties: Record<string, unknown>): Record<string, unknown> {
    const inverse: Record<string, unknown> = {};
    const content = slot.content as Record<string, unknown>;
    for (const key of Object.keys(properties)) {
      const previous = content[key];
      if (previous !== undefined) inverse[key] = previous;
    }
    return inverse;
  }

  function isTextLikeSlot(slot: LayoutSlot): boolean {
    return slot.kind === "text" || slot.kind === "text_box";
  }

  function selectedShapeSlots(): LayoutSlot[] {
    return state.selectedIds
      .map((slotId) => findSlot(slotId))
      .filter((slot): slot is LayoutSlot => !!slot && ["rect", "circle", "line", "polygon", "path", "text_box"].includes(slot.kind));
  }

  function tableCellFillSlotId(slotId: string): string | null {
    const fillMatch = slotId.match(/^(slot\.table(?:_\d+)?\.r\d+c\d+)\.fill$/);
    if (fillMatch) return slotId;
    const textMatch = slotId.match(/^(slot\.table(?:_\d+)?\.r\d+c\d+)$/);
    if (textMatch) return `${textMatch[1]}.fill`;
    return null;
  }

  function tableRowsForBase(base: string): number[] {
    return tableIndicesForBase(base, "row");
  }

  function tableColsForBase(base: string): number[] {
    return tableIndicesForBase(base, "col");
  }

  function tableIndicesForBase(base: string, axis: "row" | "col"): number[] {
    const pattern = new RegExp(`^${escapeRegExp(base)}\\.r(\\d+)c(\\d+)\\.fill$`);
    const values = new Set<number>();
    for (const slot of state.document?.slots ?? []) {
      const match = slot.id.match(pattern);
      if (!match) continue;
      values.add(Number(match[axis === "row" ? 1 : 2]));
    }
    return [...values].filter(Number.isFinite).sort((a, b) => a - b);
  }

  function clampTableVerticalDivider(base: string, col: number, position: number, rows: number[]): number {
    let min = -Infinity;
    let max = Infinity;
    for (const row of rows) {
      const leftSlot = findSlot(`${base}.r${row}c${col}.fill`);
      const rightSlot = findSlot(`${base}.r${row}c${col + 1}.fill`);
      const left = leftSlot ? slotBounds(leftSlot) : null;
      const right = rightSlot ? slotBounds(rightSlot) : null;
      if (!left || !right) continue;
      min = Math.max(min, left.x + 12);
      max = Math.min(max, right.x + right.width - 12);
    }
    if (!Number.isFinite(min) || !Number.isFinite(max) || min > max) return roundedDelta(position);
    return roundedDelta(Math.max(min, Math.min(max, position)));
  }

  function clampTableHorizontalDivider(base: string, row: number, position: number, cols: number[]): number {
    let min = -Infinity;
    let max = Infinity;
    for (const col of cols) {
      const topSlot = findSlot(`${base}.r${row}c${col}.fill`);
      const bottomSlot = findSlot(`${base}.r${row + 1}c${col}.fill`);
      const top = topSlot ? slotBounds(topSlot) : null;
      const bottom = bottomSlot ? slotBounds(bottomSlot) : null;
      if (!top || !bottom) continue;
      min = Math.max(min, top.y + 12);
      max = Math.min(max, bottom.y + bottom.height - 12);
    }
    if (!Number.isFinite(min) || !Number.isFinite(max) || min > max) return roundedDelta(position);
    return roundedDelta(Math.max(min, Math.min(max, position)));
  }

  function tableTextBaselineOffset(slotId: string): number {
    const slot = findSlot(slotId);
    const fontSize = Number((slot?.content as Record<string, unknown> | undefined)?.font_size ?? 22);
    return Number.isFinite(fontSize) ? fontSize * 0.35 : 7.7;
  }

  function escapeRegExp(value: string): string {
    return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }

  function preferredRegionId(): string | null {
    const regions = state.document?.detail.layout?.regions ?? [];
    return (
      regions.find((region) => region.role === "diagram" || region.flow === "absolute")?.id ??
      regions.find((region) => typeof region.id === "string" && region.id.trim())?.id ??
      null
    );
  }

  function withRegion(value: Record<string, unknown>, regionId = preferredRegionId()): Record<string, unknown> {
    return regionId ? { ...value, region_id: regionId } : value;
  }

  function selectedSlotsWithBounds(): { slot: LayoutSlot; bounds: Box }[] {
    return state.selectedIds
      .map((slotId) => {
        const slot = findSlot(slotId);
        const bounds = slot ? slotBounds(slot) : null;
        return slot && bounds ? { slot, bounds } : null;
      })
      .filter((item): item is { slot: LayoutSlot; bounds: Box } => item !== null);
  }

  function boundsPropertiesForSlot(slot: LayoutSlot, box: Box): Record<string, unknown> | null {
    const x = roundedDelta(box.x);
    const y = roundedDelta(box.y);
    const width = Math.max(1, roundedDelta(box.width));
    const height = Math.max(1, roundedDelta(box.height));
    if (slot.kind === "rect" || slot.kind === "text_box" || slot.kind === "image") {
      return { x, y, width, height };
    }
    if (slot.kind === "text") {
      const content = slot.content as Record<string, unknown>;
      const next: Record<string, number> = { x, y };
      if (typeof content.max_width === "number") next.max_width = width;
      if (typeof content.font_size === "number") next.font_size = Math.max(1, height);
      return next;
    }
    if (slot.kind === "circle") {
      const r = Math.max(1, Math.min(width, height) / 2);
      return { cx: roundedDelta(x + width / 2), cy: roundedDelta(y + height / 2), r: roundedDelta(r) };
    }
    if (slot.kind === "line") {
      const content = slot.content as Record<string, unknown>;
      const x1 = typeof content.x1 === "number" ? content.x1 : x;
      const y1 = typeof content.y1 === "number" ? content.y1 : y;
      const x2 = typeof content.x2 === "number" ? content.x2 : x + width;
      const y2 = typeof content.y2 === "number" ? content.y2 : y + height;
      const leftToRight = x2 >= x1;
      const topToBottom = y2 >= y1;
      return {
        x1: leftToRight ? x : x + width,
        y1: topToBottom ? y : y + height,
        x2: leftToRight ? x + width : x,
        y2: topToBottom ? y + height : y,
      };
    }
    if (slot.kind === "polygon") {
      const content = slot.content as Record<string, unknown>;
      const current = slotBounds(slot);
      const points = Array.isArray(content.points) ? content.points : [];
      if (!current || !points.length) return null;
      return {
        points: points
          .map((point) => (Array.isArray(point) && point.length === 2 ? [Number(point[0]), Number(point[1])] : null))
          .filter((point): point is [number, number] => !!point && point.every(Number.isFinite))
          .map(([px, py]) => scalePointBetweenBoxes(px, py, current, { x, y, width, height })),
      };
    }
    if (slot.kind === "path") {
      const content = slot.content as Record<string, unknown>;
      const current = slotBounds(slot);
      if (!current || typeof content.d !== "string") return null;
      return { d: transformPathBetweenBoxes(content.d, current, { x, y, width, height }) };
    }
    return null;
  }

  function scalePointBetweenBoxes(px: number, py: number, from: Box, to: Box): [number, number] {
    const sx = to.width / Math.max(from.width, 1);
    const sy = to.height / Math.max(from.height, 1);
    return [roundedDelta(to.x + (px - from.x) * sx), roundedDelta(to.y + (py - from.y) * sy)];
  }

  function transformPathBetweenBoxes(d: string, from: Box, to: Box): string {
    const sx = to.width / Math.max(from.width, 1);
    const sy = to.height / Math.max(from.height, 1);
    const tokens = d.match(/[a-zA-Z]|[-+]?(?:\d+(?:\.\d*)?|\.\d+)/g) ?? [];
    const output: string[] = [];
    let index = 0;
    let command = "";
    const isCommand = (token: string) => /^[a-zA-Z]$/.test(token);
    const readNumber = () => Number(tokens[index++]);
    const fmt = (value: number) => String(roundedDelta(value));
    const mapX = (value: number, relative: boolean) => fmt(relative ? value * sx : to.x + (value - from.x) * sx);
    const mapY = (value: number, relative: boolean) => fmt(relative ? value * sy : to.y + (value - from.y) * sy);
    const mapRx = (value: number) => fmt(value * sx);
    const mapRy = (value: number) => fmt(value * sy);

    while (index < tokens.length) {
      const token = tokens[index++];
      if (isCommand(token)) {
        command = token;
        output.push(token);
      } else {
        index -= 1;
      }

      const upper = command.toUpperCase();
      const relative = command !== upper;
      if (upper === "M" || upper === "L" || upper === "T") {
        while (index < tokens.length && !isCommand(tokens[index])) output.push(mapX(readNumber(), relative), mapY(readNumber(), relative));
      } else if (upper === "H") {
        while (index < tokens.length && !isCommand(tokens[index])) output.push(mapX(readNumber(), relative));
      } else if (upper === "V") {
        while (index < tokens.length && !isCommand(tokens[index])) output.push(mapY(readNumber(), relative));
      } else if (upper === "C") {
        while (index < tokens.length && !isCommand(tokens[index])) output.push(mapX(readNumber(), relative), mapY(readNumber(), relative), mapX(readNumber(), relative), mapY(readNumber(), relative), mapX(readNumber(), relative), mapY(readNumber(), relative));
      } else if (upper === "S" || upper === "Q") {
        while (index < tokens.length && !isCommand(tokens[index])) output.push(mapX(readNumber(), relative), mapY(readNumber(), relative), mapX(readNumber(), relative), mapY(readNumber(), relative));
      } else if (upper === "A") {
        while (index < tokens.length && !isCommand(tokens[index])) output.push(mapRx(readNumber()), mapRy(readNumber()), fmt(readNumber()), fmt(readNumber()), fmt(readNumber()), mapX(readNumber(), relative), mapY(readNumber(), relative));
      } else if (upper === "Z") {
        continue;
      } else {
        while (index < tokens.length && !isCommand(tokens[index])) output.push(tokens[index++]);
      }
    }
    return output.join(" ");
  }

  function alignmentMetric(mode: AlignMode, boxes: Box[]): number {
    if (mode === "left") return Math.min(...boxes.map((box) => box.x));
    if (mode === "center") return average(boxes.map((box) => box.x + box.width / 2));
    if (mode === "right") return Math.max(...boxes.map((box) => box.x + box.width));
    if (mode === "top") return Math.min(...boxes.map((box) => box.y));
    if (mode === "middle") return average(boxes.map((box) => box.y + box.height / 2));
    return Math.max(...boxes.map((box) => box.y + box.height));
  }

  function canvasBox(): Box | null {
    const canvas = state.document?.detail.layout?.canvas;
    if (typeof canvas?.width === "number" && typeof canvas.height === "number") {
      return { x: 0, y: 0, width: canvas.width, height: canvas.height };
    }
    return null;
  }

  function average(values: number[]): number {
    return values.reduce((sum, value) => sum + value, 0) / values.length;
  }

  function roundedDelta(value: number): number {
    return Math.round(value * 100) / 100;
  }

  function clampDelta(value: number, min: number, max: number): number {
    return Math.max(min, Math.min(max, value));
  }

  function reorderLayerIds(order: string[], selectedIds: string[], mode: LayerMode): string[] {
    const selected = selectedIds.filter((id) => order.includes(id));
    if (!selected.length) return order;
    const selectedSet = new Set(selected);
    const rest = order.filter((id) => !selectedSet.has(id));
    if (mode === "front") return [...rest, ...selected];
    if (mode === "back") return [...selected, ...rest];

    const next = [...order];
    if (mode === "forward") {
      for (let i = next.length - 2; i >= 0; i -= 1) {
        if (!selectedSet.has(next[i]) || selectedSet.has(next[i + 1])) continue;
        [next[i], next[i + 1]] = [next[i + 1], next[i]];
      }
    } else {
      for (let i = 1; i < next.length; i += 1) {
        if (!selectedSet.has(next[i]) || selectedSet.has(next[i - 1])) continue;
        [next[i - 1], next[i]] = [next[i], next[i - 1]];
      }
    }
    return next;
  }

  function sameOrder(left: string[], right: string[]): boolean {
    return left.length === right.length && left.every((id, index) => id === right[index]);
  }

  function uniqueSlotId(kind: string): string {
    const existing = new Set(state.document?.slots.map((slot) => slot.id) ?? []);
    const suffix = (kind === "triangle" ? "polygon" : kind).replace(/[^a-z0-9_]+/gi, "_").toLowerCase() || "slot";
    let index = 1;
    let candidate = `slot.editor_next.${suffix}.${index}`;
    while (existing.has(candidate)) {
      index += 1;
      candidate = `slot.editor_next.${suffix}.${index}`;
    }
    return candidate;
  }

  function uniqueBase(prefix: string): string {
    const existing = new Set(state.document?.slots.map((slot) => slot.id) ?? []);
    const cleanPrefix = prefix.replace(/[^a-z0-9_.]+/gi, "_").replace(/^_+|_+$/g, "") || "slot.generated";
    if (![...existing].some((id) => id === cleanPrefix || id.startsWith(`${cleanPrefix}.`))) return cleanPrefix;
    let index = 1;
    let candidate = `${cleanPrefix}_${index}`;
    while ([...existing].some((id) => id === candidate || id.startsWith(`${candidate}.`))) {
      index += 1;
      candidate = `${cleanPrefix}_${index}`;
    }
    return candidate;
  }

  function patchKindForInsert(kind: InsertableShapeKind): string {
    return kind === "triangle" ? "polygon" : kind;
  }

  function shiftCopiedContent(content: Record<string, unknown>, dx: number, dy: number): Record<string, unknown> {
    const shifted = { ...content };
    for (const key of ["x", "x1", "x2", "cx"]) {
      if (typeof shifted[key] === "number") shifted[key] = shifted[key] + dx;
    }
    for (const key of ["y", "y1", "y2", "cy"]) {
      if (typeof shifted[key] === "number") shifted[key] = shifted[key] + dy;
    }
    if (Array.isArray(shifted.points)) {
      shifted.points = shifted.points.map((point) => {
        if (!Array.isArray(point) || point.length !== 2) return point;
        const [x, y] = point;
        return typeof x === "number" && typeof y === "number" ? [x + dx, y + dy] : point;
      });
    }
    if (typeof shifted.d === "string") {
      shifted.d = shiftPathData(shifted.d, dx, dy);
    }
    return shifted;
  }

  function movePropertiesForSlot(slot: LayoutSlot, dx: number, dy: number): Record<string, unknown> | null {
    const content = slot.content as Record<string, unknown>;
    const xDelta = roundedDelta(dx);
    const yDelta = roundedDelta(dy);
    const num = (key: string): number | null => {
      const value = content[key];
      return typeof value === "number" && Number.isFinite(value) ? value : null;
    };
    const shiftedNumber = (key: string, delta: number): number | null => {
      const value = num(key);
      return value === null ? null : roundedDelta(value + delta);
    };

    if (slot.kind === "text" || slot.kind === "text_box" || slot.kind === "rect" || slot.kind === "image") {
      const x = shiftedNumber("x", xDelta);
      const y = shiftedNumber("y", yDelta);
      return x === null || y === null ? null : { x, y };
    }
    if (slot.kind === "line") {
      const x1 = shiftedNumber("x1", xDelta);
      const y1 = shiftedNumber("y1", yDelta);
      const x2 = shiftedNumber("x2", xDelta);
      const y2 = shiftedNumber("y2", yDelta);
      return x1 === null || y1 === null || x2 === null || y2 === null ? null : { x1, y1, x2, y2 };
    }
    if (slot.kind === "circle") {
      const cx = shiftedNumber("cx", xDelta);
      const cy = shiftedNumber("cy", yDelta);
      return cx === null || cy === null ? null : { cx, cy };
    }
    if (slot.kind === "polygon") {
      const points = content.points;
      if (!Array.isArray(points)) return null;
      return {
        points: points.map((point) => {
          if (!Array.isArray(point) || typeof point[0] !== "number" || typeof point[1] !== "number") return point;
          return [roundedDelta(point[0] + xDelta), roundedDelta(point[1] + yDelta)];
        }),
      };
    }
    if (slot.kind === "path" && typeof content.d === "string") {
      return { d: shiftPathData(content.d, xDelta, yDelta) };
    }
    return null;
  }

  function shiftPathData(d: string, dx: number, dy: number): string {
    let numberIndex = 0;
    return d.replace(/[-+]?(?:\d+(?:\.\d*)?|\.\d+)/g, (raw) => {
      const value = Number(raw);
      if (!Number.isFinite(value)) return raw;
      const shifted = value + (numberIndex % 2 === 0 ? dx : dy);
      numberIndex += 1;
      return Number.isInteger(shifted) ? String(shifted) : String(Math.round(shifted * 1000) / 1000);
    });
  }

  function centeredOrigin(width: number, height: number, canvasWidth: number, canvasHeight: number): { x: number; y: number } {
    return {
      x: Math.round((canvasWidth / 2 - width / 2) * 10) / 10,
      y: Math.round((canvasHeight / 2 - height / 2) * 10) / 10,
    };
  }

  function insertedShapeContent(kind: InsertableShapeKind, canvasWidth: number, canvasHeight: number): Record<string, string | number | [number, number][]> {
    if (kind === "text_box") {
      const { x, y } = centeredOrigin(140, 40, canvasWidth, canvasHeight);
      return { text: "Text", x, y, width: 140, height: 40, font_size: 18, fill: "#17202a" };
    }
    if (kind === "circle") {
      const r = 34;
      return { cx: Math.round(canvasWidth / 2), cy: Math.round(canvasHeight / 2), r, fill: "none", stroke: "#2563eb", stroke_width: 2 };
    }
    if (kind === "line") {
      const { x, y } = centeredOrigin(120, 0, canvasWidth, canvasHeight);
      return { x1: x, y1: y, x2: x + 120, y2: y, stroke: "#2563eb", stroke_width: 2 };
    }
    if (kind === "triangle") {
      const { x, y } = centeredOrigin(120, 90, canvasWidth, canvasHeight);
      return {
        points: [
          [x + 60, y],
          [x + 120, y + 90],
          [x, y + 90],
        ],
        fill: "none",
        stroke: "#2563eb",
        stroke_width: 2,
      };
    }
    if (kind === "path") {
      const { x, y } = centeredOrigin(120, 70, canvasWidth, canvasHeight);
      return { d: `M ${x} ${y + 60} C ${x + 30} ${y}, ${x + 80} ${y + 90}, ${x + 120} ${y + 25}`, fill: "none", stroke: "#2563eb", stroke_width: 2 };
    }
    const { x, y } = centeredOrigin(120, 48, canvasWidth, canvasHeight);
    return { x, y, width: 120, height: 48, fill: "none", stroke: "#2563eb", stroke_width: 2 };
  }

  function galleryShapePayload(definition: GalleryShapeDefinition, canvasWidth: number, canvasHeight: number): { kind: GalleryShapeKind; content: Record<string, unknown> } {
    const width = Number(definition.w ?? 120);
    const height = Number(definition.h ?? (definition.kind === "line" ? 70 : 86));
    const { x, y } = centeredOrigin(width, height, canvasWidth, canvasHeight);
    const stroke = definition.stroke ?? "#111827";
    const fill = definition.fill ?? "#ffffff";
    const stroke_width = definition.stroke_width ?? 1.5;

    if (definition.kind === "line") {
      const horizontal = definition.line === "horizontal";
      const vertical = definition.line === "vertical";
      return {
        kind: "line",
        content: horizontal
          ? { x1: x, y1: y + height / 2, x2: x + width, y2: y + height / 2, stroke, stroke_width }
          : vertical
            ? { x1: x + width / 2, y1: y, x2: x + width / 2, y2: y + height, stroke, stroke_width }
            : { x1: x, y1: y + height, x2: x + width, y2: y, stroke, stroke_width },
      };
    }
    if (definition.kind === "rect") {
      return { kind: "rect", content: { x, y, width, height, rx: definition.rx, ry: definition.ry, fill, stroke, stroke_width } };
    }
    if (definition.kind === "circle") {
      const r = Number(definition.r ?? Math.min(width, height) / 2);
      return { kind: "circle", content: { cx: x + r, cy: y + r, r, fill, stroke, stroke_width } };
    }
    if (definition.kind === "polygon") {
      return {
        kind: "polygon",
        content: {
          points: scalePoints(definition.points ?? [], x, y, width, height, definition.sourceWidth ?? 64, definition.sourceHeight ?? 52),
          fill,
          stroke,
          stroke_width,
        },
      };
    }
    return {
      kind: "path",
      content: {
        d: scaleShapePath(definition.d ?? "", x, y, width, height, definition.sourceWidth ?? 64, definition.sourceHeight ?? 52),
        fill,
        stroke,
        stroke_width,
      },
    };
  }

  function compositeShapePatches(definition: GalleryShapeDefinition, regionId: string): { patches: LayoutPatch[]; selectId: string } {
    const fallbackWidth = Number(definition.w ?? definition.sourceWidth ?? 80);
    const fallbackHeight = Number(definition.h ?? definition.sourceHeight ?? fallbackWidth);
    const { x, y } = centeredOrigin(fallbackWidth, fallbackHeight, state.document?.detail.layout?.canvas?.width ?? 900, state.document?.detail.layout?.canvas?.height ?? 420);
    const base = uniqueBase(`slot.${definition.id}`);
    const patches = (definition.parts ?? []).map((part) => {
      const value = scaledCompositePart(part, x, y, fallbackWidth, fallbackHeight, definition.sourceWidth ?? fallbackWidth, definition.sourceHeight ?? fallbackHeight);
      return {
        target: `${base}.${part.id}`,
        op: "add" as const,
        value: {
          kind: value.kind,
          region_id: regionId,
          content: value.content,
        },
      };
    });
    return { patches, selectId: patches[0]?.target ?? base };
  }

  function drawnShapeContent(definition: GalleryShapeDefinition, points: Point[]): { kind: GalleryShapeKind; content: Record<string, unknown> } | null {
    const start = snappedCanvasPoint(points[0]);
    const end = snappedCanvasPoint(points[points.length - 1]);
    const stroke = definition.stroke ?? "#111827";
    const fill = definition.fill ?? "none";
    const stroke_width = definition.stroke_width ?? 1.5;
    if (definition.kind === "line") {
      return { kind: "line", content: { x1: start.x, y1: start.y, x2: end.x, y2: end.y, stroke, stroke_width } };
    }
    if (definition.id === "elbow") {
      return { kind: "path", content: { d: `M ${start.x} ${start.y} L ${end.x} ${start.y} L ${end.x} ${end.y}`, fill: "none", stroke, stroke_width } };
    }
    if (definition.id === "freeform") {
      const cleanPoints = points.map(snappedCanvasPoint).filter((point, index, list) => index === 0 || point.x !== list[index - 1].x || point.y !== list[index - 1].y);
      if (cleanPoints.length < 2) return null;
      const [first, ...rest] = cleanPoints;
      return { kind: "path", content: { d: [`M ${first.x} ${first.y}`, ...rest.map((point) => `L ${point.x} ${point.y}`)].join(" "), fill: "none", stroke, stroke_width } };
    }
    if (definition.kind === "path") {
      const dx = end.x - start.x;
      const dy = end.y - start.y;
      const c1 = { x: snappedCanvasNumber(start.x + dx * 0.25), y: snappedCanvasNumber(start.y - Math.max(20, Math.abs(dy) * 0.6)) };
      const c2 = { x: snappedCanvasNumber(start.x + dx * 0.75), y: snappedCanvasNumber(end.y + Math.max(20, Math.abs(dy) * 0.6)) };
      return { kind: "path", content: { d: `M ${start.x} ${start.y} C ${c1.x} ${c1.y}, ${c2.x} ${c2.y}, ${end.x} ${end.y}`, fill, stroke, stroke_width } };
    }
    return null;
  }

  function snappedCanvasPoint(point: Point): Point {
    return { x: snappedCanvasNumber(point.x), y: snappedCanvasNumber(point.y) };
  }

  function snappedCanvasNumber(value: number): number {
    if (!state.snapEnabled) return Math.round(value * 100) / 100;
    return Math.round(value / 5) * 5;
  }

  function scaledCompositePart(part: GalleryShapePart, x: number, y: number, width: number, height: number, sourceWidth: number, sourceHeight: number): { kind: GalleryShapeKind; content: Record<string, unknown> } {
    const sx = width / sourceWidth;
    const sy = height / sourceHeight;
    const content: Record<string, unknown> = {};
    for (const [key, value] of Object.entries(part)) {
      if (key === "id" || key === "kind") continue;
      content[key] = value;
    }
    if (part.kind === "rect") {
      content.x = snapValue(x + Number(part.x ?? 0) * sx);
      content.y = snapValue(y + Number(part.y ?? 0) * sy);
      content.width = snapValue(Number(part.width ?? 0) * sx);
      content.height = snapValue(Number(part.height ?? 0) * sy);
      if (part.rx !== undefined) content.rx = snapValue(Number(part.rx || 0) * sx);
      if (part.ry !== undefined) content.ry = snapValue(Number(part.ry || 0) * sy);
    } else if (part.kind === "circle") {
      content.cx = snapValue(x + Number(part.cx ?? 0) * sx);
      content.cy = snapValue(y + Number(part.cy ?? 0) * sy);
      content.r = snapValue(Number(part.r ?? 0) * Math.min(sx, sy));
    } else if (part.kind === "line") {
      content.x1 = snapValue(x + Number(part.x1 ?? 0) * sx);
      content.y1 = snapValue(y + Number(part.y1 ?? 0) * sy);
      content.x2 = snapValue(x + Number(part.x2 ?? 0) * sx);
      content.y2 = snapValue(y + Number(part.y2 ?? 0) * sy);
    } else if (part.kind === "polygon") {
      content.points = scalePoints(part.points ?? [], x, y, width, height, sourceWidth, sourceHeight);
    } else if (part.kind === "path") {
      content.d = scaleShapePath(part.d ?? "", x, y, width, height, sourceWidth, sourceHeight);
    }
    return { kind: part.kind, content };
  }

  function scalePoints(points: [number, number][], x: number, y: number, width: number, height: number, sourceWidth: number, sourceHeight: number): [number, number][] {
    return points.map(([px, py]) => [snapValue(x + (px / sourceWidth) * width), snapValue(y + (py / sourceHeight) * height)]);
  }

  function scaleShapePath(d: string, x: number, y: number, width: number, height: number, sourceWidth: number, sourceHeight: number): string {
    const sx = width / sourceWidth;
    const sy = height / sourceHeight;
    const tokens = d.match(/[a-zA-Z]|[-+]?(?:\d+(?:\.\d*)?|\.\d+)/g) ?? [];
    const output: string[] = [];
    let index = 0;
    let command = "";
    const readNumber = () => Number(tokens[index++]);
    const scaled = (value: number, axis: "x" | "y" | "rx" | "ry") => {
      const next = axis === "x" ? x + value * sx : axis === "y" ? y + value * sy : axis === "rx" ? value * sx : value * sy;
      return Number.isInteger(next) ? String(next) : String(Math.round(next * 1000) / 1000);
    };

    while (index < tokens.length) {
      const token = tokens[index++];
      if (/^[a-zA-Z]$/.test(token)) {
        command = token;
        output.push(token);
      } else {
        index -= 1;
      }

      const upper = command.toUpperCase();
      const relative = command !== upper;
      const scaleX = (value: number) => (relative ? scaled(value, "rx") : scaled(value, "x"));
      const scaleY = (value: number) => (relative ? scaled(value, "ry") : scaled(value, "y"));
      if (upper === "M" || upper === "L" || upper === "T") {
        while (index < tokens.length && !/^[a-zA-Z]$/.test(tokens[index])) output.push(scaleX(readNumber()), scaleY(readNumber()));
      } else if (upper === "H") {
        while (index < tokens.length && !/^[a-zA-Z]$/.test(tokens[index])) output.push(scaleX(readNumber()));
      } else if (upper === "V") {
        while (index < tokens.length && !/^[a-zA-Z]$/.test(tokens[index])) output.push(scaleY(readNumber()));
      } else if (upper === "C") {
        while (index < tokens.length && !/^[a-zA-Z]$/.test(tokens[index])) output.push(scaleX(readNumber()), scaleY(readNumber()), scaleX(readNumber()), scaleY(readNumber()), scaleX(readNumber()), scaleY(readNumber()));
      } else if (upper === "S" || upper === "Q") {
        while (index < tokens.length && !/^[a-zA-Z]$/.test(tokens[index])) output.push(scaleX(readNumber()), scaleY(readNumber()), scaleX(readNumber()), scaleY(readNumber()));
      } else if (upper === "A") {
        while (index < tokens.length && !/^[a-zA-Z]$/.test(tokens[index])) output.push(scaled(readNumber(), "rx"), scaled(readNumber(), "ry"), String(readNumber()), String(readNumber()), String(readNumber()), scaleX(readNumber()), scaleY(readNumber()));
      } else if (upper === "Z") {
        continue;
      } else {
        while (index < tokens.length && !/^[a-zA-Z]$/.test(tokens[index])) output.push(tokens[index++]);
      }
    }
    return output.join(" ");
  }

  function tablePatches(rows: number, cols: number): { base: string; patches: LayoutPatch[] } {
    const cleanRows = clampInt(rows, 1, 20, 2);
    const cleanCols = clampInt(cols, 1, 20, 5);
    const cellWidth = 105;
    const cellHeight = 58;
    const width = cleanCols * cellWidth;
    const height = cleanRows * cellHeight;
    const { x, y } = defaultInsertOrigin(width, height);
    const base = uniqueBase("slot.table");
    const regionId = preferredRegionId();
    const patches: LayoutPatch[] = [
      {
        target: `${base}.outer`,
        op: "add",
        value: withRegion({ kind: "rect", content: { x, y, width, height, fill: "#ffffff", stroke: "#111827", stroke_width: 1 } }, regionId),
      },
    ];

    for (let row = 1; row <= cleanRows; row += 1) {
      for (let col = 1; col <= cleanCols; col += 1) {
        patches.push({
          target: `${base}.r${row}c${col}.fill`,
          op: "add",
          value: withRegion({
            kind: "rect",
            content: {
              x: snapValue(x + (col - 1) * cellWidth),
              y: snapValue(y + (row - 1) * cellHeight),
              width: cellWidth,
              height: cellHeight,
              fill: "none",
              stroke: "none",
              stroke_width: 0,
            },
          }, regionId),
        });
      }
    }
    for (let col = 1; col < cleanCols; col += 1) {
      const px = snapValue(x + col * cellWidth);
      patches.push({
        target: `${base}.v${col}`,
        op: "add",
        value: withRegion({ kind: "line", content: { x1: px, y1: y, x2: px, y2: y + height, stroke: "#111827", stroke_width: 1 } }, regionId),
      });
    }
    for (let row = 1; row < cleanRows; row += 1) {
      const py = snapValue(y + row * cellHeight);
      patches.push({
        target: `${base}.h${row}`,
        op: "add",
        value: withRegion({ kind: "line", content: { x1: x, y1: py, x2: x + width, y2: py, stroke: "#111827", stroke_width: 1 } }, regionId),
      });
    }
    for (let row = 1; row <= cleanRows; row += 1) {
      for (let col = 1; col <= cleanCols; col += 1) {
        const fontSize = 22;
        const baselineOffset = cellHeight / 2 + fontSize * 0.35;
        patches.push({
          target: `${base}.r${row}c${col}`,
          op: "add",
          value: withRegion({
            kind: "text",
            content: {
              text: "",
              x: snapValue(x + (col - 0.5) * cellWidth),
              y: snapValue(y + (row - 1) * cellHeight + baselineOffset),
              font_size: fontSize,
              max_width: Math.max(8, cellWidth - 20),
              anchor: "middle",
              style_role: "table",
              fill: "#111827",
            },
          }, regionId),
        });
      }
    }
    return { base, patches };
  }

  function graphPaperPatches(rows: number, cols: number): { base: string; patches: LayoutPatch[] } {
    const cleanRows = clampInt(rows, 1, 40, 8);
    const cleanCols = clampInt(cols, 1, 40, 10);
    const cellSize = 25;
    const width = cleanCols * cellSize;
    const height = cleanRows * cellSize;
    const { x, y } = defaultInsertOrigin(width, height);
    const originX = snapValue(x);
    const originY = snapValue(y);
    const base = uniqueBase("slot.graph_paper");
    const regionId = preferredRegionId();
    const patches: LayoutPatch[] = [];
    for (let col = 0; col <= cleanCols; col += 1) {
      const px = originX + col * cellSize;
      patches.push({
        target: `${base}.v${col}`,
        op: "add",
        value: withRegion({ kind: "line", content: { x1: px, y1: originY, x2: px, y2: originY + height, stroke: "#2563eb", stroke_width: 1 } }, regionId),
      });
    }
    for (let row = 0; row <= cleanRows; row += 1) {
      const py = originY + row * cellSize;
      patches.push({
        target: `${base}.h${row}`,
        op: "add",
        value: withRegion({ kind: "line", content: { x1: originX, y1: py, x2: originX + width, y2: py, stroke: "#2563eb", stroke_width: 1 } }, regionId),
      });
    }
    return { base, patches };
  }

  function barModelPatches(options: BarModelOptions): { base: string; patches: LayoutPatch[] } {
    const cleanBars = clampInt(options.bars, 1, 8, 2);
    const cleanCells = clampInt(options.cells, 1, 20, 3);
    const shadedList = configList(options.shadedCounts ?? "2,2");
    const colorList = configList(options.fillColors ?? "#f3d7ea");
    const cellWidth = 58;
    const barHeight = 40;
    const barGap = 54;
    const width = cleanCells * cellWidth;
    const height = cleanBars * barHeight + (cleanBars - 1) * barGap;
    const { x, y } = defaultInsertOrigin(width, height);
    const base = uniqueBase("slot.bar_model");
    const regionId = preferredRegionId();
    const strokeColor = String(options.stroke || "#666666").trim() || "#666666";
    const dashed = options.dashed ?? true;
    const patches: LayoutPatch[] = [];

    for (let barIndex = 0; barIndex < cleanBars; barIndex += 1) {
      const barY = snapValue(y + barIndex * (barHeight + barGap));
      const shaded = clampInt(configListValue(shadedList, barIndex, "0"), 0, cleanCells, 0);
      const fill = String(configListValue(colorList, barIndex, "#f3d7ea") || "#f3d7ea").trim() || "#f3d7ea";
      for (let cellIndex = 0; cellIndex < shaded; cellIndex += 1) {
        patches.push({
          target: `${base}.bar${barIndex + 1}.shade${cellIndex + 1}`,
          op: "add",
          value: withRegion({
            kind: "rect",
            content: {
              x: snapValue(x + cellIndex * cellWidth),
              y: barY,
              width: cellWidth,
              height: barHeight,
              fill,
              stroke: "none",
              stroke_width: 0,
            },
          }, regionId),
        });
      }
      patches.push({
        target: `${base}.bar${barIndex + 1}.outline`,
        op: "add",
        value: withRegion({ kind: "rect", content: { x, y: barY, width, height: barHeight, fill: "none", stroke: strokeColor, stroke_width: 1.5 } }, regionId),
      });
      for (let cellIndex = 1; cellIndex < cleanCells; cellIndex += 1) {
        const px = snapValue(x + cellIndex * cellWidth);
        patches.push({
          target: `${base}.bar${barIndex + 1}.div${cellIndex}`,
          op: "add",
          value: withRegion({
            kind: "line",
            content: {
              x1: px,
              y1: barY,
              x2: px,
              y2: snapValue(barY + barHeight),
              stroke: strokeColor,
              stroke_width: 1,
              ...(dashed ? { stroke_dasharray: "5 3" } : {}),
            },
          }, regionId),
        });
      }
    }
    return { base, patches };
  }

  function tickBarPatches(options: TickBarOptions): { base: string; patches: LayoutPatch[] } {
    const cleanRows = clampInt(options.rows, 1, 8, 2);
    const cleanTotal = clampInt(options.totalTicks, 1, 40, 14);
    const cleanMajor = clampInt(options.majorEvery, 0, cleanTotal, 7);
    const filledList = configList(options.filledTicks ?? "9,10");
    const labelList = configList(options.labels ?? "");
    const width = 464;
    const rowGap = 96;
    const labelWidth = 118;
    const height = Math.max(70, (cleanRows - 1) * rowGap + 82);
    const { x, y } = defaultInsertOrigin(labelWidth + width, height);
    const axisX = snapValue(x + labelWidth);
    const base = uniqueBase("slot.tick_bar");
    const regionId = preferredRegionId();
    const stroke = String(options.axisColor || "#111111").trim() || "#111111";
    const fill = String(options.fillColor || "#2563eb").trim() || "#2563eb";
    const step = width / cleanTotal;
    const unitText = String(options.unit || "").trim();
    const showScaleLabels = options.showScaleLabels ?? true;
    const showFractionLabel = options.showFractionLabel ?? true;
    const patches: LayoutPatch[] = [];

    for (let rowIndex = 0; rowIndex < cleanRows; rowIndex += 1) {
      const rowBase = `${base}.row${rowIndex + 1}`;
      const axisY = snapValue(y + 30 + rowIndex * rowGap);
      const filled = clampInt(configListValue(filledList, rowIndex, "0"), 0, cleanTotal, 0);
      const rowLabel = String(configListValue(labelList, rowIndex, "") || "").trim();
      if (rowLabel) {
        patches.push({
          target: `${rowBase}.label`,
          op: "add",
          value: withRegion({ kind: "text", content: { text: rowLabel, x: snapValue(x), y: snapValue(axisY + 9), font_size: 28, style_role: "label", fill: stroke } }, regionId),
        });
      }
      if (filled > 0) {
        patches.push({
          target: `${rowBase}.fill`,
          op: "add",
          value: withRegion({ kind: "line", content: { x1: axisX, y1: axisY, x2: snapValue(axisX + filled * step), y2: axisY, stroke: fill, stroke_width: 8 } }, regionId),
        });
      }
      patches.push({
        target: `${rowBase}.axis`,
        op: "add",
        value: withRegion({ kind: "line", content: { x1: axisX, y1: axisY, x2: snapValue(axisX + width), y2: axisY, stroke, stroke_width: 2 } }, regionId),
      });
      for (let tick = 0; tick <= cleanTotal; tick += 1) {
        const isMajor = cleanMajor > 0 && tick % cleanMajor === 0;
        const tickHeight = isMajor ? 18 : 14;
        const px = snapValue(axisX + tick * step);
        patches.push({
          target: `${rowBase}.tick${tick}`,
          op: "add",
          value: withRegion({ kind: "line", content: { x1: px, y1: snapValue(axisY - tickHeight / 2), x2: px, y2: snapValue(axisY + tickHeight / 2), stroke, stroke_width: 2 } }, regionId),
        });
        if (isMajor && showScaleLabels) {
          const value = cleanMajor > 0 ? tick / cleanMajor : tick;
          const label = tick === cleanTotal && unitText ? `${value}(${unitText})` : String(value);
          patches.push({
            target: `${rowBase}.label${tick}`,
            op: "add",
            value: withRegion({ kind: "text", content: { text: label, x: snapValue(px - (tick === 0 ? 6 : tick === cleanTotal ? 14 : 8)), y: snapValue(axisY + 34), font_size: 26, style_role: "label", fill: stroke } }, regionId),
          });
        }
      }
      if (showFractionLabel && cleanMajor > 0 && cleanMajor < cleanTotal) {
        patches.push({
          target: `${rowBase}.major_fraction`,
          op: "add",
          value: withRegion({ kind: "text", content: { text: `${cleanMajor}/${cleanMajor}`, x: snapValue(axisX + cleanMajor * step - 18), y: snapValue(axisY - 22), font_size: 24, style_role: "label", fill: stroke } }, regionId),
        });
      }
    }
    return { base, patches };
  }

  function fractionPatches(options: FractionInsertOptions): { base: string; patches: LayoutPatch[] } {
    const mixed = options.mixed ?? false;
    const wholeText = cleanMathText(options.whole, "1");
    const numeratorText = cleanMathText(options.numerator, "1");
    const denominatorText = cleanMathText(options.denominator, "2");
    const fontSize = 30;
    const barWidth = 42;
    const width = mixed ? 88 : 54;
    const height = 72;
    const { x, y } = selectedInsertOrigin(width, height) ?? defaultInsertOrigin(width, height);
    const fractionX = mixed ? snapValue(x + 58) : snapValue(x + width / 2);
    const base = uniqueBase(mixed ? "slot.mixed_fraction" : "slot.fraction");
    const regionId = regionIdForSelection() ?? preferredRegionId();
    const patches: LayoutPatch[] = [];

    if (mixed) {
      patches.push({
        target: `${base}.whole`,
        op: "add",
        value: withRegion({ kind: "text", content: { text: wholeText, x: snapValue(x + 18), y: snapValue(y + 44), font_size: fontSize, anchor: "middle", style_role: "body", fill: "#222222" } }, regionId),
      });
    }
    patches.push({
      target: `${base}.num`,
      op: "add",
      value: withRegion({ kind: "text", content: { text: numeratorText, x: fractionX, y: snapValue(y + 22), font_size: fontSize, anchor: "middle", style_role: "body", fill: "#222222" } }, regionId),
    });
    patches.push({
      target: `${base}.bar`,
      op: "add",
      value: withRegion({ kind: "line", content: { x1: snapValue(fractionX - barWidth / 2), y1: snapValue(y + 36), x2: snapValue(fractionX + barWidth / 2), y2: snapValue(y + 36), stroke: "#222222", stroke_width: 2.2 } }, regionId),
    });
    patches.push({
      target: `${base}.den`,
      op: "add",
      value: withRegion({ kind: "text", content: { text: denominatorText, x: fractionX, y: snapValue(y + 58), font_size: fontSize, anchor: "middle", style_role: "body", fill: "#222222" } }, regionId),
    });
    return { base, patches };
  }

  function defaultInsertOrigin(width: number, height: number): { x: number; y: number } {
    const canvas = state.document?.detail.layout?.canvas;
    return {
      x: snapValue(Math.max(10, ((canvas?.width ?? 900) - width) / 2)),
      y: snapValue(Math.max(10, ((canvas?.height ?? 420) - height) / 2)),
    };
  }

  function selectedInsertOrigin(width: number, height: number): { x: number; y: number } | null {
    if (state.selectedIds.length !== 1) return null;
    const slot = findSlot(state.selectedIds[0]);
    const box = slot ? slotBounds(slot) : null;
    if (!box) return null;
    return { x: snapValue(box.x + box.width / 2 - width / 2), y: snapValue(box.y + box.height / 2 - height / 2) };
  }

  function regionIdForSelection(): string | null {
    return state.selectedIds.length === 1 ? regionIdForSlot(state.selectedIds[0]) : null;
  }

  function snapValue(value: number): number {
    if (!state.snapEnabled) return Math.round(value * 100) / 100;
    return Math.round(value / 5) * 5;
  }

  function clampInt(value: unknown, min: number, max: number, fallback: number): number {
    const numeric = Number(value);
    const clean = Number.isFinite(numeric) ? Math.trunc(numeric) : fallback;
    return Math.max(min, Math.min(max, clean));
  }

  function configList(value: unknown): string[] {
    return String(value ?? "").split(",").map((item) => item.trim()).filter(Boolean);
  }

  function configListValue(items: string[], index: number, fallback: string): string {
    if (!items.length) return fallback;
    return items[Math.min(index, items.length - 1)] || fallback;
  }

  function cleanMathText(value: unknown, fallback: string): string {
    const text = String(value ?? "").trim();
    return text || fallback;
  }

  function readFileAsDataUrl(file: File): Promise<string> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(String(reader.result || ""));
      reader.onerror = () => reject(reader.error || new Error("Could not read image file."));
      reader.readAsDataURL(file);
    });
  }

  function imageSizeFromDataUrl(href: string): Promise<{ width: number; height: number }> {
    return new Promise((resolve) => {
      const img = new Image();
      img.onload = () => resolve({ width: img.naturalWidth || 240, height: img.naturalHeight || 160 });
      img.onerror = () => resolve({ width: 240, height: 160 });
      img.src = href;
    });
  }

  function selectSlot(slotId: string, append = false): void {
    if (!append) {
      const groupIds = generatedSelectionIds(slotId);
      if (groupIds.length > 1) {
        setState({ selectedIds: groupIds, statusMessage: `Selected ${groupIds.length} generated slots.` });
        return;
      }
    }
    setState("selectedIds", (current) => toggleSelection(current, slotId, append));
    setState({ statusMessage: append ? `Toggled ${slotId}.` : `Selected ${slotId}.` });
  }

  function clearSelectedSlots(): void {
    setState({ selectedIds: clearSelection(), statusMessage: "Selection cleared." });
  }

  function setSelectedSlots(slotIds: string[]): void {
    setState({ selectedIds: slotIds, statusMessage: slotIds.length ? `Selected ${slotIds.length} slots.` : "Selection cleared." });
  }

  function setZoom(zoom: number): void {
    const nextZoom = Math.min(3, Math.max(0.25, Math.round(zoom * 100) / 100));
    setState({ zoom: nextZoom });
  }

  function setPan(panX: number, panY: number): void {
    setState({ panX, panY });
  }

  function setActiveTool(activeTool: EditorTool): void {
    setState({ activeTool, statusMessage: activeTool === "pan" ? "Pan tool active. Drag the canvas to move the view." : "Select tool active. Drag objects to move or resize them." });
  }

  function setPickMode(pickMode: EditorPickMode): void {
    setState({ pickMode, activeTool: "select", statusMessage: pickModeStatus(pickMode) });
  }

  function setSnapEnabled(snapEnabled: boolean): void {
    setState({ snapEnabled, statusMessage: snapEnabled ? "Snap enabled: movement uses 5px increments." : "Snap disabled: movement uses free positioning." });
  }

  function resetViewport(): void {
    setState({ zoom: 1, panX: 0, panY: 0, statusMessage: "Viewport reset." });
  }

  function setStatusMessage(statusMessage: string): void {
    setState({ statusMessage });
  }

  function pickModeStatus(pickMode: EditorPickMode): string {
    switch (pickMode) {
      case "text":
        return "Pick mode: text only.";
      case "shape":
        return "Pick mode: shapes only.";
      case "linepath":
        return "Pick mode: lines and paths only.";
      default:
        return "Pick mode: all objects.";
    }
  }

  return {
    state,
    refreshProblems,
    openProblem,
    patchAndBuild,
    commitHistoryPatches,
    moveSlots,
    moveSelectedSlots,
    deleteSelectedSlots,
    updateSlotProperties,
    updateSelectedBounds,
    updateSelectedTransform,
    updateSelectedText,
    nudgeSelectedFontSize,
    alignSelectedText,
    applyShapeFill,
    applyShapeStroke,
    applyShapeDash,
    applySelectedTableCellFill,
    updateTableDivider,
    updateCanvasSize,
    alignSelectedSlots,
    layerSelectedSlots,
    insertShape,
    insertGalleryShape,
    beginDrawShape,
    cancelDrawShape,
    insertDrawnShape,
    insertTable,
    insertGraphPaper,
    insertBarModel,
    insertTickBar,
    insertFractionExpression,
    insertImageFile,
    copySelectedSlots,
    pasteCopiedSlots,
    setDslDraft,
    saveDslDraft,
    formatDslDraft,
    buildCurrentProblem,
    applyManualPatch,
    undo,
    redo,
    selectSlot,
    clearSelectedSlots,
    setSelectedSlots,
    setZoom,
    setPan,
    setActiveTool,
    setPickMode,
    setSnapEnabled,
    resetViewport,
    setStatusMessage,
  };
}

export type EditorStore = ReturnType<typeof createEditorStore>;
