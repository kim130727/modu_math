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
          _targetHintText(content),
        ),
      ),
      SolvableHint(
        level: 2,
        title: '2단계: 해결 방법',
        body: _withoutAnswer(
          content,
          [
            '방법: ${_methodText(content.solvable['method'])}',
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
        title: '4단계: 마지막 점검',
        body: _withoutAnswer(content, _finalCheckHint(content)),
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

  String _finalCheckHint(ProblemContent content) {
    final steps = content.steps;
    if (steps.isNotEmpty) {
      final lastStep = _stepText(steps.last);
      return [
        '식과 계산 방향이 문제에서 구하는 것과 맞는지 확인해 보세요.',
        '마지막으로 확인할 부분: $lastStep',
        '내가 쓴 답이 두 수를 모두 사용한 결과인지 다시 살펴보세요.',
      ].join('\n');
    }
    return '주어진 수를 모두 사용했는지, 구해야 하는 것에 맞는 식을 세웠는지 다시 확인해 보세요.';
  }

  String _stepText(SolutionStep step) {
    final explanation = sanitizeProblemText(step.explanation).trim();
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

String _targetHintText(ProblemContent content) {
  final target = _targetText(content);
  if (target == '무엇을 구해야 하는지') {
    return '무엇을 구해야 하는지 확인해 보세요.';
  }
  return '$target${_objectParticle(target)} 구하는 문제인지 확인해 보세요.';
}

String _targetText(ProblemContent content) {
  final inputs = content.solvable['inputs'];
  if (inputs is Map) {
    final inputLabel = _readText(inputs['target_label']);
    if (_isStudentFacingTargetText(inputLabel)) {
      return inputLabel;
    }
  }

  final target = content.solvable['target'];
  if (target is Map) {
    for (final key in const ['label', 'name', 'description', 'text']) {
      final text = _readText(target[key]);
      if (_isStudentFacingTargetText(text)) {
        return text;
      }
    }
    final refText = _refToStudentText(target['ref']);
    if (refText.isNotEmpty) {
      return refText;
    }
    final typeText = _targetTypeText(target['type']);
    if (typeText.isNotEmpty) {
      return typeText;
    }
  }

  final text = _readText(target);
  return text.isEmpty ? '무엇을 구해야 하는지' : text;
}

bool _isStudentFacingTargetText(String value) {
  final text = value.trim();
  if (text.isEmpty || _looksBrokenText(text)) {
    return false;
  }
  if (RegExp(r'^[a-zA-Z0-9_.]+$').hasMatch(text)) {
    return false;
  }
  return true;
}

bool _looksBrokenText(String value) {
  return RegExp(r'[\u3400-\u9FFF\uFFFD]').hasMatch(value) ||
      value.contains('??') ||
      value.contains('�');
}

String _targetTypeText(Object? value) {
  final type = value?.toString().trim() ?? '';
  if (type.isEmpty) {
    return '';
  }
  return switch (type) {
    'operator_list' => '각 빈칸에 들어갈 비교 기호',
    'count' => '전체 수',
    'digit_list' => '빈칸에 들어갈 숫자',
    'number_list' => '각 계산 결과',
    'mixed_integer_list' => '빈칸에 들어갈 수',
    'addition_results' => '각 덧셈의 계산 결과',
    'sequential_addition_results' => '차례대로 들어갈 수',
    'addition_rule_results' => '규칙에 맞게 들어갈 수',
    'missing_digits' => '빈칸에 들어갈 숫자',
    'number_pair' => '두 수',
    'choice_number' => '보기 번호',
    'choice' ||
    'selected_option' ||
    'selection' ||
    'choice_selection' =>
      '알맞은 보기',
    'choice_order' || 'ordering' || 'ordered_choice' => '알맞은 순서',
    'selected_unit' ||
    'unit_selection' ||
    'unit_choice' ||
    'unit_symbol' =>
      '알맞은 단위',
    'correct_notation' => '바른 표기',
    'comparison_word' => '알맞은 비교 말',
    'text' => '알맞은 말',
    'distance' => '전체 거리',
    'sum' => '합',
    'selected_person' ||
    'person_name' ||
    'person' ||
    'correct_speaker' ||
    'speaker_selection' ||
    'selected_friend' ||
    'selected_student' =>
      '알맞은 사람',
    'selected_object' ||
    'selected_container' ||
    'container_name' ||
    'container_choice' ||
    'select_container' ||
    'bottle_choice' ||
    'greater_capacity_choice' =>
      '알맞은 물건',
    'lighter_object' || 'lighter_object_name' => '더 가벼운 것',
    'heavier_object' || 'heavier_object_name' => '더 무거운 것',
    'heaviest_fruit' => '가장 무거운 과일',
    'least_capacity_container' => '들이가 가장 적은 그릇',
    'selected_bottles' => '알맞은 병',
    'estimated_quantity_choice' || 'estimated_capacity' => '어림한 양',
    'incorrect_weight_statement' => '잘못 말한 내용',
    _ => _phraseFromCode(type),
  };
}

String _refToStudentText(Object? value) {
  final ref = value?.toString().trim() ?? '';
  if (ref.isEmpty) {
    return '';
  }
  final knownRef = _targetRefText(ref);
  if (knownRef.isNotEmpty) {
    return knownRef;
  }
  final normalized = ref
      .replaceAll(
        RegExp(
          r'^(answer|quantity|group|object|measure|collection|comparison|choice|number|place)\.',
        ),
        '',
      )
      .replaceAll('this_year', '올해')
      .replaceAll('last_year', '작년')
      .replaceAll('_', ' ');
  final translated = normalized
      .split(RegExp(r'\s+'))
      .where((word) => word.isNotEmpty && word != 'target')
      .map(_targetWord)
      .where((word) => word.isNotEmpty)
      .join(' ')
      .trim();
  return translated;
}

String _targetRefText(String ref) {
  return switch (ref) {
    'answer.comparison_operators' => '각 빈칸에 들어갈 비교 기호',
    'group.all_readers' => '책을 읽고 있는 사람의 전체 수',
    'collection.total_stamps' => '우표의 전체 수',
    'answer.vertical_addition_blanks' => '받아올림한 수와 계산 결과',
    'answer.vertical_addition_results' => '각 세로셈의 계산 결과',
    'answer.total_distance' => '전체 거리',
    'quantity.total_pages_read' => '읽은 전체 쪽수',
    'quantity.total_pages' => '전체 쪽수',
    'quantity.total_pencil_count' => '전체 연필 수',
    'quantity.total_stamp_count' => '우표의 전체 수',
    'quantity.total_photos' => '전체 사진 수',
    'quantity.total_marbles' => '구슬의 전체 수',
    _ => '',
  };
}

String _targetWord(String word) {
  return switch (word) {
    '올해' => '올해',
    'last' => '작년',
    'apple' => '사과',
    'operators' || 'operator' => '기호',
    'comparison' => '비교',
    'count' => '수',
    'stamp' || 'stamps' => '우표',
    'total' || 'all' => '전체',
    'pages' || 'page' => '쪽수',
    'read' => '읽은',
    'readers' => '읽고 있는 사람',
    'distance' => '거리',
    'sum' => '합',
    'values' => '수',
    'blanks' => '빈칸',
    'digits' => '숫자',
    _ => RegExp(r'^[a-zA-Z0-9]+$').hasMatch(word) ? '' : word,
  };
}

String _phraseFromCode(String value) {
  final words = value
      .replaceAll('_', ' ')
      .split(RegExp(r'\s+'))
      .where((word) => word.isNotEmpty)
      .map(_targetWord)
      .where((word) => word.isNotEmpty)
      .toList();
  return words.isEmpty ? '' : words.join(' ');
}

String _objectParticle(String value) {
  final trimmed = value.trim();
  if (trimmed.isEmpty) {
    return '을';
  }
  final codeUnit = trimmed.runes.last;
  if (codeUnit < 0xAC00 || codeUnit > 0xD7A3) {
    return '을';
  }
  return (codeUnit - 0xAC00) % 28 == 0 ? '를' : '을';
}

String _methodText(Object? value) {
  final text = _readText(value, fallback: '문제에 맞는 식이나 규칙을 세워 보세요.');
  return switch (text.trim()) {
    'add_parts' => '나누어 주어진 수들을 모두 더해요.',
    'addition' => '덧셈으로 전체를 구해요.',
    'one_step' => '한 번의 계산으로 구해요.',
    'multiply_equal_groups' => '같은 묶음의 수를 곱셈으로 구해요.',
    _ => text.replaceAll('_', ' '),
  };
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
