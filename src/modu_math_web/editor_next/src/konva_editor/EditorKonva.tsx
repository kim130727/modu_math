import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { ProblemList } from "../components/ProblemList";
import {
  applyLayoutPatches,
  buildProblem,
  createProblem,
  loadProblem,
  problemDetailToCanonicalProblem,
  saveTutorFlow,
  type TutorRendererStep,
  type TutorRendererOverlay,
} from "../api/editorApi";
import { problemJsonToLayoutPatches } from "../tldraw/converters/problemJsonToLayoutPatches";
import type { EditorShape, EditorShapeDocument, InputInteraction, InputStyle } from "../types/editorShape";
import type { ProblemJson } from "../types/problem";
import sampleProblem from "../samples/sample_problem.json";
import { connectorArrowForPreset, connectorKindForPreset } from "./connectorGeometry";
import { editorDocumentToProblemJson, estimateTextWidth, fittedTextHeight, problemJsonToEditorDocument } from "./converters";
import { KONVA_PREVIEW_FONT_FAMILY } from "./fonts";
import { JsonImportExport } from "./JsonImportExport";
import { KonvaStage, type CanvasPoint } from "./KonvaStage";
import { KonvaToolbar, type ShapePreset } from "./KonvaToolbar";
import { PropertyPanel } from "./PropertyPanel";
import { TutorFlowPanel } from "./TutorFlowPanel";
import { TutorPreviewPanel } from "./TutorPreviewPanel";

const initialProblem = sampleProblem as ProblemJson;
type SidePanelTab = "properties" | "tutor" | "flow" | "json";
type SaveStatus = "saved" | "saving" | "unsaved" | "building" | "built" | "error";

