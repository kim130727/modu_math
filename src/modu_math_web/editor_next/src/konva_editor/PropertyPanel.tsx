import type { AnswerInteractionType, AnswerKeyboard, AnswerRole, AnswerValueType, EditorShape, InputInteraction, InputStyle } from "../types/editorShape";
import { KONVA_PREVIEW_FONT_FAMILY } from "./fonts";

interface PropertyPanelProps {
  shape: EditorShape | null;
  saveStatus: "saved" | "saving" | "unsaved" | "building" | "built" | "error";
  onChange: (patch: Partial<EditorShape>) => void;
}

export function PropertyPanel({ shape, saveStatus, onChange }: PropertyPanelProps) {
  if (!shape) {
    return (
      <section className="konva-property-panel">
        <PropertyPanelTitle saveStatus={saveStatus} />
        <div className="konva-empty-state">Select a shape.</div>
      </section>
    );
  }

  return (
    <section className="konva-property-panel">
      <PropertyPanelTitle saveStatus={saveStatus} />
      <div className="konva-field-grid">
        <ReadOnlyField label="id" value={shape.id} />
        <ReadOnlyField label="type" value={shape.type} />
        {isAnswerSlotShape(shape) ? <AnswerSlotFields shape={shape} onChange={onChange} /> : null}
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
        {shape.type === "line" || shape.type === "connector" || shape.type === "path" || shape.type === "rect" || shape.type === "circle" ? (
          <TextField
            label="dash"
            value={shape.strokeDasharray ?? ""}
            onChange={(strokeDasharray) => onChange({ strokeDasharray } as Partial<EditorShape>)}
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
            <TextField
              label="fontFamily"
              value={shape.fontFamily ?? KONVA_PREVIEW_FONT_FAMILY}
              onChange={(fontFamily) => onChange({ fontFamily } as Partial<EditorShape>)}
            />
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

function AnswerSlotFields({ shape, onChange }: { shape: EditorShape; onChange: (patch: Partial<EditorShape>) => void }) {
  const interaction = shape.interaction;
  const inputStyle = shape.input_style;
  const enabled = Boolean(interaction);
  return (
    <>
      <CheckboxField
        label="입력 기능"
        checked={enabled}
        onChange={(checked) =>
          onChange(
            checked
              ? ({
                  interaction: interaction ?? defaultInteractionForShape(shape),
                  input_style: inputStyle ?? defaultInputStyle(),
                } as Partial<EditorShape>)
              : ({ interaction: undefined, input_style: undefined } as Partial<EditorShape>),
          )
        }
      />
      {interaction ? (
        <>
          <SelectField
            label="입력 방식"
            value={interaction.type}
            options={["input", "select"]}
            onChange={(type) => onChange({ interaction: { ...interaction, type: type as AnswerInteractionType } } as Partial<EditorShape>)}
          />
          <SelectField
            label="역할"
            value={interaction.role}
            options={["answer", "result", "intermediate", "carry", "blank", "choice"]}
            onChange={(role) => onChange({ interaction: { ...interaction, role: role as AnswerRole } } as Partial<EditorShape>)}
          />
          <SelectField
            label="값 형식"
            value={interaction.value_type}
            options={["digit", "integer", "decimal", "fraction", "text", "choice", "select"]}
            onChange={(value_type) => onChange({ interaction: { ...interaction, value_type: value_type as AnswerValueType } } as Partial<EditorShape>)}
          />
          <NumberField
            label="최대 길이"
            value={interaction.max_length ?? 1}
            onChange={(max_length) => onChange({ interaction: { ...interaction, max_length: Math.max(1, Math.round(max_length)) } } as Partial<EditorShape>)}
          />
          <NumberField
            label="순서"
            value={interaction.order ?? 0}
            onChange={(order) => onChange({ interaction: { ...interaction, order: Math.max(0, Math.round(order)) } } as Partial<EditorShape>)}
          />
          <TextField
            label="그룹"
            value={interaction.group_id ?? ""}
            onChange={(group_id) => onChange({ interaction: { ...interaction, group_id } } as Partial<EditorShape>)}
          />
          <TextField
            label="선택 값"
            value={interaction.choice_value === undefined ? "" : String(interaction.choice_value)}
            onChange={(choice_value) => onChange({ interaction: { ...interaction, choice_value } } as Partial<EditorShape>)}
          />
          <SelectField
            label="키보드"
            value={interaction.keyboard ?? "number"}
            options={["number", "decimal", "fraction", "text", "none"]}
            onChange={(keyboard) => onChange({ interaction: { ...interaction, keyboard: keyboard as AnswerKeyboard } } as Partial<EditorShape>)}
          />
          <CheckboxField
            label="제출 포함"
            checked={interaction.include_in_submission ?? true}
            onChange={(include_in_submission) => onChange({ interaction: { ...interaction, include_in_submission } } as Partial<EditorShape>)}
          />
          <CheckboxField
            label="자동 이동"
            checked={interaction.auto_advance ?? false}
            onChange={(auto_advance) => onChange({ interaction: { ...interaction, auto_advance } } as Partial<EditorShape>)}
          />
        </>
      ) : null}
      {inputStyle ? (
        <>
          <SelectField
            label="글자 크기"
            value={inputStyle.font_size_mode ?? "auto"}
            options={["auto", "fixed"]}
            onChange={(font_size_mode) => onChange({ input_style: { ...inputStyle, font_size_mode: font_size_mode as InputStyle["font_size_mode"] } } as Partial<EditorShape>)}
          />
          <NumberField
            label="미세 조절"
            value={inputStyle.font_size_adjust ?? 0}
            onChange={(font_size_adjust) => onChange({ input_style: { ...inputStyle, font_size_adjust } } as Partial<EditorShape>)}
          />
          <NumberField
            label="고정 크기"
            value={inputStyle.font_size ?? 32}
            onChange={(font_size) => onChange({ input_style: { ...inputStyle, font_size } } as Partial<EditorShape>)}
          />
          <NumberField
            label="안쪽 여백"
            value={inputStyle.padding ?? 6}
            onChange={(padding) => onChange({ input_style: { ...inputStyle, padding: Math.max(0, padding) } } as Partial<EditorShape>)}
          />
          <TextField
            label="글자색"
            value={inputStyle.text_color ?? "#222222"}
            onChange={(text_color) => onChange({ input_style: { ...inputStyle, text_color } } as Partial<EditorShape>)}
          />
        </>
      ) : null}
    </>
  );
}

function PropertyPanelTitle({ saveStatus }: { saveStatus: PropertyPanelProps["saveStatus"] }) {
  return (
    <div className="panel-title konva-property-title">
      <span>Properties</span>
      <span className={`konva-save-status ${saveStatus}`} aria-live="polite">
        {statusLabel(saveStatus)}
      </span>
    </div>
  );
}

function statusLabel(saveStatus: PropertyPanelProps["saveStatus"]): string {
  if (saveStatus === "saving") return "Saving...";
  if (saveStatus === "unsaved") return "Unsaved";
  if (saveStatus === "building") return "Building...";
  if (saveStatus === "built") return "Build complete";
  if (saveStatus === "error") return "Error";
  return "Saved";
}

function isAnswerSlotShape(shape: EditorShape): boolean {
  return shape.type === "rect" || shape.type === "circle" || shape.type === "path" || shape.type === "text";
}

function defaultInteractionForShape(shape: EditorShape): InputInteraction {
  if (shape.type === "circle" || shape.type === "path") {
    return {
      type: "select",
      role: "choice",
      value_type: "choice",
      choice_value: shape.id,
      include_in_submission: true,
      order: 0,
      group_id: "shape_choice",
      keyboard: "none",
    };
  }
  return {
    type: "input",
    role: "answer",
    value_type: "digit",
    max_length: 1,
    include_in_submission: true,
    order: 0,
    group_id: "final_answer",
    auto_advance: true,
    keyboard: "number",
  };
}

function defaultInputStyle(): InputStyle {
  return {
    font_size_mode: "auto",
    font_size_adjust: 0,
    min_font_size: 14,
    max_font_size: 52,
    font_weight: 700,
    horizontal_align: "center",
    vertical_align: "middle",
    padding: 6,
    text_color: "#222222",
  };
}

function ReadOnlyField({ label, value }: { label: string; value: string }) {
  return (
    <label className="konva-field">
      <span>{label}</span>
      <input value={value} readOnly />
    </label>
  );
}

function CheckboxField({ label, checked, onChange }: { label: string; checked: boolean; onChange: (checked: boolean) => void }) {
  return (
    <label className="konva-field">
      <span>{label}</span>
      <input type="checkbox" checked={checked} onChange={(event) => onChange(event.target.checked)} />
    </label>
  );
}

function SelectField({ label, value, options, onChange }: { label: string; value: string; options: string[]; onChange: (value: string) => void }) {
  return (
    <label className="konva-field">
      <span>{label}</span>
      <select value={value} onChange={(event) => onChange(event.target.value)}>
        {options.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
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
