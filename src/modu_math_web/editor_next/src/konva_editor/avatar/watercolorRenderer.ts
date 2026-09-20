import type { AvatarConfig, AvatarHairStyle, AvatarPose } from "./avatarParts";

const HEADS = new URL("../../assets/watercolor/heads-v2.webp", import.meta.url).href;
const BODIES = new URL("../../assets/watercolor/bodies.webp", import.meta.url).href;
const hairOrder: AvatarHairStyle[] = ["boy_dandy", "boy_spiky", "boy_afro", "boy_wavy", "boy_curls", "boy_fade", "boy_cap", "boy_beanie", "girl_twintail", "girl_braids", "girl_ponytail", "girl_wavy_long", "girl_bob", "girl_curly_buns", "girl_headband", "girl_hijab"];
const poseOrder: AvatarPose[] = ["pencil", "pointing", "thinking", "cheering", "waving", "standing"];
type RGB = [number, number, number];
type Bounds = { left: number; top: number; right: number; bottom: number };
type Tile = { canvas: HTMLCanvasElement; pixels: ImageData; skin: Bounds };
const images = new Map<string, Promise<HTMLImageElement>>();
const tiles = new Map<string, Tile>();
const renders = new Map<string, string>();

function surface(width: number, height: number) {
  const canvas = document.createElement("canvas");
  canvas.width = width;
  canvas.height = height;
  const context = canvas.getContext("2d", { willReadFrequently: true });
  if (!context) throw new Error("이미지를 그릴 수 없습니다. 브라우저를 새로고침해주세요.");
  return { canvas, context };
}
function load(src: string): Promise<HTMLImageElement> {
  let pending = images.get(src);
  if (!pending) {
    pending = new Promise<HTMLImageElement>((resolve, reject) => {
      const image = new Image();
      image.crossOrigin = "anonymous";
      image.onload = () => resolve(image);
      image.onerror = () => { images.delete(src); reject(new Error("수채화 부품을 불러오지 못했습니다. 다시 시도해주세요.")); };
      image.src = src;
    });
    images.set(src, pending);
  }
  return pending;
}
const skinPixel = (r: number, g: number, b: number) => r > 140 && r > g * 1.1 && g > b * 1.2 && r - b > 55;
const bluePixel = (r: number, g: number, b: number) => b > r * 1.3 && b > g * 1.3;
const rgb = (hex: string, fallback: string): RGB => {
  const value = /^#[0-9a-f]{6}$/i.test(hex) ? hex : fallback;
  return [1, 3, 5].map((start) => parseInt(value.slice(start, start + 2), 16)) as RGB;
};
// A generated atlas can have a neighboring strand crossing the nominal cell edge.
// Retain the connected head silhouette, including a one-pixel antialias fringe.
function isolateHead(pixels: ImageData) {
  const { width, height, data } = pixels;
  const labels = new Int32Array(width * height);
  const queue = new Int32Array(labels.length);
  let component = 0, largest = 0, largestSize = 0;
  for (let start = 0; start < labels.length; start++) {
    if (labels[start] || data[start * 4 + 3] < 16) continue;
    component++;
    let count = 1;
    queue[0] = start; labels[start] = component;
    for (let position = 0; position < count; position++) {
      const at = queue[position], x = at % width, y = Math.floor(at / width);
      for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) {
        if (x + dx < 0 || x + dx >= width || y + dy < 0 || y + dy >= height) continue;
        const neighbor = at + dy * width + dx;
        if (!labels[neighbor] && data[neighbor * 4 + 3] >= 16) {
          labels[neighbor] = component; queue[count++] = neighbor;
        }
      }
    }
    if (count > largestSize) { largest = component; largestSize = count; }
  }
  for (let i = 0; i < labels.length; i++) {
    if (labels[i] === largest) continue;
    const x = i % width, y = Math.floor(i / width);
    let fringe = false;
    for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) {
      if (x + dx >= 0 && x + dx < width && y + dy >= 0 && y + dy < height && labels[i + dy * width + dx] === largest) fringe = true;
    }
    if (!fringe) data[i * 4 + 3] = 0;
  }
}
function tile(image: HTMLImageElement, index: number, columns: number, rows: number, head: boolean): Tile {
  const key = `${head ? "head" : "body"}:${index}`;
  const existing = tiles.get(key);
  if (existing) return existing;
  // Read a small gutter before isolating the component: organic hair can cross
  // the nominal grid by a few pixels; clipping first would amputate its ends.
  const padding = head ? Math.round(image.width / columns * .08) : 0;
  const sx = Math.max(0, Math.round(index % columns * image.width / columns) - padding);
  const sy = Math.max(0, Math.round(Math.floor(index / columns) * image.height / rows) - padding);
  const width = Math.min(image.width, Math.round((index % columns + 1) * image.width / columns) + padding) - sx;
  const height = Math.min(image.height, Math.round((Math.floor(index / columns) + 1) * image.height / rows) + padding) - sy;
  const { canvas, context } = surface(width, height);
  context.drawImage(image, sx, sy, width, height, 0, 0, width, height);
  const pixels = context.getImageData(0, 0, width, height);
  if (head) isolateHead(pixels);
  // Peach hair ties must not expand face landmarks into a ponytail or braid.
  const landmarks = context.createImageData(width, height);
  landmarks.data.set(pixels.data);
  if (head) {
    for (let i = 0; i < landmarks.data.length; i += 4) {
      if (!skinPixel(landmarks.data[i], landmarks.data[i + 1], landmarks.data[i + 2])) landmarks.data[i + 3] = 0;
    }
    isolateHead(landmarks);
  }
  const skin: Bounds = { left: width, top: height, right: 0, bottom: 0 };
  for (let y = 0; y < height; y++) for (let x = 0; x < width; x++) {
    const i = (y * width + x) * 4;
    const r = landmarks.data[i], g = landmarks.data[i + 1], b = landmarks.data[i + 2], a = landmarks.data[i + 3];
    // For bodies, register only the neck, excluding raised hands.
    if (a < 180 || !skinPixel(r, g, b) || (!head && (x < width * .43 || x > width * .57 || y > height * .3))) continue;
    skin.left = Math.min(skin.left, x); skin.right = Math.max(skin.right, x);
    skin.top = Math.min(skin.top, y); skin.bottom = Math.max(skin.bottom, y);
  }
  if (skin.right <= skin.left) throw new Error("수채화 부품의 연결 위치를 확인할 수 없습니다.");
  const result = { canvas, pixels, skin };
  tiles.set(key, result);
  return result;
}
function colorTile(source: Tile, config: AvatarConfig, head: boolean): HTMLCanvasElement {
  const { canvas, context } = surface(source.canvas.width, source.canvas.height);
  const data = context.createImageData(canvas.width, canvas.height);
  data.data.set(source.pixels.data);
  const skin = rgb(config.skinTone, "#ffedd5");
  const hair = rgb(config.hairColor, "#1e293b");
  const cloth = rgb(config.clothColor, "#6366f1");
  for (let i = 0; i < data.data.length; i += 4) {
    const r = data.data[i], g = data.data[i + 1], b = data.data[i + 2], a = data.data[i + 3];
    if (a < 8 || bluePixel(r, g, b)) continue;
    let color: RGB | undefined;
    let baseline = 190;
    if (skinPixel(r, g, b)) color = skin;
    else if (head && Math.max(r, g, b) - Math.min(r, g, b) < 65 && Math.max(r, g, b) < 190) { color = hair; baseline = 73; }
    else if (!head && g > r * 1.25 && b > r * 1.25 && g > 90 && g > b * .6) { color = cloth; baseline = 165; }
    if (!color) continue;
    // Keep the source pigment variation instead of laying a flat color over the paint.
    const density = Math.max(.55, Math.min(1.28, (.299 * r + .587 * g + .114 * b) / baseline));
    for (let channel = 0; channel < 3; channel++) {
      data.data[i + channel] = density > 1
        ? color[channel] + (255 - color[channel]) * (density - 1) * .5
        : color[channel] * density;
    }
  }
  context.putImageData(data, 0, 0);
  return canvas;
}

