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
    expect(hints[3].title, contains('마지막 점검'));
    expect(hints[3].body, contains('3 + 4를 쓴다'));
    expect(hints[3].body, contains('두 수를 모두 사용'));
    expect(hints[3].body, isNot(contains('답이 조건에 맞는지 확인한다')));
  });

  test('does not expose the final answer in any hint', () {
    final hints = service.buildHints(_content);

    for (final hint in hints) {
      expect(hint.body, isNot(contains('7')));
    }
  });

  test('naturalizes internal method codes for students', () {
    final hints = service.buildHints(_contentWithMethodCode);

    expect(hints[1].body, contains('나누어 주어진 수들을 모두 더해요'));
    expect(hints[1].body, isNot(contains('add_parts')));
  });

  test('uses target label instead of internal target refs', () {
    final hints = service.buildHints(_contentWithTargetLabel);

    expect(hints[0].body, contains('올해 수확한 사과 수를 구하는 문제'));
    expect(hints[0].body, isNot(contains('quantity.this_year_apple_count')));
    expect(hints[0].body, isNot(contains('number')));
  });

  test('naturalizes target refs when target label is missing', () {
    final hints = service.buildHints(_contentWithTargetRef);

    expect(hints[0].body, contains('올해 사과 수를 구하는 문제'));
    expect(hints[0].body, isNot(contains('quantity.this_year_apple_count')));
    expect(hints[0].body, isNot(contains('number')));
  });

  test('naturalizes common internal target types', () {
    final comparisonHints = service.buildHints(
      _contentWithTarget(
        ref: 'answer.comparison_operators',
        type: 'operator_list',
      ),
    );
    final readersHints = service.buildHints(
      _contentWithTarget(
        ref: 'group.all_readers',
        type: 'count',
      ),
    );
    final stampsHints = service.buildHints(
      _contentWithTarget(
        ref: 'collection.total_stamps',
        type: 'count',
      ),
    );

    expect(comparisonHints[0].body, contains('각 빈칸에 들어갈 비교 기호'));
    expect(readersHints[0].body, contains('책을 읽고 있는 사람의 전체 수'));
    expect(stampsHints[0].body, contains('우표의 전체 수'));
    for (final hint in [comparisonHints[0], readersHints[0], stampsHints[0]]) {
      expect(hint.body, isNot(contains('answer.comparison_operators')));
      expect(hint.body, isNot(contains('operator_list')));
      expect(hint.body, isNot(contains('group.all_readers')));
      expect(hint.body, isNot(contains('collection.total_stamps')));
    }
  });

  test('ignores internal-looking target labels', () {
    final hints = service.buildHints(
      _contentWithTarget(
        label: 'selected_unit',
        ref: 'answer.target',
        type: 'selected_unit',
      ),
    );

    expect(hints[0].body, contains('알맞은 단위'));
    expect(hints[0].body, isNot(contains('selected_unit')));
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

const _contentWithMethodCode = ProblemContent(
  summary: _summary,
  semantic: {},
  solvable: {
    'target': '전체 개수',
    'method': 'add_parts',
    'plan': '두 가족이 캔 수를 더한다',
    'steps': [
      {
        'explanation': '259와 248을 더한다',
        'value': '507',
      },
    ],
    'answer': {'value': 507},
  },
);

const _contentWithTargetLabel = ProblemContent(
  summary: _summary,
  semantic: {},
  solvable: {
    'inputs': {
      'target_label': '올해 수확한 사과 수',
    },
    'target': {
      'ref': 'quantity.this_year_apple_count',
      'type': 'number',
    },
    'answer': {'value': 1012},
  },
);

const _contentWithTargetRef = ProblemContent(
  summary: _summary,
  semantic: {},
  solvable: {
    'target': {
      'ref': 'quantity.this_year_apple_count',
      'type': 'number',
    },
    'answer': {'value': 1012},
  },
);

ProblemContent _contentWithTarget({
  String? label,
  required String ref,
  required String type,
}) {
  return ProblemContent(
    summary: _summary,
    semantic: const {},
    solvable: {
      if (label != null) 'inputs': {'target_label': label},
      'target': {
        'ref': ref,
        'type': type,
      },
      'answer': {'value': 1},
    },
  );
}

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
