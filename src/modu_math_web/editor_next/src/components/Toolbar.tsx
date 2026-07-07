import type { Editor } from "tldraw";

interface ToolbarProps {
  editor: Editor | null;
  onAddMathText: () => void;
  onAddRectangle: () => void;
  onAddCircle: () => void;
  onAddFractionBar: () => void;
  onAddNumberLine: () => void;
  onAddGroupObjects: () => void;
  onEditSelectedMathText: () => void;
  onRefreshJson: () => void;
  onSave: () => void;
}

export function Toolbar(props: ToolbarProps) {
  const disabled = !props.editor;
  return (
    <div className="mvp-toolbar">
      <button type="button" onClick={props.onAddMathText} disabled={disabled}>
        Math Text
      </button>
      <button type="button" onClick={props.onEditSelectedMathText} disabled={disabled}>
        Edit Math Text
      </button>
      <button type="button" onClick={props.onAddRectangle} disabled={disabled}>
        Rect
      </button>
      <button type="button" onClick={props.onAddCircle} disabled={disabled}>
        Circle
      </button>
      <button type="button" onClick={props.onAddFractionBar} disabled={disabled}>
        Fraction Bar
      </button>
      <button type="button" onClick={props.onAddNumberLine} disabled={disabled}>
        Number Line
      </button>
      <button type="button" onClick={props.onAddGroupObjects} disabled={disabled}>
        Groups
      </button>
      <button type="button" disabled title="TODO: connect image assets">
        Image
      </button>
      <span className="toolbar-spacer" />
      <button type="button" onClick={props.onRefreshJson} disabled={disabled}>
        Refresh JSON
      </button>
      <button type="button" className="primary" onClick={props.onSave} disabled={disabled}>
        Save JSON
      </button>
    </div>
  );
}
