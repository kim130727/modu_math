import assert from "node:assert/strict";
import { test } from "node:test";
import { build } from "esbuild";
import { fileURLToPath } from "node:url";

const bundle = await build({
  stdin: { contents: 'export * from "./src/konva_editor/avatar/avatarParts.ts";', resolveDir: fileURLToPath(new URL("..", import.meta.url)) },
  bundle: true, write: false, format: "esm",
});
const { compileAvatarSvg, getDefaultAvatarConfig, SKIN_TONE_PALETTES, HAIR_COLOR_PALETTES, CLOTH_COLOR_PALETTES } =
  await import(`data:text/javascript;base64,${Buffer.from(bundle.outputFiles[0].text).toString("base64")}`);
const svg = (config) => decodeURIComponent(compileAvatarSvg(config).split(",")[1]);
test("all skin, hair and clothing choices paint visible filled areas, not just tiny strokes", () => {
  for (const [field, palette, minimum] of [
    ["skinTone", SKIN_TONE_PALETTES, 5], ["hairColor", HAIR_COLOR_PALETTES, 1], ["clothColor", CLOTH_COLOR_PALETTES, 3],
  ]) {
    for (const { color } of palette) {
      const source = svg({ ...getDefaultAvatarConfig(), [field]: color });
      assert.ok(source.split(`fill="${color}"`).length - 1 >= minimum, `${field}: ${color}`);
    }
  }
});
test("gender changes clothing shape even with the same hairstyle and palette", () => {
  const base = getDefaultAvatarConfig();
  assert.notEqual(svg(base), svg({ ...base, gender: "girl" }));
});
test("long hair, headwear and hijab retain the selected head color", () => {
  for (const hair of ["girl_twintail", "girl_braids", "girl_hijab", "boy_cap", "boy_beanie"]) {
    assert.ok(svg({ ...getDefaultAvatarConfig(), hair, hairColor: "#78350f" }).includes('fill="#78350f"'));
  }
});
