import type { EditorShape, EditorShapeDocument } from "../types/editorShape";
import type { ProblemJson, ProblemObject } from "../types/problem";

export function problemJsonToEditorDocument(problem: ProblemJson): EditorShapeDocument {
  return {
    id: problem.id,
    title: problem.title,
    canvas: problem.canvas,
    shapes: problem.objects.flatMap(problemObjectToEditorShape),
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

function problemObjectToEditorShape(object: ProblemObject): EditorShape[] {
  switch (object.type) {
    case "math_text": {
      const text = object.props.latex || object.props.text;
      const fontSize = object.props.fontSize;
      const isTextBox = object.props.sourceKind === "text_box";
      const textAlign = object.props.textAlign ?? "left";
      const lineHeight = object.props.lineHeight ?? 1.25;
      const needsAlignmentBox = textAlign !== "left";
      const width = isTextBox || needsAlignmentBox ? object.props.width ?? estimateTextWidth(text, fontSize) : undefined;

      return [
        {
          id: object.id,
          type: "text",
          x: object.x,
          y: object.y,
          text,
          fontSize,
          fill: object.props.color ?? "#111827",
          width,
          height: isTextBox ? fittedTextHeight(text, fontSize, width ?? estimateTextWidth(text, fontSize), lineHeight) : undefined,
          align: textAlign,
          lineHeight,
          sourceKind: object.props.sourceKind ?? "text",
          visible: true,
        },
      ];
    }
    case "basic_shape":
      if (object.props.shape === "ellipse") {
        return [
          {
            id: object.id,
            type: "circle",
            x: object.x + object.props.width / 2,
            y: object.y + object.props.height / 2,
            radius: Math.min(object.props.width, object.props.height) / 2,
            fill: object.props.fill ?? "transparent",
            stroke: object.props.stroke ?? "#111827",
            strokeWidth: object.props.strokeWidth ?? 1,
            visible: true,
          },
        ];
      }
      if (object.props.shape === "line") {
        return [
          {
            id: object.id,
            type: "line",
            x: object.x,
            y: object.y,
            points: [0, 0, object.props.width, object.props.height],
            stroke: object.props.stroke ?? "#111827",
            strokeWidth: object.props.strokeWidth ?? 1,
            visible: true,
          },
        ];
      }
      return [
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
          visible: true,
        },
      ];
    case "image":
      return [
        {
          id: object.id,
          type: "image",
          x: object.x,
          y: object.y,
          src: object.props.src,
          width: object.props.width,
          height: object.props.height,
          preserveAspectRatio: object.props.preserveAspectRatio ?? "xMidYMid meet",
          visible: true,
        },
      ];
    case "path":
      return [
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
          visible: true,
        },
      ];
    default:
      return [];
  }
}

function isSupportedProblemObject(object: ProblemObject): boolean {
  return object.type === "math_text" || object.type === "basic_shape" || object.type === "image" || object.type === "path";
}

function editorShapeToProblemObject(shape: EditorShape): ProblemObject[] {
  switch (shape.type) {
    case "math":
      return [
        {
          id: shape.id,
          type: "math_text",
          x: shape.x,
          y: shape.y,
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
          },
        },
      ];
    case "text":
      return [
        {
          id: shape.id,
          type: "math_text",
          x: shape.x,
          y: shape.y,
          props: {
            latex: shape.text,
            text: shape.text,
            fontSize: shape.fontSize,
            width: shape.width,
            height: shape.height,
            color: shape.fill ?? "#111827",
            textAlign: shape.align ?? "left",
            lineHeight: shape.lineHeight ?? 1.25,
            sourceKind: shape.sourceKind ?? (shape.width ? "text_box" : "text"),
          },
        },
      ];
    case "rect":
      return [
        {
          id: shape.id,
          type: "basic_shape",
          x: shape.x,
          y: shape.y,
          props: {
            shape: "rectangle",
            width: shape.width,
            height: shape.height,
            fill: shape.fill ?? "none",
            stroke: shape.stroke ?? "#111827",
            strokeWidth: shape.strokeWidth ?? 1,
          },
        },
      ];
    case "circle":
      return [
        {
          id: shape.id,
          type: "basic_shape",
          x: shape.x - shape.radius,
          y: shape.y - shape.radius,
          props: {
            shape: "ellipse",
            width: shape.radius * 2,
            height: shape.radius * 2,
            fill: shape.fill ?? "none",
            stroke: shape.stroke ?? "#111827",
            strokeWidth: shape.strokeWidth ?? 1,
          },
        },
      ];
    case "line":
      return [
        {
          id: shape.id,
          type: "basic_shape",
          x: shape.x,
          y: shape.y,
          props: {
            shape: "line",
            width: shape.points[2] ?? 0,
            height: shape.points[3] ?? 0,
            stroke: shape.stroke ?? "#111827",
            strokeWidth: shape.strokeWidth ?? 1,
          },
        },
      ];
    case "path":
      return [
        {
          id: shape.id,
          type: "path",
          x: shape.x,
          y: shape.y,
          props: {
            d: shape.d,
            width: shape.width,
            height: shape.height,
            fill: shape.fill ?? "none",
            stroke: shape.stroke ?? "#111827",
            strokeWidth: shape.strokeWidth ?? 1,
          },
        },
      ];
    case "image":
      return [
        {
          id: shape.id,
          type: "image",
          x: shape.x,
          y: shape.y,
          props: {
            src: shape.src,
            width: shape.width,
            height: shape.height,
            preserveAspectRatio: shape.preserveAspectRatio,
          },
        },
      ];
  }
}

export function estimateTextWidth(text: string, fontSize: number): number {
  return Math.max(80, estimateLineWidth(text, fontSize));
}

export function fittedTextHeight(text: string, fontSize: number, width: number, lineHeight = 1.25): number {
  return Math.max(24, Math.ceil(estimateWrappedLineCount(text, fontSize, width) * fontSize * lineHeight + 8));
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
