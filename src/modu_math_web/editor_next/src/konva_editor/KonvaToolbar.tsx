import { useEffect, useRef, useState } from "react";

export type ShapePreset =
  | "line"
  | "arrow"
  | "doubleArrow"
  | "elbow"
  | "elbowArrow"
  | "elbowDoubleArrow"
  | "curvedConnector"
  | "curvedArrow"
  | "curvedDoubleArrow"
  | "curve"
  | "freeformShape"
  | "freeformScribble"
  | "arc"
  | "semicircle"
  | "quarterArc"
  | "rect"
  | "roundRect"
  | "circle"
  | "triangle"
  | "rightTriangle"
  | "diamond"
  | "pentagon"
  | "hexagon"
  | "plus"
  | "rightArrow"
  | "leftArrow"
  | "upArrow"
  | "downArrow"
  | "leftRightArrow"
  | "mathPlus"
  | "mathMinus"
  | "mathMultiply"
  | "mathDivide"
  | "flowProcess"
  | "flowDecision"
  | "flowDocument"
  | "flowDatabase"
  | "star"
  | "burst"
  | "ribbon"
  | "calloutRect"
  | "calloutRound"
  | "calloutOval"
  | "calloutCloud";

type ToolName =
  | "newFile"
  | "shapes"
  | "math"
  | "properFraction"
  | "mixedFraction"
  | "text"
  | "image"
  | "table"
  | "graphPaper"
  | "delete"
  | "refresh"
  | "save"
  | "build";

interface KonvaToolbarProps {
  hasSelection: boolean;
  onInsertShape: (preset: ShapePreset) => void;
  onAddMath: () => void;
  onAddProperFraction: () => void;
  onAddMixedFraction: () => void;
  onAddText: () => void;
  onAddImage: () => void;
  onAddTable: () => void;
  onAddGraphPaper: () => void;
  onDeleteSelected: () => void;
  onRefreshJson: () => void;
  onSave: () => void;
  onBuild: () => void;
  onNewFile: () => void;
}

interface IconButtonProps {
  label: string;
  icon: ToolName;
  disabled?: boolean;
  primary?: boolean;
  onClick?: () => void;
}

interface ShapePaletteSection {
  title: string;
  items: Array<{ preset: ShapePreset; label: string }>;
}

