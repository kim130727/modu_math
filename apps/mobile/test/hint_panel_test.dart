import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/models/content_models.dart';
import 'package:modu_math_app/services/solvable_hint_service.dart';
import 'package:modu_math_app/widgets/hint_panel.dart';

void main() {
  testWidgets('checks a multiple-choice mini problem inside a revealed hint',
      (tester) async {
    var revealCount = 0;
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: HintPanel(
            visibleLevel: 1,
            onRevealNext: () => revealCount += 1,
            hints: const [
              SolvableHint(
                level: 1,
                title: '1단계: 일의 자리 더하기',
                body: '맨 오른쪽에 있는 일의 자리부터 더해요.',
                miniQuestion: '9 + 8은 얼마인가요?',
                choices: [
                  HintChoice(label: '17', isCorrect: true),
                  HintChoice(label: '16'),
                  HintChoice(label: '7'),
                ],
                successMessage: '맞아요. 일의 자리 합은 17이에요.',
              ),
            ],
          ),
        ),
      ),
    );

    expect(find.text('9 + 8은 얼마인가요?'), findsOneWidget);
    expect(find.text('17'), findsOneWidget);
    expect(find.byType(TextField), findsNothing);

    await tester.tap(find.text('16'));
    await tester.pumpAndSettle();
    expect(find.textContaining('조금 달라요'), findsOneWidget);

    await tester.tap(find.text('17'));
    await tester.pumpAndSettle();
    expect(find.text('맞아요. 일의 자리 합은 17이에요.'), findsOneWidget);
    expect(revealCount, equals(0));
  });

  testWidgets('shows subproblem hints in independent tabs', (tester) async {
    var revealCount = 0;
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: HintPanel(
            visibleLevel: 0,
            onRevealNext: () => revealCount += 1,
            hints: const [
              SolvableHint(
                level: 1,
                title: '1: (1) ones place',
                body: 'First subproblem.',
                miniQuestion: 'Problem 1 ones sum?',
                choices: [
                  HintChoice(label: '13', isCorrect: true),
                  HintChoice(label: '3'),
                ],
                successMessage: 'Problem 1 correct.',
              ),
              SolvableHint(
                level: 1,
                title: '1: (2) ones place',
                body: 'Second subproblem.',
                miniQuestion: 'Problem 2 ones sum?',
                choices: [
                  HintChoice(label: '14', isCorrect: true),
                  HintChoice(label: '4'),
                ],
                successMessage: 'Problem 2 correct.',
              ),
            ],
          ),
        ),
      ),
    );

    expect(find.text('(1)'), findsOneWidget);
    expect(find.text('(2)'), findsOneWidget);
    expect(find.text('Problem 1 ones sum?'), findsNothing);
    expect(find.text('Problem 2 ones sum?'), findsNothing);

    await tester.tap(find.byType(FilledButton));
    await tester.pumpAndSettle();
    expect(find.text('Problem 1 ones sum?'), findsOneWidget);
    expect(find.text('Problem 2 ones sum?'), findsNothing);

    await tester.tap(find.text('3'));
    await tester.pumpAndSettle();
    expect(find.text('Problem 2 correct.'), findsNothing);

    await tester.tap(find.text('(2)'));
    await tester.pumpAndSettle();
    expect(find.text('Problem 1 ones sum?'), findsNothing);
    expect(find.text('Problem 2 ones sum?'), findsNothing);

    await tester.tap(find.byType(FilledButton));
    await tester.pumpAndSettle();
    expect(find.text('Problem 2 ones sum?'), findsOneWidget);

    await tester.tap(find.text('14'));
    await tester.pumpAndSettle();
    expect(find.text('Problem 2 correct.'), findsOneWidget);
    expect(revealCount, equals(2));
  });

  test('builds place value decomposition addition hints for P3_1_01_00040_15621', () {
    const service = SolvableHintService();
    const content = ProblemContent(
      summary: ProblemSummary(
        id: 'P3_1_01_00040_15621',
        grade: 3,
        subject: 'math',
        unit: 'addition',
        type: 'place_value_addition_fill_blank',
        title: '자리값을 이용한 265와 432의 덧셈',
        path: '',
        raw: {},
      ),
      solvable: {
        'problem_type': 'place_value_addition_fill_blank',
        'steps': [
          {
            'id': 'step.decompose_first',
            'expr': '265 = 200 + 60 + 5',
            'value': 60,
            'explanation': '265의 십의 자리 숫자는 6이므로 십의 자리 값은 60입니다.',
          },
          {
            'id': 'step.decompose_second',
            'expr': '432 = 400 + 30 + 2',
            'value': 2,
            'explanation': '432의 일의 자리 값은 2입니다.',
          },
          {
            'id': 'step.add_tens',
            'expr': '60 + 30',
            'value': 90,
            'explanation': '두 수의 십의 자리 값을 더하면 90입니다.',
          },
          {
            'id': 'step.add_ones',
            'expr': '5 + 2',
            'value': 7,
            'explanation': '두 수의 일의 자리 값을 더하면 7입니다.',
          },
          {
            'id': 'step.add_partial_sums',
            'expr': '600 + 90 + 7',
            'value': 697,
            'explanation': '백, 십, 일의 자리 부분합을 모두 더하면 697입니다.',
          },
        ],
      },
      semantic: {},
    );

    final hints = service.buildHints(content);
    expect(hints, hasLength(5));
    expect(hints[0].title, contains('첫 번째 수의 자리값'));
    expect(hints[0].acceptedAnswers, contains('60'));
    expect(hints[1].title, contains('두 번째 수의 자리값'));
    expect(hints[1].acceptedAnswers, contains('2'));
    expect(hints[2].title, contains('십의 자리 부분합'));
    expect(hints[2].acceptedAnswers, contains('90'));
    expect(hints[3].title, contains('일의 자리 부분합'));
    expect(hints[3].acceptedAnswers, contains('7'));
    expect(hints[4].title, contains('전체 합 완성하기'));
    expect(hints[4].acceptedAnswers, contains('697'));
  });
}
