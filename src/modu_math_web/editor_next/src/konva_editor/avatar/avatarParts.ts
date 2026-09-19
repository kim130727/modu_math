export type AvatarGender = "boy" | "girl";

export type AvatarHairStyle =
  // Boy Hairstyles (Global & Diverse)
  | "boy_dandy"
  | "boy_spiky"
  | "boy_afro"
  | "boy_wavy"
  | "boy_beanie"
  | "boy_cap"
  | "boy_fade"
  | "boy_curls"
  // Girl Hairstyles (Global & Diverse)
  | "girl_twintail"
  | "girl_braids"
  | "girl_wavy_long"
  | "girl_ponytail"
  | "girl_bob"
  | "girl_curly_buns"
  | "girl_hijab"
  | "girl_headband";

export type AvatarEyes = "smile" | "sparkle" | "gentle" | "thinking" | "focus" | "round";

export type AvatarMouth = "smile" | "talking" | "grin" | "curious" | "quiet";

export type AvatarPose = "pencil" | "pointing" | "thinking" | "cheering" | "waving" | "standing";

export type AvatarAccessory = "none" | "glasses" | "sunglasses" | "freckles" | "flower_clip" | "star_pin" | "hair_bow";

export interface AvatarConfig {
  gender: AvatarGender;
  skinTone: string;
  hairColor: string;
  hair: AvatarHairStyle;
  eyes: AvatarEyes;
  mouth: AvatarMouth;
  pose: AvatarPose;
  accessory: AvatarAccessory;
  clothColor: string;
  hasSpeechBubble?: boolean;
  speechText?: string;
  bubblePosition?: "top-right" | "top-left" | "right";
}

// -------------------------------------------------------------
// Global Skin Tones (Natural, Diverse & Global)
// -------------------------------------------------------------
export const SKIN_TONE_PALETTES = [
  { name: "라이트 베이지", color: "#ffedd5", blush: "#fda4af" },
  { name: "웜 피치", color: "#fed7aa", blush: "#fb7185" },
  { name: "골든 탠", color: "#fcd34d", blush: "#f43f5e" },
  { name: "올리브 허니", color: "#d4a373", blush: "#be123c" },
  { name: "카라멜 브라운", color: "#a87146", blush: "#9f1239" },
  { name: "딥 에스프레소", color: "#6c432b", blush: "#881337" },
];

// -------------------------------------------------------------
// Global Hair Colors
// -------------------------------------------------------------
export const HAIR_COLOR_PALETTES = [
  { name: "클래식 블랙", color: "#1e293b" },
  { name: "다크 브라운", color: "#451a03" },
  { name: "체스넛 브라운", color: "#78350f" },
  { name: "골든 블론드", color: "#facc15" },
  { name: "진저 오렌지", color: "#ea580c" },
  { name: "애쉬 플래티넘", color: "#94a3b8" },
];

// -------------------------------------------------------------
// Clothing Color Palettes
// -------------------------------------------------------------
export const CLOTH_COLOR_PALETTES = [
  { name: "인디고 블루", color: "#6366f1" },
  { name: "스카이 블루", color: "#38bdf8" },
  { name: "파스텔 핑크", color: "#f472b6" },
  { name: "민트 그린", color: "#34d399" },
  { name: "웜 옐로우", color: "#fbbf24" },
  { name: "라벤더 퍼플", color: "#a855f7" },
  { name: "코코아 오렌지", color: "#fb923c" },
  { name: "모던 차콜", color: "#475569" },
];

// -------------------------------------------------------------
// Boy & Girl Hairstyles
// -------------------------------------------------------------
export const BOY_HAIR_OPTIONS: Array<{ id: AvatarHairStyle; label: string }> = [
  { id: "boy_dandy", label: "댄디 숏컷" },
  { id: "boy_spiky", label: "스포티 스파이키" },
  { id: "boy_afro", label: "아프로 펌" },
  { id: "boy_wavy", label: "웨이브 가르마" },
  { id: "boy_curls", label: "귀여운 컬리헤어" },
  { id: "boy_fade", label: "투블럭 페이드" },
  { id: "boy_cap", label: "스냅백 캡" },
  { id: "boy_beanie", label: "웜 비니 모자" },
];

