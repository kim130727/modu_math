type ToolName =
  | "math"
  | "properFraction"
  | "mixedFraction"
  | "rect"
  | "circle"
  | "line"
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
  onAddMath: () => void;
  onAddProperFraction: () => void;
  onAddMixedFraction: () => void;
  onAddRectangle: () => void;
  onAddCircle: () => void;
  onAddLine: () => void;
  onAddText: () => void;
  onAddImage: () => void;
  onAddTable: () => void;
  onAddGraphPaper: () => void;
  onDeleteSelected: () => void;
  onRefreshJson: () => void;
  onSave: () => void;
  onBuild: () => void;
}

interface IconButtonProps {
  label: string;
  icon: ToolName;
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

function ToolbarIcon({ name }: { name: ToolName }) {
  switch (name) {
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
    case "line":
      return (
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path d="M5 18 19 6" />
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
  return (
    <div className="mvp-toolbar">
      <IconButton label="Math expression" icon="math" onClick={props.onAddMath} />
      <IconButton label="Proper fraction" icon="properFraction" onClick={props.onAddProperFraction} />
      <IconButton label="Mixed fraction" icon="mixedFraction" onClick={props.onAddMixedFraction} />
      <IconButton label="Rectangle" icon="rect" onClick={props.onAddRectangle} />
      <IconButton label="Circle" icon="circle" onClick={props.onAddCircle} />
      <IconButton label="Line" icon="line" onClick={props.onAddLine} />
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
