import { HTMLContainer, Rectangle2d, ShapeUtil, T, type TLResizeInfo } from "tldraw";
import type { LayoutLineShape } from "./types";

export class LayoutLineShapeUtil extends ShapeUtil<LayoutLineShape> {
  static override type = "layout_line" as const;

  static override props = {
    w: T.number,
    h: T.number,
    stroke: T.string,
    strokeWidth: T.number,
  };

  override getDefaultProps(): LayoutLineShape["props"] {
    return {
      w: 120,
      h: 0,
      stroke: "#111827",
      strokeWidth: 1,
    };
  }

  override getGeometry(shape: LayoutLineShape) {
    const width = Math.max(Math.abs(shape.props.w), shape.props.strokeWidth);
    const height = Math.max(Math.abs(shape.props.h), shape.props.strokeWidth);
    return new Rectangle2d({ width, height, isFilled: true });
  }

  override component(shape: LayoutLineShape) {
    const width = Math.max(Math.abs(shape.props.w), shape.props.strokeWidth);
    const height = Math.max(Math.abs(shape.props.h), shape.props.strokeWidth);
    const isVertical = Math.abs(shape.props.h) > Math.abs(shape.props.w);

    return (
      <HTMLContainer className="math-shape layout-line-shape" style={{ width, height }}>
        <div
          style={{
            position: "absolute",
            left: 0,
            top: 0,
            width: isVertical ? shape.props.strokeWidth : width,
            height: isVertical ? height : shape.props.strokeWidth,
            background: shape.props.stroke,
          }}
        />
      </HTMLContainer>
    );
  }

  override getIndicatorPath(shape: LayoutLineShape) {
    const width = Math.max(Math.abs(shape.props.w), shape.props.strokeWidth);
    const height = Math.max(Math.abs(shape.props.h), shape.props.strokeWidth);
    return new Path2D(`M0,0 h${width} v${height} h-${width} Z`);
  }

  override onResize(shape: LayoutLineShape, info: TLResizeInfo<LayoutLineShape>) {
    return {
      props: {
        w: shape.props.w * info.scaleX,
        h: shape.props.h * info.scaleY,
      },
    };
  }
}
