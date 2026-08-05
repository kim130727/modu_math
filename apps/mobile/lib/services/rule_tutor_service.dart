import '../models/content_models.dart';
import '../models/tutor_models.dart';
import '../utils/answer_normalizer.dart';
import '../utils/tutor_text_sanitizer.dart';
import 'ai_tutor_service.dart';

class RuleTutorService extends AiTutorService {
  const RuleTutorService();

  @override
  TutorMode get mode => TutorMode.rule;

  @override
  String get label => 'Rule';

  @override
  List<TutorMessage> startSession(ProblemContent content) {
    final steps = _tutorSteps(content);
    if (content.solvable.isEmpty) {
      return [
        _tutor(
          '이 문제에는 아직 풀이 규칙 데이터가 없어요.\n'
          '다른 문제를 먼저 풀어 보거나 잠시 후 다시 시도해 주세요.',
          TutorReplyType.retry,
        ),
      ];
    }
    if (steps.isEmpty) {
      return [
        _tutor(
          '풀이 데이터는 있지만 단계가 비어 있어요.\n'
          'steps 또는 plan이 있으면 단계별 튜터를 시작할 수 있어요.',
          TutorReplyType.retry,
        ),
      ];
    }
    return [_ruleResponse(content, steps, 0, _ruleIntro(content, steps))];
  }

  @override
  Future<TutorMessage> hint({
    required ProblemContent content,
    required List<TutorMessage> messages,
    required int hintLevel,
  }) async {
    final steps = _tutorSteps(content);
    final index = _lastRuleStepIndex(messages) ?? 0;
    final safeIndex = index.clamp(0, steps.length - 1);
    return _ruleResponse(
      content,
      steps,
      safeIndex,
      _confusionReply(content, steps[safeIndex], safeIndex),
    );
  }

  @override
  Future<TutorMessage> nextQuestion({
    required ProblemContent content,
    required List<TutorMessage> messages,
    required int stepIndex,
  }) async {
    final steps = _tutorSteps(content);
    final current = _lastRuleStepIndex(messages) ?? -1;
    final next = (current + 1).clamp(0, steps.length - 1);
    return _ruleResponse(
      content,
      steps,
      next,
      _renderRuleStep(content, steps, next, prefix: '좋아요. 다음 단계로 가 볼게요.'),
    );
  }

