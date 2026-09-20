import { api, createCanvas, Image } from "./watercolor-test-runtime.mjs";
import { mkdirSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

const directory = fileURLToPath(new URL("../../../../.tmp/watercolor-composer/", import.meta.url));
mkdirSync(directory, { recursive: true });
const configs = [
  ...api.POSE_OPTIONS.map(({ id }, i) => ({ ...api.getDefaultAvatarConfig(i % 2 ? "girl" : "boy"), pose: id, clothColor: api.CLOTH_COLOR_PALETTES[i].color })),
  ...[...api.BOY_HAIR_OPTIONS, ...api.GIRL_HAIR_OPTIONS].map(({ id }, i) => ({
    ...api.getDefaultAvatarConfig(id.startsWith("girl") ? "girl" : "boy"), hair: id, pose: "standing",
    skinTone: api.SKIN_TONE_PALETTES[i % 6].color, hairColor: api.HAIR_COLOR_PALETTES[i % 6].color,
    clothColor: api.CLOTH_COLOR_PALETTES[i % 8].color,
    eyes: api.EYES_OPTIONS[i % 6].id, mouth: api.MOUTH_OPTIONS[i % 5].id,
    accessory: api.ACCESSORY_OPTIONS[i % 7].id,
  })),
];
const sheet = createCanvas(1152, 1360);
const ctx = sheet.getContext("2d");
ctx.fillStyle = "#fffdf7"; ctx.fillRect(0, 0, sheet.width, sheet.height);
let total = 0;
for (let i = 0; i < configs.length; i++) {
  const url = await api.renderWatercolorAvatar(configs[i]);
  const bytes = Buffer.from(url.split(",")[1], "base64");
  total += bytes.length;
  writeFileSync(`${directory}/avatar-${i}.webp`, bytes);
  const image = new Image(); image.src = bytes; await image.decode();
  const x = i % 6 * 192, y = Math.floor(i / 6) * 340;
  ctx.drawImage(image, x, y, 192, 192 * image.height / image.width);
  ctx.fillStyle = "#34405a"; ctx.font = "11px sans-serif"; ctx.textAlign = "center";
  ctx.fillText(i < 6 ? configs[i].pose : configs[i].hair, x + 96, y + 332);
}
writeFileSync(`${directory}/preview.png`, sheet.toBuffer("image/png"));
console.log(directory, "average bytes:", Math.round(total / configs.length));
