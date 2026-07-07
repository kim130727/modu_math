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
    color: T.string,
    textAlign: T.literalEnum("left", "center", "right"),
    lineHeight: T.number,
    sourceKind: T.literalEnum("text", "text_box"),
  };

  override getDefaultProps(): MathTextShape["props"] {
    return {
      latex: "3 + 4 = []",
      text: "3 + 4 = []",
      fontSize: 36,
      w: 260,
      h: 64,
      color: "#050816",
      textAlign: "left",
      lineHeight: 1.25,
      sourceKind: "text_box",
    };
  }

  override getGeometry(shape: MathTextShape) {
    return new Rectangle2d({ width: shape.props.w, height: shape.props.h, isFilled: true });
  }

  override component(shape: MathTextShape) {
    const lines = (shape.props.text || shape.props.latex || "").split(/\n/g);
    const anchor = shape.props.textAlign === "center" ? "middle" : shape.props.textAlign === "right" ? "end" : "start";
    const x = shape.props.textAlign === "center" ? shape.props.w / 2 : shape.props.textAlign === "right" ? shape.props.w : 0;
    const lineStep = shape.props.fontSize * shape.props.lineHeight;
    return (
      <HTMLContainer className="math-shape math-text-shape" style={{ width: shape.props.w, height: shape.props.h }}>
        {/* TODO: replace plain text with KaTeX/MathJax rendering while preserving props.latex. */}
        <svg width={shape.props.w} height={Math.max(shape.props.h, lines.length * lineStep)} viewBox={`0 0 ${shape.props.w} ${Math.max(shape.props.h, lines.length * lineStep)}`}>
          <text
            x={x}
            y={shape.props.fontSize}
            fill={shape.props.color}
            fontSize={shape.props.fontSize}
            textAnchor={anchor}
            fontFamily={'"Segoe UI", "Pretendard", Arial, sans-serif'}
          >
            {lines.map((line, index) => (
              <tspan key={`${line}-${index}`} x={x} dy={index === 0 ? 0 : lineStep}>
                {line}
              </tspan>
            ))}
          </text>
        </svg>
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