  @override
  Future<TutorMessage> respondToStudent({
    required ProblemContent content,
    required List<TutorMessage> messages,
    required String message,
    required int stepIndex,
  }) async {
    final steps = _tutorSteps(content);
    if (steps.isEmpty) {
      return _tutor('아직 안내할 풀이 단계가 없어요.', TutorReplyType.retry);
    }

    final cleanMessage = message.trim();
    final waitingIndex = _lastRuleStepIndex(messages) ?? 0;
    final safeIndex = waitingIndex.clamp(0, steps.length - 1);
    final step = steps[safeIndex];

    if (_wantsRestart(cleanMessage)) {
      return _ruleResponse(content, steps, 0, _ruleIntro(content, steps));
    }
    if (_asksForNext(cleanMessage)) {
      final next = (safeIndex + 1).clamp(0, steps.length - 1);
      return _ruleResponse(
        content,
        steps,
        next,
        _renderRuleStep(content, steps, next, prefix: '좋아요. 다음 단계로 가 볼게요.'),
      );
    }
    if (_isConfused(cleanMessage)) {
      return _ruleResponse(
        content,
        steps,
        safeIndex,
        _confusionReply(content, step, safeIndex),
      );
    }
    if (_answerMatchesStep(cleanMessage, step)) {
      final next = safeIndex + 1;
      if (next >= steps.length) {
        return _tutor(_complete(content), TutorReplyType.correct);
      }
      return _ruleResponse(
        content,
        steps,
        next,
        _renderRuleStep(content, steps, next, prefix: '좋아요. 맞게 찾았어요.'),
      );
    }

    final hint = _stepExpectedHint(content, step, safeIndex);
    return _ruleResponse(
      content,
      steps,
      safeIndex,
      '조금 다르게 본 것 같아요.\n'
      '${safeIndex + 1}단계: ${step.prompt}\n'
      '${hint.isEmpty ? '이 단계에서 확인해야 하는 값을 다시 입력해 볼까요?' : '$hint 다시 입력해 볼까요?'}',
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
        '좋아요. 최종 답이 맞아요.\n'
        '풀이 단계도 차근차근 잘 이어졌어요.',
        TutorReplyType.correct,
      );
    }
    return respondToStudent(
      content: content,
      messages: messages,
      message: answer,
      stepIndex: 0,
    );
  }

  TutorMessage _ruleResponse(
    ProblemContent content,
    List<_RuleStep> steps,
    int index,
    String reply,
  ) {
    return _tutor(
      reply,
      TutorReplyType.question,
      choices: _stepChoices(content, steps, index),
    );
  }

  String _ruleIntro(ProblemContent content, List<_RuleStep> steps) {
    if (_isPlaceValueMatching(content)) {
      final multiple = _givenValue(content, 'obj.multiple')?.toString();
      final highlighted =
          _givenValue(content, 'obj.highlighted_value')?.toString();
      final lead = multiple != null && highlighted != null
          ? '$multiple에서 표시된 $highlighted의 실제 값을 찾아보는 문제예요.'
          : '자리값을 보면서 같은 값을 만드는 식을 찾아볼게요.';
      return _renderRuleStep(content, steps, 0, prefix: lead);
    }

    final method =
        (content.solvable['method'] ?? content.solvable['problem_type'] ?? '풀이')
            .toString()
            .replaceAll('_', ' ');
    return _renderRuleStep(
      content,
      steps,
      0,
      prefix: 'Rule Tutor로 단계별 풀이를 시작할게요.\n풀이 방법: $method',
    );
  }

  String _renderRuleStep(
    ProblemContent content,
    List<_RuleStep> steps,
    int index, {
    String prefix = '',
  }) {
    if (_isPlaceValueMatching(content)) {
      return _renderPlaceValueStep(content, steps, index, prefix: prefix);
    }

    final step = steps[index];
    final hint = _stepExpectedHint(content, step, index);
    final lines = <String>[
      ...prefix.split('\n').where((line) => line.trim().isNotEmpty),
      '${index + 1}단계: ${step.prompt}',
      if (step.explanation.isNotEmpty) step.explanation,
      hint.isEmpty ? '이 단계에서 필요한 값을 입력해 보세요.' : hint,
    ];
    return lines.take(4).join('\n');
  }

  String _renderPlaceValueStep(
    ProblemContent content,
    List<_RuleStep> steps,
    int index, {
    String prefix = '',
  }) {
    final step = steps[index];
    final lines = <String>[
      ...prefix.split('\n').where((line) => line.trim().isNotEmpty),
    ];

    final hasHighlighted = _givenValue(content, 'obj.multiple') != null &&
        _givenValue(content, 'obj.highlighted_value') != null;
    if (!hasHighlighted) {
      lines
        ..add('${index + 1}단계: ${step.prompt}')
        ..add('표시된 부분의 자리값을 보고 같은 곱셈식을 고르면 돼요.')
        ..add('아래 보기 중 같은 값을 만드는 식을 선택해 보세요.');
      return lines.take(4).join('\n');
    }

    if (index == 0) {
      lines
        ..add('1단계: 먼저 표시된 숫자가 얼마를 뜻하는지 봐요.')
        ..add('예를 들어 869에서 6은 십의 자리라서 60을 뜻해요.')
        ..add('그럼 표시된 부분은 무엇에 4를 곱한 걸까요?');
    } else if (index == 1) {
      lines
        ..add('2단계: ${step.prompt}')
        ..add('이제 60 × 4를 계산해 표시된 부분의 값을 확인해요.')
        ..add('60 × 4는 얼마일까요?');
    } else {
      final choices = _givenValue(content, 'obj.choice_set');
      lines.add('${index + 1}단계: ${step.prompt}');
      if (choices is List) {
        lines.add('보기: ${choices.join(', ')}');
      }
      lines.add('같은 값을 만드는 보기를 골라 입력해 보세요.');
    }
    return lines.take(4).join('\n');
  }

  String _confusionReply(ProblemContent content, _RuleStep step, int index) {
    if (_isPlaceValueMatching(content)) {
      if (index == 0) {
        return '좋아요. 다시 천천히 볼게요.\n'
            '숫자는 어느 자리에 있는지에 따라 값이 달라져요.\n'
            '표시된 숫자가 십의 자리에 있으면 10배로 생각해요.\n'
            '그 값에 몇을 곱해야 하는지 찾아볼까요?';
      }
      if (index == 1) {
        return '앞에서 표시된 부분의 값을 확인했어요.\n'
            '이제 그 값에 곱하는 수만 계산하면 돼요.\n'
            '60 × 4를 다시 계산해 볼까요?';
      }
      return '이제 새 계산을 하는 단계가 아니에요.\n'
          '앞에서 찾은 값과 같은 보기를 찾으면 돼요.\n'
          '보기 중 값이 같은 식을 골라보세요.';
    }

    final hint = _stepExpectedHint(content, step, index);
    return '좋아요. 이 단계만 다시 볼게요.\n'
        '${index + 1}단계: ${step.prompt}\n'
        '${hint.isEmpty ? '문제에서 확인해야 하는 값을 하나만 찾아보세요.' : hint}';
  }

  String _complete(ProblemContent content) {
    final answer = content.correctAnswer;
    if (answer.isNotEmpty) {
      return '좋아요. 풀이 단계가 모두 끝났어요.\n'
          '최종 답은 $answer입니다.\n'
          '이제 답칸에 맞게 정리해 보세요.';
    }
    return '좋아요. 풀이 단계가 모두 끝났어요.\n'
        '이제 문제의 답이나 보기를 맞게 정리해 보세요.';
  }

  List<_RuleStep> _tutorSteps(ProblemContent content) {
    final derived = _deriveTutorSteps(content);
    if (derived.isNotEmpty) {
      return derived;
    }

    final rawSteps = content.solvable['steps'] is List
        ? content.solvable['steps'] as List
        : content.solvable['plan'] is List
            ? content.solvable['plan'] as List
            : const [];

    return rawSteps.indexed.map((entry) {
      final index = entry.$1 + 1;
      final raw = entry.$2;
      if (raw is String) {
        return _RuleStep(prompt: _cleanPrompt(raw), expected: '');
      }
      if (raw is Map<String, dynamic>) {
        final prompt = _firstString(
          raw,
          const [
            'question',
            'prompt',
            'goal',
            'description',
            'explanation',
            'expr',
            'text',
            'id',
          ],
        );
        final explanation = _firstString(raw, const ['explanation']);
        final expected = raw.containsKey('value')
            ? _studentExpectedAnswer(raw['value'])
            : raw.containsKey('expected')
                ? _studentExpectedAnswer(raw['expected'])
                : '';
        return _RuleStep(
          prompt:
              prompt.isEmpty ? '$index번째 풀이 단계를 확인해요.' : _cleanPrompt(prompt),
          expected: expected,
          explanation: _cleanPrompt(explanation),
        );
      }
      return _RuleStep(prompt: '$index번째 풀이 단계를 확인해요.', expected: '');
    }).toList();
  }

  List<_RuleStep> _deriveTutorSteps(ProblemContent content) {
    if (_isPlaceValueMatching(content)) {
      final target = _givenValue(content, 'obj.target')?.toString();
      if (target != null && target.trim().isNotEmpty) {
        return [
          _RuleStep(
            prompt: '표시된 부분이 실제로 어떤 곱셈식인지 보기에서 골라요.',
            expected: target.trim(),
            choices: _placeValueExpressionChoices(target.trim()),
          ),
        ];
      }
    }

    final method = (content.solvable['method'] ?? '').toString().toLowerCase();
    final type =
        (content.solvable['problem_type'] ?? '').toString().toLowerCase();
    if (!method.contains('compare') &&
        !method.contains('비교') &&
        !type.contains('compare') &&
        !type.contains('비교')) {
      return const [];
    }

    final expressions = _comparisonExpressions(content);
    if (expressions.length < 2) {
      return const [];
    }

    final evaluated = expressions
        .map((expr) => (expr, _evaluateArithmetic(expr)))
        .where((item) => item.$2 != null)
        .toList();
    if (evaluated.length != expressions.length) {
      return const [];
    }

    final steps = <_RuleStep>[
      for (final item in evaluated)
        _RuleStep(
          prompt: item.$1 == item.$2.toString()
              ? '${item.$1}은 이미 수로 주어졌어요.'
              : '${item.$1}의 값을 먼저 구해요.',
          expected: item.$2.toString(),
        ),
    ];
    steps.add(
      _RuleStep(
        prompt: '계산한 값을 비교해요. 조건에 맞는 것은 무엇일까요?',
        expected: content.correctAnswer,
      ),
    );
    return steps;
  }

  List<String> _stepChoices(
    ProblemContent content,
    List<_RuleStep> steps,
    int index,
  ) {
    if (steps.isEmpty) {
      return const [];
    }
    final step = steps[index.clamp(0, steps.length - 1)];
    final expected = step.expected.trim();
    if (expected.isEmpty) {
      return const [];
    }
    if (step.choices.isNotEmpty) {
      return _uniqueChoices(step.choices);
    }

    if (_isPlaceValueMatching(content)) {
      if (index == 0 &&
          _givenValue(content, 'obj.multiple') != null &&
          _givenValue(content, 'obj.highlighted_value') != null) {
        return _uniqueChoices(['6', expected, '600', '869']);
      }
      if (index == 1) {
        return _numericChoices(expected);
      }
      final choiceSet = _givenValue(content, 'obj.choice_set');
      if (choiceSet is List) {
        return _uniqueChoices(
          choiceSet.map((value) => value.toString()).toList(),
        );
      }
      return _uniqueChoices([expected]);
    }

    if (_looksNumber(expected)) {
      return _numericChoices(expected);
    }
    final problemChoices = content.choices;
    if (problemChoices.isNotEmpty && index == steps.length - 1) {
      return _uniqueChoices(problemChoices);
    }
    return _uniqueChoices([expected]);
  }

  List<String> _numericChoices(String expected) {
    final value = num.tryParse(expected);
    if (value == null) {
      return _uniqueChoices([expected]);
    }
    if (value == 0) {
      return const ['0', '1', '10', '100'];
    }
    final number = value.round();
    return _uniqueChoices([
      (number.abs() >= 10 ? number ~/ 10 : number + 10).toString(),
      number.toString(),
      (number * 10).toString(),
      (number + (number.abs() >= 100 ? 100 : 10)).toString(),
    ]);
  }

  TutorMessage _tutor(
    String text,
    TutorReplyType type, {
    List<String> choices = const [],
  }) {
    return TutorMessage(
      role: TutorMessageRole.tutor,
      text: sanitizeTutorText(text),
      replyType: type,
      choices: choices,
      createdAt: DateTime.now(),
    );
  }
}

