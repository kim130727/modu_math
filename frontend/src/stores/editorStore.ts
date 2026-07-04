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
import type { Box } from "../editor-core/model/geometry";
import { clearSelection, toggleSelection } from "../editor-core/selection/selectionManager";
import { slotBounds } from "../editor-core/transform/bounds";
import type { BuildOutputState, BuildProblemResponse, EditorError, LayoutPatch, ProblemDetailResponse, ProblemSummary } from "../types/api";
import type { LayoutSlot } from "../types/layout";

export type EditorTool = "select" | "pan";
export type EditorPickMode = "all" | "linepath" | "text" | "shape";
export type InsertableShapeKind = "rect" | "text_box" | "circle" | "line" | "triangle" | "path";
export type AlignMode = "left" | "center" | "right" | "top" | "middle" | "bottom";
export type LayerMode = "front" | "back" | "forward" | "backward";

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
    setState({ loading: true, error: null });
    try {
      const response = await listProblems();
      setState({ problems: response.problems, loading: false });
    } catch (error) {
      setState({ loading: false, error: toEditorError(error) });
    }
  }

  async function openProblem(problemId: string): Promise<void> {
    if (!problemId.trim()) return;
    setState({ loading: true, error: null, selectedIds: clearSelection() });
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
      });
      const url = new URL(window.location.href);
      url.searchParams.set("problem", detail.problem_id);
      window.history.replaceState(null, "", url);
    } catch (error) {
      setState({ loading: false, error: toEditorError(error) });
    }
  }

  async function patchAndBuild(patches: LayoutPatch[], options: { format?: boolean } = {}): Promise<boolean> {
    if (!state.problemId || patches.length === 0) return false;
    setState({ loading: true, error: null });
    try {
      const response = await applyLayoutPatchesAndBuild(state.problemId, patches, options);
      const current = state.document?.detail;
      const artifacts = response.artifacts ?? {};
      const detail: ProblemDetailResponse = {
        problem_id: response.problem_id,
        base_dir: current?.base_dir ?? "",
        dsl: response.dsl,
        semantic: artifacts.semantic ?? current?.semantic ?? null,
        solvable: artifacts.solvable ?? current?.solvable ?? null,
        layout: artifacts.layout ?? current?.layout ?? null,
        renderer: artifacts.renderer ?? current?.renderer ?? null,
        svg: artifacts.svg ?? current?.svg ?? null,
        svg_url: current?.svg_url ?? null,
      };
      applyProblemDetail(detail);
      setState({ dirty: false, loading: false });
      return true;
    } catch (error) {
      setState({ loading: false, error: toEditorError(error) });
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
    }
    return committed;
  }

  async function moveSlots(slotIds: string[], dx: number, dy: number, label = "Move"): Promise<boolean> {
    if (slotIds.length === 0 || state.loading) return false;
    const patches: LayoutPatch[] = slotIds.map((slotId) => ({
      target: slotId,
      op: "update",
      value: { move_dx: dx, move_dy: dy },
    }));
    const inversePatches: LayoutPatch[] = slotIds.map((slotId) => ({
      target: slotId,
      op: "update",
      value: { move_dx: -dx, move_dy: -dy },
    }));
    return commitHistoryPatches(label, patches, inversePatches, { format: false });
  }

  async function moveSelectedSlots(dx: number, dy: number): Promise<boolean> {
    if (state.selectedIds.length === 0 || state.loading) return false;
    return moveSlots(state.selectedIds, dx, dy, "Keyboard move");
  }

  async function deleteSelectedSlots(): Promise<boolean> {
    if (state.selectedIds.length === 0 || state.loading) return false;
    const inversePatches = state.selectedIds
      .map((slotId) => {
        const slot = findSlot(slotId);
        if (!slot) return null;
        return addPatchForSlot(slot);
      })
      .filter((patch): patch is LayoutPatch => patch !== null);
    if (inversePatches.length !== state.selectedIds.length) return false;
    const patches: LayoutPatch[] = state.selectedIds.map((slotId) => ({
      target: slotId,
      op: "delete",
    }));
    const deleted = await commitHistoryPatches("Delete", patches, inversePatches, { format: false });
    if (deleted) {
      setState({ selectedIds: clearSelection() });
    }
    return deleted;
  }

  async function updateSlotProperties(slotId: string, properties: Record<string, string | number>): Promise<boolean> {
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
      patches.push({ target: item.slot.id, op: "update", value: { move_dx: dx, move_dy: dy } });
      inversePatches.push({ target: item.slot.id, op: "update", value: { move_dx: -dx, move_dy: -dy } });
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

  function copySelectedSlots(): boolean {
    if (!state.document || state.selectedIds.length === 0) return false;
    copyBuffer = state.selectedIds
      .map((slotId) => findSlot(slotId))
      .filter((slot): slot is LayoutSlot => slot !== null)
      .map((slot) => structuredClone(slot));
    pasteSequence = 0;
    return copyBuffer.length > 0;
  }

  async function pasteCopiedSlots(): Promise<boolean> {
    if (!state.document || state.loading || copyBuffer.length === 0) return false;
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

    if (!patches.length) return false;
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
    setState({ saving: true, error: null });
    try {
      const response = await saveDsl(state.problemId, state.dslDraft);
      const current = state.document?.detail;
      if (current) {
        applyProblemDetail({ ...current, problem_id: response.problem_id, dsl: response.dsl });
      }
      setState({ saving: false, dirty: false });
      return true;
    } catch (error) {
      setState({ saving: false, error: toEditorError(error) });
      return false;
    }
  }

  async function formatDslDraft(): Promise<boolean> {
    if (!state.problemId || state.formatting || state.loading) return false;
    setState({ formatting: true, error: null });
    const saved = await saveDslDraft();
    if (!saved) {
      setState({ formatting: false });
      return false;
    }
    try {
      const response = await formatDsl(state.problemId);
      const current = state.document?.detail;
      if (current) {
        applyProblemDetail({ ...current, problem_id: response.problem_id, dsl: response.dsl });
      }
      setState({ formatting: false, dirty: false });
      return true;
    } catch (error) {
      setState({ formatting: false, error: toEditorError(error) });
      return false;
    }
  }

  async function buildCurrentProblem(): Promise<boolean> {
    if (!state.problemId || state.building || state.loading) return false;
    setState({ building: true, error: null, buildOutput: null });
    try {
      const response = await buildProblem(state.problemId);
      applyBuildResponse(response);
      setState({ building: false });
      await refreshProblems();
      return true;
    } catch (error) {
      const apiError = toEditorError(error);
      setState({ building: false, error: apiError });
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
      setState({ error: { message: "Slot id is required.", category: "DSL_PATCH_ERROR", status: 400 } });
      return false;
    }
    let value: unknown;
    try {
      value = JSON.parse(valueSource);
    } catch (error) {
      setState({ error: { message: `Invalid patch JSON: ${String(error)}`, category: "DSL_PATCH_ERROR", status: 400 } });
      return false;
    }
    if (!isRecord(value)) {
      setState({ error: { message: "Patch value must be a JSON object.", category: "DSL_PATCH_ERROR", status: 400 } });
      return false;
    }
    const patches: LayoutPatch[] = [{ target: slotId, op: "update", value }];
    if (build) return patchAndBuild(patches, { format: false });

    setState({ loading: true, error: null });
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
      return true;
    } catch (error) {
      setState({ loading: false, error: toEditorError(error) });
      return false;
    }
  }

  async function undo(): Promise<boolean> {
    if (state.loading || state.historyBusy) return false;
    const previousHistory = state.history;
    const { entry, history } = popUndoEntry(state.history);
    if (!entry) return false;
    setState({ history, historyBusy: true });
    const applied = await patchAndBuild(entry.before, { format: false });
    setState({ historyBusy: false });
    if (!applied) {
      setState("history", previousHistory);
      return false;
    }
    return true;
  }

  async function redo(): Promise<boolean> {
    if (state.loading || state.historyBusy) return false;
    const previousHistory = state.history;
    const { entry, history } = popRedoEntry(state.history);
    if (!entry) return false;
    setState({ history, historyBusy: true });
    const applied = await patchAndBuild(entry.after, { format: false });
    setState({ historyBusy: false });
    if (!applied) {
      setState("history", previousHistory);
      return false;
    }
    return true;
  }

  function findSlot(slotId: string): LayoutSlot | null {
    return state.document?.slots.find((slot) => slot.id === slotId) ?? null;
  }

  function applyProblemDetail(detail: ProblemDetailResponse): void {
    setState({
      problemId: detail.problem_id,
      document: createEditorDocument(detail),
      dslDraft: detail.dsl,
    });
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

  function regionIdForSlot(slotId: string): string | null {
    const regions = state.document?.detail.layout?.regions ?? [];
    return regions.find((region) => region.slot_ids?.includes(slotId))?.id ?? preferredRegionId();
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

  function inverseProperties(slot: LayoutSlot, properties: Record<string, string | number>): Record<string, string | number> {
    const inverse: Record<string, string | number> = {};
    const content = slot.content as Record<string, unknown>;
    for (const key of Object.keys(properties)) {
      const previous = content[key];
      if (typeof previous === "string" || typeof previous === "number") {
        inverse[key] = previous;
      }
    }
    return inverse;
  }

  function preferredRegionId(): string | null {
    const regions = state.document?.detail.layout?.regions ?? [];
    return (
      regions.find((region) => region.role === "diagram" || region.flow === "absolute")?.id ??
      regions.find((region) => typeof region.id === "string" && region.id.trim())?.id ??
      null
    );
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
    setState("selectedIds", (current) => toggleSelection(current, slotId, append));
  }

  function clearSelectedSlots(): void {
    setState({ selectedIds: clearSelection() });
  }

  function setSelectedSlots(slotIds: string[]): void {
    setState({ selectedIds: slotIds });
  }

  function setZoom(zoom: number): void {
    const nextZoom = Math.min(3, Math.max(0.25, Math.round(zoom * 100) / 100));
    setState({ zoom: nextZoom });
  }

  function setPan(panX: number, panY: number): void {
    setState({ panX, panY });
  }

  function setActiveTool(activeTool: EditorTool): void {
    setState({ activeTool });
  }

  function setPickMode(pickMode: EditorPickMode): void {
    setState({ pickMode, activeTool: "select" });
  }

  function setSnapEnabled(snapEnabled: boolean): void {
    setState({ snapEnabled });
  }

  function resetViewport(): void {
    setState({ zoom: 1, panX: 0, panY: 0 });
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
    updateCanvasSize,
    alignSelectedSlots,
    layerSelectedSlots,
    insertShape,
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
  };
}

export type EditorStore = ReturnType<typeof createEditorStore>;
