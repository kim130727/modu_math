import type { Editor, TLShape } from "tldraw";
import type { ProblemJson, ProblemObject } from "../../types/problem";
import { angleMarkerPath } from "../shapes/AngleMarkerShape";
import { CANVAS_FRAME_ID } from "../shapes/CanvasFrameShape";
import { speechBubblePath } from "../shapes/SpeechBubbleShape";
import type {
  AngleMarkerShape,
  FractionBarShape,
  GroupObjectsShape,
  LayoutImageShape,
  LayoutLineShape,
  LayoutPathShape,
  LayoutRectShape,
  MathTextShape,
  NumberLineShape,
  SpeechBubbleShape,
  TableShape,
} from "../shapes/types";

export function tldrawToProblemJson(editor: Editor, base: ProblemJson): ProblemJson {
  const frame = editor.getCurrentPageShapes().find((shape) => shape.id === `shape:${CANVAS_FRAME_ID}` && shape.type === "canvas_frame");
  const frameProps = frame?.props as { w?: number; h?: number } | undefined;
  const objects = editor
    .getCurrentPageShapesSorted()
    .map(tldrawShapeToProblemObject)
    .filter((object): object is ProblemObject => object !== null);

  return {
    ...base,
    canvas: {
      width: typeof frameProps?.w === "number" ? frameProps.w : base.canvas.width,
      height: typeof frameProps?.h === "number" ? frameProps.h : base.canvas.height,
    },
    objects,
  };
}

function tldrawShapeToProblemObject(shape: TLShape): ProblemObject | null {
  const id = shape.id.replace(/^shape:/, "");
  switch (shape.type) {
    case "math_text": {
      const mathShape = shape as MathTextShape;
      return {
        id,
        type: "math_text",
        x: shape.x,
        y: shape.y,
        props: {
          latex: mathShape.props.latex,
          text: mathShape.props.text,
          fontSize: mathShape.props.fontSize,
          width: mathShape.props.w,
          height: mathShape.props.h,
          color: mathShape.props.color,
          textAlign: mathShape.props.textAlign,
          lineHeight: mathShape.props.lineHeight,
          sourceKind: mathShape.props.sourceKind,
        },
      };
    }
    case "layout_rect": {
      const rectShape = shape as LayoutRectShape;
      return {
        id,
        type: "basic_shape",
        x: shape.x,
        y: shape.y,
        props: {
          shape: "rectangle",
          width: rectShape.props.w,
          height: rectShape.props.h,
          fill: rectShape.props.fill,
          stroke: rectShape.props.stroke,
          strokeWidth: rectShape.props.strokeWidth,
        },
      };
    }
    case "layout_line": {
      const lineShape = shape as LayoutLineShape;
      return {
        id,
        type: "basic_shape",
        x: shape.x,
        y: shape.y,
        props: {
          shape: "line",
          width: lineShape.props.w,
          height: lineShape.props.h,
          stroke: lineShape.props.stroke,
          strokeWidth: lineShape.props.strokeWidth,
        },
      };
    }
    case "layout_image": {
      const imageShape = shape as LayoutImageShape;
      return {
        id,
        type: "image",
        x: shape.x,
        y: shape.y,
        props: {
          src: imageShape.props.src,
          width: imageShape.props.w,
          height: imageShape.props.h,
          alt: imageShape.props.alt,
        },
      };
    }
    case "layout_path": {
      const pathShape = shape as LayoutPathShape;
      return {
        id,
        type: "path",
        x: shape.x,
        y: shape.y,
        props: {
          d: pathShape.props.d,
          width: pathShape.props.w,
          height: pathShape.props.h,
          fill: pathShape.props.fill,
          stroke: pathShape.props.stroke,
          strokeWidth: pathShape.props.strokeWidth,
        },
      };
    }
    case "fraction_bar": {
      const fractionShape = shape as FractionBarShape;
      return {
        id,
        type: "fraction_bar",
        x: shape.x,
        y: shape.y,
        props: {
          denominator: fractionShape.props.denominator,
          colored: fractionShape.props.colored,
          width: fractionShape.props.w,
          height: fractionShape.props.h,
        },
      };
    }
    case "number_line": {
      const numberLineShape = shape as NumberLineShape;
      return {
        id,
        type: "number_line",
        x: shape.x,
        y: shape.y,
        props: {
          start: numberLineShape.props.start,
          end: numberLineShape.props.end,
          step: numberLineShape.props.step,
          width: numberLineShape.props.w,
        },
      };
    }
    case "group_objects": {
      const groupShape = shape as GroupObjectsShape;
      return {
        id,
        type: "group_objects",
        x: shape.x,
        y: shape.y,
        props: {
          item: groupShape.props.item,
          groups: groupShape.props.groups,
          countPerGroup: groupShape.props.countPerGroup,
          gap: groupShape.props.gap,
        },
      };
    }
    case "table": {
      const tableShape = shape as TableShape;
      return {
        id,
        type: "table",
        x: shape.x,
        y: shape.y,
        props: {
          columnWidths: tableShape.props.columnWidths,
          rowHeights: tableShape.props.rowHeights,
          cells: tableShape.props.cells,
          fill: tableShape.props.fill,
          stroke: tableShape.props.stroke,
          strokeWidth: tableShape.props.strokeWidth,
          sourceSlotIds: tableShape.props.sourceSlotIds,
          dividerKinds: tableShape.props.dividerKinds,
        },
      };
    }
    case "speech_bubble": {
      const bubbleShape = shape as SpeechBubbleShape;
      return {
        id,
        type: "path",
        x: shape.x,
        y: shape.y,
        props: {
          d: speechBubblePath(bubbleShape.props.w, bubbleShape.props.h, bubbleShape.props.tailX, bubbleShape.props.tailY),
          width: bubbleShape.props.w,
          height: Math.max(bubbleShape.props.h, bubbleShape.props.tailY),
          fill: bubbleShape.props.fill,
          stroke: bubbleShape.props.stroke,
          strokeWidth: bubbleShape.props.strokeWidth,
        },
      };
    }
    case "angle_marker": {
      const angleShape = shape as AngleMarkerShape;
      return {
        id,
        type: "path",
        x: shape.x,
        y: shape.y,
        props: {
          d: angleMarkerPath(angleShape.props.w, angleShape.props.h, angleShape.props.radius),
          width: angleShape.props.w,
          height: angleShape.props.h,
          fill: "none",
          stroke: angleShape.props.stroke,
          strokeWidth: angleShape.props.strokeWidth,
        },
      };
    }
    case "canvas_frame":
      return null;
    case "geo": {
      const props = shape.props as { geo?: string; w?: number; h?: number };
      return {
        id,
        type: "basic_shape",
        x: shape.x,
        y: shape.y,
        props: {
          shape: props.geo === "ellipse" ? "ellipse" : "rectangle",
          width: props.w ?? 100,
          height: props.h ?? 100,
        },
      };
    }
    case "image":
      // TODO: map tldraw image assets back to canonical image objects.
      return null;
    default:
      return null;
  }
}
