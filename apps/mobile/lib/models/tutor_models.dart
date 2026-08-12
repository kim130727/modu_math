import 'learning_progress.dart';

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
    this.pendingDiagnosticCode,
    this.errorCategory = ErrorCategory.none,
  });

  final TutorMessageRole role;
  final String text;
  final DateTime createdAt;
  final TutorReplyType? replyType;
  final List<String> choices;
  final String? pendingDiagnosticCode;
  final ErrorCategory errorCategory;

  bool get isTutor => role == TutorMessageRole.tutor;
}
