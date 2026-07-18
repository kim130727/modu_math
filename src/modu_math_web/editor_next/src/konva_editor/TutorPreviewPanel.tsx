import { FormEvent, useEffect, useMemo, useRef, useState, type MutableRefObject } from "react";
import {
  sendTutorPreviewMessage,
  synthesizeTutorSpeech,
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
  tutorFrameIndex?: number;
  tutorFrameCount?: number;
  saveStatus: "saved" | "saving" | "unsaved" | "building" | "built" | "error";
  message: string;
  onTutorFrameChange?: (frameIndex: number) => void;
  onTutorStepChange?: (stepId: string | null) => void;
}

export function TutorPreviewPanel({
  problemId,
  shapeDocument,
  semantic,
  solvable,
  layout,
  renderer,
  tutorFrameIndex = 0,
  tutorFrameCount = 0,
  saveStatus,
  message,
  onTutorFrameChange,
  onTutorStepChange,
}: TutorPreviewPanelProps) {
  const [mode, setMode] = useState<TutorPreviewMode>("rule");
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<TutorPreviewMessage[]>([]);
  const [choices, setChoices] = useState<string[]>([]);
  const [checks, setChecks] = useState<TutorPreviewCheck[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [openaiConfigured, setOpenaiConfigured] = useState(false);
  const [model, setModel] = useState("");
  const [voiceEnabled, setVoiceEnabled] = useState(false);
  const tutorLanguage = useMemo(() => problemLanguage(semantic), [semantic]);
  const tutorLocale = useMemo(() => languageToSpeechLocale(tutorLanguage), [tutorLanguage]);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const payload = useMemo(
    () => ({
      problem_id: problemId,
      language: tutorLanguage,
      locale: tutorLocale,
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
    [layout, problemId, renderer, semantic, shapeDocument.canvas, shapeDocument.shapes.length, solvable, tutorLanguage, tutorLocale],
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
    setChoices([]);
    setChecks([]);
    setError(null);
    onTutorStepChange?.(null);
    stopTutorSpeech(audioRef);
  }, [onTutorStepChange, problemId]);

  useEffect(() => () => stopTutorSpeech(audioRef), []);

  const submitMessage = async (text: string, displayText = text) => {
    const message = text.trim();
    if (!message || busy) return;
    setBusy(true);
    setError(null);
    setChoices([]);
    const nextMessages: TutorPreviewMessage[] = [...messages, { role: "user", content: displayText.trim() }];
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
      setChoices(response.choices ?? []);
      onTutorStepChange?.(response.current_step_id ?? null);
      const reply = formatTutorText(response.reply);
      setMessages([...nextMessages, { role: "assistant", content: reply }]);
      if (voiceEnabled) void playTutorSpeech(reply, tutorLocale, payload, setError, audioRef);
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
    <section className="konva-tutor-panel" aria-label="Rule tutor preview">
      <div className="konva-tutor-head">
        <div>
          <div className="panel-title compact konva-panel-title-with-status">
            <span>Rule Tutor Preview</span>
            <span className={`konva-save-status ${saveStatus}`} aria-live="polite">
              {statusLabel(saveStatus)}
            </span>
          </div>
          <div className="konva-tutor-subtitle">
            {mode === "rule" ? "solvable JSON 기반 선택형 진행" : mode === "openai" ? `${model || "OpenAI"} 실전 응답` : "Mock 빠른 점검"}
          </div>
        </div>
        <div className="konva-tutor-controls">
          <div className="konva-tutor-mode" role="tablist" aria-label="Tutor mode">
            <button type="button" className={mode === "rule" ? "active" : ""} onClick={() => setMode("rule")}>
              Rule
            </button>
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
              if (!next) stopTutorSpeech(audioRef);
            }}
          >
            음성
          </button>
        </div>
      </div>

      <div className={saveStatus === "error" ? "problem-list-error" : "panel-message"} aria-live="polite">
        {message}
      </div>

      <div className="konva-tutor-actions">
        <button type="button" onClick={() => void submitMessage("시작", "시작")} disabled={busy}>
          시작
        </button>
        <button type="button" onClick={() => void submitMessage("다음", "다음 단계")} disabled={busy || messages.length === 0}>
          다음 단계
        </button>
        <button type="button" onClick={() => void submitMessage("처음부터", "처음부터")} disabled={busy || messages.length === 0}>
          처음부터
        </button>
        <button
          type="button"
          onClick={() => {
            setMessages([]);
            setChoices([]);
            setChecks([]);
            setError(null);
            onTutorStepChange?.(null);
          }}
          disabled={busy || messages.length === 0}
        >
          초기화
        </button>
      </div>

      {tutorFrameCount > 1 ? (
        <div className="konva-tutor-frames" aria-label="Tutor visual frames">
          <button
            type="button"
            onClick={() => onTutorFrameChange?.(Math.max(0, tutorFrameIndex - 1))}
            disabled={tutorFrameIndex <= 0}
          >
            화면 이전
          </button>
          <span>
            화면 {tutorFrameIndex + 1}/{tutorFrameCount}
          </span>
          <button
            type="button"
            onClick={() => onTutorFrameChange?.(Math.min(tutorFrameCount - 1, tutorFrameIndex + 1))}
            disabled={tutorFrameIndex >= tutorFrameCount - 1}
          >
            화면 다음
          </button>
        </div>
      ) : null}

      <div className="konva-tutor-chat" aria-live="polite">
        {messages.length === 0 ? (
          <div className="konva-tutor-empty">solvable JSON을 바탕으로 단계별 선택지를 자동 생성합니다.</div>
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
          <button type="button" className="konva-tutor-read" onClick={() => void playTutorSpeech(latestTutorMessage, tutorLocale, payload, setError, audioRef)}>
            듣기
          </button>
        ) : null}
        {choices.length ? (
          <div className="konva-tutor-choices" aria-label="Tutor choices">
            {choices.map((choice, index) => (
              <button type="button" key={`${choice}-${index}`} onClick={() => void submitMessage(choice, choice)} disabled={busy}>
                <span>{index + 1}</span>
                {choice}
              </button>
            ))}
          </div>
        ) : null}
        {mode === "openai" && !openaiConfigured ? <div className="konva-tutor-notice">OPENAI_API_KEY가 .env에서 확인되지 않았습니다.</div> : null}
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
        <input value={input} onChange={(event) => setInput(event.target.value)} placeholder="직접 입력하거나 선택지를 클릭하세요" />
        <button type="submit" disabled={busy || !input.trim()}>
          Send
        </button>
      </form>
    </section>
  );
}

