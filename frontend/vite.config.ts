import { defineConfig } from "vite";
import solid from "vite-plugin-solid";

export default defineConfig({
  plugins: [solid()],
  base: "/static/editor_next/assets/",
  build: {
    outDir: "../src/modu_math_web/editor_next/static/editor_next/assets",
    emptyOutDir: true,
    sourcemap: true,
    rollupOptions: {
      input: "src/main.tsx",
      output: {
        entryFileNames: "editor-next.js",
        assetFileNames: "editor-next[extname]",
      },
    },
  },
});

