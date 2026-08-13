import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/models/content_models.dart';
import 'package:modu_math_app/services/solvable_hint_service.dart';

void main() {
  const service = SolvableHintService();

  test('builds multiple-choice column addition hints by place value', () {
    final hints = service.buildHints(_columnAdditionContent);

    expect(hints, hasLength(4));
    expect(hints[0].title, equals('1단계: 일의 자리 더하기'));
    expect(hints[0].miniQuestion, equals('9 + 8은 얼마인가요?'));
    expect(_correctChoice(hints[0]), equals('17'));

    expect(hints[1].title, equals('2단계: 일의 자리 쓰기'));
    expect(hints[1].miniQuestion, equals('일의 자리에는 어떤 숫자를 쓰나요?'));
    expect(_correctChoice(hints[1]), equals('7'));

    expect(hints[2].title, equals('3단계: 십의 자리 더하기'));
    expect(hints[2].miniQuestion, equals('십의 자리 계산으로 알맞은 것은 무엇인가요?'));
    expect(_correctChoice(hints[2]), equals('5 + 4 + 1'));

    expect(hints[3].title, equals('4단계: 백의 자리와 답'));
    expect(hints[3].miniQuestion, equals('백의 자리까지 계산하면 알맞은 답은 무엇인가요?'));
    expect(_correctChoice(hints[3]), equals('507'));
  });

  test('uses elementary multiple-choice fallback hints', () {
    final hints = service.buildHints(_simpleContent);

    expect(hints, hasLength(4));
    expect(hints[0].miniQuestion, equals('무엇을 구하는 문제인가요?'));
    expect(hints[0].choices.map((choice) => choice.label), contains('전체 수'));
    expect(_correctChoice(hints[0]), equals('전체 수'));
    expect(hints[1].choices.map((choice) => choice.label), contains('더하기'));
  });

  test('keeps authored student hints when column addition cannot be detected',
      () {
    final hints = service.buildHints(_contentWithStudentHints);

    expect(hints, hasLength(2));
    expect(hints[0].title, equals('1단계: 문제 이해'));
    expect(hints[0].body, contains('전체를 구하는 문제예요.'));
    expect(hints[1].body, isNot(contains('507')));
  });

  test('builds place-value hints for each addition subproblem', () {
    final hints = service.buildHints(_multiAdditionContent);

    expect(hints, hasLength(8));
    expect(hints[0].title, equals('1단계: (1) 일의 자리 더하기'));
    expect(hints[2].title, equals('3단계: (1) 십의 자리 더하기'));
    expect(_correctChoice(hints[2]), equals('7 + 5 + 1'));
    expect(hints[4].title, equals('1단계: (2) 일의 자리 더하기'));
    expect(hints[6].title, equals('3단계: (2) 십의 자리 더하기'));
    expect(_correctChoice(hints[6]), equals('5 + 5 + 1'));
  });

  test('builds hints for each comparison subproblem', () {
    final hints = service.buildHints(_comparisonContent);

    expect(hints, hasLength(12));
    expect(hints.take(5).map((hint) => hint.level), equals([1, 2, 3, 4, 5]));
    expect(
        hints.skip(5).map((hint) => hint.level), equals([1, 2, 3, 4, 5, 6, 7]));
    expect(hints[0].title, equals('1단계: (1) 왼쪽 값 확인'));
    expect(hints[1].title, equals('2단계: (1) 오른쪽 일의 자리 더하기'));
    expect(_correctChoice(hints[1]), equals('12'));
    expect(hints[2].title, equals('3단계: (1) 오른쪽 십의 자리 더하기'));
    expect(_correctChoice(hints[2]), equals('4 + 7 + 1'));
    expect(hints[4].title, equals('5단계: (1) 비교 기호 고르기'));
    expect(_correctChoice(hints[4]), equals('>'));
    expect(hints[5].title, equals('1단계: (2) 왼쪽 일의 자리 더하기'));
    expect(hints[8].title, equals('4단계: (2) 오른쪽 일의 자리 더하기'));
    expect(_correctChoice(hints[9]), equals('2 + 8 + 1'));
    expect(hints[11].title, equals('7단계: (2) 비교 기호 고르기'));
    expect(_correctChoice(hints[11]), equals('='));
  });
}

String _correctChoice(SolvableHint hint) {
  return hint.choices.singleWhere((choice) => choice.isCorrect).label;
}

const _summary = ProblemSummary(
  id: 'P-hint',
  grade: 3,
  subject: 'math',
  unit: 'addition',
  type: 'calc',
  title: '덧셈 문제',
  path: '',
  raw: {},
);

const _columnAdditionContent = ProblemContent(
  summary: _summary,
  semantic: {
    'metadata': {
      'question': '상현이네 259개와 용진이네 248개를 더해요.',
    },
  },
  solvable: {
    'method': 'vertical_addition_with_carry',
    'plan': '259 + 248을 일의 자리부터 더한다.',
    'answer': {'value': 507},
  },
);

const _simpleContent = ProblemContent(
  summary: _summary,
  semantic: {},
  solvable: {
    'target': {'text': '사과의 전체 개수'},
    'method': 'add_parts',
    'answer': {'value': 7},
  },
);

const _contentWithStudentHints = ProblemContent(
  summary: _summary,
  semantic: {},
  solvable: {
    'student_hints': [
      {
        'level': 1,
        'title': '1단계: 문제 이해',
        'text': '두 묶음을 모두 더해 전체를 구하는 문제예요.',
      },
      {
        'level': 2,
        'title': '2단계: 계산 방법',
        'text': '259와 248을 더해요. 답은 507이에요.',
      },
    ],
    'answer': {'value': 507},
  },
);

const _multiAdditionContent = ProblemContent(
  summary: _summary,
  semantic: {},
  solvable: {
    'problem_type': 'multi_numeric_answer_vertical_addition',
    'inputs': {
      'quantities': {
        'problem_1': {
          'addends': [379, 855],
        },
        'problem_2': {
          'addends': [654, 758],
        },
      },
    },
    'answer': {
      'answer_key': [
        {'value': 1234},
        {'value': 1412},
      ],
    },
  },
);

const _comparisonContent = ProblemContent(
  summary: _summary,
  semantic: {},
  solvable: {
    'problem_type': 'multi_answer_expression_comparison',
    'inputs': {
      'answer_type': 'comparison_operator',
      'quantities': {
        'problem_1': {
          'left_expression': '532',
          'left_value': 532,
          'right_expression': '248 + 274',
          'right_value': 522,
        },
        'problem_2': {
          'left_expression': '346 + 667',
          'left_value': 1013,
          'right_expression': '428 + 585',
          'right_value': 1013,
        },
      },
    },
    'answer': {
      'answer_key': [
        {'value': '>'},
        {'value': '='},
      ],
    },
  },
);
