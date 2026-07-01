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
  capturePointer(svg, ev.pointerId);
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
  releasePointerCapture(state.svg, state.pointerId);
  const end = svgPoint(state.svg, ev.clientX, ev.clientY);
  return {
    x: Math.min(state.startSvg.x, end.x),
    y: Math.min(state.startSvg.y, end.y),
    width: Math.abs(end.x - state.startSvg.x),
    height: Math.abs(end.y - state.startSvg.y),
  };
}

export function capturePointer(el, pointerId) {
  if (!el || pointerId === undefined) return false;
  try {
    el.setPointerCapture(pointerId);
    return true;
  } catch (_) {
    // Synthetic pointer events in tests may not have an active pointer.
    return false;
  }
}

export function releasePointerCapture(el, pointerId) {
  if (!el || pointerId === undefined) return false;
  try {
    if (el.hasPointerCapture(pointerId)) {
      el.releasePointerCapture(pointerId);
      return true;
    }
  } catch (_) {
    // Pointer capture can be absent in synthetic or interrupted pointer flows.
  }
  return false;
}

export function ensureDrawPreview(svg) {
  if (!svg) return null;
  let preview = document.getElementById("drawShapePreview");
  if (preview) return preview;
  preview = document.createElementNS("http://www.w3.org/2000/svg", "path");
  preview.setAttribute("id", "drawShapePreview");
  preview.setAttribute("fill", "none");
  preview.setAttribute("stroke", "#2563eb");
  preview.setAttribute("stroke-width", "2");
  preview.setAttribute("stroke-dasharray", "6 4");
  preview.style.pointerEvents = "none";
  svg.appendChild(preview);
  return preview;
}

export function removeDrawPreview() {
  document.getElementById("drawShapePreview")?.remove();
}

export function formatPathPoint(point) {
  return `${Number(point.x.toFixed(1))} ${Number(point.y.toFixed(1))}`;
}

export function curvePathFromPoints(start, end) {
  const dx = end.x - start.x;
  const dy = end.y - start.y;
  const c1 = { x: start.x + dx * 0.35, y: start.y };
  const c2 = { x: start.x + dx * 0.65, y: end.y };
  if (Math.abs(dx) < 8 && Math.abs(dy) >= 8) {
    c1.x = start.x + Math.max(20, Math.abs(dy) * 0.25);
    c1.y = start.y + dy * 0.25;
    c2.x = end.x - Math.max(20, Math.abs(dy) * 0.25);
    c2.y = start.y + dy * 0.75;
  }
  return `M ${formatPathPoint(start)} C ${formatPathPoint(c1)}, ${formatPathPoint(c2)}, ${formatPathPoint(end)}`;
}

export function freeformPathFromPoints(points) {
  if (!points.length) return "";
  if (points.length === 1) return `M ${formatPathPoint(points[0])}`;
  const out = [`M ${formatPathPoint(points[0])}`];
  for (let i = 1; i < points.length; i += 1) {
    out.push(`L ${formatPathPoint(points[i])}`);
  }
  return out.join(" ");
}

export function drawPathFromState(state) {
  if (!state || !state.def) return "";
  if (state.def.draw_mode === "freeform") return freeformPathFromPoints(state.points || []);
  return curvePathFromPoints(state.start, state.current || state.start);
}

export function createDrawState(svg, def, start, pointerId) {
  return {
    svg,
    def,
    start,
    current: start,
    points: [start],
    pointerId,
  };
}

export function updateDrawStatePoint(state, point) {
  if (!state || !point) return;
  state.current = point;
  if (state.def.draw_mode !== "freeform") return;
  const last = state.points[state.points.length - 1];
  const dx = point.x - last.x;
  const dy = point.y - last.y;
  if (Math.hypot(dx, dy) >= 3) state.points.push(point);
}

export function editablePathFromD(d) {
  const tokens = pathTokens(d);
  if (tokens.length < 4) return null;
  const num = (token) => Number(token);
  if (tokens[0] !== "M") return null;
  const start = { x: num(tokens[1]), y: num(tokens[2]), type: "anchor" };
  if (!Number.isFinite(start.x) || !Number.isFinite(start.y)) return null;
  if (tokens[3] === "C" && tokens.length === 10) {
    const values = tokens.slice(4).map(num);
    if (values.some((v) => !Number.isFinite(v))) return null;
    return {
      kind: "cubic",
      points: [
        start,
        { x: values[0], y: values[1], type: "control" },
        { x: values[2], y: values[3], type: "control" },
        { x: values[4], y: values[5], type: "anchor" },
      ],
      build(points) {
        return `M ${formatPathPoint(points[0])} C ${formatPathPoint(points[1])}, ${formatPathPoint(points[2])}, ${formatPathPoint(points[3])}`;
      },
    };
  }
  const points = [start];
  let i = 3;
  while (i < tokens.length) {
    if (tokens[i] !== "L" || i + 2 >= tokens.length) return null;
    const point = { x: num(tokens[i + 1]), y: num(tokens[i + 2]), type: "anchor" };
    if (!Number.isFinite(point.x) || !Number.isFinite(point.y)) return null;
    points.push(point);
    i += 3;
  }
  if (points.length < 2 || points.length > 80) return null;
  return {
    kind: "polyline",
    points,
    build(nextPoints) {
      return freeformPathFromPoints(nextPoints);
    },
  };
}

