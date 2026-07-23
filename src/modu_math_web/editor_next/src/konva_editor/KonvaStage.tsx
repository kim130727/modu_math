import { useEffect, useRef, useState } from "react";
import { Circle, Layer, Line, Path, Rect, Stage, Text, Transformer } from "react-konva";
import type Konva from "konva";
import type { TutorRendererOverlay } from "../api/editorApi";
import type { ConnectorShape, EditorShape, LineShape } from "../types/editorShape";
import { scalePathData } from "../utils/pathData";
import { connectorArrowForPreset, connectorBounds, connectorControl, connectorEnd, connectorKindForPreset, connectorPathData, connectorStart } from "./connectorGeometry";
import { KONVA_PREVIEW_FONT_LOAD_SPEC } from "./fonts";
import { ShapeRenderer } from "./ShapeRenderer";
import { adjustableShapePoint } from "./shapeGeometry";
import type { ShapePreset } from "./KonvaToolbar";

interface KonvaStageProps {
  width: number;
  height: number;
  shapes: EditorShape[];
  selectedShapeIds: string[];
  tutorOverlays?: TutorRendererOverlay[];
  activeTutorOverlayIndex?: number | null;
  drawingPreset?: ShapePreset | null;
  onSelectShapes: (ids: string[]) => void;
  onChangeShapes: (shapes: EditorShape[]) => void;
  onConvertShapesToAnswer?: (ids: string[]) => void;
  onRestoreShapesFromAnswer?: (ids: string[]) => void;
  onDrawShape?: (preset: ShapePreset, start: CanvasPoint, end: CanvasPoint, points?: CanvasPoint[]) => void;
  onDrawingComplete?: () => void;
  onTutorOverlaySelect?: (overlayIndex: number | null) => void;
  onTutorOverlayChange?: (overlayIndex: number, patch: Partial<TutorRendererOverlay>) => void;
  onTutorOverlayMove?: (overlayIndex: number, x: number, y: number) => void;
}

