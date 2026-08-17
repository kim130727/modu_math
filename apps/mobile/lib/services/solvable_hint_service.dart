import '../models/content_models.dart';
import '../utils/problem_text_sanitizer.dart';

class HintChoice {
  const HintChoice({
    required this.label,
    this.isCorrect = false,
  });

  final String label;
  final bool isCorrect;
}

class SolvableHint {
  const SolvableHint({
    required this.level,
    required this.title,
    required this.body,
    this.miniQuestion = '',
    this.acceptedAnswers = const [],
    this.choices = const [],
    this.groupKey,
    this.groupLabel,
    this.successMessage = '좋아요. 다음 단계로 가 볼게요.',
  });

  final int level;
  final String title;
  final String body;
  final String miniQuestion;
  final List<String> acceptedAnswers;
  final List<HintChoice> choices;
  final String? groupKey;
  final String? groupLabel;
  final String successMessage;
}

List<SolvableHint> _withHintGroup(
  List<SolvableHint> hints, {
  String? groupKey,
  String? groupLabel,
}) {
  if (groupKey == null) {
    return hints;
  }
  return hints
      .map(
        (hint) => SolvableHint(
          level: hint.level,
          title: hint.title,
          body: hint.body,
          miniQuestion: hint.miniQuestion,
          acceptedAnswers: hint.acceptedAnswers,
          choices: hint.choices,
          groupKey: hint.groupKey ?? groupKey,
          groupLabel: hint.groupLabel ?? groupLabel,
          successMessage: hint.successMessage,
        ),
      )
      .toList();
}

class SolvableHintService {
  const SolvableHintService();

  List<SolvableHint> buildHints(ProblemContent content) {
    final comparisonHints = _comparisonSubproblemHints(content);
    if (comparisonHints.isNotEmpty) {
      return comparisonHints;
    }

    final columnHints = _columnAdditionHints(content);
    if (columnHints.isNotEmpty) {
      return columnHints;
    }

    final authoredHints = _authoredStudentHints(content);
    if (authoredHints.isNotEmpty) {
      return authoredHints;
    }

    return const [
      SolvableHint(
        level: 1,
        title: '1단계: 묻는 것 찾기',
        body: '문제에서 무엇을 구해야 하는지 먼저 확인해요.',
        miniQuestion: '무엇을 구하는 문제인가요?',
        choices: [
          HintChoice(label: '전체 수', isCorrect: true),
          HintChoice(label: '처음 수'),
          HintChoice(label: '남은 수'),
        ],
        acceptedAnswers: ['전체 수', '전체'],
        successMessage: '맞아요. 구해야 하는 값을 먼저 확인하면 계산이 쉬워져요.',
      ),
      SolvableHint(
        level: 2,
        title: '2단계: 계산 방법 고르기',
        body: '전체나 합계를 구하는 문제라면 더하기를 쓰는지 확인해요.',
        miniQuestion: '전체를 구할 때 알맞은 계산은 무엇인가요?',
        choices: [
          HintChoice(label: '더하기', isCorrect: true),
          HintChoice(label: '빼기'),
          HintChoice(label: '비교하기'),
        ],
        acceptedAnswers: ['더하기', '+'],
        successMessage: '좋아요. 이제 주어진 값을 차근차근 계산해요.',
      ),
      SolvableHint(
        level: 3,
        title: '3단계: 자리 맞춰 계산',
        body: '오른쪽 자리부터 계산해요. 한 자리씩 보면 실수가 줄어요.',
        miniQuestion: '계산은 어느 자리부터 시작하나요?',
        choices: [
          HintChoice(label: '일의 자리', isCorrect: true),
          HintChoice(label: '십의 자리'),
          HintChoice(label: '백의 자리'),
        ],
        acceptedAnswers: ['일의 자리', '일'],
        successMessage: '맞아요. 일의 자리부터 시작해요.',
      ),
      SolvableHint(
        level: 4,
        title: '4단계: 다시 확인',
        body: '각 자리의 답과 올림한 1을 빠뜨리지 않았는지 확인해요.',
        miniQuestion: '마지막에 꼭 확인할 것은 무엇인가요?',
        choices: [
          HintChoice(label: '올림한 수를 더했는지', isCorrect: true),
          HintChoice(label: '글자가 크게 보이는지'),
          HintChoice(label: '문제를 한 번만 봤는지'),
        ],
        acceptedAnswers: ['올림', '받아올림'],
        successMessage: '좋아요. 올림까지 확인하면 더 정확해져요.',
      ),
    ];
  }
}

