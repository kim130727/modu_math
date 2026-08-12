import 'content_models.dart';

enum ErrorCategory {
  understandingTarget('understanding_target', '문제 목표 이해 부족'),
  understandingGiven('understanding_given', '주어진 조건 해석 오류'),
  planningConcept('planning_concept', '개념 연결 오류'),
  planningOperation('planning_operation', '연산/해결 계획 선택 오류'),
  executionCalculation('execution_calculation', '계산 실수'),
  executionRepresentation('execution_representation', '표현 또는 식 작성 오류'),
  reviewCondition('review_condition', '조건 확인 부족'),
  reviewUnit('review_unit', '단위 또는 최종 검토 오류'),
  none('none', '오류 없음');

  const ErrorCategory(this.code, this.label);

  final String code;
  final String label;

  static ErrorCategory fromCode(String? code) {
    if (code == null) return ErrorCategory.none;
    return ErrorCategory.values.firstWhere(
      (e) => e.code == code,
      orElse: () => ErrorCategory.none,
    );
  }
}

class StudentAttempt {
  const StudentAttempt({
    required this.id,
    required this.problemId,
    required this.unit,
    required this.answer,
    required this.isCorrect,
    required this.timestamp,
    this.hintLevelUsed = 0,
    this.timeSpentSeconds = 0,
    this.errorCategory = ErrorCategory.none,
  });

  final String id;
  final String problemId;
  final String unit;
  final String answer;
  final bool isCorrect;
  final DateTime timestamp;
  final int hintLevelUsed;
  final int timeSpentSeconds;
  final ErrorCategory errorCategory;

  factory StudentAttempt.fromJson(Map<String, dynamic> json) {
    return StudentAttempt(
      id: json['id']?.toString() ?? '',
      problemId: json['problemId']?.toString() ?? '',
      unit: json['unit']?.toString() ?? '미분류',
      answer: json['answer']?.toString() ?? '',
      isCorrect: json['isCorrect'] == true,
      timestamp: json['timestamp'] != null
          ? DateTime.parse(json['timestamp'].toString())
          : DateTime.now(),
      hintLevelUsed: _readInt(json['hintLevelUsed']) ?? 0,
      timeSpentSeconds: _readInt(json['timeSpentSeconds']) ?? 0,
      errorCategory: ErrorCategory.fromCode(json['errorCategory']?.toString()),
    );
  }

  StudentAttempt copyWith({
    String? id,
    String? problemId,
    String? unit,
    String? answer,
    bool? isCorrect,
    DateTime? timestamp,
    int? hintLevelUsed,
    int? timeSpentSeconds,
    ErrorCategory? errorCategory,
  }) {
    return StudentAttempt(
      id: id ?? this.id,
      problemId: problemId ?? this.problemId,
      unit: unit ?? this.unit,
      answer: answer ?? this.answer,
      isCorrect: isCorrect ?? this.isCorrect,
      timestamp: timestamp ?? this.timestamp,
      hintLevelUsed: hintLevelUsed ?? this.hintLevelUsed,
      timeSpentSeconds: timeSpentSeconds ?? this.timeSpentSeconds,
      errorCategory: errorCategory ?? this.errorCategory,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'problemId': problemId,
      'unit': unit,
      'answer': answer,
      'isCorrect': isCorrect,
      'timestamp': timestamp.toIso8601String(),
      'hintLevelUsed': hintLevelUsed,
      'timeSpentSeconds': timeSpentSeconds,
      'errorCategory': errorCategory.code,
    };
  }
}

class LearningHintUsage {
  const LearningHintUsage({
    required this.level,
    required this.usedAt,
  });

  final int level;
  final DateTime usedAt;

  factory LearningHintUsage.fromJson(Map<String, dynamic> json) {
    return LearningHintUsage(
      level: _readInt(json['level']) ?? 0,
      usedAt: _readDateTime(json['usedAt']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'level': level,
      'usedAt': usedAt.toIso8601String(),
    };
  }
}

class LearningSubmission {
  const LearningSubmission({
    required this.answer,
    required this.isCorrect,
    required this.submittedAt,
  });

  final String answer;
  final bool isCorrect;
  final DateTime submittedAt;

  factory LearningSubmission.fromJson(Map<String, dynamic> json) {
    return LearningSubmission(
      answer: json['answer']?.toString() ?? '',
      isCorrect: json['isCorrect'] == true,
      submittedAt: _readDateTime(json['submittedAt']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'answer': answer,
      'isCorrect': isCorrect,
      'submittedAt': submittedAt.toIso8601String(),
    };
  }
}

class LearningSession {
  const LearningSession({
    required this.sessionId,
    required this.problemId,
    required this.unit,
    required this.skillIds,
    required this.startedAt,
    required this.finishedAt,
    required this.hints,
    required this.submissions,
  });

  final String sessionId;
  final String problemId;
  final String unit;
  final List<String> skillIds;
  final DateTime startedAt;
  final DateTime? finishedAt;
  final List<LearningHintUsage> hints;
  final List<LearningSubmission> submissions;

  bool? get isFirstAttemptCorrect {
    if (submissions.isEmpty) {
      return null;
    }
    return submissions.first.isCorrect;
  }

  bool get isFinallyCorrect {
    return submissions.any((submission) => submission.isCorrect);
  }

  int get submissionCount => submissions.length;

