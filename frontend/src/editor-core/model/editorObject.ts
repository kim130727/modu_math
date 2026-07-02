import type { LayoutSlot } from "../../types/layout";

export interface EditorObject {
  id: string;
  kind: string;
  slot: LayoutSlot;
  regionId: string | null;
}

