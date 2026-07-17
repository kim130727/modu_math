from __future__ import annotations

from typing import Any


class TutorRendererFlowError(ValueError):
    pass


def normalize_tutor_renderer_flow(flow: Any) -> list[dict[str, Any]]:
    if flow is None:
        return []
    if isinstance(flow, dict):
        items = []
        for step_id, value in flow.items():
            if not isinstance(value, dict):
                raise TutorRendererFlowError("TUTOR_RENDERER_FLOW step entries must be objects")
            item = dict(value)
            item.setdefault("step_id", str(step_id))
            items.append(item)
        flow = items
    if not isinstance(flow, list):
        raise TutorRendererFlowError("TUTOR_RENDERER_FLOW must be a list or dict")

    normalized: list[dict[str, Any]] = []
    for index, item in enumerate(flow):
        if not isinstance(item, dict):
            raise TutorRendererFlowError(f"TUTOR_RENDERER_FLOW[{index}] must be an object")
        phase = item.get("phase")
        if phase is not None and (not isinstance(phase, str) or not phase.strip()):
            raise TutorRendererFlowError(f"TUTOR_RENDERER_FLOW[{index}].phase must be a non-empty string")
        step_id = item.get("step_id")
        if step_id is None and isinstance(phase, str) and phase.strip() and phase != "execute":
            step_id = phase
        if not isinstance(step_id, str) or not step_id.strip():
            raise TutorRendererFlowError(f"TUTOR_RENDERER_FLOW[{index}].step_id must be a non-empty string")
        frames = item.get("frames")
        if frames is None:
            overlays = item.get("overlays", [])
            if not isinstance(overlays, list):
                raise TutorRendererFlowError(f"TUTOR_RENDERER_FLOW[{index}].overlays must be an array")
            frames = [{"id": f"{step_id}.frame.1", "overlays": overlays}]
        if not isinstance(frames, list):
            raise TutorRendererFlowError(f"TUTOR_RENDERER_FLOW[{index}].frames must be an array")
        normalized_frames = [_normalize_frame(frame, index, frame_index, step_id) for frame_index, frame in enumerate(frames)]
        normalized_item = dict(item)
        normalized_item["step_id"] = step_id
        normalized_item["frames"] = normalized_frames
        normalized_item.pop("overlays", None)
        normalized.append(normalized_item)
    return normalized


def attach_tutor_renderer_flow(renderer: dict[str, Any], flow: Any) -> dict[str, Any]:
    normalized = normalize_tutor_renderer_flow(flow)
    if not normalized:
        return renderer
    out = dict(renderer)
    contract_version = out.pop("contract_version", None)
    out["tutor_flow"] = normalized
    if contract_version is not None:
        out["contract_version"] = contract_version
    return out


def validate_tutor_renderer_flow(renderer: dict[str, Any], solvable: dict[str, Any] | None = None) -> None:
    flow = renderer.get("tutor_flow")
    if flow is None:
        return
    normalized = normalize_tutor_renderer_flow(flow)

    known_step_ids: set[str] = set()
    if isinstance(solvable, dict):
        steps = solvable.get("steps")
        if isinstance(steps, list):
            for step in steps:
                if isinstance(step, dict) and isinstance(step.get("id"), str):
                    known_step_ids.add(step["id"])

    known_refs = _collect_renderer_refs(renderer)
    for index, item in enumerate(normalized):
        step_id = item["step_id"]
        phase = item.get("phase")
        is_solving_step = phase in (None, "execute")
        if known_step_ids and is_solving_step and step_id not in known_step_ids:
            raise TutorRendererFlowError(f"renderer.tutor_flow[{index}].step_id '{step_id}' does not match solvable.steps")
        for frame_index, frame in enumerate(item["frames"]):
            for overlay_index, overlay in enumerate(frame["overlays"]):
                target_ref = overlay.get("target_ref")
                if isinstance(target_ref, str) and target_ref and target_ref not in known_refs:
                    raise TutorRendererFlowError(
                        f"renderer.tutor_flow[{index}].frames[{frame_index}].overlays[{overlay_index}].target_ref "
                        f"'{target_ref}' does not match renderer source_ref/element id/layout ref"
                    )


def _normalize_frame(frame: Any, flow_index: int, frame_index: int, step_id: str) -> dict[str, Any]:
    if not isinstance(frame, dict):
        raise TutorRendererFlowError(f"TUTOR_RENDERER_FLOW[{flow_index}].frames[{frame_index}] must be an object")
    frame_id = frame.get("id", f"{step_id}.frame.{frame_index + 1}")
    if not isinstance(frame_id, str) or not frame_id.strip():
        raise TutorRendererFlowError(f"TUTOR_RENDERER_FLOW[{flow_index}].frames[{frame_index}].id must be a non-empty string")
    overlays = frame.get("overlays", [])
    if not isinstance(overlays, list):
        raise TutorRendererFlowError(f"TUTOR_RENDERER_FLOW[{flow_index}].frames[{frame_index}].overlays must be an array")
    return {
        "id": frame_id,
        "overlays": [_normalize_overlay(overlay, flow_index, overlay_index) for overlay_index, overlay in enumerate(overlays)],
    }


def _normalize_overlay(overlay: Any, flow_index: int, overlay_index: int) -> dict[str, Any]:
    if not isinstance(overlay, dict):
        raise TutorRendererFlowError(f"TUTOR_RENDERER_FLOW[{flow_index}].overlays[{overlay_index}] must be an object")
    overlay_type = overlay.get("type")
    if not isinstance(overlay_type, str) or not overlay_type.strip():
        raise TutorRendererFlowError(
            f"TUTOR_RENDERER_FLOW[{flow_index}].overlays[{overlay_index}].type must be a non-empty string"
        )

    out = dict(overlay)
    target_ref = out.get("target_ref")
    if target_ref is not None and (not isinstance(target_ref, str) or not target_ref.strip()):
        raise TutorRendererFlowError(
            f"TUTOR_RENDERER_FLOW[{flow_index}].overlays[{overlay_index}].target_ref must be a non-empty string"
        )
    text = out.get("text")
    if text is not None and not isinstance(text, str):
        raise TutorRendererFlowError(
            f"TUTOR_RENDERER_FLOW[{flow_index}].overlays[{overlay_index}].text must be a string"
        )
    return out


def _collect_renderer_refs(renderer: dict[str, Any]) -> set[str]:
    refs: set[str] = set()

    def walk(elements: Any) -> None:
        if not isinstance(elements, list):
            return
        for element in elements:
            if not isinstance(element, dict):
                continue
            element_id = element.get("id")
            if isinstance(element_id, str) and element_id:
                refs.add(element_id)
            source_ref = element.get("source_ref")
            if isinstance(source_ref, str) and source_ref:
                refs.add(source_ref)
            element_refs = element.get("refs")
            if isinstance(element_refs, dict):
                for value in element_refs.values():
                    if isinstance(value, str) and value:
                        refs.add(value)
            walk(element.get("elements"))

    walk(renderer.get("elements"))
    return refs