List<SolvableHint> _comparisonSubproblemHints(ProblemContent content) {
  if (!_isComparisonProblem(content)) {
    return const [];
  }
  final quantities = _mapAt(content.solvable['inputs'], 'quantities');
  final entries = quantities.entries
      .where((entry) => entry.value is Map)
      .map((entry) => MapEntry(entry.key.toString(), entry.value as Map))
      .where(
        (entry) =>
            entry.value.containsKey('left_expression') &&
            entry.value.containsKey('right_expression'),
      )
      .toList()
    ..sort((a, b) => a.key.compareTo(b.key));
  if (entries.isEmpty) {
    return const [];
  }

  final hints = <SolvableHint>[];
  for (final entry in entries.indexed) {
    final number = entry.$1 + 1;
    final groupKey = entries.length > 1 ? '$number' : null;
    final groupLabel = entries.length > 1 ? '($number)' : null;
    final data = entry.$2.value;
    final leftExpression = data['left_expression']?.toString() ?? '';
    final rightExpression = data['right_expression']?.toString() ?? '';
    final leftValue = _readInt(data['left_value']);
    final rightValue = _readInt(data['right_value']);
    if (leftExpression.isEmpty ||
        rightExpression.isEmpty ||
        leftValue == null ||
        rightValue == null) {
      continue;
    }
    final operator = leftValue > rightValue
        ? '>'
        : leftValue < rightValue
            ? '<'
            : '=';
    hints.addAll(
      _comparisonHintsForSubproblem(
        number: number,
        leftExpression: leftExpression,
        leftValue: leftValue,
        rightExpression: rightExpression,
        rightValue: rightValue,
        operator: operator,
        groupKey: groupKey,
        groupLabel: groupLabel,
      ),
    );
  }
  return hints;
}

List<SolvableHint> _comparisonHintsForSubproblem({
  required int number,
  required String leftExpression,
  required int leftValue,
  required String rightExpression,
  required int rightValue,
  required String operator,
  String? groupKey,
  String? groupLabel,
}) {
  final hints = <SolvableHint>[];
  var level = 1;
  level = _appendExpressionPlaceValueHints(
    hints,
    problemNumber: number,
    sideLabel: '왼쪽',
    expression: leftExpression,
    expectedValue: leftValue,
    startLevel: level,
    groupKey: groupKey,
    groupLabel: groupLabel,
  );
  level = _appendExpressionPlaceValueHints(
    hints,
    problemNumber: number,
    sideLabel: '오른쪽',
    expression: rightExpression,
    expectedValue: rightValue,
    startLevel: level,
    groupKey: groupKey,
    groupLabel: groupLabel,
  );
  hints.add(
    SolvableHint(
      level: level,
      title: '$level단계: ($number) 비교 기호 고르기',
      body: '계산한 두 값을 비교해요. 왼쪽은 $leftValue, 오른쪽은 $rightValue입니다.',
      miniQuestion: '($number)번 빈칸에 들어갈 기호는 무엇인가요?',
      choices: _textChoices(operator, ['>', '=', '<']),
      acceptedAnswers: [operator],
      groupKey: groupKey,
      groupLabel: groupLabel,
      successMessage: '좋아요. ($number)번은 $leftValue $operator $rightValue입니다.',
    ),
  );
  return _withHintGroup(hints, groupKey: groupKey, groupLabel: groupLabel);
}