export function EditorKonva() {
  const [baseProblemJson, setBaseProblemJson] = useState<ProblemJson>(initialProblem);
  const [document, setDocument] = useState<EditorShapeDocument>(() => problemJsonToEditorDocument(initialProblem));
  const [previewArtifacts, setPreviewArtifacts] = useState<{
    semantic: Record<string, unknown> | null;
    solvable: Record<string, unknown> | null;
    layout: import("../api/editorApi").LayoutDocument | null;
    renderer: import("../api/editorApi").RendererDocument | null;
  }>({ semantic: null, solvable: null, layout: null, renderer: null });
  const [selectedShapeIds, setSelectedShapeIds] = useState<string[]>([]);
  const [selectedProblemId, setSelectedProblemId] = useState(initialProblem.id);
  const [message, setMessage] = useState("Loaded sample problem in Konva editor.");
  const [saveStatus, setSaveStatus] = useState<SaveStatus>("saved");
  const [drawingPreset, setDrawingPreset] = useState<ShapePreset | null>(null);
  const [problemListVersion, setProblemListVersion] = useState(0);
  const [activeSidePanel, setActiveSidePanel] = useState<SidePanelTab>("properties");
  const [activeTutorStepId, setActiveTutorStepId] = useState<string | null>(null);
  const [activeTutorFrameIndex, setActiveTutorFrameIndex] = useState(0);
  const [activeTutorOverlayIndex, setActiveTutorOverlayIndex] = useState<number | null>(null);
  const [draftTutorFlow, setDraftTutorFlow] = useState<TutorRendererStep[] | null>(null);
  const clipboardRef = useRef<EditorShape[]>([]);
  const imageFileInputRef = useRef<HTMLInputElement | null>(null);
  const idPrefix = useMemo(() => `konva_${Date.now()}`, []);

  const selectedShape = selectedShapeIds.length === 1 ? document.shapes.find((shape) => shape.id === selectedShapeIds[0]) ?? null : null;
  const effectiveTutorFlow = draftTutorFlow ?? previewArtifacts.renderer?.tutor_flow ?? [];
  const activeTutorFrames = useMemo(() => {
    if (!activeTutorStepId) return [];
    const step = effectiveTutorFlow.find((item) => item.step_id === activeTutorStepId);
    if (!step) return [];
    return step.frames?.length ? step.frames : [{ id: `${activeTutorStepId}.frame.1`, overlays: step.overlays ?? [] }];
  }, [activeTutorStepId, effectiveTutorFlow]);
  const activeTutorOverlays = activeTutorFrames[activeTutorFrameIndex]?.overlays ?? [];
  const setTutorStep = useCallback((stepId: string | null) => {
    setActiveTutorStepId(stepId);
    setActiveTutorFrameIndex(0);
    setActiveTutorOverlayIndex(null);
  }, []);
  const selectTutorFrame = useCallback((stepId: string, frameIndex: number) => {
    setActiveTutorStepId(stepId);
    setActiveTutorFrameIndex(Math.max(0, frameIndex));
    setActiveTutorOverlayIndex(null);
  }, []);
  const selectTutorOverlay = useCallback((overlayIndex: number | null) => {
    setActiveTutorOverlayIndex(overlayIndex);
    if (overlayIndex !== null) setActiveSidePanel("flow");
  }, []);

  const setProblem = useCallback((problem: ProblemJson, nextMessage: string, artifacts = previewArtifacts) => {
    setBaseProblemJson(problem);
    setPreviewArtifacts(artifacts);
    setDocument(problemJsonToEditorDocument(problem));
    setSelectedProblemId(problem.id);
    setSelectedShapeIds([]);
    setActiveTutorStepId(null);
    setActiveTutorOverlayIndex(null);
    setDraftTutorFlow(null);
    setMessage(nextMessage);
    setSaveStatus("saved");
  }, [previewArtifacts]);

  const openProblem = useCallback(
    async (problemId: string) => {
      setMessage(`Loading ${problemId}...`);
      try {
        const detail = await loadProblem(problemId);
        setProblem(problemDetailToCanonicalProblem(detail), `Loaded ${problemId}.`, {
          semantic: detail.semantic,
          solvable: detail.solvable,
          layout: detail.layout,
          renderer: detail.renderer,
        });
      } catch (error) {
        setMessage(`Could not load ${problemId}: ${String(error)}`);
      }
    },
    [setProblem],
  );

  const createNewProblem = useCallback(async () => {
    const rawName = window.prompt("새 문제 이름 또는 경로", defaultNewProblemId());
    if (rawName === null) return;
    const problemId = normalizeNewProblemId(rawName);
    if (!problemId) {
      setMessage("새 문제 이름을 입력해 주세요.");
      return;
    }

    setMessage(`Creating ${problemId}...`);
    try {
      const detail = await createProblem(problemId, fileTitleFromProblemId(problemId));
      setProblem(problemDetailToCanonicalProblem(detail), `Created ${detail.problem_id}. Start filling slots, then save/build when ready.`, {
        semantic: detail.semantic,
        solvable: detail.solvable,
        layout: detail.layout,
        renderer: detail.renderer,
      });
      setProblemListVersion((version) => version + 1);
    } catch (error) {
      setMessage(`Could not create ${problemId}: ${String(error)}`);
    }
  }, [setProblem]);

  const updateShape = useCallback((nextShape: EditorShape) => {
    setSaveStatus("unsaved");
    setDocument((current) => ({
      ...current,
      shapes: current.shapes.map((shape) => (shape.id === nextShape.id ? nextShape : shape)),
    }));
  }, []);

  const updateShapes = useCallback((nextShapes: EditorShape[]) => {
    const nextShapeById = new Map(nextShapes.map((shape) => [shape.id, shape]));
    if (nextShapeById.size) setSaveStatus("unsaved");
    setDocument((current) => ({
      ...current,
      shapes: current.shapes.map((shape) => nextShapeById.get(shape.id) ?? shape),
    }));
  }, []);

  const patchSelectedShape = useCallback(
    (patch: Partial<EditorShape>) => {
      if (!selectedShape) return;
      updateShape(applyAutoSizing({ ...selectedShape, ...patch } as EditorShape, selectedShape));
    },
    [selectedShape, updateShape],
  );

  const addShape = useCallback(
    (shape: EditorShape) => {
      setSaveStatus("unsaved");
      setDocument((current) => ({ ...current, shapes: [...current.shapes, shape] }));
      setSelectedShapeIds([shape.id]);
    },
    [],
  );

  const addShapes = useCallback((shapes: EditorShape[]) => {
    if (!shapes.length) return;
    setSaveStatus("unsaved");
    setDocument((current) => ({ ...current, shapes: [...current.shapes, ...shapes] }));
    setSelectedShapeIds(shapes.map((shape) => shape.id));
  }, []);

  const nextId = useCallback((kind: string) => `${idPrefix}_${kind}_${Math.round(performance.now())}`, [idPrefix]);

  const insertShape = useCallback(
    (preset: ShapePreset) => {
      if (isDragDrawPreset(preset)) {
        setDrawingPreset(preset);
        setMessage(`${shapePresetLabel(preset)}: 캔버스에서 드래그해서 그리세요.`);
        return;
      }
      addShape(createShapeFromPreset(preset, nextId(preset)));
    },
    [addShape, nextId],
  );

  const setAnswerSlotState = useCallback(
    (shapeIds: string[], enabled: boolean) => {
      const ids = new Set(shapeIds);
      const targets = document.shapes.filter((shape) => ids.has(shape.id) && isAnswerSlotShape(shape));
      if (!targets.length) return;
      const startOrder = nextAnswerOrder(document.shapes);
      updateShapes(
        targets.map((shape, index) =>
          enabled
            ? ({
                ...shape,
                interaction: shape.interaction ?? defaultInteractionForShape(shape, startOrder + index),
                input_style: shape.input_style ?? defaultInputStyle(),
              } as EditorShape)
            : ({ ...shape, interaction: undefined, input_style: undefined } as EditorShape),
        ),
      );
    },
    [document.shapes, updateShapes],
  );

  const addDrawnShape = useCallback(
    (preset: ShapePreset, start: CanvasPoint, end: CanvasPoint, points?: CanvasPoint[]) => {
      addShape(createShapeFromDrag(preset, nextId(preset), start, end, points));
    },
    [addShape, nextId],
  );

  const addText = useCallback(() => {
    const text = "Text";
    const fontSize = 30;
    addShape({
      id: nextId("text"),
      type: "text",
      x: 180,
      y: 400,
      text,
      fontSize,
      fontFamily: KONVA_PREVIEW_FONT_FAMILY,
      fill: "#111827",
      width: autoTextWidth(text, fontSize),
      height: fittedTextHeight(text, fontSize, autoTextWidth(text, fontSize)),
      lineHeight: 1.25,
      sourceKind: "text",
    });
  }, [addShape, nextId]);

  const addMathShape = useCallback(
    (latex: string, width = 260, height = 72) => {
      addShape({
        id: nextId("math"),
        type: "math",
        x: 180,
        y: 470,
        latex,
        width,
        height,
        fontSize: 30,
      });
    },
    [addShape, nextId],
  );

  const addMath = useCallback(() => {
    const latex = window.prompt("LaTeX", "x + 1 = 5");
    if (latex === null) return;
    addMathShape(latex || "x + 1 = 5");
  }, [addMathShape]);

  const addProperFraction = useCallback(() => {
    addMathShape("\\frac{1}{2}", 120, 84);
  }, [addMathShape]);

  const addMixedFraction = useCallback(() => {
    addMathShape("1\\frac{1}{2}", 160, 84);
  }, [addMathShape]);

  const addImage = useCallback(() => {
    imageFileInputRef.current?.click();
  }, []);

  const importLocalImage = useCallback(
    async (file: File) => {
      if (!file.type.startsWith("image/")) {
        setMessage(`Unsupported image file: ${file.name}`);
        return;
      }

      try {
        const src = await readFileAsDataUrl(file);
        const size = await loadImageSize(src);
        const fit = fitImageSize(size.width, size.height, 360, 260);
        addShape({
          id: nextId("image"),
          type: "image",
          x: 520,
          y: 280,
          src,
          width: fit.width,
          height: fit.height,
          preserveAspectRatio: "xMidYMid meet",
        });
        setMessage(`Inserted local image: ${file.name}`);
      } catch (error) {
        setMessage(`Could not insert image ${file.name}: ${String(error)}`);
      }
    },
    [addShape, nextId],
  );

  const addTable = useCallback(() => {
    const rows = promptInteger("Rows", 3, 1, 20);
    if (rows === null) return;
    const cols = promptInteger("Columns", 3, 1, 20);
    if (cols === null) return;

    const x = 220;
    const y = 160;
    const cellWidth = 120;
    const cellHeight = 56;
    const width = cols * cellWidth;
    const height = rows * cellHeight;
    const base = nextId("table");
    const shapes: EditorShape[] = [
      {
        id: `${base}_outer`,
        type: "rect",
        x,
        y,
        width,
        height,
        fill: "#ffffff",
        stroke: "#111827",
        strokeWidth: 1,
      },
    ];

    for (let col = 1; col < cols; col += 1) {
      shapes.push({
        id: `${base}_v${col}`,
        type: "line",
        x: x + col * cellWidth,
        y,
        points: [0, 0, 0, height],
        stroke: "#111827",
        strokeWidth: 1,
      });
    }

    for (let row = 1; row < rows; row += 1) {
      shapes.push({
        id: `${base}_h${row}`,
        type: "line",
        x,
        y: y + row * cellHeight,
        points: [0, 0, width, 0],
        stroke: "#111827",
        strokeWidth: 1,
      });
    }

    for (let row = 0; row < rows; row += 1) {
      for (let col = 0; col < cols; col += 1) {
        shapes.push({
          id: `${base}_r${row + 1}c${col + 1}`,
          type: "text",
          x: x + col * cellWidth,
          y: y + row * cellHeight + 12,
        text: "",
        fontSize: 24,
        fill: "#111827",
        width: cellWidth,
        height: fittedTextHeight("", 24, cellWidth),
        align: "center",
        lineHeight: 1.25,
        sourceKind: "text_box",
      });
      }
    }

    addShapes(shapes);
  }, [addShapes, nextId]);

  const addGraphPaper = useCallback(() => {
    const rows = promptInteger("Rows", 8, 1, 40);
    if (rows === null) return;
    const cols = promptInteger("Columns", 10, 1, 40);
    if (cols === null) return;

    const cellSize = 25;
    const x = 220;
    const y = 160;
    const width = cols * cellSize;
    const height = rows * cellSize;
    const stroke = "#2563eb";
    const strokeWidth = 1;
    const base = nextId("graphpaper");
    const shapes: EditorShape[] = [];

    for (let col = 0; col <= cols; col += 1) {
      shapes.push({
        id: `${base}_v${col}`,
        type: "line",
        x: x + col * cellSize,
        y,
        points: [0, 0, 0, height],
        stroke,
        strokeWidth,
      });
    }

    for (let row = 0; row <= rows; row += 1) {
      shapes.push({
        id: `${base}_h${row}`,
        type: "line",
        x,
        y: y + row * cellSize,
        points: [0, 0, width, 0],
        stroke,
        strokeWidth,
      });
    }

    addShapes(shapes);
  }, [addShapes, nextId]);

  const deleteSelected = useCallback(() => {
    if (!selectedShapeIds.length) return;
    const selected = new Set(selectedShapeIds);
    setSaveStatus("unsaved");
    setDocument((current) => ({
      ...current,
      shapes: current.shapes.filter((shape) => !selected.has(shape.id)),
    }));
    setSelectedShapeIds([]);
  }, [selectedShapeIds]);

  const copySelected = useCallback(() => {
    const selected = new Set(selectedShapeIds);
    clipboardRef.current = document.shapes.filter((shape) => selected.has(shape.id)).map(cloneShape);
    if (clipboardRef.current.length) setMessage(`Copied ${clipboardRef.current.length} shape(s).`);
  }, [document.shapes, selectedShapeIds]);

  const pasteClipboard = useCallback(() => {
    if (!clipboardRef.current.length) return;
    const stamp = Math.round(performance.now());
    const pasted = clipboardRef.current.map((shape, index) => ({
      ...cloneShape(shape),
      id: `${idPrefix}_paste_${stamp}_${index}`,
      x: shape.x + 24,
      y: shape.y + 24,
    })) as EditorShape[];
    setSaveStatus("unsaved");
    setDocument((current) => ({ ...current, shapes: [...current.shapes, ...pasted] }));
    setSelectedShapeIds(pasted.map((shape) => shape.id));
    clipboardRef.current = pasted.map(cloneShape);
    setMessage(`Pasted ${pasted.length} shape(s).`);
  }, [idPrefix]);

  const duplicateSelected = useCallback(() => {
    const selected = new Set(selectedShapeIds);
    const source = document.shapes.filter((shape) => selected.has(shape.id));
    if (!source.length) return;
    const stamp = Math.round(performance.now());
    const duplicated = source.map((shape, index) => ({
      ...cloneShape(shape),
      id: `${idPrefix}_duplicate_${stamp}_${index}`,
      x: shape.x + 24,
      y: shape.y + 24,
    })) as EditorShape[];
    setSaveStatus("unsaved");
    setDocument((current) => ({ ...current, shapes: [...current.shapes, ...duplicated] }));
    setSelectedShapeIds(duplicated.map((shape) => shape.id));
    clipboardRef.current = duplicated.map(cloneShape);
    setMessage(`Duplicated ${duplicated.length} shape(s).`);
  }, [document.shapes, idPrefix, selectedShapeIds]);

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (isEditableTarget(event.target)) return;
      const key = event.key.toLowerCase();
      const commandKey = event.ctrlKey || event.metaKey;

      if (isArrowKey(event.key) && selectedShapeIds.length) {
        event.preventDefault();
        const distance = event.shiftKey ? 10 : 1;
        const delta = arrowKeyDelta(event.key, distance);
        const selected = new Set(selectedShapeIds);
        updateShapes(
          document.shapes
            .filter((shape) => selected.has(shape.id) && !shape.locked)
            .map((shape) => ({ ...shape, x: shape.x + delta.dx, y: shape.y + delta.dy }) as EditorShape),
        );
        return;
      }

      if (event.key === "Delete" || event.key === "Backspace") {
        if (!selectedShapeIds.length) return;
        event.preventDefault();
        deleteSelected();
        return;
      }

      if (!commandKey) return;
      if (key === "c") {
        event.preventDefault();
        copySelected();
      } else if (key === "v") {
        event.preventDefault();
        pasteClipboard();
      } else if (key === "d") {
        event.preventDefault();
        duplicateSelected();
      }
    };

    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [copySelected, deleteSelected, document.shapes, duplicateSelected, pasteClipboard, selectedShapeIds, updateShapes]);

  const refreshJson = useCallback(() => {
    setDocument((current) => ({ ...current }));
    setMessage("Shape JSON refreshed.");
  }, []);

  const importDocument = useCallback((nextDocument: EditorShapeDocument) => {
    if (!Array.isArray(nextDocument.shapes) || !nextDocument.canvas) return;
    setSaveStatus("unsaved");
    setDocument(nextDocument);
    setSelectedProblemId(nextDocument.id);
    setSelectedShapeIds([]);
    setMessage("Imported shape JSON.");
  }, []);

  const saveJson = useCallback(async () => {
    const nextProblem = editorDocumentToProblemJson(document, baseProblemJson);
    if (selectedProblemId === initialProblem.id) {
      setMessage("Sample problem is local only. Open a real problem before saving to DSL.");
      setSaveStatus("error");
      return;
    }

    const patches = problemJsonToLayoutPatches(baseProblemJson, nextProblem);
    if (!patches.length && !draftTutorFlow) {
      setMessage(`No DSL changes to save for ${selectedProblemId}.`);
      setSaveStatus("saved");
      return;
    }

    setSaveStatus("saving");
    setMessage(`Saving ${selectedProblemId}...`);
    try {
      const savedParts: string[] = [];
      if (patches.length) {
        const response = await applyLayoutPatches(selectedProblemId, patches, { format: false });
        setBaseProblemJson(nextProblem);
        savedParts.push(`${response.applied.length} layout patch(es)`);
      }
      if (draftTutorFlow) {
        const response = await saveTutorFlow(selectedProblemId, draftTutorFlow, { format: false });
        setDraftTutorFlow(response.tutor_flow);
        savedParts.push("tutor flow");
      }
      setSaveStatus("saved");
      setMessage(`Saved ${savedParts.join(" and ")} for ${selectedProblemId}. Build to refresh artifacts.`);
    } catch (error) {
      setSaveStatus("error");
      setMessage(`Could not save ${selectedProblemId}: ${String(error)}`);
    }
  }, [baseProblemJson, document, draftTutorFlow, selectedProblemId]);

  const saveCurrentTutorFlow = useCallback(
    async (tutorFlow: TutorRendererStep[]) => {
      if (selectedProblemId === initialProblem.id) {
        setMessage("Sample problem is local only. Open a real problem before saving tutor flow.");
        setSaveStatus("error");
        return;
      }

      setSaveStatus("saving");
      setMessage(`Saving tutor flow for ${selectedProblemId}...`);
      try {
        const response = await saveTutorFlow(selectedProblemId, tutorFlow, { format: false });
        setPreviewArtifacts((current) => ({
          ...current,
          renderer:
            current.renderer ? { ...current.renderer, tutor_flow: response.tutor_flow } : current.renderer,
        }));
        setDraftTutorFlow(response.tutor_flow);
        setActiveTutorFrameIndex(0);
        setSaveStatus("saved");
        setMessage(`Saved tutor flow for ${selectedProblemId}. Build to refresh artifacts.`);
      } catch (error) {
        setSaveStatus("error");
        setMessage(`Could not save tutor flow for ${selectedProblemId}: ${String(error)}`);
      }
    },
    [selectedProblemId],
  );

  const patchTutorOverlay = useCallback(
    (overlayIndex: number, patch: Partial<TutorRendererOverlay>, nextMessage?: string) => {
      if (!activeTutorStepId) return;
      const nextFlow = effectiveTutorFlow.map((step) => {
        if (step.step_id !== activeTutorStepId) return step;
        const frames = (step.frames?.length ? step.frames : [{ id: `${step.step_id}.frame.1`, overlays: step.overlays ?? [] }]).map(
          (frame, frameIndex) => {
            if (frameIndex !== activeTutorFrameIndex) return frame;
            return {
              ...frame,
              overlays: frame.overlays.map((overlay, index) => (index === overlayIndex ? { ...overlay, ...patch } : overlay)),
            };
          },
        );
        return { step_id: step.step_id, frames };
      });
      setSaveStatus("unsaved");
      setDraftTutorFlow(nextFlow);
      setActiveTutorOverlayIndex(overlayIndex);
      if (nextMessage) setMessage(nextMessage);
    },
    [activeTutorFrameIndex, activeTutorStepId, effectiveTutorFlow],
  );

  const moveActiveTutorOverlay = useCallback(
    (overlayIndex: number, x: number, y: number) => {
      patchTutorOverlay(overlayIndex, { x, y }, `Moved tutor overlay ${overlayIndex + 1}. Save to persist it.`);
    },
    [patchTutorOverlay],
  );

  const changeActiveTutorOverlay = useCallback(
    (overlayIndex: number, patch: Partial<TutorRendererOverlay>) => {
      patchTutorOverlay(overlayIndex, patch);
    },
    [patchTutorOverlay],
  );

  const buildCurrentProblem = useCallback(async () => {
    if (selectedProblemId === initialProblem.id) {
      setMessage("Sample problem is local only. Open a real problem before building.");
      setSaveStatus("error");
      return;
    }

    setSaveStatus("building");
    setMessage(`Building ${selectedProblemId}...`);
    try {
      if (draftTutorFlow) {
        setSaveStatus("saving");
        setMessage(`Saving tutor flow for ${selectedProblemId} before build...`);
        await saveTutorFlow(selectedProblemId, draftTutorFlow, { format: false });
        setSaveStatus("building");
      }
      const response = await buildProblem(selectedProblemId);
      const detail = [response.stdout, response.stderr].filter(Boolean).join("\n").trim();
      setPreviewArtifacts({
        semantic: (response.artifacts.semantic as Record<string, unknown> | null | undefined) ?? null,
        solvable: (response.artifacts.solvable as Record<string, unknown> | null | undefined) ?? null,
        layout: (response.artifacts.layout as import("../api/editorApi").LayoutDocument | null | undefined) ?? null,
        renderer: (response.artifacts.renderer as import("../api/editorApi").RendererDocument | null | undefined) ?? null,
      });
      setDraftTutorFlow(null);
      setSaveStatus("built");
      setMessage(detail ? `Build complete for ${selectedProblemId}.\n${detail}` : `Build complete for ${selectedProblemId}.`);
    } catch (error) {
      setSaveStatus("error");
      setMessage(`Could not build ${selectedProblemId}: ${String(error)}`);
    }
  }, [draftTutorFlow, selectedProblemId]);

  return (
    <div className="math-problem-editor konva-editor">
      <KonvaToolbar
        hasSelection={selectedShapeIds.length > 0}
        onInsertShape={insertShape}
        onAddMath={addMath}
        onAddProperFraction={addProperFraction}
        onAddMixedFraction={addMixedFraction}
        onAddText={addText}
        onAddImage={addImage}
        onAddTable={addTable}
        onAddGraphPaper={addGraphPaper}
        onDeleteSelected={deleteSelected}
        onRefreshJson={refreshJson}
        onSave={saveJson}
        onBuild={buildCurrentProblem}
        onNewFile={createNewProblem}
      />
      <input
        ref={imageFileInputRef}
        type="file"
        accept="image/*"
        style={{ display: "none" }}
        onChange={(event) => {
          const file = event.target.files?.[0];
          event.target.value = "";
          if (file) void importLocalImage(file);
        }}
      />
      <div className="editor-body konva-editor-body">
        <ProblemList key={problemListVersion} selectedProblemId={selectedProblemId} onOpenProblem={openProblem} />
        <div className="konva-main-panel">
          <KonvaStage
            width={document.canvas.width}
            height={document.canvas.height}
            shapes={document.shapes}
            selectedShapeIds={selectedShapeIds}
            tutorOverlays={activeTutorOverlays}
            activeTutorOverlayIndex={activeTutorOverlayIndex}
            drawingPreset={drawingPreset}
            onSelectShapes={setSelectedShapeIds}
            onChangeShapes={updateShapes}
            onConvertShapesToAnswer={(ids) => setAnswerSlotState(ids, true)}
            onRestoreShapesFromAnswer={(ids) => setAnswerSlotState(ids, false)}
            onDrawShape={addDrawnShape}
            onDrawingComplete={() => setDrawingPreset(null)}
            onTutorOverlaySelect={selectTutorOverlay}
            onTutorOverlayChange={changeActiveTutorOverlay}
            onTutorOverlayMove={moveActiveTutorOverlay}
          />
        </div>
        <div className="konva-side-panel">
          <div className="konva-side-tabs" role="tablist" aria-label="Editor side panels">
            <SidePanelButton
              active={activeSidePanel === "properties"}
              label="Properties"
              onClick={() => setActiveSidePanel("properties")}
              icon="properties"
            />
            <SidePanelButton
              active={activeSidePanel === "tutor"}
              label="Rule Tutor Preview"
              onClick={() => setActiveSidePanel("tutor")}
              icon="tutor"
            />
            <SidePanelButton
              active={activeSidePanel === "flow"}
              label="Tutor Flow"
              onClick={() => setActiveSidePanel("flow")}
              icon="flow"
            />
            <SidePanelButton
              active={activeSidePanel === "json"}
              label="Shape JSON"
              onClick={() => setActiveSidePanel("json")}
              icon="json"
            />
          </div>
          <div className="konva-side-content">
            {activeSidePanel === "properties" ? (
              <PropertyPanel shape={selectedShape} saveStatus={saveStatus} onChange={patchSelectedShape} />
            ) : null}
            {activeSidePanel === "tutor" ? (
              <TutorPreviewPanel
                problemId={selectedProblemId}
                shapeDocument={document}
                semantic={previewArtifacts.semantic}
                solvable={previewArtifacts.solvable}
                layout={previewArtifacts.layout}
                renderer={previewArtifacts.renderer}
                tutorFrameIndex={activeTutorFrameIndex}
                tutorFrameCount={activeTutorFrames.length}
                saveStatus={saveStatus}
                message={message}
                onTutorFrameChange={setActiveTutorFrameIndex}
                onTutorStepChange={setTutorStep}
              />
            ) : null}
            {activeSidePanel === "flow" ? (
              <TutorFlowPanel
                problemId={selectedProblemId}
                tutorFlow={effectiveTutorFlow}
                message={message}
                activeStepId={activeTutorStepId}
                activeFrameIndex={activeTutorFrameIndex}
                activeOverlayIndex={activeTutorOverlayIndex}
                selectedShapeIds={selectedShapeIds}
                onDraftChange={(flow) => {
                  setDraftTutorFlow(flow);
                  setSaveStatus("unsaved");
                }}
                onSelectFrame={selectTutorFrame}
                onSelectOverlay={selectTutorOverlay}
                onSave={saveCurrentTutorFlow}
              />
            ) : null}
            {activeSidePanel === "json" ? <JsonImportExport document={document} message={message} onImport={importDocument} /> : null}
          </div>
        </div>
      </div>
    </div>
  );
}