async function playTutorSpeech(
  text: string,
  locale: string,
  payload: Record<string, unknown>,
  setError: (message: string | null) => void,
  audioRef: MutableRefObject<HTMLAudioElement | null>,
): Promise<void> {
  stopTutorSpeech(audioRef);
  try {
    const audioBlob = await synthesizeTutorSpeech({ text, locale, payload });
    const url = URL.createObjectURL(audioBlob);
    const audio = new Audio(url);
    audio.dataset.objectUrl = url;
    audioRef.current = audio;
    audio.onended = () => URL.revokeObjectURL(url);
    audio.onerror = () => {
      URL.revokeObjectURL(url);
      setError("서버 TTS 오디오를 재생하지 못했습니다.");
    };
    await audio.play();
  } catch (err) {
    setError(`서버 TTS 실패: ${err instanceof Error ? err.message : String(err)}`);
  }
}

function stopTutorSpeech(audioRef: MutableRefObject<HTMLAudioElement | null>): void {
  if (audioRef.current) {
    const objectUrl = audioRef.current.dataset.objectUrl;
    audioRef.current.pause();
    audioRef.current.currentTime = 0;
    if (objectUrl) URL.revokeObjectURL(objectUrl);
    audioRef.current = null;
  }
  if (!("speechSynthesis" in window)) return;
  window.speechSynthesis.cancel();
}

function problemLanguage(semantic: Record<string, unknown> | null): string {
  const metadata = recordValue(semantic?.metadata);
  const raw = stringValue(metadata?.language) ?? stringValue(metadata?.locale) ?? stringValue(semantic?.language) ?? stringValue(semantic?.locale);
  const value = (raw ?? "ko").trim().toLowerCase().replace("_", "-");
  if (["ko", "kr", "ko-kr", "korean"].includes(value)) return "ko";
  if (["en", "en-us", "en-gb", "english"].includes(value)) return "en";
  if (["ja", "jp", "ja-jp", "japanese"].includes(value)) return "ja";
  if (["zh", "zh-cn", "zh-hans", "ch", "cn", "chinese"].includes(value)) return "zh";
  if (["km", "kh", "km-kh", "khmer", "cambodian", "cam"].includes(value)) return "km";
  if (["my", "my-mm", "burmese", "myanmar"].includes(value)) return "my";
  return value.split("-", 1)[0] || "ko";
}

function languageToSpeechLocale(language: string): string {
  return {
    ko: "ko-KR",
    en: "en-US",
    ja: "ja-JP",
    zh: "zh-CN",
    km: "km-KH",
    my: "my-MM",
  }[language] ?? language;
}

function recordValue(value: unknown): Record<string, unknown> | null {
  return typeof value === "object" && value !== null && !Array.isArray(value) ? (value as Record<string, unknown>) : null;
}

function stringValue(value: unknown): string | null {
  return typeof value === "string" && value.trim() ? value : null;
}

function formatTutorText(text: string): string {
  return text
    .replaceAll("**", "")
    .replaceAll("__", "")
    .replaceAll("`", "")
    .split("\n")
    .map((line) => line.replace(/^\s*[-*]\s*/, "").trim())
    .filter(Boolean)
    .slice(0, 4)
    .join("\n");
}

function statusLabel(saveStatus: TutorPreviewPanelProps["saveStatus"]): string {
  if (saveStatus === "saving") return "Saving...";
  if (saveStatus === "unsaved") return "Unsaved";
  if (saveStatus === "building") return "Building...";
  if (saveStatus === "built") return "Build complete";
  if (saveStatus === "error") return "Error";
  return "Saved";
}
