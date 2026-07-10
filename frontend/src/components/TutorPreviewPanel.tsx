import { For, Show, createMemo, createSignal, onMount } from "solid-js";
import { sendTutorPreviewMessage, tutorPreviewStatus } from "../api/editorApi";
import type { EditorStore } from "../stores/editorStore";
import type { TutorPreviewCheck, TutorPreviewMessage, TutorPreviewMode } from "../types/api";

interface TutorPreviewPanelProps {
  store: EditorStore;
}

export function TutorPreviewPanel(props: TutorPreviewPanelProps) {
  const [mode, setMode] = createSignal<TutorPreviewMode>("rule");
  const [input, setInput] = createSignal("");
  const [messages, setMessages] = createSignal<TutorPreviewMessage[]>([]);
  const [checks, setChecks] = createSignal<TutorPreviewCheck[]>([]);
  const [busy, setBusy] = createSignal(false);
  const [error, setError] = createSignal<string | null>(null);
  const [openaiConfigured, setOpenaiConfigured] = createSignal(false);
  const [model, setModel] = createSignal("");

  const payload = createMemo(() => {
    const detail = props.store.state.document?.detail;
    return {
      problem_id: props.store.state.problemId,
      semantic: detail?.semantic ?? null,
      solvable: detail?.solvable ?? null,
      layout: detail?.layout ?? null,
      renderer: detail?.renderer ?? null,
    };
  });

  onMount(async () => {
    try {
      const status = await tutorPreviewStatus();
      setOpenaiConfigured(status.openai_configured);
      setModel(status.model);
    } catch (err) {
      setError(String(err));
    }
  });

  async function sendMessage(text: string, displayText = text): Promise<void> {
    const message = text.trim();
    if (!message || busy()) return;
    setBusy(true);
    setError(null);
    const nextMessages: TutorPreviewMessage[] = [...messages(), { role: "user", content: displayText.trim() }];
    setMessages(nextMessages);
    setInput("");
    try {
      const response = await sendTutorPreviewMessage({
        mode: mode(),
        message,
        history: nextMessages,
        payload: payload(),
      });
      setOpenaiConfigured(response.openai_configured);
      setModel(response.model);
      setChecks(response.checks);
      setMessages([...nextMessages, { role: "assistant", content: response.reply }]);
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
      setMessages(nextMessages);
    } finally {
      setBusy(false);
    }
  }

  function resetChat(): void {
    setMessages([]);
    setChecks([]);
    setError(null);
  }

  return (
    <section class="tutor-preview">
      <div class="tutor-preview-head">
        <div>
          <h2>Rule Tutor</h2>
          <p>{mode() === "rule" ? "solvable JSON 단계 진행" : mode() === "openai" ? `${model() || "OpenAI"} via .env` : "Mock preview"}</p>
        </div>
        <div class="tutor-mode" role="tablist" aria-label="Tutor mode">
          <button type="button" classList={{ active: mode() === "rule" }} onClick={() => setMode("rule")}>
            Rule
          </button>
          <button type="button" classList={{ active: mode() === "mock" }} onClick={() => setMode("mock")}>
            Mock
          </button>
          <button type="button" classList={{ active: mode() === "openai" }} disabled={!openaiConfigured()} onClick={() => setMode("openai")}>
            OpenAI
          </button>
        </div>
      </div>

      <Show when={mode() === "openai" && !openaiConfigured()}>
        <div class="tutor-notice">OPENAI_API_KEY가 .env에 없거나 서버가 아직 읽지 못했습니다.</div>
      </Show>

      <div class="tutor-actions">
        <button type="button" onClick={() => sendMessage("시작", "시작")} disabled={busy()}>
          시작
        </button>
        <button type="button" onClick={() => sendMessage("다음", "다음 단계")} disabled={busy() || messages().length === 0}>
          다음 단계
        </button>
        <button type="button" onClick={() => sendMessage("처음부터", "처음부터")} disabled={busy() || messages().length === 0}>
          처음부터
        </button>
        <button type="button" onClick={resetChat} disabled={busy() || messages().length === 0}>
          초기화
        </button>
      </div>

      <Show when={checks().length > 0}>
        <div class="tutor-checks">
          <For each={checks()}>{(check) => <div class={`tutor-check ${check.level}`}>{check.message}</div>}</For>
        </div>
      </Show>

      <div class="tutor-chat" aria-live="polite">
        <Show when={messages().length > 0} fallback={<div class="tutor-empty">solvable JSON의 steps를 따라 무료 Rule Tutor가 단계별로 진행합니다.</div>}>
          <For each={messages()}>
            {(message) => (
              <div class={`tutor-bubble ${message.role}`}>
                <span>{message.role === "user" ? "Student" : "Tutor"}</span>
                <p>{message.content}</p>
              </div>
            )}
          </For>
        </Show>
      </div>

      <Show when={error()}>
        <div class="tutor-error">{error()}</div>
      </Show>

      <form
        class="tutor-compose"
        onSubmit={(event) => {
          event.preventDefault();
          void sendMessage(input());
        }}
      >
        <textarea value={input()} onInput={(event) => setInput(event.currentTarget.value)} placeholder="학생 답 또는 생각 입력" rows={3} />
        <button type="submit" disabled={busy() || !input().trim()}>
          Send
        </button>
      </form>
    </section>
  );
}
