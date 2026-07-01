const ERROR_TYPES = Object.freeze({
  DSL_PARSE_ERROR: "DSL_PARSE_ERROR",
  DSL_PATCH_ERROR: "DSL_PATCH_ERROR",
  BUILD_ERROR: "BUILD_ERROR",
  SCHEMA_ERROR: "SCHEMA_ERROR",
  NETWORK_ERROR: "NETWORK_ERROR",
  UNKNOWN_ERROR: "UNKNOWN_ERROR",
});

function encodedProblemPath(problemId, suffix = "") {
  const safe = String(problemId || "")
    .split("/")
    .map(encodeURIComponent)
    .join("/");
  return `/api/editor/problems/${safe}${suffix}`;
}

function getCookie(name) {
  const cookieValue = document.cookie
    .split(";")
    .map((item) => item.trim())
    .find((item) => item.startsWith(`${name}=`));
  return cookieValue ? decodeURIComponent(cookieValue.slice(name.length + 1)) : "";
}

function csrfHeaders(method) {
  if (!method || method.toUpperCase() === "GET") return {};
  const token = getCookie("csrftoken");
  return token ? { "X-CSRFToken": token } : {};
}

export function classifyApiError(message, status = 0, payload = null) {
  const text = String(message || payload?.error || "");
  if (status === 0 || /network|fetch/i.test(text)) return ERROR_TYPES.NETWORK_ERROR;
  if (/patch|DslPatchError|layout-patch|slot/i.test(text)) return ERROR_TYPES.DSL_PATCH_ERROR;
  if (/parse|syntax|invalid DSL/i.test(text)) return ERROR_TYPES.DSL_PARSE_ERROR;
  if (/schema|validation/i.test(text)) return ERROR_TYPES.SCHEMA_ERROR;
  if (/build|stderr|compiler/i.test(text) || status >= 500) return ERROR_TYPES.BUILD_ERROR;
  return ERROR_TYPES.UNKNOWN_ERROR;
}

export async function requestJson(url, options = {}) {
  const method = options.method || "GET";
  const headers = {
    ...csrfHeaders(method),
    ...(options.body ? { "Content-Type": "application/json" } : {}),
    ...(options.headers || {}),
  };

  let response;
  let payload;
  try {
    response = await fetch(url, { ...options, headers });
    payload = await response.json();
  } catch (error) {
    const wrapped = new Error("네트워크 요청에 실패했습니다.");
    wrapped.status = 0;
    wrapped.payload = { error: String(error) };
    wrapped.category = ERROR_TYPES.NETWORK_ERROR;
    throw wrapped;
  }

  if (!response.ok || payload?.ok === false) {
    const message = payload?.error || payload?.message || `HTTP ${response.status}`;
    const error = new Error(message);
    error.status = response.status;
    error.payload = payload;
    error.category = classifyApiError(message, response.status, payload);
    throw error;
  }
  return payload;
}

export function listProblems() {
  return requestJson("/api/editor/problems/");
}

export function loadProblem(problemId) {
  return requestJson(encodedProblemPath(problemId, "/"));
}

export function saveDsl(problemId, dsl) {
  return requestJson(encodedProblemPath(problemId, "/dsl/"), {
    method: "POST",
    body: JSON.stringify({ dsl }),
  });
}

export function formatDsl(problemId) {
  return requestJson(encodedProblemPath(problemId, "/dsl/format/"), { method: "POST" });
}

export function buildProblem(problemId) {
  return requestJson(encodedProblemPath(problemId, "/build/"), { method: "POST" });
}

export function applyLayoutPatches(problemId, patches, options = {}) {
  return requestJson(encodedProblemPath(problemId, "/layout-patch/"), {
    method: "POST",
    body: JSON.stringify({ patches, ...options }),
  });
}

export function applyLayoutPatchesAndBuild(problemId, patches, options = {}) {
  return requestJson(encodedProblemPath(problemId, "/layout-patch-and-build/"), {
    method: "POST",
    body: JSON.stringify({ patches, ...options }),
  });
}

