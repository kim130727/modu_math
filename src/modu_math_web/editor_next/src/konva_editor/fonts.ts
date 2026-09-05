export const KONVA_PREVIEW_FONT_FAMILY =
  '"Noto Sans KR", "Pretendard", "Segoe UI", "Malgun Gothic", "Apple SD Gothic Neo", "Segoe UI Symbol", sans-serif';
export const KONVA_PREVIEW_FONT_LOAD_SPEC = '30px "Noto Sans KR"';

export function normalizePreviewFontFamily(raw?: string | null): string {
  if (!raw) return KONVA_PREVIEW_FONT_FAMILY;
  const stripped = raw
    .replace(/["']?Poor Story["']?,?\s*/gi, "")
    .replace(/["']?PoorStory["']?,?\s*/gi, "")
    .trim();
  if (!stripped || stripped === "sans-serif" || stripped === "serif") {
    return KONVA_PREVIEW_FONT_FAMILY;
  }
  return stripped;
}