const SHAPE_SECTIONS: ShapePaletteSection[] = [
  {
    title: "\uc120",
    items: [
      { preset: "line", label: "\uc120" },
      { preset: "arrow", label: "\uc120 \ud654\uc0b4\ud45c" },
      { preset: "doubleArrow", label: "\uc120 \ud654\uc0b4\ud45c: \uc591\ubc29\ud5a5" },
      { preset: "elbow", label: "\uc5f0\uacb0\uc120: \uaebe\uc784" },
      { preset: "elbowArrow", label: "\uc5f0\uacb0\uc120: \uaebe\uc778 \ud654\uc0b4\ud45c" },
      { preset: "elbowDoubleArrow", label: "\uc5f0\uacb0\uc120: \uaebe\uc778 \uc591\ucabd \ud654\uc0b4\ud45c" },
      { preset: "curvedConnector", label: "\uc5f0\uacb0\uc120: \uad6c\ubd80\ub7ec\uc9d0" },
      { preset: "curvedArrow", label: "\uc5f0\uacb0\uc120: \uad6c\ubd80\ub7ec\uc9c4 \ud654\uc0b4\ud45c" },
      { preset: "curvedDoubleArrow", label: "\uc5f0\uacb0\uc120: \uad6c\ubd80\ub7ec\uc9c4 \uc591\ucabd \ud654\uc0b4\ud45c" },
      { preset: "curve", label: "\uace1\uc120" },
      { preset: "freeformShape", label: "\uc790\uc720\ud615: \ub3c4\ud615" },
      { preset: "freeformScribble", label: "\uc790\uc720\ud615: \uc790\uc720 \uace1\uc120" },
    ],
  },
  {
    title: "선",
    items: [
      { preset: "line", label: "선" },
      { preset: "arrow", label: "선 화살표" },
      { preset: "doubleArrow", label: "선 화살표: 양방향" },
      { preset: "elbow", label: "연결선: 꺾임" },
      { preset: "elbowArrow", label: "연결선: 꺾인 화살표" },
      { preset: "elbowDoubleArrow", label: "연결선: 꺾인 양쪽 화살표" },
      { preset: "curvedConnector", label: "연결선: 구부러짐" },
      { preset: "curvedArrow", label: "연결선: 구부러진 화살표" },
      { preset: "curvedDoubleArrow", label: "연결선: 구부러진 양쪽 화살표" },
      { preset: "curve", label: "곡선" },
      { preset: "freeformShape", label: "자유형: 도형" },
      { preset: "freeformScribble", label: "자유형: 자유 곡선" },
    ],
  },
  {
    title: "사각형",
    items: [
      { preset: "rect", label: "사각형" },
      { preset: "roundRect", label: "둥근 사각형" },
    ],
  },
  {
    title: "기본 도형",
    items: [
      { preset: "circle", label: "원" },
      { preset: "triangle", label: "삼각형" },
      { preset: "rightTriangle", label: "직각 삼각형" },
      { preset: "diamond", label: "마름모" },
      { preset: "pentagon", label: "오각형" },
      { preset: "hexagon", label: "육각형" },
      { preset: "plus", label: "십자" },
    ],
  },
  {
    title: "블록 화살표",
    items: [
      { preset: "rightArrow", label: "오른쪽 화살표" },
      { preset: "leftArrow", label: "왼쪽 화살표" },
      { preset: "upArrow", label: "위쪽 화살표" },
      { preset: "downArrow", label: "아래쪽 화살표" },
      { preset: "leftRightArrow", label: "좌우 화살표" },
    ],
  },
  {
    title: "수식 도형",
    items: [
      { preset: "mathPlus", label: "더하기" },
      { preset: "mathMinus", label: "빼기" },
      { preset: "mathMultiply", label: "곱하기" },
      { preset: "mathDivide", label: "나누기" },
    ],
  },
  {
    title: "순서도",
    items: [
      { preset: "flowProcess", label: "프로세스" },
      { preset: "flowDecision", label: "판단" },
      { preset: "flowDocument", label: "문서" },
      { preset: "flowDatabase", label: "데이터" },
    ],
  },
  {
    title: "별 및 현수막",
    items: [
      { preset: "star", label: "별" },
      { preset: "burst", label: "폭발형" },
      { preset: "ribbon", label: "리본" },
    ],
  },
  {
    title: "설명선",
    items: [
      { preset: "calloutRect", label: "사각 설명선" },
      { preset: "calloutRound", label: "둥근 설명선" },
      { preset: "calloutOval", label: "타원 설명선" },
      { preset: "calloutCloud", label: "구름 설명선" },
    ],
  },
];

function IconButton({ label, icon, disabled, primary, onClick }: IconButtonProps) {
  return (
    <button
      type="button"
      className={primary ? "icon-button primary" : "icon-button"}
      title={label}
      aria-label={label}
      onClick={onClick}
      disabled={disabled}
    >
      <ToolbarIcon name={icon} />
    </button>
  );
}

