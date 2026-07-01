const initialState = Object.freeze({
  problemId: null,
  dsl: "",
  selectedIds: [],
  hoveredId: null,
  zoom: 1,
  pan: { x: 0, y: 0 },
  activeTool: "select",
  pendingPatches: [],
  dirty: false,
  buildStatus: "idle",
  saveStatus: "idle",
  loading: false,
  saving: false,
  building: false,
  error: null,
  artifacts: null,
  openMenu: null,
  inlineEditor: null,
});

let state = cloneState(initialState);
const listeners = new Set();

function cloneState(value) {
  return {
    ...value,
    pan: { ...(value.pan || { x: 0, y: 0 }) },
    selectedIds: [...(value.selectedIds || [])],
    pendingPatches: [...(value.pendingPatches || [])],
  };
}

function notify(previous) {
  const snapshot = getState();
  for (const listener of listeners) {
    listener(snapshot, previous);
  }
}

export function getState() {
  return cloneState(state);
}

export function setState(partialState) {
  const previous = getState();
  const patch = { ...(partialState || {}) };
  if (patch.pan) patch.pan = { ...state.pan, ...patch.pan };
  if (patch.selectedIds) patch.selectedIds = [...patch.selectedIds];
  if (patch.pendingPatches) patch.pendingPatches = [...patch.pendingPatches];
  state = cloneState({ ...state, ...patch });
  notify(previous);
  return getState();
}

export function subscribe(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

export function resetState() {
  const previous = getState();
  state = cloneState(initialState);
  notify(previous);
  return getState();
}
