import json

from test_editor_api import _setup_django


def test_hint_editor_save_build_reopen_and_delete(tmp_path):
    client = _setup_django(tmp_path)
    problem_id = "hint-editor-test"
    response = client.post('/api/editor/problems/create/', data=json.dumps({'problem_id': problem_id}), content_type='application/json')
    assert response.status_code == 200, response.content
    flow = [{'step_id': 'hint.b', 'phase': 'hint', 'text': '그림을 살펴보세요.', 'title': '관찰', 'frames': [{'id': 'hint.b.1', 'overlays': []}]},
            {'step_id': 'hint.a', 'phase': 'hint', 'text': '차이를 비교하세요.', 'frames': [{'id': 'hint.a.1', 'overlays': []}]}]
    for expected in (flow, list(reversed(flow)), []):
        response = client.post(f'/api/editor/problems/{problem_id}/tutor-flow/', data=json.dumps({'tutor_flow': expected, 'format': False}), content_type='application/json')
        assert response.status_code == 200, response.content
        payload = response.json()
        assert payload['ok'], response.content
        assert payload['built'], response.content
        assert payload['artifacts']['renderer'].get('tutor_flow', []) == expected
        detail = client.get(f'/api/editor/problems/{problem_id}/').json()
        assert detail['renderer'].get('tutor_flow', []) == expected


def test_hint_editor_can_save_without_build_for_batch_workflows(tmp_path):
    client = _setup_django(tmp_path)
    problem_id = "hint-editor-no-build"
    response = client.post('/api/editor/problems/create/', data=json.dumps({'problem_id': problem_id}), content_type='application/json')
    assert response.status_code == 200, response.content

    flow = [{'step_id': 'hint.1', 'phase': 'hint', 'text': '먼저 수를 살펴보세요.'}]
    response = client.post(
        f'/api/editor/problems/{problem_id}/tutor-flow/',
        data=json.dumps({'tutor_flow': flow, 'build': False}),
        content_type='application/json',
    )

    assert response.status_code == 200, response.content
    assert response.json()['built'] is False
    assert response.json()['artifacts'] == {}
