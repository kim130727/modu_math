import 'package:shared_preferences/shared_preferences.dart';

import '../models/content_models.dart';
import '../models/learning_progress.dart';
import '../models/student_profile.dart';
import 'learning_progress_repository.dart';
import 'local_progress_repository.dart';

class PersistentProgressRepository implements LearningProgressRepository {
  PersistentProgressRepository({
    this.storageKey = defaultStorageKey,
  });

  static const defaultStorageKey = 'modu_math_progress_v1';

  final String storageKey;
  LocalProgressRepository? _delegate;

  Future<LocalProgressRepository> _repository() async {
    final existing = _delegate;
    if (existing != null) {
      return existing;
    }

    final preferences = await SharedPreferences.getInstance();
    final source = preferences.getString(storageKey);
    final repository = source == null
        ? LocalProgressRepository()
        : _parseStoredProgress(source);
    _delegate = repository;
    return repository;
  }

  LocalProgressRepository _parseStoredProgress(String source) {
    try {
      return LocalProgressRepository.fromJsonString(source);
    } on FormatException {
      return LocalProgressRepository();
    } on TypeError {
      return LocalProgressRepository();
    }
  }

  Future<void> _save(LocalProgressRepository repository) async {
    final preferences = await SharedPreferences.getInstance();
    await preferences.setString(storageKey, repository.toJsonString());
  }

  @override
  Future<StudentProfile> getProfile() async {
    return (await _repository()).getProfile();
  }

  @override
  Future<void> saveProfile(StudentProfile profile) async {
    final repository = await _repository();
    await repository.saveProfile(profile);
    await _save(repository);
  }

  @override
  Future<List<StudentAttempt>> getAttempts() async {
    return (await _repository()).getAttempts();
  }

  @override
  Future<void> recordAttempt({
    required ProblemSummary problem,
    required String answer,
    required bool isCorrect,
    int hintLevelUsed = 0,
    int timeSpentSeconds = 0,
    ErrorCategory errorCategory = ErrorCategory.none,
  }) async {
    final repository = await _repository();
    await repository.recordAttempt(
      problem: problem,
      answer: answer,
      isCorrect: isCorrect,
      hintLevelUsed: hintLevelUsed,
      timeSpentSeconds: timeSpentSeconds,
      errorCategory: errorCategory,
    );
    await _save(repository);
  }

  @override
  Future<DailySummary> getDailySummary(DateTime date) async {
    return (await _repository()).getDailySummary(date);
  }

  @override
  Future<List<SkillMastery>> getSkillMasteries() async {
    return (await _repository()).getSkillMasteries();
  }

  @override
  Future<List<StudentAttempt>> getReviewQueue() async {
    return (await _repository()).getReviewQueue();
  }

  @override
  Future<void> updateAttemptErrorCategory({
    required String attemptId,
    required ErrorCategory category,
  }) async {
    final repository = await _repository();
    await repository.updateAttemptErrorCategory(
      attemptId: attemptId,
      category: category,
    );
    await _save(repository);
  }

  @override
  Future<void> clearAll() async {
    final repository = await _repository();
    await repository.clearAll();
    await _save(repository);
  }
}
