class StudentProfile {
  const StudentProfile({
    required this.id,
    required this.name,
    required this.grade,
    this.targetDailyCount = 10,
    this.streakDays = 1,
    this.lastActiveDate,
  });

  final String id;
  final String name;
  final int grade;
  final int targetDailyCount;
  final int streakDays;
  final DateTime? lastActiveDate;

  factory StudentProfile.defaultProfile() {
    return StudentProfile(
      id: 'default_student_1',
      name: '학생',
      grade: 3,
      targetDailyCount: 10,
      streakDays: 1,
      lastActiveDate: DateTime.now(),
    );
  }

  factory StudentProfile.fromJson(Map<String, dynamic> json) {
    return StudentProfile(
      id: json['id']?.toString() ?? 'default_student_1',
      name: json['name']?.toString() ?? '학생',
      grade: _readInt(json['grade']) ?? 3,
      targetDailyCount: _readInt(json['targetDailyCount']) ?? 10,
      streakDays: _readInt(json['streakDays']) ?? 1,
      lastActiveDate: json['lastActiveDate'] != null
          ? DateTime.tryParse(json['lastActiveDate'].toString())
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'grade': grade,
      'targetDailyCount': targetDailyCount,
      'streakDays': streakDays,
      'lastActiveDate': lastActiveDate?.toIso8601String(),
    };
  }

  StudentProfile copyWith({
    String? id,
    String? name,
    int? grade,
    int? targetDailyCount,
    int? streakDays,
    DateTime? lastActiveDate,
  }) {
    return StudentProfile(
      id: id ?? this.id,
      name: name ?? this.name,
      grade: grade ?? this.grade,
      targetDailyCount: targetDailyCount ?? this.targetDailyCount,
      streakDays: streakDays ?? this.streakDays,
      lastActiveDate: lastActiveDate ?? this.lastActiveDate,
    );
  }
}

int? _readInt(Object? value) {
  if (value is int) {
    return value;
  }
  return int.tryParse(value?.toString() ?? '');
}
