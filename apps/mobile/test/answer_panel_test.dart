import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/models/content_models.dart';
import 'package:modu_math_app/utils/answer_normalizer.dart';
import 'package:modu_math_app/widgets/answer_panel.dart';

void main() {
  testWidgets('allows selecting multiple correct choices', (tester) async {
    var draft = '';
    var submitted = '';

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: AnswerPanel(
            content: _multiChoiceContent,
            answerDraft: draft,
            isCorrect: null,
            onAnswerChanged: (value) => draft = value,
            onSubmit: (value) => submitted = value,
          ),
        ),
      ),
    );

    await tester.tap(find.text('80 x 40'));
    await tester.tap(find.text('62 x 50'));
    await tester.pumpAndSettle();

    expect(draft, equals('80 x 4062 x 50'));

    await tester.tap(find.byType(FilledButton));
    await tester.pumpAndSettle();

    expect(submitted, equals('80 x 4062 x 50'));
  });

  testWidgets('allows selecting duplicate choice labels independently',
      (tester) async {
    var submitted = '';

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: AnswerPanel(
            content: _duplicateChoiceContent,
            answerDraft: '',
            isCorrect: null,
            onAnswerChanged: (_) {},
            onSubmit: (value) => submitted = value,
          ),
        ),
      ),
    );

    final duplicateChoices = find.text('80 x 40');
    expect(duplicateChoices, findsNWidgets(2));

    await tester.tap(duplicateChoices.at(0));
    await tester.tap(duplicateChoices.at(1));
    await tester.pumpAndSettle();

    final selectedChips = tester
        .widgetList<ChoiceChip>(find.byType(ChoiceChip))
        .where((chip) => chip.selected);
    expect(selectedChips, hasLength(2));

    await tester.tap(find.byType(FilledButton));
    await tester.pumpAndSettle();

    expect(submitted, equals('80 x 4080 x 40'));
  });

  test('merges alternating split marker choices into complete choice items', () {
    const content = ProblemContent(
      summary: _summary,
      semantic: {},
      renderer: {},
      solvable: {
        'answer': {
          'choices': [
            '1.',
            '320+145',
            '2.',
            '300+200',
            '3.',
            '163+326',
            '4.',
            '236+362',
            '5.',
            '405+104',
          ],
        },
      },
    );

    expect(content.choices, equals([
      '1. 320+145',
      '2. 300+200',
      '3. 163+326',
      '4. 236+362',
      '5. 405+104',
    ]));
  });

  test('merges grouped operator and number renderer elements into clean choices', () {
    const content = ProblemContent(
      summary: _summary,
      semantic: {},
      renderer: {
        'elements': [
          {'id': 'slot.choice_1_div.text', 'source_ref': 'slot.choice_1_div', 'text': '÷', 'attributes': {'x': 179.996, 'y': 140.0}},
          {'id': 'slot.choice_1_num.text', 'source_ref': 'slot.choice_1_num', 'text': '6', 'attributes': {'x': 210.996, 'y': 140.0}},
          {'id': 'slot.choice_2_div.text', 'source_ref': 'slot.choice_2_div', 'text': '÷', 'attributes': {'x': 367.996, 'y': 140.0}},
          {'id': 'slot.choice_2_num.text', 'source_ref': 'slot.choice_2_num', 'text': '5', 'attributes': {'x': 396.996, 'y': 140.0}},
          {'id': 'slot.choice_3_div.text', 'source_ref': 'slot.choice_3_div', 'text': '÷', 'attributes': {'x': 562.996, 'y': 140.0}},
          {'id': 'slot.choice_3_num.text', 'source_ref': 'slot.choice_3_num', 'text': '9', 'attributes': {'x': 597.996, 'y': 140.0}},
          {'id': 'slot.choice_4_div.text', 'source_ref': 'slot.choice_4_div', 'text': '÷', 'attributes': {'x': 747.996, 'y': 140.0}},
          {'id': 'slot.choice_4_num.text', 'source_ref': 'slot.choice_4_num', 'text': '4', 'attributes': {'x': 782.996, 'y': 140.0}},
        ],
      },
      solvable: {},
    );

    expect(content.choices, equals([
      '1. ÷ 6',
      '2. ÷ 5',
      '3. ÷ 9',
      '4. ÷ 4',
    ]));
  });

  test('extracts choices from solvable given expressions when choices array is empty', () {
    const content = ProblemContent(
      summary: _summary,
      semantic: {},
      renderer: {},
      solvable: {
        'problem_type': 'multiple_choice_division',
        'given': [
          {
            'ref': 'obj.left_division',
            'value': {'expression': '24 ÷ 7'},
          },
          {
            'ref': 'obj.right_division',
            'value': {'expression': '49 ÷ 5'},
          },
        ],
      },
    );

    expect(content.choices, equals([
      '1. 24 ÷ 7',
      '2. 49 ÷ 5',
    ]));
  });

  test('does not treat word problem given entities as multiple choice options', () {
    const content = ProblemContent(
      summary: ProblemSummary(
        id: 'P3_1_01_00040_00473',
        grade: 3,
        subject: 'math',
        unit: '1학기 1. 덧셈과 뺄셈',
        type: 'numeric_answer_addition_word_problem',
        title: '미란이가 모은 우표의 수',
        path: '',
        raw: {},
      ),
      semantic: {
        'problem_type': 'numeric_answer_addition_word_problem',
        'answer': {
          'value': 913,
          'unit': '장',
          'blanks': [
            {'id': 'slot_0', 'slot_id': 'slot_0', 'expected': 913}
          ],
        },
      },
      renderer: {
        'elements': [
          {
            'id': 'slot_0.rect',
            'type': 'rect',
            'interaction': {
              'type': 'input',
              'role': 'answer',
              'value_type': 'integer',
            },
          }
        ],
      },
      solvable: {
        'problem_type': 'numeric_answer_addition_word_problem',
        'given': [
          {
            'ref': 'collection.stamps_until_last_year',
            'value': {'count': 634, 'unit': '장', 'label': '작년까지 모은 우표'},
          },
          {
            'ref': 'collection.stamps_this_year',
            'value': {'count': 279, 'unit': '장', 'label': '올해 모은 우표'},
          },
        ],
      },
    );

    expect(content.choices, isEmpty);
  });

  test('does not treat diagram item labels in P3_1_01_00040_02164_1 as choices', () {
    const content = ProblemContent(
      summary: ProblemSummary(
        id: 'P3_1_01_00040_02164_1',
        grade: 3,
        subject: 'math',
        unit: '1학기 1. 덧셈과 뺄셈',
        type: 'addition_rule_circle_fill_blank',
        title: '원 안의 두 수를 더하는 규칙',
        path: '',
        raw: {},
      ),
      semantic: {
        'problem_type': 'addition_rule_circle_fill_blank',
        'answer': {
          'blanks': [
            {'id': 'slot_rect', 'slot_id': 'slot_rect', 'expected': 701}
          ],
          'choices': [],
        },
      },
      renderer: {
        'elements': [
          {
            'id': 'slot.example_left_value.text',
            'type': 'text',
            'attributes': {'x': 71.5, 'y': 122.1, 'data-semantic-role': 'given_value'},
            'text': '259',
          },
          {
            'id': 'slot.item_1_left_value.text',
            'type': 'text',
            'attributes': {'x': 245.2, 'y': 122.6, 'data-semantic-role': 'given_value'},
            'text': '236',
          },
          {
            'id': 'slot.item_1_right_value.text',
            'type': 'text',
            'attributes': {'x': 293.2, 'y': 122.6, 'data-semantic-role': 'given_value'},
            'text': '465',
          },
          {
            'id': 'slot_rect.rect',
            'type': 'rect',
            'interaction': {
              'type': 'input',
              'role': 'answer',
              'value_type': 'integer',
            },
          },
        ],
      },
      solvable: {
        'problem_type': 'addition_rule_circle_fill_blank',
      },
    );

    expect(content.choices, isEmpty);
  });

  test('extracts route comparison choice options for P3_1_01_00040_07646', () {
    const content = ProblemContent(
      summary: ProblemSummary(
        id: 'P3_1_01_00040_07646',
        grade: 3,
        subject: 'math',
        unit: '1학기 1. 덧셈과 뺄셈',
        type: 'text_answer_route_distance_comparison_problem',
        title: '학교까지 더 먼 길 비교하기',
        path: '',
        raw: {},
      ),
      semantic: {
        'problem_type': 'text_answer_route_distance_comparison_problem',
        'answer': {
          'type': 'choice',
          'value': '소방서',
          'choices': ['소방서', '주민센터'],
        },
      },
      renderer: {},
      solvable: {
        'problem_type': 'text_answer_route_distance_comparison_problem',
        'inputs': {
          'options': ['소방서', '주민센터'],
        },
        'answer': {
          'type': 'choice',
          'value': '소방서',
          'choices': ['소방서', '주민센터'],
        },
      },
    );

    expect(content.choices, equals(['소방서', '주민센터']));
  });

  test('does not treat <보기> options text in P3_1_01_00040_15472 as choices', () {
    const content = ProblemContent(
      summary: ProblemSummary(
        id: 'P3_1_01_00040_15472',
        grade: 3,
        subject: 'math',
        unit: '1학기 1. 덧셈과 뺄셈',
        type: 'multi_numeric_answer_select_addends_problem',
        title: '합이 749가 되는 두 수 찾기',
        path: '',
        raw: {},
      ),
      semantic: {
        'problem_type': 'multi_numeric_answer_select_addends_problem',
        'answer': {
          'type': 'multi_numeric',
          'value': [334, 415],
          'blanks': [
            {'id': 'slot_1', 'slot_id': 'slot_1', 'expected': 334},
            {'id': 'slot_2', 'slot_id': 'slot_2', 'expected': 415},
          ],
        },
      },
      renderer: {
        'elements': [
          {
            'id': 'slot.instruction.text',
            'type': 'text_box',
            'text': '다음 <보기>의 수들을 빈칸에 알맞게 써넣으시오.',
          },
          {
            'id': 'slot.options.text',
            'type': 'text_box',
            'text': '<보기>    325,   532,   334,   985,   415',
          },
          {
            'id': 'konva_1785217709470_rect_5693830.rect',
            'type': 'rect',
            'interaction': {
              'type': 'input',
              'role': 'answer',
              'value_type': 'integer',
            },
          },
          {
            'id': 'konva_1785217709470_paste_5710048_0.rect',
            'type': 'rect',
            'interaction': {
              'type': 'input',
              'role': 'answer',
              'value_type': 'integer',
            },
          },
        ],
      },
      solvable: {
        'problem_type': 'multi_numeric_answer_select_addends_problem',
        'inputs': {
          'options': [325, 532, 334, 985, 415],
        },
        'answer': {
          'type': 'multi_numeric',
          'value': [334, 415],
        },
      },
    );

    expect(content.choices, isEmpty);
  });

  test('does not treat number cards as choices for P3_1_01_00040_15611', () {
    final content = ProblemContent(
      summary: const ProblemSummary(
        id: 'P3_1_01_00040_15611',
        grade: 3,
        subject: 'math',
        unit: 'addition',
        type: 'multi_numeric_digit_card_addition_completion',
        title: '숫자 카드로 덧셈식 완성하기',
        path: '',
        raw: {},
      ),
      renderer: {
        'elements': [
          {'id': 'slot.card1.rect.rect', 'type': 'rect'},
          {'id': 'slot.card5.rect.rect', 'type': 'rect'},
          {'id': 'slot.card2.rect.rect', 'type': 'rect'},
          {'id': 'slot.card7.rect.rect', 'type': 'rect'},
          {'id': 'slot.card1.text.text', 'type': 'text', 'text': '1'},
          {'id': 'slot.card5.text.text', 'type': 'text', 'text': '5'},
          {'id': 'slot.card2.text.text', 'type': 'text', 'text': '2'},
          {'id': 'slot.card7.text.text', 'type': 'text', 'text': '7'},
          {
            'id': 'slot.top.blank_tens.rect.rect',
            'type': 'rect',
            'interaction': {'type': 'input', 'role': 'answer', 'value_type': 'digit'},
          },
        ],
      },
      solvable: {
        'problem_type': 'multi_numeric_digit_card_addition_completion',
        'given': [
          {'ref': 'set.digit_cards', 'value': [1, 5, 2, 7]},
          {'ref': 'expression.partial_addition', 'value': '2□□ + □35 = 38□'},
        ],
        'answer': {
          'type': 'multi_numeric',
          'value': [5, 2, 1, 7],
          'choices': [],
        },
      },
      semantic: const {},
    );

    expect(content.choices, isEmpty);
  });

  test('extracts choice blank square box for S3_초등_3_008588', () {
    final content = ProblemContent(
      summary: const ProblemSummary(
        id: 'S3_초등_3_008588',
        grade: 3,
        subject: 'math',
        unit: 'division',
        type: 'multiple_choice',
        title: '나머지가 4가 될 수 없는 식을 찾아 선택하세요',
        path: '',
        raw: {},
      ),
      renderer: {
        'elements': [
          {'id': 'slot.box.rect', 'type': 'rect', 'attributes': {'width': 745.0, 'height': 80.0}},
          {'id': 'slot.choice_1_blank.rect', 'type': 'rect', 'attributes': {'x': 147.996, 'y': 120.0, 'width': 25.0, 'height': 25.0}},
          {'id': 'slot.choice_1_div.text', 'type': 'text', 'attributes': {'x': 179.996, 'y': 140.0}, 'text': '÷'},
          {'id': 'slot.choice_1_num.text', 'type': 'text', 'attributes': {'x': 210.996, 'y': 140.0}, 'text': '6'},
          {'id': 'slot.choice_2_blank.rect', 'type': 'rect', 'attributes': {'x': 337.996, 'y': 120.0, 'width': 25.0, 'height': 25.0}},
          {'id': 'slot.choice_2_div.text', 'type': 'text', 'attributes': {'x': 367.996, 'y': 140.0}, 'text': '÷'},
          {'id': 'slot.choice_2_num.text', 'type': 'text', 'attributes': {'x': 396.996, 'y': 140.0}, 'text': '5'},
          {'id': 'slot.choice_3_blank.rect', 'type': 'rect', 'attributes': {'x': 532.996, 'y': 120.0, 'width': 25.0, 'height': 25.0}},
          {'id': 'slot.choice_3_div.text', 'type': 'text', 'attributes': {'x': 562.996, 'y': 140.0}, 'text': '÷'},
          {'id': 'slot.choice_3_num.text', 'type': 'text', 'attributes': {'x': 597.996, 'y': 140.0}, 'text': '9'},
          {'id': 'slot.choice_4_blank.rect', 'type': 'rect', 'attributes': {'x': 712.996, 'y': 120.0, 'width': 25.0, 'height': 25.0}},
          {'id': 'slot.choice_4_div.text', 'type': 'text', 'attributes': {'x': 747.996, 'y': 140.0}, 'text': '÷'},
          {'id': 'slot.choice_4_num.text', 'type': 'text', 'attributes': {'x': 782.996, 'y': 140.0}, 'text': '4'},
        ],
      },
      solvable: {
        'problem_type': 'multiple_choice',
        'answer': {
          'type': 'select_expression',
          'value': 4,
          'choices': [],
        },
      },
      semantic: const {},
    );

    expect(
      content.choices,
      equals([
        '1. □ ÷ 6',
        '2. □ ÷ 5',
        '3. □ ÷ 9',
        '4. □ ÷ 4',
      ]),
    );
  });

  test('extracts person names as choices for S3_초등_3_008590', () {
    final content = ProblemContent(
      summary: const ProblemSummary(
        id: 'S3_초등_3_008590',
        grade: 3,
        subject: 'math',
        unit: 'division',
        type: 'multiple_choice',
        title: '문제를 바르게 설명한 사람을 선택하세요.',
        path: '',
        raw: {},
      ),
      renderer: {
        'elements': [
          {'id': 'slot.q1', 'type': 'text', 'attributes': {'x': 155.0, 'y': 40.0}, 'text': '문제를 바르게 설명한 사람을 선택하세요.'},
          {'id': 'slot.opt1.text', 'type': 'text', 'attributes': {'x': 222.5, 'y': 208.5}, 'text': '몫은\n13이야.'},
          {'id': 'slot.name.opt1.text', 'type': 'text', 'attributes': {'x': 222.5, 'y': 430.0}, 'text': '형우'},
          {'id': 'slot.opt2.text', 'type': 'text', 'attributes': {'x': 477.5, 'y': 208.5}, 'text': '나머지는\n5보다 작아.'},
          {'id': 'slot.name.opt2.text', 'type': 'text', 'attributes': {'x': 477.5, 'y': 430.0}, 'text': '희영'},
          {'id': 'slot.opt3.text', 'type': 'text', 'attributes': {'x': 707.5, 'y': 208.5}, 'text': '나누어떨어지지\n않아.'},
          {'id': 'slot.name.opt3.text', 'type': 'text', 'attributes': {'x': 707.5, 'y': 430.0}, 'text': '성태'},
        ],
      },
      solvable: {
        'problem_type': 'division_explanation_choice',
        'given': [
          {'ref': 'obj.person.left', 'value': '형우'},
          {'ref': 'obj.person.middle', 'value': '희영'},
          {'ref': 'obj.person.right', 'value': '성태'},
        ],
        'target': {
          'ref': 'answer.target',
          'type': 'person_selection',
          'description': '문제를 바르게 설명한 사람',
        },
        'answer': {
          'type': 'person_selection',
          'description': '문제를 바르게 설명한 사람',
          'value': '성태',
          'choices': [],
        },
      },
      semantic: const {},
    );

    expect(
      content.choices,
      equals([
        '1. 형우',
        '2. 희영',
        '3. 성태',
      ]),
    );
  });

  test('extracts choice blank square box for S3_초등_3_008592', () {
    final content = ProblemContent(
      summary: const ProblemSummary(
        id: 'S3_초등_3_008592',
        grade: 3,
        subject: 'math',
        unit: 'division',
        type: 'division_remainder_selection',
        title: '나머지가 5가 될 수 없는 식',
        path: '',
        raw: {},
      ),
      renderer: {
        'elements': [
          {'id': 'slot.choice.1.no.text', 'type': 'text', 'attributes': {'x': 75.846, 'y': 105.0}, 'text': '①'},
          {'id': 'slot.choice.1.box.rect', 'type': 'rect', 'attributes': {'x': 123.008, 'y': 80.0, 'width': 25.0, 'height': 25.0}},
          {'id': 'slot.choice.1.div.text', 'type': 'text', 'attributes': {'x': 161.996, 'y': 106.0}, 'text': '÷'},
          {'id': 'slot.choice.1.den.text', 'type': 'text', 'attributes': {'x': 200.032, 'y': 103.0}, 'text': '5'},
          {'id': 'slot.choice.2.no.text', 'type': 'text', 'attributes': {'x': 276.994, 'y': 105.0}, 'text': '②'},
          {'id': 'slot.choice.2.box.rect', 'type': 'rect', 'attributes': {'x': 321.0, 'y': 80.0, 'width': 24.0, 'height': 24.0}},
          {'id': 'slot.choice.2.div.text', 'type': 'text', 'attributes': {'x': 360.0, 'y': 103.0}, 'text': '÷'},
          {'id': 'slot.choice.2.den.text', 'type': 'text', 'attributes': {'x': 396.998, 'y': 102.0}, 'text': '4'},
          {'id': 'slot.choice.3.no.text', 'type': 'text', 'attributes': {'x': 463.984, 'y': 104.0}, 'text': '③'},
          {'id': 'slot.choice.3.box.rect', 'type': 'rect', 'attributes': {'x': 510.953, 'y': 80.0, 'width': 24.0, 'height': 24.0}},
          {'id': 'slot.choice.3.div.text', 'type': 'text', 'attributes': {'x': 545.953, 'y': 101.0}, 'text': '÷'},
          {'id': 'slot.choice.3.den.text', 'type': 'text', 'attributes': {'x': 577.953, 'y': 101.0}, 'text': '8'},
          {'id': 'slot.choice.4.no.text', 'type': 'text', 'attributes': {'x': 75.888, 'y': 184.0}, 'text': '④'},
          {'id': 'slot.choice.4.box.rect', 'type': 'rect', 'attributes': {'x': 122.0, 'y': 160.0, 'width': 25.0, 'height': 25.0}},
          {'id': 'slot.choice.4.div.text', 'type': 'text', 'attributes': {'x': 162.999, 'y': 184.0}, 'text': '÷'},
          {'id': 'slot.choice.4.den.text', 'type': 'text', 'attributes': {'x': 200.032, 'y': 181.0}, 'text': '7'},
          {'id': 'slot.choice.5.no.text', 'type': 'text', 'attributes': {'x': 279.0, 'y': 183.0}, 'text': '⑤'},
          {'id': 'slot.choice.5.box.rect', 'type': 'rect', 'attributes': {'x': 319.992, 'y': 158.0, 'width': 25.0, 'height': 25.0}},
          {'id': 'slot.choice.5.div.text', 'type': 'text', 'attributes': {'x': 362.0, 'y': 182.0}, 'text': '÷'},
          {'id': 'slot.choice.5.den.text', 'type': 'text', 'attributes': {'x': 399.0, 'y': 179.0}, 'text': '6'},
        ],
      },
      solvable: {
        'problem_type': 'division_remainder_selection',
        'target': {'type': 'selection'},
        'answer': {
          'type': 'selection',
          'value': 2,
          'choices': [],
        },
      },
      semantic: const {},
    );

    expect(
      content.choices,
      equals([
        '1. □ ÷ 5',
        '2. □ ÷ 4',
        '3. □ ÷ 8',
        '4. □ ÷ 7',
        '5. □ ÷ 6',
      ]),
    );
  });

  test('extracts circled hangul consonant and blank square box for S3_초등_3_008601', () {
    final content = ProblemContent(
      summary: const ProblemSummary(
        id: 'S3_초등_3_008601',
        grade: 3,
        subject: 'math',
        unit: 'division',
        type: 'multiple_choice_division_remainder',
        title: '나머지가 3이 될 수 없는 나눗셈식을 찾아 기호를 선택해 보세요.',
        path: '',
        raw: {},
      ),
      renderer: {
        'elements': [
          {'id': 'slot.box.rect', 'type': 'rect', 'attributes': {'width': 760.0, 'height': 80.0}},
          {'id': 'slot.opt1.sym.text', 'type': 'text', 'attributes': {'x': 165.0, 'y': 150.0}, 'text': '㉠'},
          {'id': 'slot.opt1.blank.rect', 'type': 'rect', 'attributes': {'x': 210.0, 'y': 125.0, 'width': 25.0, 'height': 25.0}},
          {'id': 'slot.opt1.div.text', 'type': 'text', 'attributes': {'x': 245.0, 'y': 150.0}, 'text': '÷'},
          {'id': 'slot.opt1.num.text', 'type': 'text', 'attributes': {'x': 285.0, 'y': 150.0}, 'text': '2'},
          {'id': 'slot.opt2.sym.text', 'type': 'text', 'attributes': {'x': 380.0, 'y': 150.0}, 'text': '㉡'},
          {'id': 'slot.opt2.blank.rect', 'type': 'rect', 'attributes': {'x': 425.0, 'y': 125.0, 'width': 25.0, 'height': 25.0}},
          {'id': 'slot.opt2.div.text', 'type': 'text', 'attributes': {'x': 455.0, 'y': 150.0}, 'text': '÷'},
          {'id': 'slot.opt2.num.text', 'type': 'text', 'attributes': {'x': 490.0, 'y': 150.0}, 'text': '7'},
          {'id': 'slot.opt3.sym.text', 'type': 'text', 'attributes': {'x': 585.0, 'y': 150.0}, 'text': '㉢'},
          {'id': 'slot.opt3.blank.rect', 'type': 'rect', 'attributes': {'x': 635.0, 'y': 125.0, 'width': 25.0, 'height': 25.0}},
          {'id': 'slot.opt3.div.text', 'type': 'text', 'attributes': {'x': 670.0, 'y': 150.0}, 'text': '÷'},
          {'id': 'slot.opt3.num.text', 'type': 'text', 'attributes': {'x': 705.0, 'y': 150.0}, 'text': '5'},
        ],
      },
      solvable: {
        'problem_type': 'multiple_choice_division_remainder',
        'target': {'type': 'selected_symbol'},
        'answer': {
          'type': 'selected_symbol',
          'value': '㉠',
          'choices': [],
        },
      },
      semantic: const {},
    );

    expect(
      content.choices,
      equals([
        'ㄱ. □ ÷ 2',
        'ㄴ. □ ÷ 7',
        'ㄷ. □ ÷ 5',
      ]),
    );
  });

  test('extracts choices with expressions for S3_초등_3_008603', () {
    final content = ProblemContent(
      summary: const ProblemSummary(
        id: 'S3_초등_3_008603',
        grade: 3,
        subject: 'math',
        unit: 'division',
        type: 'divisibility_choice',
        title: '나누어떨어지는 나눗셈식',
        path: '',
        raw: {},
      ),
      renderer: {
        'elements': [
          {'id': 'slot.box.rect', 'type': 'rect', 'attributes': {'x': 197.011, 'y': 112.0, 'width': 380.0, 'height': 80.0}},
          {'id': 'slot.q1.text', 'type': 'text', 'attributes': {'x': 52.011, 'y': 71.0}, 'text': '나누어떨어지는 나눗셈식을 찾아 기호를 선택해 보세요.'},
          {'id': 'slot.v1.text', 'type': 'text', 'attributes': {'x': 227.011, 'y': 162.0}, 'text': '㉠ 64 ÷ 6'},
          {'id': 'slot.v2.text', 'type': 'text', 'attributes': {'x': 407.011, 'y': 162.0}, 'text': '㉡ 92 ÷ 4'},
        ],
      },
      solvable: {
        'problem_type': 'divisibility_choice',
        'target': {'type': 'selection'},
        'answer': {
          'type': 'selection',
          'value': 'ㄴ',
          'choices': [],
        },
      },
      semantic: const {},
    );

    expect(
      content.choices,
      equals([
        'ㄱ. 64 ÷ 6',
        'ㄴ. 92 ÷ 4',
      ]),
    );
    expect(isSameAnswer('ㄴ. 92 ÷ 4', content.correctAnswer), isTrue);
  });

  test('extracts person names as choices for S3_초등_3_008604', () {
    final content = ProblemContent(
      summary: const ProblemSummary(
        id: 'S3_초등_3_008604',
        grade: 3,
        subject: 'math',
        unit: 'division',
        type: 'multiple_choice',
        title: '문제를 바르게 설명한 사람의 이름을 선택하세요.',
        path: '',
        raw: {},
      ),
      renderer: {
        'elements': [
          {'id': 'slot.q1', 'type': 'text', 'attributes': {'x': 12.0, 'y': 28.0}, 'text': '문제를 바르게 설명한 사람의 이름을 선택하세요.'},
          {'id': 'slot.expr_text', 'type': 'text', 'attributes': {'x': 442.0, 'y': 84.0}, 'text': '67 ÷ 5'},
          {'id': 'slot.left.text', 'type': 'text', 'attributes': {'x': 257.0, 'y': 145.0}, 'text': '몫은\n13이야.'},
          {'id': 'slot.name.left.text', 'type': 'text', 'attributes': {'x': 257.0, 'y': 382.0}, 'text': '현태'},
          {'id': 'slot.right.text', 'type': 'text', 'attributes': {'x': 547.0, 'y': 145.0}, 'text': '나머지는 0으로\n나누어떨어져.'},
          {'id': 'slot.name.right.text', 'type': 'text', 'attributes': {'x': 547.0, 'y': 382.0}, 'text': '은수'},
        ],
      },
      solvable: {
        'problem_type': 'division_reasoning_multiple_choice',
        'given': [
          {'ref': 'obj.speaker.left', 'value': '현태'},
          {'ref': 'obj.speaker.right', 'value': '은수'},
        ],
        'target': {
          'ref': 'answer.target',
          'type': 'person_name',
          'description': '문제를 바르게 설명한 사람의 이름',
        },
        'answer': {
          'type': 'person_name',
          'description': '문제를 바르게 설명한 사람의 이름',
          'value': '현태',
          'choices': [],
        },
      },
      semantic: const {},
    );

    expect(
      content.choices,
      equals([
        '1. 현태',
        '2. 은수',
      ]),
    );
    expect(isSameAnswer('1. 현태', content.correctAnswer), isTrue);
  });

  test('extracts person names as choices for S3_초등_3_008608', () {
    final content = ProblemContent(
      summary: const ProblemSummary(
        id: 'S3_초등_3_008608',
        grade: 3,
        subject: 'math',
        unit: 'division',
        type: 'selection_by_division_result',
        title: '몫이 다른 사람을 선택해 보세요.',
        path: '',
        raw: {},
      ),
      renderer: {
        'elements': [
          {'id': 'slot.q1.text', 'type': 'text', 'attributes': {'x': 125.0, 'y': 55.0}, 'text': '몫이 다른 사람을 선택해 보세요.'},
          {'id': 'slot.box.left.text.text', 'type': 'text', 'attributes': {'x': 170.0, 'y': 140.0}, 'text': '30 ÷ 3'},
          {'id': 'slot.box.mid.text.text', 'type': 'text', 'attributes': {'x': 385.0, 'y': 145.0}, 'text': '40 ÷ 2'},
          {'id': 'slot.box.right.text.text', 'type': 'text', 'attributes': {'x': 610.0, 'y': 145.0}, 'text': '70 ÷ 7'},
          {'id': 'slot.name.left.text', 'type': 'text', 'attributes': {'x': 190.0, 'y': 305.0}, 'text': '은재'},
          {'id': 'slot.name.mid.text', 'type': 'text', 'attributes': {'x': 415.0, 'y': 305.0}, 'text': '성환'},
          {'id': 'slot.name.right.text', 'type': 'text', 'attributes': {'x': 635.0, 'y': 305.0}, 'text': '기영'},
        ],
      },
      solvable: {
        'problem_type': 'selection_by_division_result',
        'given': [
          {'ref': 'obj.expr.1', 'value': {'text': '30 ÷ 3'}},
          {'ref': 'obj.expr.2', 'value': {'text': '40 ÷ 2'}},
          {'ref': 'obj.expr.3', 'value': {'text': '70 ÷ 7'}},
          {'ref': 'obj.person.1', 'value': '은재'},
          {'ref': 'obj.person.2', 'value': '성환'},
          {'ref': 'obj.person.3', 'value': '기영'},
        ],
        'target': {
          'ref': 'answer.target',
          'type': 'selected_person',
          'description': '몫이 다른 사람',
        },
        'answer': {
          'type': 'selected_person',
          'description': '몫이 다른 사람',
          'value': '성환',
          'choices': [],
        },
      },
      semantic: const {},
    );

    expect(
      content.choices,
      equals([
        '1. 은재',
        '2. 성환',
        '3. 기영',
      ]),
    );
    expect(isSameAnswer('2. 성환', content.correctAnswer), isTrue);
  });

  test('creates O and X choices for divisibility judgment in S3_초등_3_008612', () {
    final content = ProblemContent(
      summary: const ProblemSummary(
        id: 'S3_초등_3_008612',
        grade: 3,
        subject: 'math',
        unit: 'division',
        type: 'divisibility_judgment',
        title: '다음 나눗셈이 나누어떨어지면 O표, 나누어떨어지지 않으면 X표를 선택하세요.',
        path: '',
        raw: {},
      ),
      renderer: {
        'elements': [
          {'id': 'slot.q.text.text', 'type': 'text', 'attributes': {'x': 75.0, 'y': 55.0}, 'text': '다음 나눗셈이 나누어떨어지면 O표,'},
          {'id': 'slot.q.text.copy2.text', 'type': 'text', 'attributes': {'x': 75.0, 'y': 100.0}, 'text': '나누어떨어지지 않으면 X표를 선택하세요.'},
          {'id': 'slot.expr.text.text', 'type': 'text', 'attributes': {'x': 280.0, 'y': 190.0}, 'text': '28 ÷ 3'},
        ],
      },
      solvable: {
        'problem_type': 'divisibility_judgment',
        'given': [
          {'ref': 'obj.dividend', 'value': 28},
          {'ref': 'obj.divisor', 'value': 3},
        ],
        'target': {
          'ref': 'answer.target',
          'type': 'selection_symbol',
          'description': '정답 기호',
        },
        'answer': {
          'type': 'selection_symbol',
          'description': '정답 기호',
          'value': 'X',
          'choices': [],
        },
      },
      semantic: const {},
    );

    expect(
      content.choices,
      equals([
        'O',
        'X',
      ]),
    );
    expect(isSameAnswer('X', content.correctAnswer), isTrue);
    expect(isSameAnswer('O', content.correctAnswer), isFalse);
  });
}

const _summary = ProblemSummary(
  id: 'multi-choice',
  grade: 3,
  subject: 'math',
  unit: 'multiplication',
  type: 'choice',
  title: 'multi choice',
  path: '',
  raw: {},
);

const _multiChoiceContent = ProblemContent(
  summary: _summary,
  semantic: {},
  renderer: {},
  solvable: {
    'answer': {
      'choices': ['80 x 40', '62 x 50', '90 x 30', '43 x 60'],
      'answer_key': [
        {'id': 'choice.1', 'value': '80 x 40'},
        {'id': 'choice.2', 'value': '62 x 50'},
      ],
      'target': {'type': 'multiple_choice_values'},
    },
  },
);

const _duplicateChoiceContent = ProblemContent(
  summary: _summary,
  semantic: {},
  renderer: {},
  solvable: {
    'answer': {
      'choices': ['80 x 40', '80 x 40', '90 x 30'],
      'answer_key': [
        {'id': 'choice.1', 'value': '80 x 40'},
        {'id': 'choice.2', 'value': '80 x 40'},
      ],
      'target': {'type': 'multiple_choice_values'},
    },
  },
);
