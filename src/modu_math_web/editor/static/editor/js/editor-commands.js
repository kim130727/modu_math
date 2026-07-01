let undoStack = [];
let redoStack = [];
const listeners = new Set();

function notify() {
  const snapshot = { canUndo: canUndo(), canRedo: canRedo() };
  for (const listener of listeners) listener(snapshot);
}

export function executeCommand(command, state) {
  if (!command || typeof command !== "object") {
    throw new Error("command must be an object");
  }
  if (typeof command.applyLocal === "function") {
    command.applyLocal(state);
  }
  undoStack.push(command);
  redoStack = [];
  notify();
  return command;
}

export function undo(state) {
  const command = undoStack.pop();
  if (!command) return null;
  if (typeof command.revertLocal === "function") {
    command.revertLocal(state);
  }
  redoStack.push(command);
  notify();
  return command;
}

export function redo(state) {
  const command = redoStack.pop();
  if (!command) return null;
  if (typeof command.applyLocal === "function") {
    command.applyLocal(state);
  }
  undoStack.push(command);
  notify();
  return command;
}

export function canUndo() {
  return undoStack.length > 0;
}

export function canRedo() {
  return redoStack.length > 0;
}

export function clearHistory() {
  undoStack = [];
  redoStack = [];
  notify();
}

export function subscribeHistory(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

export function createLayoutPatchCommand({ description, patches, applyLocal, revertLocal }) {
  return {
    type: "layout.patch",
    description: description || "레이아웃 변경",
    patches: [...(patches || [])],
    applyLocal,
    revertLocal,
  };
}
