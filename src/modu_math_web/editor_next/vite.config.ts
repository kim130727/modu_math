import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { cpSync, existsSync, rmSync } from "node:fs";
import { resolve } from "node:path";

const outDir = "static/editor_next/konva_assets";

export default defineConfig({
  plugins: [react(), copyMathJaxAssets()],
  base: "/static/editor_next/konva_assets/",
  build: {
    outDir,
    emptyOutDir: true,
    sourcemap: true,
    rollupOptions: {
      input: "index.html",
      output: {
        entryFileNames: "editor-konva.js",
        chunkFileNames: "editor-konva-[name]-[hash].js",
        assetFileNames: (assetInfo) => {
          if (assetInfo.names?.some((name) => name.endsWith(".css"))) return "editor-konva[extname]";
          return "editor-konva-[name][extname]";
        },
      },
    },
  },
});

function copyMathJaxAssets() {
  return {
    name: "copy-mathjax-assets",
    closeBundle() {
      copyDirectory(resolve("node_modules/mathjax"), resolve(outDir, "mathjax"));
      copyDirectory(resolve("node_modules/@mathjax/mathjax-newcm-font"), resolve(outDir, "mathjax-newcm"));
    },
  };
}

function copyDirectory(source: string, target: string): void {
  if (!existsSync(source)) return;
  rmSync(target, { recursive: true, force: true });
  cpSync(source, target, { recursive: true });
}
