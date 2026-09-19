import { build } from "esbuild";
import { execFileSync } from "node:child_process";
import { mkdirSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("..", import.meta.url));
const output = fileURLToPath(new URL("../../../../.tmp/avatar-marker-preview/", import.meta.url));
const sourcePath = "src/modu_math_web/editor_next/src/konva_editor/avatar/avatarParts.ts";
async function load(contents) {
  const result = await build({ stdin: { contents, loader: "ts", resolveDir: root }, bundle: true, write: false, format: "esm" });
  return import(`data:text/javascript;base64,${Buffer.from(result.outputFiles[0].text).toString("base64")}`);
}
const current = await load('export * from "./src/konva_editor/avatar/avatarParts.ts";');
const previous = await load(execFileSync("git", ["show", `HEAD:${sourcePath}`], { cwd: root, encoding: "utf8" }));
mkdirSync(output, { recursive: true });
const decode = (url) => decodeURIComponent(url.slice(url.indexOf(",") + 1));
const configurations = [
  ...current.POSE_OPTIONS.map(({ id }, i) => ({ ...current.getDefaultAvatarConfig(), pose: id, clothColor: current.CLOTH_COLOR_PALETTES[i].color })),
  ...[...current.BOY_HAIR_OPTIONS, ...current.GIRL_HAIR_OPTIONS].map(({ id }, i) => ({
    ...current.getDefaultAvatarConfig(id.startsWith("girl") ? "girl" : "boy"),
    hair: id, pose: "standing", accessory: current.ACCESSORY_OPTIONS[i % current.ACCESSORY_OPTIONS.length].id,
    eyes: current.EYES_OPTIONS[i % current.EYES_OPTIONS.length].id,
    mouth: current.MOUTH_OPTIONS[i % current.MOUTH_OPTIONS.length].id,
    hairColor: current.HAIR_COLOR_PALETTES[i % current.HAIR_COLOR_PALETTES.length].color,
    skinTone: current.SKIN_TONE_PALETTES[i % current.SKIN_TONE_PALETTES.length].color,
    clothColor: current.CLOTH_COLOR_PALETTES[i % current.CLOTH_COLOR_PALETTES.length].color,
  })),
];
const sizes = { before: [], after: [], dataUrlAfter: [] };
const cells = configurations.map((config, i) => {
  const url = current.compileAvatarSvg(config);
  const svg = decode(url);
  sizes.before.push(Buffer.byteLength(decode(previous.compileAvatarSvg(config))));
  sizes.after.push(Buffer.byteLength(svg));
  sizes.dataUrlAfter.push(Buffer.byteLength(url));
  writeFileSync(`${output}/avatar-${i}.svg`, svg);
  const x = (i % 6) * 210;
  const y = Math.floor(i / 6) * 230;
  return `<g transform="translate(${x} ${y})"><rect width="210" height="230" fill="${i % 2 ? "#fffdf7" : "#fff"}"/>${svg}<text x="105" y="213" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#555">${i < 6 ? config.pose : config.hair}</text></g>`;
});
writeFileSync(`${output}/contact-sheet.svg`, `<svg xmlns="http://www.w3.org/2000/svg" width="1260" height="920" viewBox="0 0 1260 920"><rect width="1260" height="920" fill="#fffdf7"/>${cells.join("")}</svg>`);
console.log(JSON.stringify({ output, samples: configurations.length, ...Object.fromEntries(Object.entries(sizes).map(([key, values]) => [key, { min: Math.min(...values), max: Math.max(...values), mean: Math.round(values.reduce((a, b) => a + b) / values.length) }])) }, null, 2));
