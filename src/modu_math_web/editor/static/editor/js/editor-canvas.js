export function initCanvas({ container, onSelectionChange, onCommand, getState } = {}) {
  return {
    container,
    onSelectionChange,
    onCommand,
    getState,
  };
}

export function renderSvgContainer(container, svgText) {
  if (!container) return;
  container.innerHTML = `${svgText || "<em>SVG 없음</em>"}<div class="marquee" id="marqueeBox"></div><input id="inlineTextEditor" class="inline-text-editor" autocomplete="off" spellcheck="false">`;
}

export function beginMarqueeBox(svg, container, box, ev) {
  if (!svg || !container || !box || !ev) return null;
  const start = svgPoint(svg, ev.clientX, ev.clientY);
  const state = {
    svg,
    pointerId: ev.pointerId,
    startSvg: start,
    startClientX: ev.clientX,
    startClientY: ev.clientY,
  };
  const rect = container.getBoundingClientRect();
  box.style.display = "block";
  box.style.left = `${ev.clientX - rect.left}px`;
  box.style.top = `${ev.clientY - rect.top}px`;
  box.style.width = "0px";
  box.style.height = "0px";
  try {
    svg.setPointerCapture(ev.pointerId);
  } catch (_) {
    // Synthetic pointer events in tests may not have an active pointer.
  }
  return state;
}

export function updateMarqueeBox(container, box, state, ev) {
  if (!container || !box || !state || !ev) return;
  const rect = container.getBoundingClientRect();
  const x1 = state.startClientX - rect.left;
  const y1 = state.startClientY - rect.top;
  const x2 = ev.clientX - rect.left;
  const y2 = ev.clientY - rect.top;
  box.style.left = `${Math.min(x1, x2)}px`;
  box.style.top = `${Math.min(y1, y2)}px`;
  box.style.width = `${Math.abs(x2 - x1)}px`;
  box.style.height = `${Math.abs(y2 - y1)}px`;
}

export function finishMarqueeBox(box, state, ev) {
  if (!state || !ev) return null;
  if (box) box.style.display = "none";
  try {
    if (state.svg.hasPointerCapture(state.pointerId)) state.svg.releasePointerCapture(state.pointerId);
  } catch (_) {
    // Pointer capture can be absent in synthetic or interrupted pointer flows.
  }
  const end = svgPoint(state.svg, ev.clientX, ev.clientY);
  return {
    x: Math.min(state.startSvg.x, end.x),
    y: Math.min(state.startSvg.y, end.y),
    width: Math.abs(end.x - state.startSvg.x),
    height: Math.abs(end.y - state.startSvg.y),
  };
}

export function svgPoint(svg, clientX, clientY) {
  const point = svg.createSVGPoint();
  point.x = clientX;
  point.y = clientY;
  const ctm = svg.getScreenCTM();
  if (!ctm) return { x: clientX, y: clientY };
  return point.matrixTransform(ctm.inverse());
}

export function clientRectToSvgBox(svg, rect) {
  if (!svg || !rect) return null;
  const ctm = svg.getScreenCTM();
  if (!ctm) return null;
  const point = svg.createSVGPoint();
  const inverse = ctm.inverse();
  const corners = [
    [rect.left, rect.top],
    [rect.right, rect.top],
    [rect.right, rect.bottom],
    [rect.left, rect.bottom],
  ].map(([x, y]) => {
    point.x = x;
    point.y = y;
    return point.matrixTransform(inverse);
  });
  const xs = corners.map((item) => item.x);
  const ys = corners.map((item) => item.y);
  const minX = Math.min(...xs);
  const minY = Math.min(...ys);
  const maxX = Math.max(...xs);
  const maxY = Math.max(...ys);
  return { x: minX, y: minY, width: maxX - minX, height: maxY - minY };
}

export function selectedIdsFromSlots(selectedSlots) {
  if (!selectedSlots || typeof selectedSlots.keys !== "function") return [];
  return Array.from(selectedSlots.keys());
}

export function ensureSelectionOverlay(svg, onHandlePointerDown) {
  let layer = svg.querySelector("#selectionOverlay");
  if (layer) return layer;
  layer = document.createElementNS("http://www.w3.org/2000/svg", "g");
  layer.setAttribute("id", "selectionOverlay");
  layer.setAttribute("class", "selection-overlay");
  const bounds = document.createElementNS("http://www.w3.org/2000/svg", "rect");
  bounds.setAttribute("class", "selection-bounds");
  layer.appendChild(bounds);
  const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
  line.setAttribute("class", "selection-line");
  layer.appendChild(line);
  for (const name of ["r", "nw", "n", "ne", "w", "c", "e", "sw", "s", "se", "p1", "p2"]) {
    const handle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    handle.setAttribute("class", "selection-handle");
    handle.setAttribute("data-handle", name);
    handle.setAttribute("r", "5");
    if (onHandlePointerDown) handle.addEventListener("pointerdown", onHandlePointerDown);
    layer.appendChild(handle);
  }
  svg.appendChild(layer);
  return layer;
}

