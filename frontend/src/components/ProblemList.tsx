import { createMemo, createSignal, For, Show } from "solid-js";
import type { EditorStore } from "../stores/editorStore";

interface ProblemListProps {
  store: EditorStore;
}

export function ProblemList(props: ProblemListProps) {
  const [filter, setFilter] = createSignal("");
  const visibleProblems = createMemo(() => {
    const q = filter().trim().toLocaleLowerCase("ko");
    if (!q) return props.store.state.problems;
    return props.store.state.problems.filter((problem) => problem.problem_id.toLocaleLowerCase("ko").includes(q));
  });

  return (
    <aside class="editor-next-problems">
      <div class="pane-heading">Problems</div>
      <input
        class="problem-filter"
        value={filter()}
        onInput={(event) => setFilter(event.currentTarget.value)}
        placeholder="Filter by path"
      />
      <div class="problem-count">{visibleProblems().length} / {props.store.state.problems.length}</div>
      <div class="problem-list" role="listbox" aria-label="Problems">
        <For each={visibleProblems()}>
          {(problem) => (
            <button
              type="button"
              classList={{ active: props.store.state.problemId === problem.problem_id }}
              onClick={() => void props.store.openProblem(problem.problem_id)}
            >
              <span>{problem.problem_id}</span>
              <small>
                <Show when={problem.has_svg} fallback="no svg">svg</Show>
                {" · "}
                <Show when={problem.has_layout} fallback="no layout">layout</Show>
              </small>
            </button>
          )}
        </For>
      </div>
    </aside>
  );
}

