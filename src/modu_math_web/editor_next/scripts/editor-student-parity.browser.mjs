import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { existsSync, mkdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { chromium } from 'playwright';

// Runs against the local deployed applications. Only isolated preview grading
// receives a POST; neither student attempts nor authored content is changed.
const editor = process.env.MODU_PARITY_EDITOR_URL ?? 'http://localhost:8000';
const student = process.env.MODU_PARITY_STUDENT_URL ?? 'http://localhost:3000';
const source = process.env.MODU_PARITY_PROBLEM ?? 'ko/TS_01.초등학교 3학년_01.객관식/2학기_01단원_곱셈/S3_elem_3_008540.dsl.py';
const hash = async url => {
  const response = await fetch(url);
  assert.ok(response.ok, `Student bundle available at ${url}`);
  return createHash('sha256').update(Buffer.from(await response.arrayBuffer())).digest('hex');
};
const bundle = '/static/editor_next/student_app/main.dart.js';
assert.equal(await hash(student + bundle), await hash(editor + bundle), 'Both applications serve identical Flutter JavaScript');
const chrome = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH ?? 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const browser = await chromium.launch(existsSync(chrome) ? { executablePath: chrome } : {});
try {
  const page = await browser.newPage({ viewport: { width: 1100, height: 1000 } });
  page.setDefaultTimeout(45000);
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.goto(`${editor}/editor-konva/?problem=${encodeURIComponent(source)}`);
  await page.getByTitle(source, { exact: true }).waitFor();
  await page.getByRole('button', { name: '앱처럼 풀어보기', exact: true }).click();
  const frame = page.frameLocator('.flutter-editor-frame');
  const choice = frame.getByRole('checkbox', { name: '(3) 60 × 4', exact: true });
  await choice.waitFor();
  await frame.locator('body').evaluate(() => document.fonts.ready);
  // CanvasKit may finish loading Korean fallback glyphs after the first frame.
  await page.waitForTimeout(1000);
  const output = resolve('../../../.tmp/student-parity');
  mkdirSync(output, { recursive: true });
  await page.screenshot({ path: resolve(output, 'multiplication-preview.png'), fullPage: true });
  await choice.click();
  await frame.getByRole('button', { name: '답 제출', exact: true }).click();
  await frame.getByText('맞았어요!', { exact: true }).or(frame.getByLabel(/맞았어요/)).first().waitFor();
  assert.deepEqual(errors, []);
  console.log(`Student bundle parity, multiplication preview, and choice grading passed. Screenshot: ${output}`);
} finally {
  await browser.close();
}
