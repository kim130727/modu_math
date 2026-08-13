import type { EditorShape, EditorShapeDocument, InputInteraction, InputStyle } from "../types/editorShape";
import type { ProblemCanvas, ProblemJson, ProblemObject } from "../types/problem";
import { connectorToPathObject } from "./connectorGeometry";
import { KONVA_PREVIEW_FONT_FAMILY } from "./fonts";
import { inferAdjustableShapePreset, pathDataForShape } from "./shapeGeometry";

export function problemJsonToEditorDocument(problem: ProblemJson): EditorShapeDocument {
  return {
    id: problem.id,
    title: problem.title,
    canvas: problem.canvas,
    shapes: problem.objects.flatMap((object) => problemObjectToEditorShape(object, problem.canvas)),
  };
}

export function editorDocumentToProblemJson(document: EditorShapeDocument, base: ProblemJson): ProblemJson {
  const editedObjects = document.shapes.flatMap(editorShapeToProblemObject);
  const editedIds = new Set(editedObjects.map((object) => object.id));
  const preservedObjects = base.objects.filter((object) => !editedIds.has(object.id) && !isSupportedProblemObject(object));

  return {
    ...base,
    id: document.id,
    title: document.title,
    canvas: document.canvas,
    objects: [...preservedObjects, ...editedObjects],
  };
}

function problemObjectToEditorShape(object: ProblemObject, canvas: ProblemCanvas): EditorShape[] {
  const answerProps = answerSlotProps(object.props);
  const regionProps = sourceRegionProps(object.props);
  switch (object.type) {
    case "math_text": {
      const text = object.props.latex || object.props.text;
      const fontSize = object.props.fontSize;
      const isTextBox = object.props.sourceKind === "text_box";
      const textAlign = object.props.textAlign ?? "left";
      const lineHeight = object.props.lineHeight ?? 1.25;
      const needsAlignmentBox = textAlign !== "left";
      const sourceWidth = object.props.width ?? estimateTextWidth(text, fontSize);
      const maxWidth = maxTextBoxWidthWithinCanvas(object.x, canvas.width);
      const width = isTextBox || needsAlignmentBox ? normalizedTextBoxWidth(text, fontSize, sourceWidth, textAlign, maxWidth) : undefined;
      const fittedHeight = fittedTextHeight(text, fontSize, width ?? estimateTextWidth(text, fontSize), lineHeight);

      return [
        applySvgRotateTransform(
          {
          id: object.id,
          type: "text",
          x: object.x,
          y: object.y,
          text,
          fontSize,
          fontFamily: stringProp(object.props.fontFamily) ?? KONVA_PREVIEW_FONT_FAMILY,
          fill: object.props.color ?? "#111827",
          width,
          height: isTextBox ? normalizedTextBoxHeight(text, fontSize, width ?? estimateTextWidth(text, fontSize), object.props.height, lineHeight) : undefined,
          align: textAlign,
          lineHeight,
          sourceKind: object.props.sourceKind ?? "text",
          ...regionProps,
          ...answerProps,
          visible: true,
          },
          stringProp(object.props.transform),
        ),
      ];
    }
    case "basic_shape":
      if (object.props.shape === "ellipse") {
        return [
          applySvgRotateTransform(
            {
            id: object.id,
            type: "circle",
            x: object.x + object.props.width / 2,
            y: object.y + object.props.height / 2,
            radius: Math.min(object.props.width, object.props.height) / 2,
            fill: object.props.fill ?? "transparent",
            stroke: object.props.stroke ?? "#111827",
            strokeWidth: object.props.strokeWidth ?? 1,
            strokeDasharray: object.props.strokeDasharray,
            ...regionProps,
            ...answerProps,
            visible: true,
            },
            stringProp(object.props.transform),
          ),
        ];
      }
      if (object.props.shape === "line") {
        return [
          applySvgRotateTransform(
            {
            id: object.id,
            type: "line",
            x: object.x,
            y: object.y,
            points: [0, 0, object.props.width, object.props.height],
            stroke: object.props.stroke ?? "#111827",
            strokeWidth: object.props.strokeWidth ?? 1,
            strokeDasharray: object.props.strokeDasharray,
            ...regionProps,
            ...answerProps,
            visible: true,
            },
            stringProp(object.props.transform),
          ),
        ];
      }
      return [
        applySvgRotateTransform(
          {
          id: object.id,
          type: "rect",
          x: object.x,
          y: object.y,
          width: object.props.width,
          height: object.props.height,
          fill: object.props.fill ?? "transparent",
          stroke: object.props.stroke ?? "#111827",
          strokeWidth: object.props.strokeWidth ?? 1,
          strokeDasharray: object.props.strokeDasharray,
          shapePreset: stringProp(object.props.shapePreset) ?? inferAdjustableShapePreset({
            id: object.id,
            type: "path",
            x: object.x,
            y: object.y,
            d: stringProp(object.props.d) ?? "",
            width: object.props.width,
            height: object.props.height,
          }),
          adjustment: pointProp(object.props.adjustment),
          ...regionProps,
          ...answerProps,
          visible: true,
          },
          stringProp(object.props.transform),
        ),
      ];
    case "image":
      return [
        applySvgRotateTransform(
          {
          id: object.id,
          type: "image",
          x: object.x,
          y: object.y,
          src: object.props.src,
          width: object.props.width,
          height: object.props.height,
          preserveAspectRatio: object.props.preserveAspectRatio ?? "xMidYMid meet",
          ...regionProps,
          ...answerProps,
          visible: true,
          },
          stringProp(object.props.transform),
        ),
      ];
    case "path":
      if (object.props.connectorKind === "straight" || object.props.connectorKind === "elbow" || object.props.connectorKind === "curve") {
        return [
          {
            id: object.id,
            type: "connector",
            kind: object.props.connectorKind,
            x: numberProp(object.props.connectorX, object.x),
            y: numberProp(object.props.connectorY, object.y),
            start: pointProp(object.props.connectorStart) ?? { x: 0, y: 0 },
            end: pointProp(object.props.connectorEnd) ?? { x: object.props.width, y: object.props.height },
            control: pointProp(object.props.connectorControl),
            arrowStart: booleanProp(object.props.connectorArrowStart),
            arrowEnd: booleanProp(object.props.connectorArrowEnd),
            stroke: object.props.stroke ?? "#111827",
            strokeWidth: object.props.strokeWidth ?? 1,
            strokeDasharray: object.props.strokeDasharray,
            ...regionProps,
            ...answerProps,
            visible: true,
          },
        ];
      }
      return [
        applySvgRotateTransform(
          {
          id: object.id,
          type: "path",
          x: object.x,
          y: object.y,
          d: object.props.d,
          width: object.props.width,
          height: object.props.height,
          fill: object.props.fill ?? "transparent",
          stroke: object.props.stroke ?? "#111827",
          strokeWidth: object.props.strokeWidth ?? 1,
          strokeDasharray: object.props.strokeDasharray,
          shapePreset: stringProp(object.props.shapePreset),
          adjustment: pointProp(object.props.adjustment),
          ...regionProps,
          ...answerProps,
          visible: true,
          },
          stringProp(object.props.transform),
        ),
      ];
    default:
      return [];
  }
}

