import { useEffect, useState } from "react";
import type { EditorShapeDocument } from "../types/editorShape";

interface JsonImportExportProps {
  document: EditorShapeDocument;
  message: string;
  onImport: (document: EditorShapeDocument) => void;
}

export function JsonImportExport({ document, message, onImport }: JsonImportExportProps) {
  const [draft, setDraft] = useState(() => JSON.stringify(document, null, 2));
  const [error, setError] = useState("");

  useEffect(() => {
    setDraft(JSON.stringify(document, null, 2));
    setError("");
  }, [document]);

  return (
    <section className="konva-json-panel">
      <div className="panel-title">Shape JSON</div>
      <div className={error ? "problem-list-error" : "panel-message"}>{error || message}</div>
      <textarea
        value={draft}
        onChange={(event) => {
          const nextDraft = event.target.value;
          setDraft(nextDraft);
          try {
            onImport(JSON.parse(nextDraft) as EditorShapeDocument);
            setError("");
          } catch (parseError) {
            setError(`Invalid JSON: ${String(parseError)}`);
          }
        }}
        spellCheck={false}
      />
    </section>
  );
}
