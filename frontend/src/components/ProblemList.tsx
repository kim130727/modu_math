import { createMemo, createSignal, For, Show } from "solid-js";
import type { EditorStore } from "../stores/editorStore";
import type { ProblemSummary } from "../types/api";

interface ProblemListProps {
  store: EditorStore;
}

type ProblemTreeNodeData = {
  name: string;
  path: string;
  children: ProblemTreeNodeData[];
  problem: ProblemSummary | null;
};

export function ProblemList(props: ProblemListProps) {
  const [filter, setFilter] = createSignal("");
  const [collapsedFolders, setCollapsedFolders] = createSignal<Set<string>>(new Set());
  const visibleProblems = createMemo(() => {
    const q = filter().trim().toLocaleLowerCase("ko");
    if (!q) return props.store.state.problems;
    return props.store.state.problems.filter((problem) => problem.problem_id.toLocaleLowerCase("ko").includes(q));
  });
  const tree = createMemo(() => buildProblemTree(visibleProblems()));
  const filterActive = () => filter().trim().length > 0;

  function toggleFolder(path: string): void {
    setCollapsedFolders((current) => {
      const next = new Set(current);
      if (next.has(path)) next.delete(path);
      else next.add(path);
      return next;
    });
  }

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
      <div class="tree problem-tree" role="tree" aria-label="Problems">
        <For each={tree().children}>
          {(node) => (
            <ProblemTreeNode
              node={node}
              collapsedFolders={collapsedFolders()}
              forceOpen={filterActive()}
              activeProblemId={props.store.state.problemId}
              onToggleFolder={toggleFolder}
              onOpenProblem={(problemId) => void props.store.openProblem(problemId)}
            />
          )}
        </For>
      </div>
    </aside>
  );
}

function buildProblemTree(problems: ProblemSummary[]): ProblemTreeNodeData {
  const root: ProblemTreeNodeData = { name: "", path: "", children: [], problem: null };
  for (const problem of problems) {
    const parts = problem.problem_id.split("/").filter(Boolean);
    let current = root;
    parts.forEach((part, index) => {
      const path = parts.slice(0, index + 1).join("/");
      let child = current.children.find((candidate) => candidate.name === part);
      if (!child) {
        child = { name: part, path, children: [], problem: null };
        current.children.push(child);
      }
      if (index === parts.length - 1) child.problem = problem;
      current = child;
    });
  }
  sortTree(root);
  return root;
}

function sortTree(node: ProblemTreeNodeData): void {
  node.children.sort((left, right) => {
    if (left.problem && !right.problem) return 1;
    if (!left.problem && right.problem) return -1;
    return left.name.localeCompare(right.name, "ko");
  });
  node.children.forEach(sortTree);
}

function ProblemTreeNode(props: {
  node: ProblemTreeNodeData;
  collapsedFolders: Set<string>;
  forceOpen: boolean;
  activeProblemId: string | null;
  onToggleFolder: (path: string) => void;
  onOpenProblem: (problemId: string) => void;
}) {
  const isFolder = () => props.node.children.length > 0 && !props.node.problem;
  const isCollapsed = () => !props.forceOpen && props.collapsedFolders.has(props.node.path);

  return (
    <Show
      when={isFolder()}
      fallback={
        <button
          type="button"
          class="file-btn"
          classList={{ active: props.activeProblemId === props.node.problem?.problem_id }}
          role="treeitem"
          onClick={() => props.node.problem && props.onOpenProblem(props.node.problem.problem_id)}
        >
          <span>{props.node.name}</span>
          <small>
            <Show when={props.node.problem?.has_svg} fallback="no svg">svg</Show>
            {" | "}
            <Show when={props.node.problem?.has_layout} fallback="no layout">layout</Show>
          </small>
        </button>
      }
    >
      <div class="tree-node" role="treeitem" aria-expanded={!isCollapsed()}>
        <button
          type="button"
          class="folder"
          classList={{ open: !isCollapsed() }}
          onClick={() => props.onToggleFolder(props.node.path)}
        >
          {props.node.name}
        </button>
        <div class="children" classList={{ collapsed: isCollapsed() }} role="group">
          <For each={props.node.children}>
            {(child) => (
              <ProblemTreeNode
                node={child}
                collapsedFolders={props.collapsedFolders}
                forceOpen={props.forceOpen}
                activeProblemId={props.activeProblemId}
                onToggleFolder={props.onToggleFolder}
                onOpenProblem={props.onOpenProblem}
              />
            )}
          </For>
        </div>
      </div>
    </Show>
  );
}
