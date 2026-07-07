import { HTMLContainer, Rectangle2d, ShapeUtil, T, type TLResizeInfo } from "tldraw";
import type { PointerEvent as ReactPointerEvent } from "react";
import type { TableShape } from "./types";

export class TableShapeUtil extends ShapeUtil<TableShape> {
  static override type = "table" as const;

  static override props = {
    columnWidths: T.arrayOf(T.number),
    rowHeights: T.arrayOf(T.number),
    cells: T.jsonValue,
    fill: T.string,
    stroke: T.string,
    strokeWidth: T.number,
    sourceSlotIds: T.arrayOf(T.string),
    dividerKinds: T.jsonValue,
  };

  override getDefaultProps(): TableShape["props"] {
    return {
      columnWidths: [120, 120, 120],
      rowHeights: [56, 56],
      cells: [],
      fill: "#ffffff",
      stroke: "#111827",
      strokeWidth: 1,
      sourceSlotIds: [],
      dividerKinds: {},
    };
  }

  override getGeometry(shape: TableShape) {
    return new Rectangle2d({ width: tableWidth(shape), height: tableHeight(shape), isFilled: true });
  }

  override component(shape: TableShape) {
    const width = tableWidth(shape);
    const height = tableHeight(shape);
    const cells = shape.props.cells;
    const byKey = new Map(cells.map((cell) => [`${cell.row}:${cell.col}`, cell]));

    return (
      <HTMLContainer className="math-shape table-shape" style={{ width, height }}>
        <div
          className="table-shape-grid"
          style={{
            width,
            height,
            gridTemplateColumns: shape.props.columnWidths.map((value) => `${value}px`).join(" "),
            gridTemplateRows: shape.props.rowHeights.map((value) => `${value}px`).join(" "),
            background: shape.props.fill,
            borderColor: shape.props.stroke,
            borderWidth: shape.props.strokeWidth,
          }}
        >
          {shape.props.rowHeights.flatMap((_, row) =>
            shape.props.columnWidths.map((__, col) => {
              const cell = byKey.get(`${row + 1}:${col + 1}`);
              return (
                <div
                  className="table-shape-cell"
                  key={`${row}:${col}`}
                  style={{
                    color: cell?.color ?? "#111827",
                    fontSize: cell?.fontSize ?? 24,
                    borderColor: shape.props.stroke,
                    borderWidth: shape.props.strokeWidth,
                  }}
                  onPointerDown={(event) => {
                    if (event.detail > 1) event.stopPropagation();
                  }}
                  onDoubleClick={(event) => {
                    event.stopPropagation();
                    event.preventDefault();
                    const nextText = window.prompt("Cell text", cell?.text ?? "");
                    if (nextText === null) return;
                    const nextCells = upsertCell(cells, row + 1, col + 1, nextText, cell);
                    this.editor.updateShape({ id: shape.id, type: shape.type, props: { cells: nextCells } });
                  }}
                >
                  {cell?.text ?? ""}
                </div>
              );
            }),
          )}
        </div>
        {shape.props.columnWidths.slice(0, -1).map((_, index) => {
          const left = sum(shape.props.columnWidths.slice(0, index + 1));
          return (
            <div
              className="table-divider table-divider-v"
              key={`v${index}`}
              style={{ left }}
              onPointerDown={(event) => this.startDividerDrag(event, shape, "v", index)}
              title="열 너비 조절"
            />
          );
        })}
        {shape.props.rowHeights.slice(0, -1).map((_, index) => {
          const top = sum(shape.props.rowHeights.slice(0, index + 1));
          return (
            <div
              className="table-divider table-divider-h"
              key={`h${index}`}
              style={{ top }}
              onPointerDown={(event) => this.startDividerDrag(event, shape, "h", index)}
              title="행 높이 조절"
            />
          );
        })}
      </HTMLContainer>
    );
  }

  private startDividerDrag(event: ReactPointerEvent<HTMLDivElement>, shape: TableShape, axis: "h" | "v", index: number) {
    event.preventDefault();
    event.stopPropagation();

    const startX = event.clientX;
    const startY = event.clientY;
    const startColumns = [...shape.props.columnWidths];
    const startRows = [...shape.props.rowHeights];
    const minSize = 16;

    const onMove = (moveEvent: PointerEvent) => {
      if (axis === "v") {
        const delta = moveEvent.clientX - startX;
        const nextColumns = resizeAdjacentSpans(startColumns, index, delta, minSize);
        this.editor.updateShape({ id: shape.id, type: shape.type, props: { columnWidths: nextColumns } });
      } else {
        const delta = moveEvent.clientY - startY;
        const nextRows = resizeAdjacentSpans(startRows, index, delta, minSize);
        this.editor.updateShape({ id: shape.id, type: shape.type, props: { rowHeights: nextRows } });
      }
    };

    const onUp = () => {
      window.removeEventListener("pointermove", onMove);
      window.removeEventListener("pointerup", onUp);
    };

    window.addEventListener("pointermove", onMove);
    window.addEventListener("pointerup", onUp, { once: true });
  }

  override getIndicatorPath(shape: TableShape) {
    const width = tableWidth(shape);
    const height = tableHeight(shape);
    return new Path2D(`M0,0 h${width} v${height} h-${width} Z`);
  }

  override onResize(shape: TableShape, info: TLResizeInfo<TableShape>) {
    return {
      props: {
        columnWidths: shape.props.columnWidths.map((value) => Math.max(8, value * info.scaleX)),
        rowHeights: shape.props.rowHeights.map((value) => Math.max(8, value * info.scaleY)),
      },
    };
  }
}

function tableWidth(shape: TableShape): number {
  return shape.props.columnWidths.reduce((sum, value) => sum + value, 0);
}

function tableHeight(shape: TableShape): number {
  return shape.props.rowHeights.reduce((sum, value) => sum + value, 0);
}

function resizeAdjacentSpans(spans: number[], index: number, delta: number, minSize: number): number[] {
  const next = [...spans];
  const left = next[index];
  const right = next[index + 1];
  if (left === undefined || right === undefined) return next;
  const clampedDelta = Math.max(minSize - left, Math.min(delta, right - minSize));
  next[index] = left + clampedDelta;
  next[index + 1] = right - clampedDelta;
  return next;
}

function sum(values: number[]): number {
  return values.reduce((total, value) => total + value, 0);
}

function upsertCell(
  cells: TableShape["props"]["cells"],
  row: number,
  col: number,
  text: string,
  existing?: TableShape["props"]["cells"][number],
): TableShape["props"]["cells"] {
  const next = cells.filter((cell) => cell.row !== row || cell.col !== col);
  next.push({
    row,
    col,
    text,
    fontSize: existing?.fontSize ?? 24,
    color: existing?.color ?? "#111827",
  });
  return next.sort((a, b) => a.row - b.row || a.col - b.col);
}
