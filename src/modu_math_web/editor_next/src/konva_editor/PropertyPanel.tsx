import type { EditorShape } from "../types/editorShape";

interface PropertyPanelProps {
  shape: EditorShape | null;
  onChange: (patch: Partial<EditorShape>) => void;
}

export function PropertyPanel({ shape, onChange }: PropertyPanelProps) {
  if (!shape) {
    return (
      <section className="konva-property-panel">
        <div className="panel-title">Properties</div>
        <div className="konva-empty-state">Select a shape.</div>
      </section>
    );
  }

  return (
    <section className="konva-property-panel">
      <div className="panel-title">Properties</div>
      <div className="konva-field-grid">
        <ReadOnlyField label="id" value={shape.id} />
        <ReadOnlyField label="type" value={shape.type} />
        <NumberField label="x" value={shape.x} onChange={(x) => onChange({ x } as Partial<EditorShape>)} />
        <NumberField label="y" value={shape.y} onChange={(y) => onChange({ y } as Partial<EditorShape>)} />
        <NumberField label="rotation" value={shape.rotation ?? 0} onChange={(rotation) => onChange({ rotation } as Partial<EditorShape>)} />
        <NumberField label="offsetX" value={shape.offsetX ?? 0} onChange={(offsetX) => onChange({ offsetX } as Partial<EditorShape>)} />
        <NumberField label="offsetY" value={shape.offsetY ?? 0} onChange={(offsetY) => onChange({ offsetY } as Partial<EditorShape>)} />
        {"fill" in shape ? <TextField label="fill" value={shape.fill ?? ""} onChange={(fill) => onChange({ fill } as Partial<EditorShape>)} /> : null}
        {"stroke" in shape ? (
          <TextField label="stroke" value={shape.stroke ?? ""} onChange={(stroke) => onChange({ stroke } as Partial<EditorShape>)} />
        ) : null}
        {"strokeWidth" in shape ? (
          <NumberField
            label="stroke"
            value={shape.strokeWidth ?? 1}
            onChange={(strokeWidth) => onChange({ strokeWidth } as Partial<EditorShape>)}
          />
        ) : null}
        {shape.type === "rect" || shape.type === "image" || shape.type === "math" ? (
          <>
            <NumberField label="width" value={shape.width} onChange={(width) => onChange({ width } as Partial<EditorShape>)} />
            <NumberField label="height" value={shape.height} onChange={(height) => onChange({ height } as Partial<EditorShape>)} />
          </>
        ) : null}
        {shape.type === "circle" ? (
          <NumberField label="radius" value={shape.radius} onChange={(radius) => onChange({ radius } as Partial<EditorShape>)} />
        ) : null}
        {shape.type === "text" ? (
          <>
            <TextAreaField label="text" value={shape.text} onChange={(text) => onChange({ text } as Partial<EditorShape>)} />
            <NumberField label="font" value={shape.fontSize} onChange={(fontSize) => onChange({ fontSize } as Partial<EditorShape>)} />
            <NumberField label="width" value={shape.width ?? 220} onChange={(width) => onChange({ width } as Partial<EditorShape>)} />
          </>
        ) : null}
        {shape.type === "math" ? (
          <>
            <TextAreaField label="latex" value={shape.latex} onChange={(latex) => onChange({ latex } as Partial<EditorShape>)} />
            <NumberField label="font" value={shape.fontSize ?? 28} onChange={(fontSize) => onChange({ fontSize } as Partial<EditorShape>)} />
          </>
        ) : null}
        {shape.type === "image" ? <TextAreaField label="src" value={shape.src} onChange={(src) => onChange({ src } as Partial<EditorShape>)} /> : null}
      </div>
    </section>
  );
}

function ReadOnlyField({ label, value }: { label: string; value: string }) {
  return (
    <label className="konva-field">
      <span>{label}</span>
      <input value={value} readOnly />
    </label>
  );
}

function NumberField({ label, value, onChange }: { label: string; value: number; onChange: (value: number) => void }) {
  return (
    <label className="konva-field">
      <span>{label}</span>
      <input type="number" value={round(value)} onChange={(event) => onChange(Number(event.target.value))} />
    </label>
  );
}

function TextField({ label, value, onChange }: { label: string; value: string; onChange: (value: string) => void }) {
  return (
    <label className="konva-field">
      <span>{label}</span>
      <input value={value} onChange={(event) => onChange(event.target.value)} />
    </label>
  );
}

function TextAreaField({ label, value, onChange }: { label: string; value: string; onChange: (value: string) => void }) {
  return (
    <label className="konva-field konva-field-wide">
      <span>{label}</span>
      <textarea value={value} onChange={(event) => onChange(event.target.value)} />
    </label>
  );
}

function round(value: number): number {
  return Math.round(value * 100) / 100;
}