function stringProp(value: unknown): string | undefined {
  return typeof value === "string" && value.trim() ? value : undefined;
}

function numberProp(value: unknown, fallback: number): number {
  return typeof value === "number" && Number.isFinite(value) ? value : fallback;
}

function booleanProp(value: unknown): boolean | undefined {
  return typeof value === "boolean" ? value : undefined;
}

function pointProp(value: unknown): { x: number; y: number } | undefined {
  if (!value || typeof value !== "object" || Array.isArray(value)) return undefined;
  const point = value as Record<string, unknown>;
  return typeof point.x === "number" && Number.isFinite(point.x) && typeof point.y === "number" && Number.isFinite(point.y)
    ? { x: point.x, y: point.y }
    : undefined;
}

function answerSlotProps(props: Record<string, unknown>): { interaction?: InputInteraction; input_style?: InputStyle } {
  const interaction = recordProp(props.interaction);
  const inputStyle = recordProp(props.input_style);
  return {
    ...(interaction ? { interaction: interaction as unknown as InputInteraction } : {}),
    ...(inputStyle ? { input_style: inputStyle as unknown as InputStyle } : {}),
  };
}

function sourceRegionProps(props: Record<string, unknown>): { sourceRegionId?: string } {
  const sourceRegionId = stringProp(props.sourceRegionId);
  return sourceRegionId ? { sourceRegionId } : {};
}

function answerShapeProps(shape: EditorShape): { interaction?: InputInteraction; input_style?: InputStyle } {
  return {
    ...(shape.interaction ? { interaction: shape.interaction } : {}),
    ...(shape.input_style ? { input_style: shape.input_style } : {}),
  };
}

function sourceRegionShapeProps(shape: EditorShape): { sourceRegionId?: string } {
  return shape.sourceRegionId ? { sourceRegionId: shape.sourceRegionId } : {};
}

function recordProp(value: unknown): Record<string, unknown> | undefined {
  return value && typeof value === "object" && !Array.isArray(value) ? (value as Record<string, unknown>) : undefined;
}