export const GIRL_HAIR_OPTIONS: Array<{ id: AvatarHairStyle; label: string }> = [
  { id: "girl_twintail", label: "양갈래 묶음" },
  { id: "girl_braids", label: "땋은 양갈래 (Braids)" },
  { id: "girl_ponytail", label: "하이 포니테일" },
  { id: "girl_wavy_long", label: "웨이브 긴머리" },
  { id: "girl_bob", label: "뱅 단발 (Bob)" },
  { id: "girl_curly_buns", label: "아프로 더블번" },
  { id: "girl_headband", label: "헤어밴드 웨이브" },
  { id: "girl_hijab", label: "글로벌 히잡 (Hijab)" },
];

export const EYES_OPTIONS: Array<{ id: AvatarEyes; label: string }> = [
  { id: "smile", label: "반달 미소" },
  { id: "sparkle", label: "초롱초롱" },
  { id: "gentle", label: "다정하고 또렷함" },
  { id: "thinking", label: "생각 중" },
  { id: "focus", label: "자신만만" },
  { id: "round", label: "동그란 눈" },
];

export const MOUTH_OPTIONS: Array<{ id: AvatarMouth; label: string }> = [
  { id: "smile", label: "은은한 미소" },
  { id: "talking", label: "말하는 입" },
  { id: "grin", label: "활짝 웃음" },
  { id: "curious", label: "호기심 (오!)" },
  { id: "quiet", label: "단정한 입" },
];

export const POSE_OPTIONS: Array<{ id: AvatarPose; label: string }> = [
  { id: "pencil", label: "연필 들기" },
  { id: "pointing", label: "손가락 가리키기" },
  { id: "thinking", label: "턱 괴고 생각" },
  { id: "cheering", label: "만세 / 응원" },
  { id: "waving", label: "안녕 손인사" },
  { id: "standing", label: "기본 자세" },
];

export const ACCESSORY_OPTIONS: Array<{ id: AvatarAccessory; label: string }> = [
  { id: "none", label: "없음" },
  { id: "glasses", label: "동글이 안경" },
  { id: "sunglasses", label: "선글라스" },
  { id: "freckles", label: "귀여운 주근깨" },
  { id: "flower_clip", label: "꽃 헤어핀" },
  { id: "star_pin", label: "별 머리핀" },
  { id: "hair_bow", label: "리본 핀" },
];

export function getDefaultAvatarConfig(gender: AvatarGender = "boy"): AvatarConfig {
  return {
    gender,
    skinTone: "#ffedd5",
    hairColor: "#1e293b",
    hair: gender === "boy" ? "boy_dandy" : "girl_twintail",
    eyes: gender === "boy" ? "smile" : "sparkle",
    mouth: "smile",
    pose: "pencil",
    accessory: "none",
    clothColor: gender === "boy" ? "#6366f1" : "#f472b6",
    hasSpeechBubble: false,
    speechText: "내가 도와줄게!",
    bubblePosition: "top-right",
  };
}

export function generateRandomAvatarConfig(forcedGender?: AvatarGender): AvatarConfig {
  const gender: AvatarGender = forcedGender ?? (Math.random() > 0.5 ? "boy" : "girl");
  const skin = SKIN_TONE_PALETTES[Math.floor(Math.random() * SKIN_TONE_PALETTES.length)].color;
  const hairColor = HAIR_COLOR_PALETTES[Math.floor(Math.random() * HAIR_COLOR_PALETTES.length)].color;
  const hairList = gender === "boy" ? BOY_HAIR_OPTIONS : GIRL_HAIR_OPTIONS;
  const hair = hairList[Math.floor(Math.random() * hairList.length)].id;
  const eyes = EYES_OPTIONS[Math.floor(Math.random() * EYES_OPTIONS.length)].id;
  const mouth = MOUTH_OPTIONS[Math.floor(Math.random() * MOUTH_OPTIONS.length)].id;
  const pose = POSE_OPTIONS[Math.floor(Math.random() * POSE_OPTIONS.length)].id;
  const accessory = ACCESSORY_OPTIONS[Math.floor(Math.random() * ACCESSORY_OPTIONS.length)].id;
  const clothColor = CLOTH_COLOR_PALETTES[Math.floor(Math.random() * CLOTH_COLOR_PALETTES.length)].color;

  return {
    gender,
    skinTone: skin,
    hairColor,
    hair,
    eyes,
    mouth,
    pose,
    accessory,
    clothColor,
    hasSpeechBubble: false,
    speechText: "함께 풀어보자!",
    bubblePosition: "top-right",
  };
}

