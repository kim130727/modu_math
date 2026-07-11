import { useEffect, useRef, useState } from "react";
import { Circle, Layer, Rect, Stage, Transformer } from "react-konva";
import type Konva from "konva";
import type { EditorShape, LineShape } from "../types/editorShape";
import { scalePathData } from "../utils/pathData";
import { KONVA_PREVIEW_FONT_LOAD_SPEC } from "./fonts";
import { ShapeRenderer } from "./ShapeRenderer";

interface KonvaStageProps {
  width: number;
  height: number;
  shapes: EditorShape[];
  selectedShapeIds: string[];
  onSelectShapes: (ids: string[]) => void;
  onChangeShapes: (shapes: EditorShape[]) => void;
}

export function KonvaStage({
  width,
  height,
  shapes,
  selectedShapeIds,
  onSelectShapes,
  onChangeShapes,
}: KonvaStageProps) {
  const wrapRef = useRef<HTMLDivElement | null>(null);
  const transformerRef = useRef<Konva.Transformer | null>(null);
  const shapeRefs = useRef<Record<string, Konva.Node | null>>({});
  const dragStartRef = useRef<{ activeId: string; ids: string[]; positions: Map<string, { x: number; y: number }> } | null>(null);
  const selectionStartRef = useRef<{ x: number; y: number; additive: boolean } | null>(null);
  const [viewport, setViewport] = useState({ width: 900, height: 640 });
  const [selectionRect, setSelectionRect] = useState<CanvasRect | null>(null);
  const [contextMenu, setContextMenu] = useState<{ x: number; y: number; shapeId: string } | null>(null);
  const [, setFontLoadRevision] = useState(0);

  useEffect(() => {
    if (!wrapRef.current) return;
    const observer = new ResizeObserver(([entry]) => {
      setViewport({
        width: Math.max(320, entry.contentRect.width),
        height: Math.max(320, entry.contentRect.height),
      });
    });
    observer.observe(wrapRef.current);
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    let cancelled = false;
    void document.fonts?.load(KONVA_PREVIEW_FONT_LOAD_SPEC).then(() => {
      if (!cancelled) setFontLoadRevision((revision) => revision + 1);
    });
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    if (!contextMenu) return;
    const closeMenu = () => setContextMenu(null);
    window.addEventListener("pointerdown", closeMenu);
    window.addEventListener("keydown", closeMenu);
    return () => {
      window.removeEventListener("pointerdown", closeMenu);
      window.removeEventListener("keydown", closeMenu);
    };
  }, [contextMenu]);

  useEffect(() => {
    if (!transformerRef.current) return;
    const selectedNodes = selectedShapeIds.map((id) => shapeRefs.current[id]).filter((node): node is Konva.Node => Boolean(node));
    transformerRef.current.nodes(selectedNodes);
    transformerRef.current.getLayer()?.batchDraw();
  }, [selectedShapeIds, shapes]);

  const scale = Math.min((viewport.width - 40) / width, (viewport.height - 40) / height, 1);
  const stageWidth = Math.max(viewport.width, width * scale + 40);
  const stageHeight = Math.max(viewport.height, height * scale + 40);
  const offsetX = Math.max(20, (stageWidth - width * scale) / 2);
  const offsetY = Math.max(20, (stageHeight - height * scale) / 2);
  const selectedIdSet = new Set(selectedShapeIds);
  const renderedShapes = [...shapes].sort(compareRenderOrder);
  const selectedLine =
    selectedShapeIds.length === 1
      ? shapes.find((shape): shape is LineShape => shape.id === selectedShapeIds[0] && shape.type === "line" && !shape.locked) ?? null
      : null;

  const pointFromEvent = (event: Konva.KonvaEventObject<MouseEvent | TouchEvent>) => {
    const stage = event.target.getStage();
    const pointer = stage?.getPointerPosition();
    if (!pointer) return null;
    return {
      x: (pointer.x - offsetX) / scale,
      y: (pointer.y - offsetY) / scale,
    };
  };

  const selectShape = (shapeId: string, event: Konva.KonvaEventObject<MouseEvent | TouchEvent>) => {
    event.cancelBubble = true;
    const additive = isAdditiveSelection(event.evt);
    if (!additive) {
      onSelectShapes([shapeId]);
      return;
    }
    onSelectShapes(
      selectedIdSet.has(shapeId) ? selectedShapeIds.filter((id) => id !== shapeId) : [...selectedShapeIds, shapeId],
    );
  };

  const openShapeContextMenu = (shape: EditorShape, event: Konva.KonvaEventObject<MouseEvent>) => {
    if (shape.type !== "line") return;
    event.evt.preventDefault();
    event.cancelBubble = true;
    if (!selectedIdSet.has(shape.id)) onSelectShapes([shape.id]);
    setContextMenu({ x: event.evt.clientX, y: event.evt.clientY, shapeId: shape.id });
  };

  const setLineDash = (shapeId: string, strokeDasharray: string | undefined) => {
    const shape = shapes.find((candidate): candidate is LineShape => candidate.id === shapeId && candidate.type === "line");
    if (!shape) return;
    onChangeShapes([{ ...shape, strokeDasharray }]);
    setContextMenu(null);
  };

  const startShapeDrag = (shapeId: string) => {
    const ids = selectedIdSet.has(shapeId) ? selectedShapeIds : [shapeId];
    if (!selectedIdSet.has(shapeId)) onSelectShapes([shapeId]);
    dragStartRef.current = {
      activeId: shapeId,
      ids,
      positions: new Map(
        shapes
          .filter((shape) => ids.includes(shape.id))
          .map((shape) => [shape.id, { x: shape.x, y: shape.y }]),
      ),
    };
  };

  const moveSelectedShapes = (shapeId: string, event: Konva.KonvaEventObject<DragEvent>) => {
    const dragStart = dragStartRef.current;
    const activeStart = dragStart?.positions.get(shapeId);
    if (!dragStart || !activeStart) return;
    const dx = event.target.x() - activeStart.x;
    const dy = event.target.y() - activeStart.y;
    const selected = new Set(dragStart.ids);
    onChangeShapes(
      shapes
        .filter((shape) => selected.has(shape.id))
        .map((shape) => {
          const start = dragStart.positions.get(shape.id);
          return start ? ({ ...shape, x: start.x + dx, y: start.y + dy } as EditorShape) : shape;
        }),
    );
  };

  const finishSelectedDrag = () => {
    dragStartRef.current = null;
  };

  const updateLineEndpoint = (
    line: LineShape,
    endpoint: "start" | "end",
    event: Konva.KonvaEventObject<DragEvent>,
  ) => {
    event.cancelBubble = true;
    const point = pointFromEvent(event);
    if (!point || line.points.length < 4) return;
    const localPoint = canvasPointToLocalLinePoint(line, point);
    const nextPoints = [...line.points];
    if (endpoint === "start") {
      nextPoints[0] = localPoint.x;
      nextPoints[1] = localPoint.y;
    } else {
      nextPoints[nextPoints.length - 2] = localPoint.x;
      nextPoints[nextPoints.length - 1] = localPoint.y;
    }
    onChangeShapes([{ ...line, points: nextPoints }]);
  };

  return (
    <div className="konva-stage-wrap" ref={wrapRef}>
      <Stage
        width={stageWidth}
        height={stageHeight}
        onMouseDown={(event) => {
          if (event.target !== event.target.getStage()) return;
          const point = pointFromEvent(event);
          if (!point) return;
          selectionStartRef.current = { ...point, additive: isAdditiveSelection(event.evt) };
          setSelectionRect({ x: point.x, y: point.y, width: 0, height: 0 });
        }}
        onMouseMove={(event) => {
          const start = selectionStartRef.current;
          if (!start) return;
          const point = pointFromEvent(event);
          if (!point) return;
          setSelectionRect(normalizeRect(start.x, start.y, point.x - start.x, point.y - start.y));
        }}
        onMouseUp={() => {
          const start = selectionStartRef.current;
          const rect = selectionRect;
          selectionStartRef.current = null;
          setSelectionRect(null);
          if (!start || !rect) return;

          if (Math.abs(rect.width) < 4 && Math.abs(rect.height) < 4) {
            if (!start.additive) onSelectShapes([]);
            return;
          }

          const hits = shapes.filter((shape) => intersectsRect(shapeBounds(shape), rect)).map((shape) => shape.id);
          onSelectShapes(start.additive ? Array.from(new Set([...selectedShapeIds, ...hits])) : hits);
        }}
        onTouchStart={(event) => {
          if (event.target === event.target.getStage()) onSelectShapes([]);
        }}
      >
        <Layer x={offsetX} y={offsetY} scaleX={scale} scaleY={scale}>
          <Rect width={width} height={height} fill="#ffffff" stroke="#cbd5e1" strokeWidth={1} listening={false} />
          {renderedShapes.map((shape) => (
            <ShapeRenderer
              key={shape.id}
              shape={shape}
              isSelected={selectedIdSet.has(shape.id)}
              nodeRef={(node) => {
                shapeRefs.current[shape.id] = node;
              }}
              onSelect={(event) => selectShape(shape.id, event)}
              onDragStart={() => startShapeDrag(shape.id)}
              onDragMove={(event) => moveSelectedShapes(shape.id, event)}
              onDragEnd={finishSelectedDrag}
              onContextMenu={(event) => openShapeContextMenu(shape, event)}
            />
          ))}
          {selectionRect ? (
            <Rect
              x={selectionRect.x}
              y={selectionRect.y}
              width={selectionRect.width}
              height={selectionRect.height}
              fill="rgba(37, 99, 235, 0.08)"
              stroke="#2563eb"
              strokeWidth={1}
              dash={[5, 4]}
              listening={false}
            />
          ) : null}
          {selectedLine ? (
            <LineEndpointHandles
              line={selectedLine}
              onDragMove={(endpoint, event) => updateLineEndpoint(selectedLine, endpoint, event)}
              onDragEnd={(endpoint, event) => updateLineEndpoint(selectedLine, endpoint, event)}
            />
          ) : null}
          <Transformer
            ref={transformerRef}
            rotateEnabled
            ignoreStroke
            boundBoxFunc={(_oldBox, newBox) => {
              if (newBox.width < 6 || newBox.height < 6) return _oldBox;
              return newBox;
            }}
            onTransformEnd={() => {
              const transformed = selectedShapeIds
                .map((id) => {
                  const node = shapeRefs.current[id];
                  const shape = shapes.find((candidate) => candidate.id === id);
                  return node && shape ? shapeFromNode(shape, node) : null;
                })
                .filter((shape): shape is EditorShape => Boolean(shape));
              if (transformed.length) onChangeShapes(transformed);
            }}
          />
        </Layer>
      </Stage>
      {contextMenu ? (
        <div className="konva-context-menu" style={{ left: contextMenu.x, top: contextMenu.y }} onPointerDown={(event) => event.stopPropagation()}>
          <button type="button" onClick={() => setLineDash(contextMenu.shapeId, "8 7")}>
            점선으로 변경
          </button>
          <button type="button" onClick={() => setLineDash(contextMenu.shapeId, undefined)}>
            실선으로 변경
          </button>
        </div>
      ) : null}
    </div>
  );
}

