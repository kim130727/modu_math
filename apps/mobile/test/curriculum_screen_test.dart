import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/models/content_models.dart';
import 'package:modu_math_app/models/learning_progress.dart';
import 'package:modu_math_app/models/student_profile.dart';
import 'package:modu_math_app/screens/curriculum_screen.dart';
import 'package:modu_math_app/services/content_repository.dart';
import 'package:modu_math_app/services/learning_progress_repository.dart';
import 'package:modu_math_app/l10n/app_strings.dart';
import 'package:modu_math_app/theme/app_theme.dart';

void main() {
  testWidgets('renders single focused unit when initialUnit is provided',
      (tester) async {
    final fakeRepo = _FakeCurriculumRepository();
    final fakeProgressRepo = _FakeProgressRepository();

    await tester.pumpWidget(
      MaterialApp(
        theme: buildKidsTheme(),
        home: CurriculumScreen(
          repository: fakeRepo,
          progressRepository: fakeProgressRepo,
          initialUnit: '3학년 2학기 3. 원',
        ),
      ),
    );

    await tester.pumpAndSettle();

    // 단원 상세 포커스 화면인지 확인
    expect(find.text('원 학습'), findsOneWidget);
    expect(find.text('전체 단원 학습 시작 (3문제)'), findsOneWidget);
    expect(find.text('소단원 선택 학습'), findsOneWidget);
    expect(find.text('원의 중심과 반지름'), findsOneWidget);

    // 다른 단원은 보이지 않아야 함
    expect(find.text('덧셈과 뺄셈'), findsNothing);

    // '전체 단원 보기' 클릭
    await tester.tap(find.text('전체 단원 보기').first);
    await tester.pumpAndSettle();

    // 전체 단원 목록 화면으로 복귀 확인
    expect(find.text('단원 학습'), findsOneWidget);
    expect(find.text('오늘 배울 단원을 골라요'), findsOneWidget);
    expect(find.text('수와 연산'), findsOneWidget);
    expect(find.text('도형'), findsOneWidget);
  });

  test('AppStrings localizes 기본 학습 to Basic Learning in English and other locales', () {
    final en = AppStrings.forLocale(const Locale('en'));
    expect(en.subUnitName('기본 학습'), 'Basic Learning');
    expect(en.subUnitName('__basicLearning__'), 'Basic Learning');

    final ko = AppStrings.forLocale(const Locale('ko'));
    expect(ko.subUnitName('기본 학습'), '기본 학습');
    expect(ko.subUnitName('Basic Learning'), '기본 학습');

    final ja = AppStrings.forLocale(const Locale('ja'));
    expect(ja.subUnitName('기본 학습'), '基本学習');

    final uk = AppStrings.forLocale(const Locale('uk'));
    expect(uk.subUnitName('기본 학습'), 'Базове навчання');
  });

  testWidgets('renders Basic Learning instead of 기본 학습 when locale is English',
      (tester) async {
    final fakeRepo = _FakeBasicLearningRepository();
    final fakeProgressRepo = _FakeProgressRepository();

    await tester.pumpWidget(
      AppLocaleScope(
        locale: const Locale('en'),
        onLocaleChanged: (_) {},
        child: MaterialApp(
          locale: const Locale('en'),
          localizationsDelegates: const [
            AppStringsDelegate(),
          ],
          supportedLocales: AppStrings.supportedLocales,
          theme: buildKidsTheme(),
          home: CurriculumScreen(
            repository: fakeRepo,
            progressRepository: fakeProgressRepo,
            initialUnit: '3학년 1학기 1. 덧셈과 뺄셈',
          ),
        ),
      ),
    );

    await tester.pumpAndSettle();

    // English unit title and sub-unit title should be rendered
    expect(find.text('Addition & Subtraction Learning'), findsOneWidget);
    expect(find.text('Sub-unit Practice'), findsOneWidget);
    expect(find.text('Basic Learning'), findsOneWidget);
    expect(find.text('기본 학습'), findsNothing);
  });
}

class _FakeBasicLearningRepository extends ContentRepository {
  @override
  Future<ProblemManifest> loadManifest() async {
    return const ProblemManifest(
      version: 'test',
      problems: [
        ProblemSummary(
          id: 'P_basic',
          grade: 3,
          subject: 'math',
          unit: '3학년 1학기 1. 덧셈과 뺄셈',
          type: 'addition',
          title: '덧셈 문제',
          path: '',
          raw: {
            'grade': 3,
            'semester': '1학기',
            'unitNumber': 1,
            'unitTopic': '덧셈과 뺄셈',
            'subUnit': '기본 학습',
          },
        ),
      ],
      raw: {},
    );
  }
}

class _FakeCurriculumRepository extends ContentRepository {
  @override
  Future<ProblemManifest> loadManifest() async {
    return const ProblemManifest(
      version: 'test',
      problems: [
        ProblemSummary(
          id: 'P1',
          grade: 3,
          subject: 'math',
          unit: '3학년 1학기 1. 덧셈과 뺄셈',
          type: 'addition',
          title: '덧셈 문제 1',
          path: '',
          raw: {
            'grade': 3,
            'semester': '1학기',
            'unitNumber': 1,
            'unitTopic': '덧셈과 뺄셈',
            'subUnit': '세 자리 수 덧셈',
          },
        ),
        ProblemSummary(
          id: 'P2',
          grade: 3,
          subject: 'math',
          unit: '3학년 2학기 3. 원',
          type: 'geometry',
          title: '원 문제 1',
          path: '',
          raw: {
            'grade': 3,
            'semester': '2학기',
            'unitNumber': 3,
            'unitTopic': '원',
            'subUnit': '원의 중심과 반지름',
          },
        ),
        ProblemSummary(
          id: 'P3',
          grade: 3,
          subject: 'math',
          unit: '3학년 2학기 3. 원',
          type: 'geometry',
          title: '원 문제 2',
          path: '',
          raw: {
            'grade': 3,
            'semester': '2학기',
            'unitNumber': 3,
            'unitTopic': '원',
            'subUnit': '원의 지름과 성질',
          },
        ),
        ProblemSummary(
          id: 'P4',
          grade: 3,
          subject: 'math',
          unit: '3학년 2학기 3. 원',
          type: 'geometry',
          title: '원 문제 3',
          path: '',
          raw: {
            'grade': 3,
            'semester': '2학기',
            'unitNumber': 3,
            'unitTopic': '원',
            'subUnit': '원의 지름과 성질',
          },
        ),
      ],
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
      sessionId: 'session_test',
      problemId: problem.id,
      unit: problem.unit,
      skillIds: skillIds,
      startedAt: DateTime(2026, 7, 23),
      finishedAt: null,
      hints: const [],
      submissions: const [],
    );
  }

  @override
  Future<void> recordSessionHint({
    required String sessionId,
    required int level,
  }) async {}

  @override
  Future<void> recordSessionSubmission({
    required String sessionId,
    required String answer,
    required bool isCorrect,
  }) async {}

  @override
  Future<DailySummary> getDailySummary(DateTime date) async {
    return DailySummary(
      date: date,
      totalAttempted: 0,
      totalCorrect: 0,
      streakDays: 1,
    );
  }

  @override
  Future<StudentProfile> getProfile() async {
    return StudentProfile(
      id: 'student_1',
      name: '민준',
      grade: 3,
      targetDailyCount: 10,
      streakDays: 1,
      lastActiveDate: DateTime(2026, 7, 23),
    );
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