function ToolbarIcon({ name }: { name: ToolName }) {
  switch (name) {
    case "newFile":
      return (
        <svg viewBox="0 0 24 24" aria-hidden="true" className="new-file-icon">
          <path className="document-shadow" d="M7.2 3.4h7.4l4.2 4.2v12.8H7.2z" />
          <path className="document-page" d="M6 2.8h7.6L18 7.2v12.6a1.4 1.4 0 0 1-1.4 1.4H6A1.4 1.4 0 0 1 4.6 19.8V4.2A1.4 1.4 0 0 1 6 2.8Z" />
          <path className="document-fold" d="M13.5 3v4.4h4.3" />
          <path className="document-line" d="M7.6 10.4h6.9M7.6 13.4h5.4M7.6 16.4h4.2" />
          <circle className="document-plus-bg" cx="17.2" cy="17.1" r="4" />
          <path className="document-plus" d="M17.2 14.9v4.4M15 17.1h4.4" />
        </svg>
      );
    case "shapes":
      return (
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <rect x="4" y="5" width="7" height="7" rx="1" />
          <circle cx="16.5" cy="8.5" r="3.5" />
          <path d="M5 19h14l-4-6-3 4-2-3Z" />
        </svg>
      );
    case "math":
      return (
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path d="M5 7h14M12 7v10M8 17h8" />
          <path d="M16.5 15.5 19 18m0-2.5L16.5 18" />
        </svg>
      );
    case "properFraction":
      return (
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path d="M8 12h8" />
          <text x="12" y="9" textAnchor="middle" fontSize="6" stroke="none" fill="currentColor">
            1
          </text>
          <text x="12" y="19" textAnchor="middle" fontSize="6" stroke="none" fill="currentColor">
            2
          </text>
        </svg>
      );
    case "mixedFraction":
      return (
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <text x="6" y="16" textAnchor="middle" fontSize="7" stroke="none" fill="currentColor">
            1
          </text>
          <path d="M11 12h8" />
          <text x="15" y="9" textAnchor="middle" fontSize="6" stroke="none" fill="currentColor">
            1
          </text>
          <text x="15" y="19" textAnchor="middle" fontSize="6" stroke="none" fill="currentColor">
            2
          </text>
        </svg>
      );
    case "text":
      return (
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path d="M5 7h12M11 7v10M8 17h6" />
        </svg>
      );
    case "image":
      return (
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <rect x="4" y="5" width="16" height="14" rx="1" />
          <circle cx="9" cy="10" r="1.5" />
          <path d="m5 18 5-5 3 3 2-2 4 4" />
        </svg>
      );
    case "table":
      return (
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <rect x="4" y="5" width="16" height="14" rx="1" />
          <path d="M4 10h16M4 15h16M10 5v14M16 5v14" />
        </svg>
      );
    case "graphPaper":
      return (
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <rect x="4" y="4" width="16" height="16" rx="1" />
          <path d="M8 4v16M12 4v16M16 4v16M4 8h16M4 12h16M4 16h16" />
        </svg>
      );
    case "delete":
      return (
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path d="M5 7h14M10 11v6M14 11v6M8 7l1-3h6l1 3M7 7l1 13h8l1-13" />
        </svg>
      );
    case "refresh":
      return (
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path d="M19 8a7 7 0 0 0-12-2l-2 2" />
          <path d="M5 4v4h4" />
          <path d="M5 16a7 7 0 0 0 12 2l2-2" />
          <path d="M19 20v-4h-4" />
        </svg>
      );
    case "save":
      return (
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path d="M5 4h12l2 2v14H5V4Z" />
          <path d="M8 4v6h8V4M8 20v-6h8v6" />
        </svg>
      );
    case "build":
      return (
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path d="M8 5v14l11-7Z" />
          <path d="M4 5h2M4 12h2M4 19h2" />
        </svg>
      );
  }
}