class _RuleStep {
  const _RuleStep({
    required this.prompt,
    required this.expected,
    this.explanation = '',
    this.choices = const [],
  });

  final String prompt;
  final String expected;
  final String explanation;
  final List<String> choices;
}

bool _isPlaceValueMatching(ProblemContent content) {
  final problemType = [
    content.summary.type,
    content.semantic['problem_type'],
    content.solvable['problem_type'],
    content.solvable['method'],
    content.solvable['target'] is Map
        ? (content.solvable['target'] as Map)['type']
        : null,
  ].whereType<Object>().join(' ').toLowerCase();
  return problemType.contains('place_value') ||
      problemType.contains('matching_expression') ||
      problemType.contains('자리값');
}

Object? _givenValue(ProblemContent content, String ref) {
  final given = content.solvable['given'];
  if (given is! List) {
    return null;
  }
  for (final item in given.whereType<Map<String, dynamic>>()) {
    if (item['ref'] == ref) {
      return item['value'];
    }
  }
  return null;
}

String _firstString(Map<String, dynamic> source, List<String> keys) {
  for (final key in keys) {
    final value = source[key];
    if (value is String && value.trim().isNotEmpty) {
      return value.trim();
    }
  }
  return '';
}

String _studentExpectedAnswer(Object? value) {
  if (value is Map<String, dynamic>) {
    for (final key in const ['result', 'value', 'answer', 'count']) {
      if (value.containsKey(key)) {
        return value[key].toString();
      }
    }
  }
  return value?.toString() ?? '';
}