int _appendExpressionPlaceValueHints(
  List<SolvableHint> hints, {
  required int problemNumber,
  required String sideLabel,
  required String expression,
  required int expectedValue,
  required int startLevel,
  String? groupKey,
  String? groupLabel,
}) {
  final terms = _additionExpressionTerms(expression);
  if (terms == null) {
    hints.add(
      SolvableHint(
        level: startLevel,
        title: '$startLevel단계: ($problemNumber) $sideLabel 값 확인',
        body: '$sideLabel 식은 이미 수로 주어져 있어요. 값을 그대로 확인합니다.',
        miniQuestion: '($problemNumber)번 $sideLabel 값은 무엇인가요?',
        choices: _numberChoices(
            expectedValue, [expectedValue - 10, expectedValue + 10]),
        acceptedAnswers: ['$expectedValue'],
        successMessage: '맞아요. $sideLabel 값은 $expectedValue입니다.',
      ),
    );
    return startLevel + 1;
  }

  final left = terms[0];
  final right = terms[1];
  final onesLeft = left % 10;
  final onesRight = right % 10;
  final onesSum = onesLeft + onesRight;
  final onesDigit = onesSum % 10;
  final carryToTens = onesSum ~/ 10;
  final tensLeft = (left ~/ 10) % 10;
  final tensRight = (right ~/ 10) % 10;
  final tensSum = tensLeft + tensRight + carryToTens;
  final tensDigit = tensSum % 10;
  final carryToHundreds = tensSum ~/ 10;
  final hundredsLeft = (left ~/ 100) % 10;
  final hundredsRight = (right ~/ 100) % 10;

  hints.add(
    SolvableHint(
      level: startLevel,
      title: '$startLevel단계: ($problemNumber) $sideLabel 일의 자리 더하기',
      body: '$sideLabel 식 $expression을 일의 자리부터 계산해요.',
      miniQuestion: '$onesLeft + $onesRight은 얼마인가요?',
      choices: _numberChoices(onesSum, [onesDigit, onesSum + 1]),
      acceptedAnswers: ['$onesSum'],
      successMessage: '맞아요. 일의 자리 합은 $onesSum입니다.',
    ),
  );
  hints.add(
    SolvableHint(
      level: startLevel + 1,
      title: '${startLevel + 1}단계: ($problemNumber) $sideLabel 십의 자리 더하기',
      body: '일의 자리에서 올린 $carryToTens도 십의 자리 계산에 함께 넣어요.',
      miniQuestion: '십의 자리 계산으로 알맞은 것은 무엇인가요?',
      choices: _textChoices(
        '$tensLeft + $tensRight + $carryToTens',
        ['$tensLeft + $tensRight', '$onesLeft + $onesRight'],
      ),
      acceptedAnswers: [
        '$tensLeft+$tensRight+$carryToTens',
        '$tensLeft + $tensRight + $carryToTens',
      ],
      successMessage: '좋아요. 십의 자리에는 $tensDigit을 쓰고 $carryToHundreds을 올립니다.',
    ),
  );
  hints.add(
    SolvableHint(
      level: startLevel + 2,
      title: '${startLevel + 2}단계: ($problemNumber) $sideLabel 값 완성',
      body: '마지막으로 백의 자리까지 계산해 $sideLabel 값을 완성해요.',
      miniQuestion: '$sideLabel 식 $expression의 값은 무엇인가요?',
      choices: _numberChoices(
        expectedValue,
        [
          (hundredsLeft + hundredsRight) * 100 + tensDigit * 10 + onesDigit,
          expectedValue + 10,
        ],
      ),
      acceptedAnswers: ['$expectedValue'],
      successMessage: '맞아요. $sideLabel 값은 $expectedValue입니다.',
    ),
  );
  return startLevel + 3;
}

List<int>? _additionExpressionTerms(String expression) {
  final match = RegExp(r'^\s*(\d+)\s*\+\s*(\d+)\s*$').firstMatch(expression);
  if (match == null) {
    return null;
  }
  return [int.parse(match.group(1)!), int.parse(match.group(2)!)];
}

List<SolvableHint> _columnAdditionHints(ProblemContent content) {
  final termSets = _additionTermSets(content);
  if (termSets.isEmpty || !_isAdditionProblem(content)) {
    return const [];
  }
  final hints = <SolvableHint>[];
  for (final entry in termSets.indexed) {
    final titlePrefix = termSets.length > 1 ? '(${entry.$1 + 1}) ' : '';
    final groupKey = termSets.length > 1 ? '${entry.$1 + 1}' : null;
    final groupLabel = termSets.length > 1 ? '(${entry.$1 + 1})' : null;
    hints.addAll(
      _withHintGroup(
        _columnAdditionHintsForTerms(
          entry.$2[0].abs(),
          entry.$2[1].abs(),
          startLevel: 1,
          titlePrefix: titlePrefix,
        ),
        groupKey: groupKey,
        groupLabel: groupLabel,
      ),
    );
  }
  return hints;
}

