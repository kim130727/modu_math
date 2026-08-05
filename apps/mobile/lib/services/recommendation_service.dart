import '../models/content_models.dart';
import '../models/learning_progress.dart';
import 'learning_progress_repository.dart';

class RecommendedProblem {
  const RecommendedProblem({
    required this.problem,
    required this.reason,
    required this.tag,
  });

  final ProblemSummary problem;
  final String reason;
  final String tag;
}

class RecommendationService {
  const RecommendationService();

  Future<List<RecommendedProblem>> getDailyRecommendation({
    required List<ProblemSummary> allProblems,
    required LearningProgressRepository progressRepository,
    int targetCount = 10,
  }) async {
    final attempts = await progressRepository.getAttempts();
    final reviewQueue = await progressRepository.getReviewQueue();

    final latestByProblem = <String, StudentAttempt>{};
    for (final a in attempts) {
      final existing = latestByProblem[a.problemId];
      if (existing == null || a.timestamp.isAfter(existing.timestamp)) {
        latestByProblem[a.problemId] = a;
      }
    }

    final recommendations = <RecommendedProblem>[];
    final addedProblemIds = <String>{};

    // 1. Spaced repetition review problems.
    for (final reviewAttempt in reviewQueue) {
      if (recommendations.length >= targetCount) break;
      final problem = allProblems.firstWhere(
        (p) => p.id == reviewAttempt.problemId,
        orElse: () => ProblemSummary(
          id: reviewAttempt.problemId,
          grade: 3,
          subject: 'math',
          unit: reviewAttempt.unit,
          type: 'review',
          title: reviewAttempt.problemId,
          path: '',
          raw: const {},
        ),
      );

      if (!addedProblemIds.contains(problem.id)) {
        addedProblemIds.add(problem.id);
        recommendations.add(
          RecommendedProblem(
            problem: problem,
            reason: '이전에 틀린 문제를 간격 복습으로 다시 풀어봅니다.',
            tag: '오답 복습',
          ),
        );
      }
    }

    // 2. Weak concept practice from repeated error categories.
    final weakConcepts = _repeatedErrorConcepts(attempts);
    for (final weakConcept in weakConcepts) {
      if (recommendations.length >= targetCount) break;
      final weakProblems = allProblems.where((problem) {
        return problem.unit == weakConcept.unit &&
            !addedProblemIds.contains(problem.id) &&
            !latestByProblem.containsKey(problem.id);
      });
      for (final problem in weakProblems) {
        if (recommendations.length >= targetCount) break;
        addedProblemIds.add(problem.id);
        recommendations.add(
          RecommendedProblem(
            problem: problem,
            reason:
                '${weakConcept.category.label} 오류가 반복되어 같은 단원의 문제로 다시 확인합니다.',
            tag: '취약 개념',
          ),
        );
      }
    }

    // 3. Unsolved / new problems.
    for (final problem in allProblems) {
      if (recommendations.length >= targetCount) break;
      if (!addedProblemIds.contains(problem.id) &&
          !latestByProblem.containsKey(problem.id)) {
        addedProblemIds.add(problem.id);
        recommendations.add(
          RecommendedProblem(
            problem: problem,
            reason: '오늘 새로 도전하는 3학년 수학 개념 문제입니다.',
            tag: '오늘의 도전',
          ),
        );
      }
    }

    // 4. Fallback: retry older problems to fill up to targetCount.
    if (recommendations.length < targetCount) {
      for (final problem in allProblems) {
        if (recommendations.length >= targetCount) break;
        if (!addedProblemIds.contains(problem.id)) {
          addedProblemIds.add(problem.id);
          recommendations.add(
            RecommendedProblem(
              problem: problem,
              reason: '완벽한 개념 숙달을 위해 다시 확인해보는 문제입니다.',
              tag: '개념 다지기',
            ),
          );
        }
      }
    }

    return recommendations;
  }

  List<_WeakConcept> _repeatedErrorConcepts(List<StudentAttempt> attempts) {
    final counts = <_WeakConcept, int>{};
    for (final attempt in attempts) {
      if (attempt.isCorrect || attempt.errorCategory == ErrorCategory.none) {
        continue;
      }
      final concept = _WeakConcept(
        unit: attempt.unit,
        category: attempt.errorCategory,
      );
      counts[concept] = (counts[concept] ?? 0) + 1;
    }

    final repeated = counts.entries
        .where((entry) => entry.value >= 2)
        .map((entry) => entry.key)
        .toList()
      ..sort((a, b) {
        final byUnit = a.unit.compareTo(b.unit);
        return byUnit == 0
            ? a.category.code.compareTo(b.category.code)
            : byUnit;
      });
    return repeated;
  }
}

class _WeakConcept {
  const _WeakConcept({
    required this.unit,
    required this.category,
  });

  final String unit;
  final ErrorCategory category;

  @override
  bool operator ==(Object other) {
    return other is _WeakConcept &&
        other.unit == unit &&
        other.category == category;
  }

  @override
  int get hashCode => Object.hash(unit, category);
}
