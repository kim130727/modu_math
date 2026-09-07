import type { EditorShape, InputInteraction } from "../types/editorShape";

export interface AnswerBindingOption {
  index: number;
  label: string;
  value: string;
  unit?: string;
  ref?: string;
}

export type AnswerBindingStatus = "connected" | "inferred" | "unlinked" | "duplicate";
export type AnswerPresentationMode = "canvas_slots" | "panel_input" | "choice";

export interface AnswerSlotReview {
  shapeId: string;
  displayOrder: number;
  option: AnswerBindingOption | null;
  status: AnswerBindingStatus;
}

export interface AnswerChoiceReview {
  id: string;
  label: string;
  text: string;
  correct: boolean;
  sourceRefs?: string[];
}

export function answerChoicesFromArtifacts(
  semantic: Record<string, unknown> | null,
  solvable: Record<string, unknown> | null,
  answerOptions: AnswerBindingOption[],
): AnswerChoiceReview[] {
  const raw = answerChoices(semantic) ?? answerChoices(solvable) ?? [];
  const choices = raw.filter((item) => {
    const entry = recordValue(item);
    const id = stringValue(entry?.slot_id) || stringValue(entry?.id);
    return !(id.endsWith(".marker") && raw.some((other) => {
      const candidate = recordValue(other);
      return (candidate?.slot_id ?? candidate?.id) === id.replace(/\.marker$/, ".value");
    }));
  });
  return choices.map((item, index) => {
    const record = recordValue(item);
    const id = stringValue(record?.id) || `choice.${index + 1}`;
    const label = stringValue(record?.label) || `${index + 1}`;
    const text = scalarText(record?.text ?? record?.value ?? item);
    const correct = answerOptions.some((option) => option.ref === id || (!choices.some((candidate) => recordValue(candidate)?.id === option.ref) && normalizedAnswer(option.value) === normalizedAnswer(text)));
    const sourceRefs = Array.isArray(record?.source_refs) ? record.source_refs.filter((ref): ref is string => typeof ref === "string") : typeof record?.slot_id === "string" ? [record.slot_id] : [];
    return { id, label, text, correct, sourceRefs };
  });
}

export function answerSlotReviews(shapes: EditorShape[], answerOptions: AnswerBindingOption[]): Map<string, AnswerSlotReview> {
  const reviews = new Map<string, AnswerSlotReview>();
  const optionUseCount = new Map<number, number>();

  for (const shape of shapes) {
    const interaction = shape.interaction;
    if (!interaction || !isSubmittedAnswer(interaction)) continue;
    const binding = resolveAnswerBinding(interaction, answerOptions);
    if (binding.option) optionUseCount.set(binding.option.index, (optionUseCount.get(binding.option.index) ?? 0) + 1);
    reviews.set(shape.id, {
      shapeId: shape.id,
      displayOrder: Math.max(0, interaction.order ?? binding.option?.index ?? reviews.size) + 1,
      option: binding.option,
      status: binding.status,
    });
  }

  for (const [shapeId, review] of reviews) {
    if (review.option && (optionUseCount.get(review.option.index) ?? 0) > 1) {
      reviews.set(shapeId, { ...review, status: "duplicate" });
    }
  }
  return reviews;
}

export function resolveAnswerBinding(
  interaction: InputInteraction,
  answerOptions: AnswerBindingOption[],
): { option: AnswerBindingOption | null; status: Exclude<AnswerBindingStatus, "duplicate"> } {
  if (typeof interaction.answer_key_index === "number") {
    const option = answerOptions.find((candidate) => candidate.index === interaction.answer_key_index);
    if (option) return { option, status: "connected" };
  }
  if (interaction.answer_ref) {
    const option = answerOptions.find((candidate) => candidate.ref === interaction.answer_ref);
    if (option) return { option, status: "connected" };
  }
  if (typeof interaction.answer_key_index === "number" || interaction.answer_ref) {
    return { option: null, status: "unlinked" };
  }
  if (answerOptions.length === 1) {
    return { option: answerOptions[0], status: "inferred" };
  }
  if (typeof interaction.order === "number") {
    const option = answerOptions.find((candidate) => candidate.index === interaction.order);
    if (option) return { option, status: "inferred" };
  }
  return { option: null, status: "unlinked" };
}

