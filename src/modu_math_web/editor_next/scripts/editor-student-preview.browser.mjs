import assert from 'node:assert/strict';
import { existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { chromium } from 'playwright';

// Use a static server for editor_next so this exercises the built Flutter iframe.
const base = process.env.MODU_EDITOR_TEST_URL ?? 'http://127.0.0.1:5189/static/editor_next/konva_assets/';
const chrome = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH ?? 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const browser = await chromium.launch(existsSync(chrome) ? { executablePath: chrome } : {});
const output = resolve('../../../.tmp/editor-student-preview');
mkdirSync(output, { recursive: true });
let page;
try {
  page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  page.setDefaultTimeout(60000);
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.addInitScript(() => {
    window.previewMessages = [];
    window.addEventListener('message', event => window.previewMessages.push({ type: event.data?.type, problemId: event.data?.problem?.problem_id, origin: event.origin, fromParent: event.source === window.parent }));
  });
  let fail = false;
  let loads = 0;
  const writes = [];
  await page.route('**/api/**', async route => {
    const request = route.request();
    if (request.method() !== 'GET') writes.push(request.url());
    const url = new URL(request.url());
    if (url.pathname.startsWith('/api/editor/problems/') && url.pathname !== '/api/editor/problems/') {
      loads++;
      if (fail) return route.fulfill({ status: 500, json: { error: 'Preview fixture unavailable' } });
      const id = decodeURIComponent(url.pathname.slice('/api/editor/problems/'.length).replace(/\/$/, ''));
      return route.fulfill({ json: {
        problem_id: id, base_dir: '', dsl: '', svg: null,
        semantic: { problem_id: id, problem_type: 'addition', metadata: { title: '저장된 미리보기 문제', instruction: '2 + 3을 계산하세요.' }, answer: { value: '5' } },
        solvable: { problem_id: id, answer: { value: '5' } }, layout: {},
        renderer: { problem_id: id, view_box: { x: 0, y: 0, width: 600, height: 200 }, elements: [{ id: 'sum', type: 'text', text: '2 + 3 = ?', attributes: { x: 40, y: 70, font_size: 32 } }] },
      } });
    }
    return route.fulfill({ json: { problems: [] } });
  });
  await page.goto(base);
  await page.getByRole('button', { name: '글자', exact: true }).click();
  await page.getByRole('tab', { name: 'JSON', exact: true }).click();
  const draft = await page.locator('.konva-json-panel textarea').inputValue();
  const storageBefore = await page.evaluate(() => JSON.stringify(localStorage));
  await page.getByRole('button', { name: '앱처럼 풀어보기', exact: true }).click();
  await page.getByRole('dialog').waitFor();
  const frame = page.frameLocator('.flutter-editor-frame');
  await frame.locator('flutter-view').waitFor();
  await frame.locator('flt-semantics-placeholder').evaluate(element => element.click());
  await page.screenshot({ path: resolve(output, 'loaded.png'), fullPage: true });
  await frame.getByText('2 + 3을 계산하세요.', { exact: true }).waitFor();
  assert.equal(await frame.getByText('요소 편집', { exact: true }).count(), 0);
  assert.ok(await frame.getByRole('textbox').count() > 0, 'Flutter answer input is available');
  const answer = frame.getByRole('textbox').first();
  await answer.click();
  await answer.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
  await page.keyboard.type('5');
  await page.keyboard.press('Enter');
  await frame.getByText('맞아요! 다음 문제로 넘어가도 좋아요.', { exact: true }).waitFor();
  await page.screenshot({ path: resolve(output, 'solve.png'), fullPage: true });
  await page.getByRole('button', { name: '편집으로 돌아가기', exact: true }).click();
  assert.equal(await page.locator('.konva-json-panel textarea').inputValue(), draft, 'Unsaved editor state survives preview');
  assert.equal(await page.evaluate(() => JSON.stringify(localStorage)), storageBefore, 'Preview does not persist progress');
  fail = true;
  await page.getByRole('button', { name: '앱처럼 풀어보기', exact: true }).click();
  await page.getByRole('alert').waitFor();
  fail = false;
  await page.getByRole('button', { name: '다시 시도', exact: true }).click();
  await page.locator('.flutter-editor-frame').waitFor();
  await page.getByRole('button', { name: '편집으로 돌아가기', exact: true }).click();
  assert.equal(loads, 3, 'Every opening/retry reloads the saved problem');
  assert.deepEqual(writes, [], 'Preview never saves edits or submits student attempts');
  assert.deepEqual(errors, []);
  console.log(`Flutter student preview passed. Screenshot: ${output}`);
} catch (error) {
  if (page) {
    await page.screenshot({ path: resolve(output, 'failure.png'), fullPage: true });
    const frame = page.frames().find(frame => frame.url().includes('studentPreview=1'));
    if (frame) {
      writeFileSync(resolve(output, 'failure.html'), await frame.content());
      console.log('Preview messages:', await frame.evaluate(() => window.previewMessages));
    }
  }
  throw error;
} finally {
  await browser.close();
}