export function KonvaToolbar(props: KonvaToolbarProps) {
  const [isShapeMenuOpen, setShapeMenuOpen] = useState(false);
  const shapeMenuRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!isShapeMenuOpen) return;
    const onPointerDown = (event: PointerEvent) => {
      if (shapeMenuRef.current?.contains(event.target as Node)) return;
      setShapeMenuOpen(false);
    };
    window.addEventListener("pointerdown", onPointerDown);
    return () => window.removeEventListener("pointerdown", onPointerDown);
  }, [isShapeMenuOpen]);

  return (
    <div className="mvp-toolbar">
      <button type="button" className="new-file-button" title="새파일" aria-label="새파일" onClick={props.onNewFile}>
        <ToolbarIcon name="newFile" />
        <span>새파일</span>
      </button>
      <div className="shape-menu-wrap" ref={shapeMenuRef}>
        <button
          type="button"
          className={isShapeMenuOpen ? "icon-button shape-menu-trigger active" : "icon-button shape-menu-trigger"}
          title="Insert shape"
          aria-label="Insert shape"
          aria-expanded={isShapeMenuOpen}
          onClick={() => setShapeMenuOpen((open) => !open)}
        >
          <ToolbarIcon name="shapes" />
        </button>
        {isShapeMenuOpen ? (
          <div className="shape-palette" role="menu" aria-label="Insert shape">
            {SHAPE_SECTIONS.filter((_, index) => index !== 1).map((section) => (
              <div className="shape-palette-section" key={section.title}>
                <div className="shape-palette-title">{section.title}</div>
                <div className="shape-palette-grid">
                  {section.items.map((item) => (
                    <button
                      type="button"
                      className="shape-palette-item"
                      key={item.preset}
                      title={item.label}
                      aria-label={item.label}
                      onClick={() => {
                        props.onInsertShape(item.preset);
                        setShapeMenuOpen(false);
                      }}
                    >
                      <ShapePresetIcon preset={item.preset} />
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>
        ) : null}
      </div>
      <IconButton label="Math expression" icon="math" onClick={props.onAddMath} />
      <IconButton label="Proper fraction" icon="properFraction" onClick={props.onAddProperFraction} />
      <IconButton label="Mixed fraction" icon="mixedFraction" onClick={props.onAddMixedFraction} />
      <IconButton label="Text" icon="text" onClick={props.onAddText} />
      <IconButton label="Image" icon="image" onClick={props.onAddImage} />
      <IconButton label="Table" icon="table" onClick={props.onAddTable} />
      <IconButton label="Graph Paper" icon="graphPaper" onClick={props.onAddGraphPaper} />
      <IconButton label="Delete selected" icon="delete" onClick={props.onDeleteSelected} disabled={!props.hasSelection} />
      <span className="toolbar-spacer" />
      <IconButton label="Refresh JSON" icon="refresh" onClick={props.onRefreshJson} />
      <IconButton label="Save DSL" icon="save" onClick={props.onSave} primary />
      <IconButton label="Build" icon="build" onClick={props.onBuild} />
    </div>
  );
}

function ShapePresetIcon({ preset }: { preset: ShapePreset }) {
  const d = shapePreviewPath(preset);
  if (preset === "line") {
    return (
      <svg viewBox="0 0 32 24" aria-hidden="true">
        <path d="M4 18 28 6" />
      </svg>
    );
  }
  if (preset === "arrow") {
    return (
      <svg viewBox="0 0 32 24" aria-hidden="true">
        <path d="M4 18 24 6M24 6h-7M24 6l-2 7" />
      </svg>
    );
  }
  if (preset === "doubleArrow") {
    return (
      <svg viewBox="0 0 32 24" aria-hidden="true">
        <path d="M6 18 26 6M6 18h7M6 18l2-7M26 6h-7M26 6l-2 7" />
      </svg>
    );
  }
  if (preset === "elbow") {
    return (
      <svg viewBox="0 0 32 24" aria-hidden="true">
        <path d="M6 6v10h20" />
      </svg>
    );
  }
  if (preset === "elbowArrow" || preset === "elbowDoubleArrow") {
    return (
      <svg viewBox="0 0 32 24" aria-hidden="true">
        <path d={preset === "elbowArrow" ? "M6 6v10h20M26 16l-6-4M26 16l-6 4" : "M6 6v10h20M6 6l4 6M6 6l-4 6M26 16l-6-4M26 16l-6 4"} />
      </svg>
    );
  }
  if (preset === "curvedConnector" || preset === "curvedArrow" || preset === "curvedDoubleArrow" || preset === "curve") {
    return (
      <svg viewBox="0 0 32 24" aria-hidden="true">
        <path d="M5 18 C10 4, 22 4, 27 18" />
        {preset === "curvedArrow" || preset === "curvedDoubleArrow" ? <path d="M27 18l-7-1M27 18l-3-6" /> : null}
        {preset === "curvedDoubleArrow" ? <path d="M5 18l7 1M5 18l3-6" /> : null}
      </svg>
    );
  }
  if (preset === "freeformShape" || preset === "freeformScribble") {
    return (
      <svg viewBox="0 0 32 24" aria-hidden="true">
        <path d={preset === "freeformShape" ? "M6 18 L12 7 L20 9 L26 18 Z" : "M5 16 C9 5, 13 20, 18 9 S25 13, 27 7"} />
      </svg>
    );
  }
  if (preset === "arc" || preset === "semicircle" || preset === "quarterArc") {
    return (
      <svg viewBox="0 0 32 24" aria-hidden="true">
        <path d={preset === "quarterArc" ? "M9 18 A10 10 0 0 1 21 6" : "M5 17 A12 10 0 0 1 27 17"} />
      </svg>
    );
  }
  if (preset === "rect") {
    return (
      <svg viewBox="0 0 32 24" aria-hidden="true">
        <rect x="5" y="6" width="22" height="12" />
      </svg>
    );
  }
  if (preset === "roundRect") {
    return (
      <svg viewBox="0 0 32 24" aria-hidden="true">
        <rect x="5" y="6" width="22" height="12" rx="4" />
      </svg>
    );
  }
  if (preset === "circle" || preset === "calloutOval") {
    return (
      <svg viewBox="0 0 32 24" aria-hidden="true">
        <ellipse cx="16" cy="12" rx="10" ry="7" />
        {preset === "calloutOval" ? <path d="M13 18 9 22l1-6" /> : null}
      </svg>
    );
  }
  return (
    <svg viewBox="0 0 100 80" aria-hidden="true">
      <path d={d} />
    </svg>
  );
}

function shapePreviewPath(preset: ShapePreset): string {
  switch (preset) {
    case "triangle":
      return "M50 12 L88 68 L12 68 Z";
    case "rightTriangle":
      return "M16 14 L84 68 L16 68 Z";
    case "diamond":
    case "flowDecision":
      return "M50 8 L92 40 L50 72 L8 40 Z";
    case "pentagon":
      return "M50 8 L90 34 L74 72 L26 72 L10 34 Z";
    case "hexagon":
      return "M28 10 L72 10 L94 40 L72 70 L28 70 L6 40 Z";
    case "plus":
    case "mathPlus":
      return "M38 10 L62 10 L62 30 L84 30 L84 52 L62 52 L62 72 L38 72 L38 52 L16 52 L16 30 L38 30 Z";
    case "rightArrow":
      return "M8 28 L58 28 L58 12 L92 40 L58 68 L58 52 L8 52 Z";
    case "leftArrow":
      return "M92 28 L42 28 L42 12 L8 40 L42 68 L42 52 L92 52 Z";
    case "upArrow":
      return "M38 72 L38 30 L22 30 L50 8 L78 30 L62 30 L62 72 Z";
    case "downArrow":
      return "M38 8 L62 8 L62 50 L78 50 L50 72 L22 50 L38 50 Z";
    case "leftRightArrow":
      return "M8 40 L28 18 L28 30 L72 30 L72 18 L92 40 L72 62 L72 50 L28 50 L28 62 Z";
    case "mathMinus":
      return "M18 34 L82 34 L82 50 L18 50 Z";
    case "mathMultiply":
      return "M30 14 L50 34 L70 14 L86 30 L66 50 L86 70 L70 76 L50 56 L30 76 L14 60 L34 40 L14 30 Z";
    case "mathDivide":
      return "M18 34 L82 34 L82 48 L18 48 Z M44 12 A6 6 0 1 0 56 12 A6 6 0 1 0 44 12 M44 68 A6 6 0 1 0 56 68 A6 6 0 1 0 44 68";
    case "flowProcess":
      return "M10 16 L90 16 L90 64 L10 64 Z";
    case "flowDocument":
      return "M10 12 L90 12 L90 58 C70 72 30 48 10 64 Z";
    case "flowDatabase":
      return "M16 22 C16 8 84 8 84 22 L84 58 C84 72 16 72 16 58 Z M16 22 C16 36 84 36 84 22";
    case "star":
      return "M50 8 L60 30 L84 30 L65 46 L72 70 L50 56 L28 70 L35 46 L16 30 L40 30 Z";
    case "burst":
      return "M50 8 L58 26 L76 14 L72 34 L94 36 L76 48 L88 66 L66 62 L58 76 L50 58 L38 76 L34 58 L12 66 L24 48 L6 36 L28 34 L24 14 L42 26 Z";
    case "ribbon":
      return "M12 18 L88 18 L78 40 L88 62 L12 62 L22 40 Z";
    case "calloutRect":
      return "M8 12 L92 12 L92 56 L62 56 L48 72 L52 56 L8 56 Z";
    case "calloutRound":
      return "M18 12 L82 12 Q92 12 92 22 L92 50 Q92 60 82 60 L62 60 L48 72 L52 60 L18 60 Q8 60 8 50 L8 22 Q8 12 18 12 Z";
    case "calloutCloud":
      return "M28 58 C10 58 8 42 22 36 C18 20 40 14 50 26 C62 12 84 20 80 38 C94 42 88 60 70 58 L54 58 L42 72 L44 58 Z";
    default:
      return "M10 16 L90 16 L90 64 L10 64 Z";
  }
}
