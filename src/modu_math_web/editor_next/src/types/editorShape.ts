export type EditorShape = RectShape | CircleShape | LineShape | PathShape | TextShape | ImageShape | MathShape;

export type BaseShape = {
  id: string;
  type: string;
  x: number;
  y: number;
  rotation?: number;
  offsetX?: number;
  offsetY?: number;
  opacity?: number;
  locked?: boolean;
  visible?: boolean;
};

export type RectShape = BaseShape & {
  type: "rect";
  width: number;
  height: number;
  fill?: string;
  stroke?: string;
  strokeWidth?: number;
  strokeDasharray?: string;
  cornerRadius?: number;
};

export type CircleShape = BaseShape & {
  type: "circle";
  radius: number;
  fill?: string;
  stroke?: string;
  strokeWidth?: number;
  strokeDasharray?: string;
};

export type LineShape = BaseShape & {
  type: "line";
  points: number[];
  stroke?: string;
  strokeWidth?: number;
  strokeDasharray?: string;
};

export type PathShape = BaseShape & {
  type: "path";
  d: string;
  width: number;
  height: number;
  fill?: string;
  stroke?: string;
  strokeWidth?: number;
  strokeDasharray?: string;
};

export type TextShape = BaseShape & {
  type: "text";
  text: string;
  fontSize: number;
  fontFamily?: string;
  fill?: string;
  width?: number;
  height?: number;
  align?: "left" | "center" | "right";
  lineHeight?: number;
  sourceKind?: "text" | "text_box";
};

export type ImageShape = BaseShape & {
  type: "image";
  src: string;
  width: number;
  height: number;
  preserveAspectRatio?: string;
};

export type MathShape = BaseShape & {
  type: "math";
  latex: string;
  width: number;
  height: number;
  fontSize?: number;
};

export interface EditorShapeDocument {
  id: string;
  title: string;
  canvas: {
    width: number;
    height: number;
  };
  shapes: EditorShape[];
}
