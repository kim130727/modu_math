import type { ProblemJson, ProblemObject } from "../types/problem";
import { localizePathData } from "../utils/pathData";

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
  layout: LayoutDocument | null;
  renderer: RendererDocument | null;
  semantic: Record<string, unknown> | null;
  solvable: Record<string, unknown> | null;
  svg: string | null;
}

export interface LayoutDocument {
  problem_id?: string;
  title?: string;
  canvas?: { width: number; height: number };
  slots?: LayoutSlot[];
}

export interface LayoutSlot {
  id: string;
  kind: string;
  content: Record<string, unknown>;
}

export interface RendererDocument {
  problem_id?: string;
  canvas?: { width: number; height: number };
  elements?: RendererElement[];
}

export interface RendererElement {
  id: string;
  type: string;
  attributes: Record<string, unknown>;
  source_ref?: string;
  text?: string;
}

export interface LayoutPatch {
  target: string;
  op: "add" | "update" | "delete";
  value?: Record<string, unknown>;
}

export interface LayoutPatchResponse {
  ok: boolean;
  problem_id: string;
  applied: Array<{ target: string; op: string; fields: string[] }>;
  dsl: string;
}

function encodedProblemPath(problemId: string, suffix = ""): string {
  const safe = problemId
    .split("/")
    .map((part) => encodeURIComponent(part))
    .join("/");
  return `/api/editor/problems/${safe}${suffix}`;
}

