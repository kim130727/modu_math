# 조절 가능한 수채화 캐릭터

완성형 선택 탭과 기존 SVG 렌더러를 제거하고 하나의 조절 가능한 수채화 편집기로 통합했습니다.

## 에셋과 합성

- built-in image_gen으로 승인된 시안의 질감을 유지한 투명 부품 아틀라스를 생성했습니다. API/CLI 생성은 사용하지 않았습니다.
- `src/modu_math_web/editor_next/src/assets/watercolor/heads-v2.webp`: 개선된 머리 16종, 4×4 배치, 1230×1278, 약 378 KB. 이전 `heads.webp`는 비교용으로만 보관합니다.
- `src/modu_math_web/editor_next/src/assets/watercolor/bodies.webp`: 포즈 6종, 3×2 배치, 1254×1254, 약 378 KB.
- 초기 부품 다운로드는 합계 약 756 KB이며 이후 재사용합니다. 최종 출력은 384×560 WebP입니다.
- 부품 원본의 피부·머리·옷을 구분해 채색 밝기를 보존하며 지정한 색으로 바꿉니다. 코발트 외곽선·흰 옷·알파는 보존합니다.
- 얼굴/목의 피부 영역을 기준으로 머리를 정렬합니다. 아틀라스 셀 가장자리의 이웃 그림 조각은 연결된 주 실루엣만 남겨 제거합니다.
- 눈·입·소품은 Canvas 선과 곡선으로 합성합니다. 전체 이미지나 몸통을 기존 SVG로 대체하지 않습니다.
- 완성된 WebP를 data URL로 삽입해 저장·다시 불러오기·교체를 지원합니다. 말풍선은 기존 독립 도형과 텍스트로 유지합니다.
- 렌더 결과 캐시는 최대 48개이며, 미리보기 준비 중 삽입을 막고 늦게 완료된 이전 설정은 화면에 반영하지 않습니다.
- 초기 4인 완성형 WebP 파일은 참고 원본으로 남아 있지만 새 UI/빌드에서 사용하지 않습니다.

## 확인

`npm run test:avatars`: 픽셀 기준 독립 재채색, 모든 헤어/포즈/표정/소품 변화, 동일 설정 일관성, 저장·재불러오기·교체.
`npm run preview:avatars`: 실제 합성 코드를 Node Canvas로 실행해 `.tmp/watercolor-composer/preview.png` 생성.
브라우저 직접 조작은 연결 가능한 브라우저가 없어 수행하지 못했습니다.

## 얼굴·헤어 개선 (2026-09-20)

### 귀여운 비율 조정

- 얼굴 원화는 균일 배율로 확대합니다(기준 너비 126→150px, 약 19%). 큰 헤어는 캔버스 안전 여백을 우선합니다. 눈·코·입의 얼굴 내부 비율은 유지합니다.
- 몸통 세로 배율은 기존의 90%, 하체는 72%로 조정했습니다. 합성 좌표만 바꾸며 새 원화 생성이나 에셋 다운로드 추가는 없습니다.
- 턱과 목의 접합을 다시 맞추고, 생각하는 손과 들어 올린 손은 앞쪽에 그려 머리에 가려지지 않게 합니다.
- 384×560 출력으로 빈 여백을 줄였습니다. 이전에 저장한 이미지에는 소급 적용하지 않습니다.
- 16개 헤어×6개 포즈의 출력 테두리를 검사해 그림 잘림을 회귀 테스트합니다.

- 승인된 단발 소녀를 참조해 넓은 볼, 짧은 턱, 성긴 앞머리와 부드러운 머리 끝으로 16종을 다시 생성했습니다. 원본 얼굴을 그대로 복사한 것은 아닙니다.
- 얼굴 너비로 머리 배율을 맞추고, 눈 위치는 앞머리가 아닌 턱에서 계산합니다. 작은 타원 눈, 비대칭 눈썹, 짧은 미소와 옅은 볼 터치를 사용합니다. 표정은 계속 Canvas로 합성하므로 원화의 붓맛을 완전히 재현하지는 않습니다.
- 피부색 머리끈을 얼굴 정렬에서 제외하고, 셀 주변 여유 영역까지 읽은 뒤 연결된 머리만 추출해 머리 끝 잘림을 줄였습니다.
- 기본 여아는 단발, 남아는 옆가르마, 기본 눈은 다정한 작은 눈으로 설정했습니다. 기존 저장 이미지에는 소급 적용하지 않습니다.
- 피부·머리·옷 색상 및 기존 표정·포즈·소품 기능은 유지했습니다. 골든 탠 팔레트는 노랑에서 자연스러운 황갈색으로 수정했습니다.
- `node scripts/watercolor-face-preview.mjs`로 비율을 유지한 얼굴 확대 비교판을 생성합니다.
- 새 원화는 built-in image_gen으로 생성·간격 보정한 뒤 프로젝트에 WebP로 저장했습니다. 선택된 PNG: `exec-dced7ac9-513a-448d-a59d-1d0b52fa1f52.png`.