export function inferAnswerPresentationMode(
  shapes: EditorShape[],
  semantic: Record<string, unknown> | null,
  solvable: Record<string, unknown> | null,
): AnswerPresentationMode {
  const explicit = explicitPresentationMode(semantic) ?? explicitPresentationMode(solvable);
  if (explicit) return explicit;
  if (shapes.some((shape) => shape.interaction && isCanvasAnswer(shape.interaction))) return "canvas_slots";
  if (shapes.some((shape) => shape.interaction?.role === "choice") || hasChoices(semantic) || hasChoices(solvable)) return "choice";
  return "panel_input";
}

function isSubmittedAnswer(interaction: InputInteraction): boolean {
  return interaction.include_in_submission !== false && (interaction.role === "answer" || interaction.role === "choice");
}

function isCanvasAnswer(interaction: InputInteraction): boolean {
  return interaction.include_in_submission !== false && interaction.role === "answer";
}

function explicitPresentationMode(artifact: Record<string, unknown> | null): AnswerPresentationMode | null {
  const answer = recordValue(artifact?.answer);
  const presentation = recordValue(answer?.presentation);
  const mode = presentation?.mode;
  return mode === "canvas_slots" || mode === "panel_input" || mode === "choice" ? mode : null;
}

function hasChoices(artifact: Record<string, unknown> | null): boolean {
  const answer = recordValue(artifact?.answer);
  return Boolean(answerChoices(artifact)?.length || (Array.isArray(answer?.choice_groups) && answer.choice_groups.length));
}

function answerChoices(artifact: Record<string, unknown> | null): unknown[] | null {
  const answer = recordValue(artifact?.answer);
  if (Array.isArray(answer?.choices)) return answer.choices;
  if (Array.isArray(artifact?.choices)) return artifact.choices;
  return null;
}

function scalarText(value: unknown): string {
  return value === null || value === undefined ? "" : String(value);
}

function stringValue(value: unknown): string {
  return typeof value === "string" && value.trim() ? value.trim() : "";
}

export function normalizedAnswer(value: string): string {
  const normalized = value.normalize("NFKC").trim().replace(/\s+/g, " ").toLowerCase();
  if (/^[o○◯〇]$/.test(normalized)) return "o";
  if (/^[x×✕✖]$/.test(normalized)) return "x";
  return normalized;
}

export interface AnswerReviewSettings {
  mode: AnswerPresentationMode | "ox";
  status: "pending" | "needs_changes" | "verified";
  note: string;
  answers: { value: string; ref?: string }[];
  choices: AnswerChoiceReview[];
}

export function reviewSettings(semantic: Record<string, unknown> | null, options: AnswerBindingOption[], choices: AnswerChoiceReview[], mode: AnswerPresentationMode): AnswerReviewSettings {
  const saved = recordValue(recordValue(recordValue(semantic?.answer)?.presentation)?.review);
  if (saved) return saved as unknown as AnswerReviewSettings;
  const tokens = options.length === 1 ? options[0].value.split(/\s*[,，]\s*/) : options.map((option) => option.value);
  const ox = tokens.length > 0 && tokens.every((token) => /^[ox]$/.test(normalizedAnswer(token)));
  return { mode: ox ? "ox" : mode, status: "pending", note: "",
    answers: ox ? tokens.map((value) => ({ value: normalizedAnswer(value).toUpperCase() })) : options.map(({ value, ref }) => ({ value, ref })), choices };
}

function recordValue(value: unknown): Record<string, unknown> | null {
  return value && typeof value === "object" && !Array.isArray(value) ? (value as Record<string, unknown>) : null;
}
