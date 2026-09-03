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

    expect(draft, equals('80 x 40 / 62 x 50'));

    await tester.tap(find.byType(FilledButton));
    await tester.pumpAndSettle();

    expect(submitted, equals('80 x 40 / 62 x 50'));
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

    expect(submitted, equals('80 x 40 / 80 x 40'));
  });

  testWidgets('allows selecting choice groups for multi-question problems',
      (tester) async {
    var submitted = '';

    const choiceGroupContent = ProblemContent(
      summary: _summary,
      semantic: {},
      renderer: {},
      solvable: {
        'answer': {
          'choice_groups': [
            {
              'label': '(1)번 문제',
              'choices': ['가 물병', '나 물병'],
            },
            {
              'label': '(2)번 문제',
              'choices': ['가 물병', '나 물병'],
            },
          ],
          'choices': ['가 물병', '나 물병'],
          'answer_key': ['나 물병', '나 물병'],
          'value': '나 물병, 나 물병',
          'target': {'type': 'multiple_choice_group'},
        },
      },
    );

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: AnswerPanel(
            content: choiceGroupContent,
            answerDraft: '',
            isCorrect: null,
            onAnswerChanged: (_) {},
            onSubmit: (value) => submitted = value,
          ),
        ),
      ),
    );

    expect(find.text('(1)번 문제'), findsOneWidget);
    expect(find.text('(2)번 문제'), findsOneWidget);
    expect(find.text('가 물병'), findsNWidgets(2));
    expect(find.text('나 물병'), findsNWidgets(2));

    await tester.tap(find.text('나 물병').at(0));
    await tester.tap(find.text('나 물병').at(1));
    await tester.pumpAndSettle();

    await tester.tap(find.byType(FilledButton));
    await tester.pumpAndSettle();

    expect(submitted, equals('나 물병, 나 물병'));
    expect(isSameAnswer(submitted, choiceGroupContent.correctAnswer), isTrue);
  });

  test('merges alternating split marker choices into complete choice items',
      () {
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

    expect(
        content.choices,
        equals([
          '1. 320+145',
          '2. 300+200',
          '3. 163+326',
          '4. 236+362',
          '5. 405+104',
        ]));
  });

  test('keeps standalone Hangul symbol choices separate for 008659', () {
    expect(_pointChoiceContent.choices, equals(['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ']));
  });

  testWidgets('renders 008659 symbols as four mutually exclusive choices',
      (tester) async {
    var draft = '';
    var submitted = '';

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: AnswerPanel(
            content: _pointChoiceContent,
            answerDraft: '',
            isCorrect: null,
            onAnswerChanged: (value) => draft = value,
            onSubmit: (value) => submitted = value,
          ),
        ),
      ),
    );

    expect(find.byType(ChoiceChip), findsNWidgets(4));
    for (final symbol in ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ']) {
      expect(find.text(symbol), findsOneWidget);
    }

    await tester.tap(find.text('ㄱ'));
    await tester.tap(find.text('ㄹ'));
    await tester.pumpAndSettle();

    final selectedChips = tester
        .widgetList<ChoiceChip>(find.byType(ChoiceChip))
        .where((chip) => chip.selected);
    expect(selectedChips, hasLength(1));
    expect(draft, equals('ㄹ'));

    await tester.tap(find.byType(FilledButton));
    await tester.pumpAndSettle();
    expect(submitted, equals('ㄹ'));
  });

  test('keeps all six standalone Hangul symbol choices separate for 008658',
      () {
    expect(
      _compassCenterChoiceContent.choices,
      equals(['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ']),
    );
  });

  testWidgets('renders 008658 symbols as six independent multi-select choices',
      (tester) async {
    var draft = '';

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: AnswerPanel(
            content: _compassCenterChoiceContent,
            answerDraft: '',
            isCorrect: null,
            onAnswerChanged: (value) => draft = value,
            onSubmit: (_) {},
          ),
        ),
      ),
    );

    expect(find.byType(ChoiceChip), findsNWidgets(6));
    for (final symbol in ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ']) {
      expect(find.text(symbol), findsOneWidget);
    }

    for (final symbol in ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ']) {
      await tester.tap(find.text(symbol));
    }
    await tester.pumpAndSettle();

    final selectedChips = tester
        .widgetList<ChoiceChip>(find.byType(ChoiceChip))
        .where((chip) => chip.selected);
    expect(selectedChips, hasLength(4));
    expect(draft, equals('ㄱ / ㄴ / ㄷ / ㄹ'));
  });

  test('provides comparison operator choices >, =, < for comparison problems (P3_1_01_00040_15604, P3_1_01_00040_00471_1)', () {
    const content15604 = ProblemContent(
      summary: ProblemSummary(
        id: 'P3_1_01_00040_15604',
        grade: 3,
        subject: 'math',
        unit: '덧셈과 뺄셈',
        type: 'text_answer_compare_addition_sums',
        title: '두 덧셈 결과의 크기 비교',
        path: '',
        raw: {},
      ),
      semantic: {
        'problem_type': 'text_answer_compare_addition_sums',
        'metadata': {'question': '크기를 비교하여 ○ 안에 >, <, =를 알맞게 써넣으시오.'},
        'answer': {'type': 'text', 'value': '<'},
      },
      renderer: {},
      solvable: {},
    );
    expect(content15604.choices, equals(['>', '=', '<']));

    const content00471 = ProblemContent(
      summary: ProblemSummary(
        id: 'P3_1_01_00040_00471_1',
        grade: 3,
        subject: 'math',
        unit: '덧셈과 뺄셈',
        type: 'multi_answer_expression_comparison',
        title: '덧셈식의 크기 비교',
        path: '',
        raw: {},
      ),
      semantic: {
        'problem_type': 'multi_answer_expression_comparison',
        'metadata': {'question': '크기를 비교하여 ○ 안에 >, =, <를 알맞게 써넣으시오.'},
        'answer': {
          'value': ['>'],
          'answer_key': [{'value': '>'}],
        },
      },
      renderer: {},
      solvable: {},
    );
    expect(content00471.choices, equals(['>', '=', '<']));
  });

  testWidgets('renders comparison operator choices and updates selection in AnswerPanel (P3_1_01_00040_15604)', (tester) async {
    var draft = '';
    const content15604 = ProblemContent(
      summary: ProblemSummary(
        id: 'P3_1_01_00040_15604',
        grade: 3,
        subject: 'math',
        unit: '덧셈과 뺄셈',
        type: 'text_answer_compare_addition_sums',
        title: '두 덧셈 결과의 크기 비교',
        path: '',
        raw: {},
      ),
      semantic: {
        'problem_type': 'text_answer_compare_addition_sums',
        'metadata': {'question': '크기를 비교하여 ○ 안에 >, <, =를 알맞게 써넣으시오.'},
        'answer': {'type': 'text', 'value': '<'},
      },
      renderer: {},
      solvable: {},
    );

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: AnswerPanel(
            content: content15604,
            answerDraft: '<',
            isCorrect: null,
            onAnswerChanged: (value) => draft = value,
            onSubmit: (_) {},
          ),
        ),
      ),
    );

    expect(find.byType(ChoiceChip), findsNWidgets(3));
    expect(find.text('>'), findsOneWidget);
    expect(find.text('='), findsOneWidget);
    expect(find.text('<'), findsOneWidget);

    final lessChip = tester.widget<ChoiceChip>(find.widgetWithText(ChoiceChip, '<'));
    expect(lessChip.selected, isTrue);

    await tester.tap(find.text('>'));
    await tester.pumpAndSettle();
    expect(draft, equals('>'));
  });

  testWidgets('renders comparison operator choices and updates selection in AnswerPanel (P3_1_01_00040_15610)', (tester) async {
    var draft = '';
    const content15610 = ProblemContent(
      summary: ProblemSummary(
        id: 'P3_1_01_00040_15610',
        grade: 3,
        subject: 'math',
        unit: '덧셈과 뺄셈',
        type: 'text_answer_compare_addition_expression_and_number',
        title: '덧셈식과 수의 크기 비교',
        path: '',
        raw: {},
      ),
      semantic: {
        'problem_type': 'text_answer_compare_addition_expression_and_number',
        'metadata': {'question': '○ 안에 >, =, <를 알맞게 써넣으시오.'},
        'answer': {'type': 'text', 'value': '>'},
      },
      renderer: {},
      solvable: {},
    );

    expect(content15610.choices, equals(['>', '=', '<']));

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: AnswerPanel(
            content: content15610,
            answerDraft: '>',
            isCorrect: null,
            onAnswerChanged: (value) => draft = value,
            onSubmit: (_) {},
          ),
        ),
      ),
    );

    expect(find.byType(ChoiceChip), findsNWidgets(3));
    expect(find.text('>'), findsOneWidget);
    expect(find.text('='), findsOneWidget);
    expect(find.text('<'), findsOneWidget);

    final greaterChip = tester.widget<ChoiceChip>(find.widgetWithText(ChoiceChip, '>'));
    expect(greaterChip.selected, isTrue);

    await tester.tap(find.text('='));
    await tester.pumpAndSettle();
    expect(draft, equals('='));
  });

  test('provides numbered option choices ① to ⑤ for numbered multiple choice problems (P3_1_01_00040_15608, P3_1_01_00040_15612)', () {
    const content15608 = ProblemContent(
      summary: ProblemSummary(
        id: 'P3_1_01_00040_15608',
        grade: 3,
        subject: 'math',
        unit: '덧셈과 뺄셈',
        type: 'multiple_choice_largest_addition_sum',
        title: '합이 가장 큰 덧셈식',
        path: '',
        raw: {},
      ),
      semantic: {
        'problem_type': 'multiple_choice_largest_addition_sum',
        'metadata': {'question': '다음 중 합이 가장 큰 것은 어느 것입니까?'},
        'answer': {'type': 'choice', 'value': 5},
      },
      renderer: {},
      solvable: {
        'inputs': {
          'target_label': '합이 가장 큰 덧셈식의 번호',
          'options': [
            {'number': 1, 'expression': '530 + 140'},
            {'number': 2, 'expression': '420 + 220'},
            {'number': 3, 'expression': '610 + 100'},
            {'number': 4, 'expression': '140 + 550'},
            {'number': 5, 'expression': '545 + 235'},
          ],
        },
      },
    );
    expect(content15608.choices, equals(['①', '②', '③', '④', '⑤']));

    const content15612 = ProblemContent(
      summary: ProblemSummary(
        id: 'P3_1_01_00040_15612',
        grade: 3,
        subject: 'math',
        unit: '덧셈과 뺄셈',
        type: 'multiple_choice_largest_sum_problem',
        title: '합이 가장 큰 식 찾기',
        path: '',
        raw: {},
      ),
      semantic: {
        'problem_type': 'multiple_choice_largest_sum_problem',
        'metadata': {'question': '다음 중 합이 가장 큰 것은 어느 것입니까?'},
        'answer': {'type': 'choice', 'value': 4},
      },
      renderer: {},
      solvable: {
        'inputs': {
          'target_label': '합이 가장 큰 덧셈식의 번호',
          'options': [
            {'number': 1, 'expression': '320 + 145'},
            {'number': 2, 'expression': '300 + 200'},
            {'number': 3, 'expression': '163 + 326'},
            {'number': 4, 'expression': '236 + 362'},
            {'number': 5, 'expression': '405 + 104'},
          ],
        },
      },
    );
    expect(content15612.choices, equals(['①', '②', '③', '④', '⑤']));
  });

  testWidgets('renders numbered choices and selects ⑤ for P3_1_01_00040_15608 in AnswerPanel', (tester) async {
    var draft = '';
    const content15608 = ProblemContent(
      summary: ProblemSummary(
        id: 'P3_1_01_00040_15608',
        grade: 3,
        subject: 'math',
        unit: '덧셈과 뺄셈',
        type: 'multiple_choice_largest_addition_sum',
        title: '합이 가장 큰 덧셈식',
        path: '',
        raw: {},
      ),
      semantic: {
        'problem_type': 'multiple_choice_largest_addition_sum',
        'metadata': {'question': '다음 중 합이 가장 큰 것은 어느 것입니까?'},
        'answer': {'type': 'choice', 'value': 5},
      },
      renderer: {},
      solvable: {
        'inputs': {
          'target_label': '합이 가장 큰 덧셈식의 번호',
          'options': [
            {'number': 1, 'expression': '530 + 140'},
            {'number': 2, 'expression': '420 + 220'},
            {'number': 3, 'expression': '610 + 100'},
            {'number': 4, 'expression': '140 + 550'},
            {'number': 5, 'expression': '545 + 235'},
          ],
        },
      },
    );

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: AnswerPanel(
            content: content15608,
            answerDraft: '5',
            isCorrect: null,
            onAnswerChanged: (value) => draft = value,
            onSubmit: (_) {},
          ),
        ),
      ),
    );

    expect(find.byType(ChoiceChip), findsNWidgets(5));
    expect(find.text('①'), findsOneWidget);
    expect(find.text('⑤'), findsOneWidget);

    final chip5 = tester.widget<ChoiceChip>(find.widgetWithText(ChoiceChip, '⑤'));
    expect(chip5.selected, isTrue);

    await tester.tap(find.text('③'));
    await tester.pumpAndSettle();
    expect(draft, equals('③'));
  });

  test(
      'merges grouped operator and number renderer elements into clean choices',
      () {
    const content = ProblemContent(
      summary: _summary,
      semantic: {},
      renderer: {
        'elements': [
          {
            'id': 'slot.choice_1_div.text',
            'source_ref': 'slot.choice_1_div',
            'text': '÷',
            'attributes': {'x': 179.996, 'y': 140.0}
          },
          {
            'id': 'slot.choice_1_num.text',
            'source_ref': 'slot.choice_1_num',
            'text': '6',
            'attributes': {'x': 210.996, 'y': 140.0}
          },
          {
            'id': 'slot.choice_2_div.text',
            'source_ref': 'slot.choice_2_div',
            'text': '÷',
            'attributes': {'x': 367.996, 'y': 140.0}
          },
          {
            'id': 'slot.choice_2_num.text',
            'source_ref': 'slot.choice_2_num',
            'text': '5',
            'attributes': {'x': 396.996, 'y': 140.0}
          },
          {
            'id': 'slot.choice_3_div.text',
            'source_ref': 'slot.choice_3_div',
            'text': '÷',
            'attributes': {'x': 562.996, 'y': 140.0}
          },
          {
            'id': 'slot.choice_3_num.text',
            'source_ref': 'slot.choice_3_num',
            'text': '9',
            'attributes': {'x': 597.996, 'y': 140.0}
          },
          {
            'id': 'slot.choice_4_div.text',
            'source_ref': 'slot.choice_4_div',
            'text': '÷',
            'attributes': {'x': 747.996, 'y': 140.0}
          },
          {
            'id': 'slot.choice_4_num.text',
            'source_ref': 'slot.choice_4_num',
            'text': '4',
            'attributes': {'x': 782.996, 'y': 140.0}
          },
        ],
      },
      solvable: {},
    );

    expect(
        content.choices,
        equals([
          '1. ÷ 6',
          '2. ÷ 5',
          '3. ÷ 9',
          '4. ÷ 4',
        ]));
  });

  test(
      'extracts choices from solvable given expressions when choices array is empty',
      () {
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

    expect(
        content.choices,
        equals([
          '1. 24 ÷ 7',
          '2. 49 ÷ 5',
        ]));
  });

  testWidgets('renders numbered expression option maps as readable choices',
      (tester) async {
    const content = ProblemContent(
      summary: ProblemSummary(
        id: 'P3_1_01_00040_15608',
        grade: 3,
        subject: 'math',
        unit: '덧셈과 뺄셈',
        type: 'multiple_choice_largest_addition_sum',
        title: '합이 가장 큰 덧셈식',
        path: '',
        raw: {},
      ),
      semantic: {},
      renderer: {'elements': []},
      solvable: {
        'problem_type': 'multiple_choice_largest_addition_sum',
        'inputs': {
          'options': [
            {'number': 1, 'expression': '530 + 140'},
            {'number': 2, 'expression': '420 + 220'},
            {'number': 3, 'expression': '610 + 100'},
            {'number': 4, 'expression': '140 + 550'},
            {'number': 5, 'expression': '545 + 235'},
          ],
        },
        'target': {'type': 'choice'},
        'answer': {'type': 'choice', 'value': 5},
      },
    );

    expect(
        content.choices,
        equals([
          '①',
          '②',
          '③',
          '④',
          '⑤',
        ]));
    expect(isSameAnswer(content.choices.last, content.correctAnswer), isTrue);

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: AnswerPanel(
            content: content,
            answerDraft: '',
            isCorrect: null,
            onAnswerChanged: (_) {},
            onSubmit: (_) {},
          ),
        ),
      ),
    );

    expect(find.text('①'), findsOneWidget);
    expect(find.text('⑤'), findsOneWidget);
    expect(find.textContaining('{number:'), findsNothing);
  });

  test('does not treat word problem given entities as multiple choice options',
      () {
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

  test('does not treat diagram item labels in P3_1_01_00040_02164_1 as choices',
      () {
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
            'attributes': {
              'x': 71.5,
              'y': 122.1,
              'data-semantic-role': 'given_value'
            },
            'text': '259',
          },
          {
            'id': 'slot.item_1_left_value.text',
            'type': 'text',
            'attributes': {
              'x': 245.2,
              'y': 122.6,
              'data-semantic-role': 'given_value'
            },
            'text': '236',
          },
          {
            'id': 'slot.item_1_right_value.text',
            'type': 'text',
            'attributes': {
              'x': 293.2,
              'y': 122.6,
              'data-semantic-role': 'given_value'
            },
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

  test('does not treat <보기> options text in P3_1_01_00040_15472 as choices',
      () {
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
            'interaction': {
              'type': 'input',
              'role': 'answer',
              'value_type': 'digit'
            },
          },
        ],
      },
      solvable: {
        'problem_type': 'multi_numeric_digit_card_addition_completion',
        'given': [
          {
            'ref': 'set.digit_cards',
            'value': [1, 5, 2, 7]
          },
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

  test('extracts choice blank square box for S3_elem_3_008588', () {
    final content = ProblemContent(
      summary: const ProblemSummary(
        id: 'S3_elem_3_008588',
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
          {
            'id': 'slot.box.rect',
            'type': 'rect',
            'attributes': {'width': 745.0, 'height': 80.0}
          },
          {
            'id': 'slot.choice_1_blank.rect',
            'type': 'rect',
            'attributes': {
              'x': 147.996,
              'y': 120.0,
              'width': 25.0,
              'height': 25.0
            }
          },
          {
            'id': 'slot.choice_1_div.text',
            'type': 'text',
            'attributes': {'x': 179.996, 'y': 140.0},
            'text': '÷'
          },
          {
            'id': 'slot.choice_1_num.text',
            'type': 'text',
            'attributes': {'x': 210.996, 'y': 140.0},
            'text': '6'
          },
          {
            'id': 'slot.choice_2_blank.rect',
            'type': 'rect',
            'attributes': {
              'x': 337.996,
              'y': 120.0,
              'width': 25.0,
              'height': 25.0
            }
          },
          {
            'id': 'slot.choice_2_div.text',
            'type': 'text',
            'attributes': {'x': 367.996, 'y': 140.0},
            'text': '÷'
          },
          {
            'id': 'slot.choice_2_num.text',
            'type': 'text',
            'attributes': {'x': 396.996, 'y': 140.0},
            'text': '5'
          },
          {
            'id': 'slot.choice_3_blank.rect',
            'type': 'rect',
            'attributes': {
              'x': 532.996,
              'y': 120.0,
              'width': 25.0,
              'height': 25.0
            }
          },
          {
            'id': 'slot.choice_3_div.text',
            'type': 'text',
            'attributes': {'x': 562.996, 'y': 140.0},
            'text': '÷'
          },
          {
            'id': 'slot.choice_3_num.text',
            'type': 'text',
            'attributes': {'x': 597.996, 'y': 140.0},
            'text': '9'
          },
          {
            'id': 'slot.choice_4_blank.rect',
            'type': 'rect',
            'attributes': {
              'x': 712.996,
              'y': 120.0,
              'width': 25.0,
              'height': 25.0
            }
          },
          {
            'id': 'slot.choice_4_div.text',
            'type': 'text',
            'attributes': {'x': 747.996, 'y': 140.0},
            'text': '÷'
          },
          {
            'id': 'slot.choice_4_num.text',
            'type': 'text',
            'attributes': {'x': 782.996, 'y': 140.0},
            'text': '4'
          },
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

  test('extracts person names as choices for S3_elem_3_008590', () {
    final content = ProblemContent(
      summary: const ProblemSummary(
        id: 'S3_elem_3_008590',
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
          {
            'id': 'slot.q1',
            'type': 'text',
            'attributes': {'x': 155.0, 'y': 40.0},
            'text': '문제를 바르게 설명한 사람을 선택하세요.'
          },
          {
            'id': 'slot.opt1.text',
            'type': 'text',
            'attributes': {'x': 222.5, 'y': 208.5},
            'text': '몫은\n13이야.'
          },
          {
            'id': 'slot.name.opt1.text',
            'type': 'text',
            'attributes': {'x': 222.5, 'y': 430.0},
            'text': '형우'
          },
          {
            'id': 'slot.opt2.text',
            'type': 'text',
            'attributes': {'x': 477.5, 'y': 208.5},
            'text': '나머지는\n5보다 작아.'
          },
          {
            'id': 'slot.name.opt2.text',
            'type': 'text',
            'attributes': {'x': 477.5, 'y': 430.0},
            'text': '희영'
          },
          {
            'id': 'slot.opt3.text',
            'type': 'text',
            'attributes': {'x': 707.5, 'y': 208.5},
            'text': '나누어떨어지지\n않아.'
          },
          {
            'id': 'slot.name.opt3.text',
            'type': 'text',
            'attributes': {'x': 707.5, 'y': 430.0},
            'text': '성태'
          },
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

  test('extracts choice blank square box for S3_elem_3_008592', () {
    final content = ProblemContent(
      summary: const ProblemSummary(
        id: 'S3_elem_3_008592',
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
          {
            'id': 'slot.choice.1.no.text',
            'type': 'text',
            'attributes': {'x': 75.846, 'y': 105.0},
            'text': '①'
          },
          {
            'id': 'slot.choice.1.box.rect',
            'type': 'rect',
            'attributes': {
              'x': 123.008,
              'y': 80.0,
              'width': 25.0,
              'height': 25.0
            }
          },
          {
            'id': 'slot.choice.1.div.text',
            'type': 'text',
            'attributes': {'x': 161.996, 'y': 106.0},
            'text': '÷'
          },
          {
            'id': 'slot.choice.1.den.text',
            'type': 'text',
            'attributes': {'x': 200.032, 'y': 103.0},
            'text': '5'
          },
          {
            'id': 'slot.choice.2.no.text',
            'type': 'text',
            'attributes': {'x': 276.994, 'y': 105.0},
            'text': '②'
          },
          {
            'id': 'slot.choice.2.box.rect',
            'type': 'rect',
            'attributes': {'x': 321.0, 'y': 80.0, 'width': 24.0, 'height': 24.0}
          },
          {
            'id': 'slot.choice.2.div.text',
            'type': 'text',
            'attributes': {'x': 360.0, 'y': 103.0},
            'text': '÷'
          },
          {
            'id': 'slot.choice.2.den.text',
            'type': 'text',
            'attributes': {'x': 396.998, 'y': 102.0},
            'text': '4'
          },
          {
            'id': 'slot.choice.3.no.text',
            'type': 'text',
            'attributes': {'x': 463.984, 'y': 104.0},
            'text': '③'
          },
          {
            'id': 'slot.choice.3.box.rect',
            'type': 'rect',
            'attributes': {
              'x': 510.953,
              'y': 80.0,
              'width': 24.0,
              'height': 24.0
            }
          },
          {
            'id': 'slot.choice.3.div.text',
            'type': 'text',
            'attributes': {'x': 545.953, 'y': 101.0},
            'text': '÷'
          },
          {
            'id': 'slot.choice.3.den.text',
            'type': 'text',
            'attributes': {'x': 577.953, 'y': 101.0},
            'text': '8'
          },
          {
            'id': 'slot.choice.4.no.text',
            'type': 'text',
            'attributes': {'x': 75.888, 'y': 184.0},
            'text': '④'
          },
          {
            'id': 'slot.choice.4.box.rect',
            'type': 'rect',
            'attributes': {
              'x': 122.0,
              'y': 160.0,
              'width': 25.0,
              'height': 25.0
            }
          },
          {
            'id': 'slot.choice.4.div.text',
            'type': 'text',
            'attributes': {'x': 162.999, 'y': 184.0},
            'text': '÷'
          },
          {
            'id': 'slot.choice.4.den.text',
            'type': 'text',
            'attributes': {'x': 200.032, 'y': 181.0},
            'text': '7'
          },
          {
            'id': 'slot.choice.5.no.text',
            'type': 'text',
            'attributes': {'x': 279.0, 'y': 183.0},
            'text': '⑤'
          },
          {
            'id': 'slot.choice.5.box.rect',
            'type': 'rect',
            'attributes': {
              'x': 319.992,
              'y': 158.0,
              'width': 25.0,
              'height': 25.0
            }
          },
          {
            'id': 'slot.choice.5.div.text',
            'type': 'text',
            'attributes': {'x': 362.0, 'y': 182.0},
            'text': '÷'
          },
          {
            'id': 'slot.choice.5.den.text',
            'type': 'text',
            'attributes': {'x': 399.0, 'y': 179.0},
            'text': '6'
          },
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

  test(
      'extracts circled hangul consonant and blank square box for S3_elem_3_008601',
      () {
    final content = ProblemContent(
      summary: const ProblemSummary(
        id: 'S3_elem_3_008601',
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
          {
            'id': 'slot.box.rect',
            'type': 'rect',
            'attributes': {'width': 760.0, 'height': 80.0}
          },
          {
            'id': 'slot.opt1.sym.text',
            'type': 'text',
            'attributes': {'x': 165.0, 'y': 150.0},
            'text': '㉠'
          },
          {
            'id': 'slot.opt1.blank.rect',
            'type': 'rect',
            'attributes': {
              'x': 210.0,
              'y': 125.0,
              'width': 25.0,
              'height': 25.0
            }
          },
          {
            'id': 'slot.opt1.div.text',
            'type': 'text',
            'attributes': {'x': 245.0, 'y': 150.0},
            'text': '÷'
          },
          {
            'id': 'slot.opt1.num.text',
            'type': 'text',
            'attributes': {'x': 285.0, 'y': 150.0},
            'text': '2'
          },
          {
            'id': 'slot.opt2.sym.text',
            'type': 'text',
            'attributes': {'x': 380.0, 'y': 150.0},
            'text': '㉡'
          },
          {
            'id': 'slot.opt2.blank.rect',
            'type': 'rect',
            'attributes': {
              'x': 425.0,
              'y': 125.0,
              'width': 25.0,
              'height': 25.0
            }
          },
          {
            'id': 'slot.opt2.div.text',
            'type': 'text',
            'attributes': {'x': 455.0, 'y': 150.0},
            'text': '÷'
          },
          {
            'id': 'slot.opt2.num.text',
            'type': 'text',
            'attributes': {'x': 490.0, 'y': 150.0},
            'text': '7'
          },
          {
            'id': 'slot.opt3.sym.text',
            'type': 'text',
            'attributes': {'x': 585.0, 'y': 150.0},
            'text': '㉢'
          },
          {
            'id': 'slot.opt3.blank.rect',
            'type': 'rect',
            'attributes': {
              'x': 635.0,
              'y': 125.0,
              'width': 25.0,
              'height': 25.0
            }
          },
          {
            'id': 'slot.opt3.div.text',
            'type': 'text',
            'attributes': {'x': 670.0, 'y': 150.0},
            'text': '÷'
          },
          {
            'id': 'slot.opt3.num.text',
            'type': 'text',
            'attributes': {'x': 705.0, 'y': 150.0},
            'text': '5'
          },
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

  test('extracts choices with expressions for S3_elem_3_008603', () {
    final content = ProblemContent(
      summary: const ProblemSummary(
        id: 'S3_elem_3_008603',
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
          {
            'id': 'slot.box.rect',
            'type': 'rect',
            'attributes': {
              'x': 197.011,
              'y': 112.0,
              'width': 380.0,
              'height': 80.0
            }
          },
          {
            'id': 'slot.q1.text',
            'type': 'text',
            'attributes': {'x': 52.011, 'y': 71.0},
            'text': '나누어떨어지는 나눗셈식을 찾아 기호를 선택해 보세요.'
          },
          {
            'id': 'slot.v1.text',
            'type': 'text',
            'attributes': {'x': 227.011, 'y': 162.0},
            'text': '㉠ 64 ÷ 6'
          },
          {
            'id': 'slot.v2.text',
            'type': 'text',
            'attributes': {'x': 407.011, 'y': 162.0},
            'text': '㉡ 92 ÷ 4'
          },
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

  test('extracts person names as choices for S3_elem_3_008604', () {
    final content = ProblemContent(
      summary: const ProblemSummary(
        id: 'S3_elem_3_008604',
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
          {
            'id': 'slot.q1',
            'type': 'text',
            'attributes': {'x': 12.0, 'y': 28.0},
            'text': '문제를 바르게 설명한 사람의 이름을 선택하세요.'
          },
          {
            'id': 'slot.expr_text',
            'type': 'text',
            'attributes': {'x': 442.0, 'y': 84.0},
            'text': '67 ÷ 5'
          },
          {
            'id': 'slot.left.text',
            'type': 'text',
            'attributes': {'x': 257.0, 'y': 145.0},
            'text': '몫은\n13이야.'
          },
          {
            'id': 'slot.name.left.text',
            'type': 'text',
            'attributes': {'x': 257.0, 'y': 382.0},
            'text': '현태'
          },
          {
            'id': 'slot.right.text',
            'type': 'text',
            'attributes': {'x': 547.0, 'y': 145.0},
            'text': '나머지는 0으로\n나누어떨어져.'
          },
          {
            'id': 'slot.name.right.text',
            'type': 'text',
            'attributes': {'x': 547.0, 'y': 382.0},
            'text': '은수'
          },
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

  test('extracts person names as choices for S3_elem_3_008608', () {
    final content = ProblemContent(
      summary: const ProblemSummary(
        id: 'S3_elem_3_008608',
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
          {
            'id': 'slot.q1.text',
            'type': 'text',
            'attributes': {'x': 125.0, 'y': 55.0},
            'text': '몫이 다른 사람을 선택해 보세요.'
          },
          {
            'id': 'slot.box.left.text.text',
            'type': 'text',
            'attributes': {'x': 170.0, 'y': 140.0},
            'text': '30 ÷ 3'
          },
          {
            'id': 'slot.box.mid.text.text',
            'type': 'text',
            'attributes': {'x': 385.0, 'y': 145.0},
            'text': '40 ÷ 2'
          },
          {
            'id': 'slot.box.right.text.text',
            'type': 'text',
            'attributes': {'x': 610.0, 'y': 145.0},
            'text': '70 ÷ 7'
          },
          {
            'id': 'slot.name.left.text',
            'type': 'text',
            'attributes': {'x': 190.0, 'y': 305.0},
            'text': '은재'
          },
          {
            'id': 'slot.name.mid.text',
            'type': 'text',
            'attributes': {'x': 415.0, 'y': 305.0},
            'text': '성환'
          },
          {
            'id': 'slot.name.right.text',
            'type': 'text',
            'attributes': {'x': 635.0, 'y': 305.0},
            'text': '기영'
          },
        ],
      },
      solvable: {
        'problem_type': 'selection_by_division_result',
        'given': [
          {
            'ref': 'obj.expr.1',
            'value': {'text': '30 ÷ 3'}
          },
          {
            'ref': 'obj.expr.2',
            'value': {'text': '40 ÷ 2'}
          },
          {
            'ref': 'obj.expr.3',
            'value': {'text': '70 ÷ 7'}
          },
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

  test('creates O and X choices for divisibility judgment in S3_elem_3_008612',
      () {
    final content = ProblemContent(
      summary: const ProblemSummary(
        id: 'S3_elem_3_008612',
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
          {
            'id': 'slot.q.text.text',
            'type': 'text',
            'attributes': {'x': 75.0, 'y': 55.0},
            'text': '다음 나눗셈이 나누어떨어지면 O표,'
          },
          {
            'id': 'slot.q.text.copy2.text',
            'type': 'text',
            'attributes': {'x': 75.0, 'y': 100.0},
            'text': '나누어떨어지지 않으면 X표를 선택하세요.'
          },
          {
            'id': 'slot.expr.text.text',
            'type': 'text',
            'attributes': {'x': 280.0, 'y': 190.0},
            'text': '28 ÷ 3'
          },
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

  test('sorts 2-column renderer choices sequentially in numerical order (P3_1_01_00040_15630)', () {
    const content = ProblemContent(
      summary: ProblemSummary(
        id: 'P3_1_01_00040_15630',
        grade: 3,
        subject: 'math',
        unit: '덧셈과 뺄셈',
        type: 'multiple_choice_difference_identification',
        title: '차가 123인 두 수 찾기',
        path: '',
        raw: {},
      ),
      semantic: {},
      renderer: {
        'elements': [
          {
            'id': 'slot.choice1.text',
            'type': 'text',
            'attributes': {'x': 49.6, 'y': 65.189},
            'text': '① 647, 341',
          },
          {
            'id': 'slot.choice2.text',
            'type': 'text',
            'attributes': {'x': 49.6, 'y': 87.189},
            'text': '② 488, 227',
          },
          {
            'id': 'slot.choice3.text',
            'type': 'text',
            'attributes': {'x': 49.6, 'y': 109.189},
            'text': '③ 847, 740',
          },
          {
            'id': 'slot.choice4.text',
            'type': 'text',
            'attributes': {'x': 160.4, 'y': 65.227},
            'text': '④ 528, 405',
          },
          {
            'id': 'slot.choice5.text',
            'type': 'text',
            'attributes': {'x': 160.4, 'y': 87.227},
            'text': '⑤ 386, 223',
          },
        ],
      },
      solvable: {
        'problem_type': 'multiple_choice_difference_identification',
        'target': {'type': 'choice_expression'},
        'answer': {'type': 'select_expression', 'value': '528, 405'},
      },
    );

    expect(
      content.choices,
      equals([
        '1. 647, 341',
        '2. 488, 227',
        '3. 847, 740',
        '4. 528, 405',
        '5. 386, 223',
      ]),
    );
  });

  testWidgets('renders multiple input fields for multi_numeric subquestion problems (P3_1_01_00040_15726)', (tester) async {
    const content = ProblemContent(
      summary: ProblemSummary(
        id: 'P3_1_01_00040_15726',
        grade: 3,
        subject: 'math',
        unit: '덧셈과 뺄셈',
        type: 'base_ten_model_addition_multi_answer',
        title: '수 모형으로 알아보는 262와 271의 합',
        path: '',
        raw: {},
      ),
      semantic: {
        'answer': {
          'type': 'multi_numeric',
          'value': [3, 1, 3, 4, 533],
          'values': [
            {'value': 3, 'unit': '개', 'target_ref': 'quantity.ones_sum'},
            {'value': 1, 'unit': '개', 'target_ref': 'quantity.regrouped_hundreds'},
            {'value': 3, 'unit': '개', 'target_ref': 'quantity.remaining_tens'},
            {'value': 4, 'unit': '개', 'target_ref': 'quantity.direct_hundreds_sum'},
            {'value': 533, 'unit': '', 'target_ref': 'sum.total'},
          ],
        },
      },
      renderer: {
        'elements': [
          {'id': 'slot.instruction.text', 'type': 'text', 'text': '262+271을 수 모형으로 알아보시오.'},
        ],
      },
      solvable: {
        'problem_type': 'base_ten_model_addition_multi_answer',
        'inputs': {
          'unknowns': [
            {'ref': 'quantity.ones_sum', 'label': '낱개 모형끼리 더한 개수', 'unit': '개'},
            {'ref': 'quantity.regrouped_hundreds', 'label': '십 모형을 바꾸어 얻은 백 모형의 개수', 'unit': '개'},
            {'ref': 'quantity.remaining_tens', 'label': '받아올림 뒤 남은 십 모형의 개수', 'unit': '개'},
            {'ref': 'quantity.direct_hundreds_sum', 'label': '백 모형끼리 직접 더한 개수', 'unit': '개'},
            {'ref': 'sum.total', 'label': '262와 271의 합', 'unit': ''},
          ],
        },
        'answer': {
          'type': 'multi_numeric',
          'value': [3, 1, 3, 4, 533],
        },
      },
    );

    expect(content.multiAnswerFields.length, equals(5));
    expect(content.multiAnswerFields[0].label, equals('낱개 모형끼리 더한 개수'));
    expect(content.multiAnswerFields[0].unit, equals('개'));
    expect(content.multiAnswerFields[4].label, equals('262와 271의 합'));

    String changedAnswer = '';
    String submittedAnswer = '';

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: AnswerPanel(
            content: content,
            answerDraft: '',
            isCorrect: null,
            onAnswerChanged: (value) => changedAnswer = value,
            onSubmit: (value) => submittedAnswer = value,
          ),
        ),
      ),
    );

    expect(find.byKey(const ValueKey('multi-input-field-0')), findsOneWidget);
    expect(find.byKey(const ValueKey('multi-input-field-1')), findsOneWidget);
    expect(find.byKey(const ValueKey('multi-input-field-2')), findsOneWidget);
    expect(find.byKey(const ValueKey('multi-input-field-3')), findsOneWidget);
    expect(find.byKey(const ValueKey('multi-input-field-4')), findsOneWidget);

    await tester.enterText(find.byKey(const ValueKey('multi-input-field-0')), '3');
    await tester.enterText(find.byKey(const ValueKey('multi-input-field-1')), '1');
    await tester.enterText(find.byKey(const ValueKey('multi-input-field-2')), '3');
    await tester.enterText(find.byKey(const ValueKey('multi-input-field-3')), '4');
    await tester.enterText(find.byKey(const ValueKey('multi-input-field-4')), '533');
    await tester.pump();

    expect(changedAnswer, equals('3 / 1 / 3 / 4 / 533'));

    await tester.tap(find.text('정답 확인'));
    await tester.pump();

    expect(submittedAnswer, equals('3 / 1 / 3 / 4 / 533'));
    expect(isSameAnswer(submittedAnswer, content.correctAnswer), isTrue);
  });

  test('formats choices with number labels and expressions (S3_elem_3_008555)', () {
    const content = ProblemContent(
      summary: ProblemSummary(
        id: 'S3_elem_3_008555',
        grade: 3,
        subject: 'math',
        unit: '덧셈과 뺄셈',
        type: 'multiple_choice_comparison',
        title: '500보다 큰 계산 결과 찾기',
        path: '',
        raw: {},
      ),
      semantic: {
        'answer': {
          'choices': [
            {'id': 'choice.1', 'label': '1', 'text': '35 × 13'},
            {'id': 'choice.2', 'label': '2', 'text': '28 × 19'},
          ],
          'answer_key': [
            {'id': 'choice.2', 'value': '28 × 19'},
          ],
          'value': '28 × 19',
        },
      },
      renderer: {},
      solvable: {},
    );

    expect(
      content.choices,
      equals([
        '1. 35 × 13',
        '2. 28 × 19',
      ]),
    );
    expect(isSameAnswer('2. 28 × 19', content.correctAnswer), isTrue);
    expect(isSameAnswer(content.choices[1], '2'), isTrue);
    expect(isSameAnswer('28x19', content.correctAnswer), isTrue);
    expect(isSameAnswer('1. 35 × 13', content.correctAnswer), isFalse);
  });

  test('extracts Hangul symbol choices for choice_symbol problems (S3_elem_3_008780)', () {
    const content = ProblemContent(
      summary: ProblemSummary(
        id: 'S3_elem_3_008780',
        grade: 3,
        subject: 'math',
        unit: '들이와 무게',
        type: 'compare_capacity_addition',
        title: '계산하여 들이가 더 많은 것의 기호를 선택하세요',
        path: '',
        raw: {},
      ),
      semantic: {
        'metadata': {'instruction': '계산하여 들이가 더 많은 것의 기호를 선택하세요.'},
        'domain': {
          'objects': [
            {'id': 'obj.choice_a', 'type': 'expression', 'description': '4200 mL + 1400 mL'},
            {'id': 'obj.choice_b', 'type': 'expression', 'description': '2 L 800 mL + 3 L 300 mL'},
          ],
        },
        'answer': {
          'target': {'type': 'choice_symbol', 'description': '들이가 더 많은 것의 기호'},
          'value': 'ㄴ',
        },
      },
      renderer: {},
      solvable: {
        'target': {'type': 'choice_symbol'},
        'answer': {'value': 'ㄴ'},
      },
    );

    expect(content.choices, equals(['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ']));
    expect(isSameAnswer(content.choices[1], content.correctAnswer), isTrue);
  });

  test('extracts circled Hangul symbol choices for incorrect_weight_statement (S3_elem_3_008782)', () {
    const content = ProblemContent(
      summary: ProblemSummary(
        id: 'S3_elem_3_008782',
        grade: 3,
        subject: 'math',
        unit: '들이와 무게',
        type: 'unit_conversion_mcq',
        title: '무게의 단위를 잘못 나타낸 것을 찾아 기호를 선택하세요.',
        path: '',
        raw: {},
      ),
      semantic: {
        'metadata': {'instruction': '보기 중 옳지 않은 단위를 고르기'},
        'domain': {
          'objects': [
            {'id': 'obj.choice.1', 'symbol': '㉠', 'expression': '3 kg 40 g = 3040 g'},
            {'id': 'obj.choice.2', 'symbol': '㉡', 'expression': '4000 kg = 4 t'},
            {'id': 'obj.choice.3', 'symbol': '㉢', 'expression': '2 kg 700 g = 2070 g'},
          ],
        },
        'answer': {
          'target': {'type': 'incorrect_weight_statement'},
          'value': '㉢',
        },
      },
      renderer: {},
      solvable: {},
    );

    expect(content.choices, equals(['㉠', '㉡', '㉢']));
    expect(isSameAnswer(content.choices[2], content.correctAnswer), isTrue);
    expect(isSameAnswer('ㄷ', content.correctAnswer), isTrue);
  });

  test('matches multi-choice selection of options 2 and 5 for S3_elem_3_008605', () {
    const content = ProblemContent(
      summary: ProblemSummary(
        id: 'S3_elem_3_008605',
        grade: 3,
        subject: 'math',
        unit: '나눗셈',
        type: 'multiple_choice_divisibility',
        title: '3으로 나누어떨어지는 수가 아닌 것',
        path: '',
        raw: {},
      ),
      renderer: {
        'elements': [
          {'id': 'slot.c1', 'type': 'text', 'text': '① 27'},
          {'id': 'slot.c2', 'type': 'text', 'text': '② 56'},
          {'id': 'slot.c3', 'type': 'text', 'text': '③ 84'},
          {'id': 'slot.c4', 'type': 'text', 'text': '④ 63'},
          {'id': 'slot.c5', 'type': 'text', 'text': '⑤ 70'},
        ],
      },
      semantic: {
        'answer': {
          'target': {'type': 'selected_choices'},
          'value': [2, 5],
        },
      },
      solvable: {},
    );

    expect(
      content.choices,
      equals(['1. 27', '2. 56', '3. 84', '4. 63', '5. 70']),
    );
    expect(content.correctAnswer, equals('25'));
    expect(isSameAnswer('2. 56 / 5. 70', content.correctAnswer), isTrue);
    expect(isSameAnswer('2. 56, 5. 70', content.correctAnswer), isTrue);
    expect(isSameAnswer('2, 5', content.correctAnswer), isTrue);
    expect(isSameAnswer('5, 2', content.correctAnswer), isTrue);
    expect(isSameAnswer('2. 56 / 3. 84', content.correctAnswer), isFalse);
  });

  test('resolves division expression and matches choice 3 for S3_elem_3_008621', () {
    const content = ProblemContent(
      summary: ProblemSummary(
        id: 'S3_elem_3_008621',
        grade: 3,
        subject: 'math',
        unit: '나눗셈',
        type: 'multiple_choice',
        title: '몫이 다른 하나를 찾아 선택하세요.',
        path: '',
        raw: {},
      ),
      renderer: {
        'elements': [
          {'id': 'slot.opt1', 'type': 'text', 'text': '24 ÷ 2'},
          {'id': 'slot.opt2', 'type': 'text', 'text': '48 ÷ 4'},
          {'id': 'slot.opt3', 'type': 'text', 'text': '77 ÷ 7'},
        ],
      },
      semantic: {
        'domain': {
          'objects': [
            {'id': 'obj.opt1', 'type': 'division_expression', 'expression': '24 ÷ 2'},
            {'id': 'obj.opt2', 'type': 'division_expression', 'expression': '48 ÷ 4'},
            {'id': 'obj.opt3', 'type': 'division_expression', 'expression': '77 ÷ 7'},
          ],
        },
        'answer': {
          'target': {'type': 'selected_option'},
          'value': 77,
        },
      },
      solvable: {},
    );

    expect(
      content.choices,
      equals(['1. 24 ÷ 2', '2. 48 ÷ 4', '3. 77 ÷ 7']),
    );
    expect(content.correctAnswer, equals('77 ÷ 7'));
    expect(isSameAnswer('3. 77 ÷ 7', content.correctAnswer), isTrue);
    expect(isSameAnswer(content.choices[2], content.correctAnswer), isTrue);
    expect(isSameAnswer('77÷7', content.correctAnswer), isTrue);
    expect(isSameAnswer('1. 24 ÷ 2', content.correctAnswer), isFalse);
  });

  test('renders juice bottle and milk carton labels for S3_elem_3_008755', () {
    const content = ProblemContent(
      summary: ProblemSummary(
        id: 'S3_elem_3_008755',
        grade: 3,
        subject: 'math',
        unit: '덧셈과 뺄셈',
        type: 'unit_choice',
        title: '주스병과 우유갑의 단위 선택',
        path: '',
        raw: {},
      ),
      renderer: {},
      semantic: {
        'answer': {
          'choice_groups': [
            {'label': '주스병', 'choices': ['L', 'mL']},
            {'label': '우유갑', 'choices': ['L', 'mL']},
          ],
          'value': 'L, mL',
        },
      },
      solvable: {},
    );

    expect(content.choiceGroups.length, equals(2));
    expect(content.choiceGroups[0].label, equals('주스병'));
    expect(content.choiceGroups[1].label, equals('우유갑'));
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

const _pointChoiceContent = ProblemContent(
  summary: ProblemSummary(
    id: 'S3_elem_3_008659',
    grade: 3,
    subject: 'math',
    unit: '원',
    type: 'diagram_choice',
    title: '원의 중심 찾기',
    path: '',
    raw: {},
  ),
  semantic: {},
  renderer: {},
  solvable: {
    'answer': {
      'choices': ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ'],
      'answer_key': ['ㄹ'],
      'target': {'type': 'selected_point'},
      'value': 'ㄹ',
    },
  },
);

const _compassCenterChoiceContent = ProblemContent(
  summary: ProblemSummary(
    id: 'S3_elem_3_008658',
    grade: 3,
    subject: 'math',
    unit: '원',
    type: 'geometry_compass_centers',
    title: '컴퍼스의 침을 꽂을 곳 찾기',
    path: '',
    raw: {},
  ),
  semantic: {},
  renderer: {},
  solvable: {
    'answer': {
      'choices': ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ'],
      'answer_key': ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ'],
      'target': {'type': 'multiple_choice_set'},
      'value': 'ㄱ, ㄴ, ㄷ, ㄹ',
    },
  },
);
