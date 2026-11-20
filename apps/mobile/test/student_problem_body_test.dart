import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/models/assignment.dart';
import 'package:modu_math_app/widgets/student_problem_body.dart';

void main() {
  testWidgets(
      'problem instructions remain separate from answer input semantics',
      (tester) async {
    final semantics = tester.ensureSemantics();
    final item = AssignmentItem.fromJson({
      'id': 1,
      'content': {
        'prompt': '문제를 읽고 답하세요.',
        'owner_name': '선생님',
        'input_schema': {
          'fields': [
            {'id': 'answer', 'type': 'text'}
          ]
        },
      }
    });
    await tester.pumpWidget(MaterialApp(
        home: Scaffold(
            body: StudentProblemBody(
      item: item,
      value: null,
      enabled: true,
      changed: (_) {},
    ))));
    expect(
        tester.getSemantics(find.text('문제를 읽고 답하세요.')).label, '문제를 읽고 답하세요.');
    expect(tester.getSemantics(find.byType(TextField)).label,
        isNot(contains('문제를 읽고')));
    semantics.dispose();
  });
}
