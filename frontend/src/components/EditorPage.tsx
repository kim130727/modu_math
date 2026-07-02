import { createMemo, onMount } from "solid-js";
import { createEditorStore } from "../stores/editorStore";
import { BuildOutput } from "./BuildOutput";
import { CanvasViewport } from "./CanvasViewport";
import { DslEditor } from "./DslEditor";
import { EditorToolbar } from "./EditorToolbar";
import { ProblemList } from "./ProblemList";
import { PropertyInspector } from "./PropertyInspector";
import { StatusBar } from "./StatusBar";

export function EditorPage() {
  const store = createEditorStore();
  const selectedSlot = createMemo(() => {
    const selectedId = store.state.selectedIds[0];
    return store.state.document?.slots.find((slot) => slot.id === selectedId) ?? null;
  });

  onMount(() => {
    void store.refreshProblems();
  });

  return (
    <div class="editor-next-shell">
      <EditorToolbar store={store} />
      <div class="editor-next-workspace">
        <ProblemList store={store} />
        <main class="editor-next-stage">
          <CanvasViewport store={store} />
          <BuildOutput document={store.state.document} />
        </main>
        <aside class="editor-next-inspector">
          <PropertyInspector store={store} selectedSlot={selectedSlot()} />
          <DslEditor document={store.state.document} />
        </aside>
      </div>
      <StatusBar state={store.state} />
    </div>
  );
}

