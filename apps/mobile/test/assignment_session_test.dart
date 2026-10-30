import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/services/assignment_session.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'helpers/assignment_fixture.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  setUp(() => SharedPreferences.setMockInitialValues({}));
  test('draft resume, server submission, navigation and final result',
      () async {
    final fixture = AssignmentFixture();
    await fixture.login();
    await fixture.service.persistDraft(1, 1, '42');
    final session =
        AssignmentSession(service: fixture.service, assignmentId: 1);
    addTearDown(session.dispose);
    await session.load();
    expect(session.answers[1], '42');
    expect(session.canSend, isTrue);
    await session.send();
    expect(session.completed, 1);
    expect(session.canSubmit, isFalse);
    expect(session.feedback[1], isNull);
    await session.move(1);
    session.change('10');
    await session.send();
    expect(session.canSubmit, isTrue);
    await session.finish();
    expect(session.assignment?.submittedAt, isNotNull);
    expect(session.assignment?.correct, 1);
    expect(session.canEdit, isFalse);
  });

  test('ambiguous send locks editing until the original request is resolved',
      () async {
    final fixture = AssignmentFixture();
    await fixture.login();
    final session =
        AssignmentSession(service: fixture.service, assignmentId: 1);
    addTearDown(session.dispose);
    await session.load();
    session.change('42');
    fixture.loseResponse = true;
    await session.send();
    expect(session.pending.contains(1), isTrue);
    expect(session.canEdit, isFalse);
    session.change('100');
    expect(session.answers[1], '42');
    await session.send();
    expect(session.pending, isEmpty);
    expect(fixture.keys.length, 1);
    expect(session.count(session.item!), 1);
  });

  test('false and zero are complete answers; partial multi-fields are not', () {
    expect(AssignmentSession.complete(false, 1), isTrue);
    expect(AssignmentSession.complete(0, 1), isTrue);
    expect(AssignmentSession.complete(['1', ''], 2), isFalse);
    expect(AssignmentSession.complete(['1', '2'], 2), isTrue);
  });

  test('disposed or switched-account sessions never submit as another student',
      () async {
    final fixture = AssignmentFixture();
    await fixture.login();
    final session =
        AssignmentSession(service: fixture.service, assignmentId: 1);
    await session.load();
    session.change('42');
    session.dispose();
    await fixture.login(2);
    await session.send();
    expect(fixture.posts, isEmpty);
  });
}
