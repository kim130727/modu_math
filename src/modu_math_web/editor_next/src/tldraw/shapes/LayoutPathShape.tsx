import { HTMLContainer, Rectangle2d, ShapeUtil, T, type TLResizeInfo } from "tldraw";
import { scalePathData } from "../../utils/pathData";
import type { LayoutPathShape } from "./types";

export class LayoutPathShapeUtil extends ShapeUtil<LayoutPathShape> {
  static override type = "layout_path" as const;

  static override props = {
    d: T.string,
    w: T.number,
    h: T.number,
    fill: T.string,
    stroke: T.string,
    strokeWidth: T.number,
  };

  override getDefaultProps(): LayoutPathShape["props"] {
    return {
      d: "M 0 0 L 120 0 L 120 80 L 0 80 Z",
      w: 120,
      h: 80,
      fill: "#ffffff",
      stroke: "#111827",
      strokeWidth: 1,
    };
  }

  override getGeometry(shape: LayoutPathShape) {
    return new Rectangle2d({ width: shape.props.w, height: shape.props.h, isFilled: true });
  }

  override component(shape: LayoutPathShape) {
    return (
      <HTMLContainer className="math-shape layout-path-shape" style={{ width: shape.props.w, height: shape.props.h }}>
        <svg width={shape.props.w} height={shape.props.h} viewBox={`0 0 ${shape.props.w} ${shape.props.h}`}>
          <path
            d={shape.props.d}
            fill={shape.props.fill}
            stroke={shape.props.stroke}
            strokeWidth={shape.props.strokeWidth}
            vectorEffect="non-scaling-stroke"
          />
        </svg>
      </HTMLContainer>
    );
  }

  override getIndicatorPath(shape: LayoutPathShape) {
    return new Path2D(shape.props.d);
  }

  override onResize(shape: LayoutPathShape, info: TLResizeInfo<LayoutPathShape>) {
    const scaleX = Math.max(0.01, info.scaleX);
    const scaleY = Math.max(0.01, info.scaleY);
    return {
      props: {
        d: scalePathData(shape.props.d, scaleX, scaleY),
        w: Math.max(1, shape.props.w * scaleX),
        h: Math.max(1, shape.props.h * scaleY),
      },
    };
  }
}