export function hideSelectionOverlay(layer) {
  if (!layer) return;
  layer.style.display = "none";
  layer.removeAttribute("transform");
}

export function updateSelectionOverlay(layer, { box, isCanvas = false, isLine = false, line = null, transform = "" } = {}) {
  if (!layer || !box || box.width < 0 || box.height < 0) {
    hideSelectionOverlay(layer);
    return;
  }
  if (transform) layer.setAttribute("transform", transform);
  else layer.removeAttribute("transform");

  const minSize = 1;
  const x = box.x;
  const y = box.y;
  const w = Math.max(box.width, minSize);
  const h = Math.max(box.height, minSize);
  const bounds = layer.querySelector(".selection-bounds");
  const lineNode = layer.querySelector(".selection-line");
  bounds.classList.toggle("canvas-selected", !!isCanvas);
  bounds.setAttribute("x", String(x));
  bounds.setAttribute("y", String(y));
  bounds.setAttribute("width", String(w));
  bounds.setAttribute("height", String(h));
  bounds.style.display = isLine ? "none" : "";

  if (lineNode) {
    if (isLine && line) {
      lineNode.style.display = "";
      lineNode.setAttribute("x1", String(line.x1));
      lineNode.setAttribute("y1", String(line.y1));
      lineNode.setAttribute("x2", String(line.x2));
      lineNode.setAttribute("y2", String(line.y2));
    } else {
      lineNode.style.display = "none";
    }
  }

  const points = selectionHandlePoints({ x, y, w, h, isLine, line });
  for (const handle of layer.querySelectorAll(".selection-handle")) {
    const name = handle.getAttribute("data-handle");
    const point = points[name];
    const lineHandle = name === "p1" || name === "p2";
    const visible = isLine ? (lineHandle || name === "c" || name === "r") : !lineHandle;
    handle.style.display = visible ? "" : "none";
    if (!point) continue;
    handle.setAttribute("cx", String(point[0]));
    handle.setAttribute("cy", String(point[1]));
  }

  layer.style.display = "";
}

function selectionHandlePoints({ x, y, w, h, isLine, line }) {
  const points = {
    nw: [x, y],
    n: [x + w / 2, y],
    ne: [x + w, y],
    r: [x + w / 2, y - 24],
    w: [x, y + h / 2],
    c: [x + w / 2, y + h / 2],
    e: [x + w, y + h / 2],
    sw: [x, y + h],
    s: [x + w / 2, y + h],
    se: [x + w, y + h],
  };
  if (!isLine || !line) return points;
  const { x1, y1, x2, y2 } = line;
  const mx = (x1 + x2) / 2;
  const my = (y1 + y2) / 2;
  const len = Math.hypot(x2 - x1, y2 - y1) || 1;
  const nx = -(y2 - y1) / len;
  const ny = (x2 - x1) / len;
  return {
    ...points,
    p1: [x1, y1],
    p2: [x2, y2],
    c: [mx, my],
    r: [mx + nx * 26, my + ny * 26],
  };
}

export function translateSelectionOverlay(layer, dx, dy) {
  if (!layer || layer.style.display === "none") return false;
  const moveAttr = (node, xName, yName) => {
    if (!node || node.style.display === "none") return;
    const x = Number(node.getAttribute(xName) || 0);
    const y = Number(node.getAttribute(yName) || 0);
    if (Number.isFinite(x)) node.setAttribute(xName, String(x + dx));
    if (Number.isFinite(y)) node.setAttribute(yName, String(y + dy));
  };
  const bounds = layer.querySelector(".selection-bounds");
  if (bounds && bounds.style.display !== "none") moveAttr(bounds, "x", "y");

  const line = layer.querySelector(".selection-line");
  if (line && line.style.display !== "none") {
    const x1 = Number(line.getAttribute("x1") || 0);
    const y1 = Number(line.getAttribute("y1") || 0);
    const x2 = Number(line.getAttribute("x2") || 0);
    const y2 = Number(line.getAttribute("y2") || 0);
    line.setAttribute("x1", String(x1 + dx));
    line.setAttribute("y1", String(y1 + dy));
    line.setAttribute("x2", String(x2 + dx));
    line.setAttribute("y2", String(y2 + dy));
  }

  for (const handle of layer.querySelectorAll(".selection-handle")) moveAttr(handle, "cx", "cy");
  for (const guide of layer.querySelectorAll(".path-edit-guide")) {
    const x1 = Number(guide.getAttribute("x1") || 0);
    const y1 = Number(guide.getAttribute("y1") || 0);
    const x2 = Number(guide.getAttribute("x2") || 0);
    const y2 = Number(guide.getAttribute("y2") || 0);
    guide.setAttribute("x1", String(x1 + dx));
    guide.setAttribute("y1", String(y1 + dy));
    guide.setAttribute("x2", String(x2 + dx));
    guide.setAttribute("y2", String(y2 + dy));
  }
  return true;
}

export function clearPathPointHandles(layer) {
  for (const old of layer.querySelectorAll(".path-point-handle, .path-edit-guide")) old.remove();
}

