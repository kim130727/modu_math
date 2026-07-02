import { requestJson } from "./httpClient";
import type { ProblemDetailResponse, ProblemsListResponse } from "../types/api";

function encodedProblemPath(problemId: string, suffix = ""): string {
  const safe = problemId
    .split("/")
    .map((part) => encodeURIComponent(part))
    .join("/");
  return `/api/editor/problems/${safe}${suffix}`;
}

export function listProblems(): Promise<ProblemsListResponse> {
  return requestJson<ProblemsListResponse>("/api/editor/problems/");
}

export function loadProblem(problemId: string): Promise<ProblemDetailResponse> {
  return requestJson<ProblemDetailResponse>(encodedProblemPath(problemId, "/"));
}

