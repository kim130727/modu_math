import { HTMLContainer, Rectangle2d, ShapeUtil, T, type TLResizeInfo } from "tldraw";
import type { SpeechBubbleShape } from "./types";

export class SpeechBubbleShapeUtil extends ShapeUtil<SpeechBubbleShape> {
  static override type = "speech_bubble" as const;

  static override props = {
    w: T.number,
    h: T.number,
    tailX: T.number,
    tailY: T.number,
    fill: T.string,
    stroke: T.string,
    strokeWidth: T.number,
  };

  override getDefaultProps(): SpeechBubbleShape["props"] {
    return {
      w: 180,
      h: 90,
      tailX: 44,
      tailY: 116,
      fill: "#ffffff",
      stroke: "#111827",
      strokeWidth: 2,
    };
  }

  override getGeometry(shape: SpeechBubbleShape) {
    return new Rectangle2d({ width: shape.props.w, height: Math.max(shape.props.h, shape.props.tailY), isFilled: true });
  }

  override component(shape: SpeechBubbleShape) {
    const path = speechBubblePath(shape.props.w, shape.props.h, shape.props.tailX, shape.props.tailY);
    return (
      <HTMLContainer className="math-shape speech-bubble-shape" style={{ width: shape.props.w, height: shape.props.tailY }}>
        <svg width={shape.props.w} height={shape.props.tailY} viewBox={`0 0 ${shape.props.w} ${shape.props.tailY}`}>
          <path d={path} fill={shape.props.fill} stroke={shape.props.stroke} strokeWidth={shape.props.strokeWidth} />
        </svg>
      </HTMLContainer>
    );
  }

  override getIndicatorPath(shape: SpeechBubbleShape) {
    return new Path2D(speechBubblePath(shape.props.w, shape.props.h, shape.props.tailX, shape.props.tailY));
  }

  override onResize(shape: SpeechBubbleShape, info: TLResizeInfo<SpeechBubbleShape>) {
    return {
      props: {
        w: Math.max(40, shape.props.w * info.scaleX),
        h: Math.max(32, shape.props.h * info.scaleY),
        tailX: Math.max(8, shape.props.tailX * info.scaleX),
        tailY: Math.max(40, shape.props.tailY * info.scaleY),
      },
    };
  }
}

export function speechBubblePath(w: number, h: number, tailX: number, tailY: number): string {
  const r = Math.min(18, w / 6, h / 4);
  const tailBase = Math.max(r + 12, Math.min(w - r - 12, tailX + 28));
  return [
    `M ${r} 0`,
    `H ${w - r}`,
    `Q ${w} 0 ${w} ${r}`,
    `V ${h - r}`,
    `Q ${w} ${h} ${w - r} ${h}`,
    `H ${tailBase}`,
    `L ${tailX} ${tailY}`,
    `L ${tailX + 10} ${h}`,
    `H ${r}`,
    `Q 0 ${h} 0 ${h - r}`,
    `V ${r}`,
    `Q 0 0 ${r} 0`,
    "Z",
  ].join(" ");
}
