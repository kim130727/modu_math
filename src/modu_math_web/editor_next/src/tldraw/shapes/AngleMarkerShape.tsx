import { HTMLContainer, Rectangle2d, ShapeUtil, T, type TLResizeInfo } from "tldraw";
import type { AngleMarkerShape } from "./types";

export class AngleMarkerShapeUtil extends ShapeUtil<AngleMarkerShape> {
  static override type = "angle_marker" as const;

  static override props = {
    w: T.number,
    h: T.number,
    radius: T.number,
    stroke: T.string,
    strokeWidth: T.number,
  };

  override getDefaultProps(): AngleMarkerShape["props"] {
    return {
      w: 120,
      h: 90,
      radius: 34,
      stroke: "#111827",
      strokeWidth: 2,
    };
  }

  override getGeometry(shape: AngleMarkerShape) {
    return new Rectangle2d({ width: shape.props.w, height: shape.props.h, isFilled: true });
  }

  override component(shape: AngleMarkerShape) {
    return (
      <HTMLContainer className="math-shape angle-marker-shape" style={{ width: shape.props.w, height: shape.props.h }}>
        <svg width={shape.props.w} height={shape.props.h} viewBox={`0 0 ${shape.props.w} ${shape.props.h}`}>
          <path
            d={angleMarkerPath(shape.props.w, shape.props.h, shape.props.radius)}
            fill="none"
            stroke={shape.props.stroke}
            strokeWidth={shape.props.strokeWidth}
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </HTMLContainer>
    );
  }

  override getIndicatorPath(shape: AngleMarkerShape) {
    return new Path2D(angleMarkerPath(shape.props.w, shape.props.h, shape.props.radius));
  }

  override onResize(shape: AngleMarkerShape, info: TLResizeInfo<AngleMarkerShape>) {
    return {
      props: {
        w: Math.max(32, shape.props.w * info.scaleX),
        h: Math.max(32, shape.props.h * info.scaleY),
        radius: Math.max(8, shape.props.radius * Math.min(info.scaleX, info.scaleY)),
      },
    };
  }
}

export function angleMarkerPath(w: number, h: number, radius: number): string {
  const ox = 12;
  const oy = h - 12;
  const topX = Math.min(w - 12, ox + w * 0.55);
  const topY = 12;
  const arcEndX = ox + Math.min(radius, w - 24);
  const arcEndY = oy;
  const arcStartX = ox + radius * 0.55;
  const arcStartY = oy - radius * 0.72;
  return [`M ${ox} ${oy}`, `L ${w - 10} ${oy}`, `M ${ox} ${oy}`, `L ${topX} ${topY}`, `M ${arcEndX} ${arcEndY}`, `Q ${arcStartX} ${arcStartY} ${ox + 6} ${oy - radius}`].join(" ");
}
