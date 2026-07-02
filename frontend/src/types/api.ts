import type { LayoutDocument } from "./layout";
import type { RendererDocument } from "./renderer";

export type ApiErrorCategory =
  | "DSL_PARSE_ERROR"
  | "DSL_PATCH_ERROR"
  | "BUILD_ERROR"
  | "SCHEMA_ERROR"
  | "NETWORK_ERROR"
  | "UNKNOWN_ERROR";

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
}

export interface EditorError {
  message: string;
  category: ApiErrorCategory;
  status: number;
}

