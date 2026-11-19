import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:modu_math_app/screens/practice_learning_screen.dart';
import 'package:modu_math_app/services/student_assignment_service.dart';
import 'helpers/assignment_fixture.dart';

void main() {
  setUp(() => SharedPreferences.setMockInitialValues({}));
  testWidgets(
      'opening a later page can fetch and navigate to previous problems',
      (tester) async {
    final fixture = AssignmentFixture();
    await fixture.login();
    final service = StudentAssignmentService(
        authService: fixture.auth,
        httpClient: MockClient((request) async {
          if (request.url.path == '/api/v1/problems/') {
            expect(request.url.queryParameters['page'], '1');
            return assignmentJson({
              'results': [
                {'id': 1},
                {'id': 2}
              ],
              'previous': null
            });
          }
          final id = int.parse(request.url.path.split('/')[4]);
          return assignmentJson({
            'id': id,
            'prompt': '되돌아온 문제 $id',
            'renderer_data': {},
            'input_schema': {
              'fields': [
                {'id': 'answer', 'type': 'number'}
              ]
            }
          });
        }));
    await tester.pumpWidget(MaterialApp(
        home: PracticeLearningScreen(
            service: service,
            initialProblems: [
              {'id': 3}
            ],
            initialIndex: 0,
            initialGoal: {'target': 3, 'completed_ids': []},
            nextPage: null,
            previousPage: 1,
            total: 3,
            startPosition: 2,
            classroom: null,
            grade: '3',
            category: null,
            language: 'ko')));
    await tester.pumpAndSettle();
    for (final id in [2, 1]) {
      await tester.ensureVisible(find.text('이전 문제'));
      await tester.tap(find.text('이전 문제'));
      await tester.pumpAndSettle();
      expect(find.text('되돌아온 문제 $id'), findsOneWidget);
      expect(find.text('$id / 3번 문제'), findsOneWidget);
    }
    expect(
        tester
            .widget<OutlinedButton>(
                find.widgetWithText(OutlinedButton, '이전 문제'))
            .onPressed,
        isNull);
    expect(tester.takeException(), isNull);
  });
  testWidgets(
      'navigation preserves drafts and feedback, paginates, and celebrates the server goal',
      (tester) async {
    final fixture = AssignmentFixture();
    await fixture.login();
    final completed = <int>{};
    final requests = <http.Request>[];
    Map<String, dynamic> goal() =>
        {'target': 3, 'completed_ids': completed.toList()};
    final service = StudentAssignmentService(
        authService: fixture.auth,
        httpClient: MockClient((request) async {
          requests.add(request);
          final path = request.url.path;
          if (path == '/api/v1/problems/catalog/')
            return assignmentJson({'goal': goal()});
          if (path == '/api/v1/problems/') {
            expect(request.url.queryParameters['page'], '2');
            expect(request.url.queryParameters['grade'], '3');
            expect(request.url.queryParameters['category'], '덧셈');
            return assignmentJson({
              'results': [
                {'id': 3}
              ],
              'next': null
            });
          }
          if (path == '/api/v1/attempts/') {
            final body = jsonDecode(request.body) as Map;
            final correct = body['submitted_answer'] == '7';
            if (correct) completed.add(body['problem'] as int);
            return assignmentJson({'is_correct': correct}, 201);
          }
          final id = int.parse(path.split('/')[4]);
          return assignmentJson({
            'id': id,
            'prompt': '문제 $id: 3 + 4 = ?',
            'renderer_data': {},
            'input_schema': {
              'fields': [
                {'id': 'answer', 'type': 'number'}
              ]
            }
          });
        }));
    await tester.pumpWidget(MaterialApp(
        home: PracticeLearningScreen(
            service: service,
            initialProblems: [
              {'id': 1},
              {'id': 2}
            ],
            initialIndex: 0,
            initialGoal: goal(),
            nextPage: 2,
            total: 3,
            startPosition: 0,
            classroom: null,
            grade: '3',
            category: '덧셈',
            language: 'ko')));
    await tester.pumpAndSettle();
    Future<void> tap(String text) async {
      final target = find.text(text).last;
      await tester.ensureVisible(target);
      await tester.tap(target);
      await tester.pumpAndSettle();
    }

    Future<void> enter(String text) async {
      final input = find.byKey(const ValueKey('assignment-answer-0'));
      await tester.ensureVisible(input);
      await tester.enterText(input, text);
      await tester.pump();
    }

    await enter('5');
    await tap('다음 문제');
    expect(find.text('문제 2: 3 + 4 = ?'), findsOneWidget);
    expect(find.text('0 / 3'), findsOneWidget);
    await enter('0');
    await tap('답 제출');
    expect(find.text('다시 생각해 볼까요?'), findsOneWidget);
    expect(completed, isEmpty);
    await tap('다음 문제');
    expect(find.text('문제 3: 3 + 4 = ?'), findsOneWidget);
    await enter('7');
    await tap('답 제출');
    expect(find.text('1 / 3'), findsOneWidget);
    await tap('이전 문제');
    expect(find.text('다시 생각해 볼까요?'), findsOneWidget);
    expect(
        tester
            .widget<TextField>(
                find.byKey(const ValueKey('assignment-answer-0')))
            .controller!
            .text,
        '0');
    await enter('7');
    await tap('답 제출');
    await tap('이전 문제');
    expect(
        tester
            .widget<TextField>(
                find.byKey(const ValueKey('assignment-answer-0')))
            .controller!
            .text,
        '5');
    await enter('7');
    await tap('답 제출');
    expect(find.text('오늘의 목표 달성!'), findsOneWidget);
    await tap('다음 문제');
    expect(find.text('맞았어요!'), findsOneWidget);
    expect(completed, {1, 2, 3});
    expect(requests.where((r) => r.url.path == '/api/v1/problems/1/'),
        hasLength(1));
    expect(tester.takeException(), isNull);
  });
}
