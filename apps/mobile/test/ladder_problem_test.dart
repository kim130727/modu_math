import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/models/content_models.dart';
import 'package:modu_math_app/utils/answer_normalizer.dart';
import 'package:modu_math_app/widgets/answer_panel.dart';

void main() {
  const problemId = 'S3_elem_3_008732';
  final locales = ['ko', 'en', 'ja', 'km', 'uk', 'zh'];

  Map<String, dynamic> read(String path) => File(path).existsSync()
      ? jsonDecode(File(path).readAsStringSync()) as Map<String, dynamic>
      : <String, dynamic>{};

  ProblemContent load(String locale) {
    final prefix = '../../examples/problems/$locale/$problemId';
    return ProblemContent(
      summary: ProblemSummary.fromJson({
        'id': problemId,
        'title': '사다리 타기',
        'type': 'choice',
      }),
      semantic: read('$prefix.semantic.json'),
      solvable: read('$prefix.solvable.v1.1.json'),
      renderer: read('$prefix.renderer.json'),
      layout: read('$prefix.layout.json'),
    );
  }

  group('S3_elem_3_008732 prompt sanitization and choiceGroups', () {
    test('prompt does not leak fraction digits across all locales', () {
      for (final locale in locales) {
        final content = load(locale);
        final prompt = content.prompt;

        // Prompt should be a single clean instruction without numbers on separate lines
        expect(prompt, isNotEmpty, reason: locale);
        expect(prompt.contains('\n2\n8'), isFalse,
            reason: 'Leaked numbers in $locale');
        expect(prompt.contains('\n4\n4'), isFalse,
            reason: 'Leaked numbers in $locale');

        for (final line in prompt.split('\n')) {
          expect(RegExp(r'^\d+$').hasMatch(line.trim()), isFalse,
              reason: 'Digit line "$line" found in prompt for $locale');
        }
      }
    });

    test('has 3 choice groups with fraction labels and OX choices across all locales', () {
      for (final locale in locales) {
        final content = load(locale);
        final groups = content.choiceGroups;

        expect(groups.length, equals(3), reason: 'Must have 3 groups in $locale');
        expect(groups[0].label, equals('2/8'));
        expect(groups[1].label, equals('9/10'));
        expect(groups[2].label, equals('4/4'));

        for (final g in groups) {
          expect(g.choices, containsAll(['○', '×']),
              reason: 'Group choices in $locale');
        }

        // Correct answer should match
        expect(isSameAnswer(content.correctAnswer, '○, ×, ○'), isTrue,
            reason: 'Correct answer matching in $locale');
      }
    });

    testWidgets('AnswerPanel renders 3 choice groups and combines answers correctly',
        (tester) async {
      final content = load('ko');
      String currentDraft = '';
      String? submittedAnswer;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: StatefulBuilder(
              builder: (context, setState) {
                return AnswerPanel(
                  content: content,
                  answerDraft: currentDraft,
                  isCorrect: null,
                  onAnswerChanged: (ans) {
                    setState(() {
                      currentDraft = ans;
                    });
                  },
                  onSubmit: (ans) {
                    submittedAnswer = ans;
                  },
                );
              },
            ),
          ),
        ),
      );
      await tester.pumpAndSettle();

      // Group labels are rendered
      expect(find.text('2/8'), findsOneWidget);
      expect(find.text('9/10'), findsOneWidget);
      expect(find.text('4/4'), findsOneWidget);

      // Tag shows O / X
      expect(find.text('O / X'), findsOneWidget);

      // Chips with labels are rendered (○ 참, ✕ 거짓)
      final trueChips = find.text('○  참');
      final falseChips = find.text('✕  거짓');
      expect(trueChips, findsNWidgets(3));
      expect(falseChips, findsNWidgets(3));

      // Click group 1: ○
      await tester.tap(trueChips.at(0));
      await tester.pumpAndSettle();

      // Click group 2: ✕
      await tester.tap(falseChips.at(1));
      await tester.pumpAndSettle();

      // Click group 3: ○
      await tester.tap(trueChips.at(2));
      await tester.pumpAndSettle();

      // Answer should be combined
      expect(currentDraft, equals('○, ×, ○'));

      // Submit
      final submitButton = find.text('정답 확인');
      await tester.tap(submitButton);
      await tester.pumpAndSettle();

      expect(submittedAnswer, equals('○, ×, ○'));
      expect(isSameAnswer(submittedAnswer!, content.correctAnswer), isTrue);
    });
  });
}
