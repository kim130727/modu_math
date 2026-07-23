export type EditorShape = RectShape | CircleShape | LineShape | ConnectorShape | PathShape | TextShape | ImageShape | MathShape;

export type AnswerInteractionType = "input" | "select";
export type AnswerRole = "answer" | "result" | "intermediate" | "carry" | "blank" | "choice";
export type AnswerValueType = "digit" | "integer" | "decimal" | "fraction" | "text" | "choice" | "select";
export type AnswerKeyboard = "number" | "decimal" | "fraction" | "text" | "none";

export interface InputInteraction {
  type: AnswerInteractionType;
  role: AnswerRole;
  value_type: AnswerValueType;
  max_length?: number;
  include_in_submission?: boolean;
  order?: number;
  group_id?: string;
  choice_value?: string | number;
  placeholder?: string;
  auto_advance?: boolean;
  keyboard?: AnswerKeyboard;
}

export interface ContentInset {
  left?: number;
  top?: number;
  right?: number;
  bottom?: number;
}

export interface InputStyle {
  font_family?: string;
  font_size_mode?: "auto" | "fixed";
  font_size?: number;
  font_size_adjust?: number;
  min_font_size?: number;
  max_font_size?: number;
  font_weight?: number;
  horizontal_align?: "left" | "center" | "right";
  vertical_align?: "top" | "middle" | "bottom";
  padding?: number;
  text_color?: string;
  content_inset?: ContentInset;
}

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
  interaction?: InputInteraction;
  input_style?: InputStyle;
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

export type ConnectorKind = "straight" | "elbow" | "curve";

export type ConnectorShape = BaseShape & {
  type: "connector";
  kind: ConnectorKind;
  start: { x: number; y: number };
  end: { x: number; y: number };
  control?: { x: number; y: number };
  arrowStart?: boolean;
  arrowEnd?: boolean;
  stroke?: string;
  strokeWidth?: number;
  strokeDasharray?: string;
};

export type PathShape = BaseShape & {
  type: "path";
  d: string;
  width: number;
  height: number;
  shapePreset?: string;
  adjustment?: { x: number; y: number };
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
