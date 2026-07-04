import { For } from "solid-js";
import type { EditorDocument } from "../editor-core/model/editorDocument";
import type { BuildOutputState } from "../types/api";

interface BuildOutputProps {
  document: EditorDocument | null;
  buildOutput: BuildOutputState | null;
}

type ArtifactPane = {
  title: string;
  value: unknown;
};

export function BuildOutput(props: BuildOutputProps) {
  const panes = (): ArtifactPane[] => {
    const detail = props.document?.detail;
    return [
      { title: "Semantic", value: detail?.semantic ?? null },
      { title: "Solvable", value: detail?.solvable ?? null },
      { title: "Layout", value: detail?.layout ?? null },
      { title: "Renderer", value: detail?.renderer ?? null },
    ];
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
      <div class="artifact-grid">
        <For each={panes()}>
          {(pane) => (
            <label class="artifact-pane">
              <span>{pane.title}</span>
              <textarea readonly value={formatArtifact(pane.value)} />
            </label>
          )}
        </For>
      </div>
    </section>
  );
}

function formatArtifact(value: unknown): string {
  if (value === null || value === undefined) return "";
  return JSON.stringify(value, null, 2);
}