function applySvgRotateTransform<T extends EditorShape>(shape: T, transform: string | undefined): T {
  const rotate = parseSvgRotate(transform);
  if (!rotate) return shape;
  return {
    ...shape,
    x: rotate.cx,
    y: rotate.cy,
    rotation: (shape.rotation ?? 0) + rotate.angle,
    offsetX: rotate.cx - shape.x,
    offsetY: rotate.cy - shape.y,
  };
}

function parseSvgRotate(transform: string | undefined): { angle: number; cx: number; cy: number } | null {
  if (!transform) return null;
  const match = transform.match(/^\s*rotate\(\s*([-+]?(?:\d*\.\d+|\d+)(?:e[-+]?\d+)?)\s+([-+]?(?:\d*\.\d+|\d+)(?:e[-+]?\d+)?)\s+([-+]?(?:\d*\.\d+|\d+)(?:e[-+]?\d+)?)\s*\)\s*$/i);
  if (!match) return null;
  const angle = Number(match[1]);
  const cx = Number(match[2]);
  const cy = Number(match[3]);
  return Number.isFinite(angle) && Number.isFinite(cx) && Number.isFinite(cy) ? { angle, cx, cy } : null;
}

function isSupportedProblemObject(object: ProblemObject): boolean {
  return object.type === "math_text" || object.type === "basic_shape" || object.type === "image" || object.type === "path";
}

function editorShapeToProblemObject(shape: EditorShape): ProblemObject[] {
  const answerProps = answerShapeProps(shape);
  const regionProps = sourceRegionShapeProps(shape);
  switch (shape.type) {
    case "math":
      return [
        {
          id: shape.id,
          type: "math_text",
          x: shapeBaseX(shape),
          y: shapeBaseY(shape),
          props: {
            latex: shape.latex,
            text: shape.latex,
            fontSize: shape.fontSize ?? 28,
            width: shape.width,
            height: shape.height,
            color: "#111827",
            textAlign: "left",
            lineHeight: 1.25,
            sourceKind: "text_box",
            ...regionProps,
            ...answerProps,
            ...transformProps(shape),
          },
        },
      ];
    case "text":
      const sourceKind = shape.sourceKind ?? (shape.width ? "text_box" : "text");
      const lineHeight = shape.lineHeight ?? 1.25;
      const width =
        sourceKind === "text_box" && typeof shape.width === "number"
          ? normalizedTextBoxWidth(shape.text, shape.fontSize, shape.width, shape.align ?? "left")
          : shape.width;
      const height =
        sourceKind === "text_box" && typeof width === "number"
          ? normalizedTextBoxHeight(shape.text, shape.fontSize, width, shape.height, lineHeight)
          : shape.height;
      return [
        {
          id: shape.id,
          type: "math_text",
          x: shapeBaseX(shape),
          y: shapeBaseY(shape),
          props: {
            latex: shape.text,
            text: shape.text,
            fontSize: shape.fontSize,
            fontFamily: shape.fontFamily ?? KONVA_PREVIEW_FONT_FAMILY,
            width,
            height,
            color: shape.fill ?? "#111827",
            textAlign: shape.align ?? "left",
            lineHeight,
            sourceKind,
            ...regionProps,
            ...answerProps,
            ...transformProps(shape),
          },
        },
      ];
    case "rect":
      return [
        {
          id: shape.id,
          type: "basic_shape",
          x: shapeBaseX(shape),
          y: shapeBaseY(shape),
          props: {
            shape: "rectangle",
            width: shape.width,
            height: shape.height,
            fill: shape.fill ?? "none",
            stroke: shape.stroke ?? "#111827",
            strokeWidth: shape.strokeWidth ?? 1,
            strokeDasharray: shape.strokeDasharray,
            ...regionProps,
            ...answerProps,
            ...transformProps(shape),
          },
        },
      ];
    case "circle":
      return [
        {
          id: shape.id,
          type: "basic_shape",
          x: shapeBaseX(shape) - shape.radius,
          y: shapeBaseY(shape) - shape.radius,
          props: {
            shape: "ellipse",
            width: shape.radius * 2,
            height: shape.radius * 2,
            fill: shape.fill ?? "none",
            stroke: shape.stroke ?? "#111827",
            strokeWidth: shape.strokeWidth ?? 1,
            strokeDasharray: shape.strokeDasharray,
            ...regionProps,
            ...answerProps,
            ...transformProps(shape),
          },
        },
      ];
    case "line":
      return [
        {
          id: shape.id,
          type: "basic_shape",
          x: shapeBaseX(shape),
          y: shapeBaseY(shape),
          props: {
            shape: "line",
            width: shape.points[2] ?? 0,
            height: shape.points[3] ?? 0,
            stroke: shape.stroke ?? "#111827",
            strokeWidth: shape.strokeWidth ?? 1,
            strokeDasharray: shape.strokeDasharray,
            ...regionProps,
            ...answerProps,
            ...transformProps(shape),
          },
        },
      ];
    case "connector": {
      const path = connectorToPathObject(shape);
      return [
        {
          id: shape.id,
          type: "path",
          x: path.x,
          y: path.y,
          props: {
            d: path.d,
            width: path.width,
            height: path.height,
            fill: "none",
            stroke: shape.stroke ?? "#111827",
            strokeWidth: shape.strokeWidth ?? 1,
            strokeDasharray: shape.strokeDasharray,
            connectorKind: shape.kind,
            connectorX: shape.x,
            connectorY: shape.y,
            connectorStart: shape.start,
            connectorEnd: shape.end,
            connectorControl: shape.control,
            connectorArrowStart: Boolean(shape.arrowStart),
            connectorArrowEnd: Boolean(shape.arrowEnd),
            ...regionProps,
            ...answerProps,
          },
        },
      ];
    }
    case "path":
      return [
        {
          id: shape.id,
          type: "path",
          x: shapeBaseX(shape),
          y: shapeBaseY(shape),
          props: {
            d: pathDataForShape(shape),
            width: shape.width,
            height: shape.height,
            fill: shape.fill ?? "none",
            stroke: shape.stroke ?? "#111827",
            strokeWidth: shape.strokeWidth ?? 1,
            strokeDasharray: shape.strokeDasharray,
            shapePreset: shape.shapePreset,
            adjustment: shape.adjustment,
            ...regionProps,
            ...answerProps,
            ...transformProps(shape),
          },
        },
      ];
    case "image":
      return [
        {
          id: shape.id,
          type: "image",
          x: shapeBaseX(shape),
          y: shapeBaseY(shape),
          props: {
            src: shape.src,
            width: shape.width,
            height: shape.height,
            preserveAspectRatio: shape.preserveAspectRatio,
            ...regionProps,
            ...answerProps,
            ...transformProps(shape),
          },
        },
      ];
    case "baseTenBlock":
      return baseTenBlockToProblemObjects(shape);
  }
}

