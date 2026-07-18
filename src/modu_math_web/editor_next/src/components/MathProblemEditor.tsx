import { useCallback, useMemo, useState } from "react";
import { createShapeId, type Editor, Tldraw, toRichText, type TLCreateShapePartial, type TLShape } from "tldraw";
import { DebugJsonPanel } from "./DebugJsonPanel";
import { ProblemList } from "./ProblemList";
import { Toolbar } from "./Toolbar";
import { applyLayoutPatches, loadProblem, problemDetailToCanonicalProblem } from "../api/editorApi";
import { problemJsonToLayoutPatches } from "../tldraw/converters/problemJsonToLayoutPatches";
import { problemJsonToTldrawShapes } from "../tldraw/converters/problemJsonToTldraw";
import { tldrawToProblemJson } from "../tldraw/converters/tldrawToProblemJson";
import { AngleMarkerShapeUtil } from "../tldraw/shapes/AngleMarkerShape";
import { CANVAS_FRAME_ID, CanvasFrameShapeUtil } from "../tldraw/shapes/CanvasFrameShape";
import { FractionBarShapeUtil } from "../tldraw/shapes/FractionBarShape";
import { GroupObjectsShapeUtil } from "../tldraw/shapes/GroupObjectsShape";
import { LayoutImageShapeUtil } from "../tldraw/shapes/LayoutImageShape";
import { LayoutLineShapeUtil } from "../tldraw/shapes/LayoutLineShape";
import { LayoutPathShapeUtil } from "../tldraw/shapes/LayoutPathShape";
import { LayoutRectShapeUtil } from "../tldraw/shapes/LayoutRectShape";
import { MathTextShapeUtil } from "../tldraw/shapes/MathTextShape";
import { NumberLineShapeUtil } from "../tldraw/shapes/NumberLineShape";
import { SpeechBubbleShapeUtil } from "../tldraw/shapes/SpeechBubbleShape";
import { TableShapeUtil } from "../tldraw/shapes/TableShape";
import type { ProblemJson } from "../types/problem";
import sampleProblem from "../samples/sample_problem.json";

const initialProblem = sampleProblem as ProblemJson;

const shapeUtils = [
  CanvasFrameShapeUtil,
  MathTextShapeUtil,
  LayoutRectShapeUtil,
  LayoutLineShapeUtil,
  LayoutImageShapeUtil,
  LayoutPathShapeUtil,
  FractionBarShapeUtil,
  NumberLineShapeUtil,
  GroupObjectsShapeUtil,
  TableShapeUtil,
  SpeechBubbleShapeUtil,
  AngleMarkerShapeUtil,
];

