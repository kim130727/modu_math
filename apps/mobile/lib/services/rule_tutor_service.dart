import '../models/content_models.dart';
import '../models/learning_progress.dart';
import '../models/tutor_models.dart';
import '../utils/answer_normalizer.dart';
import '../utils/tutor_text_sanitizer.dart';
import 'answer_diagnostic_service.dart';
import 'ai_tutor_service.dart';
import 'diagnostic_confirmation_service.dart';
import 'diagnostic_strategies/diagnostic_strategy.dart';

class RuleTutorService extends AiTutorService {
  const RuleTutorService({
    this.diagnosticConfirmationService = const DiagnosticConfirmationService(),
  });

  final DiagnosticConfirmationService diagnosticConfirmationService;

  @override
  TutorMode get mode => TutorMode.rule;

  @override
  String get label => '온셈이';

  @override
  List<TutorMessage> startSession(ProblemContent content) {
    final steps = _tutorSteps(content);
    if (content.solvable.isEmpty) {
      return [
        _tutor(
          '이 문제는 아직 풀이 규칙이 준비되지 않았어요.\n다른 문제를 먼저 풀거나 잠시 뒤 다시 시도해 주세요.',
          TutorReplyType.retry,
        ),
      ];
    }
    if (steps.isEmpty) {
      return [
        _tutor(
          '풀이 데이터는 있지만 단계가 비어 있어요.\n문제 파일의 steps나 plan을 확인해 주세요.',
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
      _renderRuleStep(content, steps, next, prefix: '좋아요. 다음 단계로 가볼게요.'),
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
    final pendingDiagnosticCode =
        diagnosticConfirmationService.pendingCodeFrom(messages);
    if (pendingDiagnosticCode != null) {
      final result = diagnosticConfirmationService.resultFor(
        content: content,
        diagnosticCode: pendingDiagnosticCode,
        confirmationAnswer: cleanMessage,
      );
      if (result != null) {
        return _tutor(
          result.feedback,
          TutorReplyType.question,
          pendingDiagnosticCode: result.nextDiagnosticCode,
          errorCategory: result.errorCategory,
        );
      }
    }
    if (_asksForNext(cleanMessage)) {
      final next = (safeIndex + 1).clamp(0, steps.length - 1);
      return _ruleResponse(
        content,
        steps,
        next,
        _renderRuleStep(content, steps, next, prefix: '좋아요. 다음 단계로 가볼게요.'),
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
    final diagnosticPrompt = diagnosticConfirmationService.promptFor(
      content: content,
      answer: cleanMessage,
    );
    if (diagnosticPrompt != null) {
      return _tutor(
        diagnosticPrompt.text,
        TutorReplyType.question,
        choices: diagnosticPrompt.choices,
        pendingDiagnosticCode: diagnosticPrompt.diagnosticCode,
      );
    }
    final inferredDiagnosticPrompt = _inferredDiagnosticPrompt(
      content,
      step,
      cleanMessage,
    );
    if (inferredDiagnosticPrompt != null) {
      return _tutor(
        inferredDiagnosticPrompt.text,
        TutorReplyType.question,
        choices: inferredDiagnosticPrompt.choices,
        pendingDiagnosticCode: inferredDiagnosticPrompt.diagnosticCode,
      );
    }
    final diagnostic = _diagnosticFeedback(content, step, cleanMessage);
    if (diagnostic.isNotEmpty) {
      return _ruleResponse(content, steps, safeIndex, diagnostic);
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
        _renderRuleStep(content, steps, next, prefix: '좋아요. 잘 찾았어요.'),
      );
    }

    final hint = _stepExpectedHint(content, step, safeIndex);
    return _ruleResponse(
      content,
      steps,
      safeIndex,
      '조금만 다시 볼게요.\n'
      '${safeIndex + 1}단계: ${step.prompt}\n'
      '${hint.isEmpty ? '이 단계에서 필요한 값을 다시 입력해 볼까요?' : '$hint 다시 입력해 볼까요?'}',
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
        '좋아요. 정확히 맞았어요.\n'
        '다음 문제로 넘어가 볼까요?',
        TutorReplyType.correct,
      );
    }
    final diagnosticPrompt = diagnosticConfirmationService.promptFor(
      content: content,
      answer: answer,
    );
    if (diagnosticPrompt != null) {
      return _tutor(
        diagnosticPrompt.text,
        TutorReplyType.question,
        choices: diagnosticPrompt.choices,
        pendingDiagnosticCode: diagnosticPrompt.diagnosticCode,
      );
    }
    final steps = _tutorSteps(content);
    if (steps.isNotEmpty) {
      final inferredDiagnosticPrompt = _inferredDiagnosticPrompt(
        content,
        steps.first,
        answer,
      );
      if (inferredDiagnosticPrompt != null) {
        return _tutor(
          inferredDiagnosticPrompt.text,
          TutorReplyType.question,
          choices: inferredDiagnosticPrompt.choices,
          pendingDiagnosticCode: inferredDiagnosticPrompt.diagnosticCode,
        );
      }
    }
    if (_hasRegisteredDiagnostics(content)) {
      return _tutor(
        '어느 자리에서 달라졌는지 하나씩 확인해 볼게요.',
        TutorReplyType.question,
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
          ? '$multiple에서 표시된 $highlighted의 실제 값을 찾아볼게요.'
          : '자리값을 확인해서 같은 값을 만드는 식을 찾아볼게요.';
      return _renderRuleStep(content, steps, 0, prefix: lead);
    }

    return _renderRuleStep(
      content,
      steps,
      0,
      prefix: '온셈이와 함께 한 단계씩 풀어볼게요.',
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
        ..add('표시된 자리값을 보고 같은 값을 만드는 식을 고르면 돼요.')
        ..add('보기 중에서 값이 같은 식을 선택해 보세요.');
      return lines.take(4).join('\n');
    }

    if (index == 0) {
      lines
        ..add('1단계: 먼저 표시된 숫자의 자리값을 확인해요.')
        ..add('예를 들어 869에서 6은 십의 자리라서 60이에요.')
        ..add('표시된 부분은 어떤 값을 뜻할까요?');
    } else if (index == 1) {
      lines
        ..add('2단계: ${step.prompt}')
        ..add('이제 찾은 값에 곱할 수를 계산해요.')
        ..add('계산하면 얼마가 될까요?');
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
        return '좋아요. 천천히 다시 볼게요.\n'
            '숫자는 어느 자리에 있는지에 따라 값이 달라져요.\n'
            '표시된 숫자의 자리값을 먼저 찾아볼까요?';
      }
      if (index == 1) {
        return '앞에서 찾은 값을 사용하면 돼요.\n'
            '그 값에 곱할 수를 계산해 볼까요?';
      }
      return '이제 새 계산을 하는 단계는 아니에요.\n'
          '앞에서 찾은 값과 같은 보기를 골라보세요.';
    }

    final hint = _stepExpectedHint(content, step, index);
    return '좋아요. 이 단계만 다시 볼게요.\n'
        '${index + 1}단계: ${step.prompt}\n'
        '${hint.isEmpty ? '문제에서 확인해야 하는 값을 하나만 찾아보세요.' : hint}';
  }

  String _complete(ProblemContent content) {
    final answer = content.correctAnswer;
    if (answer.isNotEmpty) {
      return '정답은 $answer이에요.\n다음 문제로 넘어가 볼까요?';
    }
    return '좋아요. 풀이가 끝났어요.\n문제의 답을 입력해 볼까요?';
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
        final expr = raw['expr']?.toString().trim() ?? '';
        return _RuleStep(
          prompt:
              prompt.isEmpty ? '$index번째 풀이 단계를 확인해요.' : _cleanPrompt(prompt),
          expected: expected,
          explanation: _cleanPrompt(explanation),
          expr: expr,
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
            prompt: '표시된 부분이 실제로 어떤 식인지 보기에서 골라요.',
            expected: target.trim(),
            choices: _placeValueExpressionChoices(target.trim()),
          ),
        ];
      }
    }

    final additionSteps = _deriveColumnAdditionSteps(content);
    if (additionSteps.isNotEmpty) {
      return additionSteps;
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
              ? '${item.$1}은 이미 값으로 주어졌어요.'
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

  List<_RuleStep> _deriveColumnAdditionSteps(ProblemContent content) {
    final terms = _columnAdditionTermSets(content);
    if (terms.length != 1 ||
        terms.single.length < 2 ||
        !_isVerticalAdditionContent(content)) {
      return const [];
    }

    final left = terms.single[0].abs();
    final right = terms.single[1].abs();
    if (left < 10 || right < 10) {
      return const [];
    }

    final answer = left + right;
    final onesLeft = left % 10;
    final onesRight = right % 10;
    final onesSum = onesLeft + onesRight;
    final carryToTens = onesSum ~/ 10;
    final tensLeft = (left ~/ 10) % 10;
    final tensRight = (right ~/ 10) % 10;
    final tensSum = tensLeft + tensRight + carryToTens;
    final carryToHundreds = tensSum ~/ 10;
    final hundredsLeft = (left ~/ 100) % 10;
    final hundredsRight = (right ~/ 100) % 10;
    final hundredsSum = hundredsLeft + hundredsRight + carryToHundreds;

    return [
      _RuleStep(
        prompt: '일의 자리 $onesLeft + $onesRight를 계산해요.',
        expected: '$onesSum',
        expr: '$onesLeft + $onesRight',
      ),
      _RuleStep(
        prompt: '십의 자리 $tensLeft + $tensRight에 받아올림 $carryToTens을 더해요.',
        expected: '$tensSum',
        expr: '$tensLeft + $tensRight + $carryToTens',
      ),
      _RuleStep(
        prompt:
            '백의 자리 $hundredsLeft + $hundredsRight에 받아올림 $carryToHundreds을 더해요.',
        expected: '$hundredsSum',
        expr: '$hundredsLeft + $hundredsRight + $carryToHundreds',
      ),
      _RuleStep(
        prompt: '각 자리의 숫자를 모아 합을 만들어요.',
        expected: '$answer',
        expr: '$left + $right',
      ),
    ];
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
      return const [];
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
    String? pendingDiagnosticCode,
    ErrorCategory errorCategory = ErrorCategory.none,
  }) {
    return TutorMessage(
      role: TutorMessageRole.tutor,
      text: sanitizeTutorText(text),
      replyType: type,
      choices: choices,
      pendingDiagnosticCode: pendingDiagnosticCode,
      errorCategory: errorCategory,
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
    this.expr = '',
  });

  final String prompt;
  final String expected;
  final String explanation;
  final List<String> choices;
  final String expr;
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

bool _isVerticalAdditionContent(ProblemContent content) {
  final target = content.solvable['target'];
  final inputs = content.solvable['inputs'];
  final pieces = <String>[
    content.summary.type,
    _readRuleText(content.solvable['method']),
    _readRuleText(content.solvable['problem_type']),
    target is Map ? _readRuleText(target['type']) : '',
    inputs is Map ? _readRuleText(inputs['answer_type']) : '',
  ].join(' ').toLowerCase();
  return pieces.contains('vertical_addition') ||
      pieces.contains('multi_blank_vertical_addition') ||
      pieces.contains('digit_list');
}

List<List<int>> _columnAdditionTermSets(ProblemContent content) {
  final fromQuantities = _columnTermSetsFromQuantities(content.solvable);
  if (fromQuantities.isNotEmpty) {
    return fromQuantities;
  }

  final fromSteps = _columnTermSetsFromSteps(content.solvable);
  if (fromSteps.isNotEmpty) {
    return fromSteps;
  }
  return const [];
}

List<List<int>> _columnTermSetsFromQuantities(Map<String, dynamic> solvable) {
  final inputs = solvable['inputs'];
  final quantities = inputs is Map ? inputs['quantities'] : null;
  if (quantities is! Map) {
    return const [];
  }

  final firstAddend = _readRuleInt(quantities['first_addend']);
  final secondAddend = _readRuleInt(quantities['second_addend']);
  if (firstAddend != null && secondAddend != null) {
    return [
      [firstAddend, secondAddend],
    ];
  }

  final sets = <List<int>>[];
  final entries = quantities.entries.toList()
    ..sort((a, b) => a.key.toString().compareTo(b.key.toString()));
  for (final entry in entries) {
    final value = entry.value;
    if (value is! Map) {
      continue;
    }
    final addends = value['addends'];
    if (addends is! List) {
      continue;
    }
    final terms = addends
        .map((item) => _readRuleInt(item))
        .whereType<int>()
        .take(2)
        .toList();
    if (terms.length >= 2) {
      sets.add(terms);
    }
  }
  return sets;
}

List<List<int>> _columnTermSetsFromSteps(Map<String, dynamic> solvable) {
  final steps = solvable['steps'];
  if (steps is! List) {
    return const [];
  }
  final sets = <List<int>>[];
  for (final step in steps.whereType<Map>()) {
    final match = RegExp(r'(\d+)\s*\+\s*(\d+)')
        .firstMatch(step['expr']?.toString() ?? '');
    if (match == null) {
      continue;
    }
    sets.add([int.parse(match.group(1)!), int.parse(match.group(2)!)]);
  }
  return sets;
}

String _readRuleText(Object? value) {
  if (value == null) {
    return '';
  }
  if (value is String || value is num || value is bool) {
    return value.toString();
  }
  if (value is List) {
    return value.map(_readRuleText).where((text) => text.isNotEmpty).join(' ');
  }
  if (value is Map) {
    return value.values
        .map(_readRuleText)
        .where((text) => text.isNotEmpty)
        .join(' ');
  }
  return '';
}

int? _readRuleInt(Object? value) {
  if (value is int) {
    return value;
  }
  if (value is num) {
    return value.round();
  }
  return int.tryParse(value?.toString() ?? '');
}

Object? _givenValue(ProblemContent content, String ref) {
  final given = content.solvable['given'];
  if (given is! List) {
    return null;
  }
  for (final item in given.whereType<Map<String, dynamic>>()) {
    if (item['ref'] == ref || item['id'] == ref) {
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
  if (step.prompt.contains('그대로') || step.prompt.contains('주어졌')) {
    return '그 수를 그대로 입력해 보세요.';
  }
  if (_isPlaceValueMatching(content)) {
    if (index == 0) {
      return '표시된 숫자가 어떤 자리의 값인지 먼저 확인해요.';
    }
    if (index == 1) {
      return '찾은 값에 무엇을 곱해야 하는지 계산해 보세요.';
    }
    return '보기 중에서 앞에서 찾은 값과 같은 식을 찾아보세요.';
  }
  if (_looksNumber(expected)) {
    return '계산한 값을 입력해 보세요.';
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

String _diagnosticFeedback(
  ProblemContent content,
  _RuleStep step,
  String message,
) {
  final registered = _registeredDiagnosticFeedback(content, message);
  if (registered.isNotEmpty) {
    return registered;
  }
  return _inferredArithmeticFeedback(step, message);
}

String _registeredDiagnosticFeedback(ProblemContent content, String message) {
  return const AnswerDiagnosticService().feedbackFor(
    content: content,
    answer: message,
  );
}

bool _hasRegisteredDiagnostics(ProblemContent content) {
  final diagnostics = content.solvable['diagnostics'];
  if (diagnostics is! Map<String, dynamic>) {
    return false;
  }
  final errors = diagnostics['errors'];
  return errors is Map && errors.isNotEmpty;
}

DiagnosticPrompt? _inferredDiagnosticPrompt(
  ProblemContent content,
  _RuleStep step,
  String message,
) {
  if (!RegExp(r'^-?\d+$').hasMatch(message.trim())) {
    return null;
  }
  if (_answerMatchesStep(message, step)) {
    return null;
  }
  final expected = int.tryParse(step.expected.trim());
  final terms = _additionTerms(step.expr);
  if (expected == null ||
      terms.length < 2 ||
      terms.fold<int>(0, (sum, item) => sum + item) != expected ||
      !_hasColumnCarry(terms)) {
    return null;
  }
  return const DiagnosticConfirmationService().promptForCode(
    content: content,
    diagnosticCode: 'execute.add_carry',
    answer: message,
  );
}

String _inferredArithmeticFeedback(_RuleStep step, String message) {
  final response = message.trim();
  if (!RegExp(r'^-?\d+$').hasMatch(response)) {
    return '';
  }
  final expected = int.tryParse(step.expected.trim());
  if (expected == null) {
    return '';
  }
  final terms = _additionTerms(step.expr);
  if (terms.length < 2 ||
      terms.fold<int>(0, (sum, item) => sum + item) != expected) {
    return '';
  }
  final normalized = response.replaceFirst(RegExp(r'^0+'), '');
  final cleanResponse = normalized.isEmpty ? '0' : normalized;
  if (cleanResponse == expected.toString()) {
    return '';
  }
  if (_hasColumnCarry(terms) &&
      cleanResponse.length > expected.abs().toString().length) {
    return '받아올림한 수나 중간 계산을 그대로 이어 쓰면 안 돼요. 일의 자리부터 계산해 각 자리 숫자로 다시 모아 보세요.';
  }
  if (_hasColumnCarry(terms)) {
    return '받아올림을 다시 확인해요. 일의 자리부터 더하고, 10이 넘으면 다음 자리로 1을 올려요.';
  }
  return '';
}

List<int> _additionTerms(String expression) {
  if (!RegExp(r'^\s*\d+\s*(?:\+\s*\d+\s*)+$').hasMatch(expression)) {
    return const [];
  }
  return RegExp(r'\d+')
      .allMatches(expression)
      .map((match) => int.parse(match.group(0)!))
      .toList();
}

bool _hasColumnCarry(List<int> terms) {
  if (terms.isEmpty) {
    return false;
  }
  var carry = 0;
  final maxDigits = terms
      .map((term) => term.abs().toString().length)
      .fold<int>(0, (max, length) => length > max ? length : max);
  for (var place = 0; place < maxDigits; place += 1) {
    final divisor = _intPow10(place);
    final columnSum = carry +
        terms.fold<int>(0, (sum, term) => sum + (term.abs() ~/ divisor) % 10);
    if (columnSum >= 10) {
      return true;
    }
    carry = columnSum ~/ 10;
  }
  return carry > 0;
}

int _intPow10(int exponent) {
  var value = 1;
  for (var index = 0; index < exponent; index += 1) {
    value *= 10;
  }
  return value;
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
  return ['몰라', '이해', '무슨말', '헷갈', '어려', '힌트', '설명', 'help', 'confus']
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
      .replaceAll('횞', '*')
      .replaceAll('×', '*')
      .replaceAll('x', '*')
      .replaceAll('X', '*')
      .replaceAll('첨', '/')
      .replaceAll('÷', '/')
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