function baseTenBlockToProblemObjects(shape: Extract<EditorShape, { type: "baseTenBlock" }>): ProblemObject[] {
  const stroke = shape.stroke ?? "#7ea86f";
  const strokeWidth = shape.strokeWidth ?? 0.8;
  const fill = shape.fill ?? "#b9dd9f";
  const topFill = shape.topFill ?? "#d2edbf";
  const sideFill = shape.sideFill ?? "#9fcd86";
  const depth = Math.max(0, Math.min(shape.depth, shape.width * 0.55, shape.height * 0.55));
  const frontY = depth;
  const grid = shape.kind === "one" ? 1 : 10;
  const objects: ProblemObject[] = [
    pathObject(`${shape.id}_top`, shape.x, shape.y, shape.width + depth, depth, `M 0 ${frontY} L ${depth} 0 L ${shape.width + depth} 0 L ${shape.width} ${frontY} Z`, topFill, stroke, strokeWidth),
    pathObject(
      `${shape.id}_side`,
      shape.x + shape.width,
      shape.y,
      depth,
      shape.height + depth,
      `M 0 ${frontY} L ${depth} 0 L ${depth} ${shape.height} L 0 ${shape.height + frontY} Z`,
      sideFill,
      stroke,
      strokeWidth,
    ),
    {
      id: `${shape.id}_front`,
      type: "basic_shape",
      x: shape.x,
      y: shape.y + frontY,
      props: {
        shape: "rectangle",
        width: shape.width,
        height: shape.height,
        fill,
        stroke,
        strokeWidth,
      },
    },
  ];

  if (grid > 1) {
    const segments: string[] = [];
    for (let i = 1; i < grid; i += 1) {
      const x = (shape.width / grid) * i;
      const y = frontY + (shape.height / grid) * i;
      const d = (depth / grid) * i;
      segments.push(segmentD(x, frontY, x, frontY + shape.height));
      segments.push(segmentD(0, y, shape.width, y));
      if (depth > 0) {
        segments.push(segmentD(d, frontY - d, shape.width + d, frontY - d));
        segments.push(segmentD(x, frontY, x + depth, 0));
        segments.push(segmentD(shape.width + d, frontY - d, shape.width + d, frontY - d + shape.height));
        segments.push(segmentD(shape.width, y, shape.width + depth, y - depth));
      }
    }
    objects.push(pathObject(`${shape.id}_grid`, shape.x, shape.y, shape.width + depth, shape.height + depth, segments.join(" "), "none", stroke, 0.38));
  }

  return objects;
}

