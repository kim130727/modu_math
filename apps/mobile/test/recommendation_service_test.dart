import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/models/content_models.dart';
import 'package:modu_math_app/models/learning_progress.dart';
import 'package:modu_math_app/services/local_progress_repository.dart';
import 'package:modu_math_app/services/recommendation_service.dart';

void main() {
  group('RecommendationService Tests', () {
    test('should recommend daily target problems from pool', () async {
      final repository = LocalProgressRepository();
      const recommendationService = RecommendationService();

      final allProblems = List.generate(
        15,
        (index) => ProblemSummary(
          id: 'P00$index',
          grade: 3,
          subject: 'math',
          unit: '단원 ${(index % 3) + 1}',
          type: 'calc',
          title: '문제 $index',
          path: '',
          raw: const {},
        ),
      );

      final recs = await recommendationService.getDailyRecommendation(
        allProblems: allProblems,
        progressRepository: repository,
        targetCount: 10,
      );

      expect(recs.length, equals(10));
      expect(recs.first.tag, equals('오늘의 도전'));
    });

    test('prioritizes review and repeated error concept practice', () async {
      final pastDate = DateTime.now().subtract(const Duration(days: 2));
      final repository = LocalProgressRepository(
        initialAttempts: [
          StudentAttempt(
            id: 'review_attempt',
            problemId: 'P-review',
            unit: '나눗셈',
            answer: '4',
            isCorrect: false,
            timestamp: pastDate,
            errorCategory: ErrorCategory.executionCalculation,
          ),
          StudentAttempt(
            id: 'weak_1',
            problemId: 'P-weak-1',
            unit: '곱셈',
            answer: '12',
            isCorrect: false,
            timestamp: DateTime.now(),
            errorCategory: ErrorCategory.planningOperation,
          ),
          StudentAttempt(
            id: 'weak_2',
            problemId: 'P-weak-2',
            unit: '곱셈',
            answer: '18',
            isCorrect: false,
            timestamp: DateTime.now().add(const Duration(minutes: 1)),
            errorCategory: ErrorCategory.planningOperation,
          ),
        ],
      );
      const recommendationService = RecommendationService();
      const allProblems = [
        ProblemSummary(
          id: 'P-review',
          grade: 3,
          subject: 'math',
          unit: '나눗셈',
          type: 'calc',
          title: '복습 문제',
          path: '',
          raw: {},
        ),
        ProblemSummary(
          id: 'P-weak-1',
          grade: 3,
          subject: 'math',
          unit: '곱셈',
          type: 'calc',
          title: '이미 틀린 문제 1',
          path: '',
          raw: {},
        ),
        ProblemSummary(
          id: 'P-weak-2',
          grade: 3,
          subject: 'math',
          unit: '곱셈',
          type: 'calc',
          title: '이미 틀린 문제 2',
          path: '',
          raw: {},
        ),
        ProblemSummary(
          id: 'P-weak-3',
          grade: 3,
          subject: 'math',
          unit: '곱셈',
          type: 'calc',
          title: '취약 개념 새 문제',
          path: '',
          raw: {},
        ),
        ProblemSummary(
          id: 'P-new',
          grade: 3,
          subject: 'math',
          unit: '길이와 시간',
          type: 'calc',
          title: '새 문제',
          path: '',
          raw: {},
        ),
      ];

      final recs = await recommendationService.getDailyRecommendation(
        allProblems: allProblems,
        progressRepository: repository,
        targetCount: 3,
      );

      expect(recs.map((rec) => rec.problem.id), [
        'P-review',
        'P-weak-3',
        'P-new',
      ]);
      expect(recs.map((rec) => rec.tag), [
        '오답 복습',
        '취약 개념',
        '오늘의 도전',
      ]);
      expect(recs[1].reason, contains('연산/해결 계획 선택 오류'));
    });
  });
}
