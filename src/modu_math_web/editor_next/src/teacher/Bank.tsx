import { useState, type FormEvent } from "react";
import { editorLink, TeacherApi } from "./api";
import { Badge, displayAnswer, Empty, Failure, Field, Loading, Modal, ReadonlyProblem, useLoad } from "./components";
import type { RunAction } from "./forms";
import type { Problem } from "./types";

const api = new TeacherApi();
import { ProblemPublicationSettings, statusLabels as statuses, visibilityLabels } from "./PublicationForm";
const initialFilters = { scope: "", language: "ko", grade: "", unit: "", concept: "", problem_type: "", difficulty: "", status: "" };

export function Bank({ selected, setSelected, createSet, busy, run }: { selected: Problem[]; setSelected: (problems: Problem[]) => void; createSet: () => void; busy: boolean; run: RunAction }) {
  const [draft, setDraft] = useState(initialFilters);
  const [filters, setFilters] = useState(initialFilters);
  const [page, setPage] = useState(1);
  const [revision, refresh] = useState(0);
  const [preview, setPreview] = useState<Problem | null>(null);
  const loaded = useLoad(signal => api.problems(filters, page, signal), [filters, page, revision]);
  const ids = new Set(selected.map(p => p.id));
  const rows = loaded.data?.results ?? [];
  const toggle = (p: Problem) => setSelected(ids.has(p.id) ? selected.filter(item => item.id !== p.id) : [...selected, p]);
  function search(event: FormEvent) { event.preventDefault(); setPage(1); setFilters({ ...draft }); }
  function togglePage() {
    if (rows.filter(p => p.can_use_in_class).every(p => ids.has(p.id))) setSelected(selected.filter(p => !rows.some(row => row.id === p.id)));
    else setSelected([...selected, ...rows.filter(p => p.can_use_in_class && !ids.has(p.id))]);
  }
  return <>
    <div className="page-heading"><div><p className="eyebrow">PROBLEM BANK</p><h1>문제은행</h1><p>수업에 맞는 문제를 고르고, 나만의 문제집을 만드세요.</p></div><a className="button" href="/editor-konva/">문제 편집기 ↗</a></div>
    <div className="bank-scopes" role="group" aria-label="문제 모아보기">{[["", "함께 쓰는 문제은행"], ["mine", "내가 만든 문제"], ["public", "모두에게 공개된 문제"]].map(([key, label]) => <button key={key} className={filters.scope === key ? "primary" : ""} onClick={() => { setDraft({ ...draft, scope: key }); setFilters({ ...filters, scope: key }); setPage(1); }}>{label}</button>)}</div>
    <p className="info-note">공개된 문제는 모든 학생이 풀 수 있어요. 내 문제는 기본적으로 나만 보며, 클래스나 전체 학생에게 공유할 수 있어요.</p>
    <form className="panel bank-filters" onSubmit={search}>
      <Field label="언어"><select value={draft.language} onChange={e => setDraft({ ...draft, language: e.target.value })}><option value="ko">한국어</option><option value="uk">우크라이나어</option><option value="">전체 언어</option></select></Field>
      <Field label="학년"><select value={draft.grade} onChange={e => setDraft({ ...draft, grade: e.target.value })}><option value="">전체 학년</option>{[1, 2, 3, 4, 5, 6].map(g => <option key={g} value={g}>{g}학년</option>)}</select></Field>
      <Field label="단원"><input value={draft.unit} onChange={e => setDraft({ ...draft, unit: e.target.value })} placeholder="예: 덧셈" /></Field>
      <Field label="개념 ID"><input value={draft.concept} onChange={e => setDraft({ ...draft, concept: e.target.value })} placeholder="개념 ID로 검색" /></Field>
      <Field label="문제 유형"><input value={draft.problem_type} onChange={e => setDraft({ ...draft, problem_type: e.target.value })} placeholder="예: choice" /></Field>
      <Field label="난이도"><select value={draft.difficulty} onChange={e => setDraft({ ...draft, difficulty: e.target.value })}><option value="">전체 난이도</option>{[1, 2, 3, 4, 5].map(d => <option key={d} value={d}>{d}단계</option>)}</select></Field>
      <Field label="작업 상태"><select value={draft.status} onChange={e => setDraft({ ...draft, status: e.target.value })}><option value="">전체 상태</option>{Object.entries(statuses).map(([key, label]) => <option key={key} value={key}>{label}</option>)}</select></Field>
      <button className="primary" type="submit">검색</button>
    </form>
    <section className="panel"><div className="section-heading"><h2>문제 목록 <span className="count">{loaded.data?.count ?? "—"}</span></h2><span className="muted">미리보기에서 문제와 정답을 검수할 수 있어요.</span></div>
      {loaded.loading ? <Loading /> : loaded.error ? <Failure message={loaded.error} retry={() => refresh(v => v + 1)} /> : !rows.length ? <Empty>검색 조건에 맞는 문제가 없습니다.</Empty> : <div className="table-wrap"><table><thead><tr><th><input type="checkbox" aria-label="현재 페이지 전체 선택" disabled={!rows.some(p => p.can_use_in_class)} checked={rows.some(p => p.can_use_in_class) && rows.filter(p => p.can_use_in_class).every(p => ids.has(p.id))} onChange={togglePage} /></th><th>문제</th><th>학년 · 단원</th><th>개념</th><th>상태</th><th>난이도</th><th>관리</th></tr></thead><tbody>{rows.map(p => <tr key={p.id} className={ids.has(p.id) ? "selected-row" : ""}><td><input type="checkbox" aria-label={`${p.title} 선택`} disabled={!p.can_use_in_class} checked={ids.has(p.id)} onChange={() => toggle(p)} /></td><td><button className="text-button row-title" onClick={() => setPreview(p)}>{p.title}</button><small className="problem-id">{p.owner_name} / {p.problem_id}</small></td><td>{p.grade ? `${p.grade}학년` : "미분류"}<small>{p.unit}</small></td><td><div className="tags">{p.concepts.map(c => <span key={c}>{c}</span>)}</div></td><td><strong>{visibilityLabels[p.visibility] ?? visibilityLabels.public}</strong><Badge tone={p.publication_status === "published" ? "green" : "neutral"}>{statuses[p.publication_status] ?? "공개"}</Badge></td><td>{p.difficulty ?? 1}단계</td><td><button onClick={() => setPreview(p)}>미리보기</button></td></tr>)}</tbody></table></div>}
      <div className="pagination"><span>{page}페이지</span><button disabled={!loaded.data?.previous || loaded.loading} onClick={() => setPage(p => p - 1)}>이전</button><button disabled={!loaded.data?.next || loaded.loading} onClick={() => setPage(p => p + 1)}>다음</button></div>
    </section>
    <div className="selection-bar"><div><strong>{selected.length}문항 선택</strong><span>선택한 순서로 문제집에 담깁니다.</span></div><button disabled={!selected.length || busy} onClick={() => setSelected([])}>선택 해제</button><button className="primary" disabled={!selected.length || selected.length > 200 || busy} onClick={createSet}>문제집 만들기 →</button></div>
    {selected.length > 200 && <p role="alert" className="form-error">문제집에는 최대 200문항까지 담을 수 있습니다.</p>}
    {preview && <Preview problem={preview} busy={busy} run={run} close={() => setPreview(null)} updated={() => refresh(v => v + 1)} />}
  </>;
}

