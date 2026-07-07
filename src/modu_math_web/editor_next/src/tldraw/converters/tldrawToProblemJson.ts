import type { Editor, TLShape } from "tldraw";
import type { ProblemJson, ProblemObject } from "../../types/problem";
import type { FractionBarShape, GroupObjectsShape, MathTextShape, NumberLineShape } from "../shapes/types";

export function tldrawToProblemJson(editor: Editor, base: ProblemJson): ProblemJson {
  const objects = editor
    .getCurrentPageShapesSorted()
    .map(tldrawShapeToProblemObject)
    .filter((object): object is ProblemObject => object !== null);

  return {
    ...base,
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
