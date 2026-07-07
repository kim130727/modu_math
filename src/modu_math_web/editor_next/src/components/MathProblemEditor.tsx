import { useCallback, useMemo, useState } from "react";
import { createShapeId, type Editor, Tldraw, toRichText } from "tldraw";
import { DebugJsonPanel } from "./DebugJsonPanel";
import { Toolbar } from "./Toolbar";
import { problemJsonToTldrawShapes } from "../tldraw/converters/problemJsonToTldraw";
import { tldrawToProblemJson } from "../tldraw/converters/tldrawToProblemJson";
import { FractionBarShapeUtil } from "../tldraw/shapes/FractionBarShape";
import { GroupObjectsShapeUtil } from "../tldraw/shapes/GroupObjectsShape";
import { MathTextShapeUtil } from "../tldraw/shapes/MathTextShape";
import { NumberLineShapeUtil } from "../tldraw/shapes/NumberLineShape";
import type { ProblemJson } from "../types/problem";
import sampleProblem from "../samples/sample_problem.json";

const initialProblem = sampleProblem as ProblemJson;

const shapeUtils = [MathTextShapeUtil, FractionBarShapeUtil, NumberLineShapeUtil, GroupObjectsShapeUtil];

export function MathProblemEditor() {
  const [editor, setEditor] = useState<Editor | null>(null);
  const [problemJson, setProblemJson] = useState<ProblemJson>(initialProblem);
  const shapeIdPrefix = useMemo(() => `mvp_${Date.now()}`, []);

  const updateDebugJson = useCallback(() => {
    if (!editor) return;
    setProblemJson(tldrawToProblemJson(editor, initialProblem));
  }, [editor]);

  const handleMount = useCallback((mountedEditor: Editor) => {
    setEditor(mountedEditor);
    mountedEditor.createShapes(problemJsonToTldrawShapes(initialProblem));
    mountedEditor.zoomToFit();
    setProblemJson(initialProblem);
  }, []);

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
      props: { latex: "x + 1 = 5", text: "x + 1 = 5", fontSize: 32, w: 260, h: 56 },
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

  const saveJson = useCallback(() => {
    if (!editor) return;
    const nextProblem = tldrawToProblemJson(editor, initialProblem);
    setProblemJson(nextProblem);
    console.log("canonical problem JSON", nextProblem);
    // TODO: POST this JSON to a Python DSL conversion endpoint.
    // TODO: trigger Python/SVG/PNG/Flutter asset export after canonical JSON is saved.
  }, [editor]);

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
        onRefreshJson={updateDebugJson}
        onSave={saveJson}
      />
      <div className="editor-body">
        <div className="tldraw-stage">
          <Tldraw shapeUtils={shapeUtils} onMount={handleMount} />
        </div>
        <DebugJsonPanel problem={problemJson} />
      </div>
    </div>
  );
}
