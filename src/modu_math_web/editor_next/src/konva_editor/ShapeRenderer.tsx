import { useEffect, useState } from "react";
import { Circle, Group, Image as KonvaImage, Line, Path, Rect, Text } from "react-konva";
import type Konva from "konva";
import type { EditorShape } from "../types/editorShape";
import { connectorPathData } from "./connectorGeometry";
import { estimateWrappedTextHeight, normalizedTextBoxHeight, normalizedTextBoxWidth, parseFractionLatex, type FractionLatex } from "./converters";
import { KONVA_PREVIEW_FONT_FAMILY, normalizePreviewFontFamily } from "./fonts";
import { renderLatexToSvgDataUrl } from "./latexRenderer";
import { pathDataForShape } from "./shapeGeometry";

interface ShapeRendererProps {
  shape: EditorShape;
  isSelected: boolean;
  nodeRef: (node: Konva.Node | null) => void;
  onSelect: (event: Konva.KonvaEventObject<MouseEvent | TouchEvent>) => void;
  onDragStart: (event: Konva.KonvaEventObject<DragEvent>) => void;
  onDragMove: (event: Konva.KonvaEventObject<DragEvent>) => void;
  onDragEnd: (event: Konva.KonvaEventObject<DragEvent>) => void;
  onContextMenu: (event: Konva.KonvaEventObject<MouseEvent>) => void;
}

export function ShapeRenderer({ shape, nodeRef, onSelect, onDragStart, onDragMove, onDragEnd, onContextMenu }: ShapeRendererProps) {
  const common = {
    id: shape.id,
    ref: nodeRef,
    x: shape.x,
    y: shape.y,
    rotation: shape.rotation ?? 0,
    offsetX: shape.offsetX ?? 0,
    offsetY: shape.offsetY ?? 0,
    opacity: shape.opacity ?? 1,
    visible: shape.visible ?? true,
    draggable: !shape.locked,
    onClick: onSelect,
    onTap: onSelect,
    onDragStart,
    onDragMove,
    onDragEnd,
    onContextMenu,
  };

  switch (shape.type) {
    case "rect":
      return (
        <Rect
          {...common}
          width={shape.width}
          height={shape.height}
          fill={normalizeFill(shape.fill)}
          stroke={shape.stroke ?? "#111827"}
          strokeWidth={shape.strokeWidth ?? 1}
          cornerRadius={shape.cornerRadius ?? 0}
        />
      );
    case "circle":
      return (
        <Circle
          {...common}
          radius={shape.radius}
          fill={normalizeFill(shape.fill)}
          stroke={shape.stroke ?? "#111827"}
          strokeWidth={shape.strokeWidth ?? 1}
        />
      );
    case "line":
      return (
        <Line
          {...common}
          points={shape.points}
          stroke={shape.stroke ?? "#111827"}
          strokeWidth={shape.strokeWidth ?? 1.2}
          dash={dashArray(shape.strokeDasharray)}
          hitStrokeWidth={Math.max(12, (shape.strokeWidth ?? 1.2) + 8)}
          lineCap="round"
        />
      );
    case "connector":
      return (
        <Path
          {...common}
          data={connectorPathData(shape)}
          fill="transparent"
          stroke={shape.stroke ?? "#111827"}
          strokeWidth={shape.strokeWidth ?? 1.2}
          dash={dashArray(shape.strokeDasharray)}
          hitStrokeWidth={Math.max(12, (shape.strokeWidth ?? 1.2) + 8)}
          lineCap="round"
          lineJoin="round"
        />
      );
    case "path":
      return (
        <Path
          {...common}
          data={pathDataForShape(shape)}
          fill={normalizeFill(shape.fill)}
          stroke={shape.stroke ?? "#111827"}
          strokeWidth={shape.strokeWidth ?? 1.2}
          dash={dashArray(shape.strokeDasharray)}
          lineCap="round"
          lineJoin="round"
        />
      );
    case "text":
      const textWidth =
        shape.sourceKind === "text_box" && typeof shape.width === "number"
          ? normalizedTextBoxWidth(shape.text, shape.fontSize, shape.width, shape.align ?? "left")
          : shape.width;
      const textHeight =
        typeof textWidth === "number"
          ? normalizedTextBoxHeight(shape.text, shape.fontSize, textWidth, shape.height, shape.lineHeight ?? 1.25, shape.fontFamily, Boolean(shape.interaction))
          : undefined;
      return (
        <Text
          {...common}
          text={shape.text}
          fontSize={shape.fontSize}
          fontFamily={normalizePreviewFontFamily(shape.fontFamily)}
          fill={shape.fill ?? "#111827"}
          width={textWidth}
          height={textHeight}
          align={shape.align ?? "left"}
          lineHeight={shape.lineHeight ?? 1.25}
        />
      );
    case "image":
      return <ImageShapeRenderer shape={shape} common={common} />;
    case "math":
      return <MathShapeRenderer shape={shape} common={common} />;
    case "baseTenBlock":
      return <BaseTenBlockRenderer shape={shape} common={common} />;
  }
}

