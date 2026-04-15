const FIELD_NAMES = ["id", "type", "x", "y", "x1", "y1", "x2", "y2", "width", "height", "r", "text", "expr"];

export function fillPropertiesForm(form, element) {
  for (const name of FIELD_NAMES) {
    const input = form.elements.namedItem(name);
    if (!input) continue;
    input.value = element?.[name] ?? "";
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

