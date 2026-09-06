# 문제 풀이 화면의 콘텐츠 분리

문제 풀이 화면은 모든 문제에 `problemVisualRenderer`를 적용합니다.
문제 ID나 학년별 예외 없이, 새 문제도 같은 표시 경로를 사용합니다.

- 상단 지문: semantic의 `metadata.question` 또는 `metadata.instruction`.
- 답 패널: 기존 `ProblemContent.choices`와 입력·채점 규칙.
- Canvas: 위 두 영역으로 옮긴 텍스트를 제외한 도형·수식·입력 칸.

새 문제를 작성할 때 지문은 semantic에 완전한 문자열로 제공하고,
renderer의 지문 요소에는 `instruction`, `question`, `stem`, `slot.q1` 등의
식별자를 사용합니다. 선택지 텍스트에는 `slot.choice.1` 등의 식별자 또는
`attributes.data-semantic-role` 값 `choice`/`option`을 사용합니다.
선택지의 내용은 답 패널에서 사용하는 선택지 문자열과 일치해야 합니다.
번호와 공백의 차이는 허용합니다. 도형 설명에는 선택지 역할을 지정하지 않습니다.

원본 renderer를 수정하지 않는 표시 전용 처리이므로 편집, 힌트, 정답 판정에는
원래 데이터를 사용합니다. 화면 재생성 때도 같은 표시 데이터를 재사용합니다.
지원되는 도형만 있는 경우 남은 그림에 맞추어 표시 영역을 조정하며,
경로나 변환 등 경계를 확정할 수 없는 요소가 있으면 원래 영역을 유지합니다.

이미지에 합쳐진 지문·선택지는 텍스트 요소로 구조화해야 분리할 수 있습니다.
SVG만 제공하는 이전 형식은 기존 SVG 표시를 유지합니다.

검증: `flutter test test/problem_presentation_test.dart
test/renderer_json_canvas_test.dart test/problem_solve_screen_test.dart`