export function MathProblemEditor() {
  const [editor, setEditor] = useState<Editor | null>(null);
  const [problemJson, setProblemJson] = useState<ProblemJson>(initialProblem);
  const [baseProblemJson, setBaseProblemJson] = useState<ProblemJson>(initialProblem);
  const [selectedProblemId, setSelectedProblemId] = useState(initialProblem.id);
  const [loadMessage, setLoadMessage] = useState("Loaded sample problem.");
  const shapeIdPrefix = useMemo(() => `mvp_${Date.now()}`, []);

  const updateDebugJson = useCallback(() => {
    if (!editor) return;
    setProblemJson(tldrawToProblemJson(editor, baseProblemJson));
  }, [baseProblemJson, editor]);

  const loadProblemJsonIntoEditor = useCallback((targetEditor: Editor, nextProblem: ProblemJson) => {
    const currentShapes = targetEditor.getCurrentPageShapes();
    if (currentShapes.length) targetEditor.deleteShapes(currentShapes);
    targetEditor.createShapes(problemJsonToTldrawShapes(nextProblem));
    targetEditor.zoomToFit();
    setBaseProblemJson(nextProblem);
    setProblemJson(nextProblem);
    setSelectedProblemId(nextProblem.id);
  }, []);

  const handleMount = useCallback((mountedEditor: Editor) => {
    setEditor(mountedEditor);
    loadProblemJsonIntoEditor(mountedEditor, initialProblem);
  }, [loadProblemJsonIntoEditor]);

  const openProblem = useCallback(
    async (problemId: string) => {
      if (!editor) return;
      setLoadMessage(`Loading ${problemId}...`);
      try {
        const detail = await loadProblem(problemId);
        const nextProblem = problemDetailToCanonicalProblem(detail);
        loadProblemJsonIntoEditor(editor, nextProblem);
        setLoadMessage(`Loaded ${problemId}.`);
      } catch (error) {
        setLoadMessage(`Could not load ${problemId}: ${String(error)}`);
      }
    },
    [editor, loadProblemJsonIntoEditor],
  );

  const nextShapeId = useCallback(
    (kind: string) => createShapeId(`${shapeIdPrefix}_${kind}_${Math.round(performance.now())}`),
    [shapeIdPrefix],
  );

  const addMathText = useCallback(() => {
    if (!editor) return;
    editor.createShape({
      id: nextShapeId("math_text"),
      type: "math_text",
      x: 160,
      y: 120,
      props: {
        latex: "x + 1 = 5",
        text: "x + 1 = 5",
        fontSize: 32,
        w: 260,
        h: 56,
        color: "#050816",
        textAlign: "left",
        lineHeight: 1.25,
        sourceKind: "text_box",
      },
    });
    updateDebugJson();
  }, [editor, nextShapeId, updateDebugJson]);

  const editSelectedMathText = useCallback(() => {
    if (!editor) return;
    const selected = editor.getSelectedShapes().find((shape) => shape.type === "math_text");
    if (!selected || selected.type !== "math_text") return;
    const current = (selected.props as { latex?: string }).latex ?? "";
    const next = window.prompt("MathText latex/text", current);
    if (next === null) return;
    editor.updateShape({
      id: selected.id,
      type: "math_text",
      props: { latex: next, text: next },
    });
    updateDebugJson();
  }, [editor, updateDebugJson]);

  const setSelectedTextFontSize = useCallback(() => {
    if (!editor) return;
    const selected = editor.getSelectedShapes().filter((shape) => shape.type === "math_text");
    if (!selected.length) return;
    const current = (selected[0].props as { fontSize?: number }).fontSize ?? 28;
    const fontSize = promptInteger("Font size", Math.round(current), 8, 120);
    if (fontSize === null) return;
    for (const shape of selected) {
      if (shape.type !== "math_text") continue;
      const props = shape.props as { h?: number; lineHeight?: number; text?: string; latex?: string };
      const lineCount = Math.max(1, String(props.text || props.latex || "").split(/\n/g).length);
      editor.updateShape({
        id: shape.id,
        type: "math_text",
        props: {
          fontSize,
          h: Math.max(props.h ?? 0, fontSize * (props.lineHeight ?? 1.2) * lineCount),
        },
      });
    }
    updateDebugJson();
  }, [editor, updateDebugJson]);

  const setCanvasSize = useCallback(() => {
    if (!editor) return;
    const currentProblem = tldrawToProblemJson(editor, baseProblemJson);
    const width = promptInteger("Canvas width", Math.round(currentProblem.canvas.width), 100, 5000);
    if (width === null) return;
    const height = promptInteger("Canvas height", Math.round(currentProblem.canvas.height), 100, 5000);
    if (height === null) return;
    editor.updateShape({
      id: createShapeId(CANVAS_FRAME_ID),
      type: "canvas_frame",
      x: 0,
      y: 0,
      props: { w: width, h: height },
    });
    const nextProblem = tldrawToProblemJson(editor, baseProblemJson);
    setProblemJson(nextProblem);
  }, [baseProblemJson, editor]);

  const addRectangle = useCallback(() => {
    if (!editor) return;
    editor.createShape({
      id: nextShapeId("rect"),
      type: "geo",
      x: 520,
      y: 160,
      props: { geo: "rectangle", w: 180, h: 100, color: "black", fill: "none", richText: toRichText("") },
    });
    updateDebugJson();
  }, [editor, nextShapeId, updateDebugJson]);

  const addCircle = useCallback(() => {
    if (!editor) return;
    editor.createShape({
      id: nextShapeId("circle"),
      type: "geo",
      x: 740,
      y: 160,
      props: { geo: "ellipse", w: 120, h: 120, color: "black", fill: "none", richText: toRichText("") },
    });
    updateDebugJson();
  }, [editor, nextShapeId, updateDebugJson]);

  const addFractionBar = useCallback(() => {
    if (!editor) return;
    editor.createShape({
      id: nextShapeId("fraction_bar"),
      type: "fraction_bar",
      x: 160,
      y: 240,
      props: { denominator: 4, colored: 1, w: 320, h: 56 },
    });
    updateDebugJson();
  }, [editor, nextShapeId, updateDebugJson]);

  const addNumberLine = useCallback(() => {
    if (!editor) return;
    editor.createShape({
      id: nextShapeId("number_line"),
      type: "number_line",
      x: 160,
      y: 360,
      props: { start: 0, end: 8, step: 1, w: 520, h: 96 },
    });
    updateDebugJson();
  }, [editor, nextShapeId, updateDebugJson]);

  const addGroupObjects = useCallback(() => {
    if (!editor) return;
    editor.createShape({
      id: nextShapeId("group_objects"),
      type: "group_objects",
      x: 160,
      y: 500,
      props: { item: "circle", groups: 2, countPerGroup: 5, gap: 12, w: 300, h: 120 },
    });
    updateDebugJson();
  }, [editor, nextShapeId, updateDebugJson]);

  const addTable = useCallback(() => {
    if (!editor) return;
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
    const prefix = `${shapeIdPrefix}_table_${Math.round(performance.now())}`;
    const shapes: TLCreateShapePartial<TLShape>[] = [
      {
        id: createShapeId(`${prefix}_outer`),
        type: "layout_rect",
        x,
        y,
        props: { w: width, h: height, fill: "#ffffff", stroke: "#111827", strokeWidth: 1 },
      },
    ];

    for (let col = 1; col < cols; col += 1) {
      shapes.push({
        id: createShapeId(`${prefix}_v${col}`),
        type: "layout_line",
        x: x + col * cellWidth,
        y,
        props: { w: 0, h: height, stroke: "#111827", strokeWidth: 1 },
      });
    }

    for (let row = 1; row < rows; row += 1) {
      shapes.push({
        id: createShapeId(`${prefix}_h${row}`),
        type: "layout_line",
        x,
        y: y + row * cellHeight,
        props: { w: width, h: 0, stroke: "#111827", strokeWidth: 1 },
      });
    }

    for (let row = 0; row < rows; row += 1) {
      for (let col = 0; col < cols; col += 1) {
        shapes.push({
          id: createShapeId(`${prefix}_r${row + 1}c${col + 1}`),
          type: "math_text",
          x: x + col * cellWidth,
          y: y + row * cellHeight + 10,
          props: {
            latex: "",
            text: "",
            fontSize: 24,
            w: cellWidth,
            h: cellHeight - 12,
            color: "#111827",
            textAlign: "center",
            lineHeight: 1.15,
            sourceKind: "text",
          },
        });
      }
    }

    editor.createShapes(shapes);
    editor.setSelectedShapes(shapes.map((shape) => shape.id).filter((id): id is NonNullable<typeof id> => Boolean(id)));
    updateDebugJson();
  }, [editor, shapeIdPrefix, updateDebugJson]);

  const addGraphPaper = useCallback(() => {
    if (!editor) return;
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
    const base = uniqueGraphPaperBase(editor);
    const shapes: TLCreateShapePartial<TLShape>[] = [];

    for (let col = 0; col <= cols; col += 1) {
      shapes.push({
        id: createShapeId(`${base}.v${col}`),
        type: "layout_line",
        x: x + col * cellSize,
        y,
        props: { w: 0, h: height, stroke, strokeWidth },
      });
    }

    for (let row = 0; row <= rows; row += 1) {
      shapes.push({
        id: createShapeId(`${base}.h${row}`),
        type: "layout_line",
        x,
        y: y + row * cellSize,
        props: { w: width, h: 0, stroke, strokeWidth },
      });
    }

    editor.createShapes(shapes);
    editor.setSelectedShapes(shapes.map((shape) => shape.id).filter((id): id is NonNullable<typeof id> => Boolean(id)));
    updateDebugJson();
  }, [editor, updateDebugJson]);

  const addSpeechBubble = useCallback(() => {
    if (!editor) return;
    editor.createShape({
      id: nextShapeId("speech_bubble"),
      type: "speech_bubble",
      x: 180,
      y: 160,
      props: { w: 190, h: 84, tailX: 48, tailY: 116, fill: "#ffffff", stroke: "#111827", strokeWidth: 2 },
    });
    updateDebugJson();
  }, [editor, nextShapeId, updateDebugJson]);

  const addAngleMarker = useCallback(() => {
    if (!editor) return;
    editor.createShape({
      id: nextShapeId("angle_marker"),
      type: "angle_marker",
      x: 180,
      y: 160,
      props: { w: 120, h: 90, radius: 34, stroke: "#111827", strokeWidth: 2 },
    });
    updateDebugJson();
  }, [editor, nextShapeId, updateDebugJson]);

  const saveJson = useCallback(async () => {
    if (!editor) return;
    const nextProblem = tldrawToProblemJson(editor, baseProblemJson);
    setProblemJson(nextProblem);
    console.log("canonical problem JSON", nextProblem);
    if (nextProblem.id === initialProblem.id) {
      setLoadMessage("Sample problem is local only. Open a real problem before saving to DSL.");
      return;
    }

    const patches = problemJsonToLayoutPatches(baseProblemJson, nextProblem);
    if (!patches.length) {
      setLoadMessage(`No DSL changes to save for ${nextProblem.id}.`);
      return;
    }

    setLoadMessage(`Saving ${patches.length} patch(es) to DSL...`);
    try {
      const response = await applyLayoutPatches(nextProblem.id, patches, { format: false });
      setBaseProblemJson(nextProblem);
      setLoadMessage(`Saved to DSL: ${response.applied.length} patch(es). Rebuild to refresh artifacts.`);
      // TODO: optionally call layout-patch-and-build after save when the UI has an explicit Build toggle.
      // TODO: expand adapter coverage for path/polygon/table/group semantic shapes.
    } catch (error) {
      setLoadMessage(`Could not save DSL: ${String(error)}`);
    }
  }, [baseProblemJson, editor]);

  return (
    <div className="math-problem-editor">
      <Toolbar
        editor={editor}
        onAddMathText={addMathText}
        onEditSelectedMathText={editSelectedMathText}
        onAddRectangle={addRectangle}
        onAddCircle={addCircle}
        onAddFractionBar={addFractionBar}
        onAddNumberLine={addNumberLine}
        onAddGroupObjects={addGroupObjects}
        onAddTable={addTable}
        onAddGraphPaper={addGraphPaper}
        onAddSpeechBubble={addSpeechBubble}
        onAddAngleMarker={addAngleMarker}
        onRefreshJson={updateDebugJson}
        onSetSelectedTextFontSize={setSelectedTextFontSize}
        onSetCanvasSize={setCanvasSize}
        onSave={saveJson}
      />
      <div className="editor-body">
        <ProblemList selectedProblemId={selectedProblemId} onOpenProblem={openProblem} />
        <div className="tldraw-stage">
          <Tldraw shapeUtils={shapeUtils} onMount={handleMount} />
        </div>
        <DebugJsonPanel problem={problemJson} message={loadMessage} />
      </div>
    </div>
  );
}

function promptInteger(label: string, fallback: number, min: number, max: number): number | null {
  const raw = window.prompt(label, String(fallback));
  if (raw === null) return null;
  const value = Math.round(Number(raw));
  if (!Number.isFinite(value)) return fallback;
  return Math.max(min, Math.min(max, value));
}

function uniqueGraphPaperBase(editor: Editor): string {
  const used = new Set<string>();
  for (const shape of editor.getCurrentPageShapes()) {
    const id = shape.id.replace(/^shape:/, "");
    const match = id.match(/^(slot\.graphpaper(?:_\d+)?)(?:\.|$)/);
    if (match) used.add(match[1]);
  }
  if (!used.has("slot.graphpaper")) return "slot.graphpaper";
  for (let index = 1; index < 10000; index += 1) {
    const candidate = `slot.graphpaper_${index}`;
    if (!used.has(candidate)) return candidate;
  }
  return `slot.graphpaper_${Date.now()}`;
}
