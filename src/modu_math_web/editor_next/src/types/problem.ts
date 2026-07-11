export interface ProblemCanvas {
  width: number;
  height: number;
}

export type ProblemObject =
  | MathTextObject
  | FractionBarObject
  | NumberLineObject
  | GroupObjectsObject
  | TableObject
  | BasicShapeObject
  | PathObject
  | ImageObject;

export interface ProblemJson {
  id: string;
  title: string;
  canvas: ProblemCanvas;
  objects: ProblemObject[];
}

export interface BaseProblemObject<Type extends string, Props extends Record<string, unknown>> {
  id: string;
  type: Type;
  x: number;
  y: number;
  props: Props;
}

export interface MathTextProps extends Record<string, unknown> {
  latex: string;
  text: string;
  fontSize: number;
  width?: number;
  height?: number;
  color?: string;
  fontFamily?: string;
  textAlign?: "left" | "center" | "right";
  lineHeight?: number;
  sourceKind?: "text" | "text_box";
}

export type MathTextObject = BaseProblemObject<"math_text", MathTextProps>;

export interface FractionBarProps extends Record<string, unknown> {
  denominator: number;
  colored: number;
  width: number;
  height: number;
}

export type FractionBarObject = BaseProblemObject<"fraction_bar", FractionBarProps>;

export interface NumberLineProps extends Record<string, unknown> {
  start: number;
  end: number;
  step: number;
  width: number;
}

export type NumberLineObject = BaseProblemObject<"number_line", NumberLineProps>;

export interface GroupObjectsProps extends Record<string, unknown> {
  item: "circle" | "square";
  groups: number;
  countPerGroup: number;
  gap: number;
}

export type GroupObjectsObject = BaseProblemObject<"group_objects", GroupObjectsProps>;

export interface TableCell {
  row: number;
  col: number;
  text: string;
  fontSize: number;
  color: string;
}

export interface TableProps extends Record<string, unknown> {
  columnWidths: number[];
  rowHeights: number[];
  cells: TableCell[];
  fill?: string;
  stroke?: string;
  strokeWidth?: number;
  sourceSlotIds?: string[];
  dividerKinds?: Record<string, "line" | "rect">;
}

export type TableObject = BaseProblemObject<"table", TableProps>;

export interface BasicShapeProps extends Record<string, unknown> {
  shape: "rectangle" | "ellipse" | "line";
  width: number;
  height: number;
  fill?: string;
  stroke?: string;
  strokeWidth?: number;
  strokeDasharray?: string;
}

export type BasicShapeObject = BaseProblemObject<"basic_shape", BasicShapeProps>;

export interface PathProps extends Record<string, unknown> {
  d: string;
  width: number;
  height: number;
  fill?: string;
  stroke?: string;
  strokeWidth?: number;
  strokeDasharray?: string;
}

export type PathObject = BaseProblemObject<"path", PathProps>;

export interface ImageProps extends Record<string, unknown> {
  src: string;
  width: number;
  height: number;
  alt?: string;
  preserveAspectRatio?: string;
}

export type ImageObject = BaseProblemObject<"image", ImageProps>;
