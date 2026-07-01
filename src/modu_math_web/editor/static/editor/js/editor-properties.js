export function initProperties({ root, onCommand, getState } = {}) {
  return {
    root,
    onCommand,
    getState,
  };
}

export function bindCommitInputs(ids, commit) {
  for (const id of ids) {
    const input = document.getElementById(id);
    if (!input) continue;
    input.addEventListener("change", commit);
    input.addEventListener("keydown", (event) => {
      if (event.key !== "Enter") return;
      event.preventDefault();
      commit();
    });
  }
}
