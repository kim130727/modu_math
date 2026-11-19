import assert from 'node:assert/strict';
import { chromium } from '../src/modu_math_web/editor_next/node_modules/playwright/index.mjs';

const browser = await chromium.launch({headless: true, executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe'});
try {
  const page = await browser.newPage({viewport: {width: 1440, height: 900}});
  page.setDefaultTimeout(30000);
  await page.route(/^https:\/\/fonts\.(googleapis|gstatic)\.com\//, route => route.abort());
  await page.route('**/api/editor/**', route => route.fulfill({json: {problems: []}}));
  await page.goto('http://127.0.0.1:8000/static/editor_next/konva_assets/index.html', {waitUntil: 'domcontentloaded'});
  await page.getByRole('button', {name: '글자', exact: true}).click();
  await page.getByRole('tab', {name: '요소 설정', exact: true}).click();
  await page.getByLabel('내용', {exact: true}).fill('532 ○ 248+274');
  await page.getByRole('tab', {name: 'JSON', exact: true}).click();
  const field = page.locator('.konva-json-panel textarea');
  const doc = JSON.parse(await field.inputValue());
  const expression = {...doc.shapes.at(-1), x: 100, y: 100, width: 300, height: 50, text: '532 ○ 248+274'};
  const instruction = {...expression, id: 'layout-instruction', semanticRole: 'instruction', x: 0, y: 0, width: 600, text: '크기를 비교하여 ○ 안에 >, =, <를 알맞게 써넣으시오.'};
  await field.fill(JSON.stringify({...doc, shapes: [instruction, expression]}));
  await page.getByRole('tab', {name: '요소 설정', exact: true}).click();
  await page.getByTitle('화면에 맞추기', {exact: true}).click();
  await page.screenshot({path: '.tmp/canvas-editor-layout.png'});
  const zoom = parseInt(await page.locator('.canvas-zoom-controls > span').textContent());
  assert.ok(zoom > 250, `Compact artwork should fill the canvas beyond the old 250% cap: ${zoom}`);
  console.log('Editor fitted zoom:', zoom);
  const detailResponse = await fetch('http://localhost:3000/api/v1/problems/61/');
  assert.ok(detailResponse.ok);
  const detail = await detailResponse.json();
  for (const width of [1893, 390]) {
    const student = await browser.newPage({viewport: {width, height: 844}});
    student.setDefaultTimeout(30000);
    await student.addInitScript(() => {
      localStorage.setItem('flutter.modu_math_auth_token_v1', '"preview-token"');
      localStorage.setItem('flutter.modu_math_auth_user_v1', JSON.stringify(JSON.stringify({id: 1, username: '학생', role: 'student'})));
    });
    await student.route('**/api/v1/**', async route => {
      const url = new URL(route.request().url());
      let body = [];
      if (url.pathname === '/api/v1/problems/') body = {results: [{id: 61, title: '두 가족이 캔 고구마의 수', owner_name: '선생님'}], next: null, previous: null};
      if (url.pathname === '/api/v1/problems/61/') body = detail;
      await route.fulfill({contentType: 'application/json; charset=utf-8', body: JSON.stringify(body)});
    });
    await student.goto('http://localhost:3000/');
    await student.getByRole('button', {name: '공개 문제', exact: true}).click();
    await student.getByText(/두 가족이 캔 고구마의 수/).click();
    await student.getByRole('button', {name: '답 제출', exact: true}).waitFor();
    await student.screenshot({path: `.tmp/canvas-student-${width}.png`});
    console.log('Student layout checked:', width);
    await student.close();
  }
} finally {await browser.close();}
