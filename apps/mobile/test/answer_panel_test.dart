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