function compareRenderOrder(a: EditorShape, b: EditorShape): number {
  return renderPriority(a) - renderPriority(b);
}

function renderPriority(shape: EditorShape): number {
  if (shape.type === "text" || shape.type === "math") return 2;
  if (shape.type === "line") return 1;
  return 0;
}

interface CanvasRect {
  x: number;
  y: number;
  width: number;
  height: number;
}

function normalizeRect(x: number, y: number, width: number, height: number): CanvasRect {
  return {
    x: width < 0 ? x + width : x,
    y: height < 0 ? y + height : y,
    width: Math.abs(width),
    height: Math.abs(height),
  };
}

function isAdditiveSelection(event: MouseEvent | TouchEvent): boolean {
  return "shiftKey" in event && (event.shiftKey || event.ctrlKey || event.metaKey);
}

function intersectsRect(a: CanvasRect, b: CanvasRect): boolean {
  return a.x <= b.x + b.width && a.x + a.width >= b.x && a.y <= b.y + b.height && a.y + a.height >= b.y;
}

function shapeBounds(shape: EditorShape): CanvasRect {
  if (shape.type === "circle") {
    return { x: shape.x - shape.radius, y: shape.y - shape.radius, width: shape.radius * 2, height: shape.radius * 2 };
  }
  if (shape.type === "line") {
    const xs = shape.points.filter((_, index) => index % 2 === 0);
    const ys = shape.points.filter((_, index) => index % 2 === 1);
    const minX = Math.min(...xs);
    const maxX = Math.max(...xs);
    const minY = Math.min(...ys);
    const maxY = Math.max(...ys);
    return { x: shape.x + minX, y: shape.y + minY, width: Math.max(1, maxX - minX), height: Math.max(1, maxY - minY) };
  }
  if (shape.type === "text") {
    return { x: shape.x, y: shape.y, width: shape.width ?? Math.max(24, shape.text.length * shape.fontSize * 0.55), height: shape.height ?? shape.fontSize * 1.3 };
  }
  if (shape.type === "path") {
    return { x: shape.x, y: shape.y, width: shape.width, height: shape.height };
  }
  return { x: shape.x, y: shape.y, width: shape.width, height: shape.height };
}

