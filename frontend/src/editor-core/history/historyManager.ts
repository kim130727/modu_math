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