export function pathPointPatchFromHandle(startValue, handle, point, snap = (v) => v) {
  const index = Number(String(handle || "").replace("path:", ""));
  if (!Number.isInteger(index)) return null;
  const editable = editablePathFromD(startValue && startValue.d);
  if (!editable || index < 0 || index >= editable.points.length) return null;
  const points = editable.points.map((p) => ({ ...p }));
  points[index] = { ...points[index], x: snap(point.x), y: snap(point.y) };
  return { ...startValue, d: editable.build(points) };
}

export function bindSlotHitProxy(proxy, target, { onPointerDown, onDoubleClick } = {}) {
  if (!proxy || !target) return proxy;
  proxy.__slotProxyTarget = target;
  proxy.style.cursor = "move";
  if (onPointerDown) {
    proxy.addEventListener("pointerdown", (ev) => onPointerDown(target, ev));
  }
  if (onDoubleClick) {
    proxy.addEventListener("dblclick", (ev) => onDoubleClick(target, ev));
  }
  return proxy;
}

export function appendStrokeHitProxy(svg, el, handlers = {}) {
  if (!svg || !el) return false;
  const tag = el.tagName.toLowerCase();
  if (!(tag === "line" || tag === "path" || tag === "polygon")) return false;
  const sourceStrokeWidth = Number(el.getAttribute("stroke-width") || 1);
  if (tag === "line" && sourceStrokeWidth >= 4) {
    el.style.pointerEvents = "stroke";
    return false;
  }
  const proxy = document.createElementNS("http://www.w3.org/2000/svg", tag);
  const copyAttrs = slotHitProxyAttrs(tag);
  for (const name of copyAttrs) {
    const value = el.getAttribute(name);
    if (value !== null) proxy.setAttribute(name, value);
  }
  proxy.setAttribute("fill", "none");
  proxy.setAttribute("stroke", "#000");
  proxy.setAttribute("stroke-opacity", "0.001");
  proxy.setAttribute("stroke-width", String(Math.max(18, sourceStrokeWidth * 6)));
  proxy.setAttribute("stroke-linecap", el.getAttribute("stroke-linecap") || "round");
  proxy.setAttribute("stroke-linejoin", el.getAttribute("stroke-linejoin") || "round");
  proxy.style.pointerEvents = "stroke";
  proxy.classList.add("slot-hit-proxy");
  bindSlotHitProxy(proxy, el, handlers);
  if (!Array.isArray(el.__slotHitProxies)) el.__slotHitProxies = [];
  el.__slotHitProxies.push(proxy);
  svg.appendChild(proxy);
  return true;
}

export function appendTextHitProxy(svg, el, box, handlers = {}) {
  if (!svg || !el || !box) return null;
  const proxy = document.createElementNS("http://www.w3.org/2000/svg", "rect");
  proxy.setAttribute("x", String(box.x));
  proxy.setAttribute("y", String(box.y));
  proxy.setAttribute("width", String(box.width));
  proxy.setAttribute("height", String(box.height));
  proxy.setAttribute("fill", "transparent");
  proxy.setAttribute("stroke", "none");
  proxy.style.pointerEvents = "all";
  proxy.classList.add("text-hit-proxy");
  bindSlotHitProxy(proxy, el, handlers);
  svg.appendChild(proxy);
  return proxy;
}

export function syncSlotHitProxies(el) {
  const proxies = el && el.__slotHitProxies;
  if (!Array.isArray(proxies)) return;
  const tag = el.tagName.toLowerCase();
  const copyAttrs = slotHitProxyAttrs(tag);
  for (const proxy of proxies) {
    for (const name of copyAttrs) {
      const value = el.getAttribute(name);
      if (value !== null) proxy.setAttribute(name, value);
      else proxy.removeAttribute(name);
    }
  }
}

export function bindCanvasSlotInteractionEvents(svg, container, handlers = {}) {
  if (!svg) return;
  if (handlers.onPointerDownCapture) {
    svg.addEventListener("pointerdown", handlers.onPointerDownCapture, true);
  }
  if (handlers.onContextMenu) {
    svg.addEventListener("contextmenu", handlers.onContextMenu);
  }
  if (handlers.onDoubleClick) {
    svg.addEventListener("dblclick", handlers.onDoubleClick);
  }
  if (handlers.onPointerDown) {
    svg.addEventListener("pointerdown", handlers.onPointerDown);
  }
  if (container && handlers.onContainerPointerDown && container.dataset.blankClickBound !== "1") {
    container.dataset.blankClickBound = "1";
    container.addEventListener("pointerdown", handlers.onContainerPointerDown);
  }
  if (handlers.onPointerMove) {
    svg.addEventListener("pointermove", handlers.onPointerMove);
  }
  if (handlers.onPointerUp) {
    svg.addEventListener("pointerup", handlers.onPointerUp);
  }
}

