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
    final expandedAdditionHints = _expandedAdditionHints(content);
    if (expandedAdditionHints.isNotEmpty) {
      return expandedAdditionHints;
    }

    final wordProblemHints = _wordProblemHints(content);
    if (wordProblemHints.isNotEmpty) {
      return wordProblemHints;
    }

    final comparisonHints = _comparisonHints(content);
    if (comparisonHints.isNotEmpty) {
      return comparisonHints;
    }

    final authoredHints = _authoredStudentHints(content);
    if (authoredHints.isNotEmpty) {
      return authoredHints;
    }

    final multiplicationPlaceValueHints =
        _multiplicationPlaceValueHints(content);
    if (multiplicationPlaceValueHints.isNotEmpty) {
      return multiplicationPlaceValueHints;
    }

    if (!_isWordProblem(content) && !_isComparisonProblem(content)) {
      final columnHints = _columnAdditionHints(content);
      if (columnHints.isNotEmpty) {
        return columnHints;
      }
    }

    final diagnosticHints = _diagnosticQuestionHints(content);
    if (diagnosticHints.isNotEmpty) {
      return diagnosticHints;
    }

    final planHints = _planBasedHints(content);
    if (planHints.isNotEmpty) {
      return planHints;
    }

    if (_isAdditionProblem(content)) {
      return _additionFallbackHints;
    }

    return _generalFallbackHints(content);
  }
}

