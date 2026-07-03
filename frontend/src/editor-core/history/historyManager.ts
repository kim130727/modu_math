export interface HistorySnapshot<T> {
  label: string;
  before: T;
  after: T;
}

export interface HistoryState<T> {
  undoStack: HistorySnapshot<T>[];
  redoStack: HistorySnapshot<T>[];
}

export function emptyHistory<T>(): HistoryState<T> {
  return { undoStack: [], redoStack: [] };
}

export function pushHistoryEntry<T>(history: HistoryState<T>, entry: HistorySnapshot<T>, limit = 100): HistoryState<T> {
  const undoStack = [...history.undoStack, entry].slice(-limit);
  return { undoStack, redoStack: [] };
}

export function popUndoEntry<T>(history: HistoryState<T>): { entry: HistorySnapshot<T> | null; history: HistoryState<T> } {
  const entry = history.undoStack.at(-1) ?? null;
  if (!entry) return { entry: null, history };
  return {
    entry,
    history: {
      undoStack: history.undoStack.slice(0, -1),
      redoStack: [...history.redoStack, entry],
    },
  };
}

export function popRedoEntry<T>(history: HistoryState<T>): { entry: HistorySnapshot<T> | null; history: HistoryState<T> } {
  const entry = history.redoStack.at(-1) ?? null;
  if (!entry) return { entry: null, history };
  return {
    entry,
    history: {
      undoStack: [...history.undoStack, entry],
      redoStack: history.redoStack.slice(0, -1),
    },
  };
}
