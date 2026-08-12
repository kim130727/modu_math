import '../models/content_models.dart';
import '../models/learning_progress.dart';
import '../models/tutor_models.dart';
import '../utils/answer_normalizer.dart';

class DiagnosticConfirmationService {
  const DiagnosticConfirmationService();

  DiagnosticPrompt? promptFor({
    required ProblemContent content,
    required String answer,
  }) {
    final code = diagnosticCodeFor(content: content, answer: answer);
    if (code == null) {
      return null;
    }

    switch (code) {
      case 'plan.copy_one_part':
        return const DiagnosticPrompt(
          diagnosticCode: 'plan.copy_one_part',
          text: '이 문제에서 구해야 하는 것은 무엇인가요?',
          choices: [
            '상현이네 가족의 수',
            '용진이네 가족의 수',
            '두 가족이 캔 전체 수',
          ],
        );
      case 'execute.add_carry':
        return const DiagnosticPrompt(
          diagnosticCode: 'execute.add_carry',
          text: '일의 자리에서 9와 8을 더하면 얼마인가요?\n'
              '그다음 받아올림이 필요한지 확인해 볼게요.',
          choices: ['17', '7', '18'],
        );
    }
    return null;
  }

  DiagnosticResult? resultFor({
    required String diagnosticCode,
    required String confirmationAnswer,
  }) {
    switch (diagnosticCode) {
      case 'plan.copy_one_part':
        if (_matchesAny(confirmationAnswer, const [
          '두 가족이 캔 전체 수',
          '전체 수',
          '모두',
          '합',
          '합계',
        ])) {
          return const DiagnosticResult(
            errorCategory: ErrorCategory.planningOperation,
            feedback: '맞아요. 구해야 하는 것은 두 가족이 캔 전체 수예요.\n'
                '한 가족의 수만 옮긴 것이 아니라 259와 248을 더해 볼게요.',
          );
        }
        return const DiagnosticResult(
          errorCategory: ErrorCategory.understandingTarget,
          feedback: '이 문제에서 구해야 하는 것은 한 가족의 수가 아니라 두 가족이 캔 전체 수예요.\n'
              '그래서 259와 248을 함께 더해야 해요.',
        );
      case 'execute.add_carry':
        return const DiagnosticResult(
          errorCategory: ErrorCategory.executionCalculation,
          feedback: '9와 8을 더하면 17이에요.\n'
              '일의 자리에 7을 쓰고 십의 자리로 1을 받아올림해서 다시 계산해 볼게요.',
        );
    }
    return null;
  }

  String? diagnosticCodeFor({
    required ProblemContent content,
    required String answer,
  }) {
    final diagnostics = content.solvable['diagnostics'];
    if (diagnostics is! Map<String, dynamic>) {
      return null;
    }
    final errors = diagnostics['errors'];
    if (errors is! Map<String, dynamic>) {
      return null;
    }
    final code = errors[answer.trim()]?.toString();
    return code == null || code.isEmpty ? null : code;
  }

  String? pendingCodeFrom(List<TutorMessage> messages) {
    for (final message in messages.reversed) {
      if (message.isTutor && message.pendingDiagnosticCode != null) {
        return message.pendingDiagnosticCode;
      }
      if (message.isTutor) {
        return null;
      }
    }
    return null;
  }

  bool _matchesAny(String value, List<String> expectedValues) {
    final normalized = normalizeAnswer(value);
    return expectedValues
        .map(normalizeAnswer)
        .any((expected) => normalized.contains(expected));
  }
}

class DiagnosticPrompt {
  const DiagnosticPrompt({
    required this.diagnosticCode,
    required this.text,
    required this.choices,
  });

  final String diagnosticCode;
  final String text;
  final List<String> choices;
}

class DiagnosticResult {
  const DiagnosticResult({
    required this.errorCategory,
    required this.feedback,
  });

  final ErrorCategory errorCategory;
  final String feedback;
}
