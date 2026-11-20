import { useEffect, useRef, useState } from "react";
import { loadProblem, type ProblemDetailResponse } from "../api/editorApi";
import { FlutterEditorSurface } from "./FlutterEditorSurface";

export function FlutterStudentPreview({ problemId, onClose }: { problemId: string; onClose: () => void }) {
  const dialogRef = useRef<HTMLDialogElement>(null);
  const [problem, setProblem] = useState<ProblemDetailResponse | null>(null);
  const [error, setError] = useState("");
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    dialogRef.current?.showModal();
  }, []);

  useEffect(() => {
    let cancelled = false;
    setProblem(null);
    setError("");
    void loadProblem(problemId).then(detail => {
      if (!detail.renderer || !detail.semantic || !detail.solvable) {
        throw new Error("문제를 저장하고 화면 반영한 뒤 다시 열어주세요.");
      }
      if (!cancelled) setProblem(detail);
    }).catch(reason => {
      if (!cancelled) setError(`저장된 문제를 불러오지 못했습니다. ${String(reason)}`);
    });
    return () => { cancelled = true; };
  }, [problemId, attempt]);

  return (
    <dialog ref={dialogRef} className="flutter-student-preview" aria-labelledby="student-preview-title" onCancel={onClose}>
      <header className="student-preview-header">
        <div><strong id="student-preview-title">앱처럼 풀어보기</strong><p>마지막으로 저장하고 화면 반영한 문제입니다. 풀이 기록은 저장하지 않습니다.</p></div>
        <button type="button" autoFocus onClick={onClose}>편집으로 돌아가기</button>
      </header>
      {error ? <div className="student-preview-message" role="alert"><p>{error}</p><button type="button" onClick={() => setAttempt(value => value + 1)}>다시 시도</button></div>
        : problem ? <FlutterEditorSurface key={attempt} problemId={problemId} renderer={null} savedProblem={problem} mode="studentTest" onModeChange={() => {}} onSelectTarget={() => {}} onLayoutPatch={() => {}} />
          : <p className="student-preview-message" role="status">저장된 문제를 불러오는 중…</p>}
    </dialog>
  );
}
