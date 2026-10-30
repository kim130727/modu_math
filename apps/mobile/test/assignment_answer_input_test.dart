import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/l10n/assignment_strings.dart';
import 'package:modu_math_app/models/assignment.dart';
import 'package:modu_math_app/screens/assignment_solve_screen.dart';
import 'package:modu_math_app/services/assignment_session.dart';
import 'package:modu_math_app/widgets/assignment_answer_input.dart';

void main() {
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
