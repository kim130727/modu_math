import assert from 'node:assert/strict';
import { existsSync, mkdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { chromium } from 'playwright';

// Exercises the real saved problem without changing its source or student records.
const base = process.env.MODU_PARITY_EDITOR_URL ?? 'http://localhost:8000';
const source = 'ko/TS_01.초등학교 3학년_01.객관식/1학기_01단원_덧셈과 뺄셈/P3_1_01_00040_00472.dsl.py';
const chrome = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH ?? 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const browser = await chromium.launch(existsSync(chrome) ? { executablePath: chrome } : {});
try {
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  page.setDefaultTimeout(45000);
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.goto(`${base}/editor-konva/?problem=${encodeURIComponent(source)}`);
  await page.getByTitle(source, { exact: true }).waitFor();
  await page.getByRole('button', { name: '앱처럼 풀어보기', exact: true }).click();
  const frame = page.frameLocator('.flutter-editor-frame');
  const field = frame.getByRole('textbox');
  await field.waitFor();
  await field.click();
  const settle = () => field.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
  await settle();
  await page.keyboard.type('1124');
  await settle();
  assert.equal(await field.inputValue(), '1124', 'Typing retains all four digits');
  await page.keyboard.press('ControlOrMeta+A');
  await page.keyboard.insertText('123456789');
  await settle();
  assert.equal(await field.inputValue(), '123456789', 'Pasted longer answers are not truncated');
  await page.keyboard.press('ControlOrMeta+A');
  await page.keyboard.insertText('1124');
  await settle();
  const grading = page.waitForResponse(response => response.url().endsWith('/student-preview/') && response.request().method() === 'POST');
  await frame.getByRole('button', { name: '답 제출', exact: true }).click();
  assert.equal((await (await grading).json()).correct, true, '1124 reaches the real server grader');
  await frame.getByText('맞았어요!', { exact: true }).or(frame.getByLabel(/맞았어요/)).first().waitFor();
  const output = resolve('../../../.tmp/answer-capacity');
  mkdirSync(output, { recursive: true });
  await page.screenshot({ path: resolve(output, '1124-accepted.png'), fullPage: true });
  assert.deepEqual(errors, []);
  console.log(`1124 typing, longer paste, and server grading passed. Screenshot: ${output}`);
} finally {
  await browser.close();
}
