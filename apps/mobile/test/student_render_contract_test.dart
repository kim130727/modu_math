import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/testing.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:modu_math_app/models/assignment.dart';
import 'package:modu_math_app/screens/practice_learning_screen.dart';
import 'package:modu_math_app/services/student_assignment_service.dart';
import 'package:modu_math_app/widgets/student_problem_canvas.dart';
import 'helpers/assignment_fixture.dart';

void main() {
  setUp(() => SharedPreferences.setMockInitialValues({}));
  testWidgets(
      'canvas fields preserve binding order, spaces, commas, and authored style',
      (tester) async {
    final item = AssignmentItem.fromJson({
      'id': 1,
      'content': {
        'presentation': {
          'mode': 'canvas_slots',
          'canvas_bindings': {'left': 1, 'right': 0}
        },
        'input_schema': {
          'fields': [
            {'id': 'a', 'type': 'text'},
            {'id': 'b', 'type': 'text'}
          ]
        },
        'renderer_data': {
          'view_box': {'width': 400, 'height': 150},
          'elements': [
            for (var i = 0; i < 2; i++)
              {
                'id': i == 0 ? 'left' : 'right',
                'type': 'rect',
                'attributes': {
                  'x': 10 + i * 180,
                  'y': 20,
                  'width': 150,
                  'height': 70,
                  'stroke': '#000000'
                },
                'interaction': {
                  'type': 'input',
                  'role': 'answer',
                  'order': i,
                  'max_length': 64
                },
                'input_style': {
                  'font_size_mode': 'fixed',
                  'font_size': 24,
                  'text_color': '#123456',
                  'horizontal_align': 'left'
                }
              },
          ]
        },
      }
    });
    dynamic answer = ['', ''];
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
                            changed: (next) =>
                                update(() => answer = next))))))));
    await tester.pump();
    await tester.enterText(
        find.byKey(const ValueKey('renderer-input-slot-0')), '12');
    await tester.pump();
    await tester.enterText(
        find.byKey(const ValueKey('renderer-input-slot-1')), '3, 4');
    await tester.pump();
    expect(answer, ['3, 4', '12']);
    final field = tester
        .widget<TextField>(find.byKey(const ValueKey('renderer-input-slot-1')));
    expect(field.style!.fontSize, 24);
    expect(field.style!.color, const Color(0xff123456));
    expect(field.textAlign, TextAlign.left);
    expect(tester.takeException(), isNull);
  });

  for (final draft in [false, true]) {
    testWidgets(
        'live update ${draft ? 'preserves a draft until accepted' : 'refreshes an unanswered problem'}',
        (tester) async {
      final fixture = AssignmentFixture();
      await fixture.login();
      var current = 'v1';
      final service = StudentAssignmentService(
          authService: fixture.auth,
          httpClient: MockClient((request) async {
            if (request.url.path.endsWith('/version/'))
              return assignmentJson({'revision': current});
            return assignmentJson({
              'id': 1,
              'revision': current,
              'prompt': '문제 $current',
              'renderer_data': {},
              'input_schema': {
                'fields': [
                  {'id': 'a', 'type': 'text'}
                ]
              }
            });
          }));
      await tester.pumpWidget(MaterialApp(
          home: PracticeLearningScreen(
              service: service,
              initialProblems: [
                {'id': 1}
              ],
              initialIndex: 0,
              initialGoal: {'target': 1, 'completed_ids': []},
              nextPage: null,
              total: 1,
              startPosition: 0,
              classroom: null,
              grade: '3',
              category: null,
              language: 'ko')));
      await tester.pumpAndSettle();
      final input = find.byKey(const ValueKey('assignment-answer-0'));
      if (draft) {
        await tester.ensureVisible(input);
        await tester.enterText(input, '내 답');
      }
      current = 'v2';
      await tester.pump(const Duration(seconds: 6));
      await tester.pumpAndSettle();
      if (draft) {
        expect(find.text('문제 v1'), findsOneWidget);
        expect(tester.widget<TextField>(input).controller!.text, '내 답');
        final apply = find.text('새 내용 적용');
        await tester.ensureVisible(apply);
        await tester.tap(apply);
        await tester.pumpAndSettle();
      }
      expect(find.text('문제 v2'), findsOneWidget);
      expect(tester.widget<TextField>(input).controller!.text, '');
      expect(tester.takeException(), isNull);
    });
  }
}
