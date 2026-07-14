import { useEffect, useMemo, useState } from "react";
import type { TutorRendererStep } from "../api/editorApi";

interface TutorFlowPanelProps {
  problemId: string;
  tutorFlow: TutorRendererStep[];
  message: string;
  activeStepId: string | null;
  activeFrameIndex: number;
  activeOverlayIndex: number | null;
  selectedShapeIds: string[];
  onDraftChange: (tutorFlow: TutorRendererStep[]) => void;
  onSelectFrame: (stepId: string, frameIndex: number) => void;
  onSelectOverlay: (overlayIndex: number | null) => void;
  onSave: (tutorFlow: TutorRendererStep[]) => Promise<void>;
}

export function TutorFlowPanel({
  problemId,
  tutorFlow,
  message,
  activeStepId,
  activeFrameIndex,
  activeOverlayIndex,
  selectedShapeIds,
  onDraftChange,
  onSelectFrame,
  onSelectOverlay,
  onSave,
}: TutorFlowPanelProps) {
  const initialDraft = useMemo(() => JSON.stringify(tutorFlow, null, 2), [tutorFlow]);
  const [draft, setDraft] = useState(initialDraft);
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    setDraft(initialDraft);
    setError("");
  }, [initialDraft]);

  useEffect(() => {
    if (activeStepId || !tutorFlow.length) return;
    const firstFrameCount = tutorFlow[0].frames?.length ?? (tutorFlow[0].overlays?.length ? 1 : 0);
    if (firstFrameCount > 0) onSelectFrame(tutorFlow[0].step_id, 0);
  }, [activeStepId, onSelectFrame, tutorFlow]);

  const parsed = useMemo(() => parseTutorFlow(draft), [draft]);
  const activeStepIndex = parsed.ok && activeStepId ? parsed.flow.findIndex((step) => step.step_id === activeStepId) : -1;
  const activeStep = parsed.ok && activeStepIndex >= 0 ? parsed.flow[activeStepIndex] : null;
  const activeFrames = activeStep?.frames?.length
    ? activeStep.frames
    : activeStep
      ? [{ id: `${activeStep.step_id}.frame.1`, overlays: activeStep.overlays ?? [] }]
      : [];
  const selectedFrameIndex = activeFrames.length ? Math.min(activeFrameIndex, activeFrames.length - 1) : 0;
  const activeFrame = activeFrames[selectedFrameIndex] ?? null;
  const activeOverlay =
    activeOverlayIndex !== null && activeFrame?.overlays[activeOverlayIndex] ? activeFrame.overlays[activeOverlayIndex] : null;

  const updateFlow = (updater: (flow: TutorRendererStep[]) => TutorRendererStep[]) => {
    if (!parsed.ok) {
      setError(parsed.error);
      return;
    }
    const nextFlow = updater(parsed.flow);
    setDraft(JSON.stringify(nextFlow, null, 2));
    setError("");
    onDraftChange(nextFlow);
  };

  const addSelectionHighlights = () => {
    if (!activeStep || !activeFrame) {
      setError("Select a tutor frame first.");
      return;
    }
    if (!selectedShapeIds.length) {
      setError("Select one or more canvas shapes first.");
      return;
    }
    updateFlow((flow) =>
      flow.map((step) => {
        if (step.step_id !== activeStep.step_id) return step;
        const frames = normalizedFrames(step).map((frame, index) =>
          index === selectedFrameIndex
            ? {
                ...frame,
                overlays: [
                  ...frame.overlays,
                  ...selectedShapeIds.map((targetRef) => ({ type: "highlight", target_ref: targetRef })),
                ],
              }
            : frame,
        );
        return { step_id: step.step_id, frames };
      }),
    );
  };

  const addLabel = () => {
    if (!activeStep || !activeFrame) {
      setError("Select a tutor frame first.");
      return;
    }
    const nextOverlayIndex = activeFrame.overlays.length;
    updateFlow((flow) =>
      flow.map((step) => {
        if (step.step_id !== activeStep.step_id) return step;
        const frames = normalizedFrames(step).map((frame, index) =>
          index === selectedFrameIndex
            ? {
                ...frame,
                overlays: [
                  ...frame.overlays,
                  { type: "label", text: "label", x: 40, y: 40, style: { fill: "#0f766e", font_size: 24 } },
                ],
              }
            : frame,
        );
        return { step_id: step.step_id, frames };
      }),
    );
    onSelectOverlay(nextOverlayIndex);
  };

  const removeLastOverlay = () => {
    if (!activeStep || !activeFrame) {
      setError("Select a tutor frame first.");
      return;
    }
    updateFlow((flow) =>
      flow.map((step) => {
        if (step.step_id !== activeStep.step_id) return step;
        const frames = normalizedFrames(step).map((frame, index) =>
          index === selectedFrameIndex ? { ...frame, overlays: frame.overlays.slice(0, -1) } : frame,
        );
        return { step_id: step.step_id, frames };
      }),
    );
  };

  const selectOverlayValue = activeOverlayIndex === null ? "" : String(activeOverlayIndex);

  const updateActiveOverlay = (patch: Record<string, unknown>) => {
    if (!activeStep || !activeFrame || activeOverlayIndex === null) {
      setError("Select an overlay first.");
      return;
    }
    updateFlow((flow) =>
      flow.map((step) => {
        if (step.step_id !== activeStep.step_id) return step;
        const frames = normalizedFrames(step).map((frame, frameIndex) => {
          if (frameIndex !== selectedFrameIndex) return frame;
          return {
            ...frame,
            overlays: frame.overlays.map((overlay, overlayIndex) =>
              overlayIndex === activeOverlayIndex ? { ...overlay, ...patch } : overlay,
            ),
          };
        });
        return { step_id: step.step_id, frames };
      }),
    );
  };

  const updateActiveOverlayStyle = (patch: Record<string, unknown>) => {
    if (!activeOverlay || activeOverlayIndex === null) {
      setError("Select an overlay first.");
      return;
    }
    const style = isRecord(activeOverlay.style) ? activeOverlay.style : {};
    updateActiveOverlay({ style: { ...style, ...patch } });
  };

  const save = async () => {
    let parsedDraft: unknown;
    try {
      parsedDraft = JSON.parse(draft);
    } catch (parseError) {
      setError(`Invalid JSON: ${String(parseError)}`);
      return;
    }
    if (!Array.isArray(parsedDraft)) {
      setError("Tutor flow must be a JSON array.");
      return;
    }
    setSaving(true);
    setError("");
    try {
      await onSave(parsedDraft as TutorRendererStep[]);
    } catch (saveError) {
      setError(`Could not save tutor flow: ${String(saveError)}`);
    } finally {
      setSaving(false);
    }
  };

  return (
    <section className="konva-json-panel konva-tutor-flow-panel">
      <div className="panel-title">Tutor Flow</div>
      <div className={error ? "problem-list-error" : "panel-message"}>
        {error || (problemId ? message : "Open a problem to edit tutor flow.")}
      </div>
      <div className="konva-flow-picker">
        <label>
          Step
          <select
            value={activeStep?.step_id ?? ""}
            onChange={(event) => {
              if (event.target.value) onSelectFrame(event.target.value, 0);
            }}
          >
            <option value="">Select</option>
            {parsed.ok
              ? parsed.flow.map((step) => (
                  <option key={step.step_id} value={step.step_id}>
                    {step.step_id}
                  </option>
                ))
              : null}
          </select>
        </label>
        <label>
          Frame
          <select
            value={String(selectedFrameIndex)}
            disabled={!activeFrames.length || !activeStep}
            onChange={(event) => {
              if (activeStep) onSelectFrame(activeStep.step_id, Number(event.target.value));
            }}
          >
            {activeFrames.map((frame, index) => (
              <option key={frame.id} value={String(index)}>
                {frame.id}
              </option>
            ))}
          </select>
        </label>
        <label>
          Overlay
          <select
            value={selectOverlayValue}
            disabled={!activeFrame?.overlays.length}
            onChange={(event) => {
              onSelectOverlay(event.target.value === "" ? null : Number(event.target.value));
            }}
          >
            <option value="">None</option>
            {activeFrame?.overlays.map((overlay, index) => (
              <option key={`${overlay.type}-${index}`} value={String(index)}>
                {index + 1}. {overlay.type}
                {overlay.type === "label" && overlay.text ? `: ${overlay.text}` : ""}
              </option>
            ))}
          </select>
        </label>
      </div>
      <div className="konva-json-actions">
        <button type="button" onClick={addSelectionHighlights} disabled={!problemId || !activeFrame}>
          Add Highlight
        </button>
        <button type="button" onClick={addLabel} disabled={!problemId || !activeFrame}>
          Add Label
        </button>
        <button type="button" onClick={removeLastOverlay} disabled={!problemId || !activeFrame}>
          Remove Last
        </button>
        <button type="button" onClick={save} disabled={saving || !problemId}>
          {saving ? "Saving..." : "Save Flow"}
        </button>
      </div>
      {activeOverlay?.type === "label" ? (
        <div className="konva-flow-editor">
          <label className="konva-flow-editor-text">
            Text
            <textarea
              value={typeof activeOverlay.text === "string" ? activeOverlay.text : ""}
              onChange={(event) => updateActiveOverlay({ text: event.target.value })}
              rows={2}
            />
          </label>
          <label>
            X
            <input
              type="number"
              value={typeof activeOverlay.x === "number" ? activeOverlay.x : 0}
              onChange={(event) => updateActiveOverlay({ x: numberInput(event.target.value, 0) })}
            />
          </label>
          <label>
            Y
            <input
              type="number"
              value={typeof activeOverlay.y === "number" ? activeOverlay.y : 0}
              onChange={(event) => updateActiveOverlay({ y: numberInput(event.target.value, 0) })}
            />
          </label>
          <label>
            Size
            <input
              type="number"
              value={numberStyle(activeOverlay.style, "font_size", 24)}
              onChange={(event) => updateActiveOverlayStyle({ font_size: numberInput(event.target.value, 24) })}
            />
          </label>
        </div>
      ) : null}
      <textarea value={draft} onChange={(event) => setDraft(event.target.value)} spellCheck={false} />
    </section>
  );
}

function normalizedFrames(step: TutorRendererStep) {
  return step.frames?.length ? step.frames : [{ id: `${step.step_id}.frame.1`, overlays: step.overlays ?? [] }];
}

function parseTutorFlow(value: string): { ok: true; flow: TutorRendererStep[] } | { ok: false; error: string } {
  try {
    const parsed = JSON.parse(value);
    if (!Array.isArray(parsed)) return { ok: false, error: "Tutor flow must be a JSON array." };
    return { ok: true, flow: parsed as TutorRendererStep[] };
  } catch (error) {
    return { ok: false, error: `Invalid JSON: ${String(error)}` };
  }
}

function numberInput(value: string, fallback: number): number {
  const numberValue = Number(value);
  return Number.isFinite(numberValue) ? numberValue : fallback;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function numberStyle(style: unknown, key: string, fallback: number): number {
  if (!isRecord(style)) return fallback;
  const value = style[key];
  return typeof value === "number" && Number.isFinite(value) ? value : fallback;
}
