import type { LayoutDocument } from "../../types/layout";
import type { RendererDocument, RendererElement } from "../../types/renderer";

export function toggleSelection(current: readonly string[], slotId: string, append: boolean): string[] {
  if (!append) return [slotId];
  return current.includes(slotId) ? current.filter((id) => id !== slotId) : [...current, slotId];
}

export function clearSelection(): string[] {
  return [];
}

export function isDraggableSlotElement(el: Element): boolean {
  if (!el) return false;
  if (
    el.classList &&
    (el.classList.contains("selection-handle") ||
      el.classList.contains("selection-bounds") ||
      el.classList.contains("selection-line") ||
      el.classList.contains("slot-hit-proxy"))
  ) {
    return false;
  }
  const tag = el.tagName.toLowerCase();
  return tag === "text" || tag === "rect" || tag === "image" || tag === "circle" || tag === "line" || tag === "path" || tag === "polygon";
}

export function fallbackSlotIdFromSvgId(svgElementId: string | null): string {
  if (!svgElementId) return "";
  const base = svgElementId
    .replace(/\.(text|line|rect|path|polygon|circle)$/i, "")
    .replace(/\.(image)$/i, "")
    .replace(/__(hit|proxy)$/i, "");
  if (!base || base === "selectionOverlay") return "";
  if (!base.startsWith("slot.")) return "";
  return base;
}

export function parseFractionPartId(svgElementId: string | null, layout: LayoutDocument | null): { prefix: string; part: string } | null {
  if (!svgElementId) return null;
  const base = svgElementId.replace(/\.(text|line|rect|path|polygon|circle|image)$/i, "");
  const m = base.match(/^(slot\..+)\.(whole|num|bar|den)$/);
  if (!m) return null;

  if (!layout) return null;
  const dslIds = new Set(layout.slots?.map((s) => s.id) ?? []);
  if (!dslIds.has(`${m[1]}.num`) || !dslIds.has(`${m[1]}.bar`) || !dslIds.has(`${m[1]}.den`)) return null;

  return { prefix: m[1], part: m[2] };
}

export function extractRendererSlotRefs(renderer: RendererDocument | null): Map<string, string[]> {
  const byElementId = new Map<string, string[]>();
  if (!renderer || !renderer.elements) return byElementId;

  const visit = (elements: RendererElement[]) => {
    for (const element of elements) {
      const id = typeof element?.id === "string" ? element.id : "";
      if (id) {
        const refs = element.refs && typeof element.refs === "object" ? element.refs : {};
        const candidates = [
          typeof refs.layout_slot_id === "string" ? refs.layout_slot_id : "",
          typeof element.source_ref === "string" ? element.source_ref : "",
        ].filter(Boolean);
        if (candidates.length) byElementId.set(id, candidates);
      }
      if (Array.isArray(element.elements)) {
        visit(element.elements);
      }
    }
  };
  visit(renderer.elements);
  return byElementId;
}

export function toDslSlotIds(
  svgElementId: string | null,
  layout: LayoutDocument | null,
  renderer: RendererDocument | null,
  dslSource: string
): string[] {
  if (!svgElementId) return [];

  const rendererSlotRefs = extractRendererSlotRefs(renderer);
  const rendererIds = rendererSlotRefs.get(svgElementId) || [];
  if (rendererIds.length) return rendererIds;

  const sourceIds = new Set<string>();
  const re = /\bid\s*=\s*["']([^"']+)["']/g;
  let m: RegExpExecArray | null = null;
  while ((m = re.exec(dslSource)) !== null) {
    sourceIds.add(m[1]);
  }

  if (sourceIds.has(svgElementId)) return [svgElementId];

  const parts = svgElementId.split(".");
  const sourceMatches: string[] = [];
  while (parts.length > 1) {
    parts.pop();
    const candidate = parts.join(".");
    if (sourceIds.has(candidate)) sourceMatches.push(candidate);
    const splitCandidates = Array.from(sourceIds)
      .filter((id) => id.startsWith(`${candidate}_`))
      .sort((a, b) => a.localeCompare(b, "ko"));
    if (splitCandidates.length > 0) return splitCandidates;
  }
  if (sourceMatches.length) return [sourceMatches[0]];

  const allIds = new Set(layout?.slots?.map((s) => s.id) ?? []);
  if (allIds.has(svgElementId)) return [svgElementId];

  const layoutParts = svgElementId.split(".");
  while (layoutParts.length > 1) {
    layoutParts.pop();
    const candidate = layoutParts.join(".");
    if (allIds.has(candidate)) return [candidate];
    const splitCandidates = Array.from(allIds)
      .filter((id) => id.startsWith(`${candidate}_`))
      .sort((a, b) => a.localeCompare(b, "ko"));
    if (splitCandidates.length > 0) return splitCandidates;
  }

  return [];
}

export function slotIdFromElement(
  el: Element,
  layout: LayoutDocument | null,
  renderer: RendererDocument | null,
  dslSource: string
): string {
  const rawId = el.getAttribute("id") || "";
  const fracInfo = parseFractionPartId(rawId, layout);
  if (fracInfo) return fracInfo.prefix;
  const ids = toDslSlotIds(rawId, layout, renderer, dslSource);
  return ids.length ? ids[0] : fallbackSlotIdFromSvgId(rawId);
}

export function matchSlotIdFromSvgElement(elementId: string | null, slotIds: readonly string[]): string | null {
  if (!elementId) return null;
  const sortedSlotIds = [...slotIds].sort((left, right) => right.length - left.length);
  return sortedSlotIds.find((slotId) => elementId === slotId || elementId.startsWith(`${slotId}.`)) ?? null;
}
