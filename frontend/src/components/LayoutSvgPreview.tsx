import { For } from "solid-js";
import type { LayoutDocument, LayoutSlot } from "../types/layout";

interface LayoutSvgPreviewProps {
  layout: LayoutDocument;
}

export function LayoutSvgPreview(props: LayoutSvgPreviewProps) {
  const width = () => props.layout.canvas?.width ?? 900;
  const height = () => props.layout.canvas?.height ?? 420;
  const background = () => props.layout.canvas?.background ?? "#ffffff";

  return (
    <svg class="layout-svg-preview" xmlns="http://www.w3.org/2000/svg" width={width()} height={height()} viewBox={`0 0 ${width()} ${height()}`}>
      <rect x="0" y="0" width={width()} height={height()} fill={background()} />
      <For each={orderedSlots(props.layout)}>
        {(slot) => <SlotShape slot={slot} />}
      </For>
    </svg>
  );
}

function orderedSlots(layout: LayoutDocument): LayoutSlot[] {
  const slots = layout.slots ?? [];
  const byId = new Map(slots.map((slot) => [slot.id, slot]));
  const orderedIds = layout.regions?.flatMap((region) => region.slot_ids ?? []) ?? [];
  const ordered = orderedIds.map((id) => byId.get(id)).filter((slot): slot is LayoutSlot => Boolean(slot));
  const seen = new Set(ordered.map((slot) => slot.id));
  return [...ordered, ...slots.filter((slot) => !seen.has(slot.id))];
}

function SlotShape(props: { slot: LayoutSlot }) {
  const content = () => props.slot.content as Record<string, unknown>;

  switch (props.slot.kind) {
          case "text":
          case "text_box":
            return (
              <text
          id={props.slot.id}
          x={numberAttr(content().x, 0)}
          y={numberAttr(content().y, 0)}
                fill={stringAttr(content().fill, "#111111")}
                font-family="Noto Sans KR, sans-serif"
                font-size={numberAttr(content().font_size, 24)}
                text-anchor={stringAttr(content().align, undefined) === "center" ? "middle" : undefined}
                transform={stringAttr(content().transform, undefined)}
              >
                {stringAttr(content().text, "")}
              </text>
            );
          case "rect":
            return (
              <rect
          id={props.slot.id}
                x={numberAttr(content().x, 0)}
                y={numberAttr(content().y, 0)}
                width={numberAttr(content().width, 0)}
                height={numberAttr(content().height, 0)}
                rx={numberAttr(content().rx, undefined)}
                ry={numberAttr(content().ry, undefined)}
                fill={stringAttr(content().fill, "none")}
                stroke={stringAttr(content().stroke, "#111111")}
                stroke-width={numberAttr(content().stroke_width, 1)}
                stroke-dasharray={stringAttr(content().stroke_dasharray, undefined)}
                transform={stringAttr(content().transform, undefined)}
              />
            );
          case "circle":
            return (
              <circle
          id={props.slot.id}
                cx={numberAttr(content().cx, 0)}
                cy={numberAttr(content().cy, 0)}
                r={numberAttr(content().r, 0)}
                fill={stringAttr(content().fill, "none")}
                stroke={stringAttr(content().stroke, "#111111")}
                stroke-width={numberAttr(content().stroke_width, 1)}
                stroke-dasharray={stringAttr(content().stroke_dasharray, undefined)}
                transform={stringAttr(content().transform, undefined)}
              />
            );
          case "line":
            return (
              <line
          id={props.slot.id}
                x1={numberAttr(content().x1, 0)}
                y1={numberAttr(content().y1, 0)}
                x2={numberAttr(content().x2, 0)}
                y2={numberAttr(content().y2, 0)}
                stroke={stringAttr(content().stroke, "#111111")}
                stroke-width={numberAttr(content().stroke_width, 1)}
                stroke-dasharray={stringAttr(content().stroke_dasharray, undefined)}
                transform={stringAttr(content().transform, undefined)}
              />
            );
          case "polygon":
            return (
              <polygon
          id={props.slot.id}
                points={pointsAttr(content().points)}
                fill={stringAttr(content().fill, "none")}
                stroke={stringAttr(content().stroke, "#111111")}
                stroke-width={numberAttr(content().stroke_width, 1)}
                stroke-dasharray={stringAttr(content().stroke_dasharray, undefined)}
                transform={stringAttr(content().transform, undefined)}
              />
            );
          case "path":
            return (
              <path
          id={props.slot.id}
                d={stringAttr(content().d, "")}
                fill={stringAttr(content().fill, "none")}
                stroke={stringAttr(content().stroke, "#111111")}
                stroke-width={numberAttr(content().stroke_width, 1)}
                stroke-dasharray={stringAttr(content().stroke_dasharray, undefined)}
                transform={stringAttr(content().transform, undefined)}
              />
            );
          case "image":
            return (
              <image
          id={props.slot.id}
                href={stringAttr(content().href, "")}
                x={numberAttr(content().x, 0)}
                y={numberAttr(content().y, 0)}
                width={numberAttr(content().width, 0)}
                height={numberAttr(content().height, 0)}
                transform={stringAttr(content().transform, undefined)}
              />
            );
          default:
            return null;
  }
}

function numberAttr(value: unknown, fallback: number | undefined): string | undefined {
  const nextValue = typeof value === "number" && Number.isFinite(value) ? value : fallback;
  return nextValue === undefined ? undefined : String(nextValue);
}

function stringAttr(value: unknown, fallback: string | undefined): string | undefined {
  return typeof value === "string" ? value : fallback;
}

function pointsAttr(value: unknown): string {
  if (!Array.isArray(value)) return "";
  return value
    .filter((point): point is [number, number] => Array.isArray(point) && typeof point[0] === "number" && typeof point[1] === "number")
    .map(([x, y]) => `${x},${y}`)
    .join(" ");
}
