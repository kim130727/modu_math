import { editorAuthHeaders, storeToken } from "../auth/session";
import type { Page, Problem, ProblemDetail } from "./types";

export class ApiError extends Error {
  constructor(public readonly status: number, message: string) { super(message); }
}

function errorText(body: unknown): string {
  if (typeof body === "string") return body;
  if (Array.isArray(body)) return body.map(errorText).join(" ");
  if (body && typeof body === "object") return Object.values(body).map(errorText).join(" ");
  return "요청을 완료하지 못했습니다. 잠시 후 다시 시도해 주세요.";
}

export class TeacherApi {
  async request<T>(path: string, init: RequestInit = {}): Promise<T> {
    if (!path.startsWith("/api/v1/")) throw new Error("허용되지 않은 API 경로입니다.");
    const response = await fetch(path, {
      ...init,
      headers: { Accept: "application/json", "Content-Type": "application/json", ...editorAuthHeaders(), ...init.headers },
    });
    const text = await response.text();
    let data: unknown;
    try { data = text ? JSON.parse(text) : null; } catch { data = null; }
    if (!response.ok) {
      if (response.status === 401) {
        storeToken("");
        window.dispatchEvent(new Event("modu-session-expired"));
      }
      throw new ApiError(response.status, data ? errorText(data) : `서버 응답 오류 (${response.status})`);
    }
    return data as T;
  }

  get<T>(path: string, signal?: AbortSignal): Promise<T> { return this.request(path, { signal }); }
  post<T>(path: string, body: unknown = {}): Promise<T> { return this.request(path, { method: "POST", body: JSON.stringify(body) }); }
  patch<T>(path: string, body: unknown): Promise<T> { return this.request(path, { method: "PATCH", body: JSON.stringify(body) }); }

  async all<T>(path: string, signal?: AbortSignal): Promise<T[]> {
    const rows: T[] = [];
    let next: string | null = path;
    while (next) {
      const data: T[] | Page<T> = await this.get(next, signal);
      if (Array.isArray(data)) return rows.concat(data);
      rows.push(...data.results);
      if (!data.next) break;
      const target: URL = new URL(data.next, window.location.origin);
      if (target.origin !== window.location.origin || !target.pathname.startsWith("/api/v1/")) throw new Error("잘못된 다음 페이지 주소입니다.");
      next = target.pathname + target.search;
    }
    return rows;
  }

  problems(filters: Record<string, string>, page: number, signal?: AbortSignal): Promise<Page<Problem>> {
    const query = new URLSearchParams({ page: String(page) });
    for (const [key, value] of Object.entries(filters)) if (value) query.set(key, value);
    return this.get(`/api/v1/problems/?${query}`, signal);
  }
  problem(id: number, signal?: AbortSignal): Promise<ProblemDetail> { return this.get(`/api/v1/problems/${id}/`, signal); }
}

export function editorLink(problem: Pick<Problem, "problem_id" | "language" | "path" | "file_prefix">): string {
  const directory = problem.path.replace(/^examples\/problems\//, "").replace(/\/+$/, "");
  const source = `${directory || problem.language}/${problem.file_prefix || problem.problem_id}.dsl.py`;
  return `/editor-konva/?problem=${encodeURIComponent(source)}`;
}

export function formatPercent(value: number): string { return `${Math.round(value * 100)}%`; }
export function formatDate(value: string | null): string {
  return value ? new Intl.DateTimeFormat("ko-KR", { timeZone: "Asia/Seoul", month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" }).format(new Date(value)) : "제한 없음";
}
