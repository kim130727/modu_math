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
    this.successMessage = '좋아요. 다음 단계로 가 볼게요.',
  });

  final int level;
  final String title;
  final String body;
  final String miniQuestion;
  final List<String> acceptedAnswers;
  final List<HintChoice> choices;
  final String successMessage;
}

class SolvableHintService {
  const SolvableHintService();

  List<SolvableHint> buildHints(ProblemContent content) {
    final columnHints = _columnAdditionHints(content);
    if (columnHints.isNotEmpty) {
      return columnHints;
    }

    final authoredHints = _authoredStudentHints(content);
    if (authoredHints.isNotEmpty) {
      return authoredHints;
    }

    return [
      const SolvableHint(
        level: 1,
        title: '1단계: 묻는 것 찾기',
        body: '문제에서 무엇을 구해야 하는지 먼저 확인해요.',
        miniQuestion: '무엇을 구하는 문제인가요?',
        choices: [
          HintChoice(label: '전체 수', isCorrect: true),
          HintChoice(label: '한쪽 수'),
          HintChoice(label: '남은 수'),
        ],
        acceptedAnswers: ['전체 수', '전체'],
        successMessage: '맞아요. 전체를 구할 때는 주어진 수들을 함께 봐야 해요.',
      ),
      const SolvableHint(
        level: 2,
        title: '2단계: 계산 방법 고르기',
        body: '전체를 구하는 문제라면 더하기를 쓰는지 확인해요.',
        miniQuestion: '전체를 구할 때 가장 알맞은 계산은 무엇인가요?',
        choices: [
          HintChoice(label: '더하기', isCorrect: true),
          HintChoice(label: '빼기'),
          HintChoice(label: '비교하기'),
        ],
        acceptedAnswers: ['더하기', '+'],
        successMessage: '좋아요. 이제 자릿값을 보며 차근차근 더해요.',
      ),
      const SolvableHint(
        level: 3,
        title: '3단계: 작은 수부터 계산',
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
      const SolvableHint(
        level: 4,
        title: '4단계: 다시 확인',
        body: '각 자리의 답과 올림한 1을 빠뜨리지 않았는지 확인해요.',
        miniQuestion: '마지막에 꼭 확인할 것은 무엇인가요?',
        choices: [
          HintChoice(label: '올림한 수를 더했는지', isCorrect: true),
          HintChoice(label: '글씨를 크게 썼는지'),
          HintChoice(label: '문제를 한 번만 봤는지'),
        ],
        acceptedAnswers: ['올림', '올림한 수', '받아올림'],
        successMessage: '좋아요. 올림한 수까지 확인하면 더 정확해져요.',
      ),
    ];
  }
}

List<SolvableHint> _columnAdditionHints(ProblemContent content) {
  final terms = _additionTerms(content);
  if (terms.length < 2 || !_isAdditionProblem(content)) {
    return const [];
  }

  final left = terms[0].abs();
  final right = terms[1].abs();
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
      level: 1,
      title: '1단계: 일의 자리 더하기',
      body: '맨 오른쪽에 있는 일의 자리부터 더해요.',
      miniQuestion: '$onesLeft + $onesRight은 얼마인가요?',
      choices: _numberChoices(onesSum, [onesSum - 1, onesDigit, onesSum + 1]),
      acceptedAnswers: ['$onesSum'],
      successMessage: '맞아요. 일의 자리 합은 $onesSum이에요.',
    ),
    SolvableHint(
      level: 2,
      title: '2단계: 일의 자리 쓰기',
      body: '$onesSum처럼 10이 넘으면 일의 자리 숫자만 아래에 쓰고, 1은 다음 자리로 올려요.',
      miniQuestion: '일의 자리에는 어떤 숫자를 쓰나요?',
      choices: _numberChoices(
        onesDigit,
        [onesSum, carryToTens, (onesDigit + 1) % 10],
      ),
      acceptedAnswers: ['$onesDigit'],
      successMessage: '좋아요. 일의 자리에는 $onesDigit을 쓰고, 1을 십의 자리로 올려요.',
    ),
    SolvableHint(
      level: 3,
      title: '3단계: 십의 자리 더하기',
      body: '십의 자리 숫자들을 더할 때, 아까 올린 1도 함께 더해요.',
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
      successMessage: '맞아요. $tensLeft + $tensRight에 올린 1을 더해서 $tensSum이 돼요.',
    ),
    SolvableHint(
      level: 4,
      title: '4단계: 백의 자리와 답',
      body: '십의 자리에서 또 10이 넘었다면 1을 백의 자리로 올려요. 마지막으로 세 자리를 이어서 답을 만들어요.',
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
  final labels = <String>[correct];
  for (final distractor in distractors) {
    if (distractor.trim().isNotEmpty && !labels.contains(distractor)) {
      labels.add(distractor);
    }
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
