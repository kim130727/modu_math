import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/models/assignment.dart';
import 'package:modu_math_app/widgets/student_problem_canvas.dart';

void main() {
  for (final scale in [1.0, 2.0]) {
    testWidgets(
        'small carry and answer cells fit and advance in authored order at $scale',
        (tester) async {
      final item = AssignmentItem.fromJson({
        'id': 1,
        'content': {
          'presentation': {
            'mode': 'canvas_slots',
            'canvas_bindings': {
              'right-carry': 1,
              'left-carry': 0,
              'tens': 3,
              'hundreds': 2,
              'units': 4,
            }
          },
          'input_schema': {
            'fields': [
              for (var i = 0; i < 5; i++) {'id': '$i', 'type': 'number'}
            ]
          },
          'renderer_data': {
            'view_box': {'width': 180, 'height': 130},
            'elements': [
              for (final entry in [
                ('right-carry', 1),
                ('left-carry', 0),
                ('tens', 3),
                ('hundreds', 2),
                ('units', 4)
              ])
                {
                  'id': entry.$1,
                  'type': 'rect',
                  'attributes': {
                    'x': 20 + (entry.$2 < 2 ? entry.$2 : entry.$2 - 2) * 24,
                    'y': entry.$2 < 2
                        ? 10.0 + entry.$2 * .2
                        : 80.0 - entry.$2 * .2,
                    'width': 19.147,
                    'height': 19.699
                  },
                  'interaction': {
                    'type': 'input',
                    'role': 'answer',
                    'value_type': 'digit',
                    'max_length': 1,
                    'order': entry.$2,
                    'auto_advance': true,
                    'keyboard': 'number'
                  },
                  'input_style': {
                    'padding': 6,
                    'min_font_size': 14,
                    'max_font_size': 52,
                    'font_size_mode': 'auto',
                    'vertical_align': 'middle'
                  }
                },
            ]
          },
        }
      });
      dynamic answer = List.filled(5, '');
      var changes = 0;
      await tester.pumpWidget(MaterialApp(
          home: Scaffold(
              body: Center(
                  child: SizedBox(
        width: 180 * scale,
        child: StatefulBuilder(
            builder: (context, update) => StudentProblemCanvas(
                  item: item,
                  value: answer,
                  enabled: true,
                  changed: (value) => update(() {
                    answer = value;
                    changes++;
                  }),
                )),
      )))));
      for (var i = 0; i < 5; i++) {
        final finder = find.byKey(ValueKey('renderer-input-slot-$i'));
        final field = tester.widget<TextField>(finder);
        // The glyph's line box must fit inside the actual editable viewport.
        expect(field.style!.fontSize! * 1.25,
            lessThanOrEqualTo(tester.getSize(finder).height + .01));
        await tester.tap(finder);
        await tester.enterText(finder, ['1', '1', '9', '2', '1'][i]);
        await tester.pump();
        if (i < 4) {
          expect(
              tester
                  .widget<TextField>(
                      find.byKey(ValueKey('renderer-input-slot-${i + 1}')))
                  .focusNode!
                  .hasFocus,
              isTrue);
        }
      }
      expect(answer, ['1', '1', '9', '2', '1']);
      final first = find.byKey(const ValueKey('renderer-input-slot-0'));
      await tester.enterText(first, '99');
      await tester.pump();
      expect(tester.widget<TextField>(first).controller!.text.length, 1);
      await tester.enterText(first, '11921');
      await tester.pump();
      await tester.pump();
      expect(answer, ['1', '1', '9', '2', '1']);
      for (var i = 0; i < 5; i++) {
        expect(
            tester
                .widget<TextField>(
                    find.byKey(ValueKey('renderer-input-slot-$i')))
                .controller!
                .text,
            ['1', '1', '9', '2', '1'][i]);
      }
      final unchanged = changes;
      await tester.enterText(first, '11921');
      await tester.pump();
      await tester.pump();
      expect(changes, unchanged,
          reason: 'Duplicate input must not clear grading feedback');
      expect(tester.takeException(), isNull);
    });
  }
}
