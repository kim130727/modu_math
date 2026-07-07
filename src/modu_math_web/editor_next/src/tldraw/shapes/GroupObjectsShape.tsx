import { HTMLContainer, Rectangle2d, ShapeUtil, T, type TLResizeInfo } from "tldraw";
import type { GroupObjectsShape } from "./types";

export class GroupObjectsShapeUtil extends ShapeUtil<GroupObjectsShape> {
  static override type = "group_objects" as const;

  static override props = {
    item: T.literalEnum("circle", "square"),
    groups: T.number,
    countPerGroup: T.number,
    gap: T.number,
    w: T.number,
    h: T.number,
  };

  override getDefaultProps(): GroupObjectsShape["props"] {
    return { item: "circle", groups: 3, countPerGroup: 4, gap: 16, w: 300, h: 120 };
  }

  override getGeometry(shape: GroupObjectsShape) {
    return new Rectangle2d({ width: shape.props.w, height: shape.props.h, isFilled: true });
  }

  override component(shape: GroupObjectsShape) {
    const groups = Math.max(1, Math.round(shape.props.groups));
    const countPerGroup = Math.max(1, Math.round(shape.props.countPerGroup));
    return (
      <HTMLContainer className="math-shape group-objects-shape" style={{ width: shape.props.w, height: shape.props.h }}>
        {Array.from({ length: groups }).map((_, groupIndex) => (
          <div key={groupIndex} className="object-group" style={{ gap: shape.props.gap }}>
            {Array.from({ length: countPerGroup }).map((__, itemIndex) => (
              <span key={itemIndex} className={shape.props.item === "square" ? "group-item square" : "group-item circle"} />
            ))}
          </div>
        ))}
      </HTMLContainer>
    );
  }

  override getIndicatorPath(shape: GroupObjectsShape) {
    return new Path2D(`M0,0 h${shape.props.w} v${shape.props.h} h-${shape.props.w} Z`);
  }

  override onResize(shape: GroupObjectsShape, info: TLResizeInfo<GroupObjectsShape>) {
    return {
      props: {
        w: Math.max(80, shape.props.w * info.scaleX),
        h: Math.max(64, shape.props.h * info.scaleY),
      },
    };
  }
}