List<SolvableHint> _columnAdditionHintsForTerms(
  int left,
  int right, {
  required int startLevel,
  String titlePrefix = '',
}) {
  final answer = left + right;
  final onesLeft = left % 10;
  final onesRight = right % 10;
  final onesSum = onesLeft + onesRight;
  final onesDigit = onesSum % 10;
  final carryToTens = onesSum ~/ 10;
  final tensLeft = (left ~/ 10) % 10;
  final tensRight = (right ~/ 10) % 10;
  final tensSum = tensLeft + tensRight + carryToTens;
  final tensDigit = tensSum % 10;
  final carryToHundreds = tensSum ~/ 10;
  final hundredsLeft = (left ~/ 100) % 10;
  final hundredsRight = (right ~/ 100) % 10;
  final hundredsSum = hundredsLeft + hundredsRight + carryToHundreds;

  return [
    SolvableHint(
      level: startLevel,
      title: '$startLevel단계: $titlePrefix일의 자리 더하기',
      body: '맨 오른쪽 일의 자리부터 더해요.',
      miniQuestion: '$onesLeft + $onesRight은 얼마인가요?',
      choices: _numberChoices(onesSum, [onesSum - 1, onesDigit, onesSum + 1]),
      acceptedAnswers: ['$onesSum'],
      successMessage: '맞아요. 일의 자리 합은 $onesSum이에요.',
    ),
    SolvableHint(
      level: startLevel + 1,
      title: '${startLevel + 1}단계: $titlePrefix일의 자리 쓰기',
      body: '$onesSum처럼 10을 넘으면 일의 자리 숫자만 아래에 쓰고, 1은 다음 자리로 올려요.',
      miniQuestion: '일의 자리에는 어떤 숫자를 쓰나요?',
      choices: _numberChoices(
        onesDigit,
        [onesSum, carryToTens, (onesDigit + 1) % 10],
      ),
      acceptedAnswers: ['$onesDigit'],
      successMessage: '좋아요. 일의 자리에는 $onesDigit을 쓰고, $carryToTens을 십의 자리로 올려요.',
    ),
    SolvableHint(
      level: startLevel + 2,
      title: '${startLevel + 2}단계: $titlePrefix십의 자리 더하기',
      body: '십의 자리 숫자들을 더할 때, 아까 올린 수도 함께 더해요.',
      miniQuestion: '십의 자리 계산으로 알맞은 것은 무엇인가요?',
      choices: _textChoices(
        '$tensLeft + $tensRight + $carryToTens',
        [
          '$tensLeft + $tensRight',
          '$onesLeft + $onesRight',
        ],
      ),
      acceptedAnswers: [
        '$tensLeft+$tensRight+$carryToTens',
        '$tensLeft + $tensRight + $carryToTens',
      ],
      successMessage:
          '맞아요. $tensLeft + $tensRight에 올린 $carryToTens을 더해서 $tensSum이 돼요.',
    ),
    SolvableHint(
      level: startLevel + 3,
      title: '${startLevel + 3}단계: $titlePrefix백의 자리와 답',
      body: '십의 자리에서 또 10을 넘으면 1을 백의 자리로 올려요. 마지막으로 각 자리 숫자를 이어 답을 만들어요.',
      miniQuestion: '백의 자리까지 계산하면 알맞은 답은 무엇인가요?',
      choices: _numberChoices(
        answer,
        [
          hundredsSum * 100 + tensDigit * 10 + onesSum,
          hundredsSum * 100 + (tensSum % 10) * 10 + carryToTens,
          answer + 10,
        ],
      ),
      acceptedAnswers: ['$answer'],
      successMessage: '좋아요. 일의 자리, 십의 자리, 백의 자리를 모두 확인했어요.',
    ),
  ];
}

List<HintChoice> _numberChoices(int correct, List<int> distractors) {
  final labels = <String>[];
  void add(int value) {
    if (value < 0) {
      return;
    }
    final label = value.toString();
    if (!labels.contains(label)) {
      labels.add(label);
    }
  }

  add(correct);
  for (final value in distractors) {
    add(value);
  }
  while (labels.length < 3) {
    add(correct + labels.length);
  }
  return labels
      .take(3)
      .map((label) => HintChoice(label: label, isCorrect: label == '$correct'))
      .toList();
}

List<HintChoice> _textChoices(String correct, List<String> distractors) {
  final labels = <String>[];
  void add(String value) {
    final label = value.trim();
    if (label.isNotEmpty && !labels.contains(label)) {
      labels.add(label);
    }
  }

  add(correct);
  for (final distractor in distractors) {
    add(distractor);
  }
  return labels
      .take(3)
      .map((label) => HintChoice(label: label, isCorrect: label == correct))
      .toList();
}

List<SolvableHint> _authoredStudentHints(ProblemContent content) {
  final rawHints = content.solvable['student_hints'];
  if (rawHints is! List) {
    return const [];
  }
  final hints = <SolvableHint>[];
  for (final item in rawHints) {
    if (item is! Map) {
      continue;
    }
    final level =
        item['level'] is int ? item['level'] as int : hints.length + 1;
    final body = _readText(item['text']);
    if (body.isEmpty) {
      continue;
    }
    hints.add(
      SolvableHint(
        level: level,
        title: _readText(item['title'], fallback: '$level단계'),
        body: _withoutAnswer(content, body),
      ),
    );
  }
  hints.sort((a, b) => a.level.compareTo(b.level));
  return hints;
}