export function createSlotDragSnapshot(selectedSlots, { slotIdFromElement, readSlotPatchValue, elementAnchor } = {}) {
  const beforeMap = new Map();
  const fractionStartAnchors = new Map();
  if (!selectedSlots || typeof selectedSlots.values !== "function") {
    return { beforeMap, fractionStartAnchors };
  }

  for (const item of selectedSlots.values()) {
    if (item.isFraction) {
      beforeMap.set(item.slotId, { move_dx: 0, move_dy: 0 });
      const elems = item.elements || [];
      if (elementAnchor && elems.length) {
        const anchor = elementAnchor(elems[0]);
        if (anchor) fractionStartAnchors.set(item.slotId, anchor);
      }
      continue;
    }

    if (item.isCharacterGroup || item.isLayoutGroup || item.isGeneratedGroup || item.isFigureGroup || item.isPaperFoldGroup || item.isMeasurementGroup || item.isTableGroup || item.isGraphPaperGroup) {
      for (const node of item.elements || []) {
        const sid = slotIdFromElement ? slotIdFromElement(node) : null;
        const value = readSlotPatchValue ? readSlotPatchValue(node) : null;
        if (sid && value) beforeMap.set(sid, clonePatchValue(value));
      }
      continue;
    }

    const value = readSlotPatchValue ? readSlotPatchValue(item.el) : null;
    if (!value) continue;
    for (const id of item.slotIds || [item.slotId]) {
      beforeMap.set(id, clonePatchValue(value));
    }
  }

  return { beforeMap, fractionStartAnchors };
}

export function scheduleDragFrame(dragState, point, frameRequested, onFrame) {
  if (!dragState || !point) return frameRequested;
  const dx = point.x - dragState.start.x;
  const dy = point.y - dragState.start.y;
  dragState.start = point;
  dragState.totalDx += dx;
  dragState.totalDy += dy;
  dragState.pendingDx = (dragState.pendingDx || 0) + dx;
  dragState.pendingDy = (dragState.pendingDy || 0) + dy;
  if (frameRequested) return true;
  requestAnimationFrame(() => {
    const pending = consumePendingDragDelta(dragState);
    if (onFrame) onFrame(pending);
  });
  return true;
}

export function consumePendingDragDelta(dragState) {
  if (!dragState) return { dx: 0, dy: 0 };
  const dx = dragState.pendingDx || 0;
  const dy = dragState.pendingDy || 0;
  dragState.pendingDx = 0;
  dragState.pendingDy = 0;
  return { dx, dy };
}

function clonePatchValue(value) {
  return JSON.parse(JSON.stringify(value));
}

function pathTokens(d) {
  return (d || "").match(/[a-zA-Z]|-?\d*\.?\d+(?:e[-+]?\d+)?/g) || [];
}

function slotHitProxyAttrs(tag) {
  if (tag === "line") return ["x1", "y1", "x2", "y2", "transform"];
  if (tag === "path") return ["d", "transform"];
  if (tag === "polygon") return ["points", "transform"];
  return [];
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

export function pointInRotatedFrame(point, rotation) {
  if (!rotation || !rotation.angle || rotation.cx === null || rotation.cy === null) return point;
  const radians = (-rotation.angle * Math.PI) / 180;
  return rotatePointAround(point, { x: rotation.cx, y: rotation.cy }, radians);
}

export function linePatchFromEndpoint(el, handle, startValue, point, snap = (v) => v) {
  const value = {
    x1: startValue.x1,
    y1: startValue.y1,
    x2: startValue.x2,
    y2: startValue.y2,
  };
  if (handle === "p1") {
    value.x1 = snap(point.x);
    value.y1 = snap(point.y);
  } else {
    value.x2 = snap(point.x);
    value.y2 = snap(point.y);
  }
  el.setAttribute("x1", String(value.x1));
  el.setAttribute("y1", String(value.y1));
  el.setAttribute("x2", String(value.x2));
  el.setAttribute("y2", String(value.y2));
  return value;
}

export function linePatchFromRotation(el, startValue, startPoint, pointerPoint, { snap = (v) => v, snapAngle = false } = {}) {
  const center = {
    x: (startValue.x1 + startValue.x2) / 2,
    y: (startValue.y1 + startValue.y2) / 2,
  };
  const a0 = Math.atan2(startPoint.y - center.y, startPoint.x - center.x);
  const a1 = Math.atan2(pointerPoint.y - center.y, pointerPoint.x - center.x);
  let delta = a1 - a0;
  if (snapAngle) delta = (Math.round((delta * 180 / Math.PI) / 5) * 5) * Math.PI / 180;
  const p1 = rotatePointAround({ x: startValue.x1, y: startValue.y1 }, center, delta);
  const p2 = rotatePointAround({ x: startValue.x2, y: startValue.y2 }, center, delta);
  const value = { x1: snap(p1.x), y1: snap(p1.y), x2: snap(p2.x), y2: snap(p2.y) };
  el.setAttribute("x1", String(value.x1));
  el.setAttribute("y1", String(value.y1));
  el.setAttribute("x2", String(value.x2));
  el.setAttribute("y2", String(value.y2));
  return value;
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
