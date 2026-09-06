import { useEffect, useState, type ComponentProps } from "react";
import type { TutorRendererStep, TutorRendererOverlay } from "../api/editorApi";
import { LegacyTutorFlowPanel } from "./LegacyTutorFlowPanel";

export function TutorFlowPanel(props: ComponentProps<typeof LegacyTutorFlowPanel>) {
  const { tutorFlow, activeStepId, onSelectFrame, onDraftChange } = props;
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);
  const hints = tutorFlow.filter(step => step.phase === "hint");
  const index = hints.findIndex(step => step.step_id === activeStepId);
  const active = hints[index];
  const frames = active?.frames?.length ? active.frames : [{ id: `${activeStepId}.frame.1`, overlays: active?.overlays ?? [] }];
  const frameIndex = Math.min(props.activeFrameIndex, frames.length - 1);
  const overlays = frames[frameIndex].overlays;
  useEffect(() => {
    if (hints.length && !hints.some(step => step.step_id === activeStepId)) onSelectFrame(hints[0].step_id, 0);
  }, [tutorFlow, activeStepId, onSelectFrame]);
  const update = (patch: Partial<TutorRendererStep>) => onDraftChange(tutorFlow.map(step => step.step_id === activeStepId ? { ...step, ...patch } : step));
  const setOverlays = (next: TutorRendererOverlay[]) => update({ frames: frames.map((frame, i) => i === frameIndex ? { ...frame, overlays: next } : frame) });
  const add = () => {
    const id = `hint.${crypto.randomUUID()}`;
    onDraftChange([...tutorFlow, { step_id: id, phase: "hint", title: "", text: "", frames: [{ id: `${id}.frame.1`, overlays: [] }] }]);
    onSelectFrame(id, 0);
  };
  const move = (delta: number) => {
    const other = hints[index + delta];
    if (!active || !other) return;
    const next = [...tutorFlow], a = next.indexOf(active), b = next.indexOf(other);
    [next[a], next[b]] = [next[b], next[a]];
    onDraftChange(next);
  };
  const save = async () => {
    if (hints.some(hint => !hint.text?.trim())) { setError("모든 힌트의 내용을 입력해 주세요."); return; }
    setSaving(true); setError("");
    try { await props.onSave(tutorFlow); } catch (error) { setError(String(error)); } finally { setSaving(false); }
  };
  return <section className="konva-hint-panel">
    <div className="panel-title">힌트 편집</div>
    <div className="konva-hint-content">
      <p>학생이 막혔을 때 볼 설명을 순서대로 작성하세요.</p>
      <fieldset disabled={saving}>
      <div className="konva-placement-buttons">
        <button type="button" onClick={add}>+ 힌트 추가</button>
        <button type="button" onClick={save}>{saving ? "저장 중…" : "힌트 저장 · 빌드"}</button>
      </div>
      {!hints.length ? <p>‘힌트 추가’로 시작하세요. 작성 전에는 앱의 기존 힌트를 사용합니다.</p> : null}
      <div className="konva-hint-list">
        {hints.map((hint, i) => <button type="button" key={hint.step_id} aria-pressed={hint === active} onClick={() => onSelectFrame(hint.step_id, 0)}>힌트 {i + 1} · {hint.title || hint.text?.slice(0, 24) || "내용 입력"}</button>)}
      </div>
      {active ? <>
        <div className="konva-placement-buttons">
          <button type="button" disabled={index <= 0} onClick={() => move(-1)}>위로</button>
          <button type="button" disabled={index === hints.length - 1} onClick={() => move(1)}>아래로</button>
          <button type="button" onClick={() => { onDraftChange(tutorFlow.filter(step => step !== active)); props.onSelectOverlay(null); }}>이 힌트 삭제</button>
        </div>
        <label>제목 (선택)<input value={active.title ?? ""} placeholder={`힌트 ${index + 1}`} onChange={e => update({ title: e.target.value })} /></label>
        <label>학생에게 보여줄 내용<textarea rows={5} value={active.text ?? ""} placeholder="어디부터 살펴보면 좋을까요?" onChange={e => update({ text: e.target.value })} /></label>
        <div className="konva-placement-buttons">
          <button type="button" disabled={!props.selectedShapeIds.length} onClick={() => setOverlays([...overlays, ...props.selectedShapeIds.filter(id => !overlays.some(o => o.type === "highlight" && o.target_ref === id)).map(id => ({ type: "highlight", target_ref: id }))])}>선택한 그림 강조</button>
          <button type="button" onClick={() => setOverlays([...overlays, { type: "label", text: "보충 설명", x: 40, y: 40, style: { fill: "#0f766e", font_size: 24 } }])}>그림에 설명 추가</button>
        </div>
        <p>왼쪽 그림에서 요소를 선택해 강조하세요. 설명은 그림에서 끌어 위치를 바꿀 수 있습니다.</p>
        {overlays.map((overlay, i) => <div className="konva-hint-overlay" key={i}>
          {overlay.type === "label" ? <input aria-label={`그림 설명 ${i + 1}`} value={overlay.text ?? ""} onFocus={() => props.onSelectOverlay(i)} onChange={e => setOverlays(overlays.map((o, j) => i === j ? { ...o, text: e.target.value } : o))} /> : <span>강조: {overlay.target_ref ?? overlay.type}</span>}
          <button type="button" onClick={() => { setOverlays(overlays.filter((_, j) => j !== i)); props.onSelectOverlay(null); }}>삭제</button>
        </div>)}
        <div className="konva-hint-preview"><strong>{active.title || `힌트 ${index + 1}`}</strong><p>{active.text || "작성한 문장이 여기에 표시됩니다."}</p><small>왼쪽 그림에서 이 힌트의 강조 표시를 확인하세요.</small></div>
        <details><summary>고급 설정 · 장면</summary>
          <select aria-label="힌트 장면" value={frameIndex} onChange={e => onSelectFrame(active.step_id, Number(e.target.value))}>{frames.map((f, i) => <option key={f.id} value={i}>장면 {i + 1}</option>)}</select>
          <pre>{JSON.stringify(active, null, 2)}</pre>
        </details>
      </> : null}
      </fieldset>
      {error ? <p role="alert">{error}</p> : null}
      <p role="status">{props.message}</p>
      <details><summary>기존 단계 데이터</summary><pre>{JSON.stringify(tutorFlow.filter(step => step.phase !== "hint"), null, 2)}</pre></details>
    </div>
  </section>;
}
