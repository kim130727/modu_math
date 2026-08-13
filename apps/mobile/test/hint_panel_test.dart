import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
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
}
