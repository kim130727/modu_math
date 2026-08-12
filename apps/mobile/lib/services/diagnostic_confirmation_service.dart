import '../models/content_models.dart';
import '../models/tutor_models.dart';
import 'diagnostic_strategies/addition_diagnostic_strategy.dart';
import 'diagnostic_strategies/diagnostic_strategy.dart';

class DiagnosticConfirmationService {
  const DiagnosticConfirmationService({
    this.strategies = _defaultStrategies,
  });

  static const _defaultStrategies = <DiagnosticStrategy>[
    AdditionDiagnosticStrategy(),
    PlaceholderDiagnosticStrategy(
      name: 'geometry',
      keywords: ['geometry', 'shape', 'perimeter', 'area', '도형', '둘레', '넓이'],
      codePrefixes: ['geometry.', 'shape.'],
    ),
    PlaceholderDiagnosticStrategy(
      name: 'time',
      keywords: ['time', 'clock', 'elapsed', '시계', '시각', '시간'],
      codePrefixes: ['time.', 'clock.'],
    ),
    PlaceholderDiagnosticStrategy(
      name: 'measurement',
      keywords: ['measurement', 'unit', 'length', 'measure', '단위', '길이'],
      codePrefixes: ['measure.', 'unit.'],
    ),
    PlaceholderDiagnosticStrategy(
      name: 'fraction',
      keywords: ['fraction', '분수'],
      codePrefixes: ['fraction.'],
    ),
  ];

  final List<DiagnosticStrategy> strategies;

  DiagnosticPrompt? promptFor({
    required ProblemContent content,
    required String answer,
  }) {
    final code = diagnosticCodeFor(content: content, answer: answer);
    if (code == null) {
      return null;
    }

    for (final strategy in strategies) {
      if (!strategy.supports(content) &&
          !strategy.supportsDiagnosticCode(code)) {
        continue;
      }
      final prompt = strategy.promptFor(
        content: content,
        diagnosticCode: code,
        answer: answer,
      );
      if (prompt != null) {
        return prompt;
      }
    }
    return null;
  }

  DiagnosticPrompt? promptForCode({
    required ProblemContent content,
    required String diagnosticCode,
    required String answer,
  }) {
    for (final strategy in strategies) {
      if (!strategy.supports(content) &&
          !strategy.supportsDiagnosticCode(diagnosticCode)) {
        continue;
      }
      final prompt = strategy.promptFor(
        content: content,
        diagnosticCode: diagnosticCode,
        answer: answer,
      );
      if (prompt != null) {
        return prompt;
      }
    }
    return null;
  }

  DiagnosticResult? resultFor({
    required ProblemContent content,
    required String diagnosticCode,
    required String confirmationAnswer,
  }) {
    for (final strategy in strategies) {
      if (!strategy.supportsDiagnosticCode(diagnosticCode)) {
        continue;
      }
      final result = strategy.resultFor(
        content: content,
        diagnosticCode: diagnosticCode,
        confirmationAnswer: confirmationAnswer,
      );
      if (result != null) {
        return result;
      }
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
}