const List<SolvableHint> _additionFallbackHints = [
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

List<SolvableHint> _generalFallbackHints(ProblemContent content) {
  return const [
    SolvableHint(
      level: 1,
      title: '1단계: 문제 파악하기',
      body: '문제에서 구하고자 하는 것이 무엇인지 꼼꼼히 읽어보세요.',
    ),
    SolvableHint(
      level: 2,
      title: '2단계: 핵심 조건 찾기',
      body: '주어진 그림이나 수식에서 필요한 단서를 찾아보세요.',
    ),
    SolvableHint(
      level: 3,
      title: '3단계: 차근차근 풀이하기',
      body: '단계를 나누어 계산하거나 규칙을 적용해 보세요.',
    ),
    SolvableHint(
      level: 4,
      title: '4단계: 정답 검토하기',
      body: '구한 답이 문제 조건과 맞는지 다시 한 번 확인해 보세요.',
    ),
  ];
}

List<SolvableHint> _diagnosticQuestionHints(ProblemContent content) {
  final understanding = _mapAt(content.solvable, 'understanding');
  final rawList = understanding['diagnostic_questions'] ??
      content.solvable['diagnostic_questions'];
  if (rawList is! List || rawList.isEmpty) {
    return const [];
  }
  final hints = <SolvableHint>[];
  for (var i = 0; i < rawList.length; i++) {
    final item = rawList[i];
    if (item is! Map) {
      continue;
    }
    final prompt = _readText(item['prompt']);
    if (prompt.isEmpty) {
      continue;
    }
    final choicesList = item['choices'];
    final rawChoices = choicesList is List
        ? choicesList.map((c) => c.toString().trim()).toList()
        : <String>[];
    if (rawChoices.isEmpty) {
      continue;
    }

    final answerIndex =
        item['answer_index'] is int ? item['answer_index'] as int : 0;
    final answerText = (answerIndex >= 0 && answerIndex < rawChoices.length)
        ? rawChoices[answerIndex]
        : _readText(item['answer'], fallback: rawChoices.first);

    final choices = rawChoices
        .map((choice) => HintChoice(
              label: choice,
              isCorrect: choice == answerText,
            ))
        .toList();

    final level = i + 1;
    hints.add(
      SolvableHint(
        level: level,
        title: '$level단계: 개념 확인 $level',
        body: prompt,
        miniQuestion: prompt,
        choices: choices,
        acceptedAnswers: [answerText],
        successMessage: '맞아요! $answerText입니다.',
      ),
    );
  }
  return hints;
}

List<SolvableHint> _expandedAdditionHints(ProblemContent content) {
  final problemType =
      _readText(content.solvable['problem_type']).toLowerCase();
  final relation =
      _mapAt(_mapAt(content.solvable, 'understanding'), 'relation');
  final relationType = relation['type']?.toString().toLowerCase() ?? '';
  final isExpanded = problemType.contains('expanded') ||
      problemType.contains('부분합') ||
      relationType.contains('expanded');

  if (!isExpanded) {
    return const [];
  }

  final steps = content.solvable['steps'];
  if (steps is! List || steps.isEmpty) {
    return const [];
  }

  final hints = <SolvableHint>[];
  for (var i = 0; i < steps.length; i++) {
    final step = steps[i];
    if (step is! Map) {
      continue;
    }
    final stepId = step['id']?.toString() ?? '';
    if (stepId.contains('collect')) {
      continue;
    }

    final expr = _readText(step['expr']);
    final value = step['value'];
    final explanation = _readText(step['explanation']);
    final level = hints.length + 1;

    String title = '$level단계: 부분합 계산 ($expr)';
    String body = explanation.isNotEmpty ? explanation : '$expr을 계산해요.';
    String miniQ = '$expr의 값은 얼마인가요?';

    if (stepId.contains('ones') || expr.contains('일의 자리')) {
      title = '$level단계: 일의 자리 부분합 ($expr)';
      body = '일의 자리 숫자끼리 먼저 더해요. $explanation';
      miniQ = '첫 번째 칸에 들어갈 $expr의 값은 얼마인가요?';
    } else if (stepId.contains('tens') || expr.contains('십의 자리')) {
      title = '$level단계: 십의 자리 부분합 ($expr)';
      body = '십의 자리 숫자가 나타내는 실제 값을 더해요. $explanation';
      miniQ = '두 번째 칸에 들어갈 $expr의 값은 얼마인가요?';
    } else if (stepId.contains('hundreds') || expr.contains('백의 자리')) {
      title = '$level단계: 백의 자리 부분합 ($expr)';
      body = '백의 자리 숫자가 나타내는 실제 값을 더해요. $explanation';
      miniQ = '세 번째 칸에 들어갈 $expr의 값은 얼마인가요?';
    } else if (stepId.contains('total') || expr.contains('전체')) {
      title = '$level단계: 전체 합 완성하기 ($expr)';
      body = '구한 각 자리의 부분합을 모두 더해 전체 합을 완성해요. $explanation';
      miniQ = '마지막 칸에 들어갈 전체 합($expr)의 값은 얼마인가요?';
    }

    final int? numVal = _readInt(value);
    if (numVal == null) {
      continue;
    }

    final distractors = <int>[
      numVal > 10 ? (numVal ~/ 10) : numVal + 1,
      numVal >= 10 ? numVal * 10 : (numVal > 1 ? numVal - 1 : numVal + 2),
    ];

    hints.add(
      SolvableHint(
        level: level,
        title: title,
        body: body,
        miniQuestion: miniQ,
        choices: _numberChoices(numVal, distractors),
        acceptedAnswers: ['$numVal'],
        successMessage: '맞아요! $expr = $numVal입니다.',
      ),
    );
  }

  return hints;
}

List<SolvableHint> _wordProblemHints(ProblemContent content) {
  if (!_isWordProblem(content)) {
    return const [];
  }

  final hints = <SolvableHint>[];

  final diagnosticHints = _diagnosticQuestionHints(content);
  for (final hint in diagnosticHints) {
    hints.add(
      SolvableHint(
        level: hints.length + 1,
        title: '${hints.length + 1}단계: ${hint.title.replaceFirst(RegExp(r'^\d+단계:\s*'), '')}',
        body: hint.body,
        miniQuestion: hint.miniQuestion,
        choices: hint.choices,
        acceptedAnswers: hint.acceptedAnswers,
        successMessage: hint.successMessage,
      ),
    );
  }

  final steps = content.solvable['steps'];
  if (steps is List && steps.isNotEmpty) {
    for (final step in steps) {
      if (step is! Map) continue;
      final stepId = step['id']?.toString() ?? '';
      if (stepId.contains('collect')) continue;

      final expr = _readText(step['expr']);
      final goal = _readText(step['goal']);
      final explanation = _readText(step['explanation']);
      final int? numVal = _extractStepValue(step['value']);

      if (expr.isEmpty || numVal == null) continue;

      final level = hints.length + 1;
      final title = goal.isNotEmpty
          ? '$level단계: $goal ($expr)'
          : '$level단계: $expr 계산하기';
      final body = explanation.isNotEmpty ? explanation : '$expr을 계산해요.';
      final miniQ = '$expr의 값은 얼마인가요?';

      final distractors = <int>[
        numVal > 10 ? (numVal - 10) : numVal + 1,
        numVal >= 10 ? (numVal + 10) : (numVal > 1 ? numVal - 1 : numVal + 2),
      ];

      hints.add(
        SolvableHint(
          level: level,
          title: title,
          body: body,
          miniQuestion: miniQ,
          choices: _numberChoices(numVal, distractors),
          acceptedAnswers: ['$numVal', '$numVal${content.summary.unit}'],
          successMessage: '맞아요! $expr = $numVal입니다.',
        ),
      );
    }
  }

  return hints;
}

bool _isWordProblem(ProblemContent content) {
  final problemType =
      _readText(content.solvable['problem_type']).toLowerCase();
  final subUnit = content.summary.subUnit.toLowerCase();
  final title = content.summary.title.toLowerCase();
  final prompt = content.prompt;

  return problemType.contains('word_problem') ||
      problemType.contains('문장제') ||
      subUnit.contains('문장제') ||
      subUnit.contains('실생활') ||
      title.contains('구슬') ||
      title.contains('연필') ||
      title.contains('학생') ||
      prompt.length > 40;
}

int? _extractStepValue(Object? value) {
  if (value is num) return value.toInt();
  if (value is Map) {
    return _readInt(value['count']) ?? _readInt(value['value']);
  }
  return _readInt(value);
}

List<SolvableHint> _multiplicationPlaceValueHints(ProblemContent content) {
  if (!_isMultiplicationPlaceValueProblem(content)) {
    return const [];
  }

  final targetExpr = _findMultiplicationTargetExpression(content);
  if (targetExpr == null) {
    return const [];
  }

  final match = RegExp(r'(\d+)\s*[×x*]\s*(\d+)').firstMatch(targetExpr);
  if (match == null) {
    return const [];
  }

  final termA = int.parse(match.group(1)!);
  final termB = int.parse(match.group(2)!);

  final int placeValue;
  final int multiplier;
  if (termA >= 10 || termB < 10) {
    placeValue = termA;
    multiplier = termB;
  } else {
    placeValue = termB;
    multiplier = termA;
  }

  final firstDigit = int.parse(placeValue.toString()[0]);
  final String placeName;
  if (placeValue < 10) {
    placeName = '일의 자리';
  } else if (placeValue < 100) {
    placeName = '십의 자리';
  } else if (placeValue < 1000) {
    placeName = '백의 자리';
  } else {
    placeName = '천의 자리';
  }

  final multiplicand = _findMultiplicand(content);
  final product = placeValue * multiplier;
  final multiplicandPrefix =
      multiplicand != null ? '$multiplicand에서 ' : '';

  final step1Distractors = <int>[firstDigit];
  if (placeValue >= 100) {
    step1Distractors.add(placeValue ~/ 10);
  } else if (placeValue >= 10) {
    step1Distractors.add(placeValue * 10);
  } else {
    step1Distractors.add(firstDigit * 10);
  }

  final step2Distractors = <int>[
    multiplier == 4 ? 2 : (multiplier > 2 ? multiplier - 2 : multiplier + 2),
    multiplier == 4 ? 8 : (multiplier + 4) % 9 + 1,
  ];

  final step3DistractorList = <String>[
    '$firstDigit × $multiplier',
    placeValue >= 100
        ? '${placeValue ~/ 10} × $multiplier'
        : '${placeValue * 10} × $multiplier',
  ];

  return [
    SolvableHint(
      level: 1,
      title: '1단계: 색칠된 자리의 실제 값 찾기',
      body: '$multiplicandPrefix색칠된 자리의 숫자 $firstDigit은 실제 얼마를 나타내는지 확인해요.',
      miniQuestion: '$multiplicandPrefix숫자 $firstDigit은 실제 얼마를 나타내나요?',
      choices: _numberChoices(placeValue, step1Distractors),
      acceptedAnswers: ['$placeValue'],
      successMessage: '맞아요. $firstDigit은 $placeName 숫자이므로 실제로는 $placeValue입니다.',
    ),
    SolvableHint(
      level: 2,
      title: '2단계: 곱하는 수 확인',
      body: '색칠된 부분에 곱해지는 한 자리 수를 확인해요.',
      miniQuestion: '곱하는 수는 얼마인가요?',
      choices: _numberChoices(multiplier, step2Distractors),
      acceptedAnswers: ['$multiplier'],
      successMessage: '좋아요. 곱하는 수는 $multiplier입니다.',
    ),
    SolvableHint(
      level: 3,
      title: '3단계: 알맞은 곱셈식 완성',
      body: '색칠된 부분($product)은 $placeValue과 $multiplier의 곱이에요.',
      miniQuestion: '색칠된 부분을 나타내는 알맞은 곱셈식은 무엇인가요?',
      choices: _textChoices('$placeValue × $multiplier', step3DistractorList),
      acceptedAnswers: [
        '$placeValue × $multiplier',
        '$placeValue×$multiplier',
        '$placeValue * $multiplier',
      ],
      successMessage: '정답이에요! 색칠된 부분은 $placeValue × $multiplier를 나타냅니다.',
    ),
  ];
}

bool _isMultiplicationPlaceValueProblem(ProblemContent content) {
  final pieces = <String>[
    content.summary.unit,
    content.summary.type,
    _readText(content.solvable['problem_type']),
    _readText(content.solvable['method']),
    content.prompt,
    _readText(content.solvable['target']),
    _readText(content.solvable['plan']),
  ].join(' ').toLowerCase();

  return (pieces.contains('multiplication') ||
          pieces.contains('곱셈') ||
          pieces.contains('세로셈')) &&
      (pieces.contains('place_value') ||
          pieces.contains('자리값') ||
          pieces.contains('부분곱') ||
          pieces.contains('색칠') ||
          pieces.contains('어떤 수의 곱'));
}

String? _findMultiplicationTargetExpression(ProblemContent content) {
  final candidates = <String>[
    content.correctAnswer,
    _readText(content.solvable['target']),
    _readText(_mapAt(content.solvable, 'answer')['value']),
    _readText(content.solvable['given']),
    _readText(content.solvable['steps']),
  ];

  for (final item in candidates) {
    final match = RegExp(r'(\d+)\s*[×x*]\s*(\d+)').firstMatch(item);
    if (match != null) {
      return '${match.group(1)} × ${match.group(2)}';
    }
  }
  return null;
}

int? _findMultiplicand(ProblemContent content) {
  final pieces = <String>[
    _readText(content.solvable['given']),
    _readText(content.solvable['steps']),
    _readText(content.solvable['plan']),
    content.prompt,
  ].join(' ');

  final match = RegExp(r'(\d{2,4})\s*[×x*]').firstMatch(pieces);
  if (match != null) {
    return int.tryParse(match.group(1)!);
  }
  final digitMatch = RegExp(r'(\d{3,4})의\s*\d').firstMatch(pieces);
  if (digitMatch != null) {
    return int.tryParse(digitMatch.group(1)!);
  }
  return null;
}

List<SolvableHint> _planBasedHints(ProblemContent content) {
  final rawPlan = content.solvable['plan'];
  if (rawPlan is! List || rawPlan.isEmpty) {
    return const [];
  }
  final planItems = rawPlan
      .map((p) => _readText(p))
      .where((p) => p.isNotEmpty)
      .toList();
  if (planItems.isEmpty) {
    return const [];
  }
  final hints = <SolvableHint>[];
  for (var i = 0; i < planItems.length; i++) {
    final level = i + 1;
    final text = planItems[i];
    hints.add(
      SolvableHint(
        level: level,
        title: '$level단계: 풀이 안내 $level',
        body: text,
      ),
    );
  }
  return hints;
}

List<SolvableHint> _comparisonHints(ProblemContent content) {
  if (!_isComparisonProblem(content)) {
    return const [];
  }

  final subproblemHints = _comparisonSubproblemHints(content);
  if (subproblemHints.isNotEmpty) {
    return subproblemHints;
  }

  final diagnosticHints = _diagnosticQuestionHints(content);
  if (diagnosticHints.isNotEmpty) {
    return diagnosticHints;
  }

  final steps = content.solvable['steps'];
  if (steps is List && steps.isNotEmpty) {
    final hints = <SolvableHint>[];
    for (final step in steps) {
      if (step is! Map) continue;
      final expr = _readText(step['expr']);
      final explanation = _readText(step['explanation']);
      final value = step['value'];
      final level = hints.length + 1;

      if (expr.isEmpty || value == null) continue;

      final valStr = value.toString().trim();
      final isOperator = valStr == '>' || valStr == '<' || valStr == '=';

      if (isOperator) {
        hints.add(
          SolvableHint(
            level: level,
            title: '$level단계: 알맞은 부등호 기호 선택 ($expr)',
            body: explanation.isNotEmpty
                ? explanation
                : '$expr에 알맞은 기호를 골라요.',
            miniQuestion: '○ 안에 들어갈 알맞은 기호는 무엇인가요?',
            choices: _textChoices(
              valStr,
              ['>', '=', '<'].where((s) => s != valStr).toList(),
            ),
            acceptedAnswers: [valStr],
            successMessage: '정답이에요! $valStr를 선택합니다.',
          ),
        );
      } else {
        final int? numVal = _readInt(value);
        if (numVal != null) {
          final distractors = <int>[numVal - 10, numVal + 10];
          hints.add(
            SolvableHint(
              level: level,
              title: '$level단계: 식 계산하기 ($expr)',
              body: explanation.isNotEmpty
                  ? explanation
                  : '$expr을 계산해요.',
              miniQuestion: '$expr의 값은 얼마인가요?',
              choices: _numberChoices(numVal, distractors),
              acceptedAnswers: ['$numVal'],
              successMessage: '맞아요! $expr = $numVal입니다.',
            ),
          );
        }
      }
    }
    if (hints.isNotEmpty) {
      return hints;
    }
  }

  return const [];
}

List<SolvableHint> _comparisonSubproblemHints(ProblemContent content) {
  if (!_isComparisonProblem(content)) {
    return const [];
  }
  final quantities = _mapAt(content.solvable['inputs'], 'quantities');
  final allEntries = quantities.entries
      .where((entry) => entry.value is Map)
      .map((entry) => MapEntry(entry.key.toString(), entry.value as Map))
      .where(
        (entry) =>
            entry.value.containsKey('left_expression') &&
            entry.value.containsKey('right_expression'),
      )
      .toList()
    ..sort((a, b) => a.key.compareTo(b.key));
  final entries = _selectComparisonEntriesForContent(content, allEntries);
  if (entries.isEmpty) {
    return const [];
  }

  final hints = <SolvableHint>[];
  for (final entry in entries.indexed) {
    final number = _comparisonEntryNumber(entry.$2.key) ?? entry.$1 + 1;
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
  final leftNeedsCalculation = _additionExpressionTerms(leftExpression) != null;
  final rightNeedsCalculation =
      _additionExpressionTerms(rightExpression) != null;
  if (leftNeedsCalculation) {
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
  }
  if (rightNeedsCalculation) {
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
  }
  if (!leftNeedsCalculation && !rightNeedsCalculation) {
    level = _appendDirectComparisonValuesHint(
      hints,
      problemNumber: number,
      leftValue: leftValue,
      rightValue: rightValue,
      startLevel: level,
      groupKey: groupKey,
      groupLabel: groupLabel,
    );
  }
  final titleProblemLabel = groupLabel == null ? '' : ' $groupLabel';
  final questionProblemLabel = groupLabel == null ? '' : '$number번 ';
  hints.add(
    SolvableHint(
      level: level,
      title: '$level단계:$titleProblemLabel 비교 기호 고르기',
      body: '계산한 두 값을 비교해요. 왼쪽은 $leftValue, 오른쪽은 $rightValue입니다.',
      miniQuestion: '${questionProblemLabel}빈칸에 들어갈 기호는 무엇인가요?',
      choices: _textChoices(operator, ['>', '=', '<']),
      acceptedAnswers: [operator],
      groupKey: groupKey,
      groupLabel: groupLabel,
      successMessage: '좋아요. $leftValue $operator $rightValue입니다.',
    ),
  );
  return _withHintGroup(hints, groupKey: groupKey, groupLabel: groupLabel);
}

List<MapEntry<String, Map<dynamic, dynamic>>>
    _selectComparisonEntriesForContent(
  ProblemContent content,
  List<MapEntry<String, Map<dynamic, dynamic>>> entries,
) {
  final suffixNumber = _subproblemNumberFromProblemId(content.summary.id);
  if (suffixNumber != null) {
    final suffixKey = 'problem_$suffixNumber';
    final selected = entries.where((entry) => entry.key == suffixKey).toList();
    if (selected.isNotEmpty) {
      return selected;
    }
  }
  final answerCount = _answerKeyCount(content);
  if (answerCount > 0 && answerCount < entries.length) {
    return entries.take(answerCount).toList();
  }
  return entries;
}

int? _subproblemNumberFromProblemId(String problemId) {
  final match = RegExp(r'_(\d+)$').firstMatch(problemId);
  if (match == null) {
    return null;
  }
  return int.tryParse(match.group(1)!);
}

int? _comparisonEntryNumber(String key) {
  final match = RegExp(r'^problem_(\d+)$').firstMatch(key);
  if (match == null) {
    return null;
  }
  return int.tryParse(match.group(1)!);
}

int _answerKeyCount(ProblemContent content) {
  final answer = _mapAt(content.solvable, 'answer').isNotEmpty
      ? _mapAt(content.solvable, 'answer')
      : _mapAt(content.semantic, 'answer');
  final key = answer['answer_key'];
  if (key is List && key.isNotEmpty) {
    return key.length;
  }
  final values = answer['values'];
  if (values is List && values.isNotEmpty) {
    return values.length;
  }
  final blanks = answer['blanks'];
  if (blanks is List && blanks.isNotEmpty) {
    return blanks.length;
  }
  return 0;
}

int _appendDirectComparisonValuesHint(
  List<SolvableHint> hints, {
  required int problemNumber,
  required int leftValue,
  required int rightValue,
  required int startLevel,
  String? groupKey,
  String? groupLabel,
}) {
  final titleProblemLabel = groupLabel == null ? '' : ' $groupLabel';
  final questionProblemLabel = groupLabel == null ? '' : '$problemNumber번 ';
  hints.add(
    SolvableHint(
      level: startLevel,
      title: '$startLevel단계:$titleProblemLabel 두 값 확인',
      body: '양쪽이 모두 수로 주어졌어요. 왼쪽 값과 오른쪽 값을 그대로 확인합니다.',
      miniQuestion: '${questionProblemLabel}왼쪽 값은 무엇인가요?',
      choices: _numberChoices(leftValue, [leftValue - 10, leftValue + 10]),
      acceptedAnswers: ['$leftValue'],
      groupKey: groupKey,
      groupLabel: groupLabel,
      successMessage: '맞아요. 왼쪽 값은 $leftValue입니다.',
    ),
  );
  return startLevel + 1;
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
    return startLevel;
  }
  final titleProblemLabel = groupLabel == null ? '' : ' $groupLabel';
  final questionProblemLabel = groupLabel == null ? '' : '$problemNumber번 ';

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
      title: '$startLevel단계:$titleProblemLabel $sideLabel 일의 자리 더하기',
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
      title: '${startLevel + 1}단계:$titleProblemLabel $sideLabel 십의 자리 더하기',
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
      title: '${startLevel + 2}단계:$titleProblemLabel $sideLabel 값 완성',
      body: '마지막으로 백의 자리까지 계산해 $sideLabel 값을 완성해요.',
      miniQuestion: '$questionProblemLabel$sideLabel 식 $expression의 값은 무엇인가요?',
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
  final inputs = _mapAt(content.solvable, 'inputs');
  final relation =
      _mapAt(_mapAt(content.solvable, 'understanding'), 'relation');
  final relationType = relation['type']?.toString().toLowerCase() ?? '';
  final pieces = <String>[
    content.summary.unit,
    content.summary.type,
    content.summary.title,
    content.summary.subUnit,
    content.prompt,
    _readText(content.solvable['method']),
    _readText(content.solvable['problem_type']),
    _readText(inputs['answer_type']),
    relationType,
  ].join(' ').toLowerCase();

  final hasSymbols = inputs['allowed_symbols'] is List ||
      inputs.containsKey('left_expression') ||
      inputs.containsKey('right_value');

  return pieces.contains('comparison') ||
      pieces.contains('compare') ||
      pieces.contains('비교') ||
      pieces.contains('크기') ||
      pieces.contains('부등호') ||
      pieces.contains('comparison_operator') ||
      hasSymbols;
}

List<List<int>> _additionTermSets(ProblemContent content) {
  final fromQuantities = _additionTermSetsFromQuantities(content);
  if (fromQuantities.isNotEmpty) {
    return fromQuantities;
  }

  final fromSteps = _additionTermSetsFromSteps(content);
  if (fromSteps.isNotEmpty) {
    return fromSteps;
  }

  final terms = _additionTerms(content);
  return terms.length >= 2 ? [terms.take(2).toList()] : const [];
}

List<List<int>> _additionTermSetsFromQuantities(ProblemContent content) {
  final quantities =
      _mapAt(_mapAt(content.solvable['inputs'], 'quantities'), null);
  if (quantities.isEmpty) {
    return const [];
  }
  final firstAddend = _readInt(quantities['first_addend']);
  final secondAddend = _readInt(quantities['second_addend']);
  if (firstAddend != null && secondAddend != null) {
    return [
      [firstAddend, secondAddend],
    ];
  }

  final entries = quantities.entries
      .where((entry) => entry.value is Map)
      .map((entry) => MapEntry(entry.key.toString(), entry.value as Map))
      .toList()
    ..sort((a, b) => a.key.toString().compareTo(b.key.toString()));
  final selectedEntries = _selectAdditionEntriesForContent(content, entries);
  final sets = <List<int>>[];
  for (final entry in entries) {
    if (!selectedEntries.any((selected) => selected.key == entry.key)) {
      continue;
    }
    final value = entry.value;
    final first = _readInt(value['first_addend']);
    final second = _readInt(value['second_addend']);
    if (first != null && second != null) {
      sets.add([first, second]);
      continue;
    }
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
  return sets;
}

List<List<int>> _additionTermSetsFromSteps(ProblemContent content) {
  final steps = content.solvable['steps'];
  if (steps is! List) {
    return const [];
  }
  final suffixNumber = _subproblemNumberFromProblemId(content.summary.id);
  final rawSteps = steps.whereType<Map>().where((step) {
    if (suffixNumber == null) {
      return true;
    }
    final id = step['id']?.toString() ?? '';
    return id.contains('problem_$suffixNumber');
  }).toList();
  final selectedSteps = suffixNumber == null && _answerKeyCount(content) > 0
      ? rawSteps.take(_answerKeyCount(content)).toList()
      : rawSteps;
  final sets = <List<int>>[];
  for (final step in selectedSteps) {
    final match = RegExp(r'(\d+)\s*\+\s*(\d+)')
        .firstMatch(step['expr']?.toString() ?? '');
    if (match == null) {
      continue;
    }
    sets.add([int.parse(match.group(1)!), int.parse(match.group(2)!)]);
  }
  return sets;
}

List<MapEntry<String, Map<dynamic, dynamic>>> _selectAdditionEntriesForContent(
  ProblemContent content,
  List<MapEntry<String, Map<dynamic, dynamic>>> entries,
) {
  final suffixNumber = _subproblemNumberFromProblemId(content.summary.id);
  if (suffixNumber != null) {
    final suffixKey = 'problem_$suffixNumber';
    final selected = entries.where((entry) => entry.key == suffixKey).toList();
    if (selected.isNotEmpty) {
      return selected;
    }
  }
  final answerCount = _answerKeyCount(content);
  if (answerCount > 0 && answerCount < entries.length) {
    return entries.take(answerCount).toList();
  }
  return entries;
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
