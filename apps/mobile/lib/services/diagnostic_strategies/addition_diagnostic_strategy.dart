import '../../models/content_models.dart';
import '../../models/learning_progress.dart';
import 'diagnostic_strategy.dart';

class AdditionDiagnosticStrategy extends DiagnosticStrategy {
  const AdditionDiagnosticStrategy();

  @override
  bool supports(ProblemContent content) {
    final signature = [
      content.summary.type,
      content.semantic['problem_type'],
      content.solvable['problem_type'],
      content.solvable['method'],
      content.solvable['diagnostics'] is Map
          ? (content.solvable['diagnostics'] as Map)['skills']
          : null,
    ].whereType<Object>().join(' ').toLowerCase();
    return signature.contains('add') || signature.contains('addition');
  }

  @override
  bool supportsDiagnosticCode(String diagnosticCode) {
    return diagnosticCode.startsWith('plan.copy_one_part') ||
        diagnosticCode.startsWith('execute.add_');
  }

  @override
  DiagnosticPrompt? promptFor({
    required ProblemContent content,
    required String diagnosticCode,
    required String answer,
  }) {
    switch (diagnosticCode) {
      case 'plan.copy_one_part':
        return const DiagnosticPrompt(
          diagnosticCode: 'plan.copy_one_part',
          text: '잠깐 확인해 볼게요.\n'
              '이 문제에서 구해야 하는 것은 상현이네 가족의 수인가요, 용진이네 가족의 수인가요, 아니면 두 가족이 캔 전체 수인가요?',
        );
      case 'execute.add_carry':
        return const DiagnosticPrompt(
          diagnosticCode: 'execute.add_carry',
          text: '계산을 바로 고치기 전에 한 자리만 확인해 볼게요.\n'
              '일의 자리에서 9와 8을 더하면 얼마인가요?',
        );
    }
    return null;
  }

  @override
  DiagnosticResult? resultFor({
    required String diagnosticCode,
    required String confirmationAnswer,
  }) {
    switch (diagnosticCode) {
      case 'plan.copy_one_part':
        if (diagnosticTextMatchesAny(confirmationAnswer, const [
          '두 가족이 캔 전체 수',
          '전체 수',
          '모두',
          '합',
          '합계',
        ])) {
          return const DiagnosticResult(
            errorCategory: ErrorCategory.planningOperation,
            feedback: '맞아요. 구해야 하는 것은 두 가족이 캔 전체 수예요.\n'
                '그러면 한 가족의 수만 쓰지 말고 259와 248을 더해 볼게요.',
          );
        }
        return const DiagnosticResult(
          errorCategory: ErrorCategory.understandingTarget,
          feedback: '여기서 구해야 하는 것은 한 가족의 수가 아니라 두 가족이 캔 전체 수예요.\n'
              '그래서 259와 248을 함께 더해야 해요.',
        );
      case 'execute.add_carry':
        if (diagnosticTextMatchesAny(confirmationAnswer, const ['17'])) {
          return const DiagnosticResult(
            errorCategory: ErrorCategory.executionCalculation,
            feedback: '맞아요. 17이니까 일의 자리에는 7을 쓰고, 1을 십의 자리로 올려요.\n'
                '이제 십의 자리만 볼게요. 5와 4, 그리고 받아올린 1을 더하면 얼마인가요?',
            nextDiagnosticCode: 'execute.add_carry.tens',
          );
        }
        return const DiagnosticResult(
          errorCategory: ErrorCategory.executionCalculation,
          feedback: '9와 8을 더하면 17이에요. 그래서 일의 자리에는 7을 쓰고, 1을 십의 자리로 올려요.\n'
              '이제 십의 자리만 볼게요. 5와 4, 그리고 받아올린 1을 더하면 얼마인가요?',
          nextDiagnosticCode: 'execute.add_carry.tens',
        );
      case 'execute.add_carry.tens':
        if (diagnosticTextMatchesAny(confirmationAnswer, const ['10'])) {
          return const DiagnosticResult(
            errorCategory: ErrorCategory.executionCalculation,
            feedback: '좋아요. 5와 4와 1을 더하면 10이에요.\n'
                '십의 자리에는 0을 쓰고, 1을 백의 자리로 올려요. 마지막으로 백의 자리에서 2와 2와 받아올린 1을 더하면 얼마인가요?',
            nextDiagnosticCode: 'execute.add_carry.hundreds',
          );
        }
        return const DiagnosticResult(
          errorCategory: ErrorCategory.executionCalculation,
          feedback: '십의 자리에는 일의 자리에서 받아올린 1도 함께 더해야 해요.\n'
              '5와 4와 1을 더하면 얼마인지 다시 확인해 볼게요.',
          nextDiagnosticCode: 'execute.add_carry.tens',
        );
      case 'execute.add_carry.hundreds':
        if (diagnosticTextMatchesAny(confirmationAnswer, const ['5'])) {
          return const DiagnosticResult(
            errorCategory: ErrorCategory.executionCalculation,
            feedback: '맞아요. 백의 자리는 5예요.\n'
                '그래서 각 자리 숫자를 모으면 507이 됩니다.',
          );
        }
        return const DiagnosticResult(
          errorCategory: ErrorCategory.executionCalculation,
          feedback: '백의 자리도 십의 자리에서 받아올린 1을 함께 더해야 해요.\n'
              '2와 2와 1을 더하면 얼마인지 확인해 볼게요.',
          nextDiagnosticCode: 'execute.add_carry.hundreds',
        );
    }
    return null;
  }
}
