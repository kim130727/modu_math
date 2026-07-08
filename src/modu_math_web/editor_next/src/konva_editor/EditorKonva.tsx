import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { ProblemList } from "../components/ProblemList";
import { applyLayoutPatches, buildProblem, loadProblem, problemDetailToCanonicalProblem } from "../api/editorApi";
import { problemJsonToLayoutPatches } from "../tldraw/converters/problemJsonToLayoutPatches";
import type { EditorShape, EditorShapeDocument } from "../types/editorShape";
import type { ProblemJson } from "../types/problem";
import sampleProblem from "../samples/sample_problem.json";
import { editorDocumentToProblemJson, estimateTextWidth, problemJsonToEditorDocument } from "./converters";
import { JsonImportExport } from "./JsonImportExport";
import { KonvaStage } from "./KonvaStage";
import { KonvaToolbar } from "./KonvaToolbar";
import { PropertyPanel } from "./PropertyPanel";

const initialProblem = sampleProblem as ProblemJson;

export function EditorKonva() {
  const [baseProblemJson, setBaseProblemJson] = useState<ProblemJson>(initialProblem);
  const [document, setDocument] = useState<EditorShapeDocument>(() => problemJsonToEditorDocument(initialProblem));
  const [selectedShapeIds, setSelectedShapeIds] = useState<string[]>([]);
  const [selectedProblemId, setSelectedProblemId] = useState(initialProblem.id);
  const [message, setMessage] = useState("Loaded sample problem in Konva editor.");
  const clipboardRef = useRef<EditorShape[]>([]);
  const idPrefix = useMemo(() => `konva_${Date.now()}`, []);

  const selectedShape = selectedShapeIds.length === 1 ? document.shapes.find((shape) => shape.id === selectedShapeIds[0]) ?? null : null;

  const setProblem = useCallback((problem: ProblemJson, nextMessage: string) => {
    setBaseProblemJson(problem);
    setDocument(problemJsonToEditorDocument(problem));
    setSelectedProblemId(problem.id);
    setSelectedShapeIds([]);
    setMessage(nextMessage);
  }, []);

  const openProblem = useCallback(
    async (problemId: string) => {
      setMessage(`Loading ${problemId}...`);
      try {
        const detail = await loadProblem(problemId);
        setProblem(problemDetailToCanonicalProblem(detail), `Loaded ${problemId}.`);
      } catch (error) {
        setMessage(`Could not load ${problemId}: ${String(error)}`);
      }
    },
    [setProblem],
  );

  const updateShape = useCallback((nextShape: EditorShape) => {
    setDocument((current) => ({
      ...current,
      shapes: current.shapes.map((shape) => (shape.id === nextShape.id ? nextShape : shape)),
    }));
  }, []);

  const updateShapes = useCallback((nextShapes: EditorShape[]) => {
    const nextShapeById = new Map(nextShapes.map((shape) => [shape.id, shape]));
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
      setDocument((current) => ({ ...current, shapes: [...current.shapes, shape] }));
      setSelectedShapeIds([shape.id]);
    },
    [],
  );

  const addShapes = useCallback((shapes: EditorShape[]) => {
    if (!shapes.length) return;
    setDocument((current) => ({ ...current, shapes: [...current.shapes, ...shapes] }));
    setSelectedShapeIds(shapes.map((shape) => shape.id));
  }, []);

  const nextId = useCallback((kind: string) => `${idPrefix}_${kind}_${Math.round(performance.now())}`, [idPrefix]);

  const addRectangle = useCallback(() => {
    addShape({
      id: nextId("rect"),
      type: "rect",
      x: 160,
      y: 120,
      width: 180,
      height: 100,
      fill: "transparent",
      stroke: "#111827",
      strokeWidth: 2,
    });
  }, [addShape, nextId]);

  const addCircle = useCallback(() => {
    addShape({
      id: nextId("circle"),
      type: "circle",
      x: 420,
      y: 180,
      radius: 60,
      fill: "transparent",
      stroke: "#111827",
      strokeWidth: 2,
    });
  }, [addShape, nextId]);

  const addLine = useCallback(() => {
    addShape({
      id: nextId("line"),
      type: "line",
      x: 180,
      y: 320,
      points: [0, 0, 220, 0],
      stroke: "#111827",
      strokeWidth: 3,
    });
  }, [addShape, nextId]);

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
      fill: "#111827",
      width: autoTextWidth(text, fontSize),
      height: 48,
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
    const src = window.prompt("Image URL or data URL", "");
    if (src === null) return;
    addShape({
      id: nextId("image"),
      type: "image",
      x: 520,
      y: 280,
      src,
      width: 180,
      height: 120,
    });
  }, [addShape, nextId]);

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
          height: cellHeight - 12,
          align: "center",
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
  }, [copySelected, deleteSelected, duplicateSelected, pasteClipboard, selectedShapeIds.length]);

  const refreshJson = useCallback(() => {
    setDocument((current) => ({ ...current }));
    setMessage("Shape JSON refreshed.");
  }, []);

  const importDocument = useCallback((nextDocument: EditorShapeDocument) => {
    if (!Array.isArray(nextDocument.shapes) || !nextDocument.canvas) return;
    setDocument(nextDocument);
    setSelectedProblemId(nextDocument.id);
    setSelectedShapeIds([]);
    setMessage("Imported shape JSON.");
  }, []);

  const saveJson = useCallback(async () => {
    const nextProblem = editorDocumentToProblemJson(document, baseProblemJson);
    if (nextProblem.id === initialProblem.id) {
      setMessage("Sample problem is local only. Open a real problem before saving to DSL.");
      return;
    }

    const patches = problemJsonToLayoutPatches(baseProblemJson, nextProblem);
    if (!patches.length) {
      setMessage(`No DSL changes to save for ${nextProblem.id}.`);
      return;
    }

    setMessage(`Saving ${patches.length} patch(es) to DSL...`);
    try {
      const response = await applyLayoutPatches(nextProblem.id, patches, { format: true });
      setBaseProblemJson(nextProblem);
      setMessage(`Saved to DSL: ${response.applied.length} patch(es). Rebuild to refresh artifacts.`);
    } catch (error) {
      setMessage(`Could not save DSL: ${String(error)}`);
    }
  }, [baseProblemJson, document]);

  const buildCurrentProblem = useCallback(async () => {
    if (document.id === initialProblem.id) {
      setMessage("Sample problem is local only. Open a real problem before building.");
      return;
    }

    setMessage(`Building ${document.id}...`);
    try {
      const response = await buildProblem(document.id);
      const detail = [response.stdout, response.stderr].filter(Boolean).join("\n").trim();
      setMessage(detail ? `Build complete for ${document.id}.\n${detail}` : `Build complete for ${document.id}.`);
    } catch (error) {
      setMessage(`Could not build ${document.id}: ${String(error)}`);
    }
  }, [document.id]);

  return (
    <div className="math-problem-editor konva-editor">
      <KonvaToolbar
        hasSelection={selectedShapeIds.length > 0}
        onAddMath={addMath}
        onAddProperFraction={addProperFraction}
        onAddMixedFraction={addMixedFraction}
        onAddRectangle={addRectangle}
        onAddCircle={addCircle}
        onAddLine={addLine}
        onAddText={addText}
        onAddImage={addImage}
        onAddTable={addTable}
        onAddGraphPaper={addGraphPaper}
        onDeleteSelected={deleteSelected}
        onRefreshJson={refreshJson}
        onSave={saveJson}
        onBuild={buildCurrentProblem}
      />
      <div className="editor-body konva-editor-body">
        <ProblemList selectedProblemId={selectedProblemId} onOpenProblem={openProblem} />
        <KonvaStage
          width={document.canvas.width}
          height={document.canvas.height}
          shapes={document.shapes}
          selectedShapeIds={selectedShapeIds}
          onSelectShapes={setSelectedShapeIds}
          onChangeShapes={updateShapes}
        />
        <div className="konva-side-panel">
          <PropertyPanel shape={selectedShape} onChange={patchSelectedShape} />
          <JsonImportExport document={document} message={message} onImport={importDocument} />
        </div>
      </div>
    </div>
  );
}

