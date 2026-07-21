import type { PathShape } from "../types/editorShape";

export function pathDataForShape(shape: PathShape): string {
  const preset = shape.shapePreset ?? inferAdjustableShapePreset(shape);
  if (preset === "triangle") {
    const adjustment = shape.adjustment ?? { x: shape.width / 2, y: 8 };
    return `M ${fmt(adjustment.x)} ${fmt(adjustment.y)} L ${fmt(shape.width - 8)} ${fmt(shape.height - 8)} L 8 ${fmt(shape.height - 8)} Z`;
  }
  if (preset === "rightTriangle") {
    const adjustment = shape.adjustment ?? { x: shape.width - 12, y: 12 };
    return `M 20 10 L ${fmt(adjustment.x)} ${fmt(adjustment.y)} L 20 ${fmt(shape.height - 8)} Z`;
  }
  return shape.d;
}

export function adjustableShapePoint(shape: PathShape): { x: number; y: number } | null {
  const preset = shape.shapePreset ?? inferAdjustableShapePreset(shape);
  if (preset === "triangle") return shape.adjustment ?? { x: shape.width / 2, y: 8 };
  if (preset === "rightTriangle") return shape.adjustment ?? { x: shape.width - 12, y: 12 };
  return null;
}

export function inferAdjustableShapePreset(shape: PathShape): "triangle" | "rightTriangle" | null {
  const compact = shape.d.replace(/\s+/g, " ").trim();
  if (compact === "M90 8 L172 112 L8 112 Z") return "triangle";
  if (compact === "M20 10 L168 112 L20 112 Z") return "rightTriangle";
  return null;
}

function fmt(value: number): number {
  return Math.round(value * 100) / 100;
}
