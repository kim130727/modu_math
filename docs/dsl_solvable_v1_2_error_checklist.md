# DSL Solvable v1.2 오류 체크리스트

이 문서는 `problem.dsl.py` 생성 후 `mb <PROBLEM_ID>` 또는 manual pipeline 빌드에서 반복적으로 나온 `modu.solvable.v1.2` 스키마 오류를 정리한 것입니다.

DSL을 새로 만들기 전, 또는 빌드 오류가 났을 때 아래 항목을 먼저 확인합니다.

## 필수 기본 구조

`SOLVABLE`에는 최소한 아래 최상위 키가 모두 있어야 합니다.

```python
SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "...",
    "inputs": {
        "target_label": "...",
        "unit": "",
    },
    "given": [],
    "target": {
        "ref": "...",
        "type": "...",
    },
    "understanding": {
        "summary": "...",
        "facts": [],
        "unknowns": [],
        "relation": {
            "type": "...",
            "statement": "...",
        },
    },
    "method": "...",
    "plan": [],
    "steps": [],
    "checks": [],
    "answer": {
        "value": "...",
        "unit": "",
    },
}
```

## 자주 나온 오류

### 1. `target.refs` 사용

오류 예:

```text
Additional properties are not allowed ('refs' was unexpected)
```

원인:

`SOLVABLE["target"]`에는 `refs`를 사용할 수 없습니다. 스키마상 허용되는 필드는 `ref`, `type`뿐입니다.

올바른 형태:

```python
"target": {
    "ref": "answer.values",
    "type": "number_pair",
}
```

잘못된 형태:

```python
"target": {
    "refs": ["quantity.left", "quantity.right"],
    "type": "number_pair",
}
```

여러 답을 구하는 문제도 `target.ref`는 대표 ref 하나만 둡니다. 개별 답 ref는 `answer.values`, `answer.blanks`, `answer.answer_key` 등에 넣습니다.

### 2. `answer.unit` 누락

오류 예:

```text
'unit' is a required property
```

원인:

`SOLVABLE["answer"]`에는 항상 최상위 `value`, `unit`이 필요합니다.

숫자 답:

```python
"answer": {
    "type": "numeric",
    "value": 534,
    "unit": "권",
    "target_ref": "quantity.total",
}
```

텍스트 답:

```python
"answer": {
    "type": "text",
    "value": "소방서",
    "unit": "",
    "target_ref": "place.fire_station",
}
```

단위가 없으면 `unit: ""`을 사용합니다.

### 3. 다중 답에서 최상위 `value`, `unit` 누락

원인:

`values`, `blanks`, `answer_key`가 있더라도 `answer` 최상위에는 `value`, `unit`이 반드시 있어야 합니다.

올바른 형태:

```python
"answer": {
    "type": "multi_numeric",
    "value": [334, 415],
    "unit": "",
    "values": [
        {"value": 334, "unit": "", "target_ref": "answer.first_blank"},
        {"value": 415, "unit": "", "target_ref": "answer.second_blank"},
    ],
}
```

### 4. `inputs.target_label` 누락

오류 예:

```text
'target_label' is a required property
```

원인:

`SOLVABLE["inputs"]`에는 항상 `target_label`이 필요합니다.

올바른 형태:

```python
"inputs": {
    "target_label": "빈칸에 들어갈 두 수",
    "unit": "",
    "options": [325, 532, 334, 985, 415],
}
```

### 5. `inputs.unit` 누락

오류 예:

```text
'unit' is a required property
```

원인:

`SOLVABLE["inputs"]`에도 항상 `unit`이 필요합니다.

올바른 형태:

```python
"inputs": {
    "target_label": "큰 수",
    "unit": "",
    "quantities": {
        "sum": 735,
    },
}
```

단위가 없는 문제도 `unit: ""`을 넣습니다.

### 6. `method` 누락

오류 예:

```text
'method' is a required property
```

원인:

`SOLVABLE` 최상위에 `method`가 필요합니다. `plan`만으로 대체되지 않습니다.

올바른 형태:

```python
"method": "표에서 필요한 두 수를 찾아 더합니다.",
"plan": [
    "표에서 첫 번째 수를 찾습니다.",
    "표에서 두 번째 수를 찾습니다.",
    "두 수를 더합니다.",
],
```

