import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import { api } from "./watercolor-test-runtime.mjs";

test("custom watercolor survives insertion, save/reload and replacement", async () => {
  const layout = JSON.parse(readFileSync(new URL("../../../../examples/problems/ko/S3_elem_3_008728.layout.json", import.meta.url), "utf8"));
  const base = api.problemDetailToCanonicalProblem({ problem_id: "watercolor", layout });
  const document = api.problemJsonToEditorDocument(base);
  const src = await api.renderWatercolorAvatar({ ...api.getDefaultAvatarConfig("girl"), skinTone: "#6c432b", hairColor: "#ea580c", clothColor: "#34d399", accessory: "glasses", pose: "waving" });
  assert.ok(src.startsWith("data:image/webp;base64,"));
  assert.ok(Buffer.from(src.split(",")[1], "base64").length < 150000);
  const avatar = { id: "konva_100_avatar_300", type: "image", src, x: 50, y: 60, width: 140, height: 150, preserveAspectRatio: "xMidYMid meet" };
  const saved = api.editorDocumentToProblemJson({ ...document, shapes: [...document.shapes, avatar] }, base);
  const loaded = api.problemJsonToEditorDocument(saved);
  assert.equal(loaded.shapes.find((s) => s.id === avatar.id).src, src);
  const patch = api.problemJsonToLayoutPatches(base, saved).find((p) => p.op === "add" && p.target === avatar.id);
  assert.ok(JSON.stringify(patch).includes(src));
  const target = api.avatarTargets(loaded.shapes).find((t) => t.id === avatar.id);
  assert.ok(target);
  const replaced = api.replaceAvatarShapes(loaded.shapes, target, [{ ...avatar, id: "konva_100_avatar_301" }]);
  assert.equal(replaced.length, loaded.shapes.length);
  assert.ok(!replaced.some((s) => s.id === avatar.id));
});
