import '../models/content_models.dart';
import '../utils/answer_normalizer.dart';

class AnswerDiagnosticService {
  const AnswerDiagnosticService();

  String feedbackFor({
    required ProblemContent content,
    required String answer,
  }) {
    final direct = _feedbackFromAnswerKeyDiagnostics(content, answer);
    if (direct.isNotEmpty) {
      return direct;
    }
    final registered = _feedbackFromRegisteredCode(content, answer);
    if (registered.isNotEmpty) {
      return registered;
    }
    return _inferredFeedback(content, answer);
  }

  String _feedbackFromAnswerKeyDiagnostics(
    ProblemContent content,
    String answer,
  ) {
    final answerKey = content.answerMap['answer_key'];
    if (answerKey is! List) {
      return '';
    }
    for (final keyItem in answerKey.whereType<Map>()) {
      final diagnostics = keyItem['diagnostics'];
      if (diagnostics is! List) {
        continue;
      }
      for (final diagnostic in diagnostics.whereType<Map>()) {
        final wrongValue = diagnostic['wrong_value'];
        if (wrongValue != null && isSameAnswer(answer, wrongValue.toString())) {
          return diagnostic['feedback']?.toString().trim() ?? '';
        }
        final pattern = diagnostic['wrong_pattern']?.toString().trim();
        if (pattern != null &&
            pattern.isNotEmpty &&
            RegExp(pattern).hasMatch(answer.trim())) {
          return diagnostic['feedback']?.toString().trim() ?? '';
        }
        if (_matchesRange(diagnostic, answer)) {
          return diagnostic['feedback']?.toString().trim() ?? '';
        }
        final conditionFeedback = _conditionFeedback(
          diagnostic,
          content,
          answer,
        );
        if (conditionFeedback.isNotEmpty) {
          return conditionFeedback;
        }
      }
    }
    return '';
  }

  bool _matchesRange(Map diagnostic, String answer) {
    final value = num.tryParse(answer.trim());
    if (value == null) {
      return false;
    }
    final min = _numberValue(diagnostic['wrong_min']);
    final max = _numberValue(diagnostic['wrong_max']);
    if (min == null && max == null) {
      return false;
    }
    if (min != null && value < min) {
      return false;
    }
    if (max != null && value > max) {
      return false;
    }
    return true;
  }

  bool _matchesCondition(
    Map diagnostic,
    ProblemContent content,
    String answer,
  ) {
    final condition = diagnostic['condition']?.toString().trim();
    if (condition == null || condition.isEmpty) {
      return false;
    }
    final value = num.tryParse(answer.trim());
    final correct = num.tryParse(content.correctAnswer.trim());
    return switch (condition) {
      'answer_equals_given_value' => _answerEqualsGivenValue(content, answer),
      'answer_equals_step_value' => _answerEqualsStepValue(content, answer),
      'numeric_wrong_answer' =>
        value != null && (correct == null || value != correct),
      'numeric_less_than_answer' =>
        value != null && correct != null && value < correct,
      'numeric_greater_than_answer' =>
        value != null && correct != null && value > correct,
      'addition_with_carry_wrong_answer' => value != null &&
          (correct == null || value != correct) &&
          _hasCarry(_additionTerms(content)),
      _ => false,
    };
  }

  String _conditionFeedback(
    Map diagnostic,
    ProblemContent content,
    String answer,
  ) {
    if (!_matchesCondition(diagnostic, content, answer)) {
      return '';
    }
    final condition = diagnostic['condition']?.toString().trim();
    if (condition == 'addition_with_carry_wrong_answer') {
      final carryFeedback = _additionCarryFeedback(content, answer);
      if (carryFeedback.isNotEmpty) {
        return carryFeedback;
      }
    }
    return diagnostic['feedback']?.toString().trim() ?? '';
  }

  bool _answerEqualsGivenValue(ProblemContent content, String answer) {
    final given = content.solvable['given'];
    if (given is! List) {
      return false;
    }
    return given.whereType<Map>().any((item) {
      final value = item['value'];
      return value != null && isSameAnswer(answer, value.toString());
    });
  }

  bool _answerEqualsStepValue(ProblemContent content, String answer) {
    final steps = content.solvable['steps'];
    if (steps is! List) {
      return false;
    }
    return steps.whereType<Map>().any((step) {
      final value = step['value'];
      return value != null &&
          isSameAnswer(answer, _answerValueText(value).toString());
    });
  }

  String _feedbackFromRegisteredCode(ProblemContent content, String answer) {
    final diagnostics = content.solvable['diagnostics'];
    if (diagnostics is! Map<String, dynamic>) {
      return '';
    }
    final errors = diagnostics['errors'];
    if (errors is! Map<String, dynamic>) {
      return '';
    }
    final code = errors[answer.trim()]?.toString();
    if (code == null || code.isEmpty) {
      return '';
    }
    return switch (code) {
      'plan.copy_one_part' =>
        '한 가족의 수만 쓰면 안 돼요. 두 가족이 캔 수를 모두 구해야 하니 두 수를 더해 보세요.',
      'execute.add_carry' =>
        '받아올림을 다시 확인해요. 일의 자리부터 더하고, 10이 넘으면 다음 자리로 1을 올려요.',
      'execute.add_fact' => '덧셈 계산을 다시 확인해요. 각 자리의 수를 차례로 더해 보세요.',
      'execute.place_value_compose' =>
        '받아올림한 수나 중간 계산을 그대로 이어 쓰면 안 돼요. 각 자리 숫자로 다시 모아 보세요.',
      _ => '',
    };
  }

