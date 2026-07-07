import { HTMLContainer, Rectangle2d, ShapeUtil, T, type TLResizeInfo } from "tldraw";
import type { LayoutImageShape } from "./types";

export class LayoutImageShapeUtil extends ShapeUtil<LayoutImageShape> {
  static override type = "layout_image" as const;

  static override props = {
    src: T.string,
    w: T.number,
    h: T.number,
    alt: T.string,
  };

  override getDefaultProps(): LayoutImageShape["props"] {
    return {
      src: "",
      w: 160,
      h: 120,
      alt: "",
    };
  }

  override getGeometry(shape: LayoutImageShape) {
    return new Rectangle2d({ width: shape.props.w, height: shape.props.h, isFilled: true });
  }

  override component(shape: LayoutImageShape) {
    return (
      <HTMLContainer className="math-shape layout-image-shape" style={{ width: shape.props.w, height: shape.props.h }}>
        {shape.props.src ? (
          <img src={shape.props.src} alt={shape.props.alt} draggable={false} />
        ) : (
          <div className="layout-image-placeholder">Image</div>
        )}
      </HTMLContainer>
    );
  }

  override getIndicatorPath(shape: LayoutImageShape) {
    return new Path2D(`M0,0 h${shape.props.w} v${shape.props.h} h-${shape.props.w} Z`);
  }

  override onResize(shape: LayoutImageShape, info: TLResizeInfo<LayoutImageShape>) {
    return {
      props: {
        w: Math.max(8, shape.props.w * info.scaleX),
        h: Math.max(8, shape.props.h * info.scaleY),
      },
    };
  }
}
