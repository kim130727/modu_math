import { useState, type FormEvent } from "react";
import { TeacherApi } from "./api";
import { Empty, Failure, Field, Loading, Modal, useLoad } from "./components";
import type { Assignment, Classroom, Problem, ProblemSet, Student } from "./types";

export type RunAction = (work: () => Promise<void>) => Promise<void>;
const api = new TeacherApi();

export function ProblemSetForm({ original, selected, busy, run, close, saved }: { original?: ProblemSet; selected: Problem[]; busy: boolean; run: RunAction; close: () => void; saved: (set: ProblemSet, assign: boolean) => void }) {
  const [title, setTitle] = useState(original?.title ?? "");
  const [description, setDescription] = useState(original?.description ?? "");
  const [ids, setIds] = useState<number[]>(original?.items.map(item => item.problem) ?? selected.map(p => p.id));
  const [revision, refresh] = useState(0);
  const loaded = useLoad(signal => original ? api.all<Problem>(`/api/v1/problems/?ids=${original.items.map(i => i.problem).join(",")}`, signal) : Promise.resolve(selected), [original?.id, revision]);
  const names = new Map([...(loaded.data ?? []), ...selected].map(p => [p.id, p.title]));
  const additions = selected.filter(p => !ids.includes(p.id));
  function move(index: number, offset: number) {
    setIds(current => { const next = [...current]; [next[index], next[index + offset]] = [next[index + offset], next[index]]; return next; });
  }
  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const assign = (event.nativeEvent as SubmitEvent).submitter?.getAttribute("data-assign") === "true";
    void run(async () => {
      const body = { title: title.trim(), description, problem_ids: ids };
      const result = original ? await api.patch<ProblemSet>(`/api/v1/problem-sets/${original.id}/`, body) : await api.post<ProblemSet>("/api/v1/problem-sets/", body);
      saved(result, assign);
    });
  }
  return <Modal title={original ? "문제집 수정" : "선택한 문제로 문제집 만들기"} close={close}>
    <form onSubmit={submit}><Field label="문제집 이름"><input required maxLength={160} value={title} onChange={e => setTitle(e.target.value)} placeholder="예: 3학년 받아올림 연습" /></Field>
      <Field label="설명 (선택)"><textarea value={description} onChange={e => setDescription(e.target.value)} rows={2} /></Field>
      <div className="section-heading"><h3>문제 순서</h3><span className="muted">{ids.length}문항</span></div>
      {original && <p className="info-note">문제를 더 담으려면 문제은행에서 선택한 뒤 이 문제집을 수정하세요. <button type="button" disabled={busy || !additions.length || ids.length + additions.length > 200} onClick={() => setIds(current => [...current, ...additions.map(p => p.id)])}>선택한 {additions.length}문항 추가</button></p>}
      {loaded.loading && <Loading />}{loaded.error && <Failure message={loaded.error} retry={() => refresh(v => v + 1)} />}
      {!ids.length && <Empty>문제은행에서 문제를 선택해 주세요.</Empty>}
      <ol className="ordered-problems">{ids.map((id, index) => <li key={`${id}-${index}`}><span className="order-number">{index + 1}</span><span className="grow">{names.get(id) ?? `문제 #${id}`}</span><button type="button" aria-label={`${index + 1}번 문제 위로`} disabled={busy || index === 0} onClick={() => move(index, -1)}>↑</button><button type="button" aria-label={`${index + 1}번 문제 아래로`} disabled={busy || index === ids.length - 1} onClick={() => move(index, 1)}>↓</button><button type="button" aria-label={`${index + 1}번 문제 제거`} disabled={busy} onClick={() => setIds(current => current.filter((_, i) => i !== index))}>제거</button></li>)}</ol>
      {original && <p className="info-note">변경 내용은 다음 배정부터 적용됩니다. 이미 배정한 과제는 그대로 유지됩니다.</p>}
      <footer><button type="button" disabled={busy} onClick={close}>취소</button><button type="submit" disabled={busy || !ids.length}>저장</button><button className="primary" data-assign="true" type="submit" disabled={busy || !ids.length}>저장 후 과제 배정 →</button></footer>
    </form>
  </Modal>;
}

