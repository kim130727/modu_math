import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/testing.dart';
import 'package:http/http.dart' as http;
import 'package:modu_math_app/app/app.dart';
import 'package:modu_math_app/models/auth_user.dart';
import 'package:modu_math_app/models/content_models.dart';
import 'package:modu_math_app/models/learning_progress.dart';
import 'package:modu_math_app/models/student_profile.dart';
import 'package:modu_math_app/screens/auth_screen.dart';
import 'package:modu_math_app/services/auth_service.dart';
import 'package:modu_math_app/services/content_repository.dart';
import 'package:modu_math_app/services/learning_progress_repository.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  setUp(() {
    SharedPreferences.setMockInitialValues({});
  });

  testWidgets('AuthScreen translates to Ukrainian and English dynamically',
      (tester) async {
    final authService = AuthService(baseUrl: 'http://test-server');

    await tester.pumpWidget(
      ModuMathApp(
        authService: authService,
        contentRepository: _FakeContentRepository(),
        progressRepository: _FakeProgressRepository(),
      ),
    );
    await tester.pumpAndSettle();

    // 1. Initially Korean. Tap Auth (account icon) to open AuthScreen.
    await tester.tap(find.byIcon(Icons.account_circle_outlined));
    await tester.pumpAndSettle();

    expect(find.text('학습 계정 로그인'), findsOneWidget);
    expect(find.text('로그인'), findsOneWidget);
    expect(find.text('회원가입'), findsOneWidget);
    expect(find.text('아이디 (사용자 이름)'), findsOneWidget);
    expect(find.text('비밀번호'), findsOneWidget);
    expect(find.text('로그인하기'), findsOneWidget);

    // 2. Switch to Ukrainian (1st tap on global LanguageToggleButton)
    await tester.tap(find.byIcon(Icons.language_rounded));
    await tester.pumpAndSettle();

    expect(find.text('Вхід до облікового запису'), findsOneWidget);
    expect(find.text('Вхід'), findsOneWidget);
    expect(find.text('Реєстрація'), findsOneWidget);
    expect(find.text('ID (ім’я користувача)'), findsOneWidget);
    expect(find.text('Пароль'), findsOneWidget);
    expect(find.text('Увійти'), findsOneWidget);

    // Switch to Register tab
    await tester.tap(find.text('Реєстрація'));
    await tester.pumpAndSettle();

    expect(find.text('ID (ім’я користувача)'), findsOneWidget);
    expect(find.text('Електронна пошта (необов’язково)'), findsOneWidget);
    expect(find.text('Пароль (від 8 символів)'), findsOneWidget);
    expect(find.text('Підтвердження пароля'), findsOneWidget);
    expect(find.text('Завершити реєстрацію'), findsOneWidget);

    // Trigger password mismatch error in Ukrainian
    await tester.enterText(
        find.widgetWithText(TextFormField, 'ID (ім’я користувача)'), 'alice');
    await tester.enterText(
        find.widgetWithText(TextFormField, 'Пароль (від 8 символів)'), '12345678');
    await tester.enterText(
        find.widgetWithText(TextFormField, 'Підтвердження пароля'), '87654321');
    await tester.tap(find.text('Завершити реєстрацію'));
    await tester.pumpAndSettle();

    expect(find.text('Паролі не збігаються.'), findsOneWidget);

    // 3. Switch to English (2nd tap on global LanguageToggleButton)
    await tester.tap(find.byIcon(Icons.language_rounded));
    await tester.pumpAndSettle();

    expect(find.text('Study Account Login'), findsOneWidget);
    expect(find.text('Log In'), findsOneWidget);
    expect(find.text('Sign Up'), findsOneWidget);
    expect(find.text('Complete Sign Up'), findsOneWidget);
    expect(find.text('Passwords do not match.'), findsOneWidget);
  });

  testWidgets('Account Info Dialog translates dynamically to Ukrainian and English',
      (tester) async {
    final mockClient = MockClient((request) async {
      return http.Response('OK', 200);
    });
    final authService = AuthService(
      baseUrl: 'http://test-server',
      httpClient: mockClient,
    );

    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(AuthService.tokenStorageKey, 'test_token');
    await prefs.setString(
      AuthService.userStorageKey,
      jsonEncode(const AuthUser(id: 1, username: 'kim130727', email: 'kim@test.com').toJson()),
    );
    await authService.restoreSession();

    await tester.pumpWidget(
      ModuMathApp(
        authService: authService,
        contentRepository: _FakeContentRepository(),
        progressRepository: _FakeProgressRepository(),
      ),
    );
    await tester.pumpAndSettle();

    // 1. Switch language to Ukrainian first (Image 1 scenario)
    await tester.tap(find.byIcon(Icons.language_rounded));
    await tester.pumpAndSettle();

    // Tap account icon (logged in)
    await tester.tap(find.byIcon(Icons.account_circle));
    await tester.pumpAndSettle();

    // Dialog should be in Ukrainian
    expect(find.text('Обліковий запис kim130727'), findsOneWidget);
    expect(
      find.text(
          'Ви увійшли в систему, і ваш прогрес навчання безпечно синхронізується з сервером.'),
      findsOneWidget,
    );
    expect(find.text('Закрити'), findsOneWidget);
    expect(find.text('Вийти'), findsOneWidget);

    // 2. Close and switch language to English
    await tester.tap(find.text('Закрити'));
    await tester.pumpAndSettle();

    await tester.tap(find.byIcon(Icons.language_rounded));
    await tester.pumpAndSettle();

    await tester.tap(find.byIcon(Icons.account_circle));
    await tester.pumpAndSettle();

    expect(find.text("kim130727's Account"), findsOneWidget);
    expect(
      find.text(
          'You are currently logged in, and your learning progress is securely synced with the server.'),
      findsOneWidget,
    );
    expect(find.text('Close'), findsOneWidget);
    expect(find.text('Log Out'), findsOneWidget);
  });
}

