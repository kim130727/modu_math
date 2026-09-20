# 얼굴·헤어 v2 생성 프롬프트

방식: built-in image_gen (CLI/API 미사용).
참조: 승인된 단발 소녀 `exec-6a946ed4-ca42-4fcc-ba63-0c0a4e0b9f70.png`.
저장: `src/modu_math_web/editor_next/src/assets/watercolor/heads-v2.webp`.

## 원화 생성

Use case: illustration-story. Create a transparent production sprite atlas of sixteen children's heads, 4 columns x 4 rows. Reference image's GIRL FACE AND HAIR are the exact aesthetic target, NOT generic avatar graphics. Heads only, no neck or body. Broad, squashy cheek silhouette, short shallow chin, small ears close to cheek level. Each face including ears is much wider than tall, width:height 1.55:1, NOT egg-shaped, NO tall oval faces. Gentle asymmetry. Keep forehead low under loose fringe. Each head with BLANK warm peach skin (#efb47b) for app expressions: NO eyes, nose, mouth, eyebrows, blush. Preserve pigment flecks and broad watercolor-marker swaths on skin.
Hair composed of a few big flowing opaque CHARCOAL gray marker swaths with visible paper gaps, coarse loose paint. Not individual strands, not smooth shading, not curls made of small loops. Wobbly thick cobalt single-pass contours. Source girl's bob-like shape especially for bottom-left: wide soft chin-length bob, off-center part, just three uneven forehead fringe strokes, face nestled INSIDE the curving hair. Avoid straight doll bangs. Naive editorial illustration, not stock vector avatar, not polished clipart.
Every head within equal square cell, transparent gutter at least 7% cell width on all sides. Face including ears width 54% of cell, height35%; cheek baseline y64%, chin y76%. Hair may extend to y88% but never cross cell. Fixed face placement.
Rows left-to-right: (1) boy tousled sidepart short; boy soft spiky; boy rounded broad-scalloped afro; boy swept wavy.
(2) boy soft curly crop; boy fade; boy charcoal cap; boy charcoal beanie.
(3) girl loose twin ponytails; girl chunky braids; girl high ponytail; girl long loose waves.
(4) girl soft sweeping bob MATCHING SOURCE; girl two curly buns; girl wavy bob with cobalt headband; girl charcoal hijab.
Exactly16. True transparent alpha, no background/glow/shadow/checkerboard/text/grid. Hair all warm-neutral charcoal so app can recolor; skin all opaque warm peach. Broad chunky brush coloring with small white gaps, match charming imperfect source. Prioritize SHORT WIDE CHEEKS and spacious curved hair silhouettes.

## 부품 간격 보정

Use case: precise-object-edit. Edit this production 4x4 sprite atlas ONLY to fix spacing and cell alignment. Preserve all 16 individual heads' exact designs, wide short cheek face shapes, hair shapes, brush textures, palette and blank faces unchanged. Place each head wholly inside one equal cell of a strict 4-column 4-row grid. Scale down each whole head uniformly just enough to leave at least 10% empty transparent margin on EVERY side of EVERY cell, especially twin ponytails, bob and long waves which currently cross into neighboring cells. Do not crop hair. Keep face centers horizontally at the cell center, chin at 73% cell height; long hair below chin can end at90%. Do not add facial features. No necks. No visible grid lines, labels, borders, glow, shadows, background. True transparent alpha background. Charcoal hair, peach skin, cobalt contours, warm-white paint gaps INSIDE heads remain opaque. Exactly16 heads in same row-major order. All subjects must be separated by clear transparent gutters.
