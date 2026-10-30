import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/l10n/app_strings.dart';
import 'package:modu_math_app/screens/student_assignments_screen.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'helpers/assignment_fixture.dart';

void main() {
  setUp(() => SharedPreferences.setMockInitialValues({}));
  Future<AssignmentFixture> open(WidgetTester tester,
      {bool ukrainian = false}) async {
    final fixture = AssignmentFixture();
    await fixture.login();
    await tester.pumpWidget(AppLocaleScope(
        locale: Locale(ukrainian ? 'uk' : 'ko'),
        onLocaleChanged: (_) {},
        child: MaterialApp(
            home: StudentAssignmentsScreen(
                authService: fixture.auth, service: fixture.service))));
    await tester.pumpAndSettle();
    return fixture;
  }

  Future<void> tap(WidgetTester tester, String label) async {
    final target = find.text(label).last;
    await tester.ensureVisible(target);
    await tester.tap(target);
    await tester.pumpAndSettle();
  }

  Future<void> enter(WidgetTester tester, String value) async {
    final input = find.byKey(const ValueKey('assignment-answer-0'));
    await tester.ensureVisible(input);
    await tester.enterText(input, value);
    await tester.pump();
  }

  testWidgets(
      'two problems use server grading and reveal answers only after final submission',
      (tester) async {
    final fixture = await open(tester);
    await tap(tester, '과제 열기');
    expect(find.text('정답: 42'), findsNothing);
    await enter(tester, '42');
    await tap(tester, '답 제출');
    expect(find.text('답을 제출했어요.'), findsOneWidget);
    expect(find.text('맞았어요!'), findsNothing);
    await tap(tester, '다음 문제');
    await enter(tester, '8');
    await tap(tester, '답 제출');
    await tap(tester, '과제 제출하기');
    expect(find.text('수고했어요! 과제를 제출했어요.'), findsOneWidget);
    expect(find.text('1 / 2개 정답'), findsOneWidget);
    expect(fixture.keys.length, 2);
    await tap(tester, '오답만 보기');
    expect(find.text('1번 문제'), findsNothing);
    expect(find.text('2번 문제'), findsOneWidget);
    expect(tester.takeException(), isNull);
  });

  testWidgets('offline draft resumes after leaving without claiming submission',
      (tester) async {
    final fixture = await open(tester);
    fixture.offlineDraft = true;
    await tap(tester, '과제 열기');
    await enter(tester, '37');
    await tester.pump(const Duration(milliseconds: 750));
    await tester.pumpAndSettle();
    expect(find.text('기기에 저장했어요. 인터넷 연결 후 다시 저장해 주세요.'), findsOneWidget);
    Navigator.of(
            tester.element(find.byKey(const ValueKey('assignment-answer-0'))))
        .pop();
    await tester.pumpAndSettle();
    await tap(tester, '과제 열기');
    final input = tester
        .widget<TextField>(find.byKey(const ValueKey('assignment-answer-0')));
    expect(input.controller!.text, '37');
    expect(fixture.posts, isEmpty);
    await tester.pumpWidget(const SizedBox.shrink());
    await tester.pumpAndSettle();
  });

  testWidgets('390px Ukrainian assignment list and class join remain usable',
      (tester) async {
    await tester.binding.setSurfaceSize(const Size(390, 844));
    addTearDown(() => tester.binding.setSurfaceSize(null));
    await open(tester, ukrainian: true);
    expect(find.text('Мої завдання'), findsOneWidget);
    await tap(tester, 'Приєднатися до класу');
    await tester.enterText(find.byType(TextFormField), 'class-code');
    await tap(tester, 'Надіслати запит');
    expect(find.text('Запит надіслано. Зачекайте на підтвердження вчителя.'),
        findsOneWidget);
    expect(tester.takeException(), isNull);
  });
}
