import type { EditorShape } from "../../types/editorShape";

export interface AvatarTarget {
  id: string;
  label: string;
  shapes: EditorShape[];
}

// Match only body parts, never a speaker's speech balloon, name or answer.
const bodyPart = /^(body|head|hair\.cap|ear\.(left|right)|eye\.(left|right)|smile|tail\.(left|right)|bow\.(left|right)|glasses\.(left|right|bridge)|hand\.(left|right))$/;

export function avatarTargets(shapes: EditorShape[]): AvatarTarget[] {
  const targets: AvatarTarget[] = [];
  for (const head of shapes) {
    if (head.type !== "circle" || !head.id.endsWith(".head")) continue;
    const prefix = head.id.slice(0, -5);
    if (!shapes.some((shape) => shape.id === `${prefix}.body`)) continue;
    const parts = shapes.filter((shape) => shape.id.startsWith(`${prefix}.`) && bodyPart.test(shape.id.slice(prefix.length + 1)));
    if (parts.some((shape) => shape.locked)) continue;
    targets.push({ id: prefix, label: "기존 캐릭터", shapes: parts });
  }
  for (const shape of shapes) {
    if (shape.type === "image" && /^konva_\d+_avatar_\d+(?:_copy\d+)?$/.test(shape.id) && !shape.locked) {
      targets.push({ id: shape.id, label: "삽입한 캐릭터", shapes: [shape] });
    }
  }
  targets.sort((a, b) => a.shapes[0].x - b.shapes[0].x);
  return targets.map((target, index) => ({ ...target, label: `${target.label} ${index + 1} (왼쪽부터)` }));
}

export function replaceAvatarShapes(shapes: EditorShape[], target: AvatarTarget | undefined, additions: EditorShape[]): EditorShape[] {
  if (!target) return [...shapes, ...additions];
  const removed = new Set(target.shapes.map((shape) => shape.id));
  const insertionIndex = shapes.findIndex((shape) => removed.has(shape.id));
  return shapes.flatMap((shape, index) => [
    ...(index === insertionIndex ? additions : []),
    ...(removed.has(shape.id) ? [] : [shape]),
  ]);
}
