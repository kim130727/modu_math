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
  if (type === "polygon") {
    return {
      id: makeId("polygon", elements),
      type,
      points: [[200, 400], [400, 150], [600, 400]],
      stroke: "#222",
      stroke_width: 2,
      fill: "none",
    };
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
  selectedIds: [], // 단일 ID 대신 배열로 관리
  lockListSelectionHighlight: false,
  drag: null,
  suppressListClickUntil: 0,
  mouseupBound: false,
  jsonDirty: false,
  undoStack: [],
  redoStack: [],
};

function pushHistory() {
  state.undoStack.push(JSON.parse(JSON.stringify(state.semantic)));
  state.redoStack = []; // 새로운 동작 시 Redo 스택 초기화
  if (state.undoStack.length > 50) state.undoStack.shift(); // 최대 50개 유지
}

function undo() {
  if (state.undoStack.length === 0) return;
  state.redoStack.push(JSON.parse(JSON.stringify(state.semantic)));
  state.semantic = state.undoStack.pop();
  syncJsonFromState();
  updateStatus("실행 취소(Undo) 완료");
}

function redo() {
  if (state.redoStack.length === 0) return;
  state.undoStack.push(JSON.parse(JSON.stringify(state.semantic)));
  state.semantic = state.redoStack.pop();
  syncJsonFromState();
  updateStatus("다시 실행(Redo) 완료");
}

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
const undoBtn = byId("undo-btn");
const redoBtn = byId("redo-btn");

function refreshDerivedBundle() {
  state.layout = deriveLayoutFromSemantic(state.problemId, state.semantic);
  state.renderer = deriveRendererFromLayout(state.layout);
}

function selectedElement() {
  const selId = state.selectedIds[0] ?? null;
  return getElements(state.semantic).find((el) => el.id === selId) ?? null;
}

function renderElementList() {
  const showActive = !state.lockListSelectionHighlight;
  const items = getElements(state.semantic)
    .map((el) => {
      const cls = showActive && state.selectedIds.includes(el.id) ? "active" : "";
      return `<li class="${cls}" data-element-id="${el.id}"><strong>${el.id}</strong> <small>${el.type}</small></li>`;
    })
    .join("");
  elementList.innerHTML = items;
}