function pathObject(
  id: string,
  x: number,
  y: number,
  width: number,
  height: number,
  d: string,
  fill: string,
  stroke: string,
  strokeWidth: number,
): ProblemObject {
  return {
    id,
    type: "path",
    x,
    y,
    props: {
      d,
      width,
      height,
      fill,
      stroke,
      strokeWidth,
    },
  };
}

function segmentD(x1: number, y1: number, x2: number, y2: number): string {
  return `M ${roundForTransform(x1)} ${roundForTransform(y1)} L ${roundForTransform(x2)} ${roundForTransform(y2)}`;
}

function shapeBaseX(shape: EditorShape): number {
  return shape.x - (shape.offsetX ?? 0);
}

function shapeBaseY(shape: EditorShape): number {
  return shape.y - (shape.offsetY ?? 0);
}

function transformProps(shape: EditorShape): { transform?: string } {
  const rotation = shape.rotation ?? 0;
  if (!rotation) return {};
  return { transform: `rotate(${roundForTransform(rotation)} ${roundForTransform(shape.x)} ${roundForTransform(shape.y)})` };
}

function roundForTransform(value: number): number {
  return Math.round(value * 1000) / 1000;
}

export function estimateTextWidth(text: string, fontSize: number): number {
  return Math.max(80, estimateLineWidth(text, fontSize));
}

export function fittedTextWidth(text: string, fontSize: number): number {
  return Math.max(12, Math.ceil(estimateLineWidth(text, fontSize) + fontSize * 0.28));
}

export function normalizedTextBoxWidth(text: string, fontSize: number, width?: number, align = "left", maxWidth?: number): number {
  const fittedWidth = fittedTextWidth(text, fontSize);
  const capped = (value: number) => Math.max(24, Math.min(value, maxWidth ?? value));
  if (typeof width !== "number" || !Number.isFinite(width)) return capped(fittedWidth);
  if (!text.trim() || align !== "left" || text.includes("\n")) return capped(width);
  if (maxWidth !== undefined && width > maxWidth) return capped(width);
  const suspiciouslyWide = width > Math.max(fittedWidth * 2.2, fittedWidth + fontSize * 2.5);
  return suspiciouslyWide ? capped(fittedWidth) : capped(width);
}

function maxTextBoxWidthWithinCanvas(x: number, canvasWidth: number): number {
  const margin = 16;
  return Math.max(24, canvasWidth - x - margin);
}

export function fittedTextHeight(text: string, fontSize: number, width: number, lineHeight = 1.25): number {
  return Math.max(24, Math.ceil(estimateWrappedLineCount(text, fontSize, width) * fontSize * lineHeight + 8));
}

export function normalizedTextBoxHeight(text: string, fontSize: number, width: number, height?: number, lineHeight = 1.25): number {
  const fittedHeight = fittedTextHeight(text, fontSize, width, lineHeight);
  if (typeof height !== "number" || !Number.isFinite(height)) return fittedHeight;
  if (!text.trim()) return Math.max(24, height);
  const suspiciouslyTall = height > Math.max(fittedHeight * 2.5, fittedHeight + fontSize * 2);
  return suspiciouslyTall ? fittedHeight : Math.max(height, fittedHeight);
}

export function estimateWrappedTextHeight(text: string, fontSize: number, width: number, lineHeight = 1.25): number {
  return fittedTextHeight(text, fontSize, width, lineHeight);
}

function estimateWrappedLineCount(text: string, fontSize: number, width: number): number {
  const usableWidth = Math.max(fontSize, width);
  return text
    .split(/\n/g)
    .map((line) => Math.max(1, Math.ceil(estimateLineWidth(line, fontSize) / usableWidth)))
    .reduce((total, lineCount) => total + lineCount, 0);
}

function estimateLineWidth(text: string, fontSize: number): number {
  let width = 0;
  for (const char of text) {
    if (char === " ") width += fontSize * 0.34;
    else if (/[\u1100-\u11ff\u3130-\u318f\uac00-\ud7af\u3400-\u9fff]/u.test(char)) width += fontSize;
    else if (/[\u2460-\u2473\u3260-\u327b]/u.test(char)) width += fontSize;
    else if (/[A-Z0-9]/u.test(char)) width += fontSize * 0.62;
    else if (/[a-z]/u.test(char)) width += fontSize * 0.54;
    else width += fontSize * 0.5;
  }
  return width;
}