export function AssignmentForm({ initialSet, sets, students, classes, busy, run, close, saved }: { initialSet?: number; sets: ProblemSet[]; students: Student[]; classes: Classroom[]; busy: boolean; run: RunAction; close: () => void; saved: (assignment: Assignment) => void }) {
  const [setId, setSetId] = useState(String(initialSet ?? sets[0]?.id ?? ""));
  const [title, setTitle] = useState(sets.find(s => s.id === initialSet)?.title ?? "");
  const [studentIds, setStudentIds] = useState<number[]>([]);
  const [classIds, setClassIds] = useState<number[]>([]);
  const [starts, setStarts] = useState("");
  const [due, setDue] = useState("");
  const [attempts, setAttempts] = useState(1);
  const [release, setRelease] = useState("after_submission");
  const [error, setError] = useState("");
  const toggle = (ids: number[], id: number) => ids.includes(id) ? ids.filter(i => i !== id) : [...ids, id];
  function submit(event: FormEvent) {
    event.preventDefault();
    setError("");
    if (!studentIds.length && !classIds.length) { setError("배정할 학생이나 학급을 선택해 주세요."); return; }
    if (starts && due && starts >= due) { setError("마감일은 시작일보다 늦어야 합니다."); return; }
    if (release === "after_due" && !due) { setError("마감 후 공개에는 마감일이 필요합니다."); return; }
    void run(async () => {
      const assignment = await api.post<Assignment>("/api/v1/assignments/", {
        title: title.trim(), problem_set: Number(setId), student_ids: studentIds, class_ids: classIds,
        starts_at: starts ? new Date(`${starts}+09:00`).toISOString() : null,
        due_at: due ? new Date(`${due}+09:00`).toISOString() : null,
        max_attempts: attempts, release_policy: release,
      });
      saved(assignment);
    });
  }
  return <Modal title="새 과제 배정" close={close}><form onSubmit={submit}>
    <div className="form-grid"><Field label="문제집"><select required value={setId} onChange={e => setSetId(e.target.value)}><option value="" disabled>문제집 선택</option>{sets.map(s => <option key={s.id} value={s.id}>{s.title} · {s.items.length}문항</option>)}</select></Field><Field label="과제 이름"><input required maxLength={160} value={title} onChange={e => setTitle(e.target.value)} placeholder="학생에게 보여줄 과제 이름" /></Field></div>
    <fieldset><legend>배정할 학생 <span className="muted">{studentIds.length}명 선택</span></legend><div className="choice-list">{students.map(s => <label key={s.id}><input type="checkbox" checked={studentIds.includes(s.id)} onChange={() => setStudentIds(ids => toggle(ids, s.id))} />{s.username}</label>)}{!students.length && <p className="muted">먼저 학생을 등록하거나 학급 가입을 승인해 주세요.</p>}</div></fieldset>
    <fieldset><legend>또는 학급 전체에 배정</legend><div className="choice-list">{classes.filter(c => !c.archived).map(c => <label key={c.id}><input type="checkbox" checked={classIds.includes(c.id)} onChange={() => setClassIds(ids => toggle(ids, c.id))} />{c.name}</label>)}{!classes.some(c => !c.archived) && <p className="muted">등록한 학급이 없습니다.</p>}</div><small>현재 승인된 학생에게 배정됩니다. 중복 선택한 학생은 한 번만 배정됩니다.</small></fieldset>
    <div className="form-grid"><Field label="시작일 (한국 시간)"><input type="datetime-local" value={starts} onChange={e => setStarts(e.target.value)} /></Field><Field label="마감일 (한국 시간)"><input type="datetime-local" value={due} onChange={e => setDue(e.target.value)} required={release === "after_due"} /></Field><Field label="문항별 시도 횟수" hint="첫 풀이를 포함한 횟수입니다."><input type="number" min={1} max={20} required value={attempts} onChange={e => setAttempts(Number(e.target.value))} /></Field><Field label="정답·해설 공개"><select value={release} onChange={e => setRelease(e.target.value)}><option value="after_submission">과제 제출 후</option><option value="immediate">각 문항 풀이 후</option><option value="after_due">마감 후</option><option value="never">공개하지 않음</option></select></Field></div>
    {error && <p role="alert" className="form-error">{error}</p>}
    <footer><button type="button" disabled={busy} onClick={close}>취소</button><button className="primary" disabled={busy || !sets.length} type="submit">{busy ? "배정 중…" : "과제 배정하기"}</button></footer>
  </form></Modal>;
}
