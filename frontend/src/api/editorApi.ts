import { requestJson } from "./httpClient";
import type {
  BuildProblemResponse,
  DslMutationResponse,
  LayoutPatch,
  LayoutPatchResponse,
  LayoutPatchBuildResponse,
  ProblemDetailResponse,
  ProblemsListResponse,
} from "../types/api";

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

export function applyLayoutPatchesAndBuild(problemId: string, patches: LayoutPatch[], options: { format?: boolean } = {}) {
  return requestJson<LayoutPatchBuildResponse>(encodedProblemPath(problemId, "/layout-patch-and-build/"), {
    method: "POST",
    body: JSON.stringify({ patches, ...options }),
  });
}

export function applyLayoutPatches(problemId: string, patches: LayoutPatch[], options: { format?: boolean } = {}) {
  return requestJson<LayoutPatchResponse>(encodedProblemPath(problemId, "/layout-patch/"), {
    method: "POST",
    body: JSON.stringify({ patches, ...options }),
  });
}

export function saveDsl(problemId: string, dsl: string): Promise<DslMutationResponse> {
  return requestJson<DslMutationResponse>(encodedProblemPath(problemId, "/dsl/"), {
    method: "POST",
    body: JSON.stringify({ dsl }),
  });
}

export function formatDsl(problemId: string): Promise<DslMutationResponse> {
  return requestJson<DslMutationResponse>(encodedProblemPath(problemId, "/dsl/format/"), { method: "POST" });
}

export function buildProblem(problemId: string): Promise<BuildProblemResponse> {
  return requestJson<BuildProblemResponse>(encodedProblemPath(problemId, "/build/"), { method: "POST" });
}
