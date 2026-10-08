import assert from "node:assert/strict";
import { existsSync, readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { test } from "node:test";
import { build } from "esbuild";

const bundle = await build({
  stdin: {
    contents: `
      export { problemDetailToCanonicalProblem } from "./src/api/editorApi";
      export { problemJsonToEditorDocument, editorDocumentToProblemJson, fitTextBoxToContent } from "./src/konva_editor/converters";
      export { problemJsonToLayoutPatches } from "./src/utils/problemJsonToLayoutPatches";
    `,
    resolveDir: fileURLToPath(new URL("..", import.meta.url)),
  },
  bundle: true,
  write: false,
  format: "esm",
  platform: "browser",
});
const { problemDetailToCanonicalProblem, problemJsonToEditorDocument, editorDocumentToProblemJson, problemJsonToLayoutPatches, fitTextBoxToContent } =
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
  const rendererPath = [
    new URL("../../../../apps/mobile/generated/examples/problems/ko/S3_elem_3_008713.renderer.json", import.meta.url),
    new URL("../../../../examples/problems/ko/S3_elem_3_008713.renderer.json", import.meta.url),
  ].find((candidate) => existsSync(candidate));
  if (!rendererPath) return;
  const renderer = JSON.parse(readFileSync(rendererPath, "utf8"));
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

test("2151 centered addend keeps its visual position when fitting width", () => {
  const shape = {
    id: "slot.second_addend",
    type: "text",
    text: "2 7 5",
    x: 149.156,
    y: 136.503,
    width: 59,
    height: 33,
    fontSize: 26,
    lineHeight: 1.25,
    align: "center",
    valign: "top",
    sourceKind: "text_box",
  };
  const oldCenter = shape.x + shape.width / 2;
  const patch = fitTextBoxToContent(shape, "width");
  assert.equal(patch.x + patch.width / 2, oldCenter);
  assert.equal(patch.y, undefined);
});

test("combined content fit preserves center and middle anchors", () => {
  const shape = {
    id: "slot.centered",
    type: "text",
    text: "2 7 5",
    x: 100,
    y: 200,
    width: 120,
    height: 80,
    fontSize: 26,
    lineHeight: 1.25,
    align: "center",
    valign: "middle",
    sourceKind: "text_box",
  };
  const patch = fitTextBoxToContent(shape, "both");
  assert.equal(patch.x + patch.width / 2, shape.x + shape.width / 2);
  assert.equal(patch.y + patch.height / 2, shape.y + shape.height / 2);
});

for (const text of ["  8   6 9  ", "869", "日本語の問題", "中文题目", "ប្រយោគគុណ"]) {
  test(`text-only edits preserve box geometry and font: ${text}`, () => {
    const slot = { id: "slot.caption", kind: "text_box", content: {
      text: "8   6   9", x: 50, y: 60, width: 340, height: 170,
      font_size: 24, font_family: "Noto Sans Khmer", align: "right", line_height: 1.5,
    } };
    const base = problemDetailToCanonicalProblem({ problem_id: "box", layout: {
      canvas: { width: 900, height: 500 }, slots: [slot],
    } });
    const doc = problemJsonToEditorDocument(base);
    assert.equal(doc.shapes[0].height, 170);
    assert.equal(doc.shapes[0].fontFamily, "Noto Sans Khmer");
    assert.equal(doc.shapes[0].align, "right");
    doc.shapes[0].text = text;
    const next = editorDocumentToProblemJson(doc, base);
    const patches = problemJsonToLayoutPatches(base, next);
    assert.deepEqual(patches, [{ target: "slot.caption", op: "update", value: { text } }]);
    assert.equal(problemJsonToEditorDocument(next).shapes[0].height, 170);
  });
}

test("vertical and horizontal text box resizing produces correct layout patches", () => {
  const slot = { id: "slot.caption", kind: "text_box", content: {
    text: "1 6 5\n+ 2 5 8", x: 50, y: 60, width: 120, height: 42,
    font_size: 28, font_family: "Noto Sans KR", align: "left", valign: "middle", line_height: 1.25,
  } };
  const base = problemDetailToCanonicalProblem({ problem_id: "box", layout: {
    canvas: { width: 900, height: 500 }, slots: [slot],
  } });
  const doc = problemJsonToEditorDocument(base);
  assert.equal(doc.shapes[0].height, 42);

  // Resize height vertically
  doc.shapes[0].height = 80;
  const nextHeight = editorDocumentToProblemJson(doc, base);
  const heightPatches = problemJsonToLayoutPatches(base, nextHeight);
  assert.deepEqual(heightPatches, [{ target: "slot.caption", op: "update", value: { height: 80 } }]);

  // Resize width horizontally
  doc.shapes[0].width = 160;
  const nextBoth = editorDocumentToProblemJson(doc, base);
  const bothPatches = problemJsonToLayoutPatches(base, nextBoth);
  assert.deepEqual(bothPatches, [{ target: "slot.caption", op: "update", value: { width: 160, height: 80 } }]);
});
