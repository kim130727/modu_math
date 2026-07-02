export function toggleSelection(current: readonly string[], slotId: string, append: boolean): string[] {
  if (!append) return [slotId];
  return current.includes(slotId) ? current.filter((id) => id !== slotId) : [...current, slotId];
}

export function matchSlotIdFromSvgElement(elementId: string | null, slotIds: readonly string[]): string | null {
  if (!elementId) return null;
  const sortedSlotIds = [...slotIds].sort((left, right) => right.length - left.length);
  return sortedSlotIds.find((slotId) => elementId === slotId || elementId.startsWith(`${slotId}.`)) ?? null;
}

export function clearSelection(): string[] {
  return [];
}
