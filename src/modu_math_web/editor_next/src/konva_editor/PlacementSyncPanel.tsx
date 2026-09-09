import { useEffect, useState } from "react";
import { listProblems, syncTextPlacements, type PlacementSyncResult } from "../api/editorApi";
import type { EditorShape } from "../types/editorShape";

const languageNames: Record<string, string> = { ko: "한국어", en: "영어", ja: "일본어", zh: "중국어", uk: "우크라이나어", km: "크메르어" };
const placementRoles = new Set(["", "question", "instruction", "choice", "diagram_label"]);

export function textPlacements(shapes: EditorShape[], selectedIds?: string[]) {
  return shapes.filter((shape) => shape.type === "text" && (!selectedIds || selectedIds.includes(shape.id))
    && placementRoles.has(shape.semanticRole ?? ""))
    .map((shape) => ({ id: shape.id, role: shape.semanticRole ?? "" }));
}

interface Props {
  problemId: string;
  shapes: EditorShape[];
  selectedIds: string[];
  onSave: () => Promise<boolean>;
}

export function PlacementSyncPanel({ problemId, shapes, selectedIds, onSave }: Props) {
  const [languages, setLanguages] = useState<string[]>([]);
  const [chosen, setChosen] = useState<string[]>([]);
  const [sourceLanguage, setSourceLanguage] = useState("");
  const [scope, setScope] = useState<"selected" | "all">("selected");
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [results, setResults] = useState<PlacementSyncResult[]>([]);
  const placements = textPlacements(shapes, scope === "selected" ? selectedIds : undefined);

  useEffect(() => {
    let canceled = false;
    listProblems().then(({ problems }) => {
      if (canceled) return;
      const source = problems.find((problem) => problem.problem_id === problemId);
      const targets = Object.keys(source?.equivalent_problem_ids ?? {}).filter((language) => language !== source?.language);
      setSourceLanguage(source?.language ?? "");
      setLanguages(targets);
      setChosen(targets);
    }).catch((err) => { if (!canceled) setError(String(err)); })
      .finally(() => { if (!canceled) setLoading(false); });
    return () => { canceled = true; };
  }, [problemId]);

  async function apply() {
    if (busy || !placements.length || !chosen.length) return;
    setBusy(true);
    setError("");
    setResults([]);
    try {
      if (!await onSave()) throw new Error("원본 문항 저장·빌드에 실패했습니다. 저장 상태를 확인하세요.");
      const response = await syncTextPlacements(problemId, chosen, placements);
      setResults(response.results);
    } catch (err) {
      setError(String(err));
    } finally {
      setBusy(false);
    }
  }

  return <section className="placement-sync-panel" aria-label="표시 위치 다국어 적용">
    <details>
      <summary>표시 위치를 다국어에 적용</summary>
      <p>현재 {languageNames[sourceLanguage] ?? sourceLanguage} 문항의 표시 위치를 같은 문항의 번역본에 적용합니다. 번역문·좌표·글자 크기는 유지합니다.</p>
      {loading ? <p role="status">번역 언어를 확인하고 있습니다…</p> : !languages.length ? <p>적용할 번역 문항이 없습니다.</p> : <>
        <fieldset disabled={busy}>
          <legend>적용 범위</legend>
          <label><input type="radio" name={`placement-scope-${problemId}`} checked={scope === "selected"} onChange={() => setScope("selected")} />선택한 글자만</label>
          <label><input type="radio" name={`placement-scope-${problemId}`} checked={scope === "all"} onChange={() => setScope("all")} />이 문항 전체</label>
        </fieldset>
        <fieldset disabled={busy}>
          <legend>대상 언어</legend>
          <label><input type="checkbox" checked={chosen.length === languages.length} onChange={(event) => setChosen(event.target.checked ? languages : [])} />모든 번역 언어</label>
          {languages.map((language) => <label key={language}><input type="checkbox" checked={chosen.includes(language)} onChange={(event) => setChosen((current) => event.target.checked ? [...current, language] : current.filter((item) => item !== language))} />{languageNames[language] ?? language}</label>)}
        </fieldset>
        <p>글자 {placements.length}개 · 대상 {chosen.length}개 언어. 대상의 기존 표시 위치를 덮어씁니다. 현재 문항의 수정 사항도 저장합니다.</p>
        <button type="button" disabled={busy || !placements.length || !chosen.length} onClick={() => void apply()}>{busy ? "언어별 저장·빌드 중…" : "다국어에 적용"}</button>
      </>}
      {error && <p role="alert">{error}</p>}
      <div aria-live="polite">
        {results.map((result) => <div key={result.language} className="placement-sync-result">
          <strong>{languageNames[result.language] ?? result.language}: {result.status === "success" ? "완료" : result.status === "error" ? "실패" : "확인 필요"}</strong>
          <p>{result.applied}개 {result.status === "error" && result.saved ? "저장됨 · 빌드 실패" : "적용"}{result.missing.length > 0 ? ` · 대응 글자 ${result.missing.length}개 없음` : ""}</p>
          {result.error && <p>{result.error}</p>}
          {result.missing.length > 0 && <details><summary>대응하지 않는 글자 보기</summary><ul>{result.missing.map((id) => {
            const shape = shapes.find((item) => item.id === id);
            return <li key={id}>{shape?.type === "text" ? shape.text : "원본 글자를 찾을 수 없습니다."}</li>;
          })}</ul></details>}
        </div>)}
      </div>
    </details>
  </section>;
}