/**
 * Compact, deterministic marker doodles. Colored subject interiors occlude overlaps;
 * the canvas itself stays transparent. No raster textures or SVG filters.
 */
export function compileAvatarSvg(config: AvatarConfig): string {
  const safeColor = (value: string, fallback: string) => /^#[0-9a-f]{6}$/i.test(value) ? value : fallback;
  const ink = "#394350";
  const cloth = safeColor(config.clothColor, "#6366f1");
  const skin = safeColor(config.skinTone, "#ffedd5");
  const hair = safeColor(config.hairColor, "#1e293b");
  const accentMap: Record<string, string> = {
    "#6366f1": "#f4bd65", "#38bdf8": "#f28c73", "#f472b6": "#62b7a5",
    "#34d399": "#ecaa65", "#fbbf24": "#7c91cb", "#a855f7": "#7bc5b0",
    "#fb923c": "#7ca7d0", "#475569": "#e4b36c",
  };
  const accent = accentMap[cloth.toLowerCase()] ?? "#e4b36c";
  const skinRgb = [1, 3, 5].map((start) => parseInt(skin.slice(start, start + 2), 16));
  const facialInk = skinRgb[0] * 0.299 + skinRgb[1] * 0.587 + skinRgb[2] * 0.114 < 115 ? "#fff4e5" : ink;
  const path = (d: string, fill = "none", width = 2.8, color = ink) =>
    `<path d="${d}" fill="${fill}" stroke="${color}" stroke-width="${width}"/>`;
  const mark = (d: string) => path(d, "none", 1.5);
  const wash = (d: string, color: string, width: number, opacity: number) =>
    `<path d="${d}" fill="none" stroke="${color}" stroke-width="${width}" opacity="${opacity}"/>`;

  // Deliberately uneven silhouettes, with the face kept large enough at insertion size.
  const hairFront: Record<AvatarHairStyle, string> = {
    boy_dandy: "M79 59 L78 49 Q81 34 102 36 L117 41 121 57 112 52 100 55 94 49 82 60Z",
    boy_spiky: "M79 60 L77 46 86 47 86 34 97 42 103 32 110 41 117 36 122 57 108 52 99 56 90 51Z",
    boy_afro: "M77 61 Q68 55 75 46 Q70 35 83 34 Q86 24 97 30 Q107 23 114 33 Q129 32 126 45 Q132 55 122 61 L112 54 96 55 85 52Z",
    boy_wavy: "M78 59 Q74 40 92 37 Q109 29 121 43 L123 60 110 52 101 58 91 51Z",
    boy_beanie: "M77 59 L78 44 Q82 29 103 31 Q121 33 122 49 L123 60 101 57Z",
    boy_cap: "M77 56 Q76 35 98 35 Q119 34 120 51 L137 55 135 60 115 59 98 55Z",
    boy_fade: "M79 60 L79 44 89 38 112 39 121 47 121 60 115 52 86 51Z",
    boy_curls: "M78 60 Q73 49 80 43 Q78 34 91 37 Q97 29 105 36 Q118 31 121 44 Q128 53 120 59 L107 53 95 56 87 52Z",
    girl_twintail: "M78 60 Q73 36 98 35 Q120 32 123 60 L112 53 102 57 94 51 85 57Z",
    girl_braids: "M78 60 Q74 35 100 35 Q123 35 122 60 L109 53 101 45 93 54Z",
    girl_wavy_long: "M77 60 Q73 33 99 34 Q125 33 124 61 L110 52 99 55 88 51Z",
    girl_ponytail: "M78 60 Q73 37 98 35 Q120 31 123 60 L113 52 99 55 90 51Z",
    girl_bob: "M76 73 L76 48 Q79 33 100 35 Q122 33 124 49 L124 78 117 77 116 54 84 53 83 77Z",
    girl_curly_buns: "M78 59 Q74 36 99 36 Q123 34 123 59 L108 52 96 55 85 52Z",
    girl_hijab: "M75 65 Q72 34 98 32 Q124 32 126 60 L131 88 112 97 96 90 74 94Z",
    girl_headband: "M77 62 Q72 35 98 34 Q123 31 125 60 L117 66 114 53 88 53 82 67Z",
  };
  const hairBack: Partial<Record<AvatarHairStyle, string>> = {
    girl_twintail: "M80 52 Q61 48 64 71 L58 87 Q72 92 78 74Z M120 51 Q139 49 135 71 L143 84 Q130 93 123 72Z",
    girl_braids: "M80 55 L70 62 73 71 68 80 72 89 79 83 76 73 81 65Z M120 55 L130 62 127 72 132 81 128 91 121 85 124 74 119 65Z",
    girl_wavy_long: "M79 49 Q66 58 71 75 L65 95 82 92 89 64Z M120 48 Q134 57 128 76 L138 94 119 93 112 64Z",
    girl_ponytail: "M115 40 Q140 29 144 51 L140 73 128 78 130 57 116 51Z",
    girl_curly_buns: "M81 40 Q64 46 64 32 Q64 21 75 23 Q88 21 89 33Z M115 36 Q111 22 125 23 Q139 22 136 35 Q133 46 120 42Z",
  };
  const armDownLeft = "M77 98 L61 118 55 151 63 153 74 130 87 119Z";
  const armDownRight = "M120 97 L138 118 145 151 136 154 125 130 113 119Z";
  const armRaisedLeft = "M82 101 L58 87 48 64 40 68 47 101 70 122Z";
  const arms: Record<AvatarPose, [string, string, string, string]> = {
    standing: [armDownLeft, armDownRight, "M55 149 Q47 152 52 159 L59 162 64 153Z", "M137 151 L145 149 Q152 157 144 162 L137 159Z"],
    pencil: [armDownLeft, "M120 97 L144 113 151 130 141 146 131 140 139 129 117 119Z", "M55 149 Q47 152 52 159 L59 162 64 153Z", "M133 137 Q139 132 144 136 L146 143 137 147 132 143Z"],
    pointing: [armDownLeft, "M120 97 L139 106 157 85 163 92 145 121 128 120 112 112Z", "M55 149 Q47 152 52 159 L59 162 64 153Z", "M156 87 L158 75 Q161 69 163 76 L163 83 168 82 169 89 163 94Z"],
    thinking: [armDownLeft, "M121 96 L140 125 128 143 111 109 107 85 115 82 121 108 127 117Z", "M55 149 Q47 152 52 159 L59 162 64 153Z", "M107 87 L103 79 Q104 75 108 79 L115 78 118 82 114 89Z"],
    cheering: [armRaisedLeft, "M119 99 L142 86 151 63 160 68 153 100 129 122Z", "M40 69 L36 59 Q37 54 42 59 L45 56 50 61 48 67Z", "M150 66 L150 58 155 55 158 59 Q164 56 164 62 L159 70Z"],
    waving: [armDownLeft, "M120 97 L141 108 151 77 160 80 154 124 138 130 116 117Z", "M55 149 Q47 152 52 159 L59 162 64 153Z", "M151 80 L146 70 Q146 66 150 68 L150 61 Q153 57 155 63 L158 59 161 65 164 63 165 71 160 82Z"],
  };
  const [left, right, leftHand, rightHand] = arms[config.pose] ?? arms.standing;
  const body = config.gender === "girl"
    ? "M86 90 L109 89 123 99 124 127 138 167 113 171 91 168 64 171 75 127 73 102Z"
    : "M86 90 L109 89 124 99 133 167 112 170 92 168 68 171 73 122 72 102Z";
  const collar = config.gender === "girl"
    ? "M88 93 Q89 105 99 100 Q109 105 112 92 L100 96Z"
    : "M88 93 L96 105 101 98 107 104 112 92 100 96Z";
  const pieces = [
    hairBack[config.hair] ? path(hairBack[config.hair]!, hair) : "",
    path(left, cloth),
    path(body, cloth),
    // Broad adjacent marker sweeps, intentionally offset with narrow paper gaps.
    wash("M82 111 L77 158 M95 108 L92 160 M111 110 L112 160", "#fff", 7, 0.14),
    wash("M84 113 L80 153 M107 112 L108 157", "#fff", 1.7, 0.5),
    mark("M76 164 L94 163"),
    path("M108 115 L120 114 119 128 109 129Z", accent, 1.5),
    path(right, cloth),
    path("M91 81 L91 92 Q100 99 108 91 L108 80", skin),
    path(collar, "#fff9ef", 1.6),
    path("M79 59 Q72 56 73 64 L79 68 M120 58 Q128 57 126 65 L121 69", skin),
    path("M80 53 L98 47 118 53 121 70 Q117 85 103 87 L91 84 80 75Z", skin),
  ];
  const eyes: Record<AvatarEyes, string> = {
    smile: "M86 65 Q89 61 92 65 M106 65 Q109 61 112 65",
    sparkle: "M88 62 L88 65 M109 61 L109 65",
    gentle: "M88 64 L90 64 M107 64 L109 64",
    thinking: "M89 60 L90 61 M110 60 L111 61",
    focus: "M86 60 L93 62 M105 62 L112 60 M89 66 L90 66 M108 66 L109 66",
    round: "M86 64 Q86 59 91 61 Q94 66 89 67Z M106 64 Q105 60 110 61 Q113 66 108 67Z",
  };
  const mouths: Record<AvatarMouth, string> = {
    smile: "M95 77 Q100 81 105 76",
    talking: "M97 76 L104 76 101 82Z",
    grin: "M94 75 Q100 85 107 75Z",
    curious: "M98 77 Q103 74 103 80 Q98 83 98 77",
    quiet: "M96 78 L103 77",
  };
  pieces.push(path(eyes[config.eyes] ?? eyes.smile, "none", 1.9, facialInk),
    path("M99 65 L97 71 101 72", "none", 1.5, facialInk),
    path(mouths[config.mouth] ?? mouths.smile, "none", 1.5, facialInk));
  if (config.hair === "girl_hijab") {
    // Wrap sits behind the face; open front leaves facial marks unobstructed.
    pieces.unshift(path(hairFront.girl_hijab, hair));
    pieces.push(path("M78 75 L88 87 105 94 M119 72 L113 83", "none", 2, accent));
  } else {
    pieces.push(path(hairFront[config.hair] ?? hairFront.boy_dandy, hair));
    pieces.push(wash("M85 44 L98 40 109 43", "#fff", 2.2, 0.5));
    if (config.hair === "boy_beanie") pieces.push(mark("M79 52 L120 52"));
    if (config.hair === "girl_headband") pieces.push(path("M82 46 Q99 32 120 47", "none", 3.5, accent));
    if (config.hair === "girl_braids") pieces.push(mark("M72 66 L78 69 M125 67 L130 70"));
  }
  const accessories: Record<AvatarAccessory, string> = {
    none: "",
    glasses: mark("M82 60 L94 59 94 69 83 70Z M104 60 L116 59 117 69 105 70Z M95 63 L104 63"),
    sunglasses: path("M82 60 L94 59 94 69 83 70Z M104 60 L116 59 117 69 105 70Z", ink, 1.9) + mark("M95 63 L104 63"),
    freckles: mark("M84 73 L85 73 M88 74 L89 74 M111 73 L112 73 M115 72 L116 72"),
    flower_clip: path("M115 43 Q107 38 113 35 Q112 28 118 32 Q125 29 123 36 Q130 41 122 43Z", accent, 1.9),
    star_pin: path("M118 31 L120 36 126 36 122 40 123 45 118 42 113 45 114 40 110 36 116 36Z", accent, 1.9),
    hair_bow: path("M111 36 L121 41 129 34 129 46 120 42 112 48Z", accent, 1.9),
  };
  pieces.push(accessories[config.accessory] ?? "");
  if (config.pose === "pencil") {
    pieces.push(path("M134 155 L152 109 160 102 160 114 142 158Z", accent, 2.5),
      mark("M152 109 L160 114 M141 150 L146 152"),
      wash("M155 119 L151 130", "#fff", 2, 0.7));
  }
  // Hands are above the face and prop so thinking and gripping remain legible.
  pieces.push(path(leftHand, skin, 2.8), path(rightHand, skin, 2.8));
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200"><g stroke-linecap="round" stroke-linejoin="round">${pieces.join("")}</g></svg>`;
  return `data:image/svg+xml;utf8,${encodeURIComponent(svg)}`;
}