function LineEndpointHandles({
  line,
  onDragMove,
  onDragEnd,
}: {
  line: LineShape;
  onDragMove: (endpoint: "start" | "end", event: Konva.KonvaEventObject<DragEvent>) => void;
  onDragEnd: (endpoint: "start" | "end", event: Konva.KonvaEventObject<DragEvent>) => void;
}) {
  if (line.points.length < 4) return null;
  const start = localLinePointToCanvasPoint(line, { x: line.points[0], y: line.points[1] });
  const end = localLinePointToCanvasPoint(line, {
    x: line.points[line.points.length - 2],
    y: line.points[line.points.length - 1],
  });

  return (
    <>
      <Circle
        x={start.x}
        y={start.y}
        radius={6}
        fill="#ffffff"
        stroke="#2563eb"
        strokeWidth={2}
        draggable
        onMouseDown={(event) => {
          event.cancelBubble = true;
        }}
        onTouchStart={(event) => {
          event.cancelBubble = true;
        }}
        onDragMove={(event) => onDragMove("start", event)}
        onDragEnd={(event) => onDragEnd("start", event)}
      />
      <Circle
        x={end.x}
        y={end.y}
        radius={6}
        fill="#ffffff"
        stroke="#2563eb"
        strokeWidth={2}
        draggable
        onMouseDown={(event) => {
          event.cancelBubble = true;
        }}
        onTouchStart={(event) => {
          event.cancelBubble = true;
        }}
        onDragMove={(event) => onDragMove("end", event)}
        onDragEnd={(event) => onDragEnd("end", event)}
      />
    </>
  );
}

