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
  { name: "골든 탠", color: "#e7b17a", blush: "#f43f5e" },
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
    skinTone: "#fed7aa",
    hairColor: "#78350f",
    hair: gender === "boy" ? "boy_dandy" : "girl_bob",
    eyes: "gentle",
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
