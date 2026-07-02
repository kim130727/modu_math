import type { EditorDocument } from "../editor-core/model/editorDocument";

interface BuildOutputProps {
  document: EditorDocument | null;
}

export function BuildOutput(props: BuildOutputProps) {
  const json = () => {
    const detail = props.document?.detail;
    if (!detail) return "";
    return JSON.stringify(
      {
        semantic: detail.semantic,
        solvable: detail.solvable,
        layout: detail.layout,
        renderer: detail.renderer,
      },
      null,
      2,
    );
  };

  return (
    <section class="artifact-section">
      <div class="pane-heading">Artifacts</div>
      <pre>{json()}</pre>
    </section>
  );
}

