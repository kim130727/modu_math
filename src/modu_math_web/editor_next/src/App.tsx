import { lazy, Suspense } from "react";
import { EditorKonva } from "./konva_editor/EditorKonva";

const MathProblemEditor = lazy(() =>
  import("./components/MathProblemEditor").then((module) => ({ default: module.MathProblemEditor })),
);

export default function App() {
  const rootMode = document.getElementById("root")?.dataset.editorMode;
  const EditorComponent = rootMode === "tldraw" ? MathProblemEditor : EditorKonva;
  return (
    <Suspense fallback={<div className="editor-loading">Loading editor...</div>}>
      <EditorComponent />
    </Suspense>
  );
}
