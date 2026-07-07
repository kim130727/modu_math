import { HTMLContainer, Rectangle2d, ShapeUtil, T, type TLResizeInfo } from "tldraw";
import type { LayoutRectShape } from "./types";

export class LayoutRectShapeUtil extends ShapeUtil<LayoutRectShape> {
  static override type = "layout_rect" as const;

  static override props = {
    w: T.number,
    h: T.number,
    fill: T.string,
    stroke: T.string,
    strokeWidth: T.number,
  };

  override getDefaultProps(): LayoutRectShape["props"] {
    return {
      w: 120,
      h: 80,
      fill: "#ffffff",
      stroke: "#111827",
      strokeWidth: 1,
    };
  }

  override getGeometry(shape: LayoutRectShape) {
    return new Rectangle2d({ width: shape.props.w, height: shape.props.h, isFilled: true });
  }

  override component(shape: LayoutRectShape) {
    return (
      <HTMLContainer
        className="math-shape layout-rect-shape"
        style={{
          width: shape.props.w,
          height: shape.props.h,
          background: shape.props.fill,
          border: `${shape.props.strokeWidth}px solid ${shape.props.stroke}`,
        }}
      />
    );
  }

  override getIndicatorPath(shape: LayoutRectShape) {
    return new Path2D(`M0,0 h${shape.props.w} v${shape.props.h} h-${shape.props.w} Z`);
  }

  override onResize(shape: LayoutRectShape, info: TLResizeInfo<LayoutRectShape>) {
    return {
      props: {
        w: Math.max(1, shape.props.w * info.scaleX),
        h: Math.max(1, shape.props.h * info.scaleY),
      },
    };
  }
}
