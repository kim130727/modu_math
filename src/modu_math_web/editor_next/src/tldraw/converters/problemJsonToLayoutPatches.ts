import type { LayoutPatch } from "../../api/editorApi";
import type {
  BasicShapeObject,
  ImageObject,
  MathTextObject,
  PathObject,
  ProblemJson,
  ProblemObject,
  TableObject,
} from "../../types/problem";
import { offsetPathData } from "../../utils/pathData";

export function problemJsonToLayoutPatches(base: ProblemJson, next: ProblemJson): LayoutPatch[] {
  const baseObjects = new Map(base.objects.map((object) => [object.id, object]));
  const nextObjects = new Map(next.objects.map((object) => [object.id, object]));
  const patches: LayoutPatch[] = canvasPatches(base, next);

  for (const object of next.objects) {
    const baseObject = baseObjects.get(object.id);
    patches.push(...objectPatches(baseObject, object));
  }

  for (const object of base.objects) {
    if (!nextObjects.has(object.id)) {
      patches.push(...deletePatches(object));
    }
  }

  return patches;
}

function canvasPatches(base: ProblemJson, next: ProblemJson): LayoutPatch[] {
  if (base.canvas.width === next.canvas.width && base.canvas.height === next.canvas.height) return [];
  return [
    {
      target: "__canvas__",
      op: "update",
      value: {
        width: round(next.canvas.width),
        height: round(next.canvas.height),
      },
    },
  ];
}

function objectPatches(baseObject: ProblemObject | undefined, object: ProblemObject): LayoutPatch[] {
  if (object.type === "table") {
    if (baseObject?.type === "table") return tableUpdatePatches(baseObject, object);
    return tableSlotPatches(object);
  }
  return [baseObject ? updatePatch(baseObject, object) : addPatch(object)];
}

function deletePatches(object: ProblemObject): LayoutPatch[] {
  if (object.type === "table") {
    return (object.props.sourceSlotIds ?? tableSlotIds(object)).map((target) => ({ target, op: "delete" as const }));
  }
  return [{ target: object.id, op: "delete" }];
}

function updatePatch(baseObject: ProblemObject, object: ProblemObject): LayoutPatch {
  return {
    target: object.id,
    op: "update",
    value: updateValue(baseObject, object),
  };
}

function addPatch(object: ProblemObject): LayoutPatch {
  const value = addValue(object);
  return {
    target: object.id,
    op: "add",
    value,
  };
}

function updateValue(baseObject: ProblemObject, object: ProblemObject): Record<string, unknown> {
  switch (object.type) {
    case "math_text": {
      const isTextBoxTarget =
        baseObject.type === "math_text" ? baseObject.props.sourceKind === "text_box" : object.props.sourceKind === "text_box";
      return mathTextFields(object, isTextBoxTarget);
    }
    case "basic_shape":
      return basicShapeFields(object);
    case "image":
      return imageFields(object);
    case "path":
      return pathFields(object);
    case "fraction_bar":
      return {
        x: round(object.x),
        y: round(object.y),
        denominator: object.props.denominator,
        colored: object.props.colored,
        width: round(object.props.width),
        height: round(object.props.height),
      };
    case "number_line":
      return {
        x: round(object.x),
        y: round(object.y),
        start: object.props.start,
        end: object.props.end,
        step: object.props.step,
        width: round(object.props.width),
      };
    case "group_objects":
      return {
        x: round(object.x),
        y: round(object.y),
        item: object.props.item,
        groups: object.props.groups,
        countPerGroup: object.props.countPerGroup,
        gap: object.props.gap,
      };
    case "table":
      return {
        move_dx: 0,
        move_dy: 0,
      };
  }
}

function addValue(object: ProblemObject): Record<string, unknown> {
  switch (object.type) {
    case "math_text":
      return {
        kind: "text_box",
        content: mathTextFields(object, true),
      };
    case "basic_shape":
      if (object.props.shape === "line") {
        return {
          kind: "line",
          content: basicShapeFields(object),
        };
      }
      if (object.props.shape === "ellipse") {
        const radius = Math.min(object.props.width, object.props.height) / 2;
        return {
          kind: "circle",
          content: {
            cx: round(object.x + object.props.width / 2),
            cy: round(object.y + object.props.height / 2),
            r: round(radius),
            fill: object.props.fill ?? "none",
            stroke: object.props.stroke ?? "#111827",
            stroke_width: round(object.props.strokeWidth ?? 1),
          },
        };
      }
      return {
        kind: "rect",
        content: basicShapeFields(object),
      };
    case "image":
      return {
        kind: "image",
        content: imageFields(object),
      };
    case "path":
      return {
        kind: "path",
        content: pathFields(object),
      };
    case "table":
      return {
        kind: "rect",
        content: tableOuterFields(object),
      };
    default:
      return {
        kind: "text_box",
        content: {
          text: object.id,
          x: round(object.x),
          y: round(object.y),
          width: 180,
          height: 48,
          font_size: 24,
        },
      };
  }
}

