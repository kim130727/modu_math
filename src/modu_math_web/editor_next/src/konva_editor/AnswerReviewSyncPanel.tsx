import { useEffect, useState } from "react";
import { listProblems, syncAnswerReviews, type AnswerReviewSyncResult } from "../api/editorApi";

const languageNames: Record<string, string> = { ko: "한국어", en: "영어", ja: "일본어", zh: "중국어", uk: "우크라이나어", km: "크메르어" };

export function AnswerReviewSyncPanel({ problemId, onSave, parentBusy }: {
  problemId: string;
  onSave: () => Promise<boolean>;
  parentBusy: boolean;
}) {
  const [languages, setLanguages] = useState<string[]>([]);
  const [chosen, setChosen] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [results, setResults] = useState<AnswerReviewSyncResult[]>([]);

  useEffect(() => {
    let canceled = false;
    listProblems().then(({ problems }) => {
      if (canceled) return;
      const source = problems.find((problem) => problem.problem_id === problemId);
      const targets = Object.keys(source?.equivalent_problem_ids ?? {}).filter((language) => language !== source?.language);
      setLanguages(targets);
      setChosen(targets);
    }).catch((err) => { if (!canceled) setError(String(err)); })
      .finally(() => { if (!canceled) setLoading(false); });
    return () => { canceled = true; };
  }, [problemId]);

  async function apply() {
    if (busy || parentBusy || !chosen.length) return;
    setBusy(true);
    setError("");
    setResults([]);
    try {
      if (!await onSave()) throw new Error("원본 문항 저장·빌드에 실패했습니다.");
      setResults((await syncAnswerReviews(problemId, chosen)).results);
    } catch (err) {
      setError(String(err));
    } finally {
      setBusy(false);
    }
  }

  return <section className="placement-sync-panel answer-review-sync" aria-label="정답 검수 다국어 적용">
    <details>
      <summary>정답 검수를 다국어에 적용</summary>
      <p>응답 방식·정답·검수 상태를 같은 문항의 번역본에 적용합니다. 번역된 선택지와 검수 메모는 유지합니다.</p>
      {loading ? <p role="status">번역 언어를 확인하고 있습니다…</p> : !languages.length ? <p>적용할 번역 문항이 없습니다.</p> : <>
        <fieldset disabled={busy || parentBusy}>
          <legend>대상 언어</legend>
          <label><input type="checkbox" checked={chosen.length === languages.length} onChange={(event) => setChosen(event.target.checked ? languages : [])} />모든 번역 언어</label>
          {languages.map((language) => <label key={language}><input type="checkbox" checked={chosen.includes(language)} onChange={(event) => setChosen((current) => event.target.checked ? [...current, language] : current.filter((item) => item !== language))} />{languageNames[language] ?? language}</label>)}
        </fieldset>
        <p>대상 {chosen.length}개 언어의 기존 검수 설정을 덮어씁니다. 현재 문항의 수정 사항도 저장합니다. 정답 연결이나 번역이 불명확한 언어는 적용하지 않고 알려드립니다.</p>
        <button type="button" disabled={busy || parentBusy || !chosen.length} onClick={() => void apply()}>{busy ? "언어별 저장·빌드 중…" : "정답 검수 다국어에 적용"}</button>
      </>}
      {error && <p role="alert">{error}</p>}
      <div aria-live="polite">{results.map((result) => <div key={result.language} className="placement-sync-result">
        <strong>{languageNames[result.language] ?? result.language}: {result.status === "success" ? "완료" : result.status === "skipped" ? "확인 필요 · 미적용" : result.saved ? "저장됨 · 빌드 실패" : "실패"}</strong>
        {result.error && <p>{result.error}</p>}
      </div>)}</div>
    </details>
  </section>;
}
