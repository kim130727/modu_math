import json
import tempfile
from pathlib import Path

from modu_math.semantic.models.problem import SemanticProblem
from modu_math.layout.models.canvas import LayoutCanvas
from modu_math.layout.models.node import ShapeNode, TextNode
from modu_math.pipeline.compile_problem import compile_problem_pipeline
from modu_math.editor.models.state import EditorState, EditorPan

def test_diff_pipeline():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        
        # 1. Setup Models
        semantic = SemanticProblem(problem_id="test_diff", problem_type="geometry")
        canvas = LayoutCanvas(width=400, height=300)
        nodes = [
            ShapeNode(id="circle1", shape_type="circle", x=100, y=100, properties={"r": 50, "fill": "blue"}),
            TextNode(id="text1", text="Hello", x=100, y=100)
        ]
        
        # 2. Setup Patches (simulate user moving the circle and editing text)
        patches = [
            {"target": "circle1", "op": "move", "dx": 50, "dy": 0},
            {"target": "circle1", "op": "update_style", "fill": "red"},
            {"target": "text1", "op": "edit_text", "text": "World"}
        ]
        
        # 3. Setup Editor State
        editor_state = EditorState(
            selection=["circle1"],
            zoom=1.5,
            pan=EditorPan(x=10, y=-20)
        )
        
        # 4. Run Pipeline
        out_prefix = tmp_path / "diff_test"
        compile_problem_pipeline(semantic, canvas, nodes, out_prefix, layout_patches=patches, editor_state=editor_state)
        
        # 5. Verify Output Layout JSON reflects the patch
        layout_path = out_prefix.with_suffix(".layout.json")
        assert layout_path.exists()
        
        with open(layout_path, "r", encoding="utf-8") as f:
            layout_data = json.load(f)
            
        circle_node = layout_data["nodes"][0]
        text_node = layout_data["nodes"][1]
        
        assert circle_node["x"] == 150.0  # 100 + 50
        assert circle_node["properties"]["fill"] == "red"
        assert text_node["properties"]["text"] == "World"
        
        # 6. Verify Editor State JSON
        editor_path = out_prefix.with_suffix(".editor_state.json")
        assert editor_path.exists()
        
        with open(editor_path, "r", encoding="utf-8") as f:
            state_data = json.load(f)
            
        assert state_data["selection"] == ["circle1"]
        assert state_data["zoom"] == 1.5
        assert state_data["pan"]["x"] == 10.0
        
        # 7. Verify Diff JSON
        diff_path = out_prefix.with_suffix(".layout.diff.json")
        assert diff_path.exists()
        with open(diff_path, "r", encoding="utf-8") as f:
            diff_data = json.load(f)
        assert len(diff_data["patches"]) == 3
        
        print("Diff pipeline test passed!")

if __name__ == "__main__":
    test_diff_pipeline()
