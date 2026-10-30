import 'dart:async';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';
import 'package:modu_math_app/services/auth_service.dart';
import 'package:modu_math_app/services/student_assignment_service.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'helpers/assignment_fixture.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  setUp(() async {
    SharedPreferences.setMockInitialValues({});
  });

  group('Mobile Platform Lifecycle & Resilience Verification', () {
    test('1. Mobile Login & Session Persistence across App Restarts', () async {
      final fixture = AssignmentFixture();

      // Student logs in on mobile device
      await fixture.login(1);
      expect(fixture.auth.isAuthenticated, isTrue);
      expect(fixture.auth.currentUser?.username, 'student1');
      expect(fixture.auth.token, isNotEmpty);

      // Simulate app kill and cold restart: fresh AuthService instance
      final restartedAuth = AuthService(
        baseUrl: 'https://assignments.test',
        httpClient: fixture.client,
      );
      await restartedAuth.restoreSession();

      expect(restartedAuth.isAuthenticated, isTrue);
      expect(restartedAuth.currentUser?.username, 'student1');
      expect(restartedAuth.token, fixture.auth.token);
    });

    test('2. Draft Saving, App Restart, and Resuming Session', () async {
      final fixture = AssignmentFixture();
      await fixture.login(1);

      // Student answers partially: saves draft for item 1
      const assignmentId = 1;
      const itemId = 1;
      const draftAnswer = '507';
      await fixture.service.persistDraft(assignmentId, itemId, draftAnswer);

      // Verify draft saved in local storage
      final savedDraft = await fixture.service.local(assignmentId, itemId, 'draft');
      expect(savedDraft?['answer'], draftAnswer);

      // Simulate app restart
      final restartedService = StudentAssignmentService(
        authService: fixture.auth,
        httpClient: fixture.client,
      );

      // Resumed session can read the stored draft
      final resumedDraft = await restartedService.local(assignmentId, itemId, 'draft');
      expect(resumedDraft?['answer'], draftAnswer);

      // When assignment detail is loaded, draft answer is preserved for resume
      final detail = await restartedService.detail(assignmentId);
      expect(detail.items.first.id, itemId);
      expect(resumedDraft?['answer'], '507');
    });

    test('3. Network Disconnection & Offline Retry with Key Idempotency', () async {
      final fixture = AssignmentFixture();
      await fixture.login(1);

      const assignmentId = 1;
      const itemId = 1;
      const answer = '42';

      // Simulate network disconnection right during submit
      fixture.loseResponse = true;

      // Submission throws API exception due to disconnected network
      await expectLater(
        fixture.service.submitAnswer(assignmentId, itemId, answer, 1200),
        throwsA(isA<AssignmentApiException>()),
      );

      // Verify pending attempt record is persisted locally with unique submission key
      final pendingBeforeRestart = await fixture.service.pending(assignmentId, itemId);
      expect(pendingBeforeRestart, isNotNull);
      expect(pendingBeforeRestart?['answer'], answer);
      final originalKey = pendingBeforeRestart?['submission_key'];
      expect(originalKey, isNotNull);

      // Simulate app kill & restart during network outage
      final restartedService = StudentAssignmentService(
        authService: fixture.auth,
        httpClient: fixture.client,
      );

      final pendingAfterRestart = await restartedService.pending(assignmentId, itemId);
      expect(pendingAfterRestart?['submission_key'], originalKey);

      // Changing answer while an unconfirmed submission is pending must be blocked
      await expectLater(
        restartedService.submitAnswer(assignmentId, itemId, '999', 100),
        throwsA(isA<AssignmentApiException>().having((e) => e.status, 'status', 409)),
      );

      // Network restores: resending original answer reuses the exact same submission_key
      fixture.loseResponse = false;
      final retryResult = await restartedService.submitAnswer(assignmentId, itemId, answer, 1500);

      expect(retryResult['item_id'], itemId);
      // Pending record is cleared after confirmed server response
      expect(await restartedService.pending(assignmentId, itemId), isNull);

      // Exactly 1 key generated across the attempts, verifying idempotency
      expect(fixture.keys.length, 1);
      expect(fixture.keys.containsKey(originalKey), isTrue);
    });

    test('4. Account Switching & Multi-User Data Isolation', () async {
      final fixture = AssignmentFixture();

      // Student 1 logs in and works on assignment 1
      await fixture.login(1);
      await fixture.service.persistDraft(1, 1, 'student-1-draft');

      fixture.loseResponse = true;
      await expectLater(
        fixture.service.submitAnswer(1, 1, 'student-1-pending', 500),
        throwsA(isA<AssignmentApiException>()),
      );

      expect((await fixture.service.local(1, 1, 'draft'))?['answer'], 'student-1-draft');
      expect((await fixture.service.pending(1, 1))?['answer'], 'student-1-pending');

      // Start an in-flight request while Student 1 is logged in
      final delayed401 = Completer<http.Response>();
      final racingService = StudentAssignmentService(
        authService: fixture.auth,
        httpClient: MockClient((_) => delayed401.future),
      );
      final stalePendingCall = racingService.detail(1);
      final failure = expectLater(stalePendingCall, throwsA(isA<AssignmentApiException>()));

      // Student 1 logs out
      await fixture.auth.logout();
      expect(fixture.auth.isAuthenticated, isFalse);

      // Student 2 logs in on the same shared mobile device
      await fixture.login(2);
      expect(fixture.auth.currentUser?.id, 2);

      // Now Student 1's delayed 401 response finally arrives
      delayed401.complete(assignmentJson({'detail': 'Token expired'}, 401));
      await failure;

      // Student 2 must remain authenticated and unaffected by the stale 401
      expect(fixture.auth.isAuthenticated, isTrue);
      expect(fixture.auth.currentUser?.id, 2);

      // Student 2 must NEVER see Student 1's draft or pending submission
      expect(await fixture.service.local(1, 1, 'draft'), isNull);
      expect(await fixture.service.pending(1, 1), isNull);

      // Student 2 creates their own draft
      await fixture.service.persistDraft(1, 1, 'student-2-draft');
      expect((await fixture.service.local(1, 1, 'draft'))?['answer'], 'student-2-draft');

      // Student 2 logs out and Student 1 logs back in
      await fixture.auth.logout();
      await fixture.login(1);

      // Student 1's draft and pending attempt are restored completely intact
      expect((await fixture.service.local(1, 1, 'draft'))?['answer'], 'student-1-draft');
      expect((await fixture.service.pending(1, 1))?['answer'], 'student-1-pending');
    });
  });
}
