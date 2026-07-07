import { Show, createMemo, createSignal, onCleanup, onMount } from "solid-js";
import { createEditorStore } from "../stores/editorStore";
import { BuildOutput } from "./BuildOutput";
import { CanvasViewport } from "./CanvasViewport";
import { DslEditor } from "./DslEditor";
import { EditorToolbar } from "./EditorToolbar";
import { ManualPatchPanel } from "./ManualPatchPanel";
import { ProblemList } from "./ProblemList";
import { PropertyInspector } from "./PropertyInspector";
import { StatusBar } from "./StatusBar";

export function EditorPage() {
  const store = createEditorStore();
  const [inspectorTab, setInspectorTab] = createSignal<"properties" | "dsl" | "json">("properties");
  const selectedSlot = createMemo(() => {
    const selectedId = store.state.selectedIds[0];
    return store.state.document?.slots.find((slot) => slot.id === selectedId) ?? null;
  });

  onMount(() => {
    const handleCopy = (event: ClipboardEvent) => {
      if (isEditableTarget(event.target)) return;
      if (!store.state.selectedIds.length || store.state.loading) return;
      event.preventDefault();
      store.copySelectedSlots();
    };
    const handlePaste = (event: ClipboardEvent) => {
      if (isEditableTarget(event.target)) return;
      if (store.state.loading) return;
      event.preventDefault();
      void store.pasteCopiedSlots();
    };
    const handleKeyDown = (event: KeyboardEvent) => {
      const commandKey = event.ctrlKey || event.metaKey;
      if (!isEditableTarget(event.target) && commandKey && !event.altKey) {
        const key = shortcutKey(event);
        if (key === "z") {
          event.preventDefault();
          if (event.shiftKey) void store.redo();
          else void store.undo();
          return;
        }
        if (key === "y") {
          event.preventDefault();
          void store.redo();
          return;
        }
        if (key === "s") {
          event.preventDefault();
          void store.saveDslDraft();
          return;
        }
        if (key === "c") {
          event.preventDefault();
          store.copySelectedSlots();
          return;
        }
        if (key === "v") {
          event.preventDefault();
          void store.pasteCopiedSlots();
          return;
        }
      }
      if (isEditableTarget(event.target) || event.altKey || event.ctrlKey || event.metaKey) return;
      if (event.key === "Delete" || event.key === "Backspace") {
        if (store.state.selectedIds.length === 0 || store.state.loading) return;
        event.preventDefault();
        void store.deleteSelectedSlots();
        return;
      }
      const step = event.shiftKey ? 10 : 1;
      const delta = arrowDelta(event.key, step);
      if (!delta) return;
      if (store.state.selectedIds.length === 0 || store.state.loading) return;
      event.preventDefault();
      void store.moveSelectedSlots(delta.x, delta.y);
    };

    window.addEventListener("copy", handleCopy, true);
    window.addEventListener("paste", handlePaste, true);
    window.addEventListener("keydown", handleKeyDown, true);
    onCleanup(() => {
      window.removeEventListener("copy", handleCopy, true);
      window.removeEventListener("paste", handlePaste, true);
      window.removeEventListener("keydown", handleKeyDown, true);
    });

    void (async () => {
      await store.refreshProblems();
      const requestedProblem = new URLSearchParams(window.location.search).get("problem");
      const fallbackProblem = store.state.problems.find((problem) => problem.has_svg)?.problem_id ?? store.state.problems[0]?.problem_id;
      const problemId = requestedProblem?.trim() || fallbackProblem;
      if (problemId) {
        await store.openProblem(problemId);
      }
    })();
  });

  return (
    <div class="editor-next-shell wrap powerpoint ppt-shell">
      <EditorToolbar store={store} />
      <div class="editor-next-workspace ppt-workspace">
        <ProblemList store={store} />
        <main class="editor-next-stage ppt-stage">
          <CanvasViewport store={store} />
        </main>
        <aside class="editor-next-inspector ppt-inspector">
          <div class="ppt-tabs" role="tablist" aria-label="Inspector tabs">
            <button type="button" role="tab" aria-selected={inspectorTab() === "properties"} classList={{ active: inspectorTab() === "properties" }} onClick={() => setInspectorTab("properties")}>
              Properties
            </button>
            <button type="button" role="tab" aria-selected={inspectorTab() === "dsl"} classList={{ active: inspectorTab() === "dsl" }} onClick={() => setInspectorTab("dsl")}>
              DSL
            </button>
            <button type="button" role="tab" aria-selected={inspectorTab() === "json"} classList={{ active: inspectorTab() === "json" }} onClick={() => setInspectorTab("json")}>
              JSON
            </button>
          </div>
          <Show when={inspectorTab() === "properties"}>
            <div class="ppt-tab-panel" role="tabpanel">
              <PropertyInspector store={store} selectedSlot={selectedSlot()} />
              <ManualPatchPanel store={store} />
            </div>
          </Show>
          <Show when={inspectorTab() === "dsl"}>
            <div class="ppt-tab-panel" role="tabpanel">
              <DslEditor store={store} />
            </div>
          </Show>
          <Show when={inspectorTab() === "json"}>
            <div class="ppt-tab-panel" role="tabpanel">
              <BuildOutput document={store.state.document} buildOutput={store.state.buildOutput} />
            </div>
          </Show>
        </aside>
      </div>
      <StatusBar state={store.state} />
    </div>
  );
}

function shortcutKey(event: KeyboardEvent): string {
  if (event.code === "KeyC") return "c";
  if (event.code === "KeyV") return "v";
  if (event.code === "KeyZ") return "z";
  if (event.code === "KeyY") return "y";
  if (event.code === "KeyS") return "s";
  return event.key.toLowerCase();
}

function arrowDelta(key: string, step: number): { x: number; y: number } | null {
  switch (key) {
    case "ArrowLeft":
      return { x: -step, y: 0 };
    case "ArrowRight":
      return { x: step, y: 0 };
    case "ArrowUp":
      return { x: 0, y: -step };
    case "ArrowDown":
      return { x: 0, y: step };
    default:
      return null;
  }
}

function isEditableTarget(target: EventTarget | null): boolean {
  const element = target instanceof HTMLElement ? target : null;
  if (!element) return false;
  const tagName = element.tagName.toLowerCase();
  return tagName === "input" || tagName === "textarea" || tagName === "select" || element.isContentEditable;
}
