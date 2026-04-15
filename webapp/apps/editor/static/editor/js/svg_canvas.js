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

function drawElement(el, selectedId) {
  const selected = el.id === selectedId;
  const stroke = selected ? "#0f766e" : (el.stroke ?? "#222");
  const strokeWidth = selected ? Math.max(2, num(el.stroke_width, 1) + 1) : num(el.stroke_width, 1);
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
  if (el.type === "text") {
    return `<text data-element-id="${esc(el.id)}" x="${num(el.x)}" y="${num(el.y)}" fill="${esc(el.fill ?? "#111")}" font-size="${num(el.font_size, 24)}">${esc(el.text ?? "")}</text>`;
  }
  if (el.type === "formula") {
    return `<text data-element-id="${esc(el.id)}" x="${num(el.x)}" y="${num(el.y)}" fill="${esc(el.fill ?? "#111")}" font-size="${num(el.font_size, 24)}" class="formula">${esc(el.expr ?? "")}</text>`;
  }
  return "";
}

export function renderCanvas(host, semantic, selectedId) {
  const render = semantic.render ?? {};
  const canvas = render.canvas ?? {};
  const width = num(canvas.width, 1200);
  const height = num(canvas.height, 700);
  const bg = canvas.background ?? "#f6f6f6";
  const elements = Array.isArray(render.elements) ? render.elements : [];

  const svg = [
    `<svg id="editor-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width} ${height}">`,
    `<rect x="0" y="0" width="${width}" height="${height}" fill="${esc(bg)}" />`,
    ...elements.map((el) => drawElement(el, selectedId)),
    "</svg>",
  ].join("");
  host.innerHTML = svg;
}

export function eventToSvgPoint(svg, event) {
  const point = svg.createSVGPoint();
  point.x = event.clientX;
  point.y = event.clientY;
  return point.matrixTransform(svg.getScreenCTM().inverse());
}

