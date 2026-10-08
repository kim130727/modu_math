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
  const src = useMemo(
    () => `/static/editor_next/flutter_editor/index.html?embedded=1&problem=${encodeURIComponent(problemId)}&v=${encodeURIComponent(assetVersion)}`,
    [assetVersion, problemId],
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
    frameRef.current?.contentWindow?.postMessage({ type: "modu-math:host-renderer", renderer }, "*");
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
