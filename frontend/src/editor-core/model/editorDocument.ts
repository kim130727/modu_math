import type { ProblemDetailResponse } from "../../types/api";
import type { LayoutSlot } from "../../types/layout";

export interface EditorDocument {
  problemId: string;
  dslSource: string;
  detail: ProblemDetailResponse;
  slots: LayoutSlot[];
}

export function createEditorDocument(detail: ProblemDetailResponse): EditorDocument {
  return {
    problemId: detail.problem_id,
    dslSource: detail.dsl,
    detail,
    slots: detail.layout?.slots ?? [],
  };
}

