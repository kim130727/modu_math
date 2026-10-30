import { spawn } from "node:child_process";
import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { createServer } from "node:net";
import { fileURLToPath } from "node:url";

export const repository = resolve(fileURLToPath(new URL("../../../..", import.meta.url)));

export async function startStudentFixture() {
  const scratch = mkdtempSync(join(tmpdir(), "modu-student-browser-"));
  const python = process.env.MODU_TEST_PYTHON ?? join(repository, ".venv", process.platform === "win32" ? "Scripts/python.exe" : "bin/python");
  const env = { ...process.env, PYTHONPATH: join(repository, "src"), PYTHONIOENCODING: "utf-8", DATABASE_URL: `sqlite:///${join(scratch, "test.sqlite3").replaceAll("\\", "/")}`, MODU_BROWSER_TEST_ROOT: scratch, MODU_PROBLEMS_ROOT: join(scratch, "problems"), MODU_GOLDEN_PROBLEMS_ROOT: join(scratch, "golden"), MODU_BROWSER_STUDENT_ASSIGNMENT: "1", DJANGO_DEBUG: "false", DJANGO_ALLOWED_HOSTS: "127.0.0.1,localhost" };
  await new Promise((accept, reject) => {
    const child = spawn(python, ["tests/backend/seed_teacher_browser.py"], { cwd: repository, env, windowsHide: true });
    let output = "";
    child.stdout.on("data", value => { output += value; }); child.stderr.on("data", value => { output += value; });
    child.on("error", reject); child.on("exit", code => code === 0 ? accept() : reject(new Error(output)));
  });
  const port = await new Promise(accept => { const probe = createServer(); probe.listen(0, "127.0.0.1", () => { const port = probe.address().port; probe.close(() => accept(port)); }); });
  const server = spawn(python, ["manage.py", "runserver", "--noreload", "--insecure", `127.0.0.1:${port}`], { cwd: repository, env, windowsHide: true });
  let log = "";
  server.stdout.on("data", data => { log += data; }); server.stderr.on("data", data => { log += data; });
  const base = `http://127.0.0.1:${port}`;
  for (let i = 0; i < 80; i++) {
    try { if ((await fetch(base + "/student/")).ok) return { base, log: () => log, stop: () => server.kill() }; } catch {}
    await new Promise(accept => setTimeout(accept, 250));
  }
  server.kill();
  throw new Error("Student fixture did not start. Build the student bundle first.\n" + log);
}
