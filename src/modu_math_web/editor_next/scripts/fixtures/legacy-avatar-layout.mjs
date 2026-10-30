// Fixed legacy geometry: editable examples may replace these people with images.
// Keep the regression fixture independent of authored lesson content.
export const legacyAvatarLayout = {
  canvas: { width: 900, height: 650 },
  slots: ["left", "right"].flatMap((side, index) => {
    const x = 80 + index * 260;
    const prefix = `slot.person.${side}`;
    return [
      { id: `${prefix}.head`, kind: "circle", content: { cx: x + 30, cy: 400, r: 25 } },
      ...["body", "hair.cap", "ear.left", "ear.right", "eye.left", "eye.right", "smile", "tail.left", "tail.right", "bow.left", "bow.right"].map((part, i) => ({ id: `${prefix}.${part}`, kind: "rect", content: { x: x + i, y: 430, width: 40, height: 20 } })),
      { id: `slot.name.${side}`, kind: "text", content: { text: side === "left" ? "상현" : "용진", x, y: 500, font_size: 20 } },
      { id: `slot.speech.${side}`, kind: "text", content: { text: "함께 풀어 보자!", x, y: 300, font_size: 20 } },
    ];
  }),
};
