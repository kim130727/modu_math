import "./EditorPublication.css";
import { useState } from "react";
import { editorAuthHeaders, sessionToken } from "../auth/session";
import { PublicationForm, type Publication } from "../teacher/PublicationForm";
import { Modal, useLoad } from "../teacher/components";

async function request(path: string, value?: Publication): Promise<Publication> {
  const response = await fetch(path, { method: value ? "PATCH" : "GET", headers: { "Content-Type": "application/json", ...editorAuthHeaders() }, ...(value ? { body: JSON.stringify(value) } : {}) });
  const data = await response.json();
  if (!response.ok) throw new Error(Object.values(data).flat().join(" "));
  return data;
}

export function EditorPublication({ sourceId, busy }: { sourceId: string; busy: boolean }) {
  const [open, setOpen] = useState(false);
  const [saved, setSaved] = useState(false);
  const path = `/api/editor/problems/${encodeURIComponent(sourceId)}/publication/`;
  const loaded = useLoad(() => open ? request(path) : Promise.resolve(null), [sourceId, open]);
  if (!sessionToken()) return null;
  return <><button disabled={busy} onClick={() => { setSaved(false); setOpen(true); }}>공개 범위 설정</button>{open && <Modal title="공개 범위 설정" close={() => setOpen(false)}>{loaded.loading ? <p>설정을 불러오고 있어요…</p> : loaded.error ? <p role="alert">{loaded.error}</p> : loaded.data && <PublicationForm key={sourceId} value={loaded.data} save={async value => { await request(path, value); setSaved(true); }} />}{saved && <p role="status">공개 설정을 저장했습니다.</p>}</Modal>}</>;
}
