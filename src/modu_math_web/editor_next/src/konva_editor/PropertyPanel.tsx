import type { AnswerInteractionType, AnswerKeyboard, AnswerRole, AnswerValueType, EditorShape, InputInteraction, InputStyle } from "../types/editorShape";
import { scalePathData } from "../utils/pathData";
import { KONVA_PREVIEW_FONT_FAMILY } from "./fonts";

interface PropertyPanelProps {
  shape: EditorShape | null;
  selectedShapes?: EditorShape[];
  answerOptions?: AnswerBindingOption[];
  saveStatus: "saved" | "saving" | "unsaved" | "building" | "built" | "error";
  onChange: (patch: Partial<EditorShape>) => void;
  onScaleSelection?: (scalePercent: number) => void;
}

export interface AnswerBindingOption {
  index: number;
  label: string;
  value: string;
  unit?: string;
  ref?: string;
}

export function PropertyPanel({ shape, selectedShapes = [], answerOptions = [], saveStatus, onChange, onScaleSelection }: PropertyPanelProps) {
  if (!shape) {
    if (selectedShapes.length > 1) {
      return (
        <section className="konva-property-panel">
          <PropertyPanelTitle saveStatus={saveStatus} />
          <div className="konva-field-grid">
            <ReadOnlyField label="selection" value={`${selectedShapes.length} shapes`} />
            <NumberField label="scale %" value={100} onChange={(scale) => onScaleSelection?.(scale)} />
          </div>
        </section>
      );
    }
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
        {isAnswerSlotShape(shape) ? <AnswerSlotFields shape={shape} answerOptions={answerOptions} onChange={onChange} /> : null}
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
        {scalableShape(shape) && shape.type !== "baseTenBlock" ? (
          <NumberField label="scale %" value={shapeScalePercent(shape)} onChange={(scale) => onChange(shapeScalePatch(shape, scale))} />
        ) : null}
        {shape.type === "rect" || shape.type === "image" || shape.type === "math" || shape.type === "baseTenBlock" ? (
          <>
            <NumberField label="width" value={shape.width} onChange={(width) => onChange({ width } as Partial<EditorShape>)} />
            <NumberField label="height" value={shape.height} onChange={(height) => onChange({ height } as Partial<EditorShape>)} />
          </>
        ) : null}
        {shape.type === "baseTenBlock" ? (
          <>
            <ReadOnlyField label="kind" value={shape.kind} />
            <NumberField label="scale %" value={baseTenScalePercent(shape)} onChange={(scale) => onChange(baseTenScalePatch(shape, scale))} />
            <NumberField label="depth" value={shape.depth} onChange={(depth) => onChange({ depth } as Partial<EditorShape>)} />
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

function AnswerSlotFields({
  shape,
  answerOptions,
  onChange,
}: {
  shape: EditorShape;
  answerOptions: AnswerBindingOption[];
  onChange: (patch: Partial<EditorShape>) => void;
}) {
  const interaction = shape.interaction;
  const inputStyle = shape.input_style;
  const enabled = Boolean(interaction);
  const selectedAnswerOption = interaction ? selectedAnswerBinding(interaction, answerOptions) : null;
  return (
    <>
      <CheckboxField
        label="입력 기능"
        checked={enabled}
        onChange={(checked) =>
          onChange(
            checked
              ? ({
                  interaction: interaction ?? defaultInteractionForShape(shape, answerOptions),
                  input_style: inputStyle ?? defaultInputStyle(),
                } as Partial<EditorShape>)
              : ({ interaction: undefined, input_style: undefined } as Partial<EditorShape>),
          )
        }
      />
      <AnswerBindingFields
        interaction={interaction}
        answerOptions={answerOptions}
        selectedAnswerOption={selectedAnswerOption}
        onChange={onChange}
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

function AnswerBindingFields({
  interaction,
  answerOptions,
  selectedAnswerOption,
  onChange,
}: {
  interaction: InputInteraction | undefined;
  answerOptions: AnswerBindingOption[];
  selectedAnswerOption: AnswerBindingOption | null;
  onChange: (patch: Partial<EditorShape>) => void;
}) {
  if (!interaction) {
    return <ReadOnlyField label="정답 연결" value="입력 기능을 켜면 정답 값을 볼 수 있습니다" />;
  }

  if (interaction.role !== "answer") {
    return <ReadOnlyField label="정답 연결" value="역할을 answer로 바꾸면 정답 값을 볼 수 있습니다" />;
  }

  return (
    <>
      {answerOptions.length ? (
        <SelectField
          label="정답"
          value={selectedAnswerOption ? String(selectedAnswerOption.index) : ""}
          options={["", ...answerOptions.map((option) => String(option.index))]}
          optionLabels={{
            "": "연결 안 함",
            ...Object.fromEntries(answerOptions.map((option) => [String(option.index), option.label])),
          }}
          onChange={(value) => {
            const answer_key_index = value === "" ? undefined : Number(value);
            const option = answerOptions.find((item) => item.index === answer_key_index);
            onChange({
              interaction: {
                ...interaction,
                answer_key_index,
                answer_ref: option?.ref,
                order: answer_key_index ?? interaction.order ?? 0,
                group_id: interaction.group_id || "final_answer",
              },
            } as Partial<EditorShape>);
          }}
        />
      ) : (
        <ReadOnlyField label="정답" value="연결할 answer_key가 없습니다" />
      )}
      <ReadOnlyField label="정답 값" value={answerValueLabel(selectedAnswerOption, interaction)} />
      <ReadOnlyField label="정답 연결 상태" value={answerBindingStatusLabel(selectedAnswerOption, interaction, answerOptions)} />
    </>
  );
}

function selectedAnswerBinding(interaction: InputInteraction, answerOptions: AnswerBindingOption[]): AnswerBindingOption | null {
  if (typeof interaction.answer_key_index === "number") {
    const byIndex = answerOptions.find((option) => option.index === interaction.answer_key_index);
    if (byIndex) return byIndex;
  }
  if (interaction.answer_ref) {
    const byRef = answerOptions.find((option) => option.ref === interaction.answer_ref);
    if (byRef) return byRef;
  }
  if (interaction.role === "answer" && typeof interaction.order === "number") {
    const byOrder = answerOptions.find((option) => option.index === interaction.order);
    if (byOrder) return byOrder;
  }
  return null;
}

function answerValueLabel(option: AnswerBindingOption | null, interaction: InputInteraction): string {
  if (option) return `${option.value}${option.unit ? ` ${option.unit}` : ""}`;
  if (interaction.answer_ref) return `연결 ref: ${interaction.answer_ref}`;
  if (typeof interaction.answer_key_index === "number") return `연결 index: ${interaction.answer_key_index}`;
  if (typeof interaction.order === "number") return `순서 ${interaction.order}에 해당하는 answer_key를 찾지 못했습니다`;
  return "연결 안 함";
}

function answerBindingStatusLabel(
  option: AnswerBindingOption | null,
  interaction: InputInteraction,
  answerOptions: AnswerBindingOption[],
): string {
  if (option) {
    const parts = [`answer_key[${option.index}]`];
    if (option.ref) parts.push(option.ref);
    if (typeof interaction.order === "number") parts.push(`order ${interaction.order}`);
    return parts.join(" · ");
  }
  if (!answerOptions.length) return "현재 문제에서 answer_key를 찾지 못했습니다";
  if (interaction.answer_ref) return `저장된 ref(${interaction.answer_ref})와 일치하는 answer_key가 없습니다`;
  if (typeof interaction.answer_key_index === "number") {
    return `저장된 index(${interaction.answer_key_index})와 일치하는 answer_key가 없습니다`;
  }
  if (typeof interaction.order === "number") return `order ${interaction.order} 기준으로 연결 후보가 없습니다`;
  return "콤보박스에서 연결할 정답을 선택하세요";
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

function defaultInteractionForShape(shape: EditorShape, answerOptions: AnswerBindingOption[] = []): InputInteraction {
  const singleAnswer = answerOptions.length === 1 ? answerOptions[0] : null;
  const firstAnswer = singleAnswer ?? answerOptions[0] ?? null;
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
    value_type: "integer",
    max_length: 3,
    include_in_submission: true,
    order: firstAnswer?.index ?? 0,
    group_id: "final_answer",
    answer_key_index: firstAnswer?.index,
    answer_ref: firstAnswer?.ref,
    auto_advance: false,
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

function SelectField({
  label,
  value,
  options,
  optionLabels = {},
  onChange,
}: {
  label: string;
  value: string;
  options: string[];
  optionLabels?: Record<string, string>;
  onChange: (value: string) => void;
}) {
  return (
    <label className="konva-field">
      <span>{label}</span>
      <select value={value} onChange={(event) => onChange(event.target.value)}>
        {options.map((option) => (
          <option key={option} value={option}>
            {optionLabels[option] ?? option}
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

function scalableShape(shape: EditorShape): shape is Extract<EditorShape, { type: "rect" | "circle" | "path" | "image" | "math" | "baseTenBlock" }> {
  return shape.type === "rect" || shape.type === "circle" || shape.type === "path" || shape.type === "image" || shape.type === "math" || shape.type === "baseTenBlock";
}

function shapeScalePercent(shape: Extract<EditorShape, { type: "rect" | "circle" | "path" | "image" | "math" }>): number {
  const base = shapeBaseSize(shape);
  if (shape.type === "circle") return round((shape.radius / base.radius) * 100);
  return round((shape.width / base.width) * 100);
}

function shapeScalePatch(shape: Extract<EditorShape, { type: "rect" | "circle" | "path" | "image" | "math" }>, scalePercent: number): Partial<EditorShape> {
  const base = shapeBaseSize(shape);
  const scale = Math.max(1, Number.isFinite(scalePercent) ? scalePercent : 100) / 100;
  if (shape.type === "circle") {
    return { radius: round(base.radius * scale) } as Partial<EditorShape>;
  }
  const nextWidth = round(base.width * scale);
  const nextHeight = round(base.height * scale);
  if (shape.type === "path") {
    const scaleX = shape.width ? nextWidth / shape.width : 1;
    const scaleY = shape.height ? nextHeight / shape.height : 1;
    return {
      width: nextWidth,
      height: nextHeight,
      d: scalePathData(shape.d, scaleX, scaleY),
      adjustment: shape.adjustment ? { x: round(shape.adjustment.x * scaleX), y: round(shape.adjustment.y * scaleY) } : undefined,
    } as Partial<EditorShape>;
  }
  return {
    width: nextWidth,
    height: nextHeight,
  } as Partial<EditorShape>;
}

function shapeBaseSize(shape: Extract<EditorShape, { type: "rect" | "circle" | "path" | "image" | "math" }>): { width: number; height: number; radius: number } {
  if (shape.type === "circle") return { width: 140, height: 140, radius: 70 };
  if (shape.type === "math") return { width: 260, height: 72, radius: 0 };
  if (shape.type === "path") return { width: 180, height: 120, radius: 0 };
  if (shape.type === "image") return { width: 180, height: 120, radius: 0 };
  return { width: 180, height: 96, radius: 0 };
}

function baseTenScalePercent(shape: Extract<EditorShape, { type: "baseTenBlock" }>): number {
  const dimensions = baseTenBaseDimensions(shape.kind);
  return round((shape.width / dimensions.width) * 100);
}

function baseTenScalePatch(shape: Extract<EditorShape, { type: "baseTenBlock" }>, scalePercent: number): Partial<EditorShape> {
  const dimensions = baseTenBaseDimensions(shape.kind);
  const scale = Math.max(1, Number.isFinite(scalePercent) ? scalePercent : 100) / 100;
  return {
    width: round(dimensions.width * scale),
    height: round(dimensions.height * scale),
    depth: round(dimensions.depth * scale),
  } as Partial<EditorShape>;
}

function baseTenBaseDimensions(kind: Extract<EditorShape, { type: "baseTenBlock" }>["kind"]): { width: number; height: number; depth: number } {
  switch (kind) {
    case "thousand":
      return { width: 120, height: 120, depth: 42 };
    case "hundred":
      return { width: 96, height: 96, depth: 20 };
    case "ten":
      return { width: 16, height: 112, depth: 7 };
    case "one":
      return { width: 28, height: 28, depth: 10 };
  }
}
