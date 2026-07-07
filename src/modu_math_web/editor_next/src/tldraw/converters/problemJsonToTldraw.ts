import { createShapeId, toRichText, type TLCreateShapePartial, type TLShape } from "tldraw";
import type { ProblemJson, ProblemObject } from "../../types/problem";
import type {
  CanvasFrameShape,
  FractionBarShape,
  GroupObjectsShape,
  LayoutImageShape,
  LayoutLineShape,
  LayoutPathShape,
  LayoutRectShape,
  MathTextShape,
  NumberLineShape,
  TableShape,
} from "../shapes/types";
import { CANVAS_FRAME_ID } from "../shapes/CanvasFrameShape";

export function problemJsonToTldrawShapes(problem: ProblemJson): TLCreateShapePartial<TLShape>[] {
  return [
    {
      id: createShapeId(CANVAS_FRAME_ID),
      type: "canvas_frame",
      x: 0,
      y: 0,
      props: {
        w: problem.canvas.width,
        h: problem.canvas.height,
        fill: "#ffffff",
        stroke: "#111827",
        strokeWidth: 1,
      },
    } satisfies TLCreateShapePartial<CanvasFrameShape>,
    ...problem.objects.map(problemObjectToShape).filter((shape): shape is TLCreateShapePartial<TLShape> => shape !== null),
  ];
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
          color: object.props.color ?? "#050816",
          textAlign: object.props.textAlign ?? "left",
          lineHeight: object.props.lineHeight ?? 1.25,
          sourceKind: object.props.sourceKind ?? "text_box",
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
    case "table":
      return {
        ...base,
        type: "table",
        props: {
          columnWidths: object.props.columnWidths,
          rowHeights: object.props.rowHeights,
          cells: object.props.cells,
          fill: object.props.fill ?? "#ffffff",
          stroke: object.props.stroke ?? "#111827",
          strokeWidth: object.props.strokeWidth ?? 1,
          sourceSlotIds: object.props.sourceSlotIds ?? [],
          dividerKinds: object.props.dividerKinds ?? {},
        },
      } satisfies TLCreateShapePartial<TableShape>;
    case "basic_shape":
      if (object.props.shape === "line") {
        return {
          ...base,
          type: "layout_line",
          props: {
            w: object.props.width,
            h: object.props.height,
            stroke: object.props.stroke ?? "#111827",
            strokeWidth: object.props.strokeWidth ?? 1,
          },
        } satisfies TLCreateShapePartial<LayoutLineShape>;
      }
      if (object.props.shape === "rectangle") {
        return {
          ...base,
          type: "layout_rect",
          props: {
            w: object.props.width,
            h: object.props.height,
            fill: object.props.fill ?? "transparent",
            stroke: object.props.stroke ?? "#111827",
            strokeWidth: object.props.strokeWidth ?? 1,
          },
        } satisfies TLCreateShapePartial<LayoutRectShape>;
      }
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
      return {
        ...base,
        type: "layout_image",
        props: {
          src: object.props.src,
          w: object.props.width,
          h: object.props.height,
          alt: object.props.alt ?? object.id,
        },
      } satisfies TLCreateShapePartial<LayoutImageShape>;
    case "path":
      return {
        ...base,
        type: "layout_path",
        props: {
          d: object.props.d,
          w: object.props.width,
          h: object.props.height,
          fill: object.props.fill ?? "none",
          stroke: object.props.stroke ?? "#111827",
          strokeWidth: object.props.strokeWidth ?? 1,
        },
      } satisfies TLCreateShapePartial<LayoutPathShape>;
  }
}
