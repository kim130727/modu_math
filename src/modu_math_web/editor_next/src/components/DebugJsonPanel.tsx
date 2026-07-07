import type { ProblemJson } from "../types/problem";

interface DebugJsonPanelProps {
  problem: ProblemJson;
  message?: string;
}

export function DebugJsonPanel({ problem, message }: DebugJsonPanelProps) {
  return (
    <aside className="debug-json-panel">
      <div className="panel-title">Canonical Problem JSON</div>
      {message ? <div className="panel-message">{message}</div> : null}
      <pre>{JSON.stringify(problem, null, 2)}</pre>
    </aside>
  );
}
