import { useState } from "react";
import { TeacherApi } from "./api";
import { Field, Failure, Loading, useLoad } from "./components";
import type { Classroom } from "./types";

export interface Publication {
  status: string; visibility: string; difficulty: number; classroom_ids: number[];
  allow_classroom_use: boolean; source_credit: string; rights_note: string; rights_confirmed: boolean;
}
export const visibilityLabels: Record<string, string> = { private: "나만 보기", class: "선택한 클래스", public: "모두에게 공개" };
export const statusLabels: Record<string, string> = { draft: "초안", review: "검수 중", published: "사용 가능", archived: "보관" };
const api = new TeacherApi();

export function PublicationForm({ value, save, busy, footer }: { value: Publication; save: (value: Publication) => Promise<void>; busy?: boolean; footer?: React.ReactNode }) {
  const [draft, setDraft] = useState(value);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const classes = useLoad(signal => api.all<Classroom>("/api/v1/classes/", signal), []);
  const disabled = busy || saving;
  const descriptions: Record<string, string> = {
    private: "다른 선생님과 학생에게 보이지 않아요. 내 학생에게 과제로 배정할 수 있어요.",
    class: "선택한 클래스에서 가입이 승인된 학생만 자유롭게 풀 수 있어요.",
    public: "클래스 가입 없이 모든 학생이 문제를 찾아 풀 수 있어요. 작성자 이름과 출처가 함께 표시돼요.",
  };
  return <form className="publication-form" onSubmit={async e => { e.preventDefault(); if (disabled) return; setSaving(true); setError(""); try { await save({ ...draft, classroom_ids: draft.visibility === "class" ? draft.classroom_ids : [], allow_classroom_use: draft.visibility === "public" && draft.allow_classroom_use }); } catch (err) { setError(err instanceof Error ? err.message : "저장하지 못했습니다."); } finally { setSaving(false); } }}>
    <h3>누구에게 보여줄까요?</h3>
    <div className="visibility-options" role="radiogroup" aria-label="공개 범위">{Object.entries(visibilityLabels).map(([key, label]) => <label key={key} className={draft.visibility === key ? "active" : ""}><input type="radio" name="visibility" value={key} checked={draft.visibility === key} disabled={disabled} onChange={() => setDraft({ ...draft, visibility: key })} /><strong>{label}</strong><span>{descriptions[key]}</span></label>)}</div>
    {draft.visibility === "class" && <fieldset disabled={disabled}><legend>공유할 클래스</legend>{classes.loading ? <Loading /> : classes.error ? <p role="alert">{classes.error}</p> : !classes.data?.some(c => !c.archived) ? <p>먼저 <a href="/teacher/#classes">클래스를 만들어 주세요 →</a></p> : classes.data.filter(c => !c.archived).map(c => <label className="sharing-check" key={c.id}><input type="checkbox" checked={draft.classroom_ids.includes(c.id)} onChange={e => setDraft({ ...draft, classroom_ids: e.target.checked ? [...draft.classroom_ids, c.id] : draft.classroom_ids.filter(id => id !== c.id) })} />{c.name}</label>)}</fieldset>}
    <div className="form-grid"><Field label="작업 상태" hint="학생에게 보이려면 ‘사용 가능’으로 설정하세요."><select disabled={disabled} value={draft.status} onChange={e => setDraft({ ...draft, status: e.target.value })}>{Object.entries(statusLabels).map(([key, label]) => <option key={key} value={key}>{label}</option>)}</select></Field><Field label="난이도"><select disabled={disabled} value={draft.difficulty} onChange={e => setDraft({ ...draft, difficulty: Number(e.target.value) })}>{[1, 2, 3, 4, 5].map(n => <option key={n} value={n}>{n}단계</option>)}</select></Field></div>
    {draft.visibility === "public" && <label className="sharing-check"><input type="checkbox" disabled={disabled} checked={draft.allow_classroom_use} onChange={e => setDraft({ ...draft, allow_classroom_use: e.target.checked })} />다른 선생님이 이 문제를 문제집과 과제에 사용하도록 허용합니다.</label>}
    <Field label="출처 · 권리자" hint="문제를 보는 학생과 선생님에게 함께 표시됩니다."><input maxLength={500} disabled={disabled} value={draft.source_credit} onChange={e => setDraft({ ...draft, source_credit: e.target.value })} placeholder="예: 직접 제작 / 홍길동 선생님" /></Field>
    <Field label="이용 조건"><textarea maxLength={1000} disabled={disabled} value={draft.rights_note} onChange={e => setDraft({ ...draft, rights_note: e.target.value })} placeholder="예: 수업에서 사용 가능, 출처 표시 필요" /></Field>
    {draft.visibility !== "private" && <label className="sharing-check"><input type="checkbox" required disabled={disabled} checked={draft.rights_confirmed} onChange={e => setDraft({ ...draft, rights_confirmed: e.target.checked })} />직접 만든 문제이거나 선택한 범위로 공유할 권한이 있습니다.</label>}
    <p className="info-note">공개 범위를 줄이면 새로운 조회와 사용이 제한됩니다. 이미 배정한 과제와 학생의 학습 기록은 유지됩니다.</p>
    {error && <p role="alert" className="form-error">{error}</p>}
    <footer>{footer}<button className="primary" disabled={disabled || (draft.visibility === "class" && (classes.loading || !!classes.error || !draft.classroom_ids.length))}>{saving ? "저장 중…" : "공개 설정 저장"}</button></footer>
  </form>;
}

export function ProblemPublicationSettings({ id, saved, footer }: { id: number; saved: () => void; footer?: React.ReactNode }) {
  const loaded = useLoad(signal => api.get<Publication>(`/api/v1/problems/${id}/publication/`, signal), [id]);
  return loaded.loading ? <Loading /> : loaded.error ? <Failure message={loaded.error} retry={saved} /> : loaded.data && <PublicationForm value={loaded.data} footer={footer} save={async value => { await api.patch(`/api/v1/problems/${id}/publication/`, value); saved(); }} />;
}
