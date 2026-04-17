import { applySemantic, saveSemantic } from "./api.js?v=20260415a";
import { fillPropertiesForm, applyPropertiesForm } from "./properties.js?v=20260415a";
import { renderCanvas, eventToSvgPoint } from "./svg_canvas.js?v=20260415a";

function byId(id) {
  return document.getElementById(id);
}

function parseJsonScript(id) {
  return JSON.parse(byId(id).textContent);
}

function ensureShape(semantic) {
  semantic.render ??= {};
  semantic.render.canvas ??= { width: 1200, height: 700, background: "#F6F6F6" };
  semantic.render.elements ??= [];
}

function getElements(semantic) {
  ensureShape(semantic);
  return semantic.render.elements;
}

function makeId(prefix, elements) {
  let i = elements.length + 1;
  while (elements.some((el) => el.id === `${prefix}_${i}`)) i += 1;
  return `${prefix}_${i}`;
}

function newElement(type, elements) {
  if (type === "line") {
    return { id: makeId("line", elements), type, x1: 180, y1: 220, x2: 360, y2: 220, stroke: "#222", stroke_width: 2 };
  }
  if (type === "rect") {
    return { id: makeId("rect", elements), type, x: 140, y: 140, width: 220, height: 120, stroke: "#222", stroke_width: 2, fill: "none" };
  }
  if (type === "circle") {
    return { id: makeId("circle", elements), type, x: 240, y: 260, r: 60, stroke: "#222", stroke_width: 2, fill: "none" };
  }
  if (type === "text") {
    return { id: makeId("text", elements), type, x: 120, y: 100, text: "새 텍스트", fill: "#111", font_size: 24 };
  }
  return { id: makeId("formula", elements), type: "formula", x: 120, y: 100, expr: "x + y = 10", fill: "#111", font_size: 24 };
}

function normalizeProblemId(problemId) {
  return String(problemId ?? "").replaceAll("/", "_");
}

function deriveLayoutFromSemantic(problemId, semantic) {
  ensureShape(semantic);
  const render = semantic.render ?? {};
  const canvas = render.canvas ?? {};
  const elements = Array.isArray(render.elements) ? render.elements : [];
  const nodes = [];

  for (const element of elements) {
    if (!element || typeof element !== "object") continue;
    const etype = String(element.type ?? "shape");
    const node = {
      id: String(element.id ?? ""),
      x: element.x ?? element.x1 ?? 0,
      y: element.y ?? element.y1 ?? 0,
    };
    if (element.width !== undefined) node.width = element.width;
    if (element.height !== undefined) node.height = element.height;
    if (element.anchor !== undefined) node.anchor = element.anchor;
    if (element.z_index !== undefined) node.z_order = element.z_index;

    const props = {};
    if (etype === "text" || etype === "formula") {
      node.type = "text";
      props.text = etype === "formula" ? String(element.expr ?? "") : String(element.text ?? "");
      if (etype === "formula") props.is_formula = true;
    } else {
      node.type = "shape";
      props.shape_type = etype;
      if (etype === "line") {
        if (element.x1 !== undefined) props.x1 = element.x1;
        if (element.y1 !== undefined) props.y1 = element.y1;
        if (element.x2 !== undefined) props.x2 = element.x2;
        if (element.y2 !== undefined) props.y2 = element.y2;
      }
      if (etype === "circle" && element.r !== undefined) props.r = element.r;
      if (etype === "polygon" && element.points !== undefined) props.points = element.points;
      if (etype === "rect") {
        if (element.rx !== undefined) props.rx = element.rx;
        if (element.ry !== undefined) props.ry = element.ry;
      }
    }

    for (const key of ["fill", "stroke", "stroke_width", "font_family", "font_size", "font_weight", "font_style", "opacity", "transform"]) {
      if (element[key] !== undefined) props[key] = element[key];
    }
    node.properties = props;
    nodes.push(node);
  }

  return {
    problem_id: semantic.problem_id ?? normalizeProblemId(problemId),
    canvas: {
      width: canvas.width ?? 1200,
      height: canvas.height ?? 700,
      background: canvas.background ?? "#F6F6F6",
    },
    nodes,
  };
}