function BaseTenBlockRenderer({
  shape,
  common,
}: {
  shape: Extract<EditorShape, { type: "baseTenBlock" }>;
  common: Record<string, unknown>;
}) {
  const stroke = shape.stroke ?? "#7ea86f";
  const strokeWidth = shape.strokeWidth ?? 0.8;
  const frontFill = normalizeFill(shape.fill ?? "#b9dd9f");
  const topFill = normalizeFill(shape.topFill ?? "#d2edbf");
  const sideFill = normalizeFill(shape.sideFill ?? "#9fcd86");
  const grid = baseTenGridSpec(shape.kind);
  const depth = normalizedBaseTenDepth(shape, grid);
  const frontY = depth;

  return (
    <Group {...common}>
      <Path
        data={`M 0 ${frontY} L ${depth} 0 L ${shape.width + depth} 0 L ${shape.width} ${frontY} Z`}
        fill={topFill}
        stroke={stroke}
        strokeWidth={strokeWidth}
        lineJoin="round"
      />
      <Path
        data={`M ${shape.width} ${frontY} L ${shape.width + depth} 0 L ${shape.width + depth} ${shape.height} L ${shape.width} ${
          shape.height + frontY
        } Z`}
        fill={sideFill}
        stroke={stroke}
        strokeWidth={strokeWidth}
        lineJoin="round"
      />
      <Rect x={0} y={frontY} width={shape.width} height={shape.height} fill={frontFill} stroke={stroke} strokeWidth={strokeWidth} />
      {grid.rows > 1 || grid.cols > 1 || grid.depthSegments > 1 ? (
        <BaseTenGridLines width={shape.width} height={shape.height} depth={depth} frontY={frontY} grid={grid} stroke={stroke} />
      ) : null}
    </Group>
  );
}

function baseTenGridSpec(kind: Extract<EditorShape, { type: "baseTenBlock" }>["kind"]): { rows: number; cols: number; depthSegments: number } {
  switch (kind) {
    case "thousand":
      return { rows: 10, cols: 10, depthSegments: 10 };
    case "hundred":
      return { rows: 10, cols: 10, depthSegments: 1 };
    case "ten":
      return { rows: 10, cols: 1, depthSegments: 1 };
    case "one":
      return { rows: 1, cols: 1, depthSegments: 1 };
  }
}

function normalizedBaseTenDepth(
  shape: Extract<EditorShape, { type: "baseTenBlock" }>,
  grid: { rows: number; cols: number; depthSegments: number },
): number {
  const cellWidth = shape.width / grid.cols;
  const cellHeight = shape.height / grid.rows;
  const unitDepth = Math.min(cellWidth, cellHeight) / Math.SQRT2;
  return Math.max(0, unitDepth * grid.depthSegments);
}
function BaseTenGridLines({
  width,
  height,
  depth,
  frontY,
  grid,
  stroke,
}: {
  width: number;
  height: number;
  depth: number;
  frontY: number;
  grid: { rows: number; cols: number; depthSegments: number };
  stroke: string;
}) {
  const lines = [];
  for (let i = 1; i < grid.cols; i += 1) {
    const x = (width / grid.cols) * i;
    lines.push(<Line key={`front-v-${i}`} points={[x, frontY, x, frontY + height]} stroke={stroke} strokeWidth={0.38} listening={false} />);
    if (depth > 0) {
      lines.push(<Line key={`top-col-${i}`} points={[x, frontY, x + depth, 0]} stroke={stroke} strokeWidth={0.32} listening={false} />);
    }
  }
  for (let i = 1; i < grid.rows; i += 1) {
    const y = frontY + (height / grid.rows) * i;
    lines.push(<Line key={`front-h-${i}`} points={[0, y, width, y]} stroke={stroke} strokeWidth={0.38} listening={false} />);
    if (depth > 0) {
      lines.push(<Line key={`side-row-${i}`} points={[width, y, width + depth, y - depth]} stroke={stroke} strokeWidth={0.32} listening={false} />);
    }
  }
  for (let i = 1; i < grid.depthSegments; i += 1) {
    const d = (depth / grid.depthSegments) * i;
    lines.push(<Line key={`top-depth-${i}`} points={[d, frontY - d, width + d, frontY - d]} stroke={stroke} strokeWidth={0.32} listening={false} />);
    lines.push(<Line key={`side-depth-${i}`} points={[width + d, frontY - d, width + d, frontY - d + height]} stroke={stroke} strokeWidth={0.32} listening={false} />);
  }
  return <>{lines}</>;
}

