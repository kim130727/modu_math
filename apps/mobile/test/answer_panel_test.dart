import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/models/content_models.dart';
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
