import { lazy, Suspense } from "react";

const MathProblemEditor = lazy(() =>
  import("./components/MathProblemEditor").then((module) => ({ default: module.MathProblemEditor })),
);
const EditorKonva = lazy(() => import("./konva_editor/EditorKonva").then((module) => ({ default: module.EditorKonva })));

export default function App() {
  const EditorComponent = window.location.pathname.includes("editor-konva") ? EditorKonva : MathProblemEditor;
  return (
    <Suspense fallback={<div className="editor-loading">Loading editor...</div>}>
      <EditorComponent />
    </Suspense>
  );
}
