import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/app/app.dart';
import 'package:modu_math_app/models/content_models.dart';
import 'package:modu_math_app/models/learning_progress.dart';
import 'package:modu_math_app/models/student_profile.dart';
import 'package:modu_math_app/screens/student_home_screen.dart';
import 'package:modu_math_app/services/content_repository.dart';
import 'package:modu_math_app/services/learning_progress_repository.dart';
import 'package:modu_math_app/theme/app_theme.dart';

void main() {
  testWidgets('renders the student home with clear Korean learning actions',
      (tester) async {
    await tester.pumpWidget(
      MaterialApp(
        theme: buildKidsTheme(),
        home: StudentHomeScreen(
          repository: _FakeContentRepository(),
          progressRepository: _FakeProgressRepository(),
        ),
      ),
    );

    await tester.pumpAndSettle();

    expect(find.text('모두수학'), findsOneWidget);
    expect(find.textContaining('오늘은 한 문제씩'), findsOneWidget);
    expect(find.text('오늘 학습 시작'), findsOneWidget);
    expect(find.text('단원에서 고르기'), findsOneWidget);

    await tester.scrollUntilVisible(
      find.text('단원별 학습'),
      240,
      scrollable: find.byType(Scrollable).first,
    );

    expect(find.text('단원별 학습'), findsOneWidget);
    expect(find.text('2학기 1. 곱셈'), findsWidgets);
    expect(find.text('Rule Tutor'), findsNothing);
  });

  testWidgets('switches the extracted UI copy to Ukrainian', (tester) async {
    await tester.pumpWidget(
      ModuMathApp(
        contentRepository: _FakeContentRepository(),
        progressRepository: _FakeProgressRepository(),
      ),
    );

    await tester.pumpAndSettle();

    await tester.tap(find.byIcon(Icons.language_rounded));
    await tester.pumpAndSettle();

    expect(find.text('Моду Математика'), findsOneWidget);
    expect(find.textContaining('Спробуємо сьогодні'), findsOneWidget);
    expect(find.text('Почати сьогодні'), findsOneWidget);
    expect(find.text('Обрати розділ'), findsOneWidget);

    await tester.tap(find.text('Обрати розділ'));
    await tester.pumpAndSettle();

    expect(find.text('Навчання за розділами'), findsOneWidget);
    expect(find.text('Оберіть розділ на сьогодні'), findsOneWidget);
    expect(find.textContaining('2 семестр'), findsOneWidget);
    expect(find.text('Множення'), findsOneWidget);
  });
}

class _FakeContentRepository extends ContentRepository {
  @override
  Future<ProblemManifest> loadManifest() async {
    return const ProblemManifest(
      version: 'test',
      problems: [
        ProblemSummary(
          id: 'P001',
          grade: 3,
          subject: 'math',
          unit: '2학기 1. 곱셈',
          type: 'multiplication',
          title: '곱이 더 큰 것을 고르세요.',
          path: '',
          raw: {
            'semester': '2학기',
            'unitNumber': 1,
            'unitTopic': '곱셈',
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
  Future<List<StudentAttempt>> getAttempts() async {
    return const [];
  }

  @override
  Future<List<LearningSession>> getLearningSessions() async {
    return const [];
  }

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
  Future<List<StudentAttempt>> getReviewQueue() async {
    return const [];
  }

  @override
  Future<List<SkillMastery>> getSkillMasteries() async {
    return const [];
  }

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
