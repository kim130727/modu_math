import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { test } from "node:test";
import { build } from "esbuild";

const bundle = await build({
  stdin: {
    contents: `
      export * from "./src/konva_editor/avatar/avatarReplacement";
      export { problemDetailToCanonicalProblem } from "./src/api/editorApi";
      export { problemJsonToEditorDocument, editorDocumentToProblemJson } from "./src/konva_editor/converters";
      export { problemJsonToLayoutPatches } from "./src/utils/problemJsonToLayoutPatches";
    `,
    resolveDir: fileURLToPath(new URL("..", import.meta.url)),
  }, bundle: true, write: false, format: "esm", platform: "browser",
});
const { avatarTargets, replaceAvatarShapes, problemDetailToCanonicalProblem, problemJsonToEditorDocument, editorDocumentToProblemJson, problemJsonToLayoutPatches } =
  await import(`data:text/javascript;base64,${Buffer.from(bundle.outputFiles[0].text).toString("base64")}`);

const layout = JSON.parse(readFileSync(new URL("../../../../examples/problems/ko/S3_elem_3_008728.layout.json", import.meta.url), "utf8"));
const base = problemDetailToCanonicalProblem({ problem_id: "avatar", layout });
const document = problemJsonToEditorDocument(base);
const avatar = { id: "konva_100_avatar_200", type: "image", src: "data:image/svg+xml;base64,PHN2Zy8+", x: 200, y: 450, width: 100, height: 110 };

test("screenshot problem: replacement removes every old body part and preserves the other person, names and speech", () => {
  const targets = avatarTargets(document.shapes);
  assert.deepEqual(targets.map((target) => target.id), ["slot.person.left", "slot.person.right"]);
  const target = targets[1];
  assert.ok(target.shapes.some((shape) => shape.id.endsWith(".tail.left")));
  assert.ok(target.shapes.some((shape) => shape.id.endsWith(".bow.right")));
  const nextShapes = replaceAvatarShapes(document.shapes, target, [avatar]);
  assert.ok(nextShapes.every((shape) => !shape.id.startsWith("slot.person.right.")));
  assert.deepEqual(nextShapes.filter((shape) => shape.id !== avatar.id), document.shapes.filter((shape) => !target.shapes.includes(shape)));
  const next = editorDocumentToProblemJson({ ...document, shapes: nextShapes }, base);
  const patches = problemJsonToLayoutPatches(base, next);
  assert.deepEqual(patches.filter((patch) => patch.op === "delete").map((patch) => patch.target).sort(), target.shapes.map((shape) => shape.id).sort());
  assert.equal(patches.filter((patch) => patch.op === "add").length, 1);
  const reloaded = problemJsonToEditorDocument(next);
  assert.ok(reloaded.shapes.every((shape) => !shape.id.startsWith("slot.person.right.")));
  assert.ok(avatarTargets(reloaded.shapes).some((target) => target.id === avatar.id));
});

test("new insertion retains existing characters; repeated replacement retains only the latest avatar", () => {
  const inserted = replaceAvatarShapes(document.shapes, undefined, [avatar]);
  assert.equal(inserted.length, document.shapes.length + 1);
  const replacement = { ...avatar, id: "konva_100_avatar_201" };
  const replaced = replaceAvatarShapes(inserted, avatarTargets(inserted).find((target) => target.id === avatar.id), [replacement]);
  assert.equal(replaced.length, inserted.length);
  assert.ok(!replaced.some((shape) => shape.id === avatar.id));
  assert.ok(replaced.some((shape) => shape.id === replacement.id));
});

test("speaker group excludes balloon tail, names, unknown children and locked characters", () => {
  const shapes = [
    { id: "slot.speaker.head", type: "circle", x: 50, y: 50, radius: 20 },
    { id: "slot.speaker.body", type: "path", x: 30, y: 70, width: 40, height: 40, d: "" },
    { id: "slot.speaker.tail", type: "path", x: 20, y: 10, width: 10, height: 10, d: "" },
    { id: "slot.speaker.name", type: "text", x: 20, y: 120, text: "이름", fontSize: 20 },
  ];
  assert.deepEqual(avatarTargets(shapes)[0].shapes.map((shape) => shape.id), ["slot.speaker.head", "slot.speaker.body"]);
  assert.deepEqual(avatarTargets(shapes.map((shape) => shape.id.endsWith(".body") ? { ...shape, locked: true } : shape)), []);
});
