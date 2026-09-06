import { readFileSync, readdirSync } from "node:fs";
import { resolve, extname } from "node:path";
import { fileURLToPath } from "node:url";
import ts from "typescript";

// Parse literals, rather than searching raw code: ?? and ?. are valid operators.
export function textEncodingErrors(bytes, filename) {
  let source;
  try {
    source = new TextDecoder("utf-8", { fatal: true }).decode(bytes);
  } catch {
    return [`${filename}: invalid UTF-8`];
  }
  const errors = [];
  if (source.includes("\uFFFD")) errors.push(`${filename}: Unicode replacement character`);
  const check = (text, line) => {
    if (/(?:\?\s*){2,}/u.test(text)) {
      errors.push(`${filename}:${line}: suspicious question marks in text: ${JSON.stringify(text)}`);
    }
  };
  if (extname(filename) === ".json") {
    const visit = (value) => {
      if (typeof value === "string") check(value, 1);
      else if (value && typeof value === "object") Object.values(value).forEach(visit);
    };
    visit(JSON.parse(source));
  } else if (/\.[jt]sx?$/.test(filename)) {
    const file = ts.createSourceFile(filename, source, ts.ScriptTarget.Latest, true);
    const visit = (node) => {
      if (ts.isStringLiteral(node) || ts.isNoSubstitutionTemplateLiteral(node) ||
          ts.isTemplateHead(node) || ts.isTemplateMiddle(node) || ts.isTemplateTail(node) || ts.isJsxText(node)) {
        check(node.text, file.getLineAndCharacterOfPosition(node.getStart(file)).line + 1);
      }
      ts.forEachChild(node, visit);
    };
    visit(file);
  }
  return errors;
}

export function checkSourceTree(directory) {
  const errors = [];
  for (const entry of readdirSync(directory, { withFileTypes: true })) {
    if (entry.name === "node_modules" || entry.name === "mathjax" || entry.name === "mathjax-newcm") continue;
    const filename = resolve(directory, entry.name);
    if (entry.isDirectory()) errors.push(...checkSourceTree(filename));
    else if (/\.(?:[jt]sx?|json|css|html)$/.test(filename)) {
      errors.push(...textEncodingErrors(readFileSync(filename), filename));
    }
  }
  return errors;
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const target = process.argv[2]
    ? resolve(process.cwd(), process.argv[2])
    : fileURLToPath(new URL("../src", import.meta.url));
  const errors = checkSourceTree(target);
  if (errors.length) {
    console.error(errors.join("\n"));
    process.exitCode = 1;
  } else {
    console.log(`Text encoding check passed for ${target}.`);
  }
}
