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
      final ruleCode = _diagnosticRuleCodeFor(content, diagnostics, answer);
      return ruleCode == null || ruleCode.isEmpty ? null : ruleCode;
    }
    final code = errors[answer.trim()]?.toString();
    if (code != null && code.isNotEmpty) {
      return code;
    }
    final ruleCode = _diagnosticRuleCodeFor(content, diagnostics, answer);
    return ruleCode == null || ruleCode.isEmpty ? null : ruleCode;
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

String? _diagnosticRuleCodeFor(
  ProblemContent content,
  Map<String, dynamic> diagnostics,
  String answer,
) {
  final rules = diagnostics['rules'];
  if (rules is! List) {
    return null;
  }
  for (final rule in rules.whereType<Map>()) {
    final condition = rule['condition']?.toString().trim();
    final code = rule['code']?.toString().trim();
    if (condition == null ||
        condition.isEmpty ||
        code == null ||
        code.isEmpty) {
      continue;
    }
    if (_matchesDiagnosticCondition(content, answer, condition)) {
      return code;
    }
  }
  return null;
}

bool _matchesDiagnosticCondition(
  ProblemContent content,
  String answer,
  String condition,
) {
  final numericAnswer = num.tryParse(answer.trim());
  final correct = num.tryParse(content.correctAnswer.trim());
  return switch (condition) {
    'answer_equals_given_value' => _answerEqualsGivenValue(content, answer),
    'numeric_wrong_answer' =>
      numericAnswer != null && (correct == null || numericAnswer != correct),
    'addition_with_carry_wrong_answer' => numericAnswer != null &&
        (correct == null || numericAnswer != correct) &&
        _hasCarry(_additionTerms(content)),
    _ => false,
  };
}

bool _answerEqualsGivenValue(ProblemContent content, String answer) {
  final given = content.solvable['given'];
  if (given is! List) {
    return false;
  }
  for (final item in given.whereType<Map>()) {
    final value = item['value'];
    if (value != null && value.toString().trim() == answer.trim()) {
      return true;
    }
  }
  return false;
}

List<int> _additionTerms(ProblemContent content) {
  final steps = content.solvable['steps'];
  if (steps is! List) {
    return const [];
  }
  for (final step in steps.whereType<Map>()) {
    final expr = step['expr']?.toString().trim();
    if (expr != null && RegExp(r'^\s*\d+\s*(?:\+\s*\d+\s*)+$').hasMatch(expr)) {
      return RegExp(r'\d+')
          .allMatches(expr)
          .map((match) => int.parse(match.group(0)!))
          .toList();
    }
  }
  return const [];
}

bool _hasCarry(List<int> terms) {
  var carry = 0;
  final maxDigits = terms
      .map((term) => term.toString().length)
      .fold<int>(0, (max, length) => length > max ? length : max);
  for (var index = 0; index < maxDigits; index += 1) {
    final divisor = _pow10(index);
    final sum = terms.fold<int>(
      carry,
      (total, term) => total + (term ~/ divisor) % 10,
    );
    if (sum >= 10) {
      return true;
    }
    carry = sum ~/ 10;
  }
  return false;
}

int _pow10(int exponent) {
  var result = 1;
  for (var index = 0; index < exponent; index += 1) {
    result *= 10;
  }
  return result;
}
