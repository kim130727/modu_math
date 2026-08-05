import '../models/content_models.dart';
import '../models/learning_progress.dart';
import '../models/student_profile.dart';

abstract class LearningProgressRepository {
  Future<StudentProfile> getProfile();

  Future<void> saveProfile(StudentProfile profile);

  Future<List<StudentAttempt>> getAttempts();

  Future<void> recordAttempt({
    required ProblemSummary problem,
    required String answer,
    required bool isCorrect,
    int hintLevelUsed = 0,
    int timeSpentSeconds = 0,
    ErrorCategory errorCategory = ErrorCategory.none,
  });

  Future<DailySummary> getDailySummary(DateTime date);

  Future<List<SkillMastery>> getSkillMasteries();

  Future<List<StudentAttempt>> getReviewQueue();

  Future<void> updateAttemptErrorCategory({
    required String attemptId,
    required ErrorCategory category,
  });

  Future<void> clearAll();
}
