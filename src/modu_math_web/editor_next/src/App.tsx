import { EditorKonva } from "./konva_editor/EditorKonva";
import { useEffect, useState } from "react";
import { sessionToken } from "./auth/session";
import { TeacherApi } from "./teacher/api";
import type { User } from "./teacher/types";

export default function App() {
  const local = document.getElementById("root")?.dataset.localEditor === "true";
  const [access, setAccess] = useState(local);
  const [error, setError] = useState("");
  useEffect(() => {
    if (local) return;
    let active = true;
    if (!sessionToken()) { setError("교사 관리 화면에서 먼저 로그인해 주세요."); return; }
    const api = new TeacherApi();
    void api.get<User>("/api/v1/auth/me/").then(async user => {
      if (user.role === "student") throw new Error("교사 또는 관리자 계정이 필요합니다.");
      await api.post("/api/v1/auth/editor-session/");
      if (active) setAccess(true);
    }).catch(err => { if (active) setError(err.message); });
    return () => { active = false; };
  }, [local]);
  return access ? <div className="authenticated-editor"><a className="teacher-return-link" href="/teacher/">← 교사 학습관리</a><EditorKonva /></div> : <main style={{ padding: 40 }}><h1>모두의 수학 문제 편집기</h1><p>{error || "교사 권한을 확인하고 있습니다…"}</p><a href="/teacher/">교사 관리 화면으로 이동 →</a></main>;
}
