import { FormEvent, useEffect, useMemo, useState } from "react";
import {
  sendTutorPreviewMessage,
  tutorPreviewStatus,
  type LayoutDocument,
  type RendererDocument,
  type TutorPreviewCheck,
  type TutorPreviewMessage,
  type TutorPreviewMode,
} from "../api/editorApi";
import type { EditorShapeDocument } from "../types/editorShape";

interface TutorPreviewPanelProps {
  problemId: string;
  shapeDocument: EditorShapeDocument;
  semantic: Record<string, unknown> | null;
  solvable: Record<string, unknown> | null;
  layout: LayoutDocument | null;
  renderer: RendererDocument | null;
}

export function TutorPreviewPanel({ problemId, shapeDocument, semantic, solvable, layout, renderer }: TutorPreviewPanelProps) {
  const [mode, setMode] = useState<TutorPreviewMode>("mock");
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<TutorPreviewMessage[]>([]);
  const [checks, setChecks] = useState<TutorPreviewCheck[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [openaiConfigured, setOpenaiConfigured] = useState(false);
  const [model, setModel] = useState("");
  const [voiceEnabled, setVoiceEnabled] = useState(false);

  const payload = useMemo(
    () => ({
      problem_id: problemId,
      semantic,
      solvable,
      layout,
      renderer,
      editor_shape_document: {
        canvas: shapeDocument.canvas,
        shape_count: shapeDocument.shapes.length,
        selected_source: "konva",
      },
    }),
    [layout, problemId, renderer, semantic, shapeDocument.canvas, shapeDocument.shapes.length, solvable],
  );

  useEffect(() => {
    let alive = true;
    tutorPreviewStatus()
      .then((status) => {
        if (!alive) return;
        setOpenaiConfigured(status.openai_configured);
        setModel(status.model);
      })
      .catch((err) => {
        if (alive) setError(String(err));
      });
    return () => {
      alive = false;
    };
  }, []);

  useEffect(() => {
    setMessages([]);
    setChecks([]);
    setError(null);
  }, [problemId]);

  const submitMessage = async (text: string) => {
    const message = text.trim();
    if (!message || busy) return;
    setBusy(true);
    setError(null);
    const nextMessages: TutorPreviewMessage[] = [...messages, { role: "user", content: message }];
    setMessages(nextMessages);
    setInput("");
    try {
      const response = await sendTutorPreviewMessage({
        mode,
        message,
        history: nextMessages,
        payload,
      });
      setOpenaiConfigured(response.openai_configured);
      setModel(response.model);
      setChecks(response.checks);
      setMessages([...nextMessages, { role: "assistant", content: response.reply }]);
      if (voiceEnabled) speakKorean(response.reply);
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setBusy(false);
    }
  };

  const onSubmit = (event: FormEvent) => {
    event.preventDefault();
    void submitMessage(input);
  };

  const latestTutorMessage = [...messages].reverse().find((message) => message.role === "assistant")?.content;

  return (
    <section className="konva-tutor-panel" aria-label="GPT tutor preview">
      <div className="konva-tutor-head">
        <div>
          <div className="panel-title compact">GPT Tutor Preview</div>
          <div className="konva-tutor-subtitle">{mode === "openai" ? `${model || "OpenAI"} 실전 응답` : "Mock 빠른 점검"}</div>
        </div>
        <div className="konva-tutor-controls">
          <div className="konva-tutor-mode" role="tablist" aria-label="Tutor mode">
            <button type="button" className={mode === "mock" ? "active" : ""} onClick={() => setMode("mock")}>
              Mock
            </button>
            <button type="button" className={mode === "openai" ? "active" : ""} disabled={!openaiConfigured} onClick={() => setMode("openai")}>
              OpenAI
            </button>
          </div>
          <button
            type="button"
            className={voiceEnabled ? "konva-tutor-voice active" : "konva-tutor-voice"}
            onClick={() => {
              const next = !voiceEnabled;
              setVoiceEnabled(next);
              if (!next) window.speechSynthesis?.cancel();
            }}
          >
            음성
          </button>
        </div>
      </div>

      <div className="konva-tutor-actions">
        <button type="button" onClick={() => void submitMessage("힌트 주세요")} disabled={busy}>
          힌트
        </button>
        <button type="button" onClick={() => void submitMessage("모르겠어요")} disabled={busy}>
          모르겠어요
        </button>
        <button type="button" onClick={() => void submitMessage("왜 그렇게 돼요?")} disabled={busy}>
          이유
        </button>
        <button
          type="button"
          onClick={() => {
            setMessages([]);
            setChecks([]);
            setError(null);
          }}
          disabled={busy || messages.length === 0}
        >
          초기화
        </button>
      </div>

      <div className="konva-tutor-chat" aria-live="polite">
        {messages.length === 0 ? (
          <div className="konva-tutor-empty">Mock은 API 없이 구조를 빠르게 확인하고, OpenAI는 실제 GPT 응답을 확인합니다.</div>
        ) : (
          messages.map((message, index) => (
            <div className={`konva-tutor-bubble ${message.role}`} key={`${message.role}-${index}`}>
              <strong>{message.role === "user" ? "Student" : "Tutor"}</strong>
              <span>{message.content}</span>
            </div>
          ))
        )}
      </div>

      <div className="konva-tutor-side">
        {latestTutorMessage ? (
          <button type="button" className="konva-tutor-read" onClick={() => speakKorean(latestTutorMessage)}>
            답변 읽기
          </button>
        ) : null}
        {!openaiConfigured ? <div className="konva-tutor-notice">OPENAI_API_KEY가 .env에서 확인되지 않았습니다.</div> : null}
        {checks.length ? (
          <div className="konva-tutor-checks">
            {checks.map((check, index) => (
              <div className={`konva-tutor-check ${check.level}`} key={`${check.level}-${index}`}>
                {check.message}
              </div>
            ))}
          </div>
        ) : null}
        {error ? <div className="konva-tutor-error">{error}</div> : null}
      </div>

      <form className="konva-tutor-compose" onSubmit={onSubmit}>
        <input value={input} onChange={(event) => setInput(event.target.value)} placeholder="학생 답변 입력" />
        <button type="submit" disabled={busy || !input.trim()}>
          Send
        </button>
      </form>
    </section>
  );
}

function speakKorean(text: string): void {
  if (!("speechSynthesis" in window)) return;
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "ko-KR";
  utterance.rate = 1;
  window.speechSynthesis.speak(utterance);
}
