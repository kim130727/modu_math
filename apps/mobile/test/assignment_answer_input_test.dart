import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/l10n/assignment_strings.dart';
import 'package:modu_math_app/models/assignment.dart';
import 'package:modu_math_app/screens/assignment_solve_screen.dart';
import 'package:modu_math_app/services/assignment_session.dart';
import 'package:modu_math_app/widgets/assignment_answer_input.dart';

void main() {
  testWidgets('choice labels fit tall glyphs and wrap long text on mobile',
      (tester) async {
    const longLabel = '여러 문장으로 구성된 긴 보기도 화면에 모두 보여야 합니다.';
    final item = AssignmentItem.fromJson({
      'id': 1,
      'content': {
        'input_schema': {
          'fields': [
            {
              'id': 'field-1',
              'type': 'choice',
              'choices': [
                {'label': '○', 'value': 1},
                {'label': '×', 'value': 2},
                {'label': longLabel, 'value': 3},
              ],
            },
          ],
        },
      },
    });
    await tester.pumpWidget(MaterialApp(
      home: Scaffold(
        body: Align(
          alignment: Alignment.topLeft,
          child: SizedBox(
            width: 280,
            child: MediaQuery(
              data: const MediaQueryData(textScaler: TextScaler.linear(1.6)),
              child: AssignmentAnswerInput(
                item: item,
                value: 1,
                enabled: true,
                changed: (_) {},
              ),
            ),
          ),
        ),
      ),
    ));
    for (final label in ['○', '×', longLabel]) {
      final text = find.text(label);
      final paragraph = tester.renderObject<RenderParagraph>(text);
      final chip = find.widgetWithText(OutlinedButton, label);
      expect(paragraph.overflow, TextOverflow.visible);
      expect(paragraph.didExceedMaxLines, isFalse);
      expect(tester.getSize(chip).height,
          greaterThan(tester.getSize(text).height));
      expect(tester.getSize(chip).width, lessThanOrEqualTo(280));
      final chipBounds = tester.getRect(chip).inflate(0.01);
      final labelOrigin = paragraph.localToGlobal(Offset.zero);
      for (final word in RegExp(r'\S+').allMatches(label)) {
        for (final line in paragraph.getBoxesForSelection(
          TextSelection(baseOffset: word.start, extentOffset: word.end),
        )) {
          final bounds = line.toRect().shift(labelOrigin);
          expect(chipBounds.contains(bounds.topLeft), isTrue,
              reason: '$label: $bounds inside $chipBounds');
          expect(chipBounds.contains(bounds.bottomRight), isTrue,
              reason: '$label: $bounds inside $chipBounds');
        }
      }
    }
    expect(tester.getSize(find.text(longLabel)).height,
        greaterThan(tester.getSize(find.text('○')).height));
    expect(tester.takeException(), isNull);
  });

  for (final limit in [1, 3]) {
    testWidgets('integer panel input keeps up to $limit digits',
        (tester) async {
      dynamic value;
      final item = AssignmentItem.fromJson({
        'id': 1,
        'content': {
          'input_schema': {
            'fields': [
              {'id': 'field-1', 'type': 'number', 'max_length': limit},
            ],
          },
        },
      });
      await tester.pumpWidget(MaterialApp(
        home: Scaffold(
          body: AssignmentAnswerInput(
            item: item,
            value: null,
            enabled: true,
            changed: (next) => value = next,
          ),
        ),
      ));
      await tester.enterText(find.byType(TextField), 'a3067');
      expect(value, '306'.substring(0, limit));
    });
  }

  testWidgets(
      'multiple selections preserve all choices and display labels in results',
      (tester) async {
    dynamic value;
    final item = AssignmentItem.fromJson({
      'id': 1,
      'submitted_answer': [2, 1],
      'content': {
        'input_schema': {
          'fields': [
            {
              'id': 'field-1',
              'type': 'multi_choice',
              'choices': [
                {'label': 'ㄱ', 'value': 1},
                {'label': 'ㄴ', 'value': 2},
                {'label': 'ㄷ', 'value': 3}
              ]
            }
          ]
        }
      }
    });
    await tester.pumpWidget(MaterialApp(
        home: Scaffold(
            body: StatefulBuilder(
                builder: (context, setState) => AssignmentAnswerInput(
                    item: item,
                    value: value,
                    enabled: true,
                    changed: (next) => setState(() {
                          value = next;
                        }))))));
    await tester.tap(find.text('ㄴ'));
    await tester.pumpAndSettle();
    await tester.tap(find.text('ㄱ'));
    await tester.pumpAndSettle();
    expect(value, [2, 1]);
    expect(
        displaySubmittedAnswer(item, const AssignmentStrings(false)), 'ㄴ, ㄱ');
    expect(AssignmentSession.complete([], 1), isFalse);
    expect(AssignmentSession.complete(value, 1), isTrue);
  });
}
