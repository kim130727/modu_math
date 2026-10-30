import { cloneElement, createContext, isValidElement, useContext, useEffect, useId, useRef, useState, type DependencyList, type ReactElement, type ReactNode } from "react";
import { Layer, Stage } from "react-konva";
import { problemDetailToCanonicalProblem, type LayoutDocument, type RendererDocument } from "../api/editorApi";
import { problemJsonToEditorDocument } from "../konva_editor/converters";
import { ShapeRenderer } from "../konva_editor/ShapeRenderer";
import type { ProblemDetail } from "./types";

export const FeedbackContext = createContext("");

export function useLoad<T>(loader: (signal: AbortSignal) => Promise<T>, deps: DependencyList) {
  const current = useRef(loader);
  current.current = loader;
  const [state, setState] = useState<{ data: T | null; loading: boolean; error: string }>({ data: null, loading: true, error: "" });
  useEffect(() => {
    const controller = new AbortController();
    setState(previous => ({ data: previous.data, loading: true, error: "" }));
    current.current(controller.signal).then(
      data => { if (!controller.signal.aborted) setState({ data, loading: false, error: "" }); },
      error => { if (!controller.signal.aborted) setState({ data: null, loading: false, error: String(error instanceof Error ? error.message : error) }); },
    );
    return () => controller.abort();
  }, deps);
  return state;
}

export function Empty({ children }: { children: ReactNode }) { return <div className="empty-state"><span aria-hidden="true">∅</span><p>{children}</p></div>; }
export function Loading() { return <div className="loading-state" role="status">학습 정보를 불러오고 있습니다…</div>; }
export function Failure({ message, retry }: { message: string; retry: () => void }) { return <div className="error-state" role="alert"><p>{message}</p><button onClick={retry}>다시 불러오기</button></div>; }
export function Badge({ children, tone = "neutral" }: { children: ReactNode; tone?: string }) { return <span className={`badge badge-${tone}`}>{children}</span>; }
export function Progress({ value }: { value: number }) { return <span className="progress-track" role="progressbar" aria-label="풀이 완료율" aria-valuenow={Math.round(value * 100)} aria-valuemin={0} aria-valuemax={100}><span style={{ width: `${Math.max(0, Math.min(1, value)) * 100}%` }} /></span>; }
export function Field({ label, children, hint }: { label: string; children: ReactNode; hint?: string }) {
  const id = useId();
  return <div className="field"><label htmlFor={id}>{label}</label>{isValidElement(children) ? cloneElement(children as ReactElement<{ id: string; "aria-describedby"?: string }>, { id, "aria-describedby": hint ? `${id}-hint` : undefined }) : children}{hint && <small id={`${id}-hint`}>{hint}</small>}</div>;
}

export function Modal({ title, children, close }: { title: string; children: ReactNode; close: () => void }) {
  const feedback = useContext(FeedbackContext);
  const ref = useRef<HTMLDialogElement>(null);
  const titleId = "teacher-dialog-title";
  useEffect(() => {
    const dialog = ref.current;
    const previous = document.activeElement as HTMLElement | null;
    dialog?.showModal();
    return () => { dialog?.close(); previous?.focus(); };
  }, []);
  return <dialog ref={ref} className="teacher-modal" aria-labelledby={titleId} onCancel={event => { event.preventDefault(); close(); }}>
    <header><div><p className="eyebrow">MODU MATH</p><h2 id={titleId}>{title}</h2></div><button className="icon-button" onClick={close} aria-label="닫기">×</button></header>
    {feedback && <p className="form-error" role="alert">{feedback}</p>}
    {children}
  </dialog>;
}

export function ReadonlyProblem({ detail, sourceId }: { detail: Pick<ProblemDetail, "problem_id" | "renderer_data"> & { layout_data?: Record<string, unknown> }; sourceId?: string }) {
  const container = useRef<HTMLDivElement>(null);
  const [width, setWidth] = useState(680);
  const [, setFonts] = useState(false);
  useEffect(() => {
    const observer = new ResizeObserver(entries => setWidth(entries[0].contentRect.width));
    if (container.current) observer.observe(container.current);
    let active = true;
    void document.fonts.ready.then(() => { if (active) setFonts(true); });
    return () => { active = false; observer.disconnect(); };
  }, []);
  const problem = problemDetailToCanonicalProblem({
    problem_id: sourceId ?? detail.problem_id,
    renderer: detail.renderer_data as unknown as RendererDocument,
    layout: detail.layout_data ? detail.layout_data as unknown as LayoutDocument : null,
    base_dir: "", dsl: "", semantic: null, solvable: null, svg: null,
  });
  const doc = problemJsonToEditorDocument(problem);
  const scale = Math.min(1, width / Math.max(1, doc.canvas.width));
  const noop = () => {};
  return <div className="readonly-problem" ref={container} role="img" aria-label="문제 캔버스 미리보기">
    <Stage width={Math.max(1, doc.canvas.width * scale)} height={Math.max(100, doc.canvas.height * scale)} scaleX={scale} scaleY={scale} listening={false}>
      <Layer>{doc.shapes.map(shape => <ShapeRenderer key={shape.id} shape={shape} interactive={false} isSelected={false} nodeRef={noop} onSelect={noop} onDragStart={noop} onDragMove={noop} onDragEnd={noop} onContextMenu={noop} />)}</Layer>
    </Stage>
    {!doc.shapes.length && <p className="muted">미리보기 도형이 없습니다. 편집기에서 문제를 확인해 주세요.</p>}
  </div>;
}

export function displayAnswer(value: unknown): string {
  if (value == null) return "미응답";
  if (Array.isArray(value)) return value.map(displayAnswer).join(", ");
  if (typeof value === "object") {
    const record = value as Record<string, unknown>;
    if ("value" in record) return displayAnswer(record.value);
    if ("answer_key" in record) return displayAnswer(record.answer_key);
    return Object.values(record).map(displayAnswer).join(", ");
  }
  return String(value);
}
