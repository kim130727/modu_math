import { HTMLContainer, Rectangle2d, ShapeUtil, T, type TLResizeInfo } from "tldraw";
import type { NumberLineShape } from "./types";

export class NumberLineShapeUtil extends ShapeUtil<NumberLineShape> {
  static override type = "number_line" as const;

  static override props = {
    start: T.number,
    end: T.number,
    step: T.number,
    w: T.number,
    h: T.number,
  };

  override getDefaultProps(): NumberLineShape["props"] {
    return { start: 0, end: 10, step: 1, w: 600, h: 96 };
  }

  override getGeometry(shape: NumberLineShape) {
    return new Rectangle2d({ width: shape.props.w, height: shape.props.h, isFilled: true });
  }

  override component(shape: NumberLineShape) {
    const { start, end, w, h } = shape.props;
    const step = Math.max(1, Math.abs(shape.props.step));
    const ticks = buildTicks(start, end, step);
    const range = Math.max(1, end - start);
    return (
      <HTMLContainer className="math-shape number-line-shape" style={{ width: w, height: h }}>
        <div className="number-line-axis" style={{ top: h / 2 }} />
        {ticks.map((tick) => {
          const left = ((tick - start) / range) * w;
          return (
            <div key={tick} className="number-line-tick" style={{ left }}>
              <span />
              <small>{tick}</small>
            </div>
          );
        })}
      </HTMLContainer>
    );
  }

  override getIndicatorPath(shape: NumberLineShape) {
    return new Path2D(`M0,0 h${shape.props.w} v${shape.props.h} h-${shape.props.w} Z`);
  }

  override onResize(shape: NumberLineShape, info: TLResizeInfo<NumberLineShape>) {
    return {
      props: {
        w: Math.max(120, shape.props.w * info.scaleX),
        h: Math.max(64, shape.props.h * info.scaleY),
      },
    };
  }
}

function buildTicks(start: number, end: number, step: number): number[] {
  const ticks: number[] = [];
  for (let value = start; value <= end + 1e-9; value += step) {
    ticks.push(Number(value.toFixed(6)));
    if (ticks.length > 100) break;
  }
  return ticks;
}
