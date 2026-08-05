import '../models/content_models.dart';
import '../models/tutor_models.dart';
import '../utils/answer_normalizer.dart';
import '../utils/tutor_text_sanitizer.dart';
import 'ai_tutor_service.dart';

class MockAiTutorService extends AiTutorService {
  const MockAiTutorService();

  @override
  TutorMode get mode => TutorMode.mock;

  @override
  String get label => 'Mock';

  @override
  List<TutorMessage> startSession(ProblemContent content) {
    return [
      _tutor(
        '좋아요. 빠른 점검 모드로 같이 볼게요.\n'
        '문제에서 무엇을 고르라고 했는지 먼저 말해 볼까요?',
        TutorReplyType.greeting,
      ),
    ];
  }

  @override
  Future<TutorMessage> hint({
    required ProblemContent content,
    required List<TutorMessage> messages,
    required int hintLevel,
  }) async {
    return _tutor(
      '힌트예요.\n'
      '보기 하나만 골라 문제의 말과 맞는지 살펴보세요.\n'
      '어느 보기부터 볼까요?',
      TutorReplyType.hint,
    );
  }

  @override
  Future<TutorMessage> nextQuestion({
    required ProblemContent content,
    required List<TutorMessage> messages,
    required int stepIndex,
  }) async {
    return _tutor(
      _questionFor(content, stepIndex),
      TutorReplyType.question,
    );
  }

  @override
  Future<TutorMessage> respondToStudent({
    required ProblemContent content,
    required List<TutorMessage> messages,
    required String message,
    required int stepIndex,
  }) async {
    if (isSameAnswer(message, content.correctAnswer)) {
      return _tutor(
        '맞아요. 정답과 같아요.\n'
        '왜 그렇게 골랐는지 한 문장으로 말해 볼까요?',
        TutorReplyType.correct,
      );
    }

    return _tutor(
      '좋아요. 그 생각을 문제 조건과 다시 맞춰 볼게요.\n'
      '${_questionFor(content, stepIndex)}',
      TutorReplyType.question,
    );
  }

  @override
  Future<TutorMessage> reviewAnswer({
    required ProblemContent content,
    required List<TutorMessage> messages,
    required String answer,
  }) async {
    if (isSameAnswer(answer, content.correctAnswer)) {
      return _tutor(
        '맞아요. 잘 골랐어요.\n'
        '이제 다음 문제로 넘어가도 좋아요.',
        TutorReplyType.correct,
      );
    }

    return _tutor(
      '아직 정답과 달라요.\n'
      '바로 답을 보기보다 보기 하나를 다시 확인해 볼까요?',
      TutorReplyType.retry,
    );
  }

  String _questionFor(ProblemContent content, int stepIndex) {
    final steps = content.steps;
    if (steps.isNotEmpty) {
      final step = steps[stepIndex.clamp(0, steps.length - 1)];
      return '${step.explanation}\n이 단계에서 알 수 있는 값을 말해 보세요.';
    }
    return '문제에서 주어진 조건 하나를 찾아 말해 볼까요?';
  }

  TutorMessage _tutor(String text, TutorReplyType type) {
    return TutorMessage(
      role: TutorMessageRole.tutor,
      text: sanitizeTutorText(text),
      replyType: type,
      createdAt: DateTime.now(),
    );
  }
}
