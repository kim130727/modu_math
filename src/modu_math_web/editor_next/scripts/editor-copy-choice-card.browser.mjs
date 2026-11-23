import assert from "node:assert/strict";
import { existsSync } from "node:fs";
import { chromium } from "playwright";

// This exercise stays in a browser draft and does not save the pasted box.
const base = process.env.MODU_PARITY_EDITOR_URL ?? "http://localhost:8000";
const problem = "ko/TS_01.초등학교 3학년_01.객관식/1학기_03단원_나눗셈/S3_초등_3_009138.dsl.py";
const chrome = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH
  ?? "C:/Program Files/Google/Chrome/Application/chrome.exe";
const browser = await chromium.launch(existsSync(chrome) ? { executablePath: chrome } : {});

try {
  const page = await browser.newPage({ viewport: { width: 1360, height: 1000 } });
  await page.goto(`${base}/editor-konva/?problem=${encodeURIComponent(problem)}`);
  const ids = ["slot.choice.option_0", "slot.choice.option_1"];
  await page.waitForFunction((ids) => {
    const stage = window.Konva?.stages[0];
    return stage && ids.every((id) => stage.findOne((node) => node.id() === id)?.isVisible());
  }, ids);
  const click = await page.evaluate(() => {
    const stage = window.Konva.stages[0];
    const box = stage.findOne((node) => node.id() === "slot.diagram.choice_frame");
    const rect = box.getClientRect({ relativeTo: stage });
    const surface = stage.content.getBoundingClientRect();
    return { x: surface.left + rect.x + 6, y: surface.top + rect.y + 6 };
  });
  await page.mouse.click(click.x, click.y);
  await page.keyboard.press("Control+c");
  await page.keyboard.press("Control+v");
  await page.getByText("Pasted 1 shape(s).", { exact: true }).first().waitFor({ state: "attached" });
  const result = await page.evaluate((ids) => {
    const stage = window.Konva.stages[0];
    const background = stage.find(
      (node) => node.getClassName() === "Rect" && node.id().includes("_paste_")
    ).at(-1);
    return ids.map((id) => {
      const node = stage.findOne((item) => item.id() === id);
      return Boolean(background && node?.isVisible() && node.zIndex() > background.zIndex());
    });
  }, ids);
  assert.deepEqual(result, [true, true], "Both expressions remain visible above the pasted background");
  console.log("Both division choices remain visible above a pasted card in the editor draft.");
} finally {
  await browser.close();
}
