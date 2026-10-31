import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:modu_math_app/screens/problem_library_screen.dart';
import 'package:modu_math_app/services/student_assignment_service.dart';
import 'helpers/assignment_fixture.dart';

void main() {
  setUp(() => SharedPreferences.setMockInitialValues({}));

  testWidgets(
      'public practice and approved class shelves use authenticated server grading',
      (tester) async {
    final fixture = AssignmentFixture();
    await fixture.login();
    final requests = <http.Request>[];
    final service = StudentAssignmentService(
        authService: fixture.auth,
        httpClient: MockClient((request) async {
          requests.add(request);
          expect(request.headers['Authorization'], isNotNull);
          final path = request.url.path;
          Object data;
          if (path == '/api/v1/student/classes/') {
            data = [
              {
                'id': 1,
                'name': '탐험대',
                'teacher_name': '김선생님',
                'status': 'approved'
              },
              {
                'id': 2,
                'name': '새 클래스',
                'teacher_name': '이선생님',
                'status': 'pending'
              },
            ];
          } else if (path == '/api/v1/problems/') {
            expect(request.url.queryParameters['grade'], isNull);
            data = {
              'results': [
                {'id': 7, 'title': '덧셈 문제', 'owner_name': '김선생님', 'unit': '덧셈'}
              ],
              'next': null,
              'previous': null
            };
          } else if (path == '/api/v1/problems/7/') {
            data = {
              'id': 7,
              'problem_id': 'public-seven',
              'prompt': '3 + 4 = ?',
              'owner_name': '김선생님',
              'source_credit': '직접 제작',
              'renderer_data': <String, dynamic>{},
              'input_schema': {
                'fields': [
                  {'id': 'a', 'type': 'number'}
                ]
              }
            };
          } else if (path == '/api/v1/attempts/') {
            final body = jsonDecode(request.body) as Map;
            expect(body['submitted_answer'], '7');
            expect(body.containsKey('is_correct'), isFalse);
            data = {'is_correct': true};
          } else {
            throw StateError(path);
          }
          return http.Response(
              jsonEncode(data), path == '/api/v1/attempts/' ? 201 : 200,
              headers: {'content-type': 'application/json; charset=utf-8'});
        }));
    await tester
        .pumpWidget(MaterialApp(home: ProblemLibraryScreen(service: service)));
    await tester.pumpAndSettle();
    expect(find.textContaining('선생님 승인 대기'), findsOneWidget);
    expect(find.widgetWithText(ChoiceChip, '새 클래스'), findsNothing);
    expect(
        requests
            .firstWhere((r) => r.url.path == '/api/v1/problems/')
            .url
            .queryParameters['scope'],
        'public');
    await tester.tap(find.text('탐험대 · 김선생님'));
    await tester.pumpAndSettle();
    expect(requests.last.url.queryParameters['classroom'], '1');
    await tester.tap(find.text('덧셈 문제'));
    await tester.pumpAndSettle();
    expect(find.text('출처: 직접 제작'), findsOneWidget);
    await tester.enterText(
        find.byKey(const ValueKey('assignment-answer-0')), '7');
    await tester.pump();
    await tester.ensureVisible(find.text('답 제출'));
    await tester.tap(find.text('답 제출'));
    await tester.pumpAndSettle();
    expect(requests.last.url.path, '/api/v1/attempts/');
    expect(find.text('맞았어요!'), findsOneWidget);
    expect(tester.takeException(), isNull);
  });
}
