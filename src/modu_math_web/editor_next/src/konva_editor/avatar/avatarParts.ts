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
 * ModuMath Unique Modern Minimalist Diverse Kid Avatar Generator (200x200 canvas)
 */
export function compileAvatarSvg(config: AvatarConfig): string {
  const line = "#1e293b"; // Clean dark slate ink line
  const skin = config.skinTone || "#ffedd5";
  const hairColor = config.hairColor || "#1e293b";
  const cloth = config.clothColor || "#6366f1";

  // Match blush color to skin tone
  const currentSkinObj = SKIN_TONE_PALETTES.find((s) => s.color === skin) ?? SKIN_TONE_PALETTES[0];
  const blush = currentSkinObj.blush;

  const parts: string[] = [];

  // 1. Back Hair Layer (Long hair, braids, buns, ponytail in background)
  parts.push(renderBackHair(config.hair, hairColor, line));

  // 2. Body & Arms Layer (Exact 2 arms per pose with distinct Boy/Girl collar)
  parts.push(renderBodyAndPose(config.pose, cloth, line, skin, config.gender));

  // 3. Head, Neck & Ears Base Layer
  parts.push(`
    <!-- Neck -->
    <path d="M 92 120 L 92 133 L 108 133 L 108 120 Z" fill="${skin}" stroke="${line}" stroke-width="2.6" stroke-linejoin="round" />
    
    <!-- Ears (Natural attached curves with inner crease) -->
    <path d="M 64 78 C 55 78, 55 92, 64 92" fill="${skin}" stroke="${line}" stroke-width="2.6" stroke-linecap="round" />
    <path d="M 63 82 C 60 84, 60 86, 63 88" stroke="${line}" stroke-width="1.8" fill="none" stroke-linecap="round" />
    
    <path d="M 136 78 C 145 78, 145 92, 136 92" fill="${skin}" stroke="${line}" stroke-width="2.6" stroke-linecap="round" />
    <path d="M 137 82 C 140 84, 140 86, 137 88" stroke="${line}" stroke-width="1.8" fill="none" stroke-linecap="round" />

    <!-- Head / Face Contour (Slightly softer curve for girl, sturdy for boy) -->
    <path d="M 63 76 C 63 46, 137 46, 137 76 C 137 106, 126 124, 100 124 C 74 124, 63 106, 63 76 Z" fill="${skin}" stroke="${line}" stroke-width="2.8" stroke-linejoin="round" />
    
    <!-- Cheerful Soft Blush -->
    <ellipse cx="74" cy="94" rx="5.5" ry="3.5" fill="${blush}" opacity="0.65" />
    <ellipse cx="126" cy="94" rx="5.5" ry="3.5" fill="${blush}" opacity="0.65" />
  `);

  // 4. Eyes & Eyebrows (Distinct features for boy vs girl)
  parts.push(renderEyes(config.eyes, line, config.gender));

  // 5. Nose & Mouth
  parts.push(renderMouth(config.mouth, line, config.gender));

  // 6. Front Hair Layer
  parts.push(renderFrontHair(config.hair, hairColor, line));

  // 7. Accessories (Glasses, Pins, Freckles)
  parts.push(renderAccessory(config.accessory, line, skin));

  const svgContent = `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <style>
      .notion-line { stroke: ${line}; stroke-width: 2.8; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .notion-fill { fill: ${line}; }
    </style>
  </defs>
  ${parts.join("\n")}
</svg>`.trim();

  return `data:image/svg+xml;utf8,${encodeURIComponent(svgContent)}`;
}

