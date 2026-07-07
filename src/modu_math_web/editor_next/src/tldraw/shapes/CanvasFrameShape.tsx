import { HTMLContainer, Rectangle2d, ShapeUtil, T, type TLResizeInfo } from "tldraw";
import type { CanvasFrameShape } from "./types";

export const CANVAS_FRAME_ID = "__canvas_frame__";

export class CanvasFrameShapeUtil extends ShapeUtil<CanvasFrameShape> {
  static override type = "canvas_frame" as const;

  static override props = {
    w: T.number,
    h: T.number,
    stroke: T.string,
    strokeWidth: T.number,
    fill: T.string,
  };

  override getDefaultProps(): CanvasFrameShape["props"] {
    return {
      w: 1280,
      h: 720,
      stroke: "#111827",
      strokeWidth: 1,
      fill: "#ffffff",
    };
  }

  override getGeometry(shape: CanvasFrameShape) {
    return new Rectangle2d({ width: shape.props.w, height: shape.props.h, isFilled: false });
  }

  override component(shape: CanvasFrameShape) {
    return (
      <HTMLContainer className="canvas-frame-shape" style={{ width: shape.props.w, height: shape.props.h }}>
        <svg width={shape.props.w} height={shape.props.h} viewBox={`0 0 ${shape.props.w} ${shape.props.h}`}>
          <rect
            x={0}
            y={0}
            width={shape.props.w}
            height={shape.props.h}
            fill={shape.props.fill}
            stroke={shape.props.stroke}
            strokeWidth={shape.props.strokeWidth}
            vectorEffect="non-scaling-stroke"
          />
        </svg>
      </HTMLContainer>
    );
  }

  override getIndicatorPath(shape: CanvasFrameShape) {
    return new Path2D(`M0,0 h${shape.props.w} v${shape.props.h} h-${shape.props.w} Z`);
  }

  override onResize(shape: CanvasFrameShape, info: TLResizeInfo<CanvasFrameShape>) {
    return {
      props: {
        w: Math.max(100, shape.props.w * info.scaleX),
        h: Math.max(100, shape.props.h * info.scaleY),
      },
    };
  }
}