function localLinePointToCanvasPoint(line: LineShape, point: { x: number; y: number }): { x: number; y: number } {
  const rotation = degreesToRadians(line.rotation ?? 0);
  const cos = Math.cos(rotation);
  const sin = Math.sin(rotation);
  return {
    x: line.x + point.x * cos - point.y * sin,
    y: line.y + point.x * sin + point.y * cos,
  };
}

function canvasPointToLocalLinePoint(line: LineShape, point: { x: number; y: number }): { x: number; y: number } {
  const rotation = degreesToRadians(-(line.rotation ?? 0));
  const dx = point.x - line.x;
  const dy = point.y - line.y;
  const cos = Math.cos(rotation);
  const sin = Math.sin(rotation);
  return {
    x: dx * cos - dy * sin,
    y: dx * sin + dy * cos,
  };
}

function degreesToRadians(degrees: number): number {
  return (degrees * Math.PI) / 180;
}

function shapeFromNode(shape: EditorShape, node: Konva.Node): EditorShape {
  const scaleX = node.scaleX();
  const scaleY = node.scaleY();
  node.scaleX(1);
  node.scaleY(1);

  if (shape.type === "rect") {
    return {
      ...shape,
      x: node.x(),
      y: node.y(),
      rotation: node.rotation(),
      width: Math.max(6, shape.width * scaleX),
      height: Math.max(6, shape.height * scaleY),
    };
  }
  if (shape.type === "image") {
    return {
      ...shape,
      x: node.x(),
      y: node.y(),
      rotation: node.rotation(),
      width: Math.max(6, shape.width * scaleX),
      height: Math.max(6, shape.height * scaleY),
    };
  }
  if (shape.type === "text") {
    return {
      ...shape,
      x: node.x(),
      y: node.y(),
      rotation: node.rotation(),
      width: Math.max(24, (shape.width ?? node.width()) * scaleX),
      height: shape.height ? Math.max(12, shape.height * scaleY) : undefined,
      sourceKind: "text_box",
    };
  }
  if (shape.type === "math") {
    return {
      ...shape,
      x: node.x(),
      y: node.y(),
      rotation: node.rotation(),
      width: Math.max(24, shape.width * scaleX),
      height: Math.max(16, shape.height * scaleY),
    };
  }
  if (shape.type === "path") {
    return {
      ...shape,
      x: node.x(),
      y: node.y(),
      rotation: node.rotation(),
      d: scalePathData(shape.d, scaleX, scaleY),
      width: Math.max(1, shape.width * Math.abs(scaleX)),
      height: Math.max(1, shape.height * Math.abs(scaleY)),
    };
  }
  if (shape.type === "circle") {
    return {
      ...shape,
      x: node.x(),
      y: node.y(),
      rotation: node.rotation(),
      radius: Math.max(4, shape.radius * ((Math.abs(scaleX) + Math.abs(scaleY)) / 2)),
    };
  }
  if (shape.type === "line") {
    return {
      ...shape,
      x: node.x(),
      y: node.y(),
      rotation: node.rotation(),
      points: shape.points.map((point, index) => point * (index % 2 === 0 ? scaleX : scaleY)),
    };
  }
  return shape;
}