function SidePanelButton({
  active,
  label,
  icon,
  onClick,
}: {
  active: boolean;
  label: string;
  icon: SidePanelTab;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      role="tab"
      aria-label={label}
      aria-selected={active}
      title={label}
      className={active ? "konva-side-tab active" : "konva-side-tab"}
      onClick={onClick}
    >
      <SidePanelIcon icon={icon} />
    </button>
  );
}

function SidePanelIcon({ icon }: { icon: SidePanelTab }) {
  if (icon === "properties") {
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M4 5h16" />
        <path d="M4 12h16" />
        <path d="M4 19h16" />
        <circle cx="8" cy="5" r="2" />
        <circle cx="16" cy="12" r="2" />
        <circle cx="10" cy="19" r="2" />
      </svg>
    );
  }
  if (icon === "tutor") {
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M5 6.5h14a2 2 0 0 1 2 2v6a2 2 0 0 1-2 2h-7l-4 3v-3H5a2 2 0 0 1-2-2v-6a2 2 0 0 1 2-2Z" />
        <path d="M8 10h8" />
        <path d="M8 13h5" />
      </svg>
    );
  }
  if (icon === "flow") {
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <circle cx="6" cy="7" r="2" />
        <circle cx="18" cy="7" r="2" />
        <circle cx="12" cy="17" r="2" />
        <path d="M8 7h8" />
        <path d="M7.5 8.7 11 15" />
        <path d="m16.5 8.7-3.5 6.3" />
      </svg>
    );
  }
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M8 4H6a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h2" />
      <path d="M16 4h2a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2h-2" />
      <path d="m10 9-3 3 3 3" />
      <path d="m14 9 3 3-3 3" />
    </svg>
  );
}

