import type { ProblemJson } from "../types/problem";

interface DebugJsonPanelProps {
  problem: ProblemJson;
}

export function DebugJsonPanel({ problem }: DebugJsonPanelProps) {
  return (
    <aside className="debug-json-panel">
      <div className="panel-title">Canonical Problem JSON</div>
      <pre>{JSON.stringify(problem, null, 2)}</pre>
    </aside>
  );
}
