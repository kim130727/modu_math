import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { test } from "node:test";
import { build } from "esbuild";

const bundle = await build({
  stdin: {
    contents: `
      export { problemDetailToCanonicalProblem } from "./src/api/editorApi";
      export { problemJsonToEditorDocument, editorDocumentToProblemJson } from "./src/konva_editor/converters";
      export { problemJsonToLayoutPatches } from "./src/utils/problemJsonToLayoutPatches";
    `,
    resolveDir: fileURLToPath(new URL("..", import.meta.url)),
  },
  bundle: true,
  write: false,
  format: "esm",
  platform: "browser",
});
const { problemDetailToCanonicalProblem, problemJsonToEditorDocument, editorDocumentToProblemJson, problemJsonToLayoutPatches } =
  await import(`data:text/javascript;base64,${Buffer.from(bundle.outputFiles[0].text).toString("base64")}`);

for (const anchor of ["start", "middle", "end"]) {
  for (const x of [100, 958]) {
    test(`plain ${anchor} text at x=${x} keeps its anchor through repeated edits and reloads`, () => {
      const slot = { id: "slot.label", kind: "text", content: { text: "0", x, y: 249, font_size: 15, anchor } };
      for (let cycle = 0; cycle < 5; cycle++) {
        const base = problemDetailToCanonicalProblem({ problem_id: "anchor", layout: { canvas: { width: 960, height: 420 }, slots: [slot] } });
        const doc = problemJsonToEditorDocument(base);
        const shape = doc.shapes[0];
        const offset = anchor === "middle" ? shape.width / 2 : anchor === "end" ? shape.width : 0;
        assert.equal(shape.x + offset, x + cycle * 2);
        const unchanged = editorDocumentToProblemJson(doc, base);
        assert.equal(problemJsonToLayoutPatches(base, unchanged).some((patch) => "x" in patch.value), false);
        shape.x += 2;
        const edited = editorDocumentToProblemJson(doc, base);
        for (const patch of problemJsonToLayoutPatches(base, edited)) Object.assign(slot.content, patch.value);
        assert.equal(slot.content.x, x + (cycle + 1) * 2);
      }
    });
  }
}

test("8713 ruler labels preserve their renderer anchors on load and save", () => {
  const renderer = JSON.parse(readFileSync(new URL("../../../../examples/problems/ko/S3_elem_3_008713.renderer.json", import.meta.url), "utf8"));
  renderer.elements = renderer.elements.filter((element) => element.id.includes("ruler.label."));
  assert.equal(renderer.elements.length, 4);
  const base = problemDetailToCanonicalProblem({ problem_id: "8713", renderer });
  const doc = problemJsonToEditorDocument(base);
  for (const shape of doc.shapes) {
    const element = renderer.elements.find((item) => item.source_ref === shape.id);
    assert.equal(shape.x + shape.width / 2, element.attributes.x);
  }
  const patches = problemJsonToLayoutPatches(base, editorDocumentToProblemJson(doc, base));
  assert.equal(patches.some((patch) => "x" in patch.value), false);
});

test("actual text boxes retain their minimum width and top-left position", () => {
  const base = { id: "box", title: "box", canvas: { width: 960, height: 420 }, objects: [{
    id: "slot.box", type: "math_text", x: 100, y: 200,
    props: { text: "0", fontSize: 15, width: 15, textAlign: "center", sourceKind: "text_box" },
  }] };
  const shape = problemJsonToEditorDocument(base).shapes[0];
  assert.equal(shape.width, 24);
  assert.equal(shape.x, 100);
});
