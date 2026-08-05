enum TutorMessageRole {
  tutor,
  student,
}

enum TutorReplyType {
  greeting,
  hint,
  question,
  correct,
  retry,
}

enum TutorMode {
  rule,
  mock,
  backend,
}

class TutorMessage {
  const TutorMessage({
    required this.role,
    required this.text,
    required this.createdAt,
    this.replyType,
    this.choices = const [],
  });

  final TutorMessageRole role;
  final String text;
  final DateTime createdAt;
  final TutorReplyType? replyType;
  final List<String> choices;

  bool get isTutor => role == TutorMessageRole.tutor;
}
