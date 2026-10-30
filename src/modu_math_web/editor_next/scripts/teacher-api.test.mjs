import assert from "node:assert/strict";
import { test } from "node:test";
import { build } from "esbuild";
import { fileURLToPath } from "node:url";

const result = await build({ stdin: { contents: 'export * from "./src/teacher/api"; export * from "./src/auth/session";', resolveDir: fileURLToPath(new URL("..", import.meta.url)) }, bundle: true, write: false, format: "esm", platform: "browser" });
const { TeacherApi, ApiError, editorLink, sessionToken, storeToken } = await import(`data:text/javascript;base64,${Buffer.from(result.outputFiles[0].text).toString("base64")}`);
const storage = new Map();
const events = [];
globalThis.window = { location: { origin: "https://math.example" }, sessionStorage: { getItem: key => storage.get(key) ?? null, setItem: (key, value) => storage.set(key, value), removeItem: key => storage.delete(key) }, dispatchEvent: event => events.push(event.type) };
const json = (data, status = 200) => new Response(JSON.stringify(data), { status });

test("authenticated JSON writes retain the caller's payload", async () => {
  storeToken("test-teacher-token");
  globalThis.fetch = async (path, options) => {
    assert.equal(path, "/api/v1/problem-sets/");
    assert.equal(options.headers.Authorization, "Token test-teacher-token");
    assert.deepEqual(JSON.parse(options.body), { title: "한글 문제집", problem_ids: [3, 1] });
    return json({ id: 8 });
  };
  assert.deepEqual(await new TeacherApi().post("/api/v1/problem-sets/", { title: "한글 문제집", problem_ids: [3, 1] }), { id: 8 });
});

test("lists collect every page and preserve cancellation", async () => {
  const controller = new AbortController();
  const calls = [];
  globalThis.fetch = async (path, options) => {
    calls.push(path);
    assert.equal(options.signal, controller.signal);
    return calls.length === 1 ? json({ count: 2, results: [{ id: 1 }], next: "https://math.example/api/v1/classes/?page=2" }) : json({ count: 2, results: [{ id: 2 }], next: null });
  };
  assert.deepEqual(await new TeacherApi().all("/api/v1/classes/", controller.signal), [{ id: 1 }, { id: 2 }]);
  assert.deepEqual(calls, ["/api/v1/classes/", "/api/v1/classes/?page=2"]);
});

test("pagination never sends credentials to another origin", async () => {
  let calls = 0;
  globalThis.fetch = async () => { calls++; return json({ results: [], next: "https://attacker.example/api/v1/users/" }); };
  await assert.rejects(new TeacherApi().all("/api/v1/students/"), /잘못된 다음 페이지/);
  assert.equal(calls, 1);
  await assert.rejects(new TeacherApi().get("https://attacker.example/"), /허용되지 않은 API/);
});

test("expired credentials are cleared without retrying a mutation", async () => {
  storeToken("expired");
  let calls = 0;
  globalThis.fetch = async () => { calls++; return json({ detail: "토큰이 만료되었습니다." }, 401); };
  await assert.rejects(new TeacherApi().post("/api/v1/assignments/", {}), error => error instanceof ApiError && error.status === 401);
  assert.equal(sessionToken(), "");
  assert.ok(events.includes("modu-session-expired"));
  assert.equal(calls, 1);
});

test("field validation errors are shown as readable messages", async () => {
  globalThis.fetch = async () => json({ username: ["이미 사용 중인 아이디입니다."] }, 400);
  await assert.rejects(new TeacherApi().post("/api/v1/students/", {}), /이미 사용 중인 아이디/);
});

test("editor links preserve the language and day directory without credentials", () => {
  const target = editorLink({ problem_id: "p1", file_prefix: "p1", language: "ko", path: "examples/problems/ko/day_03" });
  assert.equal(target, "/editor-konva/?problem=ko%2Fday_03%2Fp1.dsl.py");
  assert.ok(!target.includes("token"));
});