String _stepExpectedHint(ProblemContent content, _RuleStep step, int index) {
  final expected = step.expected.trim();
  if (expected.isEmpty) {
    return '';
  }
  if (step.prompt.contains('이미 수로 주어졌어요')) {
    return '그 수를 그대로 입력해 보세요.';
  }
  if (_isPlaceValueMatching(content)) {
    if (index == 0) {
      return '표시된 숫자의 자리가 어떤 값인지 먼저 확인해요.';
    }
    if (index == 1) {
      return '찾은 값에 몇을 곱해야 하는지 계산해 보세요.';
    }
    return '보기 중 앞에서 찾은 값과 같은 식을 찾아보세요.';
  }
  if (_looksNumber(expected)) {
    return '계산한 수를 입력해 보세요.';
  }
  return '이 단계에서 찾은 말이나 값을 입력해 보세요.';
}

int? _lastRuleStepIndex(List<TutorMessage> messages) {
  final pattern = RegExp(r'(\d+)단계:');
  for (final message in messages.reversed) {
    if (!message.isTutor) {
      continue;
    }
    final match = pattern.firstMatch(message.text);
    if (match != null) {
      return (int.tryParse(match.group(1) ?? '') ?? 1) - 1;
    }
  }
  return null;
}

bool _answerMatchesStep(String message, _RuleStep step) {
  final expected = step.expected.trim();
  if (expected.isEmpty) {
    return false;
  }
  final normalizedMessage = normalizeAnswer(message);
  final normalizedExpected = normalizeAnswer(expected);
  if (normalizedExpected.isNotEmpty &&
      normalizedMessage.contains(normalizedExpected)) {
    return true;
  }
  final expectedNumbers = RegExp(r'-?\d+(?:\.\d+)?')
      .allMatches(expected)
      .map((match) => match.group(0))
      .whereType<String>()
      .toSet();
  if (expectedNumbers.isEmpty) {
    return false;
  }
  final messageNumbers = RegExp(r'-?\d+(?:\.\d+)?')
      .allMatches(message)
      .map((match) => match.group(0))
      .whereType<String>()
      .toSet();
  return expectedNumbers.any(messageNumbers.contains);
}

