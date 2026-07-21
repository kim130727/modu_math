import type { ConnectorKind, ConnectorShape } from "../types/editorShape";

export interface ConnectorPathObject {
  x: number;
  y: number;
  width: number;
  height: number;
  d: string;
}

export function connectorKindForPreset(preset: string): ConnectorKind | null {
  if (preset === "arrow" || preset === "doubleArrow") return "straight";
  if (preset === "elbow" || preset === "elbowArrow" || preset === "elbowDoubleArrow") return "elbow";
  if (preset === "curvedConnector" || preset === "curvedArrow" || preset === "curvedDoubleArrow" || preset === "curve") return "curve";
  return null;
}

export function connectorArrowForPreset(preset: string): { arrowStart: boolean; arrowEnd: boolean } {
  return {
    arrowStart: preset === "doubleArrow" || preset === "elbowDoubleArrow" || preset === "curvedDoubleArrow",
    arrowEnd:
      preset === "arrow" ||
      preset === "doubleArrow" ||
      preset === "elbowArrow" ||
      preset === "elbowDoubleArrow" ||
      preset === "curvedArrow" ||
      preset === "curvedDoubleArrow",
  };
}

export function connectorPathData(shape: ConnectorShape, origin = { x: shape.x, y: shape.y }): string {
  const start = localToOrigin(shape, connectorStart(shape), origin);
  const end = localToOrigin(shape, connectorEnd(shape), origin);
  if (shape.kind === "elbow") {
    const control = localToOrigin(shape, connectorControl(shape), origin);
    const first = { x: start.x, y: control.y };
    const second = { x: end.x, y: control.y };
    return withArrowHeads(`M ${fmt(start.x)} ${fmt(start.y)} L ${fmt(first.x)} ${fmt(first.y)} L ${fmt(second.x)} ${fmt(second.y)} L ${fmt(end.x)} ${fmt(end.y)}`, [start, first, second, end], shape);
  }
  if (shape.kind === "curve") {
    const control = localToOrigin(shape, connectorControl(shape), origin);
    return withArrowHeads(`M ${fmt(start.x)} ${fmt(start.y)} Q ${fmt(control.x)} ${fmt(control.y)} ${fmt(end.x)} ${fmt(end.y)}`, [start, control, end], shape);
  }
  return withArrowHeads(`M ${fmt(start.x)} ${fmt(start.y)} L ${fmt(end.x)} ${fmt(end.y)}`, [start, end], shape);
}

export function connectorToPathObject(shape: ConnectorShape): ConnectorPathObject {
  const bounds = connectorBounds(shape, 12);
  return {
    ...bounds,
    d: connectorPathData(shape, { x: bounds.x, y: bounds.y }),
  };
}

export function connectorBounds(shape: ConnectorShape, padding = 6): { x: number; y: number; width: number; height: number } {
  const points = connectorKeyPoints(shape).map((point) => ({ x: shape.x + point.x, y: shape.y + point.y }));
  const xs = points.map((point) => point.x);
  const ys = points.map((point) => point.y);
  const minX = Math.min(...xs) - padding;
  const minY = Math.min(...ys) - padding;
  const maxX = Math.max(...xs) + padding;
  const maxY = Math.max(...ys) + padding;
  return { x: minX, y: minY, width: Math.max(1, maxX - minX), height: Math.max(1, maxY - minY) };
}

export function connectorControl(shape: ConnectorShape): { x: number; y: number } {
  if (shape.control) return shape.control;
  const start = connectorStart(shape);
  const end = connectorEnd(shape);
  if (shape.kind === "curve") {
    return { x: (start.x + end.x) / 2, y: (start.y + end.y) / 2 - Math.max(24, Math.hypot(end.x - start.x, end.y - start.y) * 0.2) };
  }
  return { x: (start.x + end.x) / 2, y: (start.y + end.y) / 2 };
}

export function connectorStart(shape: ConnectorShape): { x: number; y: number } {
  return shape.start;
}

export function connectorEnd(shape: ConnectorShape): { x: number; y: number } {
  return shape.end;
}

export function connectorKeyPoints(shape: ConnectorShape): { x: number; y: number }[] {
  const start = connectorStart(shape);
  const end = connectorEnd(shape);
  if (shape.kind === "straight") return [start, end];
  const control = connectorControl(shape);
  if (shape.kind === "elbow") return [start, { x: start.x, y: control.y }, control, { x: end.x, y: control.y }, end];
  return [start, control, end];
}

function localToOrigin(shape: ConnectorShape, point: { x: number; y: number }, origin: { x: number; y: number }): { x: number; y: number } {
  return { x: shape.x + point.x - origin.x, y: shape.y + point.y - origin.y };
}

function withArrowHeads(path: string, points: { x: number; y: number }[], shape: ConnectorShape): string {
  const parts = [path];
  if (shape.arrowEnd && points.length >= 2) parts.push(arrowHeadPath(points[points.length - 2], points[points.length - 1]));
  if (shape.arrowStart && points.length >= 2) parts.push(arrowHeadPath(points[1], points[0]));
  return parts.join(" ");
}

function arrowHeadPath(from: { x: number; y: number }, to: { x: number; y: number }): string {
  const angle = Math.atan2(to.y - from.y, to.x - from.x);
  const length = 11;
  const spread = Math.PI / 7;
  const left = {
    x: to.x - Math.cos(angle - spread) * length,
    y: to.y - Math.sin(angle - spread) * length,
  };
  const right = {
    x: to.x - Math.cos(angle + spread) * length,
    y: to.y - Math.sin(angle + spread) * length,
  };
  return `M ${fmt(to.x)} ${fmt(to.y)} L ${fmt(left.x)} ${fmt(left.y)} M ${fmt(to.x)} ${fmt(to.y)} L ${fmt(right.x)} ${fmt(right.y)}`;
}

function fmt(value: number): number {
  return Math.round(value * 100) / 100;
}