// -------------------------------------------------------------
// Back Hair (Rendered behind head & shoulders)
// -------------------------------------------------------------
function renderBackHair(hair: AvatarHairStyle, hairColor: string, line: string): string {
  switch (hair) {
    case "girl_twintail":
      return `
        <!-- Girl Twin-tails (Behind) -->
        <path d="M 62 76 C 40 76, 28 98, 30 125 C 32 136, 44 138, 48 126 C 52 108, 56 90, 64 80 Z" fill="${hairColor}" stroke="${line}" stroke-width="2.8" stroke-linejoin="round" />
        <path d="M 138 76 C 160 76, 172 98, 170 125 C 168 136, 156 138, 152 126 C 148 108, 144 90, 136 80 Z" fill="${hairColor}" stroke="${line}" stroke-width="2.8" stroke-linejoin="round" />
        <ellipse cx="58" cy="80" rx="4.5" ry="3.5" fill="#f43f5e" />
        <ellipse cx="142" cy="80" rx="4.5" ry="3.5" fill="#f43f5e" />
      `;
    case "girl_braids":
      return `
        <!-- Girl Braids (땋은 머리) -->
        <path d="M 60 80 C 48 95, 46 120, 50 145 C 52 152, 58 152, 58 144 C 54 122, 56 100, 66 84 Z" fill="${hairColor}" stroke="${line}" stroke-width="2.6" stroke-linejoin="round" />
        <circle cx="53" cy="100" r="4.5" fill="${hairColor}" stroke="${line}" stroke-width="1.8" />
        <circle cx="52" cy="116" r="4.5" fill="${hairColor}" stroke="${line}" stroke-width="1.8" />
        <circle cx="51" cy="132" r="4.5" fill="${hairColor}" stroke="${line}" stroke-width="1.8" />
        <ellipse cx="51" cy="142" rx="3.5" ry="2.5" fill="#38bdf8" />
        
        <path d="M 140 80 C 152 95, 154 120, 150 145 C 148 152, 142 152, 142 144 C 146 122, 144 100, 134 84 Z" fill="${hairColor}" stroke="${line}" stroke-width="2.6" stroke-linejoin="round" />
        <circle cx="147" cy="100" r="4.5" fill="${hairColor}" stroke="${line}" stroke-width="1.8" />
        <circle cx="148" cy="116" r="4.5" fill="${hairColor}" stroke="${line}" stroke-width="1.8" />
        <circle cx="149" cy="132" r="4.5" fill="${hairColor}" stroke="${line}" stroke-width="1.8" />
        <ellipse cx="149" cy="142" rx="3.5" ry="2.5" fill="#38bdf8" />
      `;
    case "girl_ponytail":
      return `
        <!-- Girl High Ponytail (Behind) -->
        <path d="M 132 42 C 154 30, 180 40, 178 72 C 176 96, 160 110, 150 112 C 156 92, 162 68, 140 52 Z" fill="${hairColor}" stroke="${line}" stroke-width="2.8" stroke-linejoin="round" />
        <ellipse cx="136" cy="46" rx="4.5" ry="5.5" fill="#f43f5e" />
      `;
    case "girl_wavy_long":
      return `
        <!-- Girl Long Wavy Hair (Behind) -->
        <path d="M 54 75 C 40 105, 42 145, 58 160 C 66 162, 70 150, 60 130 L 58 76 Z" fill="${hairColor}" stroke="${line}" stroke-width="2.6" stroke-linejoin="round" />
        <path d="M 146 75 C 160 105, 158 145, 142 160 C 134 162, 130 150, 140 130 L 142 76 Z" fill="${hairColor}" stroke="${line}" stroke-width="2.6" stroke-linejoin="round" />
      `;
    case "girl_curly_buns":
      return `
        <!-- Girl Afro Double Buns (Behind) -->
        <circle cx="54" cy="36" r="16" fill="${hairColor}" stroke="${line}" stroke-width="2.8" />
        <circle cx="146" cy="36" r="16" fill="${hairColor}" stroke="${line}" stroke-width="2.8" />
        <ellipse cx="60" cy="48" rx="4" ry="2.5" fill="#ec4899" />
        <ellipse cx="140" cy="48" rx="4" ry="2.5" fill="#ec4899" />
      `;
    case "girl_hijab":
      return `
        <!-- Global Hijab / Headscarf Base (Behind) -->
        <path d="M 52 75 C 44 110, 50 160, 70 175 L 130 175 C 150 160, 156 110, 148 75 Z" fill="#8b5cf6" stroke="${line}" stroke-width="2.8" stroke-linejoin="round" />
      `;
    default:
      return "";
  }
}