bool _wantsRestart(String message) {
  final value = message.replaceAll(' ', '').toLowerCase();
  return ['처음', '다시', '시작', 'reset', 'restart'].any(value.contains);
}

bool _asksForNext(String message) {
  final value = message.replaceAll(' ', '').toLowerCase();
  return ['다음', '넘어', 'next'].any(value.contains);
}

bool _isConfused(String message) {
  final value = message.replaceAll(' ', '').toLowerCase();
  return ['모르', '이해', '무슨말', '헷갈', '어려', '힌트', '설명', 'help', 'confus']
      .any(value.contains);
}

List<String> _comparisonExpressions(ProblemContent content) {
  final inputs = content.solvable['inputs'];
  final quantities =
      inputs is Map<String, dynamic> ? inputs['quantities'] : null;
  if (quantities is Map<String, dynamic>) {
    return quantities.values
        .whereType<String>()
        .where((value) => value.trim().isNotEmpty)
        .toList();
  }

  final given = content.solvable['given'];
  if (given is! List) {
    return const [];
  }
  return given
      .whereType<Map<String, dynamic>>()
      .map((item) => item['value'])
      .whereType<String>()
      .where((value) => value.trim().isNotEmpty)
      .toList();
}

num? _evaluateArithmetic(String expression) {
  final text = expression
      .replaceAll('×', '*')
      .replaceAll('횞', '*')
      .replaceAll('x', '*')
      .replaceAll('X', '*')
      .replaceAll('÷', '/')
      .replaceAll('첨', '/')
      .replaceAll(' ', '');
  if (!RegExp(r'^[\d+\-*/().]+$').hasMatch(text)) {
    return null;
  }
  final tokens = RegExp(r'\d+(?:\.\d+)?|[+\-*/()]')
      .allMatches(text)
      .map((match) => match.group(0)!)
      .toList();
  var index = 0;
  late num Function() parseExpression;
  late num Function() parseTerm;
  late num Function() parseFactor;

  parseExpression = () {
    var value = parseTerm();
    while (index < tokens.length &&
        (tokens[index] == '+' || tokens[index] == '-')) {
      final op = tokens[index++];
      final right = parseTerm();
      value = op == '+' ? value + right : value - right;
    }
    return value;
  };

  parseTerm = () {
    var value = parseFactor();
    while (index < tokens.length &&
        (tokens[index] == '*' || tokens[index] == '/')) {
      final op = tokens[index++];
      final right = parseFactor();
      value = op == '*' ? value * right : value / right;
    }
    return value;
  };

  parseFactor = () {
    final token = tokens[index++];
    if (token == '(') {
      final value = parseExpression();
      if (index < tokens.length && tokens[index] == ')') {
        index++;
      }
      return value;
    }
    if (token == '-') {
      return -parseFactor();
    }
    return num.parse(token);
  };

  try {
    final value = parseExpression();
    return value % 1 == 0 ? value.toInt() : value;
  } catch (_) {
    return null;
  }
}