function deriveRendererFromLayout(layout) {
  const canvas = layout?.canvas ?? {};
  const rawNodes = Array.isArray(layout?.nodes) ? layout.nodes : [];
  const orderedNodes = [...rawNodes].sort((a, b) => Number(a?.z_order ?? 0) - Number(b?.z_order ?? 0));
  const elements = [];

  for (const node of orderedNodes) {
    if (!node || typeof node !== "object") continue;
    const props = node.properties && typeof node.properties === "object" ? node.properties : {};
    const nodeType = String(node.type ?? "");
    const nodeId = String(node.id ?? "");

    if (nodeType === "text") {
      const attrs = { x: node.x ?? 0, y: node.y ?? 0 };
      if (node.anchor !== undefined) attrs["text-anchor"] = node.anchor;
      for (const key of ["fill", "stroke", "stroke_width", "font_family", "font_size", "font_weight", "font_style", "opacity", "transform"]) {
        if (props[key] !== undefined) attrs[key.replaceAll("_", "-")] = props[key];
      }
      if (props.is_formula) {
        attrs["data-formula"] = props.text ?? "";
        attrs.class = "formula-placeholder";
      }
      elements.push({
        id: nodeId,
        type: "text",
        attributes: attrs,
        text: String(props.text ?? ""),
      });
      continue;
    }

    const shapeType = String(props.shape_type ?? "shape");
    const attrs = {};
    for (const key of ["fill", "stroke", "stroke_width", "opacity", "transform"]) {
      if (props[key] !== undefined) attrs[key.replaceAll("_", "-")] = props[key];
    }
    if (shapeType === "rect") {
      attrs.x = node.x ?? 0;
      attrs.y = node.y ?? 0;
      if (node.width !== undefined) attrs.width = node.width;
      if (node.height !== undefined) attrs.height = node.height;
      if (props.rx !== undefined) attrs.rx = props.rx;
      if (props.ry !== undefined) attrs.ry = props.ry;
    } else if (shapeType === "circle") {
      attrs.cx = node.x ?? 0;
      attrs.cy = node.y ?? 0;
      if (props.r !== undefined) attrs.r = props.r;
    } else if (shapeType === "line") {
      attrs.x1 = props.x1 ?? node.x ?? 0;
      attrs.y1 = props.y1 ?? node.y ?? 0;
      if (props.x2 !== undefined) attrs.x2 = props.x2;
      if (props.y2 !== undefined) attrs.y2 = props.y2;
    } else if (shapeType === "polygon") {
      if (props.points !== undefined) attrs.points = props.points;
    } else {
      attrs.x = node.x ?? 0;
      attrs.y = node.y ?? 0;
      if (node.width !== undefined) attrs.width = node.width;
      if (node.height !== undefined) attrs.height = node.height;
    }
    elements.push({ id: nodeId, type: shapeType, attributes: attrs });
  }

  return {
    problem_id: layout?.problem_id ?? "",
    view_box: {
      width: canvas.width ?? 1200,
      height: canvas.height ?? 700,
      background: canvas.background ?? "#F6F6F6",
    },
    elements,
  };
}

const state = {
  problemId: parseJsonScript("problem-id"),
  semantic: parseJsonScript("initial-semantic"),
  layout: parseJsonScript("initial-layout"),
  renderer: parseJsonScript("initial-renderer"),
  selectedId: null,
  drag: null,
  mouseupBound: false,
  jsonDirty: false,
};

ensureShape(state.semantic);

const canvasHost = byId("canvas-host");
const cursorPosition = byId("cursor-position");
const elementList = byId("element-list");
const form = byId("properties-form");
const semanticTextarea = byId("semantic-json-text");
const layoutTextarea = byId("layout-json-text");
const rendererTextarea = byId("renderer-json-text");
const statusLine = byId("status-line");
const applyJsonBtn = byId("apply-json-btn");

function refreshDerivedBundle() {
  state.layout = deriveLayoutFromSemantic(state.problemId, state.semantic);
  state.renderer = deriveRendererFromLayout(state.layout);
}

function selectedElement() {
  return getElements(state.semantic).find((el) => el.id === state.selectedId) ?? null;
}

function renderElementList() {
  const items = getElements(state.semantic)
    .map((el) => {
      const cls = el.id === state.selectedId ? "active" : "";
      return `<li class="${cls}" data-element-id="${el.id}"><strong>${el.id}</strong> <small>${el.type}</small></li>`;
    })
    .join("");
  elementList.innerHTML = items;
}

function renderAll(forceJsonSync = false) {
  renderCanvas(canvasHost, state.semantic, state.selectedId);
  renderElementList();
  fillPropertiesForm(form, selectedElement());
  if (forceJsonSync || !state.jsonDirty) {
    semanticTextarea.value = JSON.stringify(state.semantic, null, 2);
  }
  layoutTextarea.value = JSON.stringify(state.layout, null, 2);
  rendererTextarea.value = JSON.stringify(state.renderer, null, 2);
  wireCanvasHandlers();
}

function syncJsonFromState() {
  refreshDerivedBundle();
  state.jsonDirty = false;
  renderAll(true);
}

function updateStatus(message, isError = false) {
  statusLine.textContent = message;
  statusLine.classList.toggle("error", isError);
}

function updateCursorPosition(x, y) {
  if (!cursorPosition) return;
  if (Number.isFinite(x) && Number.isFinite(y)) {
    cursorPosition.textContent = `x: ${Math.round(x)}, y: ${Math.round(y)}`;
    return;
  }
  cursorPosition.textContent = "x: -, y: -";
}

function moveElement(el, dx, dy) {
  if (!el) return;
  if (el.type === "line") {
    el.x1 = Number(el.x1 ?? 0) + dx;
    el.y1 = Number(el.y1 ?? 0) + dy;
    el.x2 = Number(el.x2 ?? 0) + dx;
    el.y2 = Number(el.y2 ?? 0) + dy;
    return;
  }
  el.x = Number(el.x ?? 0) + dx;
  el.y = Number(el.y ?? 0) + dy;
}

