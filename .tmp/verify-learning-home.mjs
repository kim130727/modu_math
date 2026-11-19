import assert from 'node:assert/strict';
import { chromium } from '../src/modu_math_web/editor_next/node_modules/playwright/index.mjs';

const browser = await chromium.launch({headless: true, executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe'});
try {
  const page = await browser.newPage({viewport: {width: 390, height: 844}});
  page.setDefaultTimeout(15000);
  const errors = [];
  const requests = [];
  page.on('pageerror', e => errors.push(e.message));
  await page.addInitScript(() => {
    localStorage.setItem('flutter.modu_math_auth_token_v1', '"preview-token"');
    localStorage.setItem('flutter.modu_math_auth_user_v1', JSON.stringify(JSON.stringify({id: 1, username: '학생', role: 'student'})));
  });
  await page.route('**/api/v1/**', async route => {
    const url = new URL(route.request().url());
    requests.push(url);
    console.log('API', url.pathname, url.search);
    let body = [];
    if (url.pathname === '/api/v1/problems/') body = {count: 1, results: [{id: 7, title: '공통 덧셈 연습', owner_name: '선생님', unit: '덧셈'}], previous: null, next: null};
    await route.fulfill({contentType: 'application/json; charset=utf-8', body: JSON.stringify(body)});
  });
  await page.goto(process.argv[2] ?? 'http://localhost:3000/');
  await page.getByRole('button', {name: '공개 문제', exact: true}).waitFor();
  await page.screenshot({path: '.tmp/learning-home-private.png'});
  console.log((await page.locator('body').innerText()).slice(0, 1800));
  const library = page.waitForResponse(r => new URL(r.url()).pathname === '/api/v1/problems/');
  await page.getByRole('button', {name: '공개 문제', exact: true}).click();
  console.log('After public click', (await page.locator('body').innerText()).slice(0, 1800));
  await page.screenshot({path: '.tmp/learning-home-after-click.png'});
  await library;
  await page.getByText(/공통 덧셈 연습/).waitFor();
  assert.equal(requests.find(u => u.pathname === '/api/v1/problems/').searchParams.get('scope'), 'public');
  await page.screenshot({path: '.tmp/learning-home-public.png'});
  await page.getByRole('button', {name: '내 과제', exact: true}).click();
  await page.getByRole('button', {name: '학급 가입', exact: true}).waitFor();
  await page.getByRole('button', {name: '로그아웃', exact: true}).click();
  await page.getByRole('button', {name: '로그인 / 회원가입', exact: true}).waitFor();
  assert.deepEqual(errors, []);
  console.log('390px browser: public/private navigation and logout passed.');
} finally { await browser.close(); }