  String _inferredFeedback(ProblemContent content, String answer) {
    if (isSameAnswer(answer, content.correctAnswer)) {
      return '';
    }
    if (int.tryParse(answer.trim()) == null) {
      return '';
    }
    final expression = _additionExpression(content);
    if (expression == null) {
      return '';
    }
    final terms = _termsFromExpression(expression);
    if (terms.length < 2 || !_hasCarry(terms)) {
      return '계산식을 다시 확인해요. 문제에 나온 수를 모두 사용했는지 살펴보세요.';
    }
    final carryFeedback = _additionCarryFeedback(content, answer);
    if (carryFeedback.isNotEmpty) {
      return carryFeedback;
    }
    return _genericCarryFeedback;
  }

  String _additionCarryFeedback(ProblemContent content, String answer) {
    final answerValue = int.tryParse(answer.trim());
    final correctValue = int.tryParse(content.correctAnswer.trim());
    if (answerValue == null ||
        correctValue == null ||
        answerValue == correctValue) {
      return '';
    }
    final terms = _additionTerms(content);
    if (terms.length < 2 || !_hasCarry(terms)) {
      return '';
    }

    final answerDigits = _digitsFromRight(answerValue);
    final correctDigits = _digitsFromRight(correctValue);
    final columns = _additionColumns(terms);
    final maxLength = [
      answerDigits.length,
      correctDigits.length,
      columns.length,
    ].reduce((a, b) => a > b ? a : b);

    for (var index = 0; index < maxLength; index += 1) {
      final answerDigit = index < answerDigits.length ? answerDigits[index] : 0;
      final correctDigit =
          index < correctDigits.length ? correctDigits[index] : 0;
      if (answerDigit == correctDigit) {
        continue;
      }
      final column = index < columns.length ? columns[index] : null;
      final place = _placeName(index);
      if (column == null) {
        return '$place 자리의 숫자를 다시 확인해요.';
      }
      if (answerDigit == correctDigit + 1 && column.carryIn > 0) {
        return '$place 자리에서 올린 1을 한 번만 더했는지 확인해요. 올림을 두 번 더하면 수가 커져요.';
      }
      if (answerDigit == correctDigit - 1 && column.carryIn > 0) {
        return '$place 자리에서 앞 자리에서 올린 1을 빠뜨리지 않았는지 확인해요.';
      }
      if (column.carryOut > 0) {
        return '$place 자리에서 10이 넘는지 확인해요. 10이 넘으면 다음 자리로 1을 올려요.';
      }
      return '$place 자리 계산을 다시 확인해요. 같은 자리 숫자끼리 차례대로 더해 보세요.';
    }
    return _genericCarryFeedback;
  }

  List<int> _additionTerms(ProblemContent content) {
    final expression = _additionExpression(content);
    return expression == null ? const [] : _termsFromExpression(expression);
  }

  List<int> _termsFromExpression(String expression) {
    return RegExp(r'\d+')
        .allMatches(expression)
        .map((match) => int.parse(match.group(0)!))
        .toList();
  }

  num? _numberValue(Object? value) {
    if (value is num) {
      return value;
    }
    return num.tryParse(value?.toString() ?? '');
  }

  Object _answerValueText(Object value) {
    if (value is Map) {
      for (final key in const ['value', 'count', 'result', 'answer']) {
        final nested = value[key];
        if (nested != null) {
          return nested;
        }
      }
    }
    return value;
  }

  String? _additionExpression(ProblemContent content) {
    final steps = content.solvable['steps'];
    if (steps is List) {
      for (final step in steps.whereType<Map>()) {
        final expr = step['expr']?.toString().trim();
        if (expr != null &&
            RegExp(r'^\s*\d+\s*(?:\+\s*\d+\s*)+$').hasMatch(expr)) {
          return expr;
        }
      }
    }
    return null;
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

  List<_AdditionColumn> _additionColumns(List<int> terms) {
    final columns = <_AdditionColumn>[];
    var carry = 0;
    final maxDigits = terms
        .map((term) => term.toString().length)
        .fold<int>(0, (max, length) => length > max ? length : max);
    for (var index = 0; index < maxDigits; index += 1) {
      final divisor = _pow10(index);
      final digits = terms.map((term) => (term ~/ divisor) % 10).toList();
      final sum = digits.fold<int>(carry, (total, digit) => total + digit);
      columns.add(
        _AdditionColumn(
          carryIn: carry,
          sum: sum,
          carryOut: sum ~/ 10,
        ),
      );
      carry = sum ~/ 10;
    }
    if (carry > 0) {
      columns.add(_AdditionColumn(carryIn: carry, sum: carry, carryOut: 0));
    }
    return columns;
  }

  List<int> _digitsFromRight(int value) {
    return value.abs().toString().split('').reversed.map(int.parse).toList();
  }

  String _placeName(int index) {
    return switch (index) {
      0 => '일의',
      1 => '십의',
      2 => '백의',
      3 => '천의',
      _ => '${index + 1}번째',
    };
  }

  int _pow10(int exponent) {
    var result = 1;
    for (var index = 0; index < exponent; index += 1) {
      result *= 10;
    }
    return result;
  }
}

const _genericCarryFeedback =
    '일의 자리부터 다시 계산해요. 10이 넘으면 올린 1을 다음 자리 계산에 꼭 넣어 보세요.';

class _AdditionColumn {
  const _AdditionColumn({
    required this.carryIn,
    required this.sum,
    required this.carryOut,
  });

  final int carryIn;
  final int sum;
  final int carryOut;
}