function normalizeNewProblemId(value: string): string {
  return value
    .trim()
    .replace(/\\/g, "/")
    .replace(/^\/+/, "")
    .replace(/\/+/g, "/")
    .replace(/[<>:"|?*]/g, "_")
    .replace(/\s+/g, "_")
    .replace(/\/(?:\.|\.\.)(?=\/|$)/g, "")
    .replace(/^(?:\.|\.\.)\/?/, "");
}

function defaultNewProblemId(): string {
  const now = new Date();
  const stamp = [
    now.getFullYear(),
    String(now.getMonth() + 1).padStart(2, "0"),
    String(now.getDate()).padStart(2, "0"),
  ].join("");
  return `drafts/new_problem_${stamp}`;
}

function fileTitleFromProblemId(problemId: string): string {
  const last = problemId.split("/").filter(Boolean).at(-1) ?? "New problem";
  return last.endsWith(".dsl.py") ? last.slice(0, -lenDslSuffix()) : last;
}

function lenDslSuffix(): number {
  return ".dsl.py".length;
}

function cloneShape<T extends EditorShape>(shape: T): T {
  return JSON.parse(JSON.stringify(shape)) as T;
}

function isAnswerSlotShape(shape: EditorShape): boolean {
  return shape.type === "rect" || shape.type === "circle" || shape.type === "path" || shape.type === "text";
}

function nextAnswerOrder(shapes: EditorShape[]): number {
  const orders = shapes
    .map((shape) => shape.interaction?.order)
    .filter((order): order is number => typeof order === "number" && Number.isFinite(order));
  return orders.length ? Math.max(...orders) + 1 : 0;
}

function defaultInteractionForShape(shape: EditorShape, order: number): InputInteraction {
  if (shape.type === "circle" || shape.type === "path") {
    return {
      type: "select",
      role: "choice",
      value_type: "choice",
      choice_value: shape.id,
      include_in_submission: true,
      order,
      group_id: "shape_choice",
      keyboard: "none",
    };
  }
  return {
    type: "input",
    role: "answer",
    value_type: "digit",
    max_length: 1,
    include_in_submission: true,
    order,
    group_id: "final_answer",
    auto_advance: true,
    keyboard: "number",
  };
}

function defaultInputStyle(): InputStyle {
  return {
    font_size_mode: "auto",
    font_size_adjust: 0,
    min_font_size: 14,
    max_font_size: 52,
    font_weight: 700,
    horizontal_align: "center",
    vertical_align: "middle",
    padding: 6,
    text_color: "#222222",
  };
}

function isDragDrawPreset(preset: ShapePreset): boolean {
  return [
    "line",
    "arrow",
    "doubleArrow",
    "elbow",
    "elbowArrow",
    "elbowDoubleArrow",
    "curvedConnector",
    "curvedArrow",
    "curvedDoubleArrow",
    "curve",
    "freeformShape",
    "freeformScribble",
  ].includes(preset);
}

function shapePresetLabel(preset: ShapePreset): string {
  const labels: Partial<Record<ShapePreset, string>> = {
    line: "선",
    arrow: "선 화살표",
    doubleArrow: "선 화살표: 양방향",
    elbow: "연결선: 꺾임",
    elbowArrow: "연결선: 꺾인 화살표",
    elbowDoubleArrow: "연결선: 꺾인 양쪽 화살표",
    curvedConnector: "연결선: 구부러짐",
    curvedArrow: "연결선: 구부러진 화살표",
    curvedDoubleArrow: "연결선: 구부러진 양쪽 화살표",
    curve: "곡선",
    freeformShape: "자유형: 도형",
    freeformScribble: "자유형: 자유 곡선",
  };
  return labels[preset] ?? "도형";
}

function createShapeFromDrag(
  preset: ShapePreset,
  id: string,
  start: CanvasPoint,
  end: CanvasPoint,
  points: CanvasPoint[] = [],
): EditorShape {
  const stroke = "#111827";
  const strokeWidth = 1.2;
  const connectorKind = connectorKindForPreset(preset);
  if (connectorKind) {
    return {
      id,
      type: "connector",
      kind: connectorKind,
      x: roundCanvasNumber(start.x),
      y: roundCanvasNumber(start.y),
      start: { x: 0, y: 0 },
      end: { x: roundCanvasNumber(end.x - start.x), y: roundCanvasNumber(end.y - start.y) },
      control: defaultConnectorControl(connectorKind, start, end),
      ...connectorArrowForPreset(preset),
      stroke,
      strokeWidth,
    };
  }
  if (preset === "line") {
    return {
      id,
      type: "line",
      x: roundCanvasNumber(start.x),
      y: roundCanvasNumber(start.y),
      points: [0, 0, roundCanvasNumber(end.x - start.x), roundCanvasNumber(end.y - start.y)],
      stroke,
      strokeWidth,
    };
  }
  const bounds = normalizeDragBounds(start, end, points);
  return {
    id,
    type: "path",
    x: roundCanvasNumber(bounds.x),
    y: roundCanvasNumber(bounds.y),
    width: roundCanvasNumber(Math.max(1, bounds.width)),
    height: roundCanvasNumber(Math.max(1, bounds.height)),
    d: pathForDrawnShape(preset, start, end, points, bounds),
    fill: preset === "freeformShape" ? "none" : "none",
    stroke,
    strokeWidth,
  };
}

function createShapeFromPreset(preset: ShapePreset, id: string): EditorShape {
  const x = 220;
  const y = 180;
  const stroke = "#111827";
  const fill = "#ffffff";
  const strokeWidth = 1.2;

  switch (preset) {
    case "line":
      return { id, type: "line", x, y, points: [0, 0, 220, 0], stroke, strokeWidth };
    case "arrow":
    case "doubleArrow":
    case "elbow":
    case "elbowArrow":
    case "elbowDoubleArrow":
    case "curvedConnector":
    case "curvedArrow":
    case "curvedDoubleArrow":
    case "curve": {
      const connectorKind = connectorKindForPreset(preset) ?? "straight";
      const end = { x: 180, y: connectorKind === "straight" ? 0 : 120 };
      return {
        id,
        type: "connector",
        kind: connectorKind,
        x,
        y,
        start: { x: 0, y: 0 },
        end,
        control: defaultConnectorControlFromDelta(connectorKind, end.x, end.y),
        ...connectorArrowForPreset(preset),
        stroke,
        strokeWidth,
      };
    }
    case "rect":
    case "flowProcess":
      return { id, type: "rect", x, y, width: 180, height: 96, fill, stroke, strokeWidth };
    case "roundRect":
      return { id, type: "rect", x, y, width: 180, height: 96, fill, stroke, strokeWidth, cornerRadius: 14 };
    case "circle":
      return { id, type: "circle", x: x + 70, y: y + 70, radius: 70, fill, stroke, strokeWidth };
    case "arc":
    case "semicircle":
    case "quarterArc":
      return {
        id,
        type: "path",
        x: x + 90,
        y: y + 60,
        offsetX: 90,
        offsetY: 60,
        d: pathForShapePreset(preset),
        width: 180,
        height: 120,
        fill: "none",
        stroke,
        strokeWidth,
      };
    default:
      return {
        id,
        type: "path",
        x,
        y,
        d: pathForShapePreset(preset),
        width: 180,
        height: 120,
        shapePreset: preset,
        adjustment: defaultShapeAdjustment(preset, 180, 120),
        fill: lineLikePreset(preset) ? "none" : fill,
        stroke,
        strokeWidth,
      };
  }
}

function defaultShapeAdjustment(preset: ShapePreset, width: number, height: number): { x: number; y: number } | undefined {
  if (preset === "triangle") return { x: width / 2, y: 8 };
  if (preset === "rightTriangle") return { x: width - 12, y: 12 };
  return undefined;
}

function defaultConnectorControl(kind: "straight" | "elbow" | "curve", start: CanvasPoint, end: CanvasPoint): { x: number; y: number } | undefined {
  return defaultConnectorControlFromDelta(kind, roundCanvasNumber(end.x - start.x), roundCanvasNumber(end.y - start.y));
}

function defaultConnectorControlFromDelta(kind: "straight" | "elbow" | "curve", dx: number, dy: number): { x: number; y: number } | undefined {
  if (kind === "straight") return undefined;
  if (kind === "curve") {
    const lift = Math.max(24, Math.min(90, Math.hypot(dx, dy) * 0.22));
    return { x: roundCanvasNumber(dx / 2), y: roundCanvasNumber(dy / 2 - lift) };
  }
  return { x: roundCanvasNumber(dx / 2), y: roundCanvasNumber(dy / 2) };
}

function lineLikePreset(preset: ShapePreset): boolean {
  return (
    preset === "arrow" ||
    preset === "doubleArrow" ||
    preset === "elbow" ||
    preset === "elbowArrow" ||
    preset === "elbowDoubleArrow" ||
    preset === "curvedConnector" ||
    preset === "curvedArrow" ||
    preset === "curvedDoubleArrow" ||
    preset === "curve" ||
    preset === "freeformScribble" ||
    preset === "arc" ||
    preset === "semicircle" ||
    preset === "quarterArc"
  );
}

function pathForShapePreset(preset: ShapePreset): string {
  switch (preset) {
    case "arrow":
      return "M0 100 L160 20 M160 20 L112 18 M160 20 L136 62";
    case "doubleArrow":
      return "M20 100 L160 20 M20 100 L68 102 M20 100 L44 58 M160 20 L112 18 M160 20 L136 62";
    case "elbow":
      return "M20 20 L20 90 L160 90";
    case "arc":
      return "M10 82 A80 58 0 0 1 170 82";
    case "semicircle":
      return "M10 96 A80 80 0 0 1 170 96";
    case "quarterArc":
      return "M24 104 A80 80 0 0 1 104 24";
    case "triangle":
      return "M90 8 L172 112 L8 112 Z";
    case "rightTriangle":
      return "M20 10 L168 112 L20 112 Z";
    case "diamond":
    case "flowDecision":
      return "M90 6 L174 60 L90 114 L6 60 Z";
    case "pentagon":
      return "M90 6 L174 44 L142 114 L38 114 L6 44 Z";
    case "hexagon":
      return "M48 8 L132 8 L176 60 L132 112 L48 112 L4 60 Z";
    case "plus":
    case "mathPlus":
      return "M68 8 L112 8 L112 42 L166 42 L166 78 L112 78 L112 112 L68 112 L68 78 L14 78 L14 42 L68 42 Z";
    case "rightArrow":
      return "M8 42 L110 42 L110 12 L176 60 L110 108 L110 78 L8 78 Z";
    case "leftArrow":
      return "M172 42 L70 42 L70 12 L4 60 L70 108 L70 78 L172 78 Z";
    case "upArrow":
      return "M68 112 L68 48 L36 48 L90 8 L144 48 L112 48 L112 112 Z";
    case "downArrow":
      return "M68 8 L112 8 L112 72 L144 72 L90 112 L36 72 L68 72 Z";
    case "leftRightArrow":
      return "M4 60 L44 20 L44 42 L136 42 L136 20 L176 60 L136 100 L136 78 L44 78 L44 100 Z";
    case "mathMinus":
      return "M24 48 L156 48 L156 76 L24 76 Z";
    case "mathMultiply":
      return "M50 10 L90 48 L130 10 L164 44 L124 82 L164 120 L130 154 L90 116 L50 154 L16 120 L56 82 L16 44 Z";
    case "mathDivide":
      return "M24 50 L156 50 L156 76 L24 76 Z M78 8 A12 12 0 1 0 102 8 A12 12 0 1 0 78 8 M78 118 A12 12 0 1 0 102 118 A12 12 0 1 0 78 118";
    case "flowDocument":
      return "M8 12 L172 12 L172 88 C132 126 52 76 8 108 Z";
    case "flowDatabase":
      return "M16 28 C16 4 164 4 164 28 L164 92 C164 116 16 116 16 92 Z M16 28 C16 52 164 52 164 28";
    case "star":
      return "M90 6 L112 42 L154 42 L120 68 L134 112 L90 86 L46 112 L60 68 L26 42 L68 42 Z";
    case "burst":
      return "M90 4 L106 34 L144 14 L136 48 L178 54 L142 74 L166 110 L124 102 L108 132 L90 94 L66 132 L58 100 L16 110 L38 74 L2 54 L44 48 L36 14 L74 34 Z";
    case "ribbon":
      return "M10 24 L170 24 L148 60 L170 96 L10 96 L32 60 Z";
    case "calloutRect":
      return "M8 12 L172 12 L172 86 L112 86 L86 118 L94 86 L8 86 Z";
    case "calloutRound":
      return "M28 12 L152 12 Q172 12 172 32 L172 76 Q172 96 152 96 L112 96 L86 118 L94 96 L28 96 Q8 96 8 76 L8 32 Q8 12 28 12 Z";
    case "calloutOval":
      return "M8 52 C8 8 172 8 172 52 C172 96 8 96 8 52 Z M74 92 L52 118 L58 88";
    case "calloutCloud":
      return "M42 94 C10 94 6 60 34 52 C28 18 72 8 92 32 C116 4 164 22 154 58 C184 66 172 100 132 96 L104 96 L82 120 L88 96 Z";
    default:
      return "M8 12 L172 12 L172 108 L8 108 Z";
  }
}

function normalizeDragBounds(start: CanvasPoint, end: CanvasPoint, points: CanvasPoint[] = []): { x: number; y: number; width: number; height: number } {
  const all = points.length ? points : [start, end];
  const xs = all.map((point) => point.x).concat([start.x, end.x]);
  const ys = all.map((point) => point.y).concat([start.y, end.y]);
  const minX = Math.min(...xs);
  const maxX = Math.max(...xs);
  const minY = Math.min(...ys);
  const maxY = Math.max(...ys);
  return { x: minX, y: minY, width: maxX - minX, height: maxY - minY };
}

function pathForDrawnShape(
  preset: ShapePreset,
  start: CanvasPoint,
  end: CanvasPoint,
  points: CanvasPoint[],
  bounds: { x: number; y: number; width: number; height: number },
): string {
  const a = localPoint(start, bounds);
  const b = localPoint(end, bounds);
  const dx = b.x - a.x;
  const dy = b.y - a.y;
  if (preset === "elbow" || preset === "elbowArrow" || preset === "elbowDoubleArrow") {
    const mid = { x: a.x, y: b.y };
    return withArrowHeads(`M ${a.x} ${a.y} L ${mid.x} ${mid.y} L ${b.x} ${b.y}`, [a, mid, b], arrowMode(preset));
  }
  if (preset === "curvedConnector" || preset === "curvedArrow" || preset === "curvedDoubleArrow" || preset === "curve") {
    const lift = Math.max(20, Math.min(90, Math.hypot(dx, dy) * 0.28));
    const c1 = { x: a.x + dx * 0.34, y: a.y - lift };
    const c2 = { x: a.x + dx * 0.66, y: b.y - lift };
    return withArrowHeads(`M ${a.x} ${a.y} C ${c1.x} ${c1.y}, ${c2.x} ${c2.y}, ${b.x} ${b.y}`, [a, c1, c2, b], arrowMode(preset));
  }
  if (preset === "freeformScribble" && points.length > 1) {
    return points.map((point, index) => `${index === 0 ? "M" : "L"} ${roundCanvasNumber(point.x - bounds.x)} ${roundCanvasNumber(point.y - bounds.y)}`).join(" ");
  }
  if (preset === "freeformShape") {
    const c = { x: a.x + dx * 0.48, y: a.y + dy * 0.18 - 22 };
    const d = { x: a.x + dx * 0.84, y: a.y + dy * 0.78 };
    return `M ${a.x} ${a.y} L ${c.x} ${c.y} L ${b.x} ${b.y} L ${d.x} ${d.y} Z`;
  }
  return withArrowHeads(`M ${a.x} ${a.y} L ${b.x} ${b.y}`, [a, b], arrowMode(preset));
}

function localPoint(point: CanvasPoint, bounds: { x: number; y: number }): CanvasPoint {
  return { x: roundCanvasNumber(point.x - bounds.x), y: roundCanvasNumber(point.y - bounds.y) };
}

function arrowMode(preset: ShapePreset): "none" | "end" | "both" {
  if (preset === "doubleArrow" || preset === "elbowDoubleArrow" || preset === "curvedDoubleArrow") return "both";
  if (preset === "arrow" || preset === "elbowArrow" || preset === "curvedArrow") return "end";
  return "none";
}

function withArrowHeads(path: string, points: CanvasPoint[], mode: "none" | "end" | "both"): string {
  if (mode === "none" || points.length < 2) return path;
  const parts = [path];
  if (mode === "end" || mode === "both") parts.push(arrowHeadPath(points[points.length - 2], points[points.length - 1]));
  if (mode === "both") parts.push(arrowHeadPath(points[1], points[0]));
  return parts.join(" ");
}

function arrowHeadPath(from: CanvasPoint, to: CanvasPoint): string {
  const angle = Math.atan2(to.y - from.y, to.x - from.x);
  const length = 11;
  const spread = Math.PI / 7;
  const left = {
    x: roundCanvasNumber(to.x - Math.cos(angle - spread) * length),
    y: roundCanvasNumber(to.y - Math.sin(angle - spread) * length),
  };
  const right = {
    x: roundCanvasNumber(to.x - Math.cos(angle + spread) * length),
    y: roundCanvasNumber(to.y - Math.sin(angle + spread) * length),
  };
  return `M ${to.x} ${to.y} L ${left.x} ${left.y} M ${to.x} ${to.y} L ${right.x} ${right.y}`;
}

function roundCanvasNumber(value: number): number {
  return Math.round(value * 100) / 100;
}

function applyAutoSizing(nextShape: EditorShape, previousShape: EditorShape): EditorShape {
  if (nextShape.type === "text" && previousShape.type === "text") return applyAutoTextSizing(nextShape, previousShape);
  if (nextShape.type === "math" && previousShape.type === "math") return applyAutoMathSizing(nextShape, previousShape);
  return nextShape;
}

function applyAutoTextSizing(nextShape: Extract<EditorShape, { type: "text" }>, previousShape: Extract<EditorShape, { type: "text" }>): EditorShape {
  if (
    nextShape.text === previousShape.text &&
    nextShape.fontSize === previousShape.fontSize &&
    nextShape.width === previousShape.width &&
    nextShape.lineHeight === previousShape.lineHeight
  ) {
    return nextShape;
  }
  if (nextShape.sourceKind === "text_box") {
    const width = nextShape.width ?? autoTextWidth(nextShape.text, nextShape.fontSize);
    return {
      ...nextShape,
      width,
      height: fittedTextHeight(nextShape.text, nextShape.fontSize, width, nextShape.lineHeight ?? 1.25),
    };
  }
  return {
    ...nextShape,
    width: Math.max(nextShape.width ?? 0, autoTextWidth(nextShape.text, nextShape.fontSize)),
    height: fittedTextHeight(nextShape.text, nextShape.fontSize, autoTextWidth(nextShape.text, nextShape.fontSize), nextShape.lineHeight ?? 1.25),
  };
}

function applyAutoMathSizing(nextShape: Extract<EditorShape, { type: "math" }>, previousShape: Extract<EditorShape, { type: "math" }>): EditorShape {
  if (nextShape.latex === previousShape.latex && nextShape.fontSize === previousShape.fontSize) return nextShape;
  const fontSize = nextShape.fontSize ?? 28;
  const fractionSize = fractionMathSize(nextShape.latex, fontSize);
  if (!fractionSize) return nextShape;
  return {
    ...nextShape,
    width: Math.max(nextShape.width, fractionSize.width),
    height: Math.max(nextShape.height, fractionSize.height),
  };
}

function fractionMathSize(latex: string, fontSize: number): { width: number; height: number } | null {
  const match = latex.trim().match(/^([+-]?\d+)?\s*\\frac\s*\{([^{}]+)\}\s*\{([^{}]+)\}$/);
  if (!match) return null;
  const smallFont = Math.max(16, fontSize * 0.78);
  const wholeWidth = match[1] ? Math.max(smallFont, match[1].length * smallFont * 0.62) + 8 : 0;
  const numeratorWidth = Math.max(smallFont, match[2].length * smallFont * 0.62);
  const denominatorWidth = Math.max(smallFont, match[3].length * smallFont * 0.62);
  const fractionWidth = Math.max(34, numeratorWidth, denominatorWidth) + 12;
  return {
    width: Math.ceil(wholeWidth + fractionWidth + fontSize),
    height: Math.ceil(smallFont * 2.25 + fontSize * 0.6),
  };
}

function autoTextWidth(text: string, fontSize: number): number {
  const longestLine = text.split(/\n/g).reduce((longest, line) => (line.length > longest.length ? line : longest), "");
  return Math.min(860, Math.ceil(estimateTextWidth(longestLine || text, fontSize) + fontSize * 0.6));
}

function readFileAsDataUrl(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      if (typeof reader.result === "string") resolve(reader.result);
      else reject(new Error("Could not read file as data URL."));
    };
    reader.onerror = () => reject(reader.error ?? new Error("Could not read file."));
    reader.readAsDataURL(file);
  });
}