// -------------------------------------------------------------
// Eyes & Eyebrows (Distinct Boy / Girl styling)
// -------------------------------------------------------------
function renderEyes(eyes: AvatarEyes, line: string, gender: AvatarGender): string {
  const isGirl = gender === "girl";
  const browWidth = isGirl ? "2.0" : "2.6";

  switch (eyes) {
    case "sparkle":
      return `
        <!-- Sparkle Eyes with Clean Natural Arched Brows -->
        <path d="M 74 69 Q 82 65 90 70" class="notion-line" stroke-width="${browWidth}" />
        <path d="M 110 70 Q 118 65 126 69" class="notion-line" stroke-width="${browWidth}" />
        
        <ellipse cx="82" cy="83" rx="5" ry="6.5" fill="${line}" />
        <circle cx="80.5" cy="80.5" r="2" fill="#ffffff" />
        <circle cx="83.5" cy="85.5" r="1.2" fill="#ffffff" />
        
        <ellipse cx="118" cy="83" rx="5" ry="6.5" fill="${line}" />
        <circle cx="116.5" cy="80.5" r="2" fill="#ffffff" />
        <circle cx="119.5" cy="85.5" r="1.2" fill="#ffffff" />
      `;
    case "gentle":
      return `
        <!-- Gentle & Bright Eyes -->
        <path d="M 74 69 Q 82 65 90 70" class="notion-line" stroke-width="${browWidth}" />
        <path d="M 110 70 Q 118 65 126 69" class="notion-line" stroke-width="${browWidth}" />
        
        <ellipse cx="82" cy="83" rx="4.5" ry="5.8" fill="${line}" />
        <circle cx="80.5" cy="81" r="1.8" fill="#ffffff" />
        
        <ellipse cx="118" cy="83" rx="4.5" ry="5.8" fill="${line}" />
        <circle cx="116.5" cy="81" r="1.8" fill="#ffffff" />
      `;
    case "thinking":
      return `
        <!-- Thinking Eyes (Looking Up) -->
        <path d="M 74 69 Q 82 65 90 70" class="notion-line" stroke-width="${browWidth}" />
        <path d="M 110 70 Q 118 67 126 66" class="notion-line" stroke-width="${browWidth}" />
        
        <ellipse cx="83" cy="79" rx="4.5" ry="5.5" fill="${line}" />
        <circle cx="82" cy="77" r="1.6" fill="#ffffff" />
        
        <ellipse cx="119" cy="79" rx="4.5" ry="5.5" fill="${line}" />
        <circle cx="118" cy="77" r="1.6" fill="#ffffff" />
      `;
    case "focus":
      return `
        <!-- Focus / Confident Eyes -->
        <path d="M 74 72 L 90 69" class="notion-line" stroke-width="${browWidth}" />
        <path d="M 110 69 L 126 72" class="notion-line" stroke-width="${browWidth}" />
        
        <ellipse cx="83" cy="84" rx="4.8" ry="5.8" fill="${line}" />
        <circle cx="81.5" cy="82" r="1.8" fill="#ffffff" />
        
        <ellipse cx="117" cy="84" rx="4.8" ry="5.8" fill="${line}" />
        <circle cx="115.5" cy="82" r="1.8" fill="#ffffff" />
      `;
    case "round":
      return `
        <!-- Round Curious Eyes -->
        <path d="M 76 69 Q 83 66 90 70" class="notion-line" stroke-width="${browWidth}" />
        <path d="M 110 70 Q 117 66 124 69" class="notion-line" stroke-width="${browWidth}" />
        
        <circle cx="83" cy="84" r="5" fill="${line}" />
        <circle cx="81" cy="82" r="1.8" fill="#ffffff" />
        
        <circle cx="117" cy="84" r="5" fill="${line}" />
        <circle cx="115" cy="82" r="1.8" fill="#ffffff" />
      `;
    case "smile":
    default:
      return `
        <!-- Smiling Crescent Eyes -->
        <path d="M 74 69 Q 82 65 90 70" class="notion-line" stroke-width="${browWidth}" />
        <path d="M 110 70 Q 118 65 126 69" class="notion-line" stroke-width="${browWidth}" />
        
        <path d="M 76 84 C 77 77, 89 77, 90 84" class="notion-line" stroke-width="2.8" />
        <path d="M 110 84 C 111 77, 123 77, 124 84" class="notion-line" stroke-width="2.8" />
      `;
  }
}

function renderMouth(mouth: AvatarMouth, line: string, gender: AvatarGender): string {
  const nose = `<path d="M 99 87 Q 102 91 99 94" class="notion-line" stroke-width="2.2" />`;
  const lipColor = gender === "girl" ? "#fb7185" : "#f43f5e";

  let mouthSvg = "";
  switch (mouth) {
    case "talking":
      mouthSvg = `
        <path d="M 93 103 Q 100 114 107 103 Z" fill="${lipColor}" stroke="${line}" stroke-width="2.4" stroke-linejoin="round" />
        <path d="M 94 104 Q 100 106 106 104" stroke="#ffffff" stroke-width="2" stroke-linecap="round" fill="none" />
      `;
      break;
    case "grin":
      mouthSvg = `
        <path d="M 90 102 Q 100 117 110 102 Z" fill="${lipColor}" stroke="${line}" stroke-width="2.4" stroke-linejoin="round" />
        <path d="M 92 103 Q 100 106 108 103" stroke="#ffffff" stroke-width="2.2" stroke-linecap="round" fill="none" />
      `;
      break;
    case "curious":
      mouthSvg = `
        <ellipse cx="100" cy="106" rx="4.5" ry="5.5" fill="${lipColor}" stroke="${line}" stroke-width="2.4" />
      `;
      break;
    case "quiet":
      mouthSvg = `<path d="M 94 105 L 106 105" class="notion-line" stroke-width="2.4" />`;
      break;
    case "smile":
    default:
      mouthSvg = `<path d="M 93 103 Q 100 110 107 103" class="notion-line" stroke-width="2.6" />`;
      break;
  }

  return `${nose}\n${mouthSvg}`;
}