function ImageShapeRenderer({ shape, common }: { shape: Extract<EditorShape, { type: "image" }>; common: Record<string, unknown> }) {
  const image = useLoadedImage(shape.src);
  if (!image) {
    return (
      <Group {...common}>
        <Rect width={shape.width} height={shape.height} fill="#f8fafc" stroke="#94a3b8" dash={[6, 4]} />
        <Text width={shape.width} height={shape.height} text="Image" align="center" verticalAlign="middle" fill="#64748b" />
      </Group>
    );
  }
  const fit = fitImageInBox(image, shape.width, shape.height, shape.preserveAspectRatio);
  return (
    <Group {...common}>
      <KonvaImage image={image} x={fit.x} y={fit.y} width={fit.width} height={fit.height} />
    </Group>
  );
}

function MathShapeRenderer({ shape, common }: { shape: Extract<EditorShape, { type: "math" }>; common: Record<string, unknown> }) {
  const fontSize = shape.fontSize ?? 28;
  const textHeight = Math.max(shape.height, estimateWrappedTextHeight(shape.latex, fontSize, shape.width));
  const fraction = parseFractionLatex(shape.latex);
  const image = useRenderedLatexImage(shape.latex, !fraction);

  if (fraction) {
    return <FractionShapeRenderer shape={shape} fraction={fraction} common={common} fontSize={fontSize} width={shape.width} height={shape.height} />;
  }

  if (image) {
    const fit = fitImageInBox(image, shape.width, shape.height, "xMinYMid meet");
    return (
      <Group {...common}>
        <Rect width={shape.width} height={shape.height} fill="#ffffff" />
        <KonvaImage image={image} x={fit.x} y={fit.y} width={fit.width} height={fit.height} />
      </Group>
    );
  }

  return (
    <Group {...common}>
      <Rect width={shape.width} height={Math.max(shape.height, textHeight)} fill="#ffffff" stroke="#94a3b8" dash={[5, 3]} cornerRadius={4} />
      <Text
        x={0}
        y={0}
        width={shape.width}
        height={textHeight}
        text={shape.latex || "ƒ(x)"}
        fontSize={fontSize}
        fontFamily={KONVA_PREVIEW_FONT_FAMILY}
        fill="#111827"
        verticalAlign="top"
      />
    </Group>
  );
}

function estimateMathDigitWidth(text: string, fontSize: number): number {
  let width = 0;
  for (const ch of text) {
    if (ch === "1" || ch === "l" || ch === "i" || ch === "." || ch === ",") {
      width += fontSize * 0.36;
    } else {
      width += fontSize * 0.58;
    }
  }
  return Math.max(fontSize * 0.36, width);
}

function FractionShapeRenderer({
  shape,
  fraction,
  common,
  fontSize,
  width,
  height,
}: {
  shape: Extract<EditorShape, { type: "math" }>;
  fraction: FractionLatex;
  common: Record<string, unknown>;
  fontSize: number;
  width: number;
  height: number;
}) {
  const color = shape.color ?? "#111827";
  const smallFont = Math.max(16, fontSize * 0.78);
  const numeratorWidth = estimateMathDigitWidth(fraction.numerator, smallFont);
  const denominatorWidth = estimateMathDigitWidth(fraction.denominator, smallFont);
  const fractionWidth = Math.max(18, Math.max(numeratorWidth, denominatorWidth) + smallFont * 0.35);
  const fractionHeight = smallFont * 2.25;
  const wholeTextWidth = fraction.whole ? estimateMathDigitWidth(fraction.whole, fontSize) : 0;
  const gap = fraction.whole ? Math.max(3, Math.round(fontSize * 0.15)) : 0;
  const wholeWidth = fraction.whole ? wholeTextWidth + gap : 0;
  const contentWidth = wholeWidth + fractionWidth;
  const contentHeight = Math.max(fractionHeight, fontSize * 1.2);
  const startX = Math.max(0, (width - contentWidth) / 2);
  const effectiveHeight = Math.min(height, Math.max(50, fontSize * 2.4));
  const startY = Math.max(0, (effectiveHeight - contentHeight) / 2);
  const fractionX = startX + wholeWidth;
  const lineY = startY + smallFont * 1.08;

  return (
    <Group {...common}>
      {shape.fill && shape.fill !== "none" ? <Rect width={width} height={height} fill={normalizeFill(shape.fill)} /> : null}
      {fraction.whole ? (
        <Text
          x={startX}
          y={startY + (contentHeight - fontSize) / 2}
          text={fraction.whole}
          fontSize={fontSize}
          fontFamily={KONVA_PREVIEW_FONT_FAMILY}
          fill={color}
        />
      ) : null}
      <Text
        x={fractionX}
        y={startY}
        width={fractionWidth}
        text={fraction.numerator}
        fontSize={smallFont}
        fontFamily={KONVA_PREVIEW_FONT_FAMILY}
        fill={color}
        align="center"
      />
      <Line points={[fractionX, lineY, fractionX + fractionWidth, lineY]} stroke={color} strokeWidth={2.2} />
      <Text
        x={fractionX}
        y={lineY + 4}
        width={fractionWidth}
        text={fraction.denominator}
        fontSize={smallFont}
        fontFamily={KONVA_PREVIEW_FONT_FAMILY}
        fill={color}
        align="center"
      />
    </Group>
  );
}

