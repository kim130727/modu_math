import type { Point } from "../model/geometry";

export function screenToSvgPoint(svg: SVGSVGElement, clientX: number, clientY: number): Point {
  const point = svg.createSVGPoint();
  point.x = clientX;
  point.y = clientY;
  const ctm = svg.getScreenCTM();
  if (!ctm) return { x: clientX, y: clientY };
  const mapped = point.matrixTransform(ctm.inverse());
  return { x: mapped.x, y: mapped.y };
}

