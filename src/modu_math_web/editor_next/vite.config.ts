import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  base: "/static/editor_next/tldraw_assets/",
  build: {
    outDir: "static/editor_next/tldraw_assets",
    emptyOutDir: true,
    sourcemap: true,
    rollupOptions: {
      input: "index.html",
      output: {
        entryFileNames: "editor-next-tldraw.js",
        assetFileNames: "editor-next-tldraw[extname]",
      },
    },
  },
});