class _FakeContentRepository extends ContentRepository {
  @override
  Future<ProblemManifest> loadManifest() async {
    return const ProblemManifest(
      version: 'test',
      problems: [],
      raw: {},
    );
  }
}

class _FakeProgressRepository implements LearningProgressRepository {
  @override
  Future<void> clearAll() async {}
  @override
  Future<List<StudentAttempt>> getAttempts() async => const [];
  @override
  Future<List<LearningSession>> getLearningSessions() async => const [];
  @override
  Future<LearningSession> startLearningSession({
    required ProblemSummary problem,
    required List<String> skillIds,
  }) async {
    return LearningSession(
      sessionId: 'test',
      problemId: 'P1',
      unit: 'test',
      skillIds: [],
      startedAt: DateTime.now(),
      finishedAt: null,
      hints: const [],
      submissions: const [],
    );
  }
  @override
  Future<void> recordSessionHint({required String sessionId, required int level}) async {}
  @override
  Future<void> recordSessionSubmission({
    required String sessionId,
    required String answer,
    required bool isCorrect,
  }) async {}
  @override
  Future<DailySummary> getDailySummary(DateTime date) async {
    return DailySummary(date: date, totalAttempted: 0, totalCorrect: 0, streakDays: 1);
  }
  @override
  Future<StudentProfile> getProfile() async {
    return StudentProfile(id: '1', name: 'Student', grade: 3, targetDailyCount: 10, streakDays: 1, lastActiveDate: DateTime.now());
  }
  @override
  Future<List<StudentAttempt>> getReviewQueue() async => const [];
  @override
  Future<List<SkillMastery>> getSkillMasteries() async => const [];
  @override
  Future<void> recordAttempt({
    required ProblemSummary problem,
    required String answer,
    required bool isCorrect,
    int hintLevelUsed = 0,
    int timeSpentSeconds = 0,
    ErrorCategory errorCategory = ErrorCategory.none,
  }) async {}
  @override
  Future<void> saveProfile(StudentProfile profile) async {}
  @override
  Future<void> updateAttemptErrorCategory({
    required String attemptId,
    required ErrorCategory category,
  }) async {}
}
