import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { ProblemList } from "../components/ProblemList";
import { applyLayoutPatches, buildProblem, loadProblem, problemDetailToCanonicalProblem } from "../api/editorApi";
import { problemJsonToLayoutPatches } from "../tldraw/converters/problemJsonToLayoutPatches";
import type { EditorShape, EditorShapeDocument } from "../types/editorShape";
import type { ProblemJson } from "../types/problem";
import sampleProblem from "../samples/sample_problem.json";
import { editorDocumentToProblemJson, estimateTextWidth, fittedTextHeight, problemJsonToEditorDocument } from "./converters";
import { JsonImportExport } from "./JsonImportExport";
import { KonvaStage } from "./KonvaStage";
import { KonvaToolbar, type ShapePreset } from "./KonvaToolbar";
import { PropertyPanel } from "./PropertyPanel";

const initialProblem = sampleProblem as ProblemJson;

export function EditorKonva() {
  const [baseProblemJson, setBaseProblemJson] = useState<ProblemJson>(initialProblem);
  const [document, setDocument] = useState<EditorShapeDocument>(() => problemJsonToEditorDocument(initialProblem));
  const [selectedShapeIds, setSelectedShapeIds] = useState<string[]>([]);
  const [selectedProblemId, setSelectedProblemId] = useState(initialProblem.id);
  const [message, setMessage] = useState("Loaded sample problem in Konva editor.");
  const clipboardRef = useRef<EditorShape[]>([]);
  const imageFileInputRef = useRef<HTMLInputElement | null>(null);
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

  const insertShape = useCallback(
    (preset: ShapePreset) => {
      addShape(createShapeFromPreset(preset, nextId(preset)));
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

function createShapeFromPreset(preset: ShapePreset, id: string): EditorShape {
  const x = 220;
  const y = 180;
  const stroke = "#111827";
  const fill = "#ffffff";
  const strokeWidth = 2;

  switch (preset) {
    case "line":
      return { id, type: "line", x, y, points: [0, 0, 220, 0], stroke, strokeWidth: 3 };
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
        fill: lineLikePreset(preset) ? "none" : fill,
        stroke,
        strokeWidth,
      };
  }
}

function lineLikePreset(preset: ShapePreset): boolean {
  return preset === "arrow" || preset === "doubleArrow" || preset === "elbow" || preset === "arc" || preset === "semicircle" || preset === "quarterArc";
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
