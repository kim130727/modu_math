import type { TLShape } from "tldraw";

declare module "tldraw" {
  export interface TLGlobalShapePropsMap {
    math_text: {
      latex: string;
      text: string;
      fontSize: number;
      w: number;
      h: number;
      color: string;
      textAlign: "left" | "center" | "right";
      lineHeight: number;
      sourceKind: "text" | "text_box";
    };
    layout_rect: {
      w: number;
      h: number;
      fill: string;
      stroke: string;
      strokeWidth: number;
    };
    layout_line: {
      w: number;
      h: number;
      stroke: string;
      strokeWidth: number;
    };
    layout_image: {
      src: string;
      w: number;
      h: number;
      alt: string;
    };
    layout_path: {
      d: string;
      w: number;
      h: number;
      fill: string;
      stroke: string;
      strokeWidth: number;
    };
    fraction_bar: {
      denominator: number;
      colored: number;
      w: number;
      h: number;
    };
    number_line: {
      start: number;
      end: number;
      step: number;
      w: number;
      h: number;
    };
    group_objects: {
      item: "circle" | "square";
      groups: number;
      countPerGroup: number;
      gap: number;
      w: number;
      h: number;
    };
    table: {
      columnWidths: number[];
      rowHeights: number[];
      cells: Array<{
        row: number;
        col: number;
        text: string;
        fontSize: number;
        color: string;
      }>;
      fill: string;
      stroke: string;
      strokeWidth: number;
      sourceSlotIds: string[];
      dividerKinds: Record<string, "line" | "rect">;
    };
    speech_bubble: {
      w: number;
      h: number;
      tailX: number;
      tailY: number;
      fill: string;
      stroke: string;
      strokeWidth: number;
    };
    angle_marker: {
      w: number;
      h: number;
      radius: number;
      stroke: string;
      strokeWidth: number;
    };
    canvas_frame: {
      w: number;
      h: number;
      stroke: string;
      strokeWidth: number;
      fill: string;
    };
  }
}

export type MathTextShape = TLShape<"math_text">;
export type LayoutRectShape = TLShape<"layout_rect">;
export type LayoutLineShape = TLShape<"layout_line">;
export type LayoutImageShape = TLShape<"layout_image">;
export type LayoutPathShape = TLShape<"layout_path">;
export type FractionBarShape = TLShape<"fraction_bar">;
export type NumberLineShape = TLShape<"number_line">;
export type GroupObjectsShape = TLShape<"group_objects">;
export type TableShape = TLShape<"table">;
export type SpeechBubbleShape = TLShape<"speech_bubble">;
export type AngleMarkerShape = TLShape<"angle_marker">;
export type CanvasFrameShape = TLShape<"canvas_frame">;

export type ModuMathShape =
  | CanvasFrameShape
  | MathTextShape
  | LayoutRectShape
  | LayoutLineShape
  | LayoutImageShape
  | LayoutPathShape
  | FractionBarShape
  | NumberLineShape
  | GroupObjectsShape
  | TableShape
  | SpeechBubbleShape
  | AngleMarkerShape;
