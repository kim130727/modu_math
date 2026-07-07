import { HTMLContainer, Rectangle2d, ShapeUtil, T, type TLResizeInfo } from "tldraw";
import type { MathTextShape } from "./types";

export class MathTextShapeUtil extends ShapeUtil<MathTextShape> {
  static override type = "math_text" as const;

  static override props = {
    latex: T.string,
    text: T.string,
    fontSize: T.number,
    w: T.number,
    h: T.number,
  };

  override getDefaultProps(): MathTextShape["props"] {
    return {
      latex: "3 + 4 = □",
      text: "3 + 4 = □",
      fontSize: 36,
      w: 260,
      h: 64,
    };
  }

  override getGeometry(shape: MathTextShape) {
    return new Rectangle2d({ width: shape.props.w, height: shape.props.h, isFilled: true });
  }

  override component(shape: MathTextShape) {
    return (
      <HTMLContainer className="math-shape math-text-shape" style={{ width: shape.props.w, height: shape.props.h }}>
        {/* TODO: replace plain text with KaTeX/MathJax rendering while preserving props.latex. */}
        <div style={{ fontSize: shape.props.fontSize }}>{shape.props.text || shape.props.latex}</div>
      </HTMLContainer>
    );
  }

  override getIndicatorPath(shape: MathTextShape) {
    return new Path2D(`M0,0 h${shape.props.w} v${shape.props.h} h-${shape.props.w} Z`);
  }

  override onResize(shape: MathTextShape, info: TLResizeInfo<MathTextShape>) {
    return {
      props: {
        w: Math.max(24, shape.props.w * info.scaleX),
        h: Math.max(24, shape.props.h * info.scaleY),
      },
    };
  }
}