function face(context: CanvasRenderingContext2D, config: AvatarConfig, bounds: Bounds) {
  const width = bounds.right - bounds.left;
  const cx = (bounds.left + bounds.right) / 2;
  // Anchor from the short chin, not the exposed forehead (which changes with bangs).
  const ey = bounds.bottom - width * .29;
  const ink = "#1145b8";
  const tone = rgb(config.skinTone, "#ffedd5");
  const facialInk = tone[0] * .299 + tone[1] * .587 + tone[2] * .114 < 110 ? "#ffdfac" : ink;
  context.save();
  context.translate(cx, ey);
  context.scale(width / 140, width / 140);
  context.lineCap = "round"; context.lineJoin = "round";
  const line = (d: string, color = facialInk, size = 3.2, fill?: string) => {
    const path = new Path2D(d);
    context.strokeStyle = color; context.lineWidth = size;
    if (fill) { context.fillStyle = fill; context.fill(path); }
    context.stroke(path);
  };
  const dot = (x: number, y: number, rx = 3.6, ry = 5.5) => {
    context.beginPath(); context.ellipse(x, y, rx, ry, -.08, 0, Math.PI * 2);
    context.fillStyle = facialInk; context.fill();
  };
  switch (config.eyes) {
    case "smile": line("M-31 2 Q-24 -8 -18 1 M18 1 Q25 -8 31 2"); break;
    case "round": line("M-30 0 C-30 -8 -18 -8 -18 0 C-18 8 -30 7 -30 0 M18 0 C18 -8 30 -8 30 0 C30 8 18 7 18 0"); break;
    case "thinking": dot(-22, -5); dot(27, -5); line("M-32 -15 Q-24 -21 -16 -17 M17 -19 L32 -22", facialInk, 2.3); break;
    case "focus": dot(-24, 2); dot(24, 2); line("M-32 -13 L-17 -9 M17 -9 L32 -13", facialInk, 2.5); break;
    case "sparkle":
      dot(-24, 0, 4.4, 6); dot(24, 0, 4.4, 6);
      line("M-25 -3 L-24 -3 M23 -3 L24 -3", "#fffdf2", 2); break;
    default:
      dot(-24, -1); dot(24, 1);
      line("M-31 -15 Q-26 -19 -21 -17 M20 -17 Q25 -19 30 -14", facialInk, 3);
  }
  line("M2 8 Q-6 8 -2 13", "#d57547", 3.8);
  const mouth = {
    smile: "M-12 23 C-7 33 6 33 14 23",
    talking: "M-7 25 Q0 22 8 25 Q7 39 0 38 Q-7 37 -7 25Z",
    grin: "M-14 24 Q0 30 15 23 Q4 45 -8 35Z",
    curious: "M-5 30 C-6 20 7 22 6 31 C5 39 -5 38 -5 30Z",
    quiet: "M-7 29 Q0 31 8 28",
  };
  line(mouth[config.mouth], facialInk, 2.8, config.mouth === "grin" ? "#fffdf2" : undefined);
  // Two translucent uneven pigment dabs keep cheeks soft, rather than a flat stamp.
  context.globalAlpha = .36;
  line("M-39 14 Q-44 18 -38 23 L-32 21 M33 16 Q40 13 42 20 L36 24", "#e98166", 8);
  context.globalAlpha = .16;
  line("M-39 17 L-34 20 M35 18 L40 21", "#e98166", 5);
  context.globalAlpha = 1;
  switch (config.accessory) {
    case "glasses":
      line("M-40 -8 Q-48 19 -25 19 Q-6 19 -10 -9 Q-24 -13 -40 -8 M10 -9 Q6 19 25 19 Q47 19 40 -8 Q25 -13 10 -9 M-10 -4 Q0 -9 10 -4", ink, 2.8); break;
    case "sunglasses":
      line("M-42 -9 L-9 -8 -13 15 -36 15Z M9 -8 L42 -9 37 15 13 15Z", ink, 2.8, ink);
      line("M-9 -3 L9 -3", ink, 3);
      line("M-35 -3 L-25 -4 M18 -3 L28 -4", "#b4dfea", 2); break;
    case "freckles": line("M-37 17 L-36 17 M-29 21 L-28 21 M29 20 L30 20 M37 16 L38 16", "#b16d49", 2.5); break;
    case "flower_clip":
      line("M39 -42 C22 -44 29 -61 39 -54 C42 -69 56 -62 51 -51 C67 -53 64 -38 51 -41 C51 -25 37 -29 39 -42Z", ink, 2, "#f493b1"); break;
    case "star_pin": line("M44 -64 L49 -51 62 -50 52 -42 55 -29 44 -37 33 -29 36 -42 26 -50 39 -51Z", ink, 2, "#f9c74a"); break;
    case "hair_bow": line("M23 -57 Q34 -65 45 -48 Q57 -65 66 -55 L65 -35 Q53 -31 45 -46 Q33 -29 24 -35Z", ink, 2, "#f28f9c"); break;
  }
  context.restore();
}