function renderAll(forceJsonSync = false) {
  renderCanvas(canvasHost, state.semantic, state.selectedIds, state.drag, _selectionBoundsFromLayout(state.selectedIds));
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

function _applyMove(el, dx, dy) {
  if (el.type === "line") {
    el.x1 = Number(el.x1 ?? 0) + dx;
    el.y1 = Number(el.y1 ?? 0) + dy;
    el.x2 = Number(el.x2 ?? 0) + dx;
    el.y2 = Number(el.y2 ?? 0) + dy;
  } else if (el.type === "polygon" && Array.isArray(el.points)) {
    el.points = el.points.map((p) => [Number(p[0] ?? 0) + dx, Number(p[1] ?? 0) + dy]);
  } else {
    el.x = Number(el.x ?? 0) + dx;
    el.y = Number(el.y ?? 0) + dy;
  }
}

function moveElement(el, dx, dy, allElements = []) {
  if (!el) return;

  const oldX = Number(el.x ?? el.x1 ?? 0);
  const oldY = Number(el.y ?? el.y1 ?? 0);

  // 1. 기본 요소 이동
  _applyMove(el, dx, dy);

  // 2. 연동 드래그 로직 (geom_point_ 로 시작하는 경우에만 발동)
  if (el.id.startsWith("geom_point_")) {
    const suffix = el.id.replace("geom_point_", "");
    const tolerance = 2.0; // 좌표 일치 판정 허용 오차

    for (const other of allElements) {
      if (other.id === el.id) continue;

      // A. ID 기반 연동 (레이블 등)
      if (other.id === `geom_label_${suffix}`) {
        _applyMove(other, dx, dy);
        continue;
      }

      // B. 좌표 기반 연동 (다각형 꼭지점)
      if (other.type === "polygon" && Array.isArray(other.points)) {
        let changed = false;
        other.points = other.points.map((p) => {
          if (Math.hypot(p[0] - oldX, p[1] - oldY) < tolerance) {
            changed = true;
            return [p[0] + dx, p[1] + dy];
          }
          return p;
        });
        continue;
      }

      // C. 좌표 기반 연동 (선, 치수선 끝점)
      if (other.type === "line") {
        if (Math.hypot(Number(other.x1 ?? 0) - oldX, Number(other.y1 ?? 0) - oldY) < tolerance) {
          other.x1 = Number(other.x1 ?? 0) + dx;
          other.y1 = Number(other.y1 ?? 0) + dy;
        }
        if (Math.hypot(Number(other.x2 ?? 0) - oldX, Number(other.y2 ?? 0) - oldY) < tolerance) {
          other.x2 = Number(other.x2 ?? 0) + dx;
          other.y2 = Number(other.y2 ?? 0) + dy;
        }
        continue;
      }

      // D. 좌표 기반 연동 (원 중심)
      if (other.type === "circle") {
        if (Math.hypot(Number(other.x ?? 0) - oldX, Number(other.y ?? 0) - oldY) < tolerance) {
          other.x = Number(other.x ?? 0) + dx;
          other.y = Number(other.y ?? 0) + dy;
        }
        continue;
      }
    }
    return;
  }

  // 3. 반대 방향 연동: 다각형(Polygon)을 옮길 때 그 꼭지점에 있는 점/레이블들도 같이 이동
  if (el.type === "polygon" && Array.isArray(el.points)) {
    const tolerance = 2.0;
    // 다각형의 '이동 전' 꼭지점 좌표들 (이미 _applyMove가 실행되었으므로 p - dx, p - dy 가 원래 좌표)
    const originalPoints = el.points.map(p => [p[0] - dx, p[1] - dy]);

    for (const other of allElements) {
      if (other.id === el.id) continue;

      // 점(Point)이나 레이블(Label)이 다각형의 어떤 꼭지점과 일치하는지 확인
      const ox = Number(other.x ?? other.x1 ?? 0);
      const oy = Number(other.y ?? other.y1 ?? 0);

      const isMatchingPoint = originalPoints.some(p => Math.hypot(p[0] - ox, p[1] - oy) < tolerance);

      if (isMatchingPoint) {
        _applyMove(other, dx, dy);

        // 점과 연결된 레이블이 있다면 그것도 함께 이동 (ID 규칙 기반)
        if (other.id.startsWith("geom_point_")) {
          const suffix = other.id.replace("geom_point_", "");
          const label = allElements.find(a => a.id === `geom_label_${suffix}`);
          if (label) _applyMove(label, dx, dy);
        }
      }
    }
  }
}

function rotateElement(el, da, cx, cy, allElements = []) {
  if (!el || el.type !== "polygon" || !Array.isArray(el.points)) return;

  const cos = Math.cos(da);
  const sin = Math.sin(da);

  // 다각형 회전
  const oldPoints = el.points.map(p => [...p]);
  el.points = el.points.map((p) => {
    const dx = p[0] - cx;
    const dy = p[1] - cy;
    return [
      dx * cos - dy * sin + cx,
      dx * sin + dy * cos + cy
    ];
  });

  // 연동된 요소들도 함께 회전
  const tolerance = 2.0;
  for (const other of allElements) {
    if (other.id === el.id) continue;

    const ox = Number(other.x ?? other.x1 ?? 0);
    const oy = Number(other.y ?? other.y1 ?? 0);

    const matchIdx = oldPoints.findIndex(p => Math.hypot(p[0] - ox, p[1] - oy) < tolerance);
    if (matchIdx >= 0) {
      // 해당 꼭지점의 새로운 좌표로 이동
      const np = el.points[matchIdx];
      const moveDx = np[0] - ox;
      const moveDy = np[1] - oy;
      _applyMove(other, moveDx, moveDy);

      // 점과 연결된 레이블이 있다면 그것도 함께 이동
      if (other.id.startsWith("geom_point_")) {
        const suffix = other.id.replace("geom_point_", "");
        const label = allElements.find(a => a.id === `geom_label_${suffix}`);
        if (label) _applyMove(label, moveDx, moveDy);
      }
    }
  }
}

function _elementPointsForBounds(el) {
  if (!el || typeof el !== "object") return [];
  if (el.type === "line") {
    return [
      [Number(el.x1 ?? 0), Number(el.y1 ?? 0)],
      [Number(el.x2 ?? 0), Number(el.y2 ?? 0)],
    ];
  }
  if (el.type === "rect") {
    const x = Number(el.x ?? 0);
    const y = Number(el.y ?? 0);
    const w = Number(el.width ?? 120);
    const h = Number(el.height ?? 80);
    return [
      [x, y],
      [x + w, y + h],
    ];
  }
  if (el.type === "circle") {
    const cx = Number(el.x ?? 0);
    const cy = Number(el.y ?? 0);
    const r = Number(el.r ?? 35);
    return [
      [cx - r, cy - r],
      [cx + r, cy + r],
    ];
  }
  if (el.type === "polygon" && Array.isArray(el.points)) {
    return el.points.map((p) => [Number(p[0] ?? 0), Number(p[1] ?? 0)]);
  }
  if (el.type === "text" || el.type === "formula") {
    return [[Number(el.x ?? 0), Number(el.y ?? 0)]];
  }
  const x = Number(el.x ?? 0);
  const y = Number(el.y ?? 0);
  const w = Number(el.width ?? 0);
  const h = Number(el.height ?? 0);
  return [
    [x, y],
    [x + w, y + h],
  ];
}

function _selectionBoundsFromElements(allElements, selectedIds) {
  if (!Array.isArray(selectedIds) || selectedIds.length === 0) return null;

  let minX = Infinity;
  let minY = Infinity;
  let maxX = -Infinity;
  let maxY = -Infinity;
  let hasPoint = false;

  for (const id of selectedIds) {
    const el = allElements.find((item) => item.id === id);
    if (!el) continue;
    for (const [x, y] of _elementPointsForBounds(el)) {
      hasPoint = true;
      minX = Math.min(minX, x);
      minY = Math.min(minY, y);
      maxX = Math.max(maxX, x);
      maxY = Math.max(maxY, y);
    }
  }

  if (!hasPoint) return null;
  if (Math.abs(maxX - minX) < 1) {
    minX -= 12;
    maxX += 12;
  }
  if (Math.abs(maxY - minY) < 1) {
    minY -= 12;
    maxY += 12;
  }
  return { minX, minY, maxX, maxY };
}

function _layoutNodePoints(node) {
  if (!node || typeof node !== "object") return [];
  const props = node.properties || {};
  const shapeType = String(props.shape_type ?? "");

  if (shapeType === "line") {
    return [
      [Number(props.x1 ?? node.x ?? 0), Number(props.y1 ?? node.y ?? 0)],
      [Number(props.x2 ?? node.x ?? 0), Number(props.y2 ?? node.y ?? 0)],
    ];
  }
  if (shapeType === "polygon" && Array.isArray(props.points)) {
    return props.points.map((p) => [Number(p[0] ?? 0), Number(p[1] ?? 0)]);
  }
  if (shapeType === "circle") {
    const cx = Number(node.x ?? 0);
    const cy = Number(node.y ?? 0);
    const r = Number(props.r ?? 35);
    return [
      [cx - r, cy - r],
      [cx + r, cy + r],
    ];
  }
  if (shapeType === "rect") {
    const x = Number(node.x ?? 0);
    const y = Number(node.y ?? 0);
    const w = Number(node.width ?? 120);
    const h = Number(node.height ?? 80);
    return [
      [x, y],
      [x + w, y + h],
    ];
  }
  if (String(node.type ?? "") === "text") {
    return [[Number(node.x ?? 0), Number(node.y ?? 0)]];
  }

  const x = Number(node.x ?? 0);
  const y = Number(node.y ?? 0);
  const w = Number(node.width ?? 0);
  const h = Number(node.height ?? 0);
  return [
    [x, y],
    [x + w, y + h],
  ];
}

function _selectionBoundsFromLayout(selectedIds) {
  if (!Array.isArray(selectedIds) || selectedIds.length === 0) return null;
  const layoutNodes = Array.isArray(state.layout?.nodes) ? state.layout.nodes : [];

  let minX = Infinity;
  let minY = Infinity;
  let maxX = -Infinity;
  let maxY = -Infinity;
  let hasPoint = false;

  for (const id of selectedIds) {
    const node = layoutNodes.find((n) => n.id === id);
    if (!node) continue;
    for (const [x, y] of _layoutNodePoints(node)) {
      hasPoint = true;
      minX = Math.min(minX, x);
      minY = Math.min(minY, y);
      maxX = Math.max(maxX, x);
      maxY = Math.max(maxY, y);
    }
  }

  if (!hasPoint) return null;
  if (Math.abs(maxX - minX) < 1) {
    minX -= 12;
    maxX += 12;
  }
  if (Math.abs(maxY - minY) < 1) {
    minY -= 12;
    maxY += 12;
  }
  return { minX, minY, maxX, maxY };
}

function _scalePoint(px, py, anchorX, anchorY, factor) {
  return [
    anchorX + (px - anchorX) * factor,
    anchorY + (py - anchorY) * factor,
  ];
}

function _applyResizeFromSnapshot(target, snapshot, factorX, factorY, anchorX, anchorY) {
  if (!target || !snapshot) return;

  if (snapshot.type === "line") {
    const sx1 = anchorX + (Number(snapshot.x1 ?? 0) - anchorX) * factorX;
    const sy1 = anchorY + (Number(snapshot.y1 ?? 0) - anchorY) * factorY;
    const sx2 = anchorX + (Number(snapshot.x2 ?? 0) - anchorX) * factorX;
    const sy2 = anchorY + (Number(snapshot.y2 ?? 0) - anchorY) * factorY;
    target.x1 = sx1;
    target.y1 = sy1;
    target.x2 = sx2;
    target.y2 = sy2;
    return;
  }

  if (snapshot.type === "polygon" && Array.isArray(snapshot.points)) {
    target.points = snapshot.points.map((p) => [
      anchorX + (Number(p[0] ?? 0) - anchorX) * factorX,
      anchorY + (Number(p[1] ?? 0) - anchorY) * factorY,
    ]);
    return;
  }

  if (snapshot.type === "circle") {
    const sx = anchorX + (Number(snapshot.x ?? 0) - anchorX) * factorX;
    const sy = anchorY + (Number(snapshot.y ?? 0) - anchorY) * factorY;
    const uniform = Math.sqrt(Math.abs(factorX * factorY));
    target.x = sx;
    target.y = sy;
    target.r = Math.max(1, Number(snapshot.r ?? 35) * uniform);
    return;
  }

  if (snapshot.type === "rect") {
    const x = Number(snapshot.x ?? 0);
    const y = Number(snapshot.y ?? 0);
    const w = Number(snapshot.width ?? 120);
    const h = Number(snapshot.height ?? 80);
    const p1x = anchorX + (x - anchorX) * factorX;
    const p1y = anchorY + (y - anchorY) * factorY;
    const p2x = anchorX + (x + w - anchorX) * factorX;
    const p2y = anchorY + (y + h - anchorY) * factorY;
    target.x = Math.min(p1x, p2x);
    target.y = Math.min(p1y, p2y);
    target.width = Math.max(1, Math.abs(p2x - p1x));
    target.height = Math.max(1, Math.abs(p2y - p1y));
    return;
  }

  const sx = anchorX + (Number(snapshot.x ?? 0) - anchorX) * factorX;
  const sy = anchorY + (Number(snapshot.y ?? 0) - anchorY) * factorY;
  const uniform = Math.sqrt(Math.abs(factorX * factorY));
  target.x = sx;
  target.y = sy;
  if (snapshot.font_size !== undefined) {
    target.font_size = Math.max(1, Number(snapshot.font_size) * uniform);
  }
  if (snapshot.width !== undefined && snapshot.height !== undefined) {
    target.width = Math.max(1, Number(snapshot.width) * factorX);
    target.height = Math.max(1, Number(snapshot.height) * factorY);
  }
}

function wireCanvasHandlers() {
  const svg = byId("editor-svg");
  if (!svg) return;

  svg.querySelectorAll("[data-element-id]").forEach((node) => {
    node.addEventListener("mousedown", (event) => {
      event.preventDefault();
      event.stopPropagation();
      const elementId = node.getAttribute("data-element-id");
      
      if (!state.selectedIds.includes(elementId)) {
        state.selectedIds = [elementId];
      }
      state.lockListSelectionHighlight = false;
      
      const p = eventToSvgPoint(svg, event);
      pushHistory();
      state.drag = { type: "move", startX: p.x, startY: p.y, originIds: [...state.selectedIds] };
      renderAll();
    });
  });

  // 배경(SVG 자체) mousedown: 다중 선택 시작
  svg.addEventListener("mousedown", (event) => {
    // 배경(canvas-background) 또는 SVG 본체를 클릭했을 때만 다중 선택 시작
    if (event.target === svg || event.target.id === "canvas-background") {
      event.preventDefault();
      const p = eventToSvgPoint(svg, event);
      state.selectedIds = []; // 선택 해제
      state.lockListSelectionHighlight = true;
      elementList.style.pointerEvents = "none";
      state.drag = { type: "selection", startX: p.x, startY: p.y, currentX: p.x, currentY: p.y };
      renderAll();
    }
  });

  // 회전 핸들 이벤트 바인딩
  svg.querySelectorAll("[data-rotate-handle]").forEach((node) => {
    node.addEventListener("mousedown", (event) => {
      event.preventDefault();
      event.stopPropagation();
      const elementId = node.getAttribute("data-rotate-handle");
      state.selectedIds = [elementId];
      state.lockListSelectionHighlight = false;
      const p = eventToSvgPoint(svg, event);
      
      const el = selectedElement();
      if (!el) return;
      let cx = 0, cy = 0;
      el.points.forEach((pt) => { cx += pt[0]; cy += pt[1]; });
      cx /= el.points.length; cy /= el.points.length;

      const startAngle = Math.atan2(p.y - cy, p.x - cx);
      pushHistory();
      state.drag = { type: "rotate", cx, cy, startAngle, originId: elementId };
      renderAll();
    });
  });

  // 크기 조절 핸들 이벤트 바인딩
  svg.querySelectorAll("[data-resize-handle]").forEach((node) => {
    node.addEventListener("mousedown", (event) => {
      event.preventDefault();
      event.stopPropagation();

      if (state.selectedIds.length === 0) return;
      const allElements = getElements(state.semantic);
      const bounds = _selectionBoundsFromLayout(state.selectedIds) ?? _selectionBoundsFromElements(allElements, state.selectedIds);
      if (!bounds) return;

      const handle = node.getAttribute("data-resize-handle");
      const anchorByHandle = {
        nw: [bounds.maxX, bounds.maxY],
        ne: [bounds.minX, bounds.maxY],
        sw: [bounds.maxX, bounds.minY],
        se: [bounds.minX, bounds.minY],
      };
      const anchor = anchorByHandle[handle];
      if (!anchor) return;

      const p = eventToSvgPoint(svg, event);
      const startHandleByKey = {
        nw: [bounds.minX, bounds.minY],
        ne: [bounds.maxX, bounds.minY],
        sw: [bounds.minX, bounds.maxY],
        se: [bounds.maxX, bounds.maxY],
      };
      const startHandlePoint = startHandleByKey[handle] ?? [p.x, p.y];
      const snapshots = {};
      state.selectedIds.forEach((id) => {
        const el = allElements.find((item) => item.id === id);
        if (el) snapshots[id] = JSON.parse(JSON.stringify(el));
      });

      pushHistory();
      state.lockListSelectionHighlight = false;
      state.drag = {
        type: "resize",
        handle,
        anchorX: anchor[0],
        anchorY: anchor[1],
        startHandleX: startHandlePoint[0],
        startHandleY: startHandlePoint[1],
        originIds: [...state.selectedIds],
        snapshots,
      };
      renderAll();
    });
  });

  svg.addEventListener("mousemove", (event) => {
    const p = eventToSvgPoint(svg, event);
    updateCursorPosition(p.x, p.y);
    if (!state.drag) return;

    if (state.drag.type === "move") {
      const dx = p.x - state.drag.startX;
      const dy = p.y - state.drag.startY;
      state.drag.startX = p.x;
      state.drag.startY = p.y;
      
      const allElements = getElements(state.semantic);
      state.drag.originIds.forEach(id => {
        const el = allElements.find(e => e.id === id);
        if (el) moveElement(el, dx, dy, allElements);
      });
    } else if (state.drag.type === "rotate") {
      const currentAngle = Math.atan2(p.y - state.drag.cy, p.x - state.drag.cx);
      const da = currentAngle - state.drag.startAngle;
      state.drag.startAngle = currentAngle;
      
      const allElements = getElements(state.semantic);
      const el = allElements.find(e => e.id === state.drag.originId);
      if (el) rotateElement(el, da, state.drag.cx, state.drag.cy, allElements);
    } else if (state.drag.type === "selection") {
      state.drag.currentX = p.x;
      state.drag.currentY = p.y;
      _updateMarqueeSelection();
    } else if (state.drag.type === "resize") {
      const startVx = state.drag.startHandleX - state.drag.anchorX;
      const startVy = state.drag.startHandleY - state.drag.anchorY;
      const currentVx = p.x - state.drag.anchorX;
      const currentVy = p.y - state.drag.anchorY;

      let fx = NaN;
      let fy = NaN;
      if (Math.abs(startVx) > 1e-6) {
        const value = currentVx / startVx;
        if (Number.isFinite(value) && value > 0) fx = value;
      }
      if (Math.abs(startVy) > 1e-6) {
        const value = currentVy / startVy;
        if (Number.isFinite(value) && value > 0) fy = value;
      }

      if (!Number.isFinite(fx) && Number.isFinite(fy)) fx = fy;
      if (!Number.isFinite(fy) && Number.isFinite(fx)) fy = fx;
      if (!Number.isFinite(fx)) fx = 1;
      if (!Number.isFinite(fy)) fy = 1;

      let factorX = fx;
      let factorY = fy;

      // Shift: 정비율(비율 고정) 스케일
      if (event.shiftKey) {
        const uniform = Math.sqrt(Math.abs(fx * fy));
        factorX = uniform;
        factorY = uniform;
      }
      factorX = Math.max(0.05, Math.min(20, factorX));
      factorY = Math.max(0.05, Math.min(20, factorY));

      const allElements = getElements(state.semantic);
      state.drag.originIds.forEach((id) => {
        const el = allElements.find((item) => item.id === id);
        const snapshot = state.drag.snapshots?.[id];
        if (el && snapshot) {
          _applyResizeFromSnapshot(el, snapshot, factorX, factorY, state.drag.anchorX, state.drag.anchorY);
        }
      });
    }
    renderAll();
  });

  svg.addEventListener("mouseleave", () => {
    updateCursorPosition(NaN, NaN);
  });

  if (!state.mouseupBound) {
    window.addEventListener("mouseup", () => {
      const finishedDragType = state.drag?.type ?? null;
      if (state.drag) {
        // 드래그 시작 시점의 상태가 아닌, 변형 후 상태를 저장하기 위해 이전에 pushHistory를 호출하지 않았다면
        // 드래그 종료 시점에 현재 상태를 히스토리에 기록할 수 있도록 설계합니다.
        // 다만 드래그는 연속적이므로 시작 시점에 한 번 저장하는 것이 일반적입니다.
        syncJsonFromState();
      }
      state.drag = null;
      if (finishedDragType === "selection") {
        state.suppressListClickUntil = Date.now() + 900;
        setTimeout(() => {
          elementList.style.pointerEvents = "";
        }, 950);
      } else {
        elementList.style.pointerEvents = "";
      }
    });
    state.mouseupBound = true;
  }
}

function shouldBlockElementListEvent(event) {
  return Date.now() < state.suppressListClickUntil && Boolean(event.target.closest("#element-list"));
}

["mousedown", "mouseup", "click"].forEach((eventName) => {
  document.addEventListener(eventName, (event) => {
    if (!shouldBlockElementListEvent(event)) return;
    event.preventDefault();
    event.stopImmediatePropagation();
    event.stopPropagation();
  }, true);
});

elementList.addEventListener("mousedown", (event) => {
  if (Date.now() < state.suppressListClickUntil) {
    event.preventDefault();
    event.stopPropagation();
    return;
  }
  const li = event.target.closest("[data-element-id]");
  if (!li) return;
  event.preventDefault();
  state.lockListSelectionHighlight = false;
  state.selectedIds = [li.getAttribute("data-element-id")];
  renderAll();
});

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const el = selectedElement();
  if (!el) return;
  pushHistory(); // 속성 변경 전 저장
  applyPropertiesForm(form, el);
  state.lockListSelectionHighlight = false;
  state.selectedIds = [el.id];
  syncJsonFromState();
});