List<String> _placeValueExpressionChoices(String expression) {
  final match =
      RegExp(r'^\s*(\d+)\s*[×횞xX*]\s*(\d+)\s*$').firstMatch(expression);
  if (match == null) {
    return _uniqueChoices([expression]);
  }
  final left = int.parse(match.group(1)!);
  final right = int.parse(match.group(2)!);
  if (left % 10 == 0 && left != 0) {
    var base = left;
    while (base % 10 == 0) {
      base ~/= 10;
    }
    return _uniqueChoices([
      '$base × $right',
      '$base × ${right * 10}',
      '$left × $right',
      '${left * 10} × $right',
    ]);
  }
  return _uniqueChoices([
    '$left × $right',
    '${left * 10} × $right',
    '${left * 100} × $right',
    '${left ~/ 10} × $right',
  ]);
}

List<String> _uniqueChoices(List<String> values) {
  final seen = <String>{};
  final choices = <String>[];
  for (final value in values) {
    final text = value.trim();
    if (text.isEmpty) {
      continue;
    }
    final key = normalizeAnswer(text);
    if (seen.add(key)) {
      choices.add(text);
    }
  }
  return choices.take(4).toList();
}

bool _looksNumber(String value) {
  return RegExp(r'^-?\d+(?:\.\d+)?$').hasMatch(value.trim());
}

String _cleanPrompt(String value) {
  final text = sanitizeTutorText(value);
  if (_looksBrokenKorean(text)) {
    return '\uBB38\uC81C\uC5D0\uC11C \uD544\uC694\uD55C \uAC12\uC744 \uD655\uC778\uD574\uC694.';
  }
  return text;
}

bool _looksBrokenKorean(String value) {
  if (value.isEmpty) {
    return false;
  }
  return RegExp(r'[\u3400-\u9FFF\uFFFD]').hasMatch(value) ||
      value.contains('??');
}
