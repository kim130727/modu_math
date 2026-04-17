function esc(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function num(value, fallback = 0) {
  const n = Number(value);
  return Number.isFinite(n) ? n : fallback;
}

function drawElement(el, selectedIds = []) {
  const selected = selectedIds.includes(el.id);
  const stroke = selected ? "#0f766e" : (el.stroke ?? "#222");
  const strokeWidth = selected ? Math.max(4, num(el.stroke_width, 1) + 2) : num(el.stroke_width, 1);
  const fill = el.fill ?? "none";
  const shared = `data-element-id="${esc(el.id)}" stroke="${esc(stroke)}" stroke-width="${strokeWidth}" fill="${esc(fill)}"`;

  if (el.type === "line") {
    return `<line ${shared} x1="${num(el.x1)}" y1="${num(el.y1)}" x2="${num(el.x2)}" y2="${num(el.y2)}" />`;
  }
  if (el.type === "rect") {
    return `<rect ${shared} x="${num(el.x)}" y="${num(el.y)}" width="${num(el.width, 120)}" height="${num(el.height, 80)}" />`;
  }
  if (el.type === "circle") {
    return `<circle ${shared} cx="${num(el.x)}" cy="${num(el.y)}" r="${num(el.r, 35)}" />`;
  }
  if (el.type === "polygon") {
    const pts = Array.isArray(el.points)
      ? el.points.map((p) => `${num(p[0])},${num(p[1])}`).join(" ")
      : "";
    return `<polygon ${shared} points="${esc(pts)}" />`;
  }
  if (el.type === "text") {
    const textFill = selected ? "#0f766e" : (el.fill ?? "#111");
    const textStroke = selected ? ' stroke="#0f766e" stroke-width="1.2" font-weight="700"' : "";
    return `<text data-element-id="${esc(el.id)}" x="${num(el.x)}" y="${num(el.y)}" fill="${esc(textFill)}" font-size="${num(el.font_size, 24)}"${textStroke}>${esc(el.text ?? "")}</text>`;
  }
  if (el.type === "formula") {
    const textFill = selected ? "#0f766e" : (el.fill ?? "#111");
    const textStroke = selected ? ' stroke="#0f766e" stroke-width="1.2" font-weight="700"' : "";
    return `<text data-element-id="${esc(el.id)}" x="${num(el.x)}" y="${num(el.y)}" fill="${esc(textFill)}" font-size="${num(el.font_size, 24)}" class="formula"${textStroke}>${esc(el.expr ?? "")}</text>`;
  }
  return "";
}

export function renderCanvas(host, semantic, selectedIds = [], drag = null, selectionBounds = null) {
  const render = semantic.render ?? {};
  const canvas = render.canvas ?? {};
  const width = num(canvas.width, 1200);
  const height = num(canvas.height, 700);
  const bg = canvas.background ?? "#f6f6f6";
  const elements = Array.isArray(render.elements) ? render.elements : [];

  const svg = [
    `<svg id="editor-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width} ${height}">`,
    `<rect id="canvas-background" x="0" y="0" width="${width}" height="${height}" fill="${esc(bg)}" />`,
    ...elements.map((el) => drawElement(el, selectedIds)),
    _drawResizeHandles(elements, selectedIds, selectionBounds),
    _drawRotateHandle(elements, selectedIds),
    _drawMarquee(drag),
    "</svg>",
  ].join("");
  host.innerHTML = svg;
}

function _drawMarquee(drag) {
  if (!drag || drag.type !== "selection") return "";
  const x = Math.min(drag.startX, drag.currentX);
  const y = Math.min(drag.startY, drag.currentY);
  const w = Math.abs(drag.startX - drag.currentX);
  const h = Math.abs(drag.startY - drag.currentY);
  return `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="rgba(15, 118, 110, 0.1)" stroke="#0f766e" stroke-width="1" stroke-dasharray="4" pointer-events="none" />`;
}

function _drawRotateHandle(elements, selectedIds) {
  if (selectedIds.length !== 1) return "";
  const selectedId = selectedIds[0];
  const el = elements.find((e) => e.id === selectedId);
  if (!el || el.type !== "polygon" || !Array.isArray(el.points) || el.points.length === 0) return "";

  // 다각형의 무게중심 계산
  let cx = 0, cy = 0;
  el.points.forEach((p) => { cx += p[0]; cy += p[1]; });
  cx /= el.points.length;
  cy /= el.points.length;

  // 무게중심에서 위쪽으로 핸들 생성
  const handleY = cy - 80; // 핸들 높이
  return `
    <g class="rotate-handle-group">
      <line x1="${cx}" y1="${cy}" x2="${cx}" y2="${handleY}" stroke="#0f766e" stroke-width="1" stroke-dasharray="4" />
      <circle data-rotate-handle="${el.id}" cx="${cx}" cy="${handleY}" r="8" fill="#0f766e" stroke="#fff" stroke-width="2" style="cursor: alias;" />
    </g>
  `;
}

function _elementPoints(el) {
  if (!el || typeof el !== "object") return [];
  if (el.type === "line") {
    return [
      [num(el.x1), num(el.y1)],
      [num(el.x2), num(el.y2)],
    ];
  }
  if (el.type === "rect") {
    const x = num(el.x);
    const y = num(el.y);
    const w = num(el.width, 120);
    const h = num(el.height, 80);
    return [
      [x, y],
      [x + w, y + h],
    ];
  }
  if (el.type === "circle") {
    const cx = num(el.x);
    const cy = num(el.y);
    const r = num(el.r, 35);
    return [
      [cx - r, cy - r],
      [cx + r, cy + r],
    ];
  }
  if (el.type === "polygon") {
    return Array.isArray(el.points) ? el.points.map((p) => [num(p[0]), num(p[1])]) : [];
  }
  if (el.type === "text" || el.type === "formula") {
    return [[num(el.x), num(el.y)]];
  }
  const x = num(el.x);
  const y = num(el.y);
  const w = num(el.width, 0);
  const h = num(el.height, 0);
  return [
    [x, y],
    [x + w, y + h],
  ];
}

function _selectionBounds(elements, selectedIds) {
  if (!Array.isArray(selectedIds) || selectedIds.length === 0) return null;
  let minX = Infinity;
  let minY = Infinity;
  let maxX = -Infinity;
  let maxY = -Infinity;
  let hasPoint = false;

  for (const id of selectedIds) {
    const el = elements.find((item) => item.id === id);
    if (!el) continue;
    for (const [x, y] of _elementPoints(el)) {
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

function _drawResizeHandles(elements, selectedIds, selectionBounds = null) {
  if (!Array.isArray(selectedIds) || selectedIds.length === 0) return "";
  const bounds = selectionBounds ?? _selectionBounds(elements, selectedIds);
  if (!bounds) return "";

  const { minX, minY, maxX, maxY } = bounds;
  const w = maxX - minX;
  const h = maxY - minY;
  const handleRadius = Math.max(5, Math.min(8, Math.min(w, h) * 0.03));
  const handles = [
    { key: "nw", x: minX, y: minY, cursor: "nwse-resize" },
    { key: "ne", x: maxX, y: minY, cursor: "nesw-resize" },
    { key: "sw", x: minX, y: maxY, cursor: "nesw-resize" },
    { key: "se", x: maxX, y: maxY, cursor: "nwse-resize" },
  ];

  return `
    <g class="resize-handle-group">
      <rect x="${minX}" y="${minY}" width="${w}" height="${h}" fill="none" stroke="#0f766e" stroke-width="1.2" stroke-dasharray="6 4" pointer-events="none" />
      ${handles.map((hnd) => `<circle data-resize-handle="${hnd.key}" cx="${hnd.x}" cy="${hnd.y}" r="${handleRadius}" fill="#0f766e" stroke="#fff" stroke-width="2" style="cursor: ${hnd.cursor};" />`).join("")}
    </g>
  `;
}

export function eventToSvgPoint(svg, event) {
  const point = svg.createSVGPoint();
  point.x = event.clientX;
  point.y = event.clientY;
  return point.matrixTransform(svg.getScreenCTM().inverse());
}
