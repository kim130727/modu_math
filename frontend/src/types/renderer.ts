export interface RendererDocument {
  problem_id?: string;
  view_box?: {
    width?: number;
    height?: number;
    background?: string;
  };
  elements?: RendererElement[];
  contract_version?: string;
}

export interface RendererElement {
  id?: string;
  type?: string;
  attributes?: Record<string, unknown>;
  refs?: {
    layout_slot_id?: string;
    [key: string]: unknown;
  };
  source_ref?: string;
  text?: string;
}

