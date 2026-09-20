import { createCanvas, Image, Path2D } from "@napi-rs/canvas";
import { build } from "esbuild";
import { fileURLToPath } from "node:url";

globalThis.document = { createElement: () => createCanvas(1, 1) };
globalThis.Path2D = Path2D;
globalThis.Image = class extends Image {
  set src(value) { super.src = value.startsWith("file:") ? fileURLToPath(value) : value; }
};
const result = await build({
  stdin: { contents: `
    export * from "./src/konva_editor/avatar/avatarParts";
    export * from "./src/konva_editor/avatar/watercolorRenderer";
    export * from "./src/konva_editor/avatar/avatarReplacement";
    export { problemDetailToCanonicalProblem } from "./src/api/editorApi";
    export { problemJsonToEditorDocument, editorDocumentToProblemJson } from "./src/konva_editor/converters";
    export { problemJsonToLayoutPatches } from "./src/utils/problemJsonToLayoutPatches";
  `, resolveDir: fileURLToPath(new URL("..", import.meta.url)) },
  define: { "import.meta.url": JSON.stringify(new URL("../src/konva_editor/avatar/watercolorRenderer.ts", import.meta.url).href) },
  bundle: true, write: false, format: "esm",
});
export const api = await import(`data:text/javascript;base64,${Buffer.from(result.outputFiles[0].text).toString("base64")}`);
export { createCanvas, Image };
