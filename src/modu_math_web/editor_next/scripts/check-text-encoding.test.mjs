import { test } from "node:test";
import assert from "node:assert/strict";
import { textEncodingErrors } from "./check-text-encoding.mjs";

const check = (source, name = "sample.tsx") => textEncodingErrors(Buffer.from(source), name);

test("accepts Korean, question sentences, and TypeScript operators", () => {
  assert.deepEqual(check('const x = value ?? "\uD55C\uAE00"; const y = obj?.name; const z = "Ready?";'), []);
});
test("rejects damaged labels in strings and JSX attributes", () => {
  assert.equal(check('const x = <label title="?? ??">???</label>;').length, 2);
});
test("checks template fragments and JSON translations", () => {
  assert.equal(check('const x = `?? ${name} ???`;').length, 2);
  assert.equal(check('{"title":"?? ??"}', 'ko.json').length, 1);
});
test("rejects invalid bytes and replacement characters", () => {
  assert.equal(textEncodingErrors(Uint8Array.from([0xc3, 0x28]), "bad.ts").length, 1);
  assert.equal(check('const x = "\uFFFD";').length, 1);
});
