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

export function renderCanvas(host, semantic, selectedIds = [], drag = null) {
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

export function eventToSvgPoint(svg, event) {
  const point = svg.createSVGPoint();
  point.x = event.clientX;
  point.y = event.clientY;
  return point.matrixTransform(svg.getScreenCTM().inverse());
}