function Preview({ problem, close, updated, busy, run }: { problem: Problem; close: () => void; updated: () => void; busy: boolean; run: RunAction }) {
  const [revision, refresh] = useState(0);
  const loaded = useLoad(signal => api.problem(problem.id, signal), [problem.id, revision]);
  return <Modal title="문제 미리보기" close={close}>
    {loaded.loading ? <Loading /> : loaded.error ? <Failure message={loaded.error} retry={() => refresh(v => v + 1)} /> : loaded.data && <><h3>{loaded.data.title}</h3><ReadonlyProblem detail={loaded.data} sourceId={new URL(editorLink(problem), window.location.origin).searchParams.get("problem") ?? undefined} />{loaded.data.answer !== undefined && <div className="answer-preview"><strong>교사용 정답</strong><p>{displayAnswer(loaded.data.answer)}</p></div>}</>}
    <p className="muted">작성: {problem.owner_name}</p>
    {problem.source_credit && <p>출처: {problem.source_credit}</p>}
    {loaded.data?.rights_note && <p>이용 조건: {loaded.data.rights_note}</p>}
    {problem.can_edit ? <ProblemPublicationSettings id={problem.id} saved={() => { updated(); close(); }} footer={<a className="button" href={editorLink(problem)}>Konva 편집기에서 열기 ↗</a>} /> : <p className="info-note">{problem.can_use_in_class ? "작성자가 수업 사용을 허용한 문제입니다. 내 문제집에 담아 과제로 배정할 수 있어요." : "학생 풀이용으로 공개된 문제입니다. 다른 선생님의 수업 사용은 허용되지 않았습니다."}</p>}

  </Modal>;
}
