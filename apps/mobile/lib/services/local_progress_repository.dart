import 'dart:convert';

import '../models/content_models.dart';
import '../models/learning_progress.dart';
import '../models/student_profile.dart';
import 'learning_progress_repository.dart';

class LocalProgressRepository implements LearningProgressRepository {
  LocalProgressRepository({
    StudentProfile? initialProfile,
    List<StudentAttempt>? initialAttempts,
  })  : _profile = initialProfile ?? StudentProfile.defaultProfile(),
        _attempts = List<StudentAttempt>.from(initialAttempts ?? const []);

  StudentProfile _profile;
  final List<StudentAttempt> _attempts;

  @override
  Future<StudentProfile> getProfile() async {
    return _profile;
  }

  @override
  Future<void> saveProfile(StudentProfile profile) async {
    _profile = profile;
  }

  @override
  Future<List<StudentAttempt>> getAttempts() async {
    return List.unmodifiable(_attempts);
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
    final now = DateTime.now();
    final attempt = StudentAttempt(
      id: 'attempt_${now.millisecondsSinceEpoch}_${problem.id}',
      problemId: problem.id,
      unit: problem.unit,
      answer: answer,
      isCorrect: isCorrect,
      timestamp: now,
      hintLevelUsed: hintLevelUsed,
      timeSpentSeconds: timeSpentSeconds,
      errorCategory: errorCategory,
    );

    _attempts.add(attempt);
    _updateStreak(now);
  }

  @override
  Future<DailySummary> getDailySummary(DateTime date) async {
    final startOfDay = DateTime(date.year, date.month, date.day);
    final endOfDay = startOfDay.add(const Duration(days: 1));

    final todayAttempts = _attempts.where((a) =>
        a.timestamp
            .isAfter(startOfDay.subtract(const Duration(milliseconds: 1))) &&
        a.timestamp.isBefore(endOfDay));

    final totalAttempted = todayAttempts.map((a) => a.problemId).toSet().length;
    final totalCorrect = todayAttempts
        .where((a) => a.isCorrect)
        .map((a) => a.problemId)
        .toSet()
        .length;

    return DailySummary(
      date: date,
      totalAttempted: totalAttempted,
      totalCorrect: totalCorrect,
      streakDays: _profile.streakDays,
    );
  }

  @override
  Future<List<SkillMastery>> getSkillMasteries() async {
    final groups = <String, List<StudentAttempt>>{};
    for (final attempt in _attempts) {
      groups.putIfAbsent(attempt.unit, () => []).add(attempt);
    }

    final masteries = <SkillMastery>[];
    for (final entry in groups.entries) {
      final unitAttempts = entry.value;
      final uniqueProblemsAttempted =
          unitAttempts.map((a) => a.problemId).toSet();
      final uniqueProblemsCorrect = unitAttempts
          .where((a) => a.isCorrect)
          .map((a) => a.problemId)
          .toSet();

      DateTime? lastAt;
      for (final a in unitAttempts) {
        if (lastAt == null || a.timestamp.isAfter(lastAt)) {
          lastAt = a.timestamp;
        }
      }

      masteries.add(
        SkillMastery(
          unit: entry.key,
          totalAttempted: uniqueProblemsAttempted.length,
          totalCorrect: uniqueProblemsCorrect.length,
          lastAttemptAt: lastAt,
        ),
      );
    }

    masteries.sort((a, b) => a.unit.compareTo(b.unit));
    return masteries;
  }

  @override
  Future<List<StudentAttempt>> getReviewQueue() async {
    final now = DateTime.now();
    final latestByProblem = <String, StudentAttempt>{};

    for (final attempt in _attempts) {
      final existing = latestByProblem[attempt.problemId];
      if (existing == null || attempt.timestamp.isAfter(existing.timestamp)) {
        latestByProblem[attempt.problemId] = attempt;
      }
    }

    final reviewItems = <StudentAttempt>[];
    for (final attempt in latestByProblem.values) {
      if (!attempt.isCorrect) {
        final daysDiff = now.difference(attempt.timestamp).inDays;
        if (daysDiff >= 1) {
          reviewItems.add(attempt);
        }
      }
    }

    reviewItems.sort((a, b) => a.timestamp.compareTo(b.timestamp));
    return reviewItems;
  }

  @override
  Future<void> updateAttemptErrorCategory({
    required String attemptId,
    required ErrorCategory category,
  }) async {
    final index = _attempts.indexWhere((a) => a.id == attemptId);
    if (index != -1) {
      _attempts[index] = _attempts[index].copyWith(errorCategory: category);
    } else if (_attempts.isNotEmpty) {
      final lastIndex = _attempts.length - 1;
      _attempts[lastIndex] =
          _attempts[lastIndex].copyWith(errorCategory: category);
    }
  }

  @override
  Future<void> clearAll() async {
    _attempts.clear();
  }

  void _updateStreak(DateTime now) {
    final last = _profile.lastActiveDate;
    if (last == null) {
      _profile = _profile.copyWith(streakDays: 1, lastActiveDate: now);
      return;
    }

    final lastDay = DateTime(last.year, last.month, last.day);
    final today = DateTime(now.year, now.month, now.day);
    final diff = today.difference(lastDay).inDays;

    if (diff == 1) {
      _profile = _profile.copyWith(
        streakDays: _profile.streakDays + 1,
        lastActiveDate: now,
      );
    } else if (diff > 1) {
      _profile = _profile.copyWith(
        streakDays: 1,
        lastActiveDate: now,
      );
    } else {
      _profile = _profile.copyWith(lastActiveDate: now);
    }
  }

  String toJsonString() {
    return jsonEncode({
      'profile': _profile.toJson(),
      'attempts': _attempts.map((a) => a.toJson()).toList(),
    });
  }

  factory LocalProgressRepository.fromJsonString(String source) {
    final decoded = jsonDecode(source) as Map<String, dynamic>;
    final profile = decoded['profile'] != null
        ? StudentProfile.fromJson(decoded['profile'] as Map<String, dynamic>)
        : StudentProfile.defaultProfile();
    final rawAttempts = decoded['attempts'];
    final attempts = rawAttempts is List
        ? rawAttempts
            .whereType<Map<String, dynamic>>()
            .map(StudentAttempt.fromJson)
            .toList()
        : <StudentAttempt>[];
    return LocalProgressRepository(
      initialProfile: profile,
      initialAttempts: attempts,
    );
  }
}