function wireCanvasHandlers() {
  const svg = byId("editor-svg");
  if (!svg) return;

  svg.querySelectorAll("[data-element-id]").forEach((node) => {
    node.addEventListener("mousedown", (event) => {
      event.preventDefault();
      const elementId = node.getAttribute("data-element-id");
      state.selectedId = elementId;
      const p = eventToSvgPoint(svg, event);
      state.drag = { startX: p.x, startY: p.y, originId: elementId };
      renderAll();
    });
  });

  svg.addEventListener("mousemove", (event) => {
    const p = eventToSvgPoint(svg, event);
    updateCursorPosition(p.x, p.y);
    if (!state.drag || !state.selectedId) return;
    const dx = p.x - state.drag.startX;
    const dy = p.y - state.drag.startY;
    state.drag.startX = p.x;
    state.drag.startY = p.y;
    moveElement(selectedElement(), dx, dy);
    renderAll();
  });

  svg.addEventListener("mouseleave", () => {
    updateCursorPosition(NaN, NaN);
  });

  if (!state.mouseupBound) {
    window.addEventListener("mouseup", () => {
      if (state.drag) {
        syncJsonFromState();
      }
      state.drag = null;
    });
    state.mouseupBound = true;
  }
}

elementList.addEventListener("click", (event) => {
  const li = event.target.closest("[data-element-id]");
  if (!li) return;
  state.selectedId = li.getAttribute("data-element-id");
  renderAll();
});

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const el = selectedElement();
  if (!el) return;
  applyPropertiesForm(form, el);
  state.selectedId = el.id;
  syncJsonFromState();
});

document.querySelectorAll("[data-add-type]").forEach((button) => {
  button.addEventListener("click", () => {
    const type = button.getAttribute("data-add-type");
    const elements = getElements(state.semantic);
    const created = newElement(type, elements);
    elements.push(created);
    state.selectedId = created.id;
    syncJsonFromState();
  });
});

byId("delete-element-btn").addEventListener("click", () => {
  if (!state.selectedId) return;
  state.semantic.render.elements = getElements(state.semantic).filter((el) => el.id !== state.selectedId);
  state.selectedId = null;
  syncJsonFromState();
});

async function applyJsonEditorToState() {
  let parsed;
  try {
    parsed = JSON.parse(semanticTextarea.value);
  } catch (error) {
    updateStatus("Semantic JSON 형식이 올바르지 않습니다.", true);
    return false;
  }

  state.semantic = parsed;
  ensureShape(state.semantic);
  refreshDerivedBundle();
  state.jsonDirty = false;
  renderAll(true);

  let result;
  try {
    result = await applySemantic(state.problemId, parsed);
  } catch (error) {
    updateStatus("캔버스는 반영했지만 서버 통신 중 오류가 발생했습니다.", true);
    return true;
  }

  if (!result.ok) {
    updateStatus(`캔버스는 반영했지만 서버 검증 실패: ${(result.errors ?? ["JSON 반영 실패"]).join(" | ")}`, true);
    return true;
  }

  state.semantic = result.semantic;
  ensureShape(state.semantic);
  state.layout = result.layout ?? deriveLayoutFromSemantic(state.problemId, state.semantic);
  state.renderer = result.renderer ?? deriveRendererFromLayout(state.layout);
  state.jsonDirty = false;
  renderAll(true);
  updateStatus("Semantic 검증 후 Layout/Renderer까지 동기화했습니다.");
  return true;
}

semanticTextarea.addEventListener("input", () => {
  state.jsonDirty = true;
});

if (applyJsonBtn) {
  applyJsonBtn.addEventListener("click", async () => {
    await applyJsonEditorToState();
  });
}

byId("save-btn").addEventListener("click", async () => {
  let parsed;
  try {
    parsed = JSON.parse(semanticTextarea.value);
  } catch (error) {
    updateStatus("Semantic JSON 형식이 올바르지 않습니다.", true);
    return;
  }

  state.semantic = parsed;
  ensureShape(state.semantic);
  refreshDerivedBundle();
  state.jsonDirty = false;
  renderAll(true);

  let result;
  try {
    result = await saveSemantic(state.problemId, state.semantic);
  } catch (error) {
    updateStatus("서버 통신 중 오류가 발생했습니다.", true);
    return;
  }

  if (!result.ok) {
    updateStatus((result.errors ?? ["저장 실패"]).join(" | "), true);
    return;
  }

  state.semantic = result.semantic;
  ensureShape(state.semantic);
  state.layout = result.layout ?? deriveLayoutFromSemantic(state.problemId, state.semantic);
  state.renderer = result.renderer ?? deriveRendererFromLayout(state.layout);
  state.jsonDirty = false;
  updateStatus("저장 완료: semantic/layout/renderer 파일에 반영했습니다.");
  renderAll(true);
});

refreshDerivedBundle();
renderAll(true);
updateCursorPosition(NaN, NaN);
