import assert from "node:assert/strict";
import { test } from "node:test";
import { api, createCanvas, Image } from "./watercolor-test-runtime.mjs";

async function pixels(config) {
  const image = new Image();
  image.src = await api.renderWatercolorAvatar(config);
  await image.decode();
  const canvas = createCanvas(384, 640);
  const context = canvas.getContext("2d");
  context.drawImage(image, 0, 0);
  return context.getImageData(0, 0, 384, 640).data;
}
function changed(a, b, box = [0, 0, 384, 640]) {
  let count = 0;
  for (let y = box[1]; y < box[3]; y++) for (let x = box[0]; x < box[2]; x++) {
    const i = (y * 384 + x) * 4;
    if (a[i + 3] > 100 && b[i + 3] > 100 && Math.abs(a[i] - b[i]) + Math.abs(a[i + 1] - b[i + 1]) + Math.abs(a[i + 2] - b[i + 2]) > 40) count++;
  }
  return count;
}
test("skin, hair and clothes repaint substantial separate regions of the watercolor", async () => {
  const config = { ...api.getDefaultAvatarConfig(), pose: "standing" };
  const original = await pixels(config);
  const skin = await pixels({ ...config, skinTone: "#6c432b" });
  const hair = await pixels({ ...config, hairColor: "#ea580c" });
  const cloth = await pixels({ ...config, clothColor: "#34d399" });
  assert.ok(changed(original, skin) > 2500);
  assert.ok(changed(original, hair, [50, 0, 330, 200]) > 2500);
  assert.ok(changed(original, cloth, [0, 205, 384, 420]) > 9000);
  assert.ok(changed(original, skin, [90, 240, 290, 330]) < 50, "skin must not repaint sweater");
  assert.ok(changed(original, cloth, [70, 20, 310, 180]) < 50, "clothes must not repaint head");
  assert.ok(changed(original, hair, [0, 220, 384, 640]) < 50, "hair must not repaint body");
  assert.equal(original[3], 0, "transparent background");
});
test("every eye, mouth, accessory and hair choice produces a distinct watercolor result", async () => {
  for (const [field, choices] of [
    ["eyes", api.EYES_OPTIONS], ["mouth", api.MOUTH_OPTIONS], ["accessory", api.ACCESSORY_OPTIONS],
    ["hair", [...api.BOY_HAIR_OPTIONS, ...api.GIRL_HAIR_OPTIONS]],
    ["pose", api.POSE_OPTIONS],
  ]) {
    const results = await Promise.all(choices.map(({ id }) => api.renderWatercolorAvatar({ ...api.getDefaultAvatarConfig(), [field]: id })));
    assert.equal(new Set(results).size, choices.length, field);
  }
  assert.notEqual(await api.renderWatercolorAvatar(api.getDefaultAvatarConfig("boy")), await api.renderWatercolorAvatar(api.getDefaultAvatarConfig("girl")));
});
test("same selection is deterministic and speech settings do not alter the image", async () => {
  const config = api.getDefaultAvatarConfig();
  assert.equal(await api.renderWatercolorAvatar(config), await api.renderWatercolorAvatar({ ...config, hasSpeechBubble: true, speechText: "안녕!" }));
});

test("all new heads retain independent face and hair coloring", async () => {
  for (const { id } of [...api.BOY_HAIR_OPTIONS, ...api.GIRL_HAIR_OPTIONS]) {
    const config = { ...api.getDefaultAvatarConfig(), hair: id, pose: "standing" };
    const original = await pixels(config);
    const skin = await pixels({ ...config, skinTone: "#6c432b" });
    const hair = await pixels({ ...config, hairColor: "#94a3b8" });
    assert.ok(changed(original, skin, [120, 100, 264, 195]) > 1800, `${id}: visible face recolors`);
    assert.ok(changed(original, hair, [50, 0, 334, 200]) > 1800, `${id}: visible hair recolors`);
    assert.ok(changed(original, hair, [163, 151, 221, 182]) < 80, `${id}: hair must not recolor central face`);
  }
});

test("reference-inspired defaults use the soft bob and small calm eyes", () => {
  assert.equal(api.getDefaultAvatarConfig("girl").hair, "girl_bob");
  for (const gender of ["boy", "girl"]) {
    assert.equal(api.getDefaultAvatarConfig(gender).eyes, "gentle");
    assert.equal(api.getDefaultAvatarConfig(gender).hairColor, "#78350f");
  }
});

test("compact proportions fit all hairstyles and poses without clipping the frame", async () => {
  for (const { id: hair } of [...api.BOY_HAIR_OPTIONS, ...api.GIRL_HAIR_OPTIONS]) {
    for (const { id: pose } of api.POSE_OPTIONS) {
      const image = new Image();
      image.src = await api.renderWatercolorAvatar({ ...api.getDefaultAvatarConfig(), hair, pose });
      await image.decode();
      assert.equal(image.width, 384);
      assert.equal(image.height, 560);
      const canvas = createCanvas(image.width, image.height);
      const ctx = canvas.getContext("2d"); ctx.drawImage(image, 0, 0);
      const rgba = ctx.getImageData(0, 0, image.width, image.height).data;
      const alpha = (x, y) => rgba[(y * image.width + x) * 4 + 3];
      for (let x = 0; x < image.width; x++) {
        assert.ok(alpha(x, 0) < 32 && alpha(x, image.height - 1) < 32, `${hair}/${pose}: vertical margin`);
      }
      for (let y = 0; y < image.height; y++) {
        assert.ok(alpha(0, y) < 32 && alpha(image.width - 1, y) < 32, `${hair}/${pose}: horizontal margin`);
      }
    }
  }
});
