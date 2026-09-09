import assert from "node:assert/strict";
import { fileURLToPath } from "node:url";
import { test } from "node:test";
import { build } from "esbuild";

const bundle = await build({
  stdin: { contents: `
    export { textPlacements } from "./src/konva_editor/PlacementSyncPanel";
    export { problemJsonToLayoutPatches } from "./src/utils/problemJsonToLayoutPatches";
  `, resolveDir: fileURLToPath(new URL("..", import.meta.url)) },
  bundle: true, write: false, format: "esm", platform: "browser",
});
const { textPlacements, problemJsonToLayoutPatches } = await import(`data:text/javascript;base64,${Buffer.from(bundle.outputFiles[0].text).toString("base64")}`);

test("scope copies only text placement roles, preserving automatic and instruction roles", () => {
  const shapes = [
    { id: "auto", type: "text", text: "auto", x: 5, y: 6, fontSize: 17 },
    { id: "instruction", type: "text", semanticRole: "instruction" },
    { id: "choice", type: "text", semanticRole: "choice" },
    { id: "unknown", type: "text", semanticRole: "work_area" },
    { id: "image", type: "image" },
  ];
  assert.deepEqual(textPlacements(shapes), [{ id: "auto", role: "" }, { id: "instruction", role: "instruction" }, { id: "choice", role: "choice" }]);
  assert.deepEqual(textPlacements(shapes, ["image", "choice"]), [{ id: "choice", role: "choice" }]);
  assert.deepEqual(textPlacements(shapes, []), []);
});

test("resetting to automatic sends an explicit empty role instead of silently keeping old placement", () => {
  const object = { id: "slot.caption", type: "math_text", x: 40, y: 60, props: { text: "Caption", fontSize: 17, semantic_role: "choice" } };
  const base = { id: "test", title: "test", canvas: { width: 300, height: 220 }, objects: [object] };
  const next = { ...base, objects: [{ ...object, props: { ...object.props, semantic_role: "" } }] };
  assert.deepEqual(problemJsonToLayoutPatches(base, next), [{ target: "slot.caption", op: "update", value: { semantic_role: "" } }]);
});
