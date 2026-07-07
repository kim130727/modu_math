import { useEffect, useMemo, useState } from "react";
import { listProblems, type ProblemSummary } from "../api/editorApi";

interface ProblemListProps {
  selectedProblemId: string;
  onOpenProblem: (problemId: string) => void;
}

interface ProblemTreeNode {
  name: string;
  path: string;
  folders: Map<string, ProblemTreeNode>;
  problems: ProblemSummary[];
}

export function ProblemList({ selectedProblemId, onOpenProblem }: ProblemListProps) {
  const [problems, setProblems] = useState<ProblemSummary[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [query, setQuery] = useState("");
  const [collapsed, setCollapsed] = useState<Set<string>>(new Set());

  useEffect(() => {
    let canceled = false;
    setLoading(true);
    listProblems()
      .then((response) => {
        if (canceled) return;
        setProblems(response.problems);
        setError(null);
      })
      .catch((err: unknown) => {
        if (canceled) return;
        setError(String(err));
      })
      .finally(() => {
        if (!canceled) setLoading(false);
      });
    return () => {
      canceled = true;
    };
  }, []);

  const filteredProblems = useMemo(() => {
    const normalizedQuery = normalizeSearch(query);
    if (!normalizedQuery) return problems;
    return problems.filter((problem) => problemMatches(problem, normalizedQuery));
  }, [problems, query]);

  const tree = useMemo(() => buildProblemTree(filteredProblems), [filteredProblems]);
  const searching = query.trim().length > 0;

  const toggleFolder = (path: string) => {
    setCollapsed((current) => {
      const next = new Set(current);
      if (next.has(path)) next.delete(path);
      else next.add(path);
      return next;
    });
  };

  return (
    <aside className="problem-list-panel">
      <div className="panel-title">문제 탐색</div>
      <div className="problem-search-wrap">
        <input
          className="problem-search-input"
          type="search"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="파일명 또는 폴더 검색"
          aria-label="파일명 또는 폴더 검색"
        />
        <div className="problem-count">
          {filteredProblems.length} / {problems.length}개
        </div>
      </div>
      {loading ? <div className="problem-list-status">Loading...</div> : null}
      {error ? <div className="problem-list-error">{error}</div> : null}
      <div className="problem-scroll tree-scroll" aria-label="Problem tree">
        {filteredProblems.length ? (
          <ProblemTree
            node={tree}
            selectedProblemId={selectedProblemId}
            collapsed={collapsed}
            searching={searching}
            onToggleFolder={toggleFolder}
            onOpenProblem={onOpenProblem}
          />
        ) : (
          <div className="problem-empty">검색 결과가 없습니다.</div>
        )}
      </div>
    </aside>
  );
}

function ProblemTree({
  node,
  selectedProblemId,
  collapsed,
  searching,
  onToggleFolder,
  onOpenProblem,
}: {
  node: ProblemTreeNode;
  selectedProblemId: string;
  collapsed: Set<string>;
  searching: boolean;
  onToggleFolder: (path: string) => void;
  onOpenProblem: (problemId: string) => void;
}) {
  const folders = Array.from(node.folders.values()).sort((a, b) => a.name.localeCompare(b.name, "ko"));
  const files = [...node.problems].sort((a, b) => problemFileName(a).localeCompare(problemFileName(b), "ko"));

  return (
    <ul className="problem-tree-list">
      {folders.map((folder) => {
        const isCollapsed = !searching && collapsed.has(folder.path);
        return (
          <li className="problem-tree-item" key={folder.path}>
            <button type="button" className="problem-folder-row" onClick={() => onToggleFolder(folder.path)}>
              <span className="problem-chevron">{isCollapsed ? "▸" : "▾"}</span>
              <span className="problem-folder-name">{folder.name}</span>
            </button>
            {isCollapsed ? null : (
              <ProblemTree
                node={folder}
                selectedProblemId={selectedProblemId}
                collapsed={collapsed}
                searching={searching}
                onToggleFolder={onToggleFolder}
                onOpenProblem={onOpenProblem}
              />
            )}
          </li>
        );
      })}
      {files.map((problem) => (
        <li className="problem-tree-item" key={problem.problem_id}>
          <button
            type="button"
            className={problem.problem_id === selectedProblemId ? "problem-file-row active" : "problem-file-row"}
            title={problemTitle(problem)}
            onClick={() => onOpenProblem(problem.problem_id)}
          >
            {problemFileName(problem)}
          </button>
        </li>
      ))}
    </ul>
  );
}

function buildProblemTree(problems: ProblemSummary[]): ProblemTreeNode {
  const root: ProblemTreeNode = { name: "", path: "", folders: new Map(), problems: [] };

  for (const problem of problems) {
    let node = root;
    for (const part of problemFolderParts(problem)) {
      const path = node.path ? `${node.path}/${part}` : part;
      let folder = node.folders.get(part);
      if (!folder) {
        folder = { name: part, path, folders: new Map(), problems: [] };
        node.folders.set(part, folder);
      }
      node = folder;
    }
    node.problems.push(problem);
  }

  return root;
}

function problemFolderParts(problem: ProblemSummary): string[] {
  const rawPath = problem.path || folderPathFromProblemId(problem.problem_id);
  const parts = rawPath.replace(/\\/g, "/").replace(/^\/+/, "").split("/").filter(Boolean);
  return parts.at(-1)?.endsWith(".dsl.py") ? parts.slice(0, -1) : parts;
}

function problemFileName(problem: ProblemSummary): string {
  const parts = problem.problem_id.replace(/\\/g, "/").split("/").filter(Boolean);
  const last = parts[parts.length - 1] || problem.problem_id;
  return last.endsWith(".dsl.py") ? last : `${last}.dsl.py`;
}

function problemTitle(problem: ProblemSummary): string {
  const folder = problem.path || folderPathFromProblemId(problem.problem_id);
  return folder ? `${folder}/${problemFileName(problem)}` : problemFileName(problem);
}

function folderPathFromProblemId(problemId: string): string {
  const parts = problemId.replace(/\\/g, "/").split("/").filter(Boolean);
  if (parts.at(-1)?.endsWith(".dsl.py")) parts.pop();
  return parts.join("/");
}

function problemMatches(problem: ProblemSummary, normalizedQuery: string): boolean {
  return (
    normalizeSearch(problem.problem_id).includes(normalizedQuery) ||
    normalizeSearch(problem.root).includes(normalizedQuery) ||
    normalizeSearch(problem.path).includes(normalizedQuery) ||
    normalizeSearch(problemFileName(problem)).includes(normalizedQuery)
  );
}

function normalizeSearch(value: string): string {
  return value.trim().toLocaleLowerCase("ko");
}
