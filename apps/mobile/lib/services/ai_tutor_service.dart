import '../models/content_models.dart';
import '../models/tutor_models.dart';
import '../utils/tutor_text_sanitizer.dart';

abstract class AiTutorService {
  const AiTutorService();

  TutorMode get mode;

  String get label;

  List<TutorMessage> startSession(ProblemContent content);

  Future<TutorMessage> hint({
    required ProblemContent content,
    required List<TutorMessage> messages,
    required int hintLevel,
  });

  Future<TutorMessage> nextQuestion({
    required ProblemContent content,
    required List<TutorMessage> messages,
    required int stepIndex,
  });

  Future<TutorMessage> respondToStudent({
    required ProblemContent content,
    required List<TutorMessage> messages,
    required String message,
    required int stepIndex,
  });

  Future<TutorMessage> reviewAnswer({
    required ProblemContent content,
    required List<TutorMessage> messages,
    required String answer,
  });

  TutorMessage student(String text) {
    return TutorMessage(
      role: TutorMessageRole.student,
      text: sanitizeTutorText(text),
      createdAt: DateTime.now(),
    );
  }
}