// -------------------------------------------------------------
// Front Hair (Foreground hair on forehead & crown)
// -------------------------------------------------------------
function renderFrontHair(hair: AvatarHairStyle, hairColor: string, line: string): string {
  switch (hair) {
    // ---------------- BOY HAIRS ----------------
    case "boy_dandy":
      return `
        <!-- Boy Dandy Side-part -->
        <path d="M 58 76 C 56 42, 85 28, 116 29 C 142 30, 146 54, 143 78 C 137 70, 131 66, 122 66 C 110 66, 102 73, 91 67 C 82 62, 73 70, 60 76 Z" fill="${hairColor}" stroke="${line}" stroke-width="2.8" stroke-linejoin="round" />
      `;
    case "boy_spiky":
      return `
        <!-- Boy Spiky / Sporty -->
        <path d="M 58 78 C 55 46, 75 32, 100 31 C 125 30, 145 46, 142 78 C 138 72, 132 64, 122 65 C 114 66, 108 61, 98 62 C 86 63, 80 68, 60 78 Z" fill="${hairColor}" stroke="${line}" stroke-width="2.8" stroke-linejoin="round" />
        <path d="M 82 32 L 86 22 L 94 30" fill="${hairColor}" stroke="${line}" stroke-width="2.2" />
        <path d="M 98 30 L 104 18 L 112 28" fill="${hairColor}" stroke="${line}" stroke-width="2.2" />
        <path d="M 116 30 L 122 22 L 128 32" fill="${hairColor}" stroke="${line}" stroke-width="2.2" />
      `;
    case "boy_afro":
      return `
        <!-- Global Afro Curls (Boy) -->
        <path d="M 54 80 C 46 60, 52 38, 70 28 C 84 18, 116 18, 130 28 C 148 38, 154 60, 146 80 C 138 70, 128 66, 116 66 C 102 66, 92 70, 80 66 C 68 66, 62 72, 54 80 Z" fill="${hairColor}" stroke="${line}" stroke-width="2.8" stroke-linejoin="round" />
        <circle cx="68" cy="40" r="10" fill="${hairColor}" />
        <circle cx="88" cy="28" r="11" fill="${hairColor}" />
        <circle cx="112" cy="28" r="11" fill="${hairColor}" />
        <circle cx="132" cy="40" r="10" fill="${hairColor}" />
      `;
    case "boy_wavy":
      return `
        <!-- Boy Wavy Parted -->
        <path d="M 58 76 C 55 44, 76 29, 100 29 C 124 29, 145 44, 142 76 C 135 68, 120 63, 106 68 C 96 73, 90 64, 75 64 C 65 64, 60 70, 58 76 Z" fill="${hairColor}" stroke="${line}" stroke-width="2.8" stroke-linejoin="round" />
        <path d="M 98 32 C 98 48, 104 62, 106 68" stroke="${line}" stroke-width="2.2" fill="none" />
      `;
    case "boy_curls":
      return `
        <!-- Boy Curly Perm -->
        <path d="M 58 76 C 54 58, 62 42, 74 36 C 84 30, 96 32, 104 29 C 116 26, 130 32, 138 42 C 145 52, 144 68, 142 77 C 136 70, 127 65, 117 65 C 108 65, 99 71, 88 66 C 76 60, 68 70, 58 76 Z" fill="${hairColor}" stroke="${line}" stroke-width="2.8" stroke-linejoin="round" />
        <circle cx="78" cy="38" r="7" fill="${hairColor}" />
        <circle cx="100" cy="33" r="8" fill="${hairColor}" />
        <circle cx="122" cy="36" r="7" fill="${hairColor}" />
      `;
    case "boy_fade":
      return `
        <!-- Boy Clean Fade / Crop -->
        <path d="M 60 76 C 58 46, 76 32, 100 32 C 124 32, 142 46, 140 76 C 136 70, 128 66, 100 66 C 72 66, 64 70, 60 76 Z" fill="${hairColor}" stroke="${line}" stroke-width="2.8" stroke-linejoin="round" />
        <path d="M 60 72 L 60 84" stroke="${line}" stroke-width="2" />
        <path d="M 140 72 L 140 84" stroke="${line}" stroke-width="2" />
      `;
    case "boy_cap":
      return `
        <!-- Boy Snapback Baseball Cap -->
        <path d="M 58 72 C 55 42, 75 28, 100 28 C 125 28, 145 42, 142 72 Z" fill="#3b82f6" stroke="${line}" stroke-width="2.8" stroke-linejoin="round" />
        <path d="M 54 70 C 54 70, 90 60, 146 70 C 158 72, 150 82, 138 80 L 60 76 Z" fill="#3b82f6" stroke="${line}" stroke-width="2.6" stroke-linejoin="round" />
        <circle cx="100" cy="28" r="3.5" fill="#1e293b" />
      `;
    case "boy_beanie":
      return `
        <!-- Boy Warm Beanie -->
        <path d="M 56 74 C 54 36, 76 22, 100 22 C 124 22, 146 36, 144 74 Z" fill="#f59e0b" stroke="${line}" stroke-width="2.8" stroke-linejoin="round" />
        <rect x="54" y="66" width="92" height="12" rx="4" fill="#d97706" stroke="${line}" stroke-width="2.4" />
        <circle cx="100" cy="22" r="5.5" fill="#d97706" stroke="${line}" stroke-width="2" />
      `;

    // ---------------- GIRL HAIRS ----------------
    case "girl_twintail":
    case "girl_braids":
    case "girl_ponytail":
      return `
        <!-- Girl Bangs & Top Hair -->
        <path d="M 57 76 C 54 38, 76 26, 100 26 C 124 26, 146 38, 143 76 C 137 68, 128 64, 116 68 C 104 72, 94 65, 82 66 C 70 67, 63 71, 57 76 Z" fill="${hairColor}" stroke="${line}" stroke-width="2.8" stroke-linejoin="round" />
      `;
    case "girl_wavy_long":
      return `
        <!-- Girl Long Wavy Crown & Soft Bangs -->
        <path d="M 56 76 C 52 36, 76 25, 100 25 C 124 25, 148 36, 144 76 C 138 68, 128 65, 100 65 C 72 65, 62 68, 56 76 Z" fill="${hairColor}" stroke="${line}" stroke-width="2.8" stroke-linejoin="round" />
        <path d="M 75 66 C 85 74, 95 66, 105 72" stroke="${line}" stroke-width="2" fill="none" />
      `;
    case "girl_bob":
      return `
        <!-- Girl Bob with Bangs (단발) -->
        <path d="M 54 75 C 48 95, 52 118, 66 122 C 72 124, 76 116, 68 106 L 60 78 Z" fill="${hairColor}" stroke="${line}" stroke-width="2.6" stroke-linejoin="round" />
        <path d="M 146 75 C 152 95, 148 118, 134 122 C 128 124, 124 116, 132 106 L 140 78 Z" fill="${hairColor}" stroke="${line}" stroke-width="2.6" stroke-linejoin="round" />
        <path d="M 56 76 C 52 38, 76 26, 100 26 C 124 26, 148 38, 144 76 C 138 68, 126 63, 100 63 C 74 63, 62 68, 56 76 Z" fill="${hairColor}" stroke="${line}" stroke-width="2.8" stroke-linejoin="round" />
      `;
    case "girl_curly_buns":
      return `
        <!-- Girl Afro Buns Front Bangs -->
        <path d="M 58 76 C 55 42, 76 28, 100 28 C 124 28, 145 42, 142 76 C 136 68, 124 65, 100 65 C 76 65, 64 68, 58 76 Z" fill="${hairColor}" stroke="${line}" stroke-width="2.8" stroke-linejoin="round" />
        <circle cx="80" cy="50" r="4" fill="${hairColor}" />
        <circle cx="120" cy="50" r="4" fill="${hairColor}" />
      `;
    case "girl_headband":
      return `
        <!-- Girl Headband Short -->
        <path d="M 56 76 C 52 40, 76 28, 100 28 C 124 28, 148 40, 144 76 C 138 70, 126 66, 100 66 C 74 66, 62 70, 56 76 Z" fill="${hairColor}" stroke="${line}" stroke-width="2.8" stroke-linejoin="round" />
        <path d="M 58 64 C 62 36, 138 36, 142 64" stroke="#ec4899" stroke-width="6" stroke-linecap="round" fill="none" />
        <path d="M 58 64 C 62 36, 138 36, 142 64" class="notion-line" stroke-width="2.4" />
        <polygon points="128,40 138,34 138,46" fill="#ec4899" stroke="${line}" stroke-width="2" />
        <polygon points="148,40 138,34 138,46" fill="#ec4899" stroke="${line}" stroke-width="2" />
        <circle cx="138" cy="40" r="2.8" fill="#ffffff" stroke="${line}" stroke-width="1.8" />
      `;
    case "girl_hijab":
      return `
        <!-- Global Hijab Front Wrap -->
        <path d="M 58 74 C 54 44, 76 28, 100 28 C 124 28, 146 44, 142 74 C 142 104, 130 126, 100 126 C 70 126, 58 104, 58 74 Z" fill="none" stroke="#8b5cf6" stroke-width="6" stroke-linejoin="round" />
        <path d="M 58 74 C 54 44, 76 28, 100 28 C 124 28, 146 44, 142 74 C 142 104, 130 126, 100 126 C 70 126, 58 104, 58 74 Z" class="notion-line" stroke-width="2.6" />
      `;
    default:
      return "";
  }
}