function estimatePlainTextWidth(text: string, fontSize: number): number {
  return Math.max(fontSize, text.length * fontSize * 0.62);
}

function useRenderedLatexImage(latex: string, enabled: boolean): HTMLImageElement | null {
  const [image, setImage] = useState<HTMLImageElement | null>(null);

  useEffect(() => {
    let cancelled = false;
    setImage(null);
    if (!enabled) return () => {
      cancelled = true;
    };
    renderLatexToSvgDataUrl(latex).then((dataUrl) => {
      if (cancelled || !dataUrl) return;
      const nextImage = new window.Image();
      nextImage.onload = () => {
        if (!cancelled) setImage(nextImage);
      };
      nextImage.onerror = () => {
        if (!cancelled) setImage(null);
      };
      nextImage.src = dataUrl;
    });
    return () => {
      cancelled = true;
    };
  }, [enabled, latex]);

  return image;
}

function useLoadedImage(src: string): HTMLImageElement | null {
  const [image, setImage] = useState<HTMLImageElement | null>(null);

  useEffect(() => {
    if (!src) {
      setImage(null);
      return;
    }
    const nextImage = new window.Image();
    nextImage.crossOrigin = "anonymous";
    nextImage.onload = () => setImage(nextImage);
    nextImage.onerror = () => setImage(null);
    nextImage.src = src;
    return () => {
      nextImage.onload = null;
      nextImage.onerror = null;
    };
  }, [src]);

  return image;
}

function dashArray(value: string | undefined): number[] | undefined {
  if (!value) return undefined;
  const dash = value
    .split(/[\s,]+/)
    .map((part) => Number(part))
    .filter((part) => Number.isFinite(part) && part > 0);
  return dash.length ? dash : undefined;
}

function normalizeFill(fill: string | undefined): string {
  if (!fill || fill === "none") return "transparent";
  return fill;
}

function fitImageInBox(image: HTMLImageElement, boxWidth: number, boxHeight: number, preserveAspectRatio = "xMidYMid meet") {
  const intrinsicWidth = image.naturalWidth || image.width || boxWidth;
  const intrinsicHeight = image.naturalHeight || image.height || boxHeight;
  if (!intrinsicWidth || !intrinsicHeight || preserveAspectRatio.includes("none")) {
    return { x: 0, y: 0, width: boxWidth, height: boxHeight };
  }

  const scale = preserveAspectRatio.includes("slice")
    ? Math.max(boxWidth / intrinsicWidth, boxHeight / intrinsicHeight)
    : Math.min(boxWidth / intrinsicWidth, boxHeight / intrinsicHeight);
  const width = intrinsicWidth * scale;
  const height = intrinsicHeight * scale;
  const x = alignOffset(boxWidth, width, preserveAspectRatio, "xMin", "xMax");
  const y = alignOffset(boxHeight, height, preserveAspectRatio, "YMin", "YMax");
  return { x, y, width, height };
}

function alignOffset(boxSize: number, contentSize: number, preserveAspectRatio: string, minToken: string, maxToken: string): number {
  if (preserveAspectRatio.includes(minToken)) return 0;
  if (preserveAspectRatio.includes(maxToken)) return boxSize - contentSize;
  return (boxSize - contentSize) / 2;
}