## 에셋 준비

`uv run --no-project --with pillow python tools/prepare_watercolor_layers.py SOURCE_DIR`
생성된 알파 이미지를 WebP로 재인코딩합니다. 실제 부품 선택·채색·합성은 에디터 런타임에서 처리합니다.

## 최종 생성 프롬프트

### heads

Use case: illustration-story. Create ONE production sprite atlas of 16 interchangeable watercolor children's HEADS, exact 4 columns x 4 rows evenly spaced square grid. Reference is style reference for watercolor/gouache/marker texture and cobalt outlines. TRANSPARENT ALPHA BACKGROUND, no visible grid lines, text, borders, numbers, labels. Every head has IDENTICAL front-facing blank warm peach (#efb47b) oval face with ears, NO eyes, NO nose, NO mouth, NO brows (features will be added by app). Face center is exactly x50% y57% of its cell, chin y78%, face width about 40% of cell. All hair is dark neutral CHARCOAL gray (not brown, not blue) with irregular real brush texture and paper slivers; heavy cobalt blue hand-painted outlines. Whole hairstyle fits inside each cell with margin, no overlap. No neck, no shoulders, no torso. Face skin is visibly opaque peach with subtle pigment grain. Hair styles by row, left to right: ROW 1: boy neat side-part short, boy spiky tousled, boy rounded curly afro, boy wavy side part. ROW 2: boy soft curly crop, boy fade haircut, boy baseball cap in charcoal, boy knitted beanie in charcoal. ROW 3: girl twin ponytails, girl two braids, girl high ponytail, girl long wavy hair. ROW 4: girl blunt bob with bangs, girl two curly buns, girl shoulder length hair with cobalt headband, girl charcoal hijab framing blank oval peach face. Front facing, SAME face position and same oval face shape in all cells. Charming organic painted shapes exactly like reference, NO clean vector art, no 3D. Subtle granular opaque paint, irregular pigment, hand painted cobalt single outlines. 1536x1536 square atlas. Transparent space outside heads, opaque face/hair.

### bodies

Use case: illustration-story. Create ONE production sprite atlas with exactly SIX HEADLESS child body paper-doll pieces, exact 3 columns x 2 rows grid on TRANSPARENT alpha background. No grid lines, text or labels. Reference sheet is sole style reference: beautiful textured broad gouache/marker strokes, vivid cobalt-blue hand-painted outlines, charming children's proportions. Each cell tall portrait aspect 2:3, total atlas square 1536x1536. ALL SIX have same straight front-facing torso, white/ivory pants, white sneakers with blue edges, medium CYAN turquoise (#25bbce) oversized sweater, warm peach (#efb47b) hands and short neck. NO HEAD, NO HAIR, NO FACE. Important registration: short peach neck is centered at x50% y30% of each cell, collar y34%, waist y61%, shoes y94%; reserve top 25% of each cell empty for attaching head later. Body widths similar, sweaters generous. Paint all sweaters cyan to allow recoloring, no yellow, no pink. Preserve opaque ivory pants, rich irregular paint texture and paper gaps, visible cobalt edges. ALL limbs and props within their own cell, no touching other cells. Top row left to right: holding a big BLUE AND WHITE pencil on viewer left, other hand on hip; pointing upward with viewer-right arm (finger ends near y20% of cell), other arm relaxed down; thinking with one hand at where chin would be (x55% y29%) and other arm crossing belly. Bottom row left to right: cheering with TWO raised arms with fists at cell y16%, arms clear of empty head area; waving with viewer-right hand beside missing head (x80% y25%), other arm down; standing relaxed BOTH arms down. Exactly two arms/two hands/two legs per piece, warm peach hands. Neck is a short flat peach stub, no disturbing cut detail. These are toy dress-up sprites, not real people. Center all pieces on same fixed neck and shoes registration coordinates. Only pieces and transparency, no paper rectangle, no shadow, no floor, no glow. Match approved watercolor material faithfully.
