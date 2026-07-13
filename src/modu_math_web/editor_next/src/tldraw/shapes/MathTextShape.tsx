import { HTMLContainer, Rectangle2d, ShapeUtil, T, type TLResizeInfo } from "tldraw";
import type { MathTextShape } from "./types";

export class MathTextShapeUtil extends ShapeUtil<MathTextShape> {
  static override type = "math_text" as const;

  static override props = {
    latex: T.string,
    text: T.string,
    fontSize: T.number,
    w: T.number,
    h: T.number,
    color: T.string,
    textAlign: T.literalEnum("left", "center", "right"),
    lineHeight: T.number,
    sourceKind: T.literalEnum("text", "text_box"),
  };

  override getDefaultProps(): MathTextShape["props"] {
    return {
      latex: "3 + 4 = []",
      text: "3 + 4 = []",
      fontSize: 36,
      w: 260,
      h: 64,
      color: "#050816",
      textAlign: "left",
      lineHeight: 1.25,
      sourceKind: "text_box",
    };
  }

  override getGeometry(shape: MathTextShape) {
    return new Rectangle2d({ width: shape.props.w, height: shape.props.h, isFilled: true });
  }

  override component(shape: MathTextShape) {
    const rawText = shape.props.text || shape.props.latex || "";
    const lines = shape.props.sourceKind === "text_box" ? wrapText(rawText, shape.props.w, shape.props.fontSize) : rawText.split(/\n/g);
    const anchor = shape.props.textAlign === "center" ? "middle" : shape.props.textAlign === "right" ? "end" : "start";
    const x = shape.props.textAlign === "center" ? shape.props.w / 2 : shape.props.textAlign === "right" ? shape.props.w : 0;
    const lineStep = shape.props.fontSize * shape.props.lineHeight;
    const svgHeight = Math.max(shape.props.h, shape.props.fontSize + Math.max(lines.length - 1, 0) * lineStep);
    return (
      <HTMLContainer className="math-shape math-text-shape" style={{ width: shape.props.w, height: shape.props.h }}>
        {/* TODO: replace plain text with KaTeX/MathJax rendering while preserving props.latex. */}
        <svg width={shape.props.w} height={svgHeight} viewBox={`0 0 ${shape.props.w} ${svgHeight}`}>
          <text
            x={x}
            y={shape.props.fontSize}
            fill={shape.props.color}
            fontSize={shape.props.fontSize}
            textAnchor={anchor}
            fontFamily={'"Noto Sans KR", "Segoe UI", "Pretendard", Arial, sans-serif'}
          >
            {lines.map((line, index) => (
              <tspan key={`${line}-${index}`} x={x} dy={index === 0 ? 0 : lineStep}>
                {line}
              </tspan>
            ))}
          </text>
        </svg>
      </HTMLContainer>
    );
  }

  override getIndicatorPath(shape: MathTextShape) {
    return new Path2D(`M0,0 h${shape.props.w} v${shape.props.h} h-${shape.props.w} Z`);
  }

  override onResize(shape: MathTextShape, info: TLResizeInfo<MathTextShape>) {
    return {
      props: {
        w: Math.max(24, shape.props.w * info.scaleX),
        h: Math.max(24, shape.props.h * info.scaleY),
      },
    };
  }
}

function textUnitWidth(ch: string, fontSize: number): number {
  if (/\s/.test(ch)) return fontSize * 0.35;
  if (ch.codePointAt(0)! < 128) return fontSize * 0.58;
  return fontSize * 0.92;
}

function textWidth(text: string, fontSize: number): number {
  let width = 0;
  for (const ch of text) width += textUnitWidth(ch, fontSize);
  return width;
}

function wrapLongToken(token: string, maxWidth: number, fontSize: number): string[] {
  const lines: string[] = [];
  let current = "";
  for (const ch of token) {
    const trial = current + ch;
    if (current && textWidth(trial, fontSize) > maxWidth) {
      lines.push(current);
      current = ch;
    } else {
      current = trial;
    }
  }
  return current ? [...lines, current] : lines.length ? lines : [token];
}

function wrapText(text: string, maxWidth: number, fontSize: number): string[] {
  if (!Number.isFinite(maxWidth) || maxWidth <= 0) return text.split(/\n/g);
  const out: string[] = [];
  for (const paragraph of text.split(/\n/g)) {
    if (!paragraph) {
      out.push("");
      continue;
    }
    let current = "";
    for (const word of paragraph.split(" ")) {
      for (const piece of wrapLongToken(word, maxWidth, fontSize)) {
        const trial = current ? `${current} ${piece}` : piece;
        if (current && textWidth(trial, fontSize) > maxWidth) {
          out.push(current);
          current = piece;
        } else {
          current = trial;
        }
      }
    }
    if (current) out.push(current);
  }
  return out.length ? out : [""];
}
