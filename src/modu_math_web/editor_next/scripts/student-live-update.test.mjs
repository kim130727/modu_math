import assert from "node:assert/strict";
import { existsSync, mkdirSync } from "node:fs";
import { join } from "node:path";
import { test } from "node:test";
import { chromium } from "playwright";
import { repository, startStudentFixture } from "./platform-browser-server.mjs";

test("saved editor builds reach the open Flutter canvas and preserve drafts until accepted", {timeout: 180000}, async () => {
  const fixture = await startStudentFixture({assignment: false});
  const chrome = "C:/Program Files/Google/Chrome/Application/chrome.exe";
  const browser = await chromium.launch(existsSync(chrome) ? {executablePath: chrome, headless: true} : {headless: true});
  const output = join(repository, ".tmp/student-live-update");
  mkdirSync(output, {recursive: true});
  const page = await browser.newPage({viewport: {width: 1440, height: 1000}});
  page.setDefaultTimeout(30000);
  async function api(path, token, body) {
    const response = await fetch(fixture.base + path, {method: body ? "POST" : "GET",
      headers: {"Content-Type": "application/json", ...(token ? {Authorization: `Token ${token}`} : {})},
      body: body ? JSON.stringify(body) : undefined});
    const data = await response.json();
    assert.ok(response.ok, JSON.stringify(data));
    return data;
  }
  try {
    const teacher = await api("/api/v1/auth/login/", null, {username: "browser_teacher", password: "browser-teacher-password"});
    const student = await api("/api/v1/auth/login/", null, {username: "browser_student_1", password: "browser-student-password"});
    await page.addInitScript(({token, user}) => {
      localStorage.setItem("flutter.modu_math_auth_token_v1", JSON.stringify(token));
      localStorage.setItem("flutter.modu_math_auth_user_v1", JSON.stringify(JSON.stringify(user)));
    }, student);
    await page.goto(fixture.base + "/student/");
    await page.getByText(/3학년/).click();
    await page.getByText(/전체 분류/).click();
    await page.getByText(/덧셈 연습 01/).click();
    const input = page.getByRole("textbox");
    await input.waitFor();
    async function edit(text, x) {
      return api("/api/editor/problems/ko/day_01/browser_01.dsl.py/layout-patch-and-build/", teacher.token, {
        format: false, fast: true, patches: [
          {target: "slot.question", op: "update", value: {text, semantic_role: "instruction"}},
          {target: "slot.answer", op: "update", value: {x}},
        ],
      });
    }
    const initial = await api("/api/v1/problems/1/?presentation=student", student.token);
    await edit("자동 반영 안내문", 560);
    await page.getByText("자동 반영 안내문", {exact: true}).waitFor();
    const current = await api("/api/v1/problems/1/?presentation=student", student.token);
    assert.notEqual(current.revision, initial.revision);
    assert.equal(current.presentation.mode, "canvas_slots");
    assert.ok(current.renderer_data.elements.some(e => e.attributes.x === 560));
    await input.click();
    await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
    await page.keyboard.type("30");
    await edit("입력 보존 안내문", 580);
    await page.getByRole("button", {name: "새 내용 적용", exact: true}).waitFor();
    await page.getByText("자동 반영 안내문", {exact: true}).waitFor();
    await page.screenshot({path: join(output, "update-preserves-draft.png")});
    await page.getByRole("button", {name: "새 내용 적용", exact: true}).click();
    await page.getByText("입력 보존 안내문", {exact: true}).waitFor();
    await input.click();
    await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
    await page.keyboard.type("30");
    await page.getByRole("button", {name: "답 제출", exact: true}).click();
    await page.getByText("맞았어요!", {exact: true}).waitFor();
    await page.screenshot({path: join(output, "updated-canvas-graded.png")});
  } catch (error) {
    await page.screenshot({path: join(output, "failure.png")}).catch(() => {});
    console.error(fixture.log().slice(-3500));
    throw error;
  } finally {await browser.close(); fixture.stop();}
});
