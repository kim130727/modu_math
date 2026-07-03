import type { EditorDocument } from "../editor-core/model/editorDocument";
import type { BuildOutputState } from "../types/api";

interface BuildOutputProps {
  document: EditorDocument | null;
  buildOutput: BuildOutputState | null;
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
      <div class="pane-heading artifact-heading">
        <span>Artifacts</span>
        {props.buildOutput ? <small>{props.buildOutput.ok ? "Build passed" : "Build failed"}</small> : null}
      </div>
      {props.buildOutput ? (
        <pre class="build-log">
          {[props.buildOutput.error, props.buildOutput.stdout, props.buildOutput.stderr].filter(Boolean).join("\n\n")}
        </pre>
      ) : null}
      <pre>{json()}</pre>
    </section>
  );
}
