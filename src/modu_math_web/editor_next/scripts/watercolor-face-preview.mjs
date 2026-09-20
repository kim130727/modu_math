// Visual QA through the production compositor (not a separate drawing implementation).
import { api, createCanvas, Image } from "./watercolor-test-runtime.mjs";
import { mkdirSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

const directory = fileURLToPath(new URL("../../../../.tmp/watercolor-composer/", import.meta.url));
mkdirSync(directory, { recursive: true });
const sheet = createCanvas(1200, 640);
const ctx = sheet.getContext("2d");
ctx.fillStyle = "#fffdf7"; ctx.fillRect(0, 0, 1200, 640);
const styles = ["girl_bob", "girl_ponytail", "girl_braids", "boy_dandy", "boy_afro", "girl_hijab"];
for (let i = 0; i < 12; i++) {
  const config = { ...api.getDefaultAvatarConfig(), hair: styles[i % 6], eyes: "gentle", mouth: "smile", pose: "standing",
    skinTone: i < 6 ? "#fed7aa" : api.SKIN_TONE_PALETTES[i % 6].color, hairColor: i < 6 ? "#78350f" : api.HAIR_COLOR_PALETTES[i % 6].color };
  const image = new Image(); image.src = await api.renderWatercolorAvatar(config); await image.decode();
  const x = i % 6 * 200, y = Math.floor(i / 6) * 320;
  ctx.drawImage(image, 42, 0, 300, 240, x, y + 40, 200, 160);
  ctx.fillStyle = "#34405a"; ctx.font = "14px sans-serif"; ctx.textAlign = "center";
  ctx.fillText(config.hair, x + 100, y + 276);
}
const name = process.argv[2] || "faces-after";
if (!/^[a-z-]+$/.test(name)) throw new Error("Invalid preview name");
writeFileSync(`${directory}/${name}.png`, sheet.toBuffer("image/png"));
console.log(`${directory}/${name}.png`);