export function watercolorKey(config: AvatarConfig): string {
  return JSON.stringify([config.gender, config.hair, config.eyes, config.mouth, config.pose, config.accessory, config.skinTone, config.hairColor, config.clothColor]);
}
export async function renderWatercolorAvatar(config: AvatarConfig): Promise<string> {
  const key = watercolorKey(config);
  const cached = renders.get(key);
  if (cached) return cached;
  const [headImage, bodyImage] = await Promise.all([load(HEADS), load(BODIES)]);
  const head = tile(headImage, Math.max(0, hairOrder.indexOf(config.hair)), 4, 4, true);
  const body = tile(bodyImage, Math.max(0, poseOrder.indexOf(config.pose)), 3, 2, false);
  const { canvas, context } = surface(384, 560);
  const bodyScale = 360 / body.canvas.width;
  const neckX = (body.skin.left + body.skin.right) / 2;
  const bx = 192 - neckX * bodyScale;
  // Keep the approved painted parts; adjust their assembly, not their artwork.
  // A slightly shorter torso and shorter legs give a compact childlike silhouette.
  const upperScale = bodyScale * .90;
  const lowerScale = bodyScale * .72;
  const waist = body.canvas.height * .60;
  const by = 207 - body.skin.top * upperScale;
  const waistY = by + waist * upperScale;
  const paintedBody = colorTile(body, config, false);
  context.drawImage(paintedBody, 0, 0, body.canvas.width, waist,
    bx, by, body.canvas.width * bodyScale, waist * upperScale);
  context.drawImage(paintedBody, 0, waist, body.canvas.width, body.canvas.height - waist,
    bx, waistY, body.canvas.width * bodyScale, (body.canvas.height - waist) * lowerScale);
  // Register using painted skin landmarks, not approximate uniform atlas cell centers.
  // Equal face width across hair volumes: a bob must not shrink the face,
  // and a close crop must not enlarge it. Keep room for the widest silhouettes.
  const headScale = Math.min(150 / (head.skin.right - head.skin.left), 290 / head.canvas.width, 206 / head.skin.bottom);
  const hx = 192 - (head.skin.left + head.skin.right) / 2 * headScale;
  const hy = 216 - head.skin.bottom * headScale;
  context.drawImage(colorTile(head, config, true), hx, hy, head.canvas.width * headScale, head.canvas.height * headScale);
  face(context, config, {
    left: hx + head.skin.left * headScale, right: hx + head.skin.right * headScale,
    top: hy + head.skin.top * headScale, bottom: hy + head.skin.bottom * headScale,
  });
  // The thinking hand belongs in front of the chin, even with long hairstyles.
  if (config.pose === "thinking") {
    const x = body.canvas.width * .42, y = body.canvas.height * .19;
    const w = body.canvas.width * .19, h = body.canvas.height * .13;
    context.drawImage(paintedBody, x, y, w, h, bx + x * bodyScale, by + y * upperScale, w * bodyScale, h * upperScale);
  }
  // Raised hands stay readable in front of the larger bob/ponytails.
  if (["pointing", "cheering", "waving"].includes(config.pose)) {
    const sides = config.pose === "cheering" ? [0, .72] : [.72];
    for (const side of sides) {
      const x = body.canvas.width * side;
      const w = body.canvas.width * .28, h = body.canvas.height * .32;
      context.drawImage(paintedBody, x, 0, w, h, bx + x * bodyScale, by, w * bodyScale, h * upperScale);
    }
  }
  const url = canvas.toDataURL("image/webp", .9);
  renders.set(key, url);
  // Bounded result cache: previews must not retain every randomized combination.
  if (renders.size > 48) renders.delete(renders.keys().next().value!);
  return url;
}
