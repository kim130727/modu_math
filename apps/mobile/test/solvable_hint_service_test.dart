import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/models/content_models.dart';
import 'package:modu_math_app/services/solvable_hint_service.dart';

void main() {
  const service = SolvableHintService();

  test('builds step hints from solvable data', () {
    final hints = service.buildHints(_content);

    expect(hints, hasLength(4));
    expect(hints[0].body, contains('사과의 전체 개수'));
    expect(hints[1].body, contains('덧셈'));
    expect(hints[1].body, contains('두 묶음을 더한다'));
    expect(hints[2].body, contains('3 + 4를 쓴다'));
    expect(hints[3].body, contains('3 + 4를 쓴다 = 7'));
    expect(hints[3].body, contains('답이 조건에 맞는지 확인한다'));
  });

  test('does not expose the final answer before level 4', () {
    final hints = service.buildHints(_content);

    for (final hint in hints.take(3)) {
      expect(hint.body, isNot(contains('7')));
    }
    expect(hints[3].body, contains('7'));
  });

  test('uses safe fallback text when solvable data has an unexpected shape',
      () {
    final hints = service.buildHints(
      const ProblemContent(
        summary: _summary,
        semantic: {},
        solvable: {'steps': 'not a list'},
      ),
    );

    expect(hints, hasLength(4));
    expect(hints[0].body, contains('무엇을 구해야 하는지'));
    expect(hints[2].body, contains('첫 번째로'));
    expect(hints[3].body, isNotEmpty);
  });
}

const _summary = ProblemSummary(
  id: 'P-hint',
  grade: 3,
  subject: 'math',
  unit: 'addition',
  type: 'calc',
  title: '사과 문제',
  path: '',
  raw: {},
);

const _content = ProblemContent(
  summary: _summary,
  semantic: {},
  solvable: {
    'target': {'text': '사과의 전체 개수 7개'},
    'method': '덧셈',
    'plan': ['두 묶음을 더한다'],
    'steps': [
      {
        'explanation': '3 + 4를 쓴다',
        'value': '7',
      },
    ],
    'explanation': '두 수를 더하면 전체가 된다.',
    'checks': ['답이 조건에 맞는지 확인한다'],
    'answer': {'value': 7},
  },
);
