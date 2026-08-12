import '../../models/content_models.dart';
import '../../models/learning_progress.dart';
import '../../utils/answer_normalizer.dart';

abstract class DiagnosticStrategy {
  const DiagnosticStrategy();

  bool supports(ProblemContent content);

  bool supportsDiagnosticCode(String diagnosticCode);

  DiagnosticPrompt? promptFor({
    required ProblemContent content,
    required String diagnosticCode,
    required String answer,
  });

  DiagnosticResult? resultFor({
    required String diagnosticCode,
    required String confirmationAnswer,
  });
}

class DiagnosticPrompt {
  const DiagnosticPrompt({
    required this.diagnosticCode,
    required this.text,
    this.choices = const [],
  });

  final String diagnosticCode;
  final String text;
  final List<String> choices;
}

class DiagnosticResult {
  const DiagnosticResult({
    required this.errorCategory,
    required this.feedback,
    this.nextDiagnosticCode,
  });

  final ErrorCategory errorCategory;
  final String feedback;
  final String? nextDiagnosticCode;
}

bool diagnosticTextMatchesAny(String value, List<String> expectedValues) {
  final normalized = normalizeAnswer(value);
  return expectedValues
      .map(normalizeAnswer)
      .any((expected) => normalized.contains(expected));
}

class PlaceholderDiagnosticStrategy extends DiagnosticStrategy {
  const PlaceholderDiagnosticStrategy({
    required this.name,
    required this.keywords,
    required this.codePrefixes,
  });

  final String name;
  final List<String> keywords;
  final List<String> codePrefixes;

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
    return keywords.any(signature.contains);
  }

  @override
  bool supportsDiagnosticCode(String diagnosticCode) {
    return codePrefixes.any(diagnosticCode.startsWith);
  }

  @override
  DiagnosticPrompt? promptFor({
    required ProblemContent content,
    required String diagnosticCode,
    required String answer,
  }) {
    return null;
  }

  @override
  DiagnosticResult? resultFor({
    required String diagnosticCode,
    required String confirmationAnswer,
  }) {
    return null;
  }
}
