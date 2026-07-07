type Axis = "x" | "y" | "other";

const COMMAND_AXES: Record<string, Axis[]> = {
  M: ["x", "y"],
  L: ["x", "y"],
  T: ["x", "y"],
  H: ["x"],
  V: ["y"],
  Q: ["x", "y", "x", "y"],
  S: ["x", "y", "x", "y"],
  C: ["x", "y", "x", "y", "x", "y"],
  A: ["other", "other", "other", "other", "other", "x", "y"],
};

export interface LocalizedPathData {
  d: string;
  x: number;
  y: number;
  width: number;
  height: number;
}

export function localizePathData(d: string): LocalizedPathData {
  const points = collectAbsolutePoints(d);
  if (!points.length) {
    return { d, x: 0, y: 0, width: 1, height: 1 };
  }

  const xs = points.map((point) => point.x);
  const ys = points.map((point) => point.y);
  const x = Math.min(...xs);
  const y = Math.min(...ys);
  const width = Math.max(1, Math.max(...xs) - x);
  const height = Math.max(1, Math.max(...ys) - y);

  return {
    d: transformPathData(d, (value, axis, command) => {
      if (isRelativeCommand(command)) return value;
      if (axis === "x") return value - x;
      if (axis === "y") return value - y;
      return value;
    }),
    x,
    y,
    width,
    height,
  };
}

export function offsetPathData(d: string, dx: number, dy: number): string {
  return transformPathData(d, (value, axis, command) => {
    if (isRelativeCommand(command)) return value;
    if (axis === "x") return value + dx;
    if (axis === "y") return value + dy;
    return value;
  });
}

export function scalePathData(d: string, scaleX: number, scaleY: number): string {
  return transformPathData(d, (value, axis) => {
    if (axis === "x") return value * scaleX;
    if (axis === "y") return value * scaleY;
    return value;
  });
}

function collectAbsolutePoints(d: string): Array<{ x: number; y: number }> {
  const points: Array<{ x: number; y: number }> = [];
  let currentX = 0;
  let currentY = 0;

  visitPathNumbers(d, (value, axis, command) => {
    if (isRelativeCommand(command)) return;
    if (axis === "x") currentX = value;
    if (axis === "y") {
      currentY = value;
      points.push({ x: currentX, y: currentY });
    }
  });

  return points;
}

function transformPathData(d: string, transform: (value: number, axis: Axis, command: string) => number): string {
  const tokens = tokenizePathData(d);
  let command = "";
  let axisIndex = 0;
  const output: string[] = [];

  for (const token of tokens) {
    if (isCommandToken(token)) {
      command = token;
      axisIndex = 0;
      output.push(token);
      continue;
    }

    const value = Number(token);
    if (!Number.isFinite(value)) {
      output.push(token);
      continue;
    }

    const axes = COMMAND_AXES[command.toUpperCase()] ?? [];
    const axis = axes.length ? axes[axisIndex % axes.length] : "other";
    output.push(formatNumber(transform(value, axis, command)));
    axisIndex += 1;
  }

  return output.join(" ");
}

function visitPathNumbers(d: string, visitor: (value: number, axis: Axis, command: string) => void): void {
  const tokens = tokenizePathData(d);
  let command = "";
  let axisIndex = 0;

  for (const token of tokens) {
    if (isCommandToken(token)) {
      command = token;
      axisIndex = 0;
      continue;
    }

    const value = Number(token);
    if (!Number.isFinite(value)) continue;
    const axes = COMMAND_AXES[command.toUpperCase()] ?? [];
    visitor(value, axes.length ? axes[axisIndex % axes.length] : "other", command);
    axisIndex += 1;
  }
}

function tokenizePathData(d: string): string[] {
  return d.match(/[a-zA-Z]|[-+]?(?:\d*\.\d+|\d+)(?:e[-+]?\d+)?/gi) ?? [];
}

function isCommandToken(token: string): boolean {
  return /^[a-zA-Z]$/.test(token);
}

function isRelativeCommand(command: string): boolean {
  return command === command.toLowerCase();
}

function formatNumber(value: number): string {
  return String(Math.round(value * 1000) / 1000);
}
