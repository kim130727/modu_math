import '../models/content_models.dart';
import '../utils/problem_text_sanitizer.dart';

class SolvableHint {
  const SolvableHint({
    required this.level,
    required this.title,
    required this.body,
  });

  final int level;
  final String title;
  final String body;
}

class SolvableHintService {
  const SolvableHintService();

  List<SolvableHint> buildHints(ProblemContent content) {
    return [
      SolvableHint(
        level: 1,
        title: '1단계: 구해야 할 것',
        body: _withoutAnswer(
          content,
          '이 문제에서는 ${_readText(content.solvable['target'], fallback: '무엇을 구해야 하는지')} 확인해 보세요.',
        ),
      ),
      SolvableHint(
        level: 2,
        title: '2단계: 해결 방법',
        body: _withoutAnswer(
          content,
          [
            '방법: ${_readText(content.solvable['method'], fallback: '문제에 맞는 식이나 규칙을 세워 보세요.')}',
            '계획: ${_readText(content.solvable['plan'], fallback: '주어진 조건을 차례대로 사용해 보세요.')}',
          ].join('\n'),
        ),
      ),
      SolvableHint(
        level: 3,
        title: '3단계: 계산 시작',
        body: _withoutAnswer(
          content,
          _firstStepText(content),
        ),
      ),
      SolvableHint(
        level: 4,
        title: '4단계: 전체 풀이',
        body: _fullSolutionText(content),
      ),
    ];
  }

  String _firstStepText(ProblemContent content) {
    final steps = content.steps;
    if (steps.isEmpty) {
      return '첫 번째로 주어진 수와 조건을 확인한 뒤 식을 세워 보세요.';
    }
    return '첫 번째 단계: ${_stepText(steps.first)}';
  }

  String _fullSolutionText(ProblemContent content) {
    final parts = <String>[];
    final steps = content.steps;
    if (steps.isNotEmpty) {
      parts.add(
        steps.indexed.map((entry) {
          return '${entry.$1 + 1}. ${_stepText(entry.$2, includeValue: true)}';
        }).join('\n'),
      );
    }

    final explanation = _readText(content.solvable['explanation']);
    if (explanation.isNotEmpty) {
      parts.add('설명: $explanation');
    }

    final checks = _readText(content.solvable['checks']);
    if (checks.isNotEmpty) {
      parts.add('확인: $checks');
    }

    if (parts.isEmpty) {
      return '등록된 풀이 데이터가 부족해요. 주어진 조건을 다시 확인하고 답을 검산해 보세요.';
    }
    return parts.join('\n\n');
  }

  String _stepText(SolutionStep step, {bool includeValue = false}) {
    final explanation = sanitizeProblemText(step.explanation).trim();
    final value = sanitizeProblemText(step.value).trim();
    if (includeValue && value.isNotEmpty) {
      return '$explanation = $value';
    }
    return explanation.isEmpty ? '주어진 조건을 이용해 첫 계산을 시작해 보세요.' : explanation;
  }

  String _withoutAnswer(ProblemContent content, String text) {
    final answer = content.correctAnswer.trim();
    if (answer.isEmpty) {
      return text;
    }
    return text.replaceAll(answer, '□');
  }
}

String _readText(Object? value, {String fallback = ''}) {
  final text = _readTextParts(value).join(', ').trim();
  return text.isEmpty ? fallback : text;
}

List<String> _readTextParts(Object? value) {
  if (value == null) {
    return const [];
  }
  if (value is String || value is num || value is bool) {
    final text = sanitizeProblemText(value.toString()).trim();
    return text.isEmpty ? const [] : [text];
  }
  if (value is List) {
    return value.expand(_readTextParts).toList();
  }
  if (value is Map) {
    const preferredKeys = [
      'text',
      'description',
      'explanation',
      'expr',
      'value',
      'label',
      'name',
      'result',
      'answer',
    ];
    final parts = <String>[];
    for (final key in preferredKeys) {
      if (value.containsKey(key)) {
        parts.addAll(_readTextParts(value[key]));
      }
    }
    if (parts.isNotEmpty) {
      return parts;
    }
    return value.values.expand(_readTextParts).toList();
  }
  return const [];
}
