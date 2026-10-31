import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { existsSync, mkdirSync, mkdtempSync, readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { createServer } from "node:net";
import { fileURLToPath } from "node:url";
import { test } from "node:test";
import { chromium } from "playwright";

const repo = resolve(fileURLToPath(new URL("../../../..", import.meta.url)));
const python = process.env.MODU_TEST_PYTHON ?? join(repo, ".venv", process.platform === "win32" ? "Scripts/python.exe" : "bin/python");
const scratch = mkdtempSync(join(tmpdir(), "modu-teacher-browser-"));
const artifacts = join(repo, ".tmp", "teacher-browser");
mkdirSync(artifacts, { recursive: true });
const env = { ...process.env, PYTHONPATH: join(repo, "src"), PYTHONIOENCODING: "utf-8", DATABASE_URL: `sqlite:///${join(scratch, "test.sqlite3").replaceAll("\\", "/")}`, MODU_BROWSER_TEST_ROOT: scratch, MODU_PROBLEMS_ROOT: join(scratch, "problems"), MODU_GOLDEN_PROBLEMS_ROOT: join(scratch, "golden"), DJANGO_DEBUG: "false", DJANGO_ALLOWED_HOSTS: "127.0.0.1,localhost" };

function run(args) {
  return new Promise((accept, reject) => {
    const process = spawn(python, args, { cwd: repo, env, windowsHide: true });
    let output = "";
    process.stdout.on("data", value => { output += value; });
    process.stderr.on("data", value => { output += value; });
    process.on("error", reject);
    process.on("exit", code => code === 0 ? accept() : reject(new Error(output)));
  });
}

test("teacher workspace: real login, ten questions, two students, results and editor", { timeout: 180000 }, async () => {
  await run(["tests/backend/seed_teacher_browser.py"]);
  const port = await new Promise(accept => { const server = createServer(); server.listen(0, "127.0.0.1", () => { const port = server.address().port; server.close(() => accept(port)); }); });
  const base = `http://127.0.0.1:${port}`;
  const server = spawn(python, ["manage.py", "runserver", "--noreload", "--insecure", `127.0.0.1:${port}`], { cwd: repo, env, windowsHide: true });
  let serverLog = "";
  server.stdout.on("data", data => { serverLog += data; });
  server.stderr.on("data", data => { serverLog += data; });
  let browser;
  try {
    let ready = false;
    for (let i = 0; i < 60; i++) {
      try { if ((await fetch(base + "/teacher/")).ok) { ready = true; break; } } catch {}
      await new Promise(accept => setTimeout(accept, 250));
    }
    assert.ok(ready, serverLog);
    const chrome = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH ?? (process.platform === "win32" ? "C:/Program Files/Google/Chrome/Application/chrome.exe" : undefined);
    browser = await chromium.launch(chrome && existsSync(chrome) ? { executablePath: chrome, headless: true } : { headless: true });
    const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, timezoneId: "Asia/Seoul", locale: "ko-KR" });
    const page = await context.newPage();
    page.setDefaultTimeout(15000);
    const errors = [];
    page.on("pageerror", error => errors.push(error.message));
    await page.goto(base + "/teacher/");
    await page.getByLabel("아이디", { exact: true }).fill("browser_student_1");
    await page.getByLabel("비밀번호", { exact: true }).fill("browser-student-password");
    await page.getByRole("button", { name: "로그인", exact: true }).click();
    await page.getByRole("alert").filter({ hasText: "교사 또는 관리자" }).waitFor();
    await page.getByLabel("아이디", { exact: true }).fill("browser_teacher");
    await page.getByLabel("비밀번호", { exact: true }).fill("browser-teacher-password");
    await page.getByRole("button", { name: "로그인", exact: true }).click();
    await page.getByRole("heading", { name: "browser_teacher 선생님의 교실" }).waitFor();
    await page.screenshot({ path: join(artifacts, "dashboard.png"), fullPage: true });
    await page.reload();
    await page.getByRole("heading", { name: "browser_teacher 선생님의 교실" }).waitFor();
    await page.getByRole("link", { name: "문제은행", exact: true }).click();
    await page.getByRole("button", { name: "미리보기", exact: true }).first().click();
    await page.getByRole("dialog").getByRole("img", { name: "문제 캔버스 미리보기" }).waitFor();
    await page.getByRole("dialog").getByRole("button", { name: "닫기", exact: true }).click();
    await page.getByLabel("현재 페이지 전체 선택").check();
    await page.getByLabel("학년", { exact: true }).selectOption("4");
    await page.getByRole("button", { name: "검색", exact: true }).click();
    await page.getByText("검색 조건에 맞는 문제가 없습니다.").waitFor();
    await page.getByText("10문항 선택", { exact: true }).waitFor();
    await page.getByLabel("학년", { exact: true }).selectOption("3");
    await page.getByRole("button", { name: "검색", exact: true }).click();
    await page.getByRole("button", { name: "미리보기", exact: true }).first().waitFor();
    await page.getByRole("button", { name: "문제집 만들기 →", exact: true }).click();
    await page.getByLabel("문제집 이름", { exact: true }).fill("브라우저 통합 10문항");
    await page.getByRole("button", { name: "1번 문제 아래로", exact: true }).click();
    await page.getByRole("button", { name: "저장 후 과제 배정 →", exact: true }).click();
    await page.getByRole("dialog").getByRole("heading", { name: "새 과제 배정" }).waitFor();
    await page.getByLabel("과제 이름", { exact: true }).fill("두 학생 수학 과제");
    await page.getByRole("checkbox", { name: "browser_student_1", exact: true }).check();
    await page.getByRole("checkbox", { name: "browser_student_2", exact: true }).check();
    await page.getByRole("button", { name: "과제 배정하기", exact: true }).click();
    await page.getByRole("heading", { name: "학생별 학습 현황" }).waitFor();

    async function api(path, token, method = "GET", body) {
      const response = await fetch(base + "/api/v1/" + path, { method, headers: { "Content-Type": "application/json", ...(token ? { Authorization: `Token ${token}` } : {}) }, body: body === undefined ? undefined : JSON.stringify(body) });
      const data = await response.json();
      assert.ok(response.ok, JSON.stringify(data));
      return data;
    }
    for (const number of [1, 2]) {
      const { token } = await api("auth/login/", null, "POST", { username: `browser_student_${number}`, password: "browser-student-password" });
      const [assignment] = await api("student/assignments/", token);
      const detail = await api(`student/assignments/${assignment.id}/`, token);
      assert.equal(detail.items.length, 10);
      for (const item of detail.items) {
        assert.equal(item.answer, undefined);
        const index = Number(item.content.problem_id.split("_")[1]) - 1;
        const answer = number === 2 && index < 2 ? -1 : 30 + 2 * index;
        const result = await api(`student/assignments/${assignment.id}/answers/`, token, "POST", { item_id: item.id, answer, submission_key: `browser-${number}-${item.id}`, elapsed_ms: 1500 });
        assert.equal(result.is_correct, undefined);
      }
      await api(`student/assignments/${assignment.id}/submit/`, token, "POST", {});
    }
    await page.reload();
    await page.getByRole("heading", { name: "학생별 학습 현황" }).waitFor();
    assert.match(await page.locator(".metric").filter({ hasText: "전체 정답률" }).textContent(), /90%/);
    await page.getByRole("row").filter({ hasText: "browser_student_2" }).getByRole("button", { name: "상세 결과" }).click();
    await page.getByRole("dialog").getByText("오답", { exact: true }).first().waitFor();
    await page.getByRole("dialog").getByRole("button", { name: "닫기", exact: true }).click();
    await page.screenshot({ path: join(artifacts, "results.png"), fullPage: true });
    await page.getByRole("row").filter({ hasText: "browser_student_2" }).getByRole("button", { name: "오답 재배정" }).click();
    await page.getByRole("combobox", { name: "결과를 볼 과제" }).locator("option").filter({ hasText: "browser_student_2 오답 복습" }).waitFor({ state: "attached" });
    assert.equal(await page.getByRole("combobox", { name: "결과를 볼 과제" }).inputValue(), "1");
    await page.getByRole("link", { name: "학생 관리", exact: true }).click();
    await page.getByRole("button", { name: "+ 학생 등록", exact: true }).click();
    await page.getByLabel("학생 아이디", { exact: true }).fill("created_in_browser");
    await page.getByLabel("초기 비밀번호").fill("created-password-123");
    await page.getByRole("button", { name: "학생 등록하기" }).click();
    await page.getByText("created_in_browser", { exact: true }).waitFor();
    await page.getByRole("link", { name: "학급 관리", exact: true }).click();
    await page.getByRole("button", { name: "+ 학급 만들기" }).click();
    await page.getByLabel("학급 이름", { exact: true }).fill("브라우저 수학반");
    await page.getByRole("button", { name: "학급 생성하기" }).click();
    await page.getByRole("button", { name: "학급 관리하기 →" }).click();
    await page.getByLabel("담당 학생 편성", { exact: true }).selectOption({ label: "browser_student_1" });
    await page.getByRole("button", { name: "학급에 추가", exact: true }).click();
    await page.getByRole("dialog").getByText("승인", { exact: true }).waitFor();
    const invite = await page.getByLabel("학급 초대 코드", { exact: true }).inputValue();
    await api("auth/register/", null, "POST", { username: "invited_student", password: "invited-password", invite_code: invite });
    await page.getByRole("dialog").getByRole("button", { name: "닫기", exact: true }).first().click();
    await page.getByRole("button", { name: "학급 관리하기 →" }).click();
    await page.getByRole("button", { name: "가입 승인", exact: true }).click();
    await page.getByRole("row").filter({ hasText: "invited_student" }).getByText("승인", { exact: true }).waitFor();
    await page.getByRole("dialog").getByRole("button", { name: "닫기", exact: true }).first().click();
    await page.getByRole("link", { name: "문제은행", exact: true }).click();
    await page.getByRole("button", { name: "미리보기", exact: true }).first().click();
    const editor = page.getByRole("link", { name: "Konva 편집기에서 열기 ↗" });
    await page.getByRole("radio", { name: /선택한 클래스/ }).check();
    await page.getByRole("checkbox", { name: "브라우저 수학반", exact: true }).check();
    await page.getByRole("button", { name: "공개 설정 저장", exact: true }).click();
    await page.getByRole("dialog").waitFor({ state: "hidden" });
    await page.getByRole("button", { name: "미리보기", exact: true }).first().click();
    await page.getByRole("radio", { name: /선택한 클래스/ }).waitFor();
    assert.equal(await page.getByRole("radio", { name: /선택한 클래스/ }).isChecked(), true);
    await page.screenshot({ path: join(artifacts, "visibility-settings.png"), fullPage: true });
    assert.match(await editor.getAttribute("href"), /problem=ko%2Fday_01/);
    await editor.click();
    await page.waitForURL(/editor-konva/);
    await page.locator(".problem-file-row.active").filter({ hasText: "browser_01.dsl.py" }).waitFor();
    await page.locator("canvas").first().waitFor();
    await page.getByRole("link", { name: "← 교사 학습관리" }).click();
    await page.getByRole("heading", { name: "browser_teacher 선생님의 교실" }).waitFor();
    await page.setViewportSize({ width: 390, height: 844 });
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth), true);
    await page.screenshot({ path: join(artifacts, "mobile.png"), fullPage: true });
    assert.deepEqual(errors, []);
    await page.getByRole("button", { name: "로그아웃", exact: true }).click();
    await page.getByRole("heading", { name: "선생님, 반갑습니다." }).waitFor();
    await browser.close(); browser = undefined;
  } catch (error) {
    console.error(serverLog.slice(-5000));
    if (browser) { const pages = browser.contexts()[0]?.pages(); if (pages?.[0]) await pages[0].screenshot({ path: join(artifacts, "failure.png"), fullPage: true }).catch(() => {}); }
    throw error;
  } finally {
    if (browser) await browser.close();
    server.kill();
  }
});