// -------------------------------------------------------------
// Accessories (Glasses, Freckles, Hairpins)
// -------------------------------------------------------------
function renderAccessory(acc: AvatarAccessory, line: string, skin: string): string {
  switch (acc) {
    case "glasses":
      return `
        <!-- Round Glasses -->
        <circle cx="82" cy="83" r="12" fill="none" stroke="${line}" stroke-width="2.6" />
        <circle cx="118" cy="83" r="12" fill="none" stroke="${line}" stroke-width="2.6" />
        <path d="M 94 83 L 106 83" class="notion-line" stroke-width="2.6" />
        <path d="M 70 82 L 62 80" class="notion-line" stroke-width="2.2" />
        <path d="M 130 82 L 138 80" class="notion-line" stroke-width="2.2" />
      `;
    case "sunglasses":
      return `
        <!-- Cool Sunglasses -->
        <rect x="70" y="74" width="25" height="18" rx="5" fill="${line}" stroke="${line}" stroke-width="2" />
        <rect x="105" y="74" width="25" height="18" rx="5" fill="${line}" stroke="${line}" stroke-width="2" />
        <path d="M 95 80 L 105 80" class="notion-line" stroke-width="3" />
        <line x1="72" y1="78" x2="88" y2="78" stroke="#ffffff" stroke-width="1.8" opacity="0.8" />
        <line x1="107" y1="78" x2="123" y2="78" stroke="#ffffff" stroke-width="1.8" opacity="0.8" />
      `;
    case "freckles":
      return `
        <!-- Cute Cheerful Freckles -->
        <circle cx="72" cy="91" r="1.2" fill="#78350f" />
        <circle cx="76" cy="94" r="1.2" fill="#78350f" />
        <circle cx="80" cy="91" r="1.2" fill="#78350f" />
        <circle cx="120" cy="91" r="1.2" fill="#78350f" />
        <circle cx="124" cy="94" r="1.2" fill="#78350f" />
        <circle cx="128" cy="91" r="1.2" fill="#78350f" />
      `;
    case "flower_clip":
      return `
        <!-- Cute Flower Clip -->
        <g transform="translate(62, 48)">
          <circle cx="0" cy="0" r="4.5" fill="#f43f5e" />
          <circle cx="-6" cy="0" r="3.5" fill="#fb7185" />
          <circle cx="6" cy="0" r="3.5" fill="#fb7185" />
          <circle cx="0" cy="-6" r="3.5" fill="#fb7185" />
          <circle cx="0" cy="6" r="3.5" fill="#fb7185" />
          <circle cx="0" cy="0" r="2" fill="#fef08a" stroke="${line}" stroke-width="1.2" />
        </g>
      `;
    case "star_pin":
      return `
        <!-- Star Pin -->
        <polygon points="68,54 70,60 76,60 71,64 73,70 68,66 63,70 65,64 60,60 66,60" fill="#facc15" stroke="${line}" stroke-width="2" stroke-linejoin="round" />
      `;
    case "hair_bow":
      return `
        <!-- Hair Ribbon Bow -->
        <polygon points="124,52 134,46 134,58" fill="#f43f5e" stroke="${line}" stroke-width="2" />
        <polygon points="144,52 134,46 134,58" fill="#f43f5e" stroke="${line}" stroke-width="2" />
        <circle cx="134" cy="52" r="3" fill="#ffffff" stroke="${line}" stroke-width="1.8" />
      `;
    case "none":
    default:
      return "";
  }
}