export function renderTableAdjustmentHandles(layer, dividerInfos, onHandlePointerDown) {
  for (const old of layer.querySelectorAll(".table-adjust-handle")) old.remove();
  for (const info of dividerInfos || []) {
    const handle = document.createElementNS("http://www.w3.org/2000/svg", "line");
    handle.setAttribute("class", "selection-handle table-adjust-handle");
    handle.setAttribute("data-handle", `table-${info.axis}:${info.slotId}`);
    handle.setAttribute("x1", String(info.x1));
    handle.setAttribute("y1", String(info.y1));
    handle.setAttribute("x2", String(info.x2));
    handle.setAttribute("y2", String(info.y2));
    handle.style.cursor = info.axis === "v" ? "ew-resize" : "ns-resize";
    if (onHandlePointerDown) handle.addEventListener("pointerdown", onHandlePointerDown);
    layer.appendChild(handle);
  }
}

export function renderPathPointHandles(layer, editable, onHandlePointerDown) {
  clearPathPointHandles(layer);
  if (!editable) return;
  if (editable.kind === "cubic") {
    const pairs = [[0, 1], [3, 2]];
    for (const [a, b] of pairs) {
      const guide = document.createElementNS("http://www.w3.org/2000/svg", "line");
      guide.setAttribute("class", "path-edit-guide");
      guide.setAttribute("x1", String(editable.points[a].x));
      guide.setAttribute("y1", String(editable.points[a].y));
      guide.setAttribute("x2", String(editable.points[b].x));
      guide.setAttribute("y2", String(editable.points[b].y));
      layer.appendChild(guide);
    }
  }
  editable.points.forEach((point, index) => {
    const handle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    handle.setAttribute("class", "selection-handle path-point-handle");
    handle.setAttribute("data-handle", `path:${index}`);
    handle.setAttribute("data-point-type", point.type || "anchor");
    handle.setAttribute("r", point.type === "control" ? "4.5" : "5.5");
    handle.setAttribute("cx", String(point.x));
    handle.setAttribute("cy", String(point.y));
    if (onHandlePointerDown) handle.addEventListener("pointerdown", onHandlePointerDown);
    layer.appendChild(handle);
  });
}

export function cloneBBox(box) {
  return { x: box.x, y: box.y, width: box.width, height: box.height };
}

export function adjustedBBox(startBox, handle, dx, dy) {
  if (handle === "c") {
    return { x: startBox.x + dx, y: startBox.y + dy, width: startBox.width, height: startBox.height };
  }
  let left = startBox.x;
  let right = startBox.x + startBox.width;
  let top = startBox.y;
  let bottom = startBox.y + startBox.height;
  if (handle.includes("w")) left += dx;
  if (handle.includes("e")) right += dx;
  if (handle.includes("n")) top += dy;
  if (handle.includes("s")) bottom += dy;
  const minSize = 4;
  if (right - left < minSize) {
    if (handle.includes("w")) left = right - minSize;
    else right = left + minSize;
  }
  if (bottom - top < minSize) {
    if (handle.includes("n")) top = bottom - minSize;
    else bottom = top + minSize;
  }
  return { x: left, y: top, width: right - left, height: bottom - top };
}

export function adjustedCanvasBox(startBox, handle, dx, dy) {
  let width = startBox.width;
  let height = startBox.height;
  if (handle.includes("e")) width = startBox.width + dx;
  if (handle.includes("w")) width = startBox.width - dx;
  if (handle.includes("s")) height = startBox.height + dy;
  if (handle.includes("n")) height = startBox.height - dy;
  return {
    x: 0,
    y: 0,
    width: Math.max(20, width),
    height: Math.max(20, height),
  };
}

export function rotatePointAround(point, center, angleRadians) {
  const cos = Math.cos(angleRadians);
  const sin = Math.sin(angleRadians);
  const dx = point.x - center.x;
  const dy = point.y - center.y;
  return {
    x: center.x + dx * cos - dy * sin,
    y: center.y + dx * sin + dy * cos,
  };
}

export function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

export function inflateHitBox(box, pad) {
  if (!box) return null;
  return {
    x: box.x - pad,
    y: box.y - pad,
    width: box.width + pad * 2,
    height: box.height + pad * 2,
  };
}

export function pointToSegmentDistance(point, a, b) {
  const dx = b.x - a.x;
  const dy = b.y - a.y;
  const len2 = dx * dx + dy * dy;
  if (!len2) return Math.hypot(point.x - a.x, point.y - a.y);
  const t = clamp(((point.x - a.x) * dx + (point.y - a.y) * dy) / len2, 0, 1);
  return Math.hypot(point.x - (a.x + dx * t), point.y - (a.y + dy * t));
}

export function pointToBoxDistance(point, box) {
  if (!box) return Infinity;
  const insideX = point.x >= box.x && point.x <= box.x + box.width;
  const insideY = point.y >= box.y && point.y <= box.y + box.height;
  if (insideX && insideY) return 0;
  const cx = clamp(point.x, box.x, box.x + box.width);
  const cy = clamp(point.y, box.y, box.y + box.height);
  return Math.hypot(point.x - cx, point.y - cy);
}