### 7. `understanding.relation.results` 사용

원인:

`understanding.relation`에는 `results`를 사용할 수 없습니다. 허용되는 필드는 `type`, `statement`, `symbolic`, `uses`, `result`입니다.

올바른 형태:

```python
"relation": {
    "type": "sequential_addition",
    "statement": "앞에서 구한 결과를 다음 덧셈의 시작 수로 사용합니다.",
    "symbolic": "156 + 278 = middle; middle + 697 = end",
    "uses": [
        "number.start",
        "operation.add_278",
        "operation.add_697",
    ],
    "result": "answer.all",
}
```

잘못된 형태:

```python
"relation": {
    "type": "system",
    "statement": "...",
    "results": ["quantity.x", "quantity.y"],
}
```

### 8. semantic answer와 solvable answer 불일치

오류 예:

```text
CrossLayerValidationError: semantic.answer must exactly match solvable.answer
```

원인:

`SEMANTIC_OVERRIDE["answer"]`와 `SOLVABLE["answer"]`가 서로 다릅니다.

권장 패턴:

```python
ANSWER = {
    "type": "numeric",
    "value": 534,
    "unit": "권",
    "target_ref": "quantity.total",
    "derived_from": "step.add",
}

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "...",
    "domain": {...},
    "answer": ANSWER,
}

SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "...",
    ...
    "answer": ANSWER,
}

SEMANTIC_ANSWER = SOLVABLE["answer"]
```

주의:

`SEMANTIC_ANSWER = SOLVABLE["answer"]`는 반드시 `SOLVABLE` 정의 뒤에 둡니다.

### 9. `diagnostic_questions[].choices`에 숫자 사용

오류 예:

```text
595 is not of type 'string'
```

원인:

`SOLVABLE["understanding"]["diagnostic_questions"][].choices`의 각 항목은 문자열이어야 합니다.

숫자 선택지도 문자열로 작성합니다.

올바른 형태:

```python
"diagnostic_questions": [
    {
        "id": "understand.left_sum",
        "type": "multiple_choice",
        "prompt": "450+146의 계산 결과는 얼마인가요?",
        "choices": ["595", "596", "597"],
        "answer_index": 1,
    }
]
```

잘못된 형태:

```python
"diagnostic_questions": [
    {
        "id": "understand.left_sum",
        "type": "multiple_choice",
        "prompt": "450+146의 계산 결과는 얼마인가요?",
        "choices": [595, 596, 597],
        "answer_index": 1,
    }
]
```

## 생성 전 최종 점검

새 DSL을 만들기 전에 아래를 확인합니다.

- `ProblemTemplate.id`, `SEMANTIC_OVERRIDE["problem_id"]`, `SOLVABLE["problem_id"]`가 모두 같습니다.
- `SOLVABLE["schema"]`는 정확히 `"modu.solvable.v1.2"`입니다.
- `SOLVABLE["inputs"]`에 `target_label`, `unit`이 있습니다.
- `SOLVABLE["target"]`에는 `ref`, `type`만 사용합니다.
- `SOLVABLE["method"]`가 있습니다.
- `SOLVABLE["plan"]`, `steps`, `checks`가 있습니다.
- 모든 `steps` 항목에는 최소 `id`, `expr`, `value`가 있습니다.
- 모든 `checks` 항목에는 최소 `id`, `expr`, `expected`, `actual`, `pass`가 있습니다.
- `diagnostic_questions[].choices`의 모든 항목은 문자열입니다.
- `SOLVABLE["answer"]`에는 최상위 `value`, `unit`이 있습니다.
- 텍스트 답 또는 단위 없는 답은 `unit: ""`을 사용합니다.
- `SEMANTIC_OVERRIDE["answer"]`와 `SOLVABLE["answer"]`는 같은 객체 또는 완전히 같은 값입니다.

## 빌드 확인 명령

```powershell
mb <PROBLEM_ID>
```

또는 직접 검증:

```powershell
uv run python tools/validate_generated_dsl.py --dsl examples/problems/<PROBLEM_ID>.dsl.py --strict --emit-solvable
```
