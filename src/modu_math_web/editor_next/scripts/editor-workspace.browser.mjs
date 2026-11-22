import assert from "node:assert/strict";
import { chromium } from "playwright";
import { existsSync, mkdirSync } from "node:fs";
import { resolve } from "node:path";

// Run against a local Vite server. API calls are isolated from real problem files.
const base = process.env.MODU_EDITOR_TEST_URL ?? "http://127.0.0.1:5174/static/editor_next/konva_assets/";
const chrome = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH ?? "C:/Program Files/Google/Chrome/Application/chrome.exe";
const browser = await chromium.launch(existsSync(chrome) ? { executablePath: chrome } : {});
const output = resolve("../../../.tmp/editor-workspace");
mkdirSync(output, { recursive: true });
try {
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  const errors = [];
  page.on("pageerror", error => { errors.push(error.message); console.error(error.message); });
  page.setDefaultTimeout(10000);
  await page.route("**/api/editor/**", route => route.fulfill({ json: { problems: [] } }));
  await page.goto(base, { waitUntil: "domcontentloaded" });
  await page.getByText("문제 스튜디오", { exact: true }).waitFor();
  const button = name => page.getByRole("button", { name, exact: true });
  assert.ok((await page.locator(".editor-toolbox").boundingBox()).height <= 92, "Header and tools occupy only two compact rows on desktop");
  assert.equal(await page.locator(".konva-question-preview").count(), 0, "An empty prompt reserves no canvas space");
  assert.ok((await button("문제 탐색").boundingBox()).width > 50, "Dock labels fit horizontally");
  for (const name of ["새파일", "저장", "저장하고 화면 반영", "문제 편집", "정답 검수", "글자", "수식", "이미지", "표", "캐릭터", "도형 추가"]) {
    assert.ok(await button(name).isVisible(), name);
  }
  await button("도형 추가").click();
  const presets = await page.locator(".shape-palette-item").count();
  assert.equal(presets, 42, "Every existing shape preset stays available");
  await page.keyboard.press("Escape");
  assert.equal(await page.locator(".shape-palette").count(), 0);
  assert.equal(await button("도형 추가").evaluate(element => element === document.activeElement), true);
  await button("수학 교구").click();
  for (const name of ["진분수", "대분수", "모눈종이", "천 모형", "백 모형", "십 모형", "일 모형"]) assert.ok(await button(name).isVisible(), name);
  await button("정답 및 파일").click();
  for (const name of ["선택 요소를 정답칸으로", "JSON 새로고침", "화면 다시 생성"]) assert.ok(await button(name).isVisible(), name);
  assert.ok(await button("선택 삭제").isDisabled());
  await button("기본 요소").click();
  await button("글자").click();
  assert.ok(await button("선택 삭제").isEnabled());
  await page.getByRole("status").filter({ hasText: "저장하지 않은 변경" }).first().waitFor();
  await page.getByRole("tab", { name: "요소 설정", exact: true }).click();
  await page.getByLabel("내용", { exact: true }).fill("직관적인 문제 편집");
  await page.getByRole("tab", { name: "JSON", exact: true }).click();
  assert.ok((await page.locator(".konva-json-panel textarea").inputValue()).includes("직관적인 문제 편집"));
  await page.getByRole("tab", { name: "힌트 편집", exact: true }).click();
  await page.getByRole("tab", { name: "요소 설정", exact: true }).click();
  await page.screenshot({ path: resolve(output, "desktop.png"), fullPage: true });
  await page.getByRole("tab", { name: "정답", exact: true }).click();
  await page.getByText("정답 만들기", { exact: true }).waitFor();
  await page.getByLabel("응답 방식", { exact: true }).selectOption("choice");
  for (let index = 1; index <= 3; index++) {
    await button("선택지 추가").click();
    await page.getByLabel(`선택지 ${index} 내용`, { exact: true }).fill([">", "=", "<"][index - 1]);
  }
  assert.ok(await button("정답 저장하고 화면 반영").isDisabled(), "Choices require a correct answer");
  await page.getByLabel("선택지 1 정답", { exact: true }).check();
  await page.getByLabel("선택지 3 정답", { exact: true }).check();
  assert.ok(await button("정답 저장하고 화면 반영").isEnabled(), "Multiple correct choices remain supported");
  assert.equal(await page.locator(".review-choice-editor.is-correct").count(), 2);
  const firstChoice = page.locator(".review-choice-editor").first();
  assert.ok((await firstChoice.boundingBox()).height < 125, "Short choices use compact rows");
  await firstChoice.locator("summary").click();
  await page.getByLabel("선택지 1 번호", { exact: true }).fill("①");
  assert.ok(await firstChoice.getByRole("button", { name: "원본 선택", exact: true }).isDisabled());
  await firstChoice.locator("summary").click();
  const answerDock = await page.locator(".answer-authoring-dock").boundingBox();
  assert.ok(answerDock.width >= 380, "Answer writing has a wider dock on desktop");
  const saveButton = await button("정답 저장하고 화면 반영").boundingBox();
  assert.ok(saveButton.y + saveButton.height <= answerDock.y + answerDock.height, "Save remains visible without scrolling");
  await page.getByText("검수 상태·메모 및 화면 편집", { exact: true }).click();
  await page.getByPlaceholder("문항의 모호함, 정답 오류, 그림 수정 사항").fill("복수 정답 확인");
  await page.getByText("검수 상태·메모 및 화면 편집", { exact: true }).click();
  await page.locator(".answer-authoring-panel").evaluate(element => { element.scrollTop = 0; });
  await page.screenshot({ path: resolve(output, "choice-authoring.png"), fullPage: true });
  for (const width of [1024, 768]) {
    await page.setViewportSize({ width, height: 900 });
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true, `Answer writing fits at ${width}px`);
    assert.ok(await button("정답 저장하고 화면 반영").isVisible());
  }
  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.getByLabel("응답 방식", { exact: true }).selectOption("panel_input");
  await page.getByLabel("답 1", { exact: true }).fill("12");
  await page.getByLabel("답 1 단위", { exact: true }).fill("cm");
  assert.ok(await button("정답 저장하고 화면 반영").isEnabled());
  await button("＋ 정답 추가").click();
  assert.ok(await button("정답 저장하고 화면 반영").isDisabled());
  await page.getByLabel("답 2", { exact: true }).fill("8");
  await page.getByLabel("응답 방식", { exact: true }).selectOption("canvas_slots");
  await button("＋ 문제에 정답 빈칸 추가").click();
  assert.equal(await page.getByLabel("답 1", { exact: true }).inputValue(), "12");
  assert.equal(await page.getByLabel("답 1 단위", { exact: true }).inputValue(), "cm");
  await page.locator(".konva-side-content > .answer-review-panel").evaluate(element => { element.scrollTop = 0; });
  await page.screenshot({ path: resolve(output, "answer-setup.png"), fullPage: true });
  await page.getByRole("tab", { name: "JSON", exact: true }).click();
  const shapeDocument = JSON.parse(await page.locator(".konva-json-panel textarea").inputValue());
  const blank = shapeDocument.shapes.find(shape => shape.id.includes("answer_blank"));
  assert.equal(blank.interaction.role, "answer");
  assert.equal(blank.interaction.answer_key_index, 0);
  assert.ok(blank.interaction.answer_ref);
  await page.getByRole("tab", { name: "요소 설정", exact: true }).click();
  await page.getByRole("combobox", { name: "정답", exact: true }).waitFor();
  const bindingLabels = await page.getByRole("combobox", { name: "정답", exact: true }).locator("option").allTextContents();
  assert.ok(bindingLabels.some(text => text.includes("12 cm")), `Answer bindings reflect unsaved values immediately: ${JSON.stringify(bindingLabels)}`);
  await button("정답 검수").click();
  await page.getByLabel("학생 답안 1", { exact: true }).fill("12");
  assert.ok(await button("정답 확인").isDisabled());
  await page.getByLabel("학생 답안 2", { exact: true }).fill("8");
  await button("정답 확인").click();
  await page.getByRole("status").filter({ hasText: "채점 일치" }).waitFor();
  await button("문제 편집").click();
  await page.getByRole("tab", { name: "정답", exact: true }).click();
  await button("＋ 문제에 정답 빈칸 추가").click();
  await page.locator(".review-answer-row").first().getByRole("button", { name: "삭제", exact: true }).click();
  assert.equal(await page.getByLabel("답 1", { exact: true }).inputValue(), "8");
  await page.getByRole("tab", { name: "JSON", exact: true }).click();
  const afterDelete = JSON.parse(await page.locator(".konva-json-panel textarea").inputValue());
  const remainingBlanks = afterDelete.shapes.filter(shape => shape.id.includes("answer_blank"));
  assert.equal(remainingBlanks.length, 1, "Deleting an answer removes only its newly created blank");
  assert.equal(remainingBlanks[0].interaction.answer_key_index, 0, "Remaining blanks retain their answer after row deletion");
  await button("정답 검수").click();
  assert.equal(await button("정답 검수").getAttribute("aria-pressed"), "true");
  await page.screenshot({ path: resolve(output, "review.png"), fullPage: true });
  await button("문제 편집").click();
  for (const width of [1024, 768]) {
    await page.setViewportSize({ width, height: 900 });
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true, `No page overflow at ${width}px`);
    assert.ok(await button("저장하고 화면 반영").isVisible());
    await page.screenshot({ path: resolve(output, `${width}.png`), fullPage: true });
  }
  // Exercise the prompt/canvas/choices layout that used to overlap at short heights.
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.getByRole("tab", { name: "JSON", exact: true }).click();
  const layoutFixture = JSON.parse(await page.locator(".konva-json-panel textarea").inputValue());
  layoutFixture.shapes = [
    { id: "prompt", type: "text", x: 20, y: 20, width: 650, fontSize: 20, text: "원의 반지름을 재어 알맞은 말을 선택하세요.", semanticRole: "question", semanticRoleSource: "inferred", sourceRegionId: "region.stem" },
    { id: "instruction", type: "text", x: 20, y: 50, width: 650, fontSize: 14, text: "맞는 보기를 골라 답하세요.", semanticRole: "instruction" },
    { id: "circle", type: "circle", x: 300, y: 230, radius: 130, stroke: "#172033", strokeWidth: 2 },
    { id: "radius", type: "line", x: 300, y: 230, points: [0, 0, 112, -66], stroke: "#172033", strokeWidth: 2 },
    { id: "answer-prompt", type: "text", x: 20, y: 420, width: 600, fontSize: 20, text: "한 원의 반지름은 모두", semanticRole: "answer_prompt" },
    ...["같습니다", "다릅니다", "알 수 없습니다", "없습니다"].map((text, index) => ({ id: `choice-${index}`, type: "text", x: 20, y: 460 + index * 30, width: 200, fontSize: 18, text, semanticRole: "choice", semanticRoleSource: "inferred", sourceRegionId: "region.choices" })),
  ];
  await page.locator(".konva-json-panel textarea").fill(JSON.stringify(layoutFixture));
  await page.getByRole("tab", { name: "요소 설정", exact: true }).click();
  const canvas = page.locator(".konva-canvas-viewport");
  const assertCanvasFits = async () => {
    await page.waitForFunction(() => {
      const cell = document.querySelector(".konva-canvas-viewport");
      const stage = cell?.querySelector(".konvajs-content");
      return cell && stage && Math.abs(stage.getBoundingClientRect().width - cell.clientWidth) <= 2 && Math.abs(stage.getBoundingClientRect().height - cell.clientHeight) <= 2;
    });
    const surface = await canvas.boundingBox();
    const answers = await page.locator(".konva-answer-prompt-preview").boundingBox();
    const panel = await page.locator(".konva-side-panel").count() ? await page.locator(".konva-side-panel").boundingBox() : null;
    const prompt = await page.locator(".konva-question-preview").boundingBox();
    assert.ok(surface.height > 150, "Canvas retains useful height");
    assert.ok(surface.y + surface.height <= answers.y + 1, "Choices never overlap the canvas");
    if (panel) {
      assert.ok(surface.x + surface.width <= panel.x, "Inspector never overlaps the canvas");
      assert.ok(Math.abs(panel.y - prompt.y) <= 1, "Inspector spans the prompt and canvas rows");
    }
  };
  for (const viewport of [{ width: 1906, height: 840 }, { width: 1440, height: 900 }, { width: 1024, height: 768 }, { width: 768, height: 900 }]) {
    await page.setViewportSize(viewport);
    await assertCanvasFits();
    assert.ok(await page.locator(".konva-question-preview .presentation-prompt-item > span:last-child").evaluateAll(elements => elements.length === 2 && elements.every(element => parseFloat(getComputedStyle(element).fontSize) >= 24)), "Question and instruction stay readable at every viewport width");
  }
  await page.setViewportSize({ width: 1440, height: 900 });
  await assertCanvasFits();
  assert.ok((await canvas.boundingBox()).height > 450, "Canvas is the main editing area even with a prompt and four choices");
  assert.ok((await page.locator(".konva-answer-prompt-preview").boundingBox()).height < 100, "Choices use a compact horizontal row");
  const dockedWidth = (await canvas.boundingBox()).width;
  await button("문제 탐색").click();
  await button("속성 패널").click();
  await assertCanvasFits();
  assert.ok((await canvas.boundingBox()).width > dockedWidth + 400, "Closing both docks expands the canvas");
  await page.getByTitle("실제 크기", { exact: true }).click();
  assert.equal(await page.locator(".canvas-zoom-controls > span").textContent(), "100%");
  await button("캔버스 확대").click();
  assert.equal(await page.locator(".canvas-zoom-controls > span").textContent(), "125%");
  await page.getByTitle("화면에 맞추기", { exact: true }).click();
  await assertCanvasFits();
  await page.screenshot({ path: resolve(output, "canvas-expanded.png"), fullPage: true });
  await button("문제 탐색").click();
  await button("속성 패널").click();
  await assertCanvasFits();
  await page.screenshot({ path: resolve(output, "canvas-layout.png"), fullPage: true });
  assert.deepEqual(errors, []);
  console.log(`Editor workspace passed: ${presets} shape presets, all tool groups, editing, JSON, hints, review, responsive layout. Screenshots: ${output}`);
} finally {
  await browser.close();
}
