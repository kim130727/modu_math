import { useEffect, useMemo, useRef, useState } from "react";

interface FlutterEditorSurfaceProps {
  problemId: string;
  renderer: Record<string, unknown> | null;
  mode: "edit" | "studentTest";
  onModeChange: (mode: "edit" | "studentTest") => void;
  onSelectTarget: (targetId: string) => void;
  onLayoutPatch: (targetId: string, value: Record<string, number>) => void;
}

export function FlutterEditorSurface({ problemId, renderer, mode, onModeChange, onSelectTarget, onLayoutPatch }: FlutterEditorSurfaceProps) {
  const frameRef = useRef<HTMLIFrameElement | null>(null);
  const [ready, setReady] = useState(false);
  const assetVersion = document.querySelector<HTMLElement>("#root")?.dataset.flutterEditorVersion ?? "dev";
  const problemPrefix = useMemo(() => {
    const last = problemId.replace(/\\/g, "/").split("/").filter(Boolean).at(-1) ?? problemId;
    return last.endsWith(".dsl.py") ? last.slice(0, -".dsl.py".length) : last;
  }, [problemId]);
  const src = useMemo(
    () => `/static/editor_next/flutter_editor/index.html?embedded=1&problem=${encodeURIComponent(problemPrefix)}&problemId=${encodeURIComponent(problemId)}&v=${encodeURIComponent(assetVersion)}`,
    [assetVersion, problemId, problemPrefix],
  );

  useEffect(() => {
    const receive = (event: MessageEvent) => {
      if (event.source !== frameRef.current?.contentWindow || !event.data || typeof event.data !== "object") return;
      const message = event.data as Record<string, unknown>;
      if (message.type === "modu-math:flutter-editor-ready") {
        setReady(true);
        frameRef.current?.contentWindow?.postMessage({ type: "modu-math:host-mode", mode }, "*");
        return;
      }
      if (message.type === "modu-math:flutter-element-selected" && typeof message.targetId === "string") {
        onSelectTarget(message.targetId);
        return;
      }
      if (message.type === "modu-math:flutter-layout-patch") {
        const patch = message.patch as { target?: unknown; value?: unknown } | undefined;
        if (typeof patch?.target === "string" && patch.value && typeof patch.value === "object") {
          const value = Object.fromEntries(
            Object.entries(patch.value as Record<string, unknown>)
              .filter((entry): entry is [string, number] => typeof entry[1] === "number" && Number.isFinite(entry[1])),
          );
          onLayoutPatch(patch.target, value);
        }
        return;
      }
      if (message.type === "modu-math:flutter-mode-changed" && (message.mode === "edit" || message.mode === "studentTest")) {
        onModeChange(message.mode);
      }
    };
    window.addEventListener("message", receive);
    return () => window.removeEventListener("message", receive);
  }, [mode, onLayoutPatch, onModeChange, onSelectTarget]);

  useEffect(() => {
    if (!ready) return;
    frameRef.current?.contentWindow?.postMessage({ type: "modu-math:host-mode", mode }, "*");
  }, [mode, ready]);

  useEffect(() => {
    if (!ready || !renderer) return;
    const postRenderer = () => {
      frameRef.current?.contentWindow?.postMessage({ type: "modu-math:host-renderer", renderer }, "*");
    };
    postRenderer();
    const timer1 = window.setTimeout(postRenderer, 150);
    const timer2 = window.setTimeout(postRenderer, 450);
    return () => {
      window.clearTimeout(timer1);
      window.clearTimeout(timer2);
    };
  }, [ready, renderer]);

  useEffect(() => setReady(false), [src]);

  return (
    <section className="flutter-editor-surface" aria-label="Flutter 직접 편집 화면">
      {!ready ? <div className="flutter-editor-loading">Flutter 편집 화면을 불러오는 중…</div> : null}
      <iframe
        ref={frameRef}
        key={src}
        className="flutter-editor-frame"
        src={src}
        title={`Flutter editor: ${problemId}`}
        allow="clipboard-write"
      />
    </section>
  );
}
