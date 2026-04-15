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

const state = {
  problemId: parseJsonScript("problem-id"),
  semantic: parseJsonScript("initial-semantic"),
  selectedId: null,
  drag: null,
  mouseupBound: false,
  jsonDirty: false,
};

ensureShape(state.semantic);

const canvasHost = byId("canvas-host");
const elementList = byId("element-list");
const form = byId("properties-form");
const jsonTextarea = byId("semantic-json-text");
const statusLine = byId("status-line");
const applyJsonBtn = byId("apply-json-btn");

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
    jsonTextarea.value = JSON.stringify(state.semantic, null, 2);
  }
  wireCanvasHandlers();
}

function syncJsonFromState() {
  state.jsonDirty = false;
  renderAll(true);
}

function updateStatus(message, isError = false) {
  statusLine.textContent = message;
  statusLine.classList.toggle("error", isError);
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
    if (!state.drag || !state.selectedId) return;
    const p = eventToSvgPoint(svg, event);
    const dx = p.x - state.drag.startX;
    const dy = p.y - state.drag.startY;
    state.drag.startX = p.x;
    state.drag.startY = p.y;
    moveElement(selectedElement(), dx, dy);
    renderAll();
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
    parsed = JSON.parse(jsonTextarea.value);
  } catch (error) {
    updateStatus("semantic JSON 형식이 올바르지 않습니다.", true);
    return false;
  }

  // 즉시 로컬 반영
  state.semantic = parsed;
  ensureShape(state.semantic);
  state.jsonDirty = false;
  renderAll(true);

  // 서버 canonicalize/validate 반영
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
  state.jsonDirty = false;
  renderAll(true);
  updateStatus("JSON 내용을 검증/정규화 후 캔버스에 반영했습니다.");
  return true;
}

jsonTextarea.addEventListener("input", () => {
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
    parsed = JSON.parse(jsonTextarea.value);
  } catch (error) {
    updateStatus("semantic JSON 형식이 올바르지 않습니다.", true);
    return;
  }

  state.semantic = parsed;
  ensureShape(state.semantic);
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
  state.jsonDirty = false;
  updateStatus("저장 완료: semantic JSON 파일까지 반영했습니다.");
  renderAll(true);
});

renderAll(true);