// -------------------------------------------------------------
// Body & Poses (Clean distinct Boy / Girl Collar details)
// -------------------------------------------------------------
function renderBodyAndPose(
  pose: AvatarPose,
  clothColor: string,
  line: string,
  skin: string,
  gender: AvatarGender,
): string {
  const isGirl = gender === "girl";

  // Distinct collar: Girl gets soft rounded peter-pan collar, Boy gets neat polo collar
  const collar = isGirl
    ? `
      <!-- Girl Rounded Peter-Pan Collar -->
      <path d="M 88 132 C 92 142, 98 142, 100 138 C 102 142, 108 142, 112 132" fill="#ffffff" stroke="${line}" stroke-width="2" stroke-linejoin="round" />
      <circle cx="100" cy="146" r="2" fill="${line}" />
    `
    : `
      <!-- Boy Polo Collar -->
      <polygon points="92,130 100,140 96,146 88,132" fill="#ffffff" stroke="${line}" stroke-width="2" stroke-linejoin="round" />
      <polygon points="108,130 100,140 104,146 112,132" fill="#ffffff" stroke="${line}" stroke-width="2" stroke-linejoin="round" />
    `;

  const torso = `
    <!-- Torso / Shirt -->
    <path d="M 68 195 C 66 156, 74 132, 92 130 L 108 130 C 126 132, 134 156, 132 195 Z" fill="${clothColor}" stroke="${line}" stroke-width="2.8" stroke-linejoin="round" />
    ${collar}
  `;

  switch (pose) {
    case "pencil":
      return `
        <!-- Pencil Pose: Left arm down, Right arm holding pencil to the side -->
        <!-- Left Arm & Hand -->
        <path d="M 72 134 C 62 148, 58 170, 60 186" stroke="${clothColor}" stroke-width="12" stroke-linecap="round" fill="none" />
        <path d="M 72 134 C 62 148, 58 170, 60 186" class="notion-line" stroke-width="2.6" />
        <circle cx="60" cy="186" r="6.5" fill="${skin}" stroke="${line}" stroke-width="2.4" />

        ${torso}

        <!-- Right Arm Bending to Side holding pencil (Safe angle away from face) -->
        <path d="M 128 134 C 142 146, 150 162, 144 175" stroke="${clothColor}" stroke-width="12" stroke-linecap="round" fill="none" />
        <path d="M 128 134 C 142 146, 150 162, 144 175" class="notion-line" stroke-width="2.6" />

        <!-- Cute Big Pencil tilted safely at side (angle 35 deg to the right) -->
        <g transform="rotate(35 152 155)">
          <rect x="146" y="118" width="10" height="38" fill="#facc15" stroke="${line}" stroke-width="2.2" rx="1" />
          <polygon points="146,118 156,118 151,104" fill="#fde047" stroke="${line}" stroke-width="2.2" stroke-linejoin="round" />
          <polygon points="149,110 153,110 151,104" fill="${line}" />
          <!-- Eraser -->
          <rect x="146" y="156" width="10" height="7" fill="#f43f5e" stroke="${line}" stroke-width="2.2" rx="2" />
          <line x1="146" y1="156" x2="156" y2="156" stroke="${line}" stroke-width="1.8" />
        </g>

        <!-- Right Hand gripping pencil at side -->
        <circle cx="148" cy="168" r="7" fill="${skin}" stroke="${line}" stroke-width="2.4" />
        <path d="M 144 165 C 148 163, 152 166, 150 170" class="notion-line" stroke-width="2" />
      `;

    case "pointing":
      return `
        <!-- Pointing Pose: Left arm down, Right arm pointing up-right -->
        <!-- Left Arm & Hand -->
        <path d="M 72 134 C 62 148, 58 170, 60 186" stroke="${clothColor}" stroke-width="12" stroke-linecap="round" fill="none" />
        <path d="M 72 134 C 62 148, 58 170, 60 186" class="notion-line" stroke-width="2.6" />
        <circle cx="60" cy="186" r="6.5" fill="${skin}" stroke="${line}" stroke-width="2.4" />

        ${torso}

        <!-- Right Arm with natural sleeve -->
        <path d="M 128 134 C 144 138, 156 132, 164 122" stroke="${clothColor}" stroke-width="12" stroke-linecap="round" fill="none" />
        <path d="M 128 134 C 144 138, 156 132, 164 122" class="notion-line" stroke-width="2.6" />

        <!-- Pointing Hand -->
        <g transform="translate(158, 108)">
          <ellipse cx="6" cy="14" rx="6.5" ry="5.5" fill="${skin}" stroke="${line}" stroke-width="2.4" />
          <rect x="3" y="0" width="5.5" height="15" rx="2.8" fill="${skin}" stroke="${line}" stroke-width="2.2" />
        </g>
      `;

    case "thinking":
      return `
        <!-- Thinking Pose: Left arm down, Right arm supporting chin -->
        <!-- Left Arm & Hand -->
        <path d="M 72 134 C 62 148, 58 170, 60 186" stroke="${clothColor}" stroke-width="12" stroke-linecap="round" fill="none" />
        <path d="M 72 134 C 62 148, 58 170, 60 186" class="notion-line" stroke-width="2.6" />
        <circle cx="60" cy="186" r="6.5" fill="${skin}" stroke="${line}" stroke-width="2.4" />

        ${torso}

        <!-- Right Arm bending up to chin -->
        <path d="M 128 134 C 140 148, 134 162, 122 138 C 118 128, 114 120, 112 118" stroke="${clothColor}" stroke-width="10" stroke-linecap="round" fill="none" />
        <path d="M 128 134 C 140 148, 134 162, 122 138 C 118 128, 114 120, 112 118" class="notion-line" stroke-width="2.6" />

        <!-- Hand gently on cheek/chin -->
        <ellipse cx="110" cy="118" rx="6" ry="5" fill="${skin}" stroke="${line}" stroke-width="2.4" />
        <path d="M 107 115 C 109 112, 113 113, 112 119" class="notion-line" stroke-width="1.8" />
      `;

    case "cheering":
      return `
        <!-- Cheering Pose: Both arms raised high -->
        <path d="M 72 134 C 54 118, 42 94, 46 80" stroke="${clothColor}" stroke-width="12" stroke-linecap="round" fill="none" />
        <path d="M 72 134 C 54 118, 42 94, 46 80" class="notion-line" stroke-width="2.6" />
        <circle cx="46" cy="76" r="7" fill="${skin}" stroke="${line}" stroke-width="2.4" />

        <path d="M 128 134 C 146 118, 158 94, 154 80" stroke="${clothColor}" stroke-width="12" stroke-linecap="round" fill="none" />
        <path d="M 128 134 C 146 118, 158 94, 154 80" class="notion-line" stroke-width="2.6" />
        <circle cx="154" cy="76" r="7" fill="${skin}" stroke="${line}" stroke-width="2.4" />

        ${torso}
      `;

    case "waving":
      return `
        <!-- Waving Pose: Left arm down, Right arm waving -->
        <path d="M 72 134 C 62 148, 58 170, 60 186" stroke="${clothColor}" stroke-width="12" stroke-linecap="round" fill="none" />
        <path d="M 72 134 C 62 148, 58 170, 60 186" class="notion-line" stroke-width="2.6" />
        <circle cx="60" cy="186" r="6.5" fill="${skin}" stroke="${line}" stroke-width="2.4" />

        ${torso}

        <path d="M 128 134 C 144 122, 158 102, 156 88" stroke="${clothColor}" stroke-width="12" stroke-linecap="round" fill="none" />
        <path d="M 128 134 C 144 122, 158 102, 156 88" class="notion-line" stroke-width="2.6" />
        <circle cx="156" cy="84" r="7" fill="${skin}" stroke="${line}" stroke-width="2.4" />
        <path d="M 166 74 C 170 80, 170 88, 166 94" class="notion-line" stroke-width="2" />
        <path d="M 172 71 C 178 80, 178 91, 172 100" class="notion-line" stroke-width="2" />
      `;

    case "standing":
    default:
      return `
        <!-- Standing Pose: Both arms down at sides naturally -->
        <path d="M 72 134 C 62 148, 58 170, 60 186" stroke="${clothColor}" stroke-width="12" stroke-linecap="round" fill="none" />
        <path d="M 72 134 C 62 148, 58 170, 60 186" class="notion-line" stroke-width="2.6" />
        <circle cx="60" cy="186" r="6.5" fill="${skin}" stroke="${line}" stroke-width="2.4" />

        <path d="M 128 134 C 138 148, 142 170, 140 186" stroke="${clothColor}" stroke-width="12" stroke-linecap="round" fill="none" />
        <path d="M 128 134 C 138 148, 142 170, 140 186" class="notion-line" stroke-width="2.6" />
        <circle cx="140" cy="186" r="6.5" fill="${skin}" stroke="${line}" stroke-width="2.4" />

        ${torso}
      `;
  }
}