  int get maxHintLevel {
    var maxLevel = 0;
    for (final hint in hints) {
      if (hint.level > maxLevel) {
        maxLevel = hint.level;
      }
    }
    return maxLevel;
  }

  Duration? get timeSpent {
    final finished = finishedAt;
    if (finished == null) {
      return null;
    }
    return finished.difference(startedAt);
  }

  factory LearningSession.fromJson(Map<String, dynamic> json) {
    final rawHints = json['hints'];
    final rawSubmissions = json['submissions'];
    final rawSkillIds = json['skillIds'];
    return LearningSession(
      sessionId: json['sessionId']?.toString() ?? '',
      problemId: json['problemId']?.toString() ?? '',
      unit: json['unit']?.toString() ?? '미분류',
      skillIds: rawSkillIds is List
          ? rawSkillIds.map((skill) => skill.toString()).toList()
          : const [],
      startedAt: _readDateTime(json['startedAt']),
      finishedAt: json['finishedAt'] == null
          ? null
          : DateTime.tryParse(json['finishedAt'].toString()),
      hints: rawHints is List
          ? rawHints
              .whereType<Map<String, dynamic>>()
              .map(LearningHintUsage.fromJson)
              .toList()
          : const [],
      submissions: rawSubmissions is List
          ? rawSubmissions
              .whereType<Map<String, dynamic>>()
              .map(LearningSubmission.fromJson)
              .toList()
          : const [],
    );
  }

  LearningSession copyWith({
    DateTime? finishedAt,
    List<LearningHintUsage>? hints,
    List<LearningSubmission>? submissions,
  }) {
    return LearningSession(
      sessionId: sessionId,
      problemId: problemId,
      unit: unit,
      skillIds: skillIds,
      startedAt: startedAt,
      finishedAt: finishedAt ?? this.finishedAt,
      hints: hints ?? this.hints,
      submissions: submissions ?? this.submissions,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'sessionId': sessionId,
      'problemId': problemId,
      'unit': unit,
      'skillIds': skillIds,
      'startedAt': startedAt.toIso8601String(),
      'finishedAt': finishedAt?.toIso8601String(),
      'hints': hints.map((hint) => hint.toJson()).toList(),
      'submissions':
          submissions.map((submission) => submission.toJson()).toList(),
    };
  }
}

class DailySummary {
  const DailySummary({
    required this.date,
    required this.totalAttempted,
    required this.totalCorrect,
    required this.streakDays,
  });

  final DateTime date;
  final int totalAttempted;
  final int totalCorrect;
  final int streakDays;

  double get accuracy =>
      totalAttempted == 0 ? 0.0 : totalCorrect / totalAttempted;
}

class SkillMastery {
  const SkillMastery({
    required this.unit,
    required this.totalAttempted,
    required this.totalCorrect,
    required this.lastAttemptAt,
  });

  final String unit;
  final int totalAttempted;
  final int totalCorrect;
  final DateTime? lastAttemptAt;

  double get accuracy =>
      totalAttempted == 0 ? 0.0 : totalCorrect / totalAttempted;

  String get masteryLevel {
    if (totalAttempted == 0) return '시작 전';
    if (accuracy >= 0.8) return '잘하고 있어요';
    if (accuracy >= 0.5) return '연습 중';
    return '복습 필요';
  }
}

class LearningProgressSummary {
  const LearningProgressSummary({
    required this.results,
  });

  final List<LearningProblemResult> results;

  factory LearningProgressSummary.fromAttempts({
    required List<ProblemSummary> problems,
    required List<StudentAttempt> attempts,
  }) {
    final problemById = {
      for (final problem in problems) problem.id: problem,
    };
    final latestByProblem = <String, StudentAttempt>{};
    for (final attempt in attempts) {
      final existing = latestByProblem[attempt.problemId];
      if (existing == null || attempt.timestamp.isAfter(existing.timestamp)) {
        latestByProblem[attempt.problemId] = attempt;
      }
    }

    final results = <LearningProblemResult>[];
    for (final entry in latestByProblem.entries) {
      final problem = problemById[entry.key];
      if (problem == null) {
        continue;
      }
      final attempt = entry.value;
      results.add(
        LearningProblemResult(
          problem: problem,
          answer: attempt.answer,
          isCorrect: attempt.isCorrect,
        ),
      );
    }
    return LearningProgressSummary(results: results);
  }

  int get solvedCount => results.length;

  int get correctCount => results.where((result) => result.isCorrect).length;

  double get accuracy => solvedCount == 0 ? 0 : correctCount / solvedCount;

  List<LearningProblemResult> get wrongResults =>
      results.where((result) => !result.isCorrect).toList();

  LearningProblemResult? resultFor(String problemId) {
    return results
        .where((result) => result.problem.id == problemId)
        .firstOrNull;
  }
}

class LearningProblemResult {
  const LearningProblemResult({
    required this.problem,
    required this.answer,
    required this.isCorrect,
  });

  final ProblemSummary problem;
  final String answer;
  final bool isCorrect;
}

int? _readInt(Object? value) {
  if (value is int) {
    return value;
  }
  return int.tryParse(value?.toString() ?? '');
}

DateTime _readDateTime(Object? value) {
  return DateTime.tryParse(value?.toString() ?? '') ?? DateTime.now();
}

extension _FirstOrNull<T> on Iterable<T> {
  T? get firstOrNull {
    final iterator = this.iterator;
    if (!iterator.moveNext()) {
      return null;
    }
    return iterator.current;
  }
}
