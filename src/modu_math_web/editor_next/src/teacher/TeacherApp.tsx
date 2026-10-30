import { useCallback, useEffect, useRef, useState, type FormEvent } from "react";
import { sessionToken, storeToken } from "../auth/session";
import { formatDate, formatPercent, TeacherApi } from "./api";
import { Bank } from "./Bank";
import { Badge, Empty, Failure, FeedbackContext, Field, Loading, Progress, useLoad } from "./components";
import { AssignmentForm, ProblemSetForm } from "./forms";
import { Classes, Students } from "./People";
import { Metric, Results } from "./Results";
import type { Assignment, Classroom, Dashboard, Problem, ProblemSet, Section, Student, User } from "./types";

const api = new TeacherApi();
const menus: { id: Section; label: string; icon: string }[] = [
  { id: "dashboard", label: "대시보드", icon: "◫" }, { id: "bank", label: "문제은행", icon: "▤" },
  { id: "sets", label: "문제집 관리", icon: "▥" }, { id: "assignments", label: "과제 배정", icon: "↗" },
  { id: "students", label: "학생 관리", icon: "♧" }, { id: "classes", label: "학급 관리", icon: "▦" },
  { id: "results", label: "학습 결과", icon: "▧" },
];

function sectionFromHash(): Section { return menus.find(m => `#${m.id}` === window.location.hash.split("/")[0])?.id ?? "dashboard"; }
function resultFromHash(): number | null { const match = window.location.hash.match(/^#results\/(\d+)$/); return match ? Number(match[1]) : null; }

export default function TeacherApp() {
  const [user, setUser] = useState<User | null>(null);
  const [restoring, setRestoring] = useState(true);
  const [error, setError] = useState("");
  useEffect(() => {
    let active = true;
    const expired = () => { setUser(null); setError("로그인이 만료되었습니다. 다시 로그인해 주세요."); };
    window.addEventListener("modu-session-expired", expired);
    if (!sessionToken()) setRestoring(false);
    else void api.get<User>("/api/v1/auth/me/").then(async current => {
      if (current.role === "student") throw new Error("교사 또는 관리자 계정으로 로그인해 주세요.");
      await api.post("/api/v1/auth/editor-session/");
      if (active) setUser(current);
    }).catch(err => { if (active) { storeToken(""); setError(err.message); } }).finally(() => { if (active) setRestoring(false); });
    return () => { active = false; window.removeEventListener("modu-session-expired", expired); };
  }, []);
  async function login(username: string, password: string) {
    const response = await api.post<{ token: string; user: User }>("/api/v1/auth/login/", { username, password });
    if (response.user.role === "student") throw new Error("교사 또는 관리자 계정으로 로그인해 주세요.");
    storeToken(response.token);
    try { await api.post("/api/v1/auth/editor-session/"); }
    catch (err) { storeToken(""); throw err; }
    setError(""); setUser(response.user);
  }
  async function logout() {
    try { await api.post("/api/v1/auth/logout/"); }
    finally { storeToken(""); setUser(null); }
  }
  if (restoring) return <main className="login-shell"><Loading /></main>;
  return user ? <Workspace user={user} logout={logout} /> : <Login login={login} initialError={error} />;
}

function Login({ login, initialError }: { login: (username: string, password: string) => Promise<void>; initialError: string }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(initialError);
  async function submit(event: FormEvent) {
    event.preventDefault(); if (busy) return;
    setBusy(true); setError("");
    try { await login(username.trim(), password); } catch (err) { setError(err instanceof Error ? err.message : "로그인하지 못했습니다."); } finally { setBusy(false); }
  }
  return <main className="login-shell"><div className="login-story"><div className="brand"><span className="brand-mark">m<span>²</span></span><strong>모두의 수학</strong></div><p className="eyebrow">FOR EVERY LEARNING MOMENT</p><h1>문제에서 배움으로,<br />배움에서 성장으로.</h1><p>좋은 문제를 고르고, 학생에게 전하고,<br />한 명 한 명의 배움을 함께 살펴보세요.</p><div className="math-motif" aria-hidden="true"><span>+</span><span>∑</span><span>÷</span><span>×</span></div></div><section className="login-card"><p className="eyebrow">TEACHER WORKSPACE</p><h2>선생님, 반갑습니다.</h2><p className="muted">교사 또는 관리자 계정으로 로그인하세요.</p><form onSubmit={submit}><Field label="아이디"><input required autoComplete="username" value={username} onChange={e => setUsername(e.target.value)} /></Field><Field label="비밀번호"><input type="password" required autoComplete="current-password" value={password} onChange={e => setPassword(e.target.value)} /></Field>{error && <p className="form-error" role="alert">{error}</p>}<button className="primary wide" disabled={busy}>{busy ? "로그인 중…" : "로그인"}</button></form><p className="login-help">교사 권한이 필요하면 플랫폼 관리자에게 요청해 주세요.</p></section></main>;
}

function Workspace({ user, logout }: { user: User; logout: () => Promise<void> }) {
  const [section, setSection] = useState<Section>(sectionFromHash);
  const [revision, refresh] = useState(0);
  const [busy, setBusy] = useState(false);
  const pending = useRef(false);
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");
  const [selected, setSelected] = useState<Problem[]>([]);
  const [setModal, setSetModal] = useState<"new" | ProblemSet | null>(null);
  const [assignModal, setAssignModal] = useState<{ setId?: number; set?: ProblemSet } | null>(null);
  const [resultId, setResultId] = useState<number | null>(resultFromHash);
  const loaded = useLoad(async signal => {
    const [dashboard, students, classes, sets, assignments] = await Promise.all([
      api.get<Dashboard>("/api/v1/teacher/dashboard/", signal), api.all<Student>("/api/v1/students/", signal),
      api.all<Classroom>("/api/v1/classes/", signal), api.all<ProblemSet>("/api/v1/problem-sets/", signal), api.all<Assignment>("/api/v1/assignments/", signal),
    ]);
    return { dashboard, students, classes, sets, assignments };
  }, [revision]);
  const navigate = useCallback((next: Section) => { setError(""); window.location.hash = next; setSection(next); }, []);
  useEffect(() => { const change = () => { setSection(sectionFromHash()); const id = resultFromHash(); if (id) setResultId(id); }; window.addEventListener("hashchange", change); return () => window.removeEventListener("hashchange", change); }, []);
  useEffect(() => {
    const id = resultId ?? loaded.data?.assignments[0]?.id;
    if (!id) return;
    if (resultId === null) setResultId(id);
    if (section === "results") window.history.replaceState(null, "", `#results/${id}`);
  }, [loaded.data, resultId, section]);
  async function run(work: () => Promise<void>) {
    if (pending.current) return;
    pending.current = true; setBusy(true); setError(""); setNotice("");
    try { await work(); setNotice("변경 내용을 저장했습니다."); } catch (err) { setError(err instanceof Error ? err.message : "요청을 처리하지 못했습니다."); }
    finally { pending.current = false; setBusy(false); }
  }
  const reload = () => refresh(v => v + 1);
  const data = loaded.data;
  function showResult(id: number) { setResultId(id); setError(""); setSection("results"); window.location.hash = `results/${id}`; }
  return <FeedbackContext.Provider value={error}><div className="teacher-layout">
    <aside className="teacher-sidebar"><a href="/teacher/" className="brand"><span className="brand-mark">m<span>²</span></span><span><strong>모두의 수학</strong><small>TEACHER WORKSPACE</small></span></a><p className="nav-label">학습 관리</p><nav aria-label="교사 메뉴">{menus.map(m => <a key={m.id} href={`#${m.id}`} aria-current={section === m.id ? "page" : undefined} onClick={() => { setError(""); setSection(m.id); }}><span aria-hidden="true">{m.icon}</span>{m.label}{m.id === "bank" && selected.length > 0 && <small>{selected.length}</small>}</a>)}</nav><div className="sidebar-bottom"><div className="sidebar-tip"><span>작은 배움이 모여<br />큰 성장이 됩니다.</span><i aria-hidden="true">✳</i></div><a href="/editor-konva/">문제 편집기 열기 ↗</a></div></aside>
    <div className="teacher-body"><header className="teacher-topbar"><span>나의 교실 <span className="breadcrumb">/ {menus.find(m => m.id === section)?.label}</span></span><div><span className="account-avatar">{user.username.slice(0, 1).toUpperCase()}</span><strong>{user.username}</strong><Badge>{user.role === "admin" ? "관리자" : "교사"}</Badge><button disabled={busy} onClick={() => { void run(logout); }}>로그아웃</button></div></header><main className="teacher-main" aria-busy={loaded.loading || busy}>
      {notice && <div className="notice" role="status">✓ {notice}</div>}{error && <div className="error-state" role="alert">{error}</div>}
      {loaded.loading && !data ? <Loading /> : loaded.error ? <Failure message={loaded.error} retry={reload} /> : data && <>
        {section === "dashboard" && <><div className="page-heading"><div><p className="eyebrow">YOUR LEARNING SPACE</p><h1>{user.username} 선생님의 교실</h1><p>학생들의 오늘을 살피고, 다음 배움을 준비하세요.</p></div><time className="today">{new Intl.DateTimeFormat("ko-KR", { timeZone: "Asia/Seoul", year: "numeric", month: "long", day: "numeric", weekday: "long" }).format(new Date())}</time></div><section className="welcome-banner"><div><Badge>수업 준비, 한 곳에서</Badge><h2>좋은 문제 하나가<br />새로운 배움의 시작이니까요.</h2><p>문제 선택부터 결과 확인까지, 차근차근 함께해요.</p><button onClick={() => navigate("bank")}>문제 고르러 가기 <span>↗</span></button></div><div className="banner-shapes" aria-hidden="true"><span>+</span><span>÷</span><span>×</span></div></section><div className="metric-grid"><Metric label="담당 학생" value={`${data.dashboard.students}명`} /><Metric label="운영 중인 학급" value={`${data.dashboard.classes}개`} /><Metric label="배정한 과제" value={`${data.dashboard.assignments}개`} /><Metric label="미제출 과제" value={`${data.dashboard.unsubmitted}건`} /></div><section className="panel quick-start"><div className="section-heading"><h2>다음 수업을 준비해 볼까요?</h2><span className="muted">네 단계로 이어지는 학습</span></div><div className="workflow">{[{ label: "문제 선택", sub: "수업에 맞는 문제 찾기", target: "bank" }, { label: "문제집 구성", sub: "순서와 분량 정하기", target: "sets" }, { label: "과제 배정", sub: "학생·학급에 전달하기", target: "assignments" }, { label: "결과 확인", sub: "배움의 다음 단계 찾기", target: "results" }].map((step, i) => <button key={step.target} onClick={() => navigate(step.target as Section)}><span>{String(i + 1).padStart(2, "0")}</span><strong>{step.label}</strong><small>{step.sub}</small><i aria-hidden="true">↗</i></button>)}</div></section><section className="panel"><div className="section-heading"><h2>최근 배정한 과제</h2><button className="text-button" onClick={() => navigate("assignments")}>전체 보기 →</button></div><AssignmentTable assignments={data.assignments.slice(0, 5)} result={showResult} /></section></>}
        {section === "bank" && <Bank selected={selected} setSelected={setSelected} createSet={() => { setError(""); setSetModal("new"); }} busy={busy} run={run} />}
        {section === "sets" && <><div className="page-heading"><div><p className="eyebrow">PROBLEM SETS</p><h1>문제집 관리</h1><p>문제를 순서대로 담고, 수업에 맞게 다듬으세요.</p></div><button className="primary" onClick={() => navigate("bank")}>+ 문제은행에서 만들기</button></div><section className="panel">{!data.sets.length ? <Empty>아직 문제집이 없습니다. 문제은행에서 문제를 선택해 주세요.</Empty> : <div className="table-wrap"><table><thead><tr><th>문제집</th><th>문항 수</th><th>버전</th><th>관리</th></tr></thead><tbody>{data.sets.map(s => <tr key={s.id}><td><strong>{s.title}</strong><small>{s.description}</small></td><td>{s.items.length}문항</td><td><Badge>v{s.version}</Badge></td><td><div className="actions"><button disabled={busy} onClick={() => { setError(""); setSetModal(s); }}>구성 수정</button><button disabled={busy} onClick={() => { void run(async () => { await api.post(`/api/v1/problem-sets/${s.id}/duplicate/`); reload(); }); }}>복제</button><button className="primary" disabled={busy} onClick={() => { setError(""); setAssignModal({ setId: s.id }); }}>과제 배정</button></div></td></tr>)}</tbody></table></div>}</section></>}
        {section === "assignments" && <><div className="page-heading"><div><p className="eyebrow">ASSIGNMENTS</p><h1>과제 배정</h1><p>학생에게 배움을 전하고, 제출 현황을 살펴보세요.</p></div><button className="primary" disabled={!data.sets.length || busy} onClick={() => { setError(""); setAssignModal({}); }}>+ 새 과제 배정</button></div>{!data.sets.length && <p className="info-note">먼저 문제은행에서 문제집을 만들어 주세요.</p>}<section className="panel"><AssignmentTable assignments={data.assignments} result={showResult} update={(a, value) => { void run(async () => { await api.patch(`/api/v1/assignments/${a.id}/`, { status: value }); reload(); }); }} busy={busy} /></section></>}
        {section === "students" && <Students user={user} students={data.students} busy={busy} run={run} refresh={reload} />}
        {section === "classes" && <Classes classes={data.classes} students={data.students} busy={busy} run={run} refresh={reload} />}
        {section === "results" && <Results assignments={data.assignments} assignmentId={resultId ?? data.assignments[0]?.id ?? null} select={setResultId} busy={busy} run={run} reviewed={assignment => { setNotice(`${assignment.title} 과제를 배정했습니다.`); reload(); }} />}
      </>}
      <footer className="page-footer">MODU MATH <span>한 사람의 배움도 놓치지 않도록.</span></footer>
    </main></div>
    {setModal && <ProblemSetForm original={setModal === "new" ? undefined : setModal} selected={selected} busy={busy} run={run} close={() => { if (!busy) setSetModal(null); }} saved={(set, assign) => { setSetModal(null); setSelected([]); if (assign) { setAssignModal({ setId: set.id, set }); navigate("assignments"); } else navigate("sets"); reload(); }} />}
    {assignModal && data && <AssignmentForm initialSet={assignModal.setId} sets={assignModal.set ? [...data.sets.filter(s => s.id !== assignModal.set?.id), assignModal.set] : data.sets} students={data.students} classes={data.classes} busy={busy} run={run} close={() => { if (!busy) setAssignModal(null); }} saved={assignment => { setAssignModal(null); reload(); showResult(assignment.id); }} />}
  </div></FeedbackContext.Provider>;
}

function AssignmentTable({ assignments, result, update, busy }: { assignments: Assignment[]; result: (id: number) => void; update?: (assignment: Assignment, status: string) => void; busy?: boolean }) {
  if (!assignments.length) return <Empty>아직 배정한 과제가 없습니다.</Empty>;
  return <div className="table-wrap"><table><thead><tr><th>과제</th><th>마감일</th><th>제출 현황</th><th>정답률</th><th>상태</th><th>결과</th></tr></thead><tbody>{assignments.map(a => <tr key={a.id}><td><strong>{a.title}</strong><small>{a.item_count}문항 · {a.recipient_count}명 · 문제집 v{a.source_version}</small></td><td>{formatDate(a.due_at)}</td><td><Progress value={a.recipient_count ? a.submitted_count / a.recipient_count : 0} /><small>{a.submitted_count}/{a.recipient_count}명 제출</small></td><td>{formatPercent(a.accuracy)}</td><td>{update ? <select aria-label={`${a.title} 상태`} value={a.status} disabled={busy} onChange={e => update(a, e.target.value)}><option value="active">진행</option><option value="closed">종료</option><option value="cancelled">취소</option></select> : <Badge tone={a.status === "active" ? "green" : "neutral"}>{({ active: "진행", closed: "종료", cancelled: "취소" })[a.status]}</Badge>}</td><td><button onClick={() => result(a.id)}>결과 보기 →</button></td></tr>)}</tbody></table></div>;
}
