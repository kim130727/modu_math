import type { TLShape } from "tldraw";

declare module "tldraw" {
  export interface TLGlobalShapePropsMap {
    math_text: {
      latex: string;
      text: string;
      fontSize: number;
      w: number;
      h: number;
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
  }
}

export type MathTextShape = TLShape<"math_text">;
export type FractionBarShape = TLShape<"fraction_bar">;
export type NumberLineShape = TLShape<"number_line">;
export type GroupObjectsShape = TLShape<"group_objects">;

export type ModuMathShape = MathTextShape | FractionBarShape | NumberLineShape | GroupObjectsShape;
