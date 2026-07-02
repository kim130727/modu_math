export interface Point {
  x: number;
  y: number;
}

export interface Box {
  x: number;
  y: number;
  width: number;
  height: number;
}

export function formatNumber(value: unknown): string {
  return typeof value === "number" && Number.isFinite(value) ? String(Math.round(value * 100) / 100) : "";
}

