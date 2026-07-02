import { createStore } from "solid-js/store";
import { loadProblem, listProblems } from "../api/editorApi";
import { EditorApiError } from "../api/httpClient";
import { createEditorDocument, type EditorDocument } from "../editor-core/model/editorDocument";
import { clearSelection, toggleSelection } from "../editor-core/selection/selectionManager";
import type { EditorError, ProblemSummary } from "../types/api";

export type EditorTool = "select" | "pan";
export type EditorPickMode = "all" | "linepath" | "text" | "shape";

export interface EditorState {
  problemId: string | null;
  problems: ProblemSummary[];
  document: EditorDocument | null;
  selectedIds: string[];
  zoom: number;
  panX: number;
  panY: number;
  activeTool: EditorTool;
  pickMode: EditorPickMode;
  dirty: boolean;
  loading: boolean;
  error: EditorError | null;
}

const initialState: EditorState = {
  problemId: null,
  problems: [],
  document: null,
  selectedIds: [],
  zoom: 1,
  panX: 0,
  panY: 0,
  activeTool: "select",
  pickMode: "all",
  dirty: false,
  loading: false,
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
        selectedIds: clearSelection(),
        zoom: 1,
        panX: 0,
        panY: 0,
        dirty: false,
        loading: false,
      });
      const url = new URL(window.location.href);
      url.searchParams.set("problem", detail.problem_id);
      window.history.replaceState(null, "", url);
    } catch (error) {
      setState({ loading: false, error: toEditorError(error) });
    }
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

  function resetViewport(): void {
    setState({ zoom: 1, panX: 0, panY: 0 });
  }

  return {
    state,
    refreshProblems,
    openProblem,
    selectSlot,
    clearSelectedSlots,
    setSelectedSlots,
    setZoom,
    setPan,
    setActiveTool,
    setPickMode,
    resetViewport,
  };
}

export type EditorStore = ReturnType<typeof createEditorStore>;
