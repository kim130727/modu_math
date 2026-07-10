import type { LayoutDocument } from "./layout";
import type { RendererDocument } from "./renderer";

export type ApiErrorCategory =
  | "DSL_PARSE_ERROR"
  | "DSL_PATCH_ERROR"
  | "BUILD_ERROR"
  | "SCHEMA_ERROR"
  | "NETWORK_ERROR"
  | "UNKNOWN_ERROR";

export type TutorPreviewMode = "mock" | "openai";

export interface TutorPreviewMessage {
  role: "user" | "assistant";
  content: string;
}

export interface TutorPreviewCheck {
  level: "ok" | "warn" | "error" | string;
  message: string;
}

export interface TutorPreviewStatusResponse {
  ok: boolean;
  openai_configured: boolean;
  model: string;
}

export interface TutorPreviewResponse extends TutorPreviewStatusResponse {
  reply: string;
  checks: TutorPreviewCheck[];
}

export interface ProblemSummary {
  problem_id: string;
  root: string;
  path: string;
  has_input_png: boolean;
  has_dsl: boolean;
  has_semantic: boolean;
  has_solvable: boolean;
  has_layout: boolean;
  has_renderer: boolean;
  has_svg: boolean;
}

export interface ProblemsListResponse {
  problems: ProblemSummary[];
}

export interface ProblemDetailResponse {
  problem_id: string;
  base_dir: string;
  dsl: string;
  semantic: Record<string, unknown> | null;
  solvable: Record<string, unknown> | null;
  layout: LayoutDocument | null;
  renderer: RendererDocument | null;
  svg: string | null;
  svg_url?: string | null;
}

export interface LayoutPatch {
  target: string;
  op: "update" | "add" | "delete" | "layer" | string;
  value?: Record<string, unknown>;
}

export interface LayoutPatchResponse {
  ok: boolean;
  problem_id: string;
  dsl: string;
  applied: Record<string, unknown>[];
}

export interface LayoutPatchBuildResponse {
  ok: boolean;
  problem_id: string;
  dsl: string;
  applied: Record<string, unknown>[];
  build?: {
    ok: boolean;
    stdout: string;
    stderr: string;
    error?: string;
  };
  artifacts?: {
    semantic?: Record<string, unknown> | null;
    solvable?: Record<string, unknown> | null;
    layout?: LayoutDocument | null;
    renderer?: RendererDocument | null;
    svg?: string | null;
  };
}

export interface DslMutationResponse {
  ok: boolean;
  problem_id: string;
  dsl: string;
}

export interface BuildProblemResponse {
  ok: boolean;
  problem_id: string;
  stdout: string;
  stderr: string;
  error?: string;
  artifacts?: {
    semantic?: Record<string, unknown> | null;
    solvable?: Record<string, unknown> | null;
    layout?: LayoutDocument | null;
    renderer?: RendererDocument | null;
    svg?: string | null;
  };
}

export interface BuildOutputState {
  ok: boolean;
  stdout: string;
  stderr: string;
  error?: string;
}

export interface EditorError {
  message: string;
  category: ApiErrorCategory;
  status: number;
}