function mathTextFields(object: MathTextObject, includeBoxSize: boolean): Record<string, unknown> {
  const fontSize = object.props.fontSize;
  const width = object.props.width ?? 280;
  const textAlign = object.props.textAlign ?? "left";
  const anchorX = textAlign === "center" ? object.x + width / 2 : textAlign === "right" ? object.x + width : object.x;
  const fields: Record<string, unknown> = {
    text: object.props.text,
    x: round(anchorX),
    y: round(object.y + fontSize),
    font_size: round(fontSize),
    fill: object.props.color ?? "#111111",
  };

  if (includeBoxSize) {
    fields.x = round(object.x);
    fields.y = round(object.y);
    fields.width = round(width);
    fields.height = round(object.props.height ?? Math.max(24, fontSize * 1.25));
    fields.align = textAlign;
    fields.line_height = object.props.lineHeight ?? 1.25;
  } else {
    if (textAlign !== "left") {
      fields.anchor = textAlign === "center" ? "middle" : "end";
    }
    fields.max_width = null;
  }

  return fields;
}

function basicShapeFields(object: BasicShapeObject): Record<string, unknown> {
  if (object.props.shape === "line") {
    return {
      x1: round(object.x),
      y1: round(object.y),
      x2: round(object.x + object.props.width),
      y2: round(object.y + object.props.height),
      stroke: object.props.stroke ?? "#111827",
      stroke_width: round(object.props.strokeWidth ?? 1),
    };
  }

  if (object.props.shape === "ellipse") {
    const radius = Math.min(object.props.width, object.props.height) / 2;
    return {
      cx: round(object.x + object.props.width / 2),
      cy: round(object.y + object.props.height / 2),
      r: round(radius),
      fill: object.props.fill ?? "none",
      stroke: object.props.stroke ?? "#111827",
      stroke_width: round(object.props.strokeWidth ?? 1),
    };
  }

  return {
    x: round(object.x),
    y: round(object.y),
    width: round(object.props.width),
    height: round(object.props.height),
    fill: object.props.fill ?? "none",
    stroke: object.props.stroke ?? "#111827",
    stroke_width: round(object.props.strokeWidth ?? 1),
  };
}

function imageFields(object: ImageObject): Record<string, unknown> {
  return {
    href: dslImageHref(object.props.src),
    x: round(object.x),
    y: round(object.y),
    width: round(object.props.width),
    height: round(object.props.height),
    preserve_aspect_ratio: object.props.preserveAspectRatio ?? "xMidYMid meet",
  };
}

function pathFields(object: PathObject): Record<string, unknown> {
  return {
    d: offsetPathData(object.props.d, object.x, object.y),
    fill: object.props.fill ?? "none",
    stroke: object.props.stroke ?? "#111827",
    stroke_width: round(object.props.strokeWidth ?? 1),
  };
}

function tableUpdatePatches(base: TableObject, next: TableObject): LayoutPatch[] {
  if (!tableStructureChanged(base, next)) {
    const dx = next.x - base.x;
    const dy = next.y - base.y;
    if (Math.abs(dx) < 0.001 && Math.abs(dy) < 0.001) return [];
    return [
      {
        target: next.id,
        op: "update",
        value: {
          move_dx: round(dx),
          move_dy: round(dy),
        },
      },
    ];
  }

  return tableSlotPatches(next);
}

function tableSlotPatches(object: TableObject): LayoutPatch[] {
  const patches: LayoutPatch[] = [
    {
      target: `${object.id}.outer`,
      op: "update",
      value: tableOuterFields(object),
    },
  ];

  const xEdges = tableEdges(object.x, object.props.columnWidths);
  const yEdges = tableEdges(object.y, object.props.rowHeights);
  const tableWidth = sum(object.props.columnWidths);
  const tableHeight = sum(object.props.rowHeights);

  for (let index = 1; index < xEdges.length - 1; index += 1) {
    const target = `${object.id}.v${index}`;
    patches.push({
      target,
      op: "update",
      value:
        object.props.dividerKinds?.[target] === "rect"
          ? tableVerticalRectDividerFields(object, xEdges[index], tableHeight)
          : tableVerticalLineDividerFields(object, xEdges[index], tableHeight),
    });
  }

  for (let index = 1; index < yEdges.length - 1; index += 1) {
    const target = `${object.id}.h${index}`;
    patches.push({
      target,
      op: "update",
      value:
        object.props.dividerKinds?.[target] === "rect"
          ? tableHorizontalRectDividerFields(object, yEdges[index], tableWidth)
          : tableHorizontalLineDividerFields(object, yEdges[index], tableWidth),
    });
  }

  for (const cell of object.props.cells) {
    const left = xEdges[cell.col - 1];
    const right = xEdges[cell.col];
    const top = yEdges[cell.row - 1];
    const bottom = yEdges[cell.row];
    if (left === undefined || right === undefined || top === undefined || bottom === undefined) continue;
    const fontSize = cell.fontSize || 24;
    patches.push({
      target: `${object.id}.r${cell.row}c${cell.col}`,
      op: "update",
      value: {
        text: cell.text,
        x: round((left + right) / 2),
        y: round(Math.max(top + fontSize, top + (bottom - top - fontSize) / 2 + fontSize)),
        font_size: round(fontSize),
        max_width: round(Math.max(8, right - left - 20)),
        anchor: "middle",
        fill: cell.color || "#111827",
      },
    });
  }

  return patches;
}

