import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/models/content_models.dart';
import 'package:modu_math_app/services/solvable_hint_service.dart';

void main() {
  const service = SolvableHintService();

  test('builds multiple-choice column addition hints by place value', () {
    final hints = service.buildHints(_columnAdditionContent);

    expect(hints, hasLength(4));
    expect(hints.map((hint) => hint.groupKey).toSet(), equals({null}));
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

  test('treats direct addend quantities as one column addition problem', () {
    final hints = service.buildHints(_directQuantityColumnAdditionContent);

    expect(hints, hasLength(4));
    expect(hints.map((hint) => hint.groupKey).toSet(), equals({null}));
    expect(hints[0].miniQuestion, equals('4 + 7은 얼마인가요?'));
    expect(_correctChoice(hints[0]), equals('11'));
    expect(_correctChoice(hints[3]), equals('921'));
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
    expect(hints.map((hint) => hint.groupKey).toSet(), equals({'1', '2'}));
    expect(hints.where((hint) => hint.groupKey == '1'), hasLength(4));
    expect(hints.where((hint) => hint.groupKey == '2'), hasLength(4));
    expect(hints[0].title, equals('1단계: (1) 일의 자리 더하기'));
    expect(hints[2].title, equals('3단계: (1) 십의 자리 더하기'));
    expect(_correctChoice(hints[2]), equals('7 + 5 + 1'));
    expect(hints[4].title, equals('1단계: (2) 일의 자리 더하기'));
    expect(hints[6].title, equals('3단계: (2) 십의 자리 더하기'));
    expect(_correctChoice(hints[6]), equals('5 + 5 + 1'));
  });

  test('uses only the matching addition subproblem for suffixed ids', () {
    final hints = service.buildHints(_additionSubproblemOneContent);

    expect(hints, hasLength(4));
    expect(hints.map((hint) => hint.groupKey).toSet(), equals({null}));
    expect(hints[0].title, equals('1단계: 일의 자리 더하기'));
    expect(hints[0].miniQuestion, equals('9 + 5은 얼마인가요?'));
    expect(_correctChoice(hints[0]), equals('14'));
    expect(hints[3].title, equals('4단계: 백의 자리와 답'));
    expect(_correctChoice(hints[3]), equals('724'));
  });

  test('builds hints for each comparison subproblem', () {
    final hints = service.buildHints(_comparisonContent);

    expect(hints, hasLength(11));
    expect(hints.map((hint) => hint.groupKey).toSet(), equals({'1', '2'}));
    expect(hints.where((hint) => hint.groupKey == '1'), hasLength(4));
    expect(hints.where((hint) => hint.groupKey == '2'), hasLength(7));
    expect(hints.take(4).map((hint) => hint.level), equals([1, 2, 3, 4]));
    expect(
        hints.skip(4).map((hint) => hint.level), equals([1, 2, 3, 4, 5, 6, 7]));
    expect(hints[0].title, equals('1단계: (1) 오른쪽 일의 자리 더하기'));
    expect(_correctChoice(hints[0]), equals('12'));
    expect(hints[1].title, equals('2단계: (1) 오른쪽 십의 자리 더하기'));
    expect(_correctChoice(hints[1]), equals('4 + 7 + 1'));
    expect(hints[3].title, equals('4단계: (1) 비교 기호 고르기'));
    expect(_correctChoice(hints[3]), equals('>'));
    expect(hints[4].title, equals('1단계: (2) 왼쪽 일의 자리 더하기'));
    expect(hints[7].title, equals('4단계: (2) 오른쪽 일의 자리 더하기'));
    expect(_correctChoice(hints[8]), equals('2 + 8 + 1'));
    expect(hints[10].title, equals('7단계: (2) 비교 기호 고르기'));
    expect(_correctChoice(hints[10]), equals('='));
  });

  test('uses only the matching comparison subproblem for suffixed ids', () {
    final hints = service.buildHints(_comparisonSubproblemOneContent);

    expect(hints, hasLength(4));
    expect(hints.map((hint) => hint.groupKey).toSet(), equals({null}));
    expect(hints[0].title, equals('1단계: 오른쪽 일의 자리 더하기'));
    expect(hints[0].miniQuestion, equals('8 + 4은 얼마인가요?'));
    expect(hints[3].title, equals('4단계: 비교 기호 고르기'));
    expect(hints[3].miniQuestion, equals('빈칸에 들어갈 기호는 무엇인가요?'));
    expect(_correctChoice(hints[3]), equals('>'));
  });

  test('builds intelligent place-value hints for multiplication partial products', () {
    final hints = service.buildHints(_multiplicationPlaceValueContent);

    expect(hints, hasLength(3));
    expect(hints[0].title, equals('1단계: 색칠된 자리의 실제 값 찾기'));
    expect(hints[0].miniQuestion, contains('숫자 6은 실제 얼마를 나타내나요?'));
    expect(_correctChoice(hints[0]), equals('60'));

    expect(hints[1].title, equals('2단계: 곱하는 수 확인'));
    expect(hints[1].miniQuestion, equals('곱하는 수는 얼마인가요?'));
    expect(_correctChoice(hints[1]), equals('4'));

    expect(hints[2].title, equals('3단계: 알맞은 곱셈식 완성'));
    expect(hints[2].miniQuestion, contains('색칠된 부분을 나타내는 알맞은 곱셈식은 무엇인가요?'));
    expect(_correctChoice(hints[2]), equals('60 × 4'));
  });

  test('builds hints from diagnostic questions when available', () {
    final hints = service.buildHints(_diagnosticQuestionContent);

    expect(hints, hasLength(2));
    expect(hints[0].title, equals('1단계: 개념 확인 1'));
    expect(hints[0].miniQuestion, equals('원의 중심에서 원 위의 한 점까지의 거리를 무엇이라고 하나요?'));
    expect(_correctChoice(hints[0]), equals('반지름'));

    expect(hints[1].title, equals('2단계: 개념 확인 2'));
    expect(hints[1].miniQuestion, equals('한 원에서 그을 수 있는 반지름은 몇 개인가요?'));
    expect(_correctChoice(hints[1]), equals('무수히 많다'));
  });

  test('builds 4 rich place-value calculation hints for expanded addition', () {
    final hints = service.buildHints(_expandedAdditionContent);

    expect(hints, hasLength(4));
    expect(hints[0].title, equals('1단계: 일의 자리 부분합 (7 + 2)'));
    expect(hints[0].miniQuestion, equals('첫 번째 칸에 들어갈 7 + 2의 값은 얼마인가요?'));
    expect(_correctChoice(hints[0]), equals('9'));

    expect(hints[1].title, equals('2단계: 십의 자리 부분합 (10 + 40)'));
    expect(hints[1].miniQuestion, equals('두 번째 칸에 들어갈 10 + 40의 값은 얼마인가요?'));
    expect(_correctChoice(hints[1]), equals('50'));

    expect(hints[2].title, equals('3단계: 백의 자리 부분합 (200 + 500)'));
    expect(hints[2].miniQuestion, equals('세 번째 칸에 들어갈 200 + 500의 값은 얼마인가요?'));
    expect(_correctChoice(hints[2]), equals('700'));

    expect(hints[3].title, equals('4단계: 전체 합 완성하기 (9 + 50 + 700)'));
    expect(hints[3].miniQuestion, equals('마지막 칸에 들어갈 전체 합(9 + 50 + 700)의 값은 얼마인가요?'));
    expect(_correctChoice(hints[3]), equals('759'));
  });

  test('builds 4 structured pedagogical hints for word problems', () {
    final hints = service.buildHints(_wordProblemContent);

    expect(hints, hasLength(4));
    expect(hints[0].title, equals('1단계: 개념 확인 1'));
    expect(hints[0].miniQuestion, equals('이 문제에서 구해야 하는 것은 무엇인가요?'));
    expect(_correctChoice(hints[0]), equals('기영이가 처음 가지고 있던 구슬 수'));

    expect(hints[1].title, equals('2단계: 개념 확인 2'));
    expect(hints[1].miniQuestion, equals('처음 가지고 있던 구슬 수를 구하려면 어떻게 해야 하나요?'));
    expect(_correctChoice(hints[1]), equals('120, 130, 220을 모두 더합니다.'));

    expect(hints[2].title, equals('3단계: 두 사람에게 준 구슬 수를 구합니다. (120 + 130)'));
    expect(hints[2].miniQuestion, equals('120 + 130의 값은 얼마인가요?'));
    expect(_correctChoice(hints[2]), equals('250'));

    expect(hints[3].title, equals('4단계: 처음 가지고 있던 구슬 수를 구합니다. (250 + 220)'));
    expect(hints[3].miniQuestion, equals('250 + 220의 값은 얼마인가요?'));
    expect(_correctChoice(hints[3]), equals('470'));
  });

  test('builds comparison hints for addition expression and number comparison', () {
    final hints = service.buildHints(_compareAdditionAndNumberContent);

    expect(hints, hasLength(2));
    expect(hints[0].title, equals('1단계: 개념 확인 1'));
    expect(hints[0].miniQuestion, equals('400+156의 계산 결과는 얼마인가요?'));
    expect(_correctChoice(hints[0]), equals('556'));

    expect(hints[1].title, equals('2단계: 개념 확인 2'));
    expect(hints[1].miniQuestion, equals('556과 501의 크기를 바르게 비교한 것은 무엇인가요?'));
    expect(_correctChoice(hints[1]), equals('556 > 501'));
  });
}

const _compareAdditionAndNumberContent = ProblemContent(
  summary: ProblemSummary(
    id: 'P3_1_01_00040_15610',
    grade: 3,
    subject: 'math',
    unit: 'addition',
    type: 'comparison',
    title: '덧셈식과 수의 크기 비교',
    path: '',
    raw: {},
  ),
  semantic: {},
  solvable: {
    'problem_type': 'text_answer_compare_addition_expression_and_number',
    'inputs': {
      'left_expression': {'first': 400, 'operator': '+', 'second': 156},
      'right_value': 501,
      'allowed_symbols': ['>', '=', '<'],
    },
    'understanding': {
      'diagnostic_questions': [
        {
          'id': 'understand.calculate_sum',
          'prompt': '400+156의 계산 결과는 얼마인가요?',
          'choices': ['456', '556', '656'],
          'answer_index': 1,
        },
        {
          'id': 'understand.compare',
          'prompt': '556과 501의 크기를 바르게 비교한 것은 무엇인가요?',
          'choices': ['556 > 501', '556 = 501', '556 < 501'],
          'answer_index': 0,
        },
      ],
    },
    'steps': [
      {'id': 'step.calculate_sum', 'expr': '400 + 156', 'value': 556},
      {'id': 'step.compare_values', 'expr': '556 > 501', 'value': '>'},
    ],
    'answer': {'value': '>'},
  },
);

const _wordProblemContent = ProblemContent(
  summary: ProblemSummary(
    id: 'P3_1_01_00040_15603',
    grade: 3,
    subject: 'math',
    unit: 'addition',
    type: 'word_problem',
    title: '기영이가 처음 가지고 있던 구슬 수',
    path: '',
    raw: {},
  ),
  semantic: {},
  solvable: {
    'problem_type': 'numeric_answer_addition_word_problem',
    'understanding': {
      'diagnostic_questions': [
        {
          'id': 'understand.target',
          'prompt': '이 문제에서 구해야 하는 것은 무엇인가요?',
          'choices': [
            '호근이에게 준 구슬 수',
            '두 사람에게 주고 남은 구슬 수',
            '기영이가 처음 가지고 있던 구슬 수',
          ],
          'answer_index': 2,
        },
        {
          'id': 'understand.relation',
          'prompt': '처음 가지고 있던 구슬 수를 구하려면 어떻게 해야 하나요?',
          'choices': [
            '120, 130, 220을 모두 더합니다.',
            '220에서 120과 130을 뺍니다.',
            '120과 130만 더합니다.',
          ],
          'answer_index': 0,
        },
      ],
    },
    'steps': [
      {
        'id': 'step.add_given_marbles',
        'goal': '두 사람에게 준 구슬 수를 구합니다.',
        'expr': '120 + 130',
        'value': {'count': 250, 'unit': '개'},
        'explanation': '120과 130을 더하면 두 사람에게 준 구슬은 250개입니다.',
      },
      {
        'id': 'step.restore_initial_marbles',
        'goal': '처음 가지고 있던 구슬 수를 구합니다.',
        'expr': '250 + 220',
        'value': {'count': 470, 'unit': '개'},
        'explanation': '250개와 220개를 더하면 처음에 가지고 있던 구슬은 470개입니다.',
      },
    ],
  },
);

const _expandedAdditionContent = ProblemContent(
  summary: ProblemSummary(
    id: 'P3_1_01_00040_15598_1',
    grade: 3,
    subject: 'math',
    unit: 'addition',
    type: 'calc',
    title: '자리값별 부분합으로 덧셈하기',
    path: '',
    raw: {},
  ),
  semantic: {},
  solvable: {
    'problem_type': 'multi_numeric_answer_expanded_vertical_addition_problem',
    'understanding': {
      'diagnostic_questions': [
        {
          'id': 'understand.first_box',
          'prompt': '각 계산의 첫 번째 작은 칸에는 무엇을 쓰나요?',
          'choices': ['일의 자리끼리 더한 값', '십의 자리끼리 더한 값', '두 수의 전체 합'],
          'answer_index': 0,
        },
      ],
    },
    'steps': [
      {'id': 'step.1.ones', 'expr': '7 + 2', 'value': 9, 'explanation': '일의 자리끼리 더합니다.'},
      {'id': 'step.1.tens', 'expr': '10 + 40', 'value': 50, 'explanation': '십의 자리 숫자가 나타내는 값을 더합니다.'},
      {'id': 'step.1.hundreds', 'expr': '200 + 500', 'value': 700, 'explanation': '백의 자리 숫자가 나타내는 값을 더합니다.'},
      {'id': 'step.1.total', 'expr': '9 + 50 + 700', 'value': 759, 'explanation': '세 부분합을 모두 더합니다.'},
      {'id': 'step.collect_answers', 'expr': '[9, 50, 700, 759]', 'value': [9, 50, 700, 759]},
    ],
  },
);

const _multiplicationPlaceValueSummary = ProblemSummary(
  id: 'S3_초등_3_008559',
  grade: 3,
  subject: 'math',
  unit: 'multiplication',
  type: 'calc',
  title: '색칠된 부분은 실제 어떤 수의 곱인지 찾아 선택하세요.',
  path: '',
  raw: {},
);

const _multiplicationPlaceValueContent = ProblemContent(
  summary: _multiplicationPlaceValueSummary,
  semantic: {},
  solvable: {
    'problem_type': 'multiplication_place_value_choice',
    'given': [
      {'ref': 'obj.target', 'value': '60 × 4'},
    ],
    'plan': [
      '색칠된 부분의 자리값을 확인합니다.',
      '762에서 6은 십의 자리 숫자이므로 실제로는 60을 뜻합니다.',
      '색칠된 부분은 60 × 4를 나타냅니다.',
    ],
    'steps': [
      {'id': 'step.1', 'expr': '762의 6 = 60', 'value': 60},
      {'id': 'step.2', 'expr': '색칠된 부분 = 60 × 4', 'value': '60 × 4'},
    ],
    'answer': {
      'value': '60 × 4',
    },
  },
);

const _diagnosticQuestionContent = ProblemContent(
  summary: ProblemSummary(
    id: 'S3_초등_3_008636',
    grade: 3,
    subject: 'math',
    unit: 'geometry',
    type: 'choice',
    title: '원의 중심을 찾아 선택하세요.',
    path: '',
    raw: {},
  ),
  semantic: {},
  solvable: {
    'understanding': {
      'diagnostic_questions': [
        {
          'id': 'q1',
          'prompt': '원의 중심에서 원 위의 한 점까지의 거리를 무엇이라고 하나요?',
          'choices': ['지름', '반지름', '둘레'],
          'answer_index': 1,
        },
        {
          'id': 'q2',
          'prompt': '한 원에서 그을 수 있는 반지름은 몇 개인가요?',
          'choices': ['1개', '무수히 많다', '4개'],
          'answer_index': 1,
        },
      ],
    },
    'answer': {'value': '반지름'},
  },
);

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

const _directQuantityColumnAdditionContent = ProblemContent(
  summary: _summary,
  semantic: {},
  solvable: {
    'problem_type': 'multi_blank_vertical_addition',
    'inputs': {
      'answer_type': 'digit_list',
      'quantities': {
        'first_addend': 664,
        'second_addend': 257,
      },
    },
    'target': {'type': 'digit_list'},
    'steps': [
      {'id': 'step.add_ones', 'expr': '4 + 7', 'value': 11},
      {
        'id': 'step.write_ones_and_carry',
        'expr': '11 = 1 x 10 + 1',
        'value': {'carry': 1, 'digit': 1},
      },
      {'id': 'step.add_tens', 'expr': '6 + 5 + 1', 'value': 12},
      {
        'id': 'step.write_tens_and_carry',
        'expr': '12 = 1 x 10 + 2',
        'value': {'carry': 1, 'digit': 2},
      },
      {'id': 'step.add_hundreds', 'expr': '6 + 2 + 1', 'value': 9},
      {'id': 'step.compose_answer', 'expr': '900 + 20 + 1', 'value': 921},
    ],
    'answer': {
      'value': [1, 1, 9, 2, 1]
    },
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

const _additionSubproblemOneSummary = ProblemSummary(
  id: 'P3_1_01_00040_02151_1',
  grade: 3,
  subject: 'math',
  unit: 'addition',
  type: 'calc',
  title: '세 자리 수의 덧셈 계산',
  path: '',
  raw: {},
);

const _additionSubproblemOneContent = ProblemContent(
  summary: _additionSubproblemOneSummary,
  semantic: {},
  solvable: {
    'problem_type': 'multi_answer_vertical_addition',
    'inputs': {
      'answer_type': 'number_list',
      'quantities': {
        'problem_1': {
          'first_addend': 449,
          'second_addend': 275,
        },
        'problem_2': {
          'first_addend': 373,
          'second_addend': 468,
        },
        'problem_3': {
          'first_addend': 536,
          'second_addend': 287,
        },
      },
    },
    'answer': {
      'answer_key': [
        {'value': 724},
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

const _comparisonSubproblemOneSummary = ProblemSummary(
  id: 'P3_1_01_00040_00471_1',
  grade: 3,
  subject: 'math',
  unit: 'addition',
  type: 'calc',
  title: '비교 문제',
  path: '',
  raw: {},
);

const _comparisonSubproblemOneContent = ProblemContent(
  summary: _comparisonSubproblemOneSummary,
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
      ],
    },
  },
);
