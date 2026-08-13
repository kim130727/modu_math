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
}
