from __future__ import annotations

import argparse
import json
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse


DEFAULT_ROOT = Path(r"C:\projects\modu_math\examples\problems")


class ProblemDevHandler(BaseHTTPRequestHandler):
    root: Path

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/problems":
            self._send_problem_list()
            return
        if parsed.path.startswith("/files/"):
            self._send_problem_file(parsed.path.removeprefix("/files/"))
            return
        self._send_json(
            {
                "ok": True,
                "endpoints": ["/api/problems", "/files/<relative-path>"],
            }
        )

    def end_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.end_headers()

    def _send_problem_list(self) -> None:
        paths = sorted(
            path.relative_to(self.root).as_posix()
            for path in self.root.rglob("*.renderer.json")
            if path.is_file()
        )
        self._send_json({"root": str(self.root), "paths": paths})

    def _send_problem_file(self, encoded_path: str) -> None:
        relative_path = unquote(encoded_path).replace("\\", "/")
        file_path = (self.root / relative_path).resolve()
        if not self._is_inside_root(file_path) or not file_path.is_file():
            self.send_error(404, "File not found")
            return

        content_type = mimetypes.guess_type(file_path.name)[0] or "text/plain"
        data = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _send_json(self, payload: dict[str, object]) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _is_inside_root(self, path: Path) -> bool:
        try:
            path.relative_to(self.root)
            return True
        except ValueError:
            return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()

    root = args.root.resolve()
    if not root.is_dir():
        raise SystemExit(f"Problem directory does not exist: {root}")

    ProblemDevHandler.root = root
    server = ThreadingHTTPServer((args.host, args.port), ProblemDevHandler)
    print(f"Serving {root} at http://{args.host}:{args.port}")
    print("Problem list: /api/problems")
    server.serve_forever()


if __name__ == "__main__":
    main()
