from __future__ import annotations

import re
import subprocess
import sys
import unittest
from pathlib import Path

from PIL import Image, ImageChops


REPO_ROOT = Path(__file__).resolve().parents[1]


class RegressionRenderTests(unittest.TestCase):
    def test_problem_0001_regression(self) -> None:
        self._run_and_compare(
            problem_id="0001",
            scene_class="TimeConversionProblem",
            rendered_png=REPO_ROOT / "problem" / "0001" / "manim" / "images" / "TimeConversionProblem_ManimCE_v0.20.1.png",
        )

    def test_problem_0002_regression(self) -> None:
        self._run_and_compare(
            problem_id="0002",
            scene_class="RulerEraserProblem",
            rendered_png=REPO_ROOT / "problem" / "0002" / "manim" / "images" / "RulerEraserProblem_ManimCE_v0.20.1.png",
        )

    def _run_and_compare(self, problem_id: str, scene_class: str, rendered_png: Path) -> None:
        script = REPO_ROOT / "problem" / problem_id / "manim" / f"{problem_id}_manim.py"
        problem_dir = REPO_ROOT / "problem" / problem_id

        baseline_svg = problem_dir / "baseline" / "semantic.svg"
        baseline_png = problem_dir / "baseline" / "scene.png"

        self.assertTrue(baseline_svg.exists(), f"missing baseline svg: {baseline_svg}")
        self.assertTrue(baseline_png.exists(), f"missing baseline png: {baseline_png}")

        subprocess.run([sys.executable, str(script), "--all"], check=True, cwd=REPO_ROOT)
        subprocess.run([sys.executable, "-m", "manim", "-ql", "-s", str(script), scene_class], check=True, cwd=REPO_ROOT)

        rendered_svg = problem_dir / "svg" / "semantic.svg"
        self.assertTrue(rendered_svg.exists(), f"rendered svg missing: {rendered_svg}")
        self.assertTrue(rendered_png.exists(), f"rendered png missing: {rendered_png}")

        self.assertEqual(
            _normalize_svg(rendered_svg.read_text(encoding="utf-8")),
            _normalize_svg(baseline_svg.read_text(encoding="utf-8")),
            f"svg regression detected for problem {problem_id}",
        )

        rendered_image = Image.open(rendered_png).convert("RGBA")
        baseline_image = Image.open(baseline_png).convert("RGBA")

        self.assertEqual(rendered_image.size, baseline_image.size, "png size mismatch")
        diff = ImageChops.difference(rendered_image, baseline_image)
        self.assertIsNone(diff.getbbox(), f"png regression detected for problem {problem_id}")


def _normalize_svg(svg: str) -> str:
    # Remove line-to-line spacing noise while preserving meaningful text content.
    svg = svg.replace("\r\n", "\n")
    svg = re.sub(r">\s+<", "><", svg)
    return svg.strip()


if __name__ == "__main__":
    unittest.main()