document.querySelectorAll("[data-add-type]").forEach((button) => {
  button.addEventListener("click", () => {
    const type = button.getAttribute("data-add-type");
    const elements = getElements(state.semantic);
    pushHistory(); // 요소 추가 전 저장
    const created = newElement(type, elements);
    elements.push(created);
    state.lockListSelectionHighlight = false;
    state.selectedIds = [created.id];
    syncJsonFromState();
  });
});

byId("delete-element-btn").addEventListener("click", () => {
  if (state.selectedIds.length === 0) return;
  pushHistory(); // 삭제 전 저장
  const selectedSet = new Set(state.selectedIds);
  state.semantic.render.elements = getElements(state.semantic).filter((el) => !selectedSet.has(el.id));
  state.lockListSelectionHighlight = false;
  state.selectedIds = [];
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

  pushHistory(); // 직접 편집 반영 전 저장
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

if (undoBtn) undoBtn.addEventListener("click", undo);
if (redoBtn) redoBtn.addEventListener("click", redo);

window.addEventListener("keydown", (e) => {
  if (e.target.tagName === "TEXTAREA" || e.target.tagName === "INPUT") return;
  
  if (e.ctrlKey || e.metaKey) {
    if (e.key === "z") {
      e.preventDefault();
      undo();
    } else if (e.key === "y" || (e.shiftKey && e.key === "Z")) {
      e.preventDefault();
      redo();
    }
  } else {
    if (e.key === "[") {
      scaleSelectedElements(0.9);
    } else if (e.key === "]") {
      scaleSelectedElements(1.1);
    }
  }
});

refreshDerivedBundle();
renderAll(true);
updateCursorPosition(NaN, NaN);

function _updateMarqueeSelection() {
  if (!state.drag || state.drag.type !== "selection") return;
  
  // 캔버스 크기 가져오기
  const canvas = state.semantic.render?.canvas || state.layout?.canvas || {};
  const cw = Number(canvas.width || 1200);
  const ch = Number(canvas.height || 700);
  
  const x1 = Math.max(0, Math.min(cw, Math.min(state.drag.startX, state.drag.currentX)));
  const y1 = Math.max(0, Math.min(ch, Math.min(state.drag.startY, state.drag.currentY)));
  const x2 = Math.max(0, Math.min(cw, Math.max(state.drag.startX, state.drag.currentX)));
  const y2 = Math.max(0, Math.min(ch, Math.max(state.drag.startY, state.drag.currentY)));

  // layout 데이터를 기준으로 위치 판단 (실제 화면 좌표가 여기 있음)
  const layoutNodes = state.layout?.nodes || [];
  state.selectedIds = layoutNodes.filter(node => {
    // 배경 영역 제외
    if (node.id === "geom_diagram_region" || node.id === "canvas-background") return false;

    // 노드의 좌표 (points가 있으면 첫 번째 점, 없으면 x, y)
    const props = node.properties || {};
    const ex = Number(node.x ?? props.x1 ?? (props.points ? props.points[0][0] : 0));
    const ey = Number(node.y ?? props.y1 ?? (props.points ? props.points[0][1] : 0));
    
    return ex >= x1 && ex <= x2 && ey >= y1 && ey <= y2;
  }).map(node => node.id);
}

function scaleSelectedElements(factor) {
  if (state.selectedIds.length === 0) return;
  pushHistory();
  
  const allElements = getElements(state.semantic);
  const layoutNodes = state.layout?.nodes || [];
  
  // 선택된 요소들의 현재 '실제' 위치 정보(layout) 수집
  const selectedNodes = layoutNodes.filter(n => state.selectedIds.includes(n.id));
  if (selectedNodes.length === 0) return;

  // 전체 선택 그룹의 중심점 계산
  let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
  selectedNodes.forEach(node => {
    const props = node.properties || {};
    const pts = props.points || [[node.x ?? props.x1 ?? 0, node.y ?? props.y1 ?? 0], [props.x2 ?? node.x ?? 0, props.y2 ?? node.y ?? 0]];
    pts.forEach(p => {
      minX = Math.min(minX, Number(p[0] || 0));
      minY = Math.min(minY, Number(p[1] || 0));
      maxX = Math.max(maxX, Number(p[0] || 0));
      maxY = Math.max(maxY, Number(p[1] || 0));
    });
  });
  const cx = (minX + maxX) / 2;
  const cy = (minY + maxY) / 2;

  // semantic 데이터 업데이트
  state.selectedIds.forEach(id => {
    const el = allElements.find(e => e.id === id);
    if (!el) return;
    const node = layoutNodes.find(n => n.id === id);
    if (!node) return;
    const props = node.properties || {};

    // 1. 현재 레이아웃 정보를 semantic으로 강제 동기화 (좌표가 없는 경우 대비)
    if (el.type === "polygon" || props.shape_type === "polygon") {
      el.type = "polygon";
      el.points = (props.points || []).map(p => [
        (p[0] - cx) * factor + cx,
        (p[1] - cy) * factor + cy
      ]);
    } else if (el.type === "circle" || props.shape_type === "circle") {
      const nx = (Number(node.x) - cx) * factor + cx;
      const ny = (Number(node.y) - cy) * factor + cy;
      el.x = nx; el.y = ny;
      el.r = Number(props.r || 35) * factor;
    } else if (el.type === "line" || props.shape_type === "line") {
      el.x1 = (Number(props.x1) - cx) * factor + cx;
      el.y1 = (Number(props.y1) - cy) * factor + cy;
      el.x2 = (Number(props.x2) - cx) * factor + cx;
      el.y2 = (Number(props.y2) - cy) * factor + cy;
    } else {
      // 텍스트 등 일반 요소
      const nx = (Number(node.x) - cx) * factor + cx;
      const ny = (Number(node.y) - cy) * factor + cy;
      el.x = nx; el.y = ny;
      if (el.font_size || props.font_size) {
        el.font_size = Number(el.font_size || props.font_size || 24) * factor;
      }
    }
  });
  
  syncJsonFromState();
}
