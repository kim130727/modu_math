from copy import deepcopy

import libcst as cst

from .dsl_patch import TutorRendererFlowUpdater
from .problems import resolve_problem_paths


def normalize_choice_groups(groups):
    if not isinstance(groups, list):
        raise ValueError('소문항은 목록이어야 합니다.')
    result = []
    ids = set()
    for group in groups:
        if not isinstance(group, dict):
            raise ValueError('소문항 형식이 올바르지 않습니다.')
        identity = group.get('id')
        label = group.get('label')
        choices = group.get('choices')
        correct = group.get('correct_index')
        if not isinstance(identity, str) or not identity.strip() or identity in ids:
            raise ValueError('소문항 ID는 비어 있지 않고 서로 달라야 합니다.')
        if not isinstance(label, str) or not label.strip():
            raise ValueError('각 소문항의 질문을 입력하세요.')
        if not isinstance(choices, list) or len(choices) < 2 or any(not isinstance(c, str) or not c.strip() for c in choices):
            raise ValueError('선택지를 두 개 이상 입력하세요.')
        choices = [c.strip() for c in choices]
        if len(set(choices)) != len(choices):
            raise ValueError('한 소문항 안의 선택지는 서로 달라야 합니다.')
        if type(correct) is not int or not 0 <= correct < len(choices):
            raise ValueError('각 소문항의 정답을 선택하세요.')
        refs = group.get('source_refs', [])
        if not isinstance(refs, list) or any(not isinstance(ref, str) for ref in refs):
            raise ValueError('원본 문장 연결이 올바르지 않습니다.')
        result.append({'id': identity, 'label': label.strip(), 'choices': choices, 'correct_index': correct, 'source_refs': refs})
        ids.add(identity)
    return result


def save_choice_groups(problem_id, groups):
    groups = normalize_choice_groups(groups)
    paths = resolve_problem_paths(problem_id)
    module = cst.parse_module(paths.dsl_path.read_text(encoding='utf-8'))
    updater = TutorRendererFlowUpdater(groups, variable_name='EDITOR_CHOICE_GROUPS')
    paths.dsl_path.write_text(module.visit(updater).code, encoding='utf-8')
    return groups


def apply_choice_groups(semantic, solvable, groups):
    groups = normalize_choice_groups(groups)
    if not groups:
        return semantic, solvable
    answer = {'type': 'choice', 'choice_groups': groups,
              'value': ', '.join(group['choices'][group['correct_index']] for group in groups), 'unit': ''}
    semantic, solvable = deepcopy((semantic, solvable))
    semantic['answer'] = deepcopy(answer)
    if isinstance(solvable, dict):
        solvable['answer'] = deepcopy(answer)
    return semantic, solvable
