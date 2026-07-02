import type { Box } from "../model/geometry";
import type { LayoutSlot } from "../../types/layout";

export function slotBounds(slot: LayoutSlot): Box | null {
  switch (slot.kind) {
    case "text": {
      const content = slot.content;
      return numberBox(content.x, content.y, content.max_width ?? 0, content.font_size ?? 0);
    }
    case "text_box":
    case "rect":
    case "image": {
      const content = slot.content;
      return numberBox(content.x, content.y, content.width, content.height);
    }
    case "circle": {
      const content = slot.content;
      if (typeof content.cx !== "number" || typeof content.cy !== "number" || typeof content.r !== "number") return null;
      return { x: content.cx - content.r, y: content.cy - content.r, width: content.r * 2, height: content.r * 2 };
    }
    case "line": {
      const content = slot.content;
      if (
        typeof content.x1 !== "number" ||
        typeof content.y1 !== "number" ||
        typeof content.x2 !== "number" ||
        typeof content.y2 !== "number"
      ) {
        return null;
      }
      return {
        x: Math.min(content.x1, content.x2),
        y: Math.min(content.y1, content.y2),
        width: Math.abs(content.x2 - content.x1),
        height: Math.abs(content.y2 - content.y1),
      };
    }
    case "polygon": {
      const points = slot.content.points;
      if (!Array.isArray(points) || points.length === 0) return null;
      const xs = points.map((point) => point[0]);
      const ys = points.map((point) => point[1]);
      const x = Math.min(...xs);
      const y = Math.min(...ys);
      return { x, y, width: Math.max(...xs) - x, height: Math.max(...ys) - y };
    }
    default:
      return null;
  }
}

function numberBox(x: unknown, y: unknown, width: unknown, height: unknown): Box | null {
  if (typeof x !== "number" || typeof y !== "number") return null;
  return {
    x,
    y,
    width: typeof width === "number" ? width : 0,
    height: typeof height === "number" ? height : 0,
  };
}
