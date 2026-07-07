import { createShapeId, toRichText, type TLCreateShapePartial, type TLShape } from "tldraw";
import type { ProblemJson, ProblemObject } from "../../types/problem";
import type { FractionBarShape, GroupObjectsShape, MathTextShape, NumberLineShape } from "../shapes/types";

export function problemJsonToTldrawShapes(problem: ProblemJson): TLCreateShapePartial<TLShape>[] {
  return problem.objects.map(problemObjectToShape).filter((shape): shape is TLCreateShapePartial<TLShape> => shape !== null);
}

function problemObjectToShape(object: ProblemObject): TLCreateShapePartial<TLShape> | null {
  const base = {
    id: createShapeId(object.id),
    x: object.x,
    y: object.y,
  };

  switch (object.type) {
    case "math_text":
      return {
        ...base,
        type: "math_text",
        props: {
          latex: object.props.latex,
          text: object.props.text,
          fontSize: object.props.fontSize,
          w: object.props.width ?? 280,
          h: object.props.height ?? Math.max(48, object.props.fontSize * 1.6),
        },
      } satisfies TLCreateShapePartial<MathTextShape>;
    case "fraction_bar":
      return {
        ...base,
        type: "fraction_bar",
        props: {
          denominator: object.props.denominator,
          colored: object.props.colored,
          w: object.props.width,
          h: object.props.height,
        },
      } satisfies TLCreateShapePartial<FractionBarShape>;
    case "number_line":
      return {
        ...base,
        type: "number_line",
        props: {
          start: object.props.start,
          end: object.props.end,
          step: object.props.step,
          w: object.props.width,
          h: 96,
        },
      } satisfies TLCreateShapePartial<NumberLineShape>;
    case "group_objects":
      return {
        ...base,
        type: "group_objects",
        props: {
          item: object.props.item,
          groups: object.props.groups,
          countPerGroup: object.props.countPerGroup,
          gap: object.props.gap,
          w: 320,
          h: 128,
        },
      } satisfies TLCreateShapePartial<GroupObjectsShape>;
    case "basic_shape":
      return {
        ...base,
        type: "geo",
        props: {
          geo: object.props.shape === "ellipse" ? "ellipse" : "rectangle",
          w: object.props.width,
          h: object.props.height,
          color: "black",
          fill: "none",
          richText: toRichText(""),
        },
      };
    case "image":
      // TODO: convert canonical image objects to tldraw image assets.
      return null;
  }
}