bool _isAdditionProblem(ProblemContent content) {
  final pieces = <String>[
    content.summary.unit,
    content.summary.type,
    _readText(content.solvable['method']),
    _readText(content.solvable['problem_type']),
    _readText(content.solvable['plan']),
    _readText(content.solvable['steps']),
  ].join(' ').toLowerCase();
  return pieces.contains('addition') ||
      pieces.contains('add_parts') ||
      pieces.contains('vertical_addition') ||
      pieces.contains('+') ||
      pieces.contains('더하기') ||
      pieces.contains('덧셈');
}

bool _isComparisonProblem(ProblemContent content) {
  final pieces = <String>[
    content.summary.unit,
    content.summary.type,
    _readText(content.solvable['method']),
    _readText(content.solvable['problem_type']),
    _readText(_mapAt(content.solvable['inputs'], 'answer_type')),
  ].join(' ').toLowerCase();
  return pieces.contains('comparison') ||
      pieces.contains('compare') ||
      pieces.contains('비교') ||
      pieces.contains('comparison_operator');
}

List<List<int>> _additionTermSets(ProblemContent content) {
  final fromQuantities = _additionTermSetsFromQuantities(content.solvable);
  if (fromQuantities.isNotEmpty) {
    return fromQuantities;
  }

  final fromSteps = _additionTermSetsFromSteps(content.solvable);
  if (fromSteps.isNotEmpty) {
    return fromSteps;
  }

  final terms = _additionTerms(content);
  return terms.length >= 2 ? [terms.take(2).toList()] : const [];
}

List<List<int>> _additionTermSetsFromQuantities(Map<String, dynamic> solvable) {
  final quantities = _mapAt(_mapAt(solvable['inputs'], 'quantities'), null);
  if (quantities.isEmpty) {
    return const [];
  }
  final sets = <List<int>>[];
  final firstAddend = _readInt(quantities['first_addend']);
  final secondAddend = _readInt(quantities['second_addend']);
  if (firstAddend != null && secondAddend != null) {
    sets.add([firstAddend, secondAddend]);
    return sets;
  }

  final entries = quantities.entries.toList()
    ..sort((a, b) => a.key.toString().compareTo(b.key.toString()));
  for (final entry in entries) {
    final value = entry.value;
    if (value is Map) {
      final addends = value['addends'];
      if (addends is List) {
        final terms = addends
            .map((item) => _readInt(item))
            .whereType<int>()
            .take(2)
            .toList();
        if (terms.length >= 2) {
          sets.add(terms);
        }
      }
    }
  }
  return sets;
}

List<List<int>> _additionTermSetsFromSteps(Map<String, dynamic> solvable) {
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

List<int> _additionTerms(ProblemContent content) {
  final pieces = <String>[
    content.prompt,
    _readText(content.solvable['steps']),
    _readText(content.solvable['plan']),
    _readText(content.solvable['explanation']),
  ].join(' ');
  final match = RegExp(r'(\d+)\s*\+\s*(\d+)').firstMatch(pieces);
  if (match != null) {
    return [
      int.parse(match.group(1)!),
      int.parse(match.group(2)!),
    ];
  }

  final numbers = RegExp(r'\d+')
      .allMatches(pieces)
      .map((match) => int.tryParse(match.group(0) ?? ''))
      .whereType<int>()
      .where((number) => number >= 10)
      .toList();
  if (numbers.length >= 2) {
    return numbers.take(2).toList();
  }
  return const [];
}

String _withoutAnswer(ProblemContent content, String text) {
  final answer = content.correctAnswer.trim();
  if (answer.isEmpty) {
    return text;
  }
  return text.replaceAll(answer, '□');
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
      'label',
      'name',
      'value',
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

Map<String, dynamic> _mapAt(Object? value, Object? key) {
  final target = key == null
      ? value
      : value is Map
          ? value[key]
          : null;
  if (target is Map<String, dynamic>) {
    return target;
  }
  if (target is Map) {
    return target.map((key, value) => MapEntry(key.toString(), value));
  }
  return const {};
}

int? _readInt(Object? value) {
  if (value is int) {
    return value;
  }
  if (value is num) {
    return value.round();
  }
  return int.tryParse(value?.toString() ?? '');
}
