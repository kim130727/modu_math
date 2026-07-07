import { HTMLContainer, Rectangle2d, ShapeUtil, T, type TLResizeInfo } from "tldraw";
import type { FractionBarShape } from "./types";

export class FractionBarShapeUtil extends ShapeUtil<FractionBarShape> {
  static override type = "fraction_bar" as const;

  static override props = {
    denominator: T.number,
    colored: T.number,
    w: T.number,
    h: T.number,
  };

  override getDefaultProps(): FractionBarShape["props"] {
    return { denominator: 5, colored: 3, w: 400, h: 60 };
  }

  override getGeometry(shape: FractionBarShape) {
    return new Rectangle2d({ width: shape.props.w, height: shape.props.h, isFilled: true });
  }

  override component(shape: FractionBarShape) {
    const denominator = Math.max(1, Math.round(shape.props.denominator));
    const colored = Math.max(0, Math.min(denominator, Math.round(shape.props.colored)));
    return (
      <HTMLContainer className="math-shape fraction-bar-shape" style={{ width: shape.props.w, height: shape.props.h }}>
        {Array.from({ length: denominator }).map((_, index) => (
          <div key={index} className={index < colored ? "fraction-cell colored" : "fraction-cell"} />
        ))}
      </HTMLContainer>
    );
  }

  override getIndicatorPath(shape: FractionBarShape) {
    return new Path2D(`M0,0 h${shape.props.w} v${shape.props.h} h-${shape.props.w} Z`);
  }

  override onResize(shape: FractionBarShape, info: TLResizeInfo<FractionBarShape>) {
    return {
      props: {
        w: Math.max(32, shape.props.w * info.scaleX),
        h: Math.max(24, shape.props.h * info.scaleY),
      },
    };
  }
}
