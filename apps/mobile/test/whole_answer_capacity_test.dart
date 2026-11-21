import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/models/assignment.dart';
import 'package:modu_math_app/widgets/student_problem_canvas.dart';

void main() {
  for (final type in ['integer']) {
    testWidgets('old $type snapshots accept complete answers and fit text',
        (tester) async {
      final item = AssignmentItem.fromJson({
        'id': 1,
        'content': {
          'presentation': {
            'mode': 'canvas_slots',
            'canvas_bindings': {'whole': 0}
          },
          'input_schema': {
            'fields': [
              {'id': 'answer', 'type': 'number'}
            ]
          },
          'renderer_data': {
            'view_box': {'width': 400, 'height': 150},
            'elements': [
              {
                'id': 'whole',
                'type': 'rect',
                'attributes': {'x': 20, 'y': 20, 'width': 160, 'height': 90},
                'interaction': {
                  'type': 'input',
                  'role': 'answer',
                  'value_type': type,
                  'keyboard': 'number',
                  'max_length': type == 'digit' ? 1 : 3
                },
              }
            ]
          },
        }
      });
      dynamic answer;
      await tester.pumpWidget(MaterialApp(
          home: Scaffold(
              body: Center(
                  child: SizedBox(
        width: 400,
        child: StatefulBuilder(
            builder: (context, update) => StudentProblemCanvas(
                item: item,
                value: answer,
                enabled: true,
                changed: (value) => update(() => answer = value))),
      )))));
      final input = find.byKey(const ValueKey('renderer-input-slot-0'));
      final originalSize = tester.widget<TextField>(input).style!.fontSize!;
      for (final value in ['1124', '123456789', '-1234.50', '7/8', '1,124']) {
        await tester.enterText(input, value);
        await tester.pump();
        expect(answer, value);
        expect(tester.widget<TextField>(input).controller!.text, value);
        if (value == '123456789') {
          expect(tester.widget<TextField>(input).style!.fontSize!,
              lessThan(originalSize));
        }
      }
      expect(tester.takeException(), isNull);
    });
  }
}
