export function toggleSelection(current: readonly string[], slotId: string, append: boolean): string[] {
  if (!append) return [slotId];
  return current.includes(slotId) ? current.filter((id) => id !== slotId) : [...current, slotId];
}

export function clearSelection(): string[] {
  return [];
}

