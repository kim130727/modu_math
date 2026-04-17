const FIELD_NAMES = ["id", "type", "x", "y", "x1", "y1", "x2", "y2", "width", "height", "r", "text", "expr", "font_size"];

export function fillPropertiesForm(form, element) {
  for (const name of FIELD_NAMES) {
    const input = form.elements.namedItem(name);
    if (!input) continue;
    input.value = element?.[name] ?? "";
  }

  // Show effective font size for text/formula even when raw value is omitted.
  const fontInput = form.elements.namedItem("font_size");
  if (fontInput && element && (element.type === "text" || element.type === "formula")) {
    if (fontInput.value === "") {
      fontInput.value = "24";
    }
  }
}

function maybeNumber(value) {
  if (value === "") return undefined;
  const n = Number(value);
  return Number.isFinite(n) ? n : value;
}

export function applyPropertiesForm(form, element) {
  if (!element) return element;
  for (const name of FIELD_NAMES) {
    const input = form.elements.namedItem(name);
    if (!input) continue;
    const raw = input.value.trim();
    if (raw === "") {
      continue;
    }
    element[name] = maybeNumber(raw);
  }
  return element;
}
