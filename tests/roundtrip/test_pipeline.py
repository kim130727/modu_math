import json
import tempfile
import shutil
from pathlib import Path
from modu_math import Problem, Rect, Circle, Text

def test_pipeline_integration():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        # 1. Build using legacy DSL
        p = Problem()
        p.problem_id = "test_0001"
        p.problem_type = "addition_word_problem"
        p.set_metadata({"difficulty": 3})
        p.set_domain({
            "profile": "addition_word_problem",
            "context": "apples",
            "question": "How many apples?",
            "operands": [2, 3],
            "operation": "add",
            "objects": [],
            "relations": []
        })
        
        p.set_canvas(width=400, height=300, background="#ffffff")
        p.add(Rect(id="bg", x=0, y=0, width=400, height=300, fill="#ffffff"))
        p.add(Circle(id="c1", cx=200, cy=150, r=50, fill="red"))
        p.add(Text(id="t1", x=200, y=150, text="5", font_size=24))

        # 2. Run pipeline (save)
        out_prefix = tmp_path / "test_out"
        p.save(out_prefix)

        # 3. Verify Semantic JSON
        semantic_path = out_prefix.with_suffix(".semantic.json")
        assert semantic_path.exists(), "semantic.json was not generated"
        with open(semantic_path, "r", encoding="utf-8") as f:
            semantic_data = json.load(f)
            
        assert semantic_data["problem_id"] == "test_0001"
        assert semantic_data["domain"]["operation"] == "add"
        # Ensure layout details did not leak into semantic
        assert "canvas" not in semantic_data
        assert "elements" not in semantic_data
        
        # 4. Verify Layout JSON
        layout_path = out_prefix.with_suffix(".layout.json")
        assert layout_path.exists(), "layout.json was not generated"
        with open(layout_path, "r", encoding="utf-8") as f:
            layout_data = json.load(f)
            
        assert layout_data["problem_id"] == "test_0001"
        assert layout_data["canvas"]["width"] == 400
        assert layout_data["canvas"]["height"] == 300
        assert len(layout_data["nodes"]) == 3
        assert layout_data["nodes"][1]["type"] == "shape"
        assert layout_data["nodes"][1]["properties"]["shape_type"] == "circle"

        # 5. Verify Renderer JSON
        renderer_path = out_prefix.with_suffix(".renderer.json")
        assert renderer_path.exists(), "renderer.json was not generated"
        with open(renderer_path, "r", encoding="utf-8") as f:
            renderer_data = json.load(f)

        assert renderer_data["problem_id"] == "test_0001"
        assert renderer_data["view_box"]["width"] == 400
        assert renderer_data["view_box"]["height"] == 300
        assert len(renderer_data["elements"]) == 3
        assert renderer_data["elements"][1]["type"] == "circle"
        assert renderer_data["elements"][2]["type"] == "text"
        assert renderer_data["elements"][2]["text"] == "5"

        # 6. Verify SVG
        svg_path = out_prefix.with_suffix(".svg")
        assert svg_path.exists(), "svg was not generated"
        svg_text = svg_path.read_text(encoding="utf-8")
        assert "viewBox=\"0 0 400 300\"" in svg_text
        assert "<circle" in svg_text
        assert "<text" in svg_text
        assert ">5</text>" in svg_text
        
        print("All tests passed!")

if __name__ == "__main__":
    test_pipeline_integration()
