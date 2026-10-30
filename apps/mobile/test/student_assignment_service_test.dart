import 'dart:async';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';
import 'package:modu_math_app/services/student_assignment_service.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'helpers/assignment_fixture.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  setUp(() => SharedPreferences.setMockInitialValues({}));

  test('answer-free detail and server-authoritative submission', () async {
    final fixture = AssignmentFixture();
    await fixture.login();
    final detail = await fixture.service.detail(1);
    expect(detail.items.first.answer, isNull);
    expect(detail.items.first.fields.single.type, 'number');
    final result = await fixture.service.submitAnswer(1, 1, '42', 1500);
    expect(result.containsKey('is_correct'), isFalse);
    expect(fixture.posts.single.containsKey('is_correct'), isFalse);
    expect(fixture.posts.single['elapsed_ms'], 1500);
    expect(await fixture.service.pending(1, 1), isNull);
  });

  test('lost response survives service restart and reuses the same key',
      () async {
    final fixture = AssignmentFixture();
    await fixture.login();
    fixture.loseResponse = true;
    await expectLater(fixture.service.submitAnswer(1, 1, '42', 100),
        throwsA(isA<AssignmentApiException>()));
    final restarted = StudentAssignmentService(
        authService: fixture.auth, httpClient: fixture.client);
    final pending = await restarted.pending(1, 1);
    expect(pending?['answer'], '42');
    await expectLater(
        restarted.submitAnswer(1, 1, '99', 100),
        throwsA(isA<AssignmentApiException>()
            .having((e) => e.status, 'status', 409)));
    await restarted.submitAnswer(1, 1, '42', 999);
    expect(fixture.keys.length, 1);
    expect(fixture.posts[0], fixture.posts[1]);
  });

  test('local drafts and pending attempts are isolated by account', () async {
    final fixture = AssignmentFixture();
    await fixture.login();
    await fixture.service.persistDraft(1, 1, 'private draft');
    fixture.loseResponse = true;
    await expectLater(fixture.service.submitAnswer(1, 1, '42', 100),
        throwsA(isA<AssignmentApiException>()));
    await fixture.auth.logout();
    await fixture.login(2);
    expect(await fixture.service.local(1, 1, 'draft'), isNull);
    expect(await fixture.service.pending(1, 1), isNull);
    await fixture.auth.logout();
    await fixture.login();
    expect((await fixture.service.local(1, 1, 'draft'))?['answer'],
        'private draft');
    expect(await fixture.service.pending(1, 1), isNotNull);
  });

  test('a stale 401 cannot sign out a newly logged-in account', () async {
    final fixture = AssignmentFixture();
    await fixture.login();
    final response = Completer<http.Response>();
    final service = StudentAssignmentService(
        authService: fixture.auth,
        httpClient: MockClient((_) => response.future));
    final old = service.detail(1);
    final failure = expectLater(old, throwsA(isA<AssignmentApiException>()));
    await fixture.login(2);
    response.complete(assignmentJson({'detail': 'expired'}, 401));
    await failure;
    expect(fixture.auth.currentUser?.id, 2);
    expect(fixture.auth.isAuthenticated, isTrue);
  });

  test('offline draft saving never creates a graded attempt', () async {
    final fixture = AssignmentFixture();
    await fixture.login();
    fixture.offlineDraft = true;
    await fixture.service.persistDraft(1, 1, '42');
    expect(await fixture.service.saveDraft(1, 1, '42'), isFalse);
    expect((await fixture.service.local(1, 1, 'draft'))?['answer'], '42');
    expect(fixture.posts, isEmpty);
  });

  test('timeout covers connecting to the server as well as the body', () async {
    final fixture = AssignmentFixture();
    await fixture.login();
    final service = StudentAssignmentService(
        authService: fixture.auth,
        timeout: const Duration(milliseconds: 10),
        httpClient: MockClient((_) => Completer<http.Response>().future));
    await expectLater(
        service.detail(1),
        throwsA(isA<AssignmentApiException>()
            .having((e) => e.offline, 'offline', isTrue)));
  });
}