async function requestJson<T>(url: string, init?: RequestInit): Promise<T> {
  const response = await fetch(url, {
    ...init,
    headers: { Accept: "application/json", ...init?.headers },
  });
  const body = (await response.json()) as unknown;
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${JSON.stringify(body)}`);
  }
  return body as T;
}

export function listProblems(): Promise<ProblemsListResponse> {
  return requestJson<ProblemsListResponse>("/api/editor/problems/");
}

export function loadProblem(problemId: string): Promise<ProblemDetailResponse> {
  return requestJson<ProblemDetailResponse>(encodedProblemPath(problemId, "/"));
}

export async function applyLayoutPatches(
  problemId: string,
  patches: LayoutPatch[],
  options: { format?: boolean } = {},
): Promise<LayoutPatchResponse> {
  return requestJson<LayoutPatchResponse>(encodedProblemPath(problemId, "/layout-patch/"), {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify({ patches, format: options.format ?? true }),
  });
}

export function problemDetailToCanonicalProblem(detail: ProblemDetailResponse): ProblemJson {
  const layout = detail.layout;
  const renderer = detail.renderer;
  const canvas = renderer?.canvas ?? layout?.canvas ?? { width: 1280, height: 720 };
  return {
    id: detail.problem_id,
    title: layout?.title ?? detail.problem_id,
    canvas,
    // Keep table parts as individual editable shapes for now. The custom TableShape
    // prototype is useful for whole-table semantics, but it blocks practical cell
    // and divider editing until we add a dedicated in-shape interaction model.
    objects: renderer?.elements?.length
      ? renderer.elements.flatMap((element) => rendererElementToProblemObject(detail.problem_id, element))
      : (layout?.slots ?? []).flatMap((slot) => layoutSlotToProblemObject(detail.problem_id, slot)),
  };
}

function rendererElementsToTableObjects(elements: RendererElement[]): { objects: ProblemObject[]; consumedSlotIds: Set<string> } {
  const groups = new Map<string, RendererElement[]>();
  for (const element of elements) {
    const slotId = sourceId(element);
    const base = tableBaseFromSlotId(slotId);
    if (!base) continue;
    const group = groups.get(base) ?? [];
    group.push(element);
    groups.set(base, group);
  }

  const consumedSlotIds = new Set<string>();
  const objects: ProblemObject[] = [];
  for (const [base, group] of groups) {
    const table = rendererTableGroupToProblemObject(base, group);
    if (!table) continue;
    objects.push(table);
    for (const element of group) consumedSlotIds.add(sourceId(element));
  }
  return { objects, consumedSlotIds };
}

function layoutSlotsToTableObjects(slots: LayoutSlot[]): { objects: ProblemObject[]; consumedSlotIds: Set<string> } {
  const groups = new Map<string, LayoutSlot[]>();
  for (const slot of slots) {
    const base = tableBaseFromSlotId(slot.id);
    if (!base) continue;
    const group = groups.get(base) ?? [];
    group.push(slot);
    groups.set(base, group);
  }

  const consumedSlotIds = new Set<string>();
  const objects: ProblemObject[] = [];
  for (const [base, group] of groups) {
    const table = layoutTableGroupToProblemObject(base, group);
    if (!table) continue;
    objects.push(table);
    for (const slot of group) consumedSlotIds.add(slot.id);
  }
  return { objects, consumedSlotIds };
}

function rendererTableGroupToProblemObject(base: string, elements: RendererElement[]): ProblemObject | null {
  const outer = elements.find((element) => sourceId(element) === `${base}.outer` && element.type === "rect");
  if (!outer) return null;
  const attrs = outer.attributes;
  const x = numberValue(attrs.x, 0);
  const y = numberValue(attrs.y, 0);
  const width = numberValue(attrs.width, 1);
  const height = numberValue(attrs.height, 1);
  const verticals = elements
    .filter((element) => /^v\d+$/.test(tableSuffix(sourceId(element), base)) && (element.type === "line" || element.type === "rect"))
    .map((element) =>
      element.type === "line"
        ? numberValue(element.attributes.x1, x)
        : numberValue(element.attributes.x, x) + numberValue(element.attributes.width, 0) / 2,
    )
    .sort((a, b) => a - b);
  const horizontals = elements
    .filter((element) => /^h\d+$/.test(tableSuffix(sourceId(element), base)) && (element.type === "line" || element.type === "rect"))
    .map((element) =>
      element.type === "line"
        ? numberValue(element.attributes.y1, y)
        : numberValue(element.attributes.y, y) + numberValue(element.attributes.height, 0) / 2,
    )
    .sort((a, b) => a - b);

  const columnEdges = [x, ...verticals, x + width];
  const rowEdges = [y, ...horizontals, y + height];
  return {
    id: base,
    type: "table",
    x,
    y,
    props: {
      columnWidths: edgesToSpans(columnEdges),
      rowHeights: edgesToSpans(rowEdges),
      cells: elements.flatMap((element) => rendererElementToTableCell(base, element)),
      fill: stringValue(attrs.fill, "#ffffff"),
      stroke: stringValue(attrs.stroke, "#111827"),
      strokeWidth: numberValue(attrs["stroke-width"], 1),
      sourceSlotIds: elements.map((element) => sourceId(element)),
      dividerKinds: Object.fromEntries(
        elements
          .filter((element) => /^[vh]\d+$/.test(tableSuffix(sourceId(element), base)))
          .map((element) => [sourceId(element), element.type === "rect" ? "rect" : "line"]),
      ),
    },
  };
}

function layoutTableGroupToProblemObject(base: string, slots: LayoutSlot[]): ProblemObject | null {
  const outer = slots.find((slot) => slot.id === `${base}.outer` && slot.kind === "rect");
  if (!outer) return null;
  const content = outer.content;
  const x = numberValue(content.x, 0);
  const y = numberValue(content.y, 0);
  const width = numberValue(content.width, 1);
  const height = numberValue(content.height, 1);
  const verticals = slots
    .filter((slot) => /^v\d+$/.test(tableSuffix(slot.id, base)) && (slot.kind === "line" || slot.kind === "rect"))
    .map((slot) =>
      slot.kind === "line"
        ? numberValue(slot.content.x1, x)
        : numberValue(slot.content.x, x) + numberValue(slot.content.width, 0) / 2,
    )
    .sort((a, b) => a - b);
  const horizontals = slots
    .filter((slot) => /^h\d+$/.test(tableSuffix(slot.id, base)) && (slot.kind === "line" || slot.kind === "rect"))
    .map((slot) =>
      slot.kind === "line"
        ? numberValue(slot.content.y1, y)
        : numberValue(slot.content.y, y) + numberValue(slot.content.height, 0) / 2,
    )
    .sort((a, b) => a - b);

  const columnEdges = [x, ...verticals, x + width];
  const rowEdges = [y, ...horizontals, y + height];
  return {
    id: base,
    type: "table",
    x,
    y,
    props: {
      columnWidths: edgesToSpans(columnEdges),
      rowHeights: edgesToSpans(rowEdges),
      cells: slots.flatMap((slot) => layoutSlotToTableCell(base, slot)),
      fill: stringValue(content.fill, "#ffffff"),
      stroke: stringValue(content.stroke, "#111827"),
      strokeWidth: numberValue(content.stroke_width, 1),
      sourceSlotIds: slots.map((slot) => slot.id),
      dividerKinds: Object.fromEntries(
        slots
          .filter((slot) => /^[vh]\d+$/.test(tableSuffix(slot.id, base)))
          .map((slot) => [slot.id, slot.kind === "rect" ? "rect" : "line"]),
      ),
    },
  };
}

function rendererElementToProblemObject(problemId: string, element: RendererElement): ProblemObject[] {
  const attrs = element.attributes;
  switch (element.type) {
    case "text": {
      const text = stringValue(element.text, "");
      if (!text) return [];
      const fontSize = numberValue(attrs["font-size"], 28);
      const width = textWidthEstimate(text, fontSize, optionalNumberValue(attrs.max_width));
      const height = Math.max(24, fontSize * 1.25);
      const anchor = stringValue(attrs["text-anchor"], "start");
      const x = numberValue(attrs.x, 0) - (anchor === "middle" ? width / 2 : anchor === "end" ? width : 0);
      const y = numberValue(attrs.y, 0) - fontSize;
      return [
        {
          id: sourceId(element),
          type: "math_text",
          x,
          y,
          props: {
            latex: text,
            text,
            fontSize,
            width,
            height,
            color: stringValue(attrs.fill, "#111111"),
            textAlign: anchor === "middle" ? "center" : anchor === "end" ? "right" : "left",
            lineHeight: 1.2,
            sourceKind: "text",
          },
        },
      ];
    }
    case "rect":
      return [
        {
          id: sourceId(element),
          type: "basic_shape",
          x: numberValue(attrs.x, 0),
          y: numberValue(attrs.y, 0),
          props: {
            shape: "rectangle",
            width: numberValue(attrs.width, 120),
            height: numberValue(attrs.height, 80),
            fill: stringValue(attrs.fill, "transparent"),
            stroke: stringValue(attrs.stroke, "#111827"),
            strokeWidth: numberValue(attrs["stroke-width"], 1),
          },
        },
      ];
    case "line": {
      const x1 = numberValue(attrs.x1, 0);
      const y1 = numberValue(attrs.y1, 0);
      const x2 = numberValue(attrs.x2, x1);
      const y2 = numberValue(attrs.y2, y1);
      return [
        {
          id: sourceId(element),
          type: "basic_shape",
          x: Math.min(x1, x2),
          y: Math.min(y1, y2),
          props: {
            shape: "line",
            width: Math.abs(x2 - x1),
            height: Math.abs(y2 - y1),
            stroke: stringValue(attrs.stroke, "#111827"),
            strokeWidth: numberValue(attrs["stroke-width"], 1),
          },
        },
      ];
    }
    case "image": {
      const href = stringValue(attrs.href, stringValue(attrs["xlink:href"], ""));
      return [
        {
          id: sourceId(element),
          type: "image",
          x: numberValue(attrs.x, 0),
          y: numberValue(attrs.y, 0),
          props: {
            src: resolveProblemAssetUrl(problemId, href),
            width: numberValue(attrs.width, 120),
            height: numberValue(attrs.height, 80),
            alt: sourceId(element),
          },
        },
      ];
    }
    case "path": {
      const path = localizePathData(stringValue(attrs.d, ""));
      return [
        {
          id: sourceId(element),
          type: "path",
          x: path.x,
          y: path.y,
          props: {
            d: path.d,
            width: path.width,
            height: path.height,
            fill: stringValue(attrs.fill, "none"),
            stroke: stringValue(attrs.stroke, "#111827"),
            strokeWidth: numberValue(attrs["stroke-width"], 1),
          },
        },
      ];
    }
    default:
      return [];
  }
}

function layoutSlotToProblemObject(problemId: string, slot: LayoutSlot): ProblemObject[] {
  const content = slot.content;
  switch (slot.kind) {
    case "text": {
      const text = stringValue(content.text, slot.id);
      const fontSize = numberValue(content.font_size, 28);
      const width = numberValue(content.max_width, textWidthEstimate(text, fontSize));
      const anchor = stringValue(content.anchor, "start");
      const x = numberValue(content.x, 0) - (anchor === "middle" ? width / 2 : anchor === "end" ? width : 0);
      const y = numberValue(content.y, 0) - fontSize;
      return [
        {
          id: slot.id,
          type: "math_text",
          x,
          y,
          props: {
            latex: text,
            text,
            fontSize,
            width,
            height: Math.max(24, fontSize * 1.2),
            color: stringValue(content.fill, "#111111"),
            textAlign: anchor === "middle" ? "center" : anchor === "end" ? "right" : "left",
            lineHeight: 1.2,
            sourceKind: "text",
          },
        },
      ];
    }
    case "text_box": {
      const text = stringValue(content.text, slot.id);
      const x = numberValue(content.x, 0);
      const y = numberValue(content.y, 0);
      return [
        {
          id: slot.id,
          type: "math_text",
          x,
          y,
          props: {
            latex: text,
            text,
            fontSize: numberValue(content.font_size, 28),
            width: numberValue(content.width, 280),
            height: numberValue(content.height, 48),
            color: stringValue(content.fill, "#111111"),
            textAlign: stringValue(content.anchor, "start") === "middle" ? "center" : "left",
            lineHeight: numberValue(content.line_height, 1.25),
            sourceKind: "text_box",
          },
        },
      ];
    }
    case "rect":
      return [
        {
          id: slot.id,
          type: "basic_shape",
          x: numberValue(content.x, 0),
          y: numberValue(content.y, 0),
          props: {
            shape: "rectangle",
            width: numberValue(content.width, 120),
            height: numberValue(content.height, 80),
            fill: stringValue(content.fill, "none"),
            stroke: stringValue(content.stroke, "#111827"),
            strokeWidth: numberValue(content.stroke_width, 1),
          },
        },
      ];
    case "line": {
      const x1 = numberValue(content.x1, 0);
      const y1 = numberValue(content.y1, 0);
      const x2 = numberValue(content.x2, x1);
      const y2 = numberValue(content.y2, y1);
      return [
        {
          id: slot.id,
          type: "basic_shape",
          x: Math.min(x1, x2),
          y: Math.min(y1, y2),
          props: {
            shape: "line",
            width: Math.abs(x2 - x1),
            height: Math.abs(y2 - y1),
            stroke: stringValue(content.stroke, "#111827"),
            strokeWidth: numberValue(content.stroke_width, 1),
          },
        },
      ];
    }
    case "circle": {
      const r = numberValue(content.r, 40);
      const cx = numberValue(content.cx, r);
      const cy = numberValue(content.cy, r);
      return [
        {
          id: slot.id,
          type: "basic_shape",
          x: cx - r,
          y: cy - r,
          props: {
            shape: "ellipse",
            width: r * 2,
            height: r * 2,
            fill: stringValue(content.fill, "none"),
            stroke: stringValue(content.stroke, "#111827"),
          },
        },
      ];
    }
    case "image":
      return [
        {
          id: slot.id,
          type: "image",
          x: numberValue(content.x, 0),
          y: numberValue(content.y, 0),
          props: {
            src: resolveProblemAssetUrl(problemId, stringValue(content.href, "")),
            width: numberValue(content.width, 120),
            height: numberValue(content.height, 80),
          },
        },
      ];
    case "path": {
      const path = localizePathData(stringValue(content.d, ""));
      return [
        {
          id: slot.id,
          type: "path",
          x: path.x,
          y: path.y,
          props: {
            d: path.d,
            width: path.width,
            height: path.height,
            fill: stringValue(content.fill, "none"),
            stroke: stringValue(content.stroke, "#111827"),
            strokeWidth: numberValue(content.stroke_width, 1),
          },
        },
      ];
    }
    default:
      return [];
  }
}

function rendererElementToTableCell(base: string, element: RendererElement) {
  if (element.type !== "text") return [];
  const match = tableCellMatch(sourceId(element), base);
  if (!match) return [];
  return [
    {
      row: match.row,
      col: match.col,
      text: stringValue(element.text, ""),
      fontSize: numberValue(element.attributes["font-size"], 24),
      color: stringValue(element.attributes.fill, "#111827"),
    },
  ];
}

function layoutSlotToTableCell(base: string, slot: LayoutSlot) {
  if (slot.kind !== "text" && slot.kind !== "text_box") return [];
  const match = tableCellMatch(slot.id, base);
  if (!match) return [];
  return [
    {
      row: match.row,
      col: match.col,
      text: stringValue(slot.content.text, ""),
      fontSize: numberValue(slot.content.font_size, 24),
      color: stringValue(slot.content.fill, "#111827"),
    },
  ];
}

function tableBaseFromSlotId(slotId: string): string | null {
  const match = slotId.match(/^(slot\.table(?:_\d+)?)(?:\.|$)/);
  return match?.[1] ?? null;
}

function tableSuffix(slotId: string, base: string): string {
  return slotId.startsWith(`${base}.`) ? slotId.slice(base.length + 1) : "";
}

function tableCellMatch(slotId: string, base: string): { row: number; col: number } | null {
  const match = tableSuffix(slotId, base).match(/^r(\d+)c(\d+)$/);
  if (!match) return null;
  return { row: Number(match[1]), col: Number(match[2]) };
}

function edgesToSpans(edges: number[]): number[] {
  return edges.slice(0, -1).map((edge, index) => Math.max(1, edges[index + 1] - edge));
}

function numberValue(value: unknown, fallback: number): number {
  return typeof value === "number" && Number.isFinite(value) ? value : fallback;
}

function optionalNumberValue(value: unknown): number | undefined {
  return typeof value === "number" && Number.isFinite(value) ? value : undefined;
}

function textWidthEstimate(text: string, fontSize: number, maxWidth?: number): number {
  if (typeof maxWidth === "number" && Number.isFinite(maxWidth) && maxWidth > 0) return maxWidth;
  return Math.max(fontSize, text.length * fontSize * 0.72);
}

function stringValue(value: unknown, fallback: string): string {
  return typeof value === "string" ? value : fallback;
}

function sourceId(element: RendererElement): string {
  return element.source_ref || element.id.replace(/\.(text|rect|line|path|image)$/, "");
}

function resolveProblemAssetUrl(problemId: string, href: string): string {
  if (!href) return "";
  if (/^(?:data:|https?:|blob:)/i.test(href)) return href;
  if (href.includes("/") || href.includes("\\")) return href;
  return `/api/editor/assets/${encodeURIComponent(problemId)}/${encodeURIComponent(href)}`;
}
