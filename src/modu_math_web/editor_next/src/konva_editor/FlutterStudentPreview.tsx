import { useEffect, useRef, useState } from "react";
import { checkStudentPreview, loadStudentPreview } from "../api/editorApi";

type PreviewViewport = "full" | "tablet" | "mobile";

export function FlutterStudentPreview({ problemId, onClose }: { problemId: string; onClose: () => void }) {
  const frameRef = useRef<HTMLIFrameElement>(null);
  const [problem, setProblem] = useState<Record<string, unknown> | null>(null);
  const [loadingProblem, setLoadingProblem] = useState(true);
  const [ready, setReady] = useState(false);
  const [error, setError] = useState("");
  const [attempt, setAttempt] = useState(0);
  const [viewport, setViewport] = useState<PreviewViewport>("full");

  useEffect(() => {
    let cancelled = false;
    setLoadingProblem(true);
    setError("");
    void loadStudentPreview(problemId).then(detail => {
      if (!cancelled) {
        setProblem(detail);
        setLoadingProblem(false);
      }
    }).catch(reason => {
      if (!cancelled) {
        setProblem(null);
        setLoadingProblem(false);
        setError(`저장된 문제를 불러오지 못했습니다. ${String(reason)}`);
      }
    });
    return () => { cancelled = true; };
  }, [problemId, attempt]);

  useEffect(() => {
    setReady(false);
  }, [attempt]);

  useEffect(() => {
    let active = true;
    const post = (message: Record<string, unknown>) => frameRef.current?.contentWindow?.postMessage(message, window.location.origin);
    const receive = (event: MessageEvent) => {
      if (event.origin !== window.location.origin || event.source !== frameRef.current?.contentWindow || !event.data) return;
      if (event.data.type === "modu-math:student-ready") setReady(true);
      if (event.data.type === "modu-math:student-submit" && problem && event.data.revision === problem.revision) {
        void checkStudentPreview(problemId, event.data.answer, String(problem.revision)).then(result => {
          if (active) post({ type: "modu-math:student-result", correct: result.correct });
        }).catch(reason => {
          if (active) post({ type: "modu-math:student-error", error: String(reason) });
        });
      }
    };
    window.addEventListener("message", receive);
    return () => { active = false; window.removeEventListener("message", receive); };
  }, [problem, problemId]);

  useEffect(() => {
    if (ready && problem) frameRef.current?.contentWindow?.postMessage({ type: "modu-math:student-content", content: problem }, window.location.origin);
  }, [ready, problem]);

  useEffect(() => {
    if (!problem || ready) return;
    const timer = window.setTimeout(() => setError("학생 앱을 불러오지 못했습니다. 다시 시도해주세요."), 30000);
    return () => window.clearTimeout(timer);
  }, [problem, ready]);

  const version = document.querySelector<HTMLElement>("#root")?.dataset.studentAppVersion ?? "dev";

  return (
    <section className="flutter-student-preview" aria-labelledby="student-preview-title">
      <header className="student-preview-header">
        <div className="student-preview-heading">
          <strong id="student-preview-title">앱처럼 풀어보기</strong>
          <p>마지막으로 저장하고 화면 반영한 문제입니다. 풀이 기록은 저장하지 않습니다.</p>
        </div>
        <div className="student-preview-actions">
          <div className="student-preview-viewport" role="group" aria-label="미리보기 화면 크기">
            {([["full", "전체"], ["tablet", "태블릿"], ["mobile", "모바일"]] as const).map(([key, label]) => (
              <button
                key={key}
                type="button"
                aria-pressed={viewport === key}
                onClick={() => setViewport(key)}
              >
                {label}
              </button>
            ))}
          </div>
          <button type="button" onClick={() => setAttempt(value => value + 1)}>새로고침</button>
          <button type="button" onClick={onClose}>편집으로 돌아가기</button>
        </div>
      </header>
      {error ? (
        <div className="student-preview-message" role="alert">
          <p>{error}</p>
          <button type="button" onClick={() => setAttempt(value => value + 1)}>다시 시도</button>
        </div>
      ) : (
        <section className={`flutter-editor-surface viewport-${viewport}`} aria-label="학생 앱 문제풀이 화면">
          {!ready || loadingProblem ? (
            <div className="flutter-editor-loading" role="status">
              {loadingProblem && !ready ? "저장된 문제를 불러오는 중…" : !ready ? "학생 앱을 불러오는 중…" : "문제를 전환하는 중…"}
            </div>
          ) : null}
          {problem || ready ? (
            <iframe
              ref={frameRef}
              key={attempt}
              className="flutter-editor-frame"
              title="학생 앱 문제풀이"
              src={`/static/editor_next/student_app/index.html?studentPreview=1&v=${encodeURIComponent(version)}`}
            />
          ) : null}
        </section>
      )}
    </section>
  );
}