export function KonvaStage({
  width,
  height,
  shapes,
  selectedShapeIds,
  tutorOverlays = [],
  activeTutorOverlayIndex = null,
  drawingPreset = null,
  onSelectShapes,
  onChangeShapes,
  onConvertShapesToAnswer,
  onRestoreShapesFromAnswer,
  onDrawShape,
  onDrawingComplete,
  onTutorOverlaySelect,
  onTutorOverlayChange,
  onTutorOverlayMove,
}: KonvaStageProps) {
  const wrapRef = useRef<HTMLDivElement | null>(null);
  const transformerRef = useRef<Konva.Transformer | null>(null);
  const shapeRefs = useRef<Record<string, Konva.Node | null>>({});
  const dragStartRef = useRef<{ activeId: string; ids: string[]; positions: Map<string, { x: number; y: number }> } | null>(null);
  const selectionStartRef = useRef<{ x: number; y: number; additive: boolean } | null>(null);
  const drawStartRef = useRef<CanvasPoint | null>(null);
  const drawPointsRef = useRef<CanvasPoint[]>([]);
  const tutorTextEditorRef = useRef<HTMLTextAreaElement | null>(null);
  const [viewport, setViewport] = useState({ width: 900, height: 640 });
  const [selectionRect, setSelectionRect] = useState<CanvasRect | null>(null);
  const [drawingPreview, setDrawingPreview] = useState<EditorShape | null>(null);
  const [contextMenu, setContextMenu] = useState<{ x: number; y: number; shapeId: string } | null>(null);
  const [editingTutorLabel, setEditingTutorLabel] = useState<{
    index: number;
    text: string;
    left: number;
    top: number;
    width: number;
    fontSize: number;
    color: string;
  } | null>(null);
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
    const selectedNodes = selectedShapeIds
      .map((id) => {
        const shape = shapes.find((candidate) => candidate.id === id);
        if (shape?.type === "line" || shape?.type === "connector") return null;
        return shapeRefs.current[id];
      })
      .filter((node): node is Konva.Node => Boolean(node));
    transformerRef.current.nodes(selectedNodes);
    transformerRef.current.getLayer()?.batchDraw();
  }, [selectedShapeIds, shapes]);

  useEffect(() => {
    if (!editingTutorLabel) return;
    tutorTextEditorRef.current?.focus();
    tutorTextEditorRef.current?.select();
  }, [editingTutorLabel?.index]);

  const fitScale = Math.min((viewport.width - 40) / width, (viewport.height - 40) / height);
  const scale = Math.min(fitScale, 2.5);
  const stageWidth = Math.max(viewport.width, width * scale + 40);
  const stageHeight = Math.max(viewport.height, height * scale + 40);
  const offsetX = Math.max(20, (stageWidth - width * scale) / 2);
  const offsetY = Math.max(20, (stageHeight - height * scale) / 2);
  const selectedIdSet = new Set(selectedShapeIds);
  const renderedShapes = [...shapes].sort(compareRenderOrder);
  const shapesById = new Map(shapes.map((shape) => [shape.id, shape]));
  const selectedLine =
    selectedShapeIds.length === 1
      ? shapes.find((shape): shape is LineShape => shape.id === selectedShapeIds[0] && shape.type === "line" && !shape.locked) ?? null
      : null;
  const selectedConnector =
    selectedShapeIds.length === 1
      ? shapes.find((shape): shape is ConnectorShape => shape.id === selectedShapeIds[0] && shape.type === "connector" && !shape.locked) ?? null
      : null;
  const selectedAdjustablePath =
    selectedShapeIds.length === 1
      ? shapes.find(
          (shape): shape is Extract<EditorShape, { type: "path" }> =>
            shape.id === selectedShapeIds[0] && shape.type === "path" && !shape.locked && Boolean(adjustableShapePoint(shape)),
        ) ?? null
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
    if (!canOpenShapeContextMenu(shape)) return;
    event.evt.preventDefault();
    event.cancelBubble = true;
    if (!selectedIdSet.has(shape.id)) onSelectShapes([shape.id]);
    setContextMenu({ x: event.evt.clientX, y: event.evt.clientY, shapeId: shape.id });
  };

  const setLineDash = (shapeId: string, strokeDasharray: string | undefined) => {
    const shape = shapes.find(
      (candidate): candidate is LineShape | ConnectorShape =>
        candidate.id === shapeId && (candidate.type === "line" || candidate.type === "connector"),
    );
    if (!shape) return;
    onChangeShapes([{ ...shape, strokeDasharray }]);
    setContextMenu(null);
  };

  const contextMenuShape = contextMenu ? shapes.find((shape) => shape.id === contextMenu.shapeId) ?? null : null;
  const contextMenuSelectionIds = contextMenuShape
    ? selectedIdSet.has(contextMenuShape.id)
      ? selectedShapeIds
      : [contextMenuShape.id]
    : [];
  const contextAnswerTargets = shapes.filter((shape) => contextMenuSelectionIds.includes(shape.id) && isAnswerSlotShape(shape));

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
    const start = localLinePointToCanvasPoint(line, { x: line.points[0], y: line.points[1] });
    const end = localLinePointToCanvasPoint(line, {
      x: line.points[line.points.length - 2],
      y: line.points[line.points.length - 1],
    });
    const nextStart = endpoint === "start" ? point : start;
    const nextEnd = endpoint === "end" ? point : end;
    onChangeShapes([
      {
        ...line,
        x: nextStart.x,
        y: nextStart.y,
        rotation: 0,
        offsetX: 0,
        offsetY: 0,
        points: [0, 0, roundStageNumber(nextEnd.x - nextStart.x), roundStageNumber(nextEnd.y - nextStart.y)],
      },
    ]);
  };

  const updateConnectorEndpoint = (
    connector: ConnectorShape,
    endpoint: "start" | "end",
    event: Konva.KonvaEventObject<DragEvent>,
  ) => {
    event.cancelBubble = true;
    const point = pointFromEvent(event);
    if (!point) return;
    const start = connectorPointToCanvasPoint(connector, connectorStart(connector));
    const end = connectorPointToCanvasPoint(connector, connectorEnd(connector));
    const control = connector.kind === "straight" ? undefined : connectorPointToCanvasPoint(connector, connectorControl(connector));
    const nextStart = endpoint === "start" ? point : start;
    const nextEnd = endpoint === "end" ? point : end;
    onChangeShapes([
      {
        ...connector,
        x: nextStart.x,
        y: nextStart.y,
        rotation: 0,
        offsetX: 0,
        offsetY: 0,
        start: { x: 0, y: 0 },
        end: { x: roundStageNumber(nextEnd.x - nextStart.x), y: roundStageNumber(nextEnd.y - nextStart.y) },
        control: control
          ? { x: roundStageNumber(control.x - nextStart.x), y: roundStageNumber(control.y - nextStart.y) }
          : undefined,
      },
    ]);
  };

  const updateConnectorControl = (connector: ConnectorShape, event: Konva.KonvaEventObject<DragEvent>) => {
    event.cancelBubble = true;
    const point = pointFromEvent(event);
    if (!point || connector.kind === "straight") return;
    onChangeShapes([
      {
        ...connector,
        control: { x: roundStageNumber(point.x - connector.x), y: roundStageNumber(point.y - connector.y) },
      },
    ]);
  };

  const updatePathAdjustment = (shape: Extract<EditorShape, { type: "path" }>, event: Konva.KonvaEventObject<DragEvent>) => {
    event.cancelBubble = true;
    const point = pointFromEvent(event);
    if (!point) return;
    const localPoint = canvasPointToLocalPathPoint(shape, point);
    onChangeShapes([
      {
        ...shape,
        adjustment: {
          x: roundStageNumber(clamp(localPoint.x, 0, shape.width)),
          y: roundStageNumber(clamp(localPoint.y, 0, shape.height)),
        },
      },
    ]);
  };

  return (
    <div className={drawingPreset ? "konva-stage-wrap drawing" : "konva-stage-wrap"} ref={wrapRef}>
      <Stage
        width={stageWidth}
        height={stageHeight}
        onMouseDown={(event) => {
          if (event.target !== event.target.getStage()) return;
          const point = pointFromEvent(event);
          if (!point) return;
          if (drawingPreset && onDrawShape) {
            drawStartRef.current = point;
            drawPointsRef.current = [point];
            setDrawingPreview(previewShapeForDrawing(drawingPreset, point, point, drawPointsRef.current));
            onSelectShapes([]);
            return;
          }
          selectionStartRef.current = { ...point, additive: isAdditiveSelection(event.evt) };
          setSelectionRect({ x: point.x, y: point.y, width: 0, height: 0 });
        }}
        onMouseMove={(event) => {
          if (drawStartRef.current && drawingPreset) {
            const point = pointFromEvent(event);
            if (!point) return;
            if (drawingPreset === "freeformScribble") drawPointsRef.current = appendFreeformPoint(drawPointsRef.current, point);
            setDrawingPreview(previewShapeForDrawing(drawingPreset, drawStartRef.current, point, drawPointsRef.current));
            return;
          }
          const start = selectionStartRef.current;
          if (!start) return;
          const point = pointFromEvent(event);
          if (!point) return;
          setSelectionRect(normalizeRect(start.x, start.y, point.x - start.x, point.y - start.y));
        }}
        onMouseUp={(event) => {
          if (drawStartRef.current && drawingPreset && onDrawShape) {
            const start = drawStartRef.current;
            const points = drawPointsRef.current;
            const end = pointFromEvent(event) ?? drawingEndPoint(drawingPreview ?? previewShapeForDrawing(drawingPreset, start, start, points));
            drawStartRef.current = null;
            drawPointsRef.current = [];
            const preview = drawingPreview;
            setDrawingPreview(null);
            if (preview && shapeLongEnough(preview)) {
              onDrawShape(drawingPreset, start, end, points);
            }
            onDrawingComplete?.();
            return;
          }
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
          {renderedShapes.map((shape) => (shape.interaction ? <AnswerSlotOverlay key={`${shape.id}.answer-overlay`} shape={shape} /> : null))}
          <TutorOverlayLayer
            overlays={tutorOverlays}
            shapesById={shapesById}
            activeOverlayIndex={activeTutorOverlayIndex}
            onOverlaySelect={onTutorOverlaySelect}
            onOverlayTextEditStart={(index, overlay, metrics) => {
              onTutorOverlaySelect?.(index);
              setEditingTutorLabel({
                index,
                text: overlay.text ?? "",
                left: offsetX + (overlay.x ?? 0) * scale,
                top: offsetY + (overlay.y ?? 0) * scale,
                width: Math.max(160, metrics.width * scale),
                fontSize: Math.max(14, metrics.fontSize * scale),
                color: metrics.fill,
              });
            }}
            onOverlayMove={onTutorOverlayMove}
          />
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
          {drawingPreview ? (
            <ShapeRenderer
              shape={drawingPreview}
              isSelected={false}
              nodeRef={() => undefined}
              onSelect={(event) => {
                event.cancelBubble = true;
              }}
              onDragStart={() => undefined}
              onDragMove={() => undefined}
              onDragEnd={() => undefined}
              onContextMenu={(event) => {
                event.cancelBubble = true;
              }}
            />
          ) : null}
          {selectedLine ? (
            <LineEndpointHandles
              line={selectedLine}
              onDragMove={(endpoint, event) => updateLineEndpoint(selectedLine, endpoint, event)}
              onDragEnd={(endpoint, event) => updateLineEndpoint(selectedLine, endpoint, event)}
            />
          ) : null}
          {selectedConnector ? (
            <ConnectorHandles
              connector={selectedConnector}
              onEndpointDrag={(endpoint, event) => updateConnectorEndpoint(selectedConnector, endpoint, event)}
              onControlDrag={(event) => updateConnectorControl(selectedConnector, event)}
            />
          ) : null}
          <Transformer
            ref={transformerRef}
            rotateEnabled
            ignoreStroke
            borderStroke="#6b7280"
            borderStrokeWidth={1}
            anchorFill="#ffffff"
            anchorStroke="#6b7280"
            anchorStrokeWidth={2}
            anchorSize={10}
            anchorCornerRadius={10}
            rotateAnchorOffset={34}
            rotateAnchorCursor="grab"
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
          {selectedAdjustablePath ? (
            <PathAdjustmentHandle
              shape={selectedAdjustablePath}
              onDragMove={(event) => updatePathAdjustment(selectedAdjustablePath, event)}
              onDragEnd={(event) => updatePathAdjustment(selectedAdjustablePath, event)}
            />
          ) : null}
        </Layer>
      </Stage>
      {editingTutorLabel ? (
        <textarea
          ref={tutorTextEditorRef}
          className="konva-overlay-text-editor"
          value={editingTutorLabel.text}
          style={{
            left: editingTutorLabel.left,
            top: editingTutorLabel.top,
            width: editingTutorLabel.width,
            fontSize: editingTutorLabel.fontSize,
            color: editingTutorLabel.color,
          }}
          onChange={(event) => {
            const text = event.target.value;
            setEditingTutorLabel((current) => (current ? { ...current, text } : current));
            onTutorOverlayChange?.(editingTutorLabel.index, { text });
          }}
          onBlur={() => setEditingTutorLabel(null)}
          onPointerDown={(event) => event.stopPropagation()}
          onKeyDown={(event) => {
            if (event.key === "Escape" || (event.key === "Enter" && (event.ctrlKey || event.metaKey))) {
              event.preventDefault();
              setEditingTutorLabel(null);
            }
          }}
        />
      ) : null}
      {contextMenu ? (
        <div className="konva-context-menu" style={{ left: contextMenu.x, top: contextMenu.y }} onPointerDown={(event) => event.stopPropagation()}>
          {contextAnswerTargets.length ? (
            contextAnswerTargets.every((shape) => shape.interaction) ? (
              <button
                type="button"
                onClick={() => {
                  onRestoreShapesFromAnswer?.(contextAnswerTargets.map((shape) => shape.id));
                  setContextMenu(null);
                }}
              >
                일반 도형으로 되돌리기
              </button>
            ) : (
              <button
                type="button"
                onClick={() => {
                  onConvertShapesToAnswer?.(contextAnswerTargets.map((shape) => shape.id));
                  setContextMenu(null);
                }}
              >
                AnswerSlot으로 변환
              </button>
            )
          ) : null}
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

function TutorOverlayLayer({
  overlays,
  shapesById,
  activeOverlayIndex,
  onOverlaySelect,
  onOverlayTextEditStart,
  onOverlayMove,
}: {
  overlays: TutorRendererOverlay[];
  shapesById: Map<string, EditorShape>;
  activeOverlayIndex: number | null;
  onOverlaySelect?: (overlayIndex: number | null) => void;
  onOverlayTextEditStart?: (
    overlayIndex: number,
    overlay: TutorRendererOverlay,
    metrics: { width: number; fontSize: number; fill: string },
  ) => void;
  onOverlayMove?: (overlayIndex: number, x: number, y: number) => void;
}) {
  if (!overlays.length) return null;
  return (
    <>
      {overlays.map((overlay, index) => {
        if (overlay.type === "highlight" && overlay.target_ref) {
          const shape = shapesById.get(overlay.target_ref);
          if (!shape) return null;
          return <TutorHighlight key={`highlight-${overlay.target_ref}-${index}`} shape={shape} />;
        }
        if (overlay.type === "label" && typeof overlay.text === "string" && typeof overlay.x === "number" && typeof overlay.y === "number") {
          const style = isRecord(overlay.style) ? overlay.style : {};
          const fontSize = numberStyle(style.font_size, 22);
          const fill = stringStyle(style.fill, "#0f766e");
          const width = Math.max(120, overlay.text.length * fontSize * 0.62 + 24);
          const isActive = activeOverlayIndex === index;
          const canEdit = Boolean(onOverlayMove);
          return (
            <Text
              key={`label-${index}`}
              x={overlay.x}
              y={overlay.y}
              text={overlay.text}
              fontSize={fontSize}
              fontFamily="Noto Sans KR, sans-serif"
              fill={fill}
              width={width}
              height={fontSize * 1.45}
              padding={4}
              draggable={canEdit}
              listening={canEdit}
              stroke={isActive ? "#0f766e" : undefined}
              strokeWidth={isActive ? 0.5 : 0}
              onMouseDown={(event) => {
                event.cancelBubble = true;
                onOverlaySelect?.(index);
              }}
              onTouchStart={(event) => {
                event.cancelBubble = true;
                onOverlaySelect?.(index);
              }}
              onDblClick={(event) => {
                event.cancelBubble = true;
                onOverlayTextEditStart?.(index, overlay, { width, fontSize, fill });
              }}
              onDblTap={(event) => {
                event.cancelBubble = true;
                onOverlayTextEditStart?.(index, overlay, { width, fontSize, fill });
              }}
              onDragStart={(event) => {
                event.cancelBubble = true;
                onOverlaySelect?.(index);
              }}
              onDragEnd={(event) => {
                onOverlaySelect?.(index);
                onOverlayMove?.(index, roundCanvasNumber(event.target.x()), roundCanvasNumber(event.target.y()));
              }}
            />
          );
        }
        return null;
      })}
    </>
  );
}

function roundCanvasNumber(value: number): number {
  return Math.round(value * 100) / 100;
}

function TutorHighlight({ shape }: { shape: EditorShape }) {
  const common = {
    stroke: "#0f766e",
    strokeWidth: 5,
    dash: [8, 5],
    opacity: 0.92,
    listening: false,
  };
  if (shape.type === "circle") {
    return <Circle x={shape.x} y={shape.y} radius={shape.radius + 5} {...common} fill="rgba(15, 118, 110, 0.08)" />;
  }
  if (shape.type === "line") {
    return (
      <Line
        x={shape.x}
        y={shape.y}
        points={shape.points}
        rotation={shape.rotation ?? 0}
        offsetX={shape.offsetX ?? 0}
        offsetY={shape.offsetY ?? 0}
        lineCap="round"
        {...common}
      />
    );
  }
  if (shape.type === "path") {
    return (
      <Path
        x={shape.x}
        y={shape.y}
        data={shape.d}
        rotation={shape.rotation ?? 0}
        offsetX={shape.offsetX ?? 0}
        offsetY={shape.offsetY ?? 0}
        fill="rgba(15, 118, 110, 0.04)"
        {...common}
      />
    );
  }
  if (shape.type === "connector") {
    return (
      <Path
        x={shape.x}
        y={shape.y}
        data={connectorPathData(shape)}
        rotation={shape.rotation ?? 0}
        offsetX={shape.offsetX ?? 0}
        offsetY={shape.offsetY ?? 0}
        fill="rgba(15, 118, 110, 0.04)"
        {...common}
      />
    );
  }
  const bounds = paddedRect(shapeBounds(shape), 6);
  return (
    <Rect
      x={bounds.x}
      y={bounds.y}
      width={bounds.width}
      height={bounds.height}
      fill="rgba(15, 118, 110, 0.10)"
      cornerRadius={8}
      {...common}
    />
  );
}

function AnswerSlotOverlay({ shape }: { shape: EditorShape }) {
  const bounds = paddedRect(shapeBounds(shape), 5);
  const interaction = shape.interaction;
  const inputStyle = shape.input_style;
  if (!interaction) return null;
  const fontSize = calculateAnswerPreviewFontSize(shape);
  const label = [
    interaction.role ?? "answer",
    interaction.value_type ?? "digit",
    interaction.max_length ? `${interaction.max_length}자` : null,
    inputStyle?.font_size_mode === "fixed" ? `${inputStyle.font_size ?? fontSize}px` : `${fontSize}px`,
  ]
    .filter(Boolean)
    .join(" · ");
  return (
    <>
      <Rect
        x={bounds.x}
        y={bounds.y}
        width={bounds.width}
        height={bounds.height}
        stroke="#2563eb"
        strokeWidth={1.2}
        dash={[5, 4]}
        fill="rgba(37, 99, 235, 0.05)"
        listening={false}
      />
      <Text
        x={bounds.x}
        y={Math.max(0, bounds.y - 18)}
        text={label}
        fontSize={11}
        fontFamily="Noto Sans KR, sans-serif"
        fill="#1d4ed8"
        listening={false}
      />
    </>
  );
}

function calculateAnswerPreviewFontSize(shape: EditorShape): number {
  const bounds = shapeBounds(shape);
  const style = shape.input_style;
  if (style?.font_size_mode === "fixed" && typeof style.font_size === "number") return Math.round(style.font_size);
  const maxLength = Math.max(1, shape.interaction?.max_length ?? (shape.interaction?.value_type === "integer" ? 3 : 1));
  const padding = style?.padding ?? 6;
  const availableWidth = Math.max(1, bounds.width - padding * 2);
  const availableHeight = Math.max(1, bounds.height - padding * 2);
  const byHeight = availableHeight * 0.68;
  const byWidth = availableWidth / maxLength / characterWidthRatio(shape.interaction?.value_type);
  const adjusted = Math.min(byHeight, byWidth) + (style?.font_size_adjust ?? 0);
  return Math.round(clamp(adjusted, style?.min_font_size ?? 14, style?.max_font_size ?? 52));
}

function characterWidthRatio(valueType: string | undefined): number {
  if (valueType === "digit") return 0.58;
  if (valueType === "integer") return 0.6;
  if (valueType === "decimal") return 0.62;
  if (valueType === "fraction") return 0.72;
  if (valueType === "text") return 0.92;
  return 0.7;
}

function compareRenderOrder(a: EditorShape, b: EditorShape): number {
  return renderPriority(a) - renderPriority(b);
}

function renderPriority(shape: EditorShape): number {
  if (shape.type === "text" || shape.type === "math") return 2;
  if (shape.type === "line" || shape.type === "connector") return 1;
  return 0;
}

function canOpenShapeContextMenu(shape: EditorShape): boolean {
  return shape.type === "line" || shape.type === "connector" || isAnswerSlotShape(shape);
}

function isAnswerSlotShape(shape: EditorShape): boolean {
  return shape.type === "rect" || shape.type === "circle" || shape.type === "path" || shape.type === "text";
}

interface CanvasRect {
  x: number;
  y: number;
  width: number;
  height: number;
}

export interface CanvasPoint {
  x: number;
  y: number;
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
  if (shape.type === "connector") {
    return connectorBounds(shape);
  }
  if (shape.type === "text") {
    return { x: shape.x, y: shape.y, width: shape.width ?? Math.max(24, shape.text.length * shape.fontSize * 0.55), height: shape.height ?? shape.fontSize * 1.3 };
  }
  if (shape.type === "path") {
    return { x: shape.x, y: shape.y, width: shape.width, height: shape.height };
  }
  return { x: shape.x, y: shape.y, width: shape.width, height: shape.height };
}

function paddedRect(rect: CanvasRect, padding: number): CanvasRect {
  return {
    x: rect.x - padding,
    y: rect.y - padding,
    width: rect.width + padding * 2,
    height: rect.height + padding * 2,
  };
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function numberStyle(value: unknown, fallback: number): number {
  return typeof value === "number" && Number.isFinite(value) ? value : fallback;
}

function stringStyle(value: unknown, fallback: string): string {
  return typeof value === "string" && value.trim() ? value : fallback;
}

function previewShapeForDrawing(preset: ShapePreset, start: CanvasPoint, end: CanvasPoint, points: CanvasPoint[] = []): EditorShape {
  const stroke = "#111827";
  const strokeWidth = 1.2;
  const connectorKind = connectorKindForPreset(preset);
  if (connectorKind) {
    return {
      id: "drawing.preview",
      type: "connector",
      kind: connectorKind,
      x: start.x,
      y: start.y,
      start: { x: 0, y: 0 },
      end: { x: end.x - start.x, y: end.y - start.y },
      control: defaultPreviewConnectorControl(connectorKind, start, end),
      ...connectorArrowForPreset(preset),
      stroke,
      strokeWidth,
    };
  }
  if (preset === "line") {
    return {
      id: "drawing.preview",
      type: "line",
      x: start.x,
      y: start.y,
      points: [0, 0, end.x - start.x, end.y - start.y],
      stroke,
      strokeWidth,
    };
  }
  const bounds = normalizeRect(start.x, start.y, end.x - start.x, end.y - start.y);
  const width = Math.max(1, bounds.width);
  const height = Math.max(1, bounds.height);
  return {
    id: "drawing.preview",
    type: "path",
    x: bounds.x,
    y: bounds.y,
    width,
    height,
    d: pathForDrawingPreset(preset, start, end, points, bounds),
    fill: preset === "freeformShape" ? "rgba(255,255,255,0.01)" : "none",
    stroke,
    strokeWidth,
  };
}

function defaultPreviewConnectorControl(kind: "straight" | "elbow" | "curve", start: CanvasPoint, end: CanvasPoint): { x: number; y: number } | undefined {
  const dx = end.x - start.x;
  const dy = end.y - start.y;
  if (kind === "straight") return undefined;
  if (kind === "curve") {
    const lift = Math.max(24, Math.min(90, Math.hypot(dx, dy) * 0.22));
    return { x: dx / 2, y: dy / 2 - lift };
  }
  return { x: dx / 2, y: dy / 2 };
}

function pathForDrawingPreset(
  preset: ShapePreset,
  start: CanvasPoint,
  end: CanvasPoint,
  points: CanvasPoint[],
  bounds: CanvasRect,
): string {
  const a = { x: start.x - bounds.x, y: start.y - bounds.y };
  const b = { x: end.x - bounds.x, y: end.y - bounds.y };
  const dx = b.x - a.x;
  const dy = b.y - a.y;
  if (preset === "elbow" || preset === "elbowArrow" || preset === "elbowDoubleArrow") {
    const mid = { x: a.x, y: b.y };
    return withArrowHeads(`M ${a.x} ${a.y} L ${mid.x} ${mid.y} L ${b.x} ${b.y}`, [a, mid, b], arrowMode(preset));
  }
  if (preset === "curvedConnector" || preset === "curvedArrow" || preset === "curvedDoubleArrow" || preset === "curve") {
    const lift = Math.max(20, Math.min(90, Math.hypot(dx, dy) * 0.28));
    const c1 = { x: a.x + dx * 0.34, y: a.y - lift };
    const c2 = { x: a.x + dx * 0.66, y: b.y - lift };
    return withArrowHeads(`M ${a.x} ${a.y} C ${c1.x} ${c1.y}, ${c2.x} ${c2.y}, ${b.x} ${b.y}`, [a, c1, c2, b], arrowMode(preset));
  }
  if (preset === "freeformScribble" && points.length > 1) {
    const local = points.map((point) => ({ x: point.x - bounds.x, y: point.y - bounds.y }));
    return local.map((point, index) => `${index === 0 ? "M" : "L"} ${point.x} ${point.y}`).join(" ");
  }
  if (preset === "freeformShape") {
    const c = { x: a.x + dx * 0.48, y: a.y + dy * 0.18 - 22 };
    const d = { x: a.x + dx * 0.84, y: a.y + dy * 0.78 };
    return `M ${a.x} ${a.y} L ${c.x} ${c.y} L ${b.x} ${b.y} L ${d.x} ${d.y} Z`;
  }
  return withArrowHeads(`M ${a.x} ${a.y} L ${b.x} ${b.y}`, [a, b], arrowMode(preset));
}

function arrowMode(preset: ShapePreset): "none" | "end" | "both" {
  if (preset === "doubleArrow" || preset === "elbowDoubleArrow" || preset === "curvedDoubleArrow") return "both";
  if (preset === "arrow" || preset === "elbowArrow" || preset === "curvedArrow") return "end";
  return "none";
}

function withArrowHeads(path: string, points: CanvasPoint[], mode: "none" | "end" | "both"): string {
  if (mode === "none" || points.length < 2) return path;
  const parts = [path];
  if (mode === "end" || mode === "both") parts.push(arrowHeadPath(points[points.length - 2], points[points.length - 1]));
  if (mode === "both") parts.push(arrowHeadPath(points[1], points[0]));
  return parts.join(" ");
}

function arrowHeadPath(from: CanvasPoint, to: CanvasPoint): string {
  const angle = Math.atan2(to.y - from.y, to.x - from.x);
  const length = 11;
  const spread = Math.PI / 7;
  const left = {
    x: to.x - Math.cos(angle - spread) * length,
    y: to.y - Math.sin(angle - spread) * length,
  };
  const right = {
    x: to.x - Math.cos(angle + spread) * length,
    y: to.y - Math.sin(angle + spread) * length,
  };
  return `M ${to.x} ${to.y} L ${left.x} ${left.y} M ${to.x} ${to.y} L ${right.x} ${right.y}`;
}

function appendFreeformPoint(points: CanvasPoint[], point: CanvasPoint): CanvasPoint[] {
  const last = points[points.length - 1];
  if (last && Math.hypot(point.x - last.x, point.y - last.y) < 3) return points;
  return [...points, point];
}

function shapeLongEnough(shape: EditorShape): boolean {
  if (shape.type === "line") return Math.hypot(shape.points[2] ?? 0, shape.points[3] ?? 0) >= 4;
  if (shape.type === "connector") return Math.hypot(shape.end.x - shape.start.x, shape.end.y - shape.start.y) >= 4;
  if (shape.type === "path" || shape.type === "rect" || shape.type === "image" || shape.type === "math") {
    return Math.max(shape.width, shape.height) >= 4;
  }
  if (shape.type === "text") return Math.max(shape.width ?? 0, shape.height ?? 0) >= 4;
  if (shape.type === "circle") return shape.radius >= 2;
  return false;
}

function drawingEndPoint(shape: EditorShape): CanvasPoint {
  if (shape.type === "line") {
    return { x: shape.x + (shape.points[2] ?? 0), y: shape.y + (shape.points[3] ?? 0) };
  }
  if (shape.type === "connector") {
    return connectorPointToCanvasPoint(shape, connectorEnd(shape));
  }
  if (shape.type === "path" || shape.type === "rect" || shape.type === "image" || shape.type === "math") {
    return { x: shape.x + shape.width, y: shape.y + shape.height };
  }
  return { x: shape.x, y: shape.y };
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
        radius={5}
        fill="#ffffff"
        stroke="#6b7280"
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
        radius={5}
        fill="#ffffff"
        stroke="#6b7280"
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

function ConnectorHandles({
  connector,
  onEndpointDrag,
  onControlDrag,
}: {
  connector: ConnectorShape;
  onEndpointDrag: (endpoint: "start" | "end", event: Konva.KonvaEventObject<DragEvent>) => void;
  onControlDrag: (event: Konva.KonvaEventObject<DragEvent>) => void;
}) {
  const start = connectorPointToCanvasPoint(connector, connectorStart(connector));
  const end = connectorPointToCanvasPoint(connector, connectorEnd(connector));
  const control = connector.kind === "straight" ? null : connectorPointToCanvasPoint(connector, connectorControl(connector));
  return (
    <>
      <Circle
        x={start.x}
        y={start.y}
        radius={5}
        fill="#ffffff"
        stroke="#6b7280"
        strokeWidth={2}
        draggable
        onMouseDown={(event) => {
          event.cancelBubble = true;
        }}
        onTouchStart={(event) => {
          event.cancelBubble = true;
        }}
        onDragMove={(event) => onEndpointDrag("start", event)}
        onDragEnd={(event) => onEndpointDrag("start", event)}
      />
      <Circle
        x={end.x}
        y={end.y}
        radius={5}
        fill="#ffffff"
        stroke="#6b7280"
        strokeWidth={2}
        draggable
        onMouseDown={(event) => {
          event.cancelBubble = true;
        }}
        onTouchStart={(event) => {
          event.cancelBubble = true;
        }}
        onDragMove={(event) => onEndpointDrag("end", event)}
        onDragEnd={(event) => onEndpointDrag("end", event)}
      />
      {control ? (
        <Circle
          x={control.x}
          y={control.y}
          radius={6}
          fill="#facc15"
          stroke="#6b7280"
          strokeWidth={2}
          draggable
          onMouseDown={(event) => {
            event.cancelBubble = true;
          }}
          onTouchStart={(event) => {
            event.cancelBubble = true;
          }}
          onDragMove={onControlDrag}
          onDragEnd={onControlDrag}
        />
      ) : null}
    </>
  );
}

function PathAdjustmentHandle({
  shape,
  onDragMove,
  onDragEnd,
}: {
  shape: Extract<EditorShape, { type: "path" }>;
  onDragMove: (event: Konva.KonvaEventObject<DragEvent>) => void;
  onDragEnd: (event: Konva.KonvaEventObject<DragEvent>) => void;
}) {
  const point = adjustableShapePoint(shape);
  if (!point) return null;
  const canvasPoint = localPathPointToCanvasPoint(shape, point);
  return (
    <Circle
      x={canvasPoint.x}
      y={canvasPoint.y}
      radius={6}
      fill="#facc15"
      stroke="#6b7280"
      strokeWidth={2}
      draggable
      onMouseDown={(event) => {
        event.cancelBubble = true;
      }}
      onTouchStart={(event) => {
        event.cancelBubble = true;
      }}
      onDragMove={onDragMove}
      onDragEnd={onDragEnd}
    />
  );
}

function localPathPointToCanvasPoint(shape: Extract<EditorShape, { type: "path" }>, point: { x: number; y: number }): { x: number; y: number } {
  const rotation = degreesToRadians(shape.rotation ?? 0);
  const localX = point.x - (shape.offsetX ?? 0);
  const localY = point.y - (shape.offsetY ?? 0);
  const cos = Math.cos(rotation);
  const sin = Math.sin(rotation);
  return {
    x: shape.x + localX * cos - localY * sin,
    y: shape.y + localX * sin + localY * cos,
  };
}

function canvasPointToLocalPathPoint(shape: Extract<EditorShape, { type: "path" }>, point: { x: number; y: number }): { x: number; y: number } {
  const rotation = degreesToRadians(-(shape.rotation ?? 0));
  const dx = point.x - shape.x;
  const dy = point.y - shape.y;
  const cos = Math.cos(rotation);
  const sin = Math.sin(rotation);
  return {
    x: dx * cos - dy * sin + (shape.offsetX ?? 0),
    y: dx * sin + dy * cos + (shape.offsetY ?? 0),
  };
}

function connectorPointToCanvasPoint(connector: ConnectorShape, point: { x: number; y: number }): { x: number; y: number } {
  const rotation = degreesToRadians(connector.rotation ?? 0);
  const localX = point.x - (connector.offsetX ?? 0);
  const localY = point.y - (connector.offsetY ?? 0);
  const cos = Math.cos(rotation);
  const sin = Math.sin(rotation);
  return {
    x: connector.x + localX * cos - localY * sin,
    y: connector.y + localX * sin + localY * cos,
  };
}

function localLinePointToCanvasPoint(line: LineShape, point: { x: number; y: number }): { x: number; y: number } {
  const rotation = degreesToRadians(line.rotation ?? 0);
  const localX = point.x - (line.offsetX ?? 0);
  const localY = point.y - (line.offsetY ?? 0);
  const cos = Math.cos(rotation);
  const sin = Math.sin(rotation);
  return {
    x: line.x + localX * cos - localY * sin,
    y: line.y + localX * sin + localY * cos,
  };
}

function degreesToRadians(degrees: number): number {
  return (degrees * Math.PI) / 180;
}

function roundStageNumber(value: number): number {
  return Math.round(value * 100) / 100;
}

function clamp(value: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, value));
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
      adjustment: shape.adjustment ? { x: shape.adjustment.x * scaleX, y: shape.adjustment.y * scaleY } : undefined,
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
  if (shape.type === "connector") {
    return {
      ...shape,
      x: node.x(),
      y: node.y(),
      rotation: node.rotation(),
      start: { x: shape.start.x * scaleX, y: shape.start.y * scaleY },
      end: { x: shape.end.x * scaleX, y: shape.end.y * scaleY },
      control: shape.control ? { x: shape.control.x * scaleX, y: shape.control.y * scaleY } : undefined,
    };
  }
  return shape;
}
