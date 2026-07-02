export type LayoutSlot =
  | TextLayoutSlot
  | TextBoxLayoutSlot
  | RectLayoutSlot
  | CircleLayoutSlot
  | LineLayoutSlot
  | PolygonLayoutSlot
  | PathLayoutSlot
  | ImageLayoutSlot
  | UnknownLayoutSlot;

export interface LayoutDocument {
  schema?: string;
  problem_id?: string;
  title?: string;
  canvas?: LayoutCanvas;
  regions?: LayoutRegion[];
  slots?: LayoutSlot[];
}

export interface LayoutCanvas {
  width: number;
  height: number;
  coordinate_mode?: string;
  background?: string;
}

export interface LayoutRegion {
  id: string;
  role?: string;
  flow?: string;
  slot_ids?: string[];
}

interface BaseLayoutSlot<K extends string, C extends Record<string, unknown>> {
  id: string;
  kind: K;
  prompt?: string;
  content: C;
}

export interface TextLayoutSlot
  extends BaseLayoutSlot<
    "text",
    {
      text?: string;
      x?: number;
      y?: number;
      font_size?: number;
      max_width?: number;
      fill?: string;
      style_role?: string;
      transform?: string;
    }
  > {}

export interface TextBoxLayoutSlot
  extends BaseLayoutSlot<
    "text_box",
    {
      text?: string;
      x?: number;
      y?: number;
      width?: number;
      height?: number;
      font_size?: number;
      fill?: string;
      align?: string;
      valign?: string;
      style_role?: string;
      transform?: string;
    }
  > {}

export interface RectLayoutSlot
  extends BaseLayoutSlot<
    "rect",
    {
      x?: number;
      y?: number;
      width?: number;
      height?: number;
      fill?: string;
      stroke?: string;
      stroke_width?: number;
      stroke_dasharray?: string;
      rx?: number;
      ry?: number;
      transform?: string;
    }
  > {}

export interface CircleLayoutSlot
  extends BaseLayoutSlot<
    "circle",
    {
      cx?: number;
      cy?: number;
      r?: number;
      fill?: string;
      stroke?: string;
      stroke_width?: number;
      stroke_dasharray?: string;
      transform?: string;
    }
  > {}

export interface LineLayoutSlot
  extends BaseLayoutSlot<
    "line",
    {
      x1?: number;
      y1?: number;
      x2?: number;
      y2?: number;
      stroke?: string;
      stroke_width?: number;
      stroke_dasharray?: string;
      transform?: string;
    }
  > {}

export interface PolygonLayoutSlot
  extends BaseLayoutSlot<
    "polygon",
    {
      points?: [number, number][];
      fill?: string;
      stroke?: string;
      stroke_width?: number;
      stroke_dasharray?: string;
      transform?: string;
    }
  > {}

export interface PathLayoutSlot
  extends BaseLayoutSlot<
    "path",
    {
      d?: string;
      fill?: string;
      stroke?: string;
      stroke_width?: number;
      stroke_dasharray?: string;
      transform?: string;
    }
  > {}

export interface ImageLayoutSlot
  extends BaseLayoutSlot<
    "image",
    {
      href?: string;
      x?: number;
      y?: number;
      width?: number;
      height?: number;
      preserve_aspect_ratio?: string;
      transform?: string;
    }
  > {}

export interface UnknownLayoutSlot extends BaseLayoutSlot<"unknown", Record<string, unknown>> {}