function tableOuterFields(object: TableObject): Record<string, unknown> {
  return {
    x: round(object.x),
    y: round(object.y),
    width: round(sum(object.props.columnWidths)),
    height: round(sum(object.props.rowHeights)),
    fill: object.props.fill ?? "#ffffff",
    stroke: object.props.stroke ?? "#111827",
    stroke_width: round(object.props.strokeWidth ?? 1),
  };
}

function tableVerticalLineDividerFields(object: TableObject, x: number, tableHeight: number): Record<string, unknown> {
  return {
    x1: round(x),
    y1: round(object.y),
    x2: round(x),
    y2: round(object.y + tableHeight),
    stroke: object.props.stroke ?? "#111827",
    stroke_width: round(object.props.strokeWidth ?? 1),
  };
}

function tableHorizontalLineDividerFields(object: TableObject, y: number, tableWidth: number): Record<string, unknown> {
  return {
    x1: round(object.x),
    y1: round(y),
    x2: round(object.x + tableWidth),
    y2: round(y),
    stroke: object.props.stroke ?? "#111827",
    stroke_width: round(object.props.strokeWidth ?? 1),
  };
}

function tableVerticalRectDividerFields(object: TableObject, x: number, tableHeight: number): Record<string, unknown> {
  const thickness = Math.max(1, object.props.strokeWidth ?? 1);
  return {
    x: round(x - thickness / 2),
    y: round(object.y),
    width: round(thickness),
    height: round(tableHeight),
    fill: object.props.stroke ?? "#111827",
    stroke: "none",
  };
}

function tableHorizontalRectDividerFields(object: TableObject, y: number, tableWidth: number): Record<string, unknown> {
  const thickness = Math.max(1, object.props.strokeWidth ?? 1);
  return {
    x: round(object.x),
    y: round(y - thickness / 2),
    width: round(tableWidth),
    height: round(thickness),
    fill: object.props.stroke ?? "#111827",
    stroke: "none",
  };
}

function tableSlotIds(object: TableObject): string[] {
  const ids = [`${object.id}.outer`];
  for (let col = 1; col < object.props.columnWidths.length; col += 1) ids.push(`${object.id}.v${col}`);
  for (let row = 1; row < object.props.rowHeights.length; row += 1) ids.push(`${object.id}.h${row}`);
  for (const cell of object.props.cells) ids.push(`${object.id}.r${cell.row}c${cell.col}`);
  return ids;
}

function tableStructureChanged(base: TableObject, next: TableObject): boolean {
  return (
    !numberArrayEqual(base.props.columnWidths, next.props.columnWidths) ||
    !numberArrayEqual(base.props.rowHeights, next.props.rowHeights) ||
    JSON.stringify(base.props.cells) !== JSON.stringify(next.props.cells) ||
    (base.props.fill ?? "#ffffff") !== (next.props.fill ?? "#ffffff") ||
    (base.props.stroke ?? "#111827") !== (next.props.stroke ?? "#111827") ||
    (base.props.strokeWidth ?? 1) !== (next.props.strokeWidth ?? 1)
  );
}

function tableEdges(start: number, spans: number[]): number[] {
  const edges = [start];
  for (const span of spans) edges.push(edges[edges.length - 1] + span);
  return edges;
}

function numberArrayEqual(left: number[], right: number[]): boolean {
  if (left.length !== right.length) return false;
  return left.every((value, index) => Math.abs(value - right[index]) < 0.001);
}

function sum(values: number[]): number {
  return values.reduce((total, value) => total + value, 0);
}

function dslImageHref(src: string): string {
  if (!src.startsWith("/api/editor/assets/")) return src;
  const parts = src.split("/");
  return decodeURIComponent(parts[parts.length - 1] ?? src);
}

function round(value: number): number {
  return Math.round(value * 1000) / 1000;
}
