import { useState } from "react";
import { formatDate, formatPercent, TeacherApi } from "./api";
import { Badge, displayAnswer, Empty, Failure, Loading, Modal, Progress, useLoad } from "./components";
import type { RunAction } from "./forms";
import type { Assignment, Recipient, Results as ResultsData } from "./types";

const api = new TeacherApi();
interface RecipientDetail extends Recipient { items: { id: number; content: { prompt: string; problem_id: string }; submitted_answer?: unknown; answer?: unknown; is_correct?: boolean; solution?: { steps?: Record<string, unknown>[] } }[] }

export function Results({ assignments, assignmentId, select, busy, run, reviewed }: { assignments: Assignment[]; assignmentId: number | null; select: (id: number) => void; busy: boolean; run: RunAction; reviewed: (assignment: Assignment) => void }) {
  const [revision, refresh] = useState(0);
  const [detail, setDetail] = useState<number | null>(null);
  const loaded = useLoad(signal => assignmentId ? api.get<ResultsData>(`/api/v1/assignments/${assignmentId}/results/`, signal) : Promise.resolve(null), [assignmentId, revision]);
  const result = loaded.data;
  return <>
    <div className="page-heading"><div><p className="eyebrow">LEARNING RESULTS</p><h1>학습 결과</h1><p>이 과제에서의 학습 진도와 문항별 정답률을 확인하세요.</p></div><select aria-label="결과를 볼 과제" value={assignmentId ?? ""} onChange={e => { setDetail(null); select(Number(e.target.value)); }}><option value="" disabled>과제 선택</option>{assignments.map(a => <option value={a.id} key={a.id}>{a.title}</option>)}</select></div>
    {!assignmentId ? <section className="panel"><Empty>배정한 과제가 없습니다. 먼저 과제를 배정해 주세요.</Empty></section> : loaded.loading ? <Loading /> : loaded.error ? <Failure message={loaded.error} retry={() => refresh(v => v + 1)} /> : result && <>
      <div className="scope-note"><Badge tone="green">과제별 통계</Badge><span>{result.assignment.title} · 배정 당시 {result.assignment.recipient_count}명 · {result.assignment.item_count}문항</span><small>전체 학습 이력과 별도로 집계합니다.</small></div>
      <div className="metric-grid"><Metric label="과제 제출" value={`${result.assignment.submitted_count} / ${result.assignment.recipient_count}`} /><Metric label="전체 정답률" value={formatPercent(result.assignment.accuracy)} /><Metric label="미제출 학생" value={`${result.unsubmitted_recipient_ids.length}명`} /><Metric label="배정 문항" value={`${result.assignment.item_count}문항`} /></div>
      <section className="panel"><div className="section-heading"><h2>학생별 학습 현황</h2><span className="muted">풀이 완료율과 최종 제출은 별도로 표시됩니다.</span></div><div className="table-wrap"><table><thead><tr><th>학생</th><th>완료율</th><th>정답률</th><th>풀이 시간</th><th>힌트</th><th>제출 상태</th><th>관리</th></tr></thead><tbody>{result.recipients.map(r => <tr key={r.recipient_id}><td><strong>{r.username}</strong></td><td><Progress value={r.progress} /><small>{r.completed}/{r.total}문항 · {formatPercent(r.progress)}</small></td><td>{formatPercent(r.accuracy)}</td><td>{Math.round(r.elapsed_ms / 1000)}초</td><td>{r.hint_count ?? 0}회</td><td><Badge tone={r.submitted_at ? "green" : "orange"}>{r.submitted_at ? "제출 완료" : "미제출"}</Badge>{r.submitted_at && <small>{formatDate(r.submitted_at)}</small>}</td><td><div className="actions"><button onClick={() => setDetail(r.recipient_id)}>상세 결과</button><button disabled={busy || !r.submitted_at || !r.wrong_item_ids.length} onClick={() => { void run(async () => { const review = await api.post<Assignment>(`/api/v1/assignments/${assignmentId}/reassign-wrong/`, { recipient_id: r.recipient_id, title: `${r.username} 오답 복습` }); reviewed(review); }); }}>오답 재배정</button></div></td></tr>)}</tbody></table></div></section>
      <div className="result-grid"><section className="panel"><div className="section-heading"><h2>문항별 정답률</h2></div><div className="table-wrap"><table><thead><tr><th>문항</th><th>응답</th><th>정답</th><th>정답률</th></tr></thead><tbody>{result.items.map(item => <tr key={item.item_id}><td>{item.position + 1}번</td><td>{item.answered}명</td><td>{item.correct}명</td><td><Progress value={item.accuracy} /><small>{formatPercent(item.accuracy)}</small></td></tr>)}</tbody></table></div></section><section className="panel"><div className="section-heading"><h2>개념별 성취</h2></div>{Object.entries(result.concepts).length ? Object.entries(result.concepts).map(([concept, metric]) => <div key={concept} className="concept-metric"><strong>{concept}</strong><span>{formatPercent(metric.total ? metric.correct / metric.total : 0)}</span><Progress value={metric.total ? metric.correct / metric.total : 0} /><small>{metric.correct}/{metric.total}개 정답</small></div>) : <Empty>등록된 개념이 없습니다.</Empty>}<p className="muted">이 과제의 최종 답안 기준이며, 미응답 문항은 정답에 포함되지 않습니다.</p></section></div>
    </>}
    {detail !== null && assignmentId && <RecipientModal assignmentId={assignmentId} recipientId={detail} close={() => setDetail(null)} />}
  </>;
}

export function Metric({ label, value }: { label: string; value: string }) { return <section className="metric"><p>{label}</p><strong>{value}</strong></section>; }

function RecipientModal({ assignmentId, recipientId, close }: { assignmentId: number; recipientId: number; close: () => void }) {
  const [revision, refresh] = useState(0);
  const loaded = useLoad(async signal => {
    const rows = await api.get<RecipientDetail[]>(`/api/v1/assignments/${assignmentId}/recipients/`, signal);
    return rows.find(r => r.recipient_id === recipientId) ?? null;
  }, [assignmentId, recipientId, revision]);
  return <Modal title="학생 문항별 결과" close={close}>{loaded.loading ? <Loading /> : loaded.error ? <Failure message={loaded.error} retry={() => refresh(v => v + 1)} /> : loaded.data ? <><h3>{loaded.data.username}</h3>{loaded.data.items.map((item, i) => <section key={item.id} className="answer-preview"><div className="section-heading"><strong>{i + 1}번 · {item.content.problem_id}</strong><Badge tone={item.is_correct === true ? "green" : "orange"}>{item.is_correct === true ? "정답" : item.is_correct === false ? "오답" : "미응답"}</Badge></div><p>{item.content.prompt}</p><p>학생 답안: <strong>{displayAnswer(item.submitted_answer)}</strong></p><p>정답: <strong>{displayAnswer(item.answer)}</strong></p>{item.solution?.steps?.map((step, index) => <p className="muted" key={index}>{String(step.explanation ?? step.expr ?? step.goal ?? "")}</p>)}</section>)}</> : <Empty>학생의 결과를 찾을 수 없습니다.</Empty>}</Modal>;
}
