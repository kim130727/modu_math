import { useState } from "react";
import { TeacherApi } from "./api";
import { Badge, Empty, Failure, Field, Loading, Modal, useLoad } from "./components";
import type { RunAction } from "./forms";
import type { Classroom, Enrollment, Student, User } from "./types";

const api = new TeacherApi();

export function Students({ students, user, busy, run, refresh }: { students: Student[]; user: User; busy: boolean; run: RunAction; refresh: () => void }) {
  const [creating, setCreating] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  return <>
    <div className="page-heading"><div><p className="eyebrow">STUDENTS</p><h1>학생 관리</h1><p>담당 학생을 등록하고, 학급에서 함께 학습하세요.</p></div><button className="primary" onClick={() => setCreating(true)}>+ 학생 등록</button></div>
    <section className="panel"><div className="section-heading"><h2>담당 학생 <span className="count">{students.length}</span></h2><span className="muted">등록한 학생과 가입을 승인한 학생이 표시됩니다.</span></div>{students.length ? <div className="table-wrap"><table><thead><tr><th>학생 아이디</th><th>학생 번호</th><th>계정 안내</th></tr></thead><tbody>{students.map((s, i) => <tr key={s.id}><td><span className={`student-avatar color-${i % 4}`}>{s.username.slice(0, 1).toUpperCase()}</span><strong>{s.username}</strong></td><td>#{s.id}</td><td className="muted">본인의 과제와 학습 기록만 볼 수 있습니다.</td></tr>)}</tbody></table></div> : <Empty>학생을 등록하거나 학급 초대 코드를 전달해 주세요.</Empty>}</section>
    {user.role === "admin" && <UserAccess busy={busy} run={run} user={user} />}
    {creating && <Modal title="학생 계정 등록" close={() => { if (!busy) setCreating(false); }}><form onSubmit={e => { e.preventDefault(); void run(async () => { await api.post("/api/v1/students/", { username: username.trim(), password }); setUsername(""); setPassword(""); setCreating(false); refresh(); }); }}><p className="info-note">생년월일이나 연락처 없이 학생 아이디와 비밀번호만으로 등록합니다.</p><Field label="학생 아이디"><input required maxLength={150} autoComplete="off" value={username} onChange={e => setUsername(e.target.value)} /></Field><Field label="초기 비밀번호" hint="8자 이상으로 입력하고 학생에게 직접 전달해 주세요."><input type="password" required minLength={8} maxLength={128} autoComplete="new-password" value={password} onChange={e => setPassword(e.target.value)} /></Field><footer><button type="button" disabled={busy} onClick={() => setCreating(false)}>취소</button><button className="primary" disabled={busy}>학생 등록하기</button></footer></form></Modal>}
  </>;
}

function UserAccess({ busy, run, user }: { busy: boolean; run: RunAction; user: User }) {
  const [revision, refresh] = useState(0);
  const loaded = useLoad(signal => api.all<User>("/api/v1/admin/users/", signal), [revision]);
  return <section className="panel"><div className="section-heading"><h2>전체 사용자 및 권한</h2><Badge>관리자 전용</Badge></div>{loaded.loading ? <Loading /> : loaded.error ? <Failure message={loaded.error} retry={() => refresh(v => v + 1)} /> : <div className="table-wrap"><table><thead><tr><th>아이디</th><th>역할</th><th>계정 상태</th><th>관리</th></tr></thead><tbody>{loaded.data?.map(u => <tr key={u.id}><td>{u.username}</td><td><select aria-label={`${u.username} 역할`} value={u.role} disabled={busy || u.id === user.id} onChange={e => { const role = e.target.value; void run(async () => { await api.patch(`/api/v1/admin/users/${u.id}/`, { role }); refresh(v => v + 1); }); }}><option value="student">학생</option><option value="teacher">교사</option><option value="admin">관리자</option></select></td><td><Badge tone={u.is_active ? "green" : "neutral"}>{u.is_active ? "활성" : "중지"}</Badge></td><td><button disabled={busy || u.id === user.id} onClick={() => { if (!window.confirm(`${u.username} 계정을 ${u.is_active ? "중지" : "활성화"}할까요?`)) return; void run(async () => { await api.patch(`/api/v1/admin/users/${u.id}/`, { is_active: !u.is_active }); refresh(v => v + 1); }); }}>{u.is_active ? "이용 중지" : "다시 활성화"}</button></td></tr>)}</tbody></table></div>}<p className="muted">관리자 권한 변경은 최고 관리자만 할 수 있습니다.</p></section>;
}

export function Classes({ classes, students, busy, run, refresh }: { classes: Classroom[]; students: Student[]; busy: boolean; run: RunAction; refresh: () => void }) {
  const [creating, setCreating] = useState(false);
  const [name, setName] = useState("");
  const [current, setCurrent] = useState<Classroom | null>(null);
  return <>
    <div className="page-heading"><div><p className="eyebrow">CLASSROOMS</p><h1>학급 관리</h1><p>학급을 만들고, 학생의 가입 요청을 승인하세요.</p></div><button className="primary" onClick={() => setCreating(true)}>+ 학급 만들기</button></div>
    {!classes.length ? <section className="panel"><Empty>첫 번째 학급을 만들어 주세요.</Empty></section> : <div className="class-grid">{classes.map((c, i) => <section className="panel class-card" key={c.id}><div className="class-card-top"><span className={`class-icon color-${i % 4}`} aria-hidden="true">▦</span><Badge tone={c.archived ? "neutral" : "green"}>{c.archived ? "보관" : "운영 중"}</Badge></div><h2>{c.name}</h2><p className="muted">학생 편성 · 가입 승인 · 초대 코드</p><button className="wide" onClick={() => setCurrent(c)}>학급 관리하기 →</button></section>)}</div>}
    {creating && <Modal title="학급 만들기" close={() => { if (!busy) setCreating(false); }}><form onSubmit={e => { e.preventDefault(); void run(async () => { await api.post("/api/v1/classes/", { name: name.trim() }); setName(""); setCreating(false); refresh(); }); }}><Field label="학급 이름"><input required maxLength={120} value={name} onChange={e => setName(e.target.value)} placeholder="예: 3학년 수학 탐험대" /></Field><footer><button className="primary" disabled={busy}>학급 생성하기</button></footer></form></Modal>}
    {current && <ClassDetail classroom={current} students={students} busy={busy} run={run} close={() => { if (!busy) setCurrent(null); }} changed={c => { setCurrent(c); refresh(); }} />}
  </>;
}

function ClassDetail({ classroom, students, busy, run, close, changed }: { classroom: Classroom; students: Student[]; busy: boolean; run: RunAction; close: () => void; changed: (c: Classroom) => void }) {
  const [revision, refresh] = useState(0);
  const [studentId, setStudentId] = useState("");
  const [copied, setCopied] = useState(false);
  const loaded = useLoad(signal => api.get<Enrollment[]>(`/api/v1/classes/${classroom.id}/enrollments/`, signal), [classroom.id, revision]);
  function status(enrollment: Enrollment, value: string) { void run(async () => { await api.patch(`/api/v1/classes/${classroom.id}/enrollments/${enrollment.id}/`, { status: value }); refresh(v => v + 1); changed(classroom); }); }
  return <Modal title={classroom.name} close={close}>
    <div className="invite-box"><p className="eyebrow">학급 초대 코드</p><input aria-label="학급 초대 코드" readOnly value={classroom.invite_code} onFocus={e => e.currentTarget.select()} /><p>학생이 가입하면 승인 대기 명단에 표시됩니다.</p><div className="actions"><button onClick={() => { void navigator.clipboard.writeText(classroom.invite_code).then(() => setCopied(true)).catch(() => setCopied(false)); }}>{copied ? "복사됨" : "코드 복사"}</button><button disabled={busy} onClick={() => { if (!window.confirm("기존 초대 코드를 폐기하고 새 코드를 만들까요?")) return; void run(async () => { const result = await api.post<Classroom>(`/api/v1/classes/${classroom.id}/rotate-code/`); setCopied(false); changed(result); }); }}>새 코드 발급</button></div></div>
    <form className="inline-form" onSubmit={e => { e.preventDefault(); void run(async () => { await api.post(`/api/v1/classes/${classroom.id}/enrollments/`, { student_id: Number(studentId) }); setStudentId(""); refresh(v => v + 1); changed(classroom); }); }}><Field label="담당 학생 편성"><select required value={studentId} onChange={e => setStudentId(e.target.value)}><option value="">학생 선택</option>{students.filter(s => !loaded.data?.some(e => e.student === s.id && e.status === "approved")).map(s => <option key={s.id} value={s.id}>{s.username}</option>)}</select></Field><button className="primary" disabled={busy || classroom.archived}>학급에 추가</button></form>
    <h3>학생 명단</h3>{loaded.loading ? <Loading /> : loaded.error ? <Failure message={loaded.error} retry={() => refresh(v => v + 1)} /> : !loaded.data?.length ? <Empty>아직 가입한 학생이 없습니다.</Empty> : <div className="table-wrap"><table><thead><tr><th>학생</th><th>상태</th><th>관리</th></tr></thead><tbody>{loaded.data.map(e => <tr key={e.id}><td>{e.username}</td><td><Badge tone={e.status === "approved" ? "green" : "neutral"}>{({ pending: "승인 대기", approved: "승인", inactive: "비활성" })[e.status]}</Badge></td><td>{e.status !== "approved" ? <button disabled={busy || classroom.archived} onClick={() => status(e, "approved")}>가입 승인</button> : <button disabled={busy} onClick={() => status(e, "inactive")}>비활성화</button>}</td></tr>)}</tbody></table></div>}
    <footer><button disabled={busy} onClick={() => { void run(async () => { const updated = await api.patch<Classroom>(`/api/v1/classes/${classroom.id}/`, { archived: !classroom.archived }); changed(updated); }); }}>{classroom.archived ? "학급 다시 운영" : "학급 보관"}</button><button onClick={close}>닫기</button></footer>
  </Modal>;
}