function loadImageSize(src: string): Promise<{ width: number; height: number }> {
  return new Promise((resolve, reject) => {
    const image = new window.Image();
    image.onload = () => resolve({ width: image.naturalWidth || image.width, height: image.naturalHeight || image.height });
    image.onerror = () => reject(new Error("Could not load image."));
    image.src = src;
  });
}

function fitImageSize(width: number, height: number, maxWidth: number, maxHeight: number): { width: number; height: number } {
  if (!width || !height) return { width: 180, height: 120 };
  const scale = Math.min(maxWidth / width, maxHeight / height, 1);
  return {
    width: Math.max(12, Math.round(width * scale)),
    height: Math.max(12, Math.round(height * scale)),
  };
}

function isEditableTarget(target: EventTarget | null): boolean {
  if (!(target instanceof HTMLElement)) return false;
  const tagName = target.tagName.toLowerCase();
  return tagName === "input" || tagName === "textarea" || tagName === "select" || target.isContentEditable;
}

function isArrowKey(key: string): boolean {
  return key === "ArrowLeft" || key === "ArrowRight" || key === "ArrowUp" || key === "ArrowDown";
}

function arrowKeyDelta(key: string, distance: number): { dx: number; dy: number } {
  switch (key) {
    case "ArrowLeft":
      return { dx: -distance, dy: 0 };
    case "ArrowRight":
      return { dx: distance, dy: 0 };
    case "ArrowUp":
      return { dx: 0, dy: -distance };
    case "ArrowDown":
      return { dx: 0, dy: distance };
    default:
      return { dx: 0, dy: 0 };
  }
}

function promptInteger(label: string, fallback: number, min: number, max: number): number | null {
  const raw = window.prompt(label, String(fallback));
  if (raw === null) return null;
  const value = Math.round(Number(raw));
  if (!Number.isFinite(value)) return fallback;
  return Math.max(min, Math.min(max, value));
}
