import assert from 'node:assert/strict';
import { chromium } from '../src/modu_math_web/editor_next/node_modules/playwright/index.mjs';

const browser = await chromium.launch({headless: true, executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe'});
const catalog = await (await fetch('http://localhost:3000/api/v1/problems/catalog/?scope=public&language=ko')).json();
try {
  for (const width of [1440, 390]) {
    const page = await browser.newPage({viewport: {width, height: 960}});
    page.setDefaultTimeout(30000);
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    await page.addInitScript(() => {
      localStorage.setItem('flutter.modu_math_auth_token_v1', '"preview-token"');
      localStorage.setItem('flutter.modu_math_auth_user_v1', JSON.stringify(JSON.stringify({id: 1, username: '학생', role: 'student'})));
    });
    await page.route('**/api/v1/**', async route => {
      const url = new URL(route.request().url());
      let data = [];
      if (url.pathname === '/api/v1/problems/catalog/') data = catalog;
      else if (url.pathname.startsWith('/api/v1/problems/')) data = await (await fetch(url)).json();
      await route.fulfill({contentType: 'application/json; charset=utf-8', body: JSON.stringify(data)});
    });
    await page.goto('http://localhost:3000/');
    await page.getByRole('button', {name: '공개 문제', exact: true}).waitFor();
    if (width < 600) await page.mouse.wheel(0, 600);
    await page.getByText(/3학년/).waitFor();
    await page.screenshot({path: `.tmp/learning-levels-${width}.png`});
    await page.getByText(/3학년/).click();
    await page.getByText(/전체 분류/).waitFor();
    await page.screenshot({path: `.tmp/learning-categories-${width}.png`});
    await page.getByText(/전체 분류/).click();
    await page.getByRole('button', {name: '학습 시작', exact: true}).click();
    await page.getByRole('button', {name: '다음 문제', exact: true}).waitFor();
    await page.screenshot({path: `.tmp/learning-lesson-${width}.png`});
    assert.deepEqual(errors, []);
    console.log('Level → category → lesson checked:', width);
    await page.close();
  }
} finally {await browser.close();}
