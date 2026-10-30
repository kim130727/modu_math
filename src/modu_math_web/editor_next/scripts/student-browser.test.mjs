import assert from "node:assert/strict";
import { existsSync, mkdirSync } from "node:fs";
import { join } from "node:path";
import { test } from "node:test";
import { chromium } from "playwright";
import { repository, startStudentFixture } from "./platform-browser-server.mjs";

test("two students solve ten questions through the real Flutter app", { timeout: 300000 }, async () => {
  const fixture = await startStudentFixture();
  const artifacts = join(repository, ".tmp", "student-browser"); mkdirSync(artifacts, { recursive: true });
  const chrome = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH ?? (process.platform === "win32" ? "C:/Program Files/Google/Chrome/Application/chrome.exe" : undefined);
  const browser = await chromium.launch(chrome && existsSync(chrome) ? { executablePath: chrome, headless: true } : { headless: true });
  let current;
  try {
    for (const student of [1, 2]) {
      const context = await browser.newContext({ viewport: { width: 1500, height: 1150 }, locale: "ko-KR", timezoneId: "Asia/Seoul" });
      const page = await context.newPage(); current = page; page.setDefaultTimeout(45000);
      const errors = []; page.on("pageerror", error => errors.push(error.message));
      const privateRequests = []; page.on("request", request => { if (/\.solvable\.|\.semantic\.json|\.renderer\.json|\.dsl\.py|assets\/generated/.test(request.url())) privateRequests.push(request.url()); });
      async function type(field, text) {
        await field.click();
        // Semantics text inputs activate their Flutter editing channel on the
        // next frame. Type real keyboard events after that focus update.
        await field.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
        await page.keyboard.press('ControlOrMeta+A');
        await page.keyboard.type(text);
      }
      await page.goto(fixture.base + "/student/");
      await page.getByRole("button", { name: "로그인 / 회원가입", exact: true }).click();
      await type(page.getByRole("textbox", { name: /아이디/ }), `browser_student_${student}`);
      await type(page.getByLabel("비밀번호", { exact: true }), "browser-student-password");
      await page.getByRole("button", { name: "로그인하기", exact: true }).click();
      await page.getByRole("button", { name: "과제 열기", exact: true }).click();
      await page.getByRole("textbox").waitFor();
      if (student === 1) await page.screenshot({ path: join(artifacts, "solve.png"), fullPage: true });
      for (let index = 0; index < 10; index++) {
        const value = student === 2 && index < 2 ? -1 : 30 + 2 * index;
        await type(page.getByRole("textbox"), String(value));
        await page.getByRole("button", { name: "답 제출", exact: true }).click();
        await page.getByText("답을 제출했어요.", { exact: true }).waitFor();
        assert.equal(await page.getByText("맞았어요!", { exact: true }).count(), 0);
        if (index < 9) await page.getByRole("button", { name: "다음 문제", exact: true }).click();
      }
      await page.getByRole("button", { name: "과제 제출하기", exact: true }).click();
      await page.getByText("수고했어요! 과제를 제출했어요.", { exact: true }).waitFor();
      await page.getByText(`${student === 1 ? 10 : 8} / 10개 정답`, { exact: true }).waitFor();
      await page.screenshot({ path: join(artifacts, `result-${student}.png`), fullPage: true });
      assert.deepEqual(privateRequests, []);
      assert.deepEqual(errors, []);
      await context.close();
    }
    async function api(path, token, body) {
      const response = await fetch(fixture.base + "/api/v1/" + path, { method: body ? "POST" : "GET", headers: { "Content-Type": "application/json", ...(token ? { Authorization: `Token ${token}` } : {}) }, body: body ? JSON.stringify(body) : undefined });
      const data = await response.json(); assert.ok(response.ok, JSON.stringify(data)); return data;
    }
    const teacher = await api("auth/login/", null, { username: "browser_teacher", password: "browser-teacher-password" });
    const [assignment] = await api("assignments/", teacher.token);
    const result = await api(`assignments/${assignment.id}/results/`, teacher.token);
    assert.equal(result.assignment.accuracy, .9);
    assert.equal(result.assignment.submitted_count, 2);
    assert.deepEqual(result.unsubmitted_recipient_ids, []);
  } catch (error) {
    if (current && !current.isClosed()) {
      await current.screenshot({ path: join(artifacts, "failure.png"), fullPage: true }).catch(() => {});
      console.error((await current.locator("body").innerText()).slice(0, 2000));
    }
    console.error(fixture.log().slice(-4500));
    throw error;
  } finally { await browser.close(); fixture.stop(); }
});
