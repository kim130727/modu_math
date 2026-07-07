import type { Editor } from "tldraw";

type IconName =
  | "mathText"
  | "editText"
  | "fontSize"
  | "rect"
  | "circle"
  | "fraction"
  | "numberLine"
  | "groups"
  | "table"
  | "graphPaper"
  | "bubble"
  | "angle"
  | "image"
  | "canvas"
  | "refresh"
  | "save";

interface ToolbarProps {
  editor: Editor | null;
  onAddMathText: () => void;
  onAddRectangle: () => void;
  onAddCircle: () => void;
  onAddFractionBar: () => void;
  onAddNumberLine: () => void;
  onAddGroupObjects: () => void;
  onAddTable: () => void;
  onAddGraphPaper: () => void;
  onAddSpeechBubble: () => void;
  onAddAngleMarker: () => void;
  onEditSelectedMathText: () => void;
  onSetSelectedTextFontSize: () => void;
  onSetCanvasSize: () => void;
  onRefreshJson: () => void;
  onSave: () => void;
}

interface IconButtonProps {
  label: string;
  icon: IconName;
  disabled?: boolean;
  primary?: boolean;
  onClick?: () => void;
}

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

function ToolbarIcon({ name }: { name: IconName }) {
  switch (name) {
    case "mathText":
      return (
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path d="M5 7h14M12 7v10M8 17h8" />
          <path d="M16.5 15.5 19 18m0-2.5L16.5 18" />
        </svg>
      );
    case "editText":
      return (
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path d="M4 7h8M8 7v10M5 17h6" />
          <path d="M14 17.5 18.5 13l2.5 2.5-4.5 4.5H14v-2.5Z" />
        </svg>
      );
    case "fontSize":
      return (
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path d="M4 7h9M8.5 7v10M6 17h5" />
          <path d="M14 17h6M17 8v9M15 8h4" />
        </svg>
      );
    case "rect":
      return (
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <rect x="5" y="6" width="14" height="12" rx="1" />
        </svg>
      );
    case "circle":
      return (
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <circle cx="12" cy="12" r="7" />
        </svg>
      );
    case "fraction":
      return (
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <rect x="4" y="7" width="16" height="10" rx="1" />
          <path d="M8 7v10M12 7v10M16 7v10" />
          <path d="M4 12h16" />
        </svg>
      );
    case "numberLine":
      return (
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path d="M4 14h16" />
          <path d="M6 10v8M10 11v6M14 10v8M18 11v6" />
          <path d="M19 12l2 2-2 2" />
        </svg>
      );
    case "groups":
      return (
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <circle cx="8" cy="8" r="2.5" />
          <circle cx="15" cy="8" r="2.5" />
          <circle cx="8" cy="15" r="2.5" />
          <circle cx="15" cy="15" r="2.5" />
          <path d="M4 4h15v15H4z" />
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
    case "bubble":
      return (
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path d="M5 6h14v9H9l-4 3v-3H5V6Z" />
        </svg>
      );
    case "angle":
      return (
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path d="M5 18 18 6M5 18h14" />
          <path d="M10 18a5 5 0 0 1 1.5-3.5" />
          <text x="13.2" y="17" fontSize="6" stroke="none" fill="currentColor">
            θ
          </text>
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
    case "canvas":
      return (
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <rect x="4" y="5" width="16" height="14" rx="1" />
          <path d="M8 5V3M16 5V3M8 21v-2M16 21v-2M4 9H2M4 15H2M22 9h-2M22 15h-2" />
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
  }
}

export function Toolbar(props: ToolbarProps) {
  const disabled = !props.editor;
  return (
    <div className="mvp-toolbar">
      <IconButton label="Math Text" icon="mathText" onClick={props.onAddMathText} disabled={disabled} />
      <IconButton label="Edit Math Text" icon="editText" onClick={props.onEditSelectedMathText} disabled={disabled} />
      <IconButton label="Font Size" icon="fontSize" onClick={props.onSetSelectedTextFontSize} disabled={disabled} />
      <IconButton label="Rectangle" icon="rect" onClick={props.onAddRectangle} disabled={disabled} />
      <IconButton label="Circle" icon="circle" onClick={props.onAddCircle} disabled={disabled} />
      <IconButton label="Fraction Bar" icon="fraction" onClick={props.onAddFractionBar} disabled={disabled} />
      <IconButton label="Number Line" icon="numberLine" onClick={props.onAddNumberLine} disabled={disabled} />
      <IconButton label="Groups" icon="groups" onClick={props.onAddGroupObjects} disabled={disabled} />
      <IconButton label="Table" icon="table" onClick={props.onAddTable} disabled={disabled} />
      <IconButton label="Graph Paper" icon="graphPaper" onClick={props.onAddGraphPaper} disabled={disabled} />
      <IconButton label="Speech Bubble" icon="bubble" onClick={props.onAddSpeechBubble} disabled={disabled} />
      <IconButton label="Angle Marker" icon="angle" onClick={props.onAddAngleMarker} disabled={disabled} />
      <IconButton label="Image assets TODO" icon="image" disabled />
      <IconButton label="Canvas Size" icon="canvas" onClick={props.onSetCanvasSize} disabled={disabled} />
      <span className="toolbar-spacer" />
      <IconButton label="Refresh JSON" icon="refresh" onClick={props.onRefreshJson} disabled={disabled} />
      <IconButton label="Save DSL" icon="save" onClick={props.onSave} disabled={disabled} primary />
    </div>
  );
}
