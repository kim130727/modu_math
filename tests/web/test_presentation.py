from copy import deepcopy
import json

from modu_math_web.editor.services.presentation import structure_presentation
from test_editor_api import _setup_django


def test_roles_restore_without_classifying_diagram_labels():
    layout = {"slots": [
        {"id": "slot.q1", "kind": "text", "content": {"text": "New question"}},
        {"id": "slot.choice.1", "kind": "text", "content": {"text": "(1) New"}},
        {"id": "slot.choice.2", "kind": "text", "content": {"text": "(2) B"}},
        {"id": "slot.diagram", "kind": "text", "content": {"text": "(1) New"}},
    ]}
    semantic = {"metadata": {"question": "Old question"},
                "answer": {"choices": ["(1) Old", "(2) B"], "value": "Old"}}
    original = deepcopy((layout, semantic))
    result, updated, _ = structure_presentation(layout, semantic)
    assert updated["metadata"]["presentation_prompt"] == "New question"
    assert updated["answer"]["choices"][0]["text"] == "(1) New"
    assert updated["answer"]["value"] == "New"
    assert "semantic_role" not in result["slots"][3]["content"]
    assert (layout, semantic) == original
    assert structure_presentation(result, updated) == (result, updated, None)


def test_explicit_roles_and_deleted_prompt():
    layout = {"slots": [
        {"id": "random", "kind": "text_box", "content": {"text": "Question", "semantic_role": "question"}},
        {"id": "slot.q1", "kind": "text", "content": {"text": "Label", "semantic_role": "diagram_label"}},
    ]}
    result, semantic, _ = structure_presentation(layout, {})
    result["slots"] = result["slots"][1:]
    _, updated, _ = structure_presentation(result, semantic)
    assert updated["metadata"]["presentation_prompt"] == ""


def test_new_text_choices_replace_blank_template_placeholders():
    layout = {"slots": [
        {"id": "custom-a", "kind": "text_box", "content": {"text": "A", "semantic_role": "choice"}},
        {"id": "custom-b", "kind": "text_box", "content": {"text": "B", "semantic_role": "choice"}},
    ]}
    semantic = {"answer": {"choices": [{"id": str(i), "text": ""} for i in range(4)]}}
    _, updated, solvable = structure_presentation(layout, semantic, semantic)
    assert [c['text'] for c in updated['answer']['choices']] == ['A', 'B']
    assert updated['answer'] == solvable['answer']


def test_new_problem_edit_build_and_reopen_keep_presentation(tmp_path):
    client = _setup_django(tmp_path)
    created = client.post('/api/editor/problems/create/',
                          data=json.dumps({"problem_id": "presentation-new"}), content_type='application/json')
    assert created.status_code == 200, created.content
    response = client.post('/api/editor/problems/presentation-new/layout-patch-and-build/',
        data=json.dumps({"patches": [{"target": "slot.question", "op": "update",
                                    "value": {"text": "새로 편집한 문제입니다."}}]}),
        content_type='application/json')
    assert response.status_code == 200, response.json().get("build")
    detail = client.get('/api/editor/problems/presentation-new/').json()
    assert detail['semantic']['metadata']['question'] == '새로 편집한 문제입니다.'
    assert '알맞은 답을 구하세요.' in detail['semantic']['metadata']['presentation_prompt']
    question = next(e for e in detail['renderer']['elements'] if e.get('source_ref') == 'slot.question')
    assert question['attributes']['data-semantic-role'] == 'question'


def test_instruction_without_layout_slot_not_synthesized_into_presentation_prompt():
    layout = {"slots": [
        {"id": "slot.q_text", "kind": "text", "content": {"text": "길이가 가장 긴 선분은 어느 것인가요?"}},
    ]}
    semantic = {
        "metadata": {
            "question": "길이가 가장 긴 선분은 어느 것인가요?",
            "instruction": "도형을 보고 보기 중 맞는 선분을 고르기",
        }
    }
    _, updated, _ = structure_presentation(layout, semantic)
    assert updated["metadata"]["presentation_prompt"] == "길이가 가장 긴 선분은 어느 것인가요?"