function cloneShape<T extends EditorShape>(shape: T): T {
  return JSON.parse(JSON.stringify(shape)) as T;
}

function applyAutoSizing(nextShape: EditorShape, previousShape: EditorShape): EditorShape {
  if (nextShape.type === "text" && previousShape.type === "text") return applyAutoTextSizing(nextShape, previousShape);
  if (nextShape.type === "math" && previousShape.type === "math") return applyAutoMathSizing(nextShape, previousShape);
  return nextShape;
}

function applyAutoTextSizing(nextShape: Extract<EditorShape, { type: "text" }>, previousShape: Extract<EditorShape, { type: "text" }>): EditorShape {
  if (nextShape.sourceKind === "text_box") return nextShape;
  if (nextShape.text === previousShape.text && nextShape.fontSize === previousShape.fontSize) return nextShape;
  return {
    ...nextShape,
    width: Math.max(nextShape.width ?? 0, autoTextWidth(nextShape.text, nextShape.fontSize)),
    height: Math.max(nextShape.height ?? 0, nextShape.fontSize * 1.6),
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

function isEditableTarget(target: EventTarget | null): boolean {
  if (!(target instanceof HTMLElement)) return false;
  const tagName = target.tagName.toLowerCase();
  return tagName === "input" || tagName === "textarea" || tagName === "select" || target.isContentEditable;
}

function promptInteger(label: string, fallback: number, min: number, max: number): number | null {
  const raw = window.prompt(label, String(fallback));
  if (raw === null) return null;
  const value = Math.round(Number(raw));
  if (!Number.isFinite(value)) return fallback;
  return Math.max(min, Math.min(max, value));
}
