import '../../models/content_models.dart';
import '../../models/learning_progress.dart';
import 'diagnostic_strategy.dart';

class AdditionDiagnosticStrategy extends DiagnosticStrategy {
  const AdditionDiagnosticStrategy();

  static const _carryPrefix = 'execute.add_carry';

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
    return signature.contains('add') || signature.contains('addition');
  }

  @override
  bool supportsDiagnosticCode(String diagnosticCode) {
    return diagnosticCode.startsWith('plan.copy_one_part') ||
        diagnosticCode.startsWith('execute.add_');
  }

  @override
  DiagnosticPrompt? promptFor({
    required ProblemContent content,
    required String diagnosticCode,
    required String answer,
  }) {
    switch (diagnosticCode) {
      case 'plan.copy_one_part':
        return DiagnosticPrompt(
          diagnosticCode: 'plan.copy_one_part',
          text: _targetQuestion(content),
        );
      case _carryPrefix:
        final problem = _additionProblem(content);
        if (problem == null || problem.columns.isEmpty) {
          return null;
        }
        return DiagnosticPrompt(
          diagnosticCode: _carryCode(0),
          text: '계산을 바로 고치기 전에 한 자리만 확인해 볼게요.\n'
              '${_columnQuestion(problem.columns.first)}',
        );
    }
    return null;
  }

  @override
  DiagnosticResult? resultFor({
    required ProblemContent content,
    required String diagnosticCode,
    required String confirmationAnswer,
  }) {
    if (diagnosticCode == 'plan.copy_one_part') {
      return _targetResult(content, confirmationAnswer);
    }
    if (!diagnosticCode.startsWith(_carryPrefix)) {
      return null;
    }

    final problem = _additionProblem(content);
    if (problem == null || problem.columns.isEmpty) {
      return null;
    }
    final columnIndex =
        _carryColumnIndex(diagnosticCode).clamp(0, problem.columns.length - 1);
    final column = problem.columns[columnIndex];
    final isCorrect = _matchesNumber(confirmationAnswer, column.sum);
    final nextIndex = columnIndex + 1;
    final explanation = isCorrect
        ? '맞아요. ${column.sum}이니까 ${_placeName(columnIndex)} 자리에는 ${column.resultDigit}을 쓰고'
        : '${_addendText(column.digits, column.carryIn)}을 더하면 ${column.sum}이에요. 그래서 ${_placeName(columnIndex)} 자리에는 ${column.resultDigit}을 쓰고';
    final carryText = column.carryOut > 0
        ? ', ${column.carryOut}을 ${_placeName(nextIndex)} 자리로 올려요.'
        : '.';

    if (nextIndex < problem.columns.length) {
      return DiagnosticResult(
        errorCategory: ErrorCategory.executionCalculation,
        feedback: '$explanation$carryText\n'
            '이제 ${_placeName(nextIndex)} 자리만 볼게요. ${_columnQuestion(problem.columns[nextIndex])}',
        nextDiagnosticCode: _carryCode(nextIndex),
      );
    }

    return DiagnosticResult(
      errorCategory: ErrorCategory.executionCalculation,
      feedback: '$explanation$carryText\n'
          '각 자리 숫자를 모으면 ${problem.answer}이 됩니다.',
    );
  }

  DiagnosticResult _targetResult(
    ProblemContent content,
    String confirmationAnswer,
  ) {
    final problem = _additionProblem(content);
    final expression = problem?.expression ?? '주어진 수들';
    if (diagnosticTextMatchesAny(confirmationAnswer, [
      _targetLabel(content),
      '전체',
      '모두',
      '합',
      '합계',
    ])) {
      return DiagnosticResult(
        errorCategory: ErrorCategory.planningOperation,
        feedback: '맞아요. 구해야 하는 것은 ${_targetLabel(content)}예요.\n'
            '그러면 한 부분만 쓰지 말고 $expression을 더해 볼게요.',
      );
    }
    return DiagnosticResult(
      errorCategory: ErrorCategory.understandingTarget,
      feedback: '여기서 구해야 하는 것은 한 부분의 수가 아니라 ${_targetLabel(content)}예요.\n'
          '그래서 $expression을 함께 더해야 해요.',
    );
  }

  String _targetQuestion(ProblemContent content) {
    final partLabels = _partLabels(content);
    final target = _targetLabel(content);
    if (partLabels.length >= 2) {
      final parts = partLabels.take(2).join('인가요, ');
      return '잠깐 확인해 볼게요.\n'
          '이 문제에서 구해야 하는 것은 $parts인가요, 아니면 $target인가요?';
    }
    return '잠깐 확인해 볼게요.\n'
        '이 문제에서 구해야 하는 것은 한 부분의 수인가요, 아니면 $target인가요?';
  }

  _AdditionProblem? _additionProblem(ProblemContent content) {
    final expression = _additionExpression(content);
    if (expression == null) {
      return null;
    }
    final terms = RegExp(r'\d+')
        .allMatches(expression)
        .map((match) => int.parse(match.group(0)!))
        .toList();
    if (terms.length < 2) {
      return null;
    }
    final answer = terms.fold<int>(0, (sum, term) => sum + term);
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
          placeIndex: index,
          digits: digits,
          carryIn: carry,
          sum: sum,
          resultDigit: sum % 10,
          carryOut: sum ~/ 10,
        ),
      );
      carry = sum ~/ 10;
    }
    if (carry > 0) {
      columns.add(
        _AdditionColumn(
          placeIndex: maxDigits,
          digits: const [],
          carryIn: carry,
          sum: carry,
          resultDigit: carry,
          carryOut: 0,
        ),
      );
    }
    return _AdditionProblem(
      expression: expression,
      terms: terms,
      answer: answer,
      columns: columns,
    );
  }

  String? _additionExpression(ProblemContent content) {
    final steps = content.solvable['steps'];
    if (steps is List) {
      for (final step in steps.whereType<Map<String, dynamic>>()) {
        final expr = step['expr']?.toString().trim();
        if (expr != null &&
            RegExp(r'^\s*\d+\s*(?:\+\s*\d+\s*)+$').hasMatch(expr)) {
          return expr.replaceAll(RegExp(r'\s+'), ' ');
        }
      }
    }
    final given = content.solvable['given'];
    if (given is List) {
      final values = given
          .whereType<Map<String, dynamic>>()
          .map((item) => int.tryParse(item['value']?.toString() ?? ''))
          .whereType<int>()
          .toList();
      if (values.length >= 2) {
        return values.join(' + ');
      }
    }
    return null;
  }

  List<String> _partLabels(ProblemContent content) {
    final given = content.solvable['given'];
    if (given is! List) {
      return const [];
    }
    final labels = <String>[];
    for (final item in given.whereType<Map<String, dynamic>>()) {
      final label = _cleanLabel(item['label']?.toString());
      if (label != null) {
        labels.add(label);
      }
    }
    if (labels.isNotEmpty) {
      return labels;
    }
    return List.generate(given.length, (index) => '${index + 1}번째 부분의 수');
  }

  String _targetLabel(ProblemContent content) {
    final target = content.solvable['target'];
    if (target is Map<String, dynamic>) {
      final label = _cleanLabel(target['label']?.toString());
      if (label != null) {
        return label;
      }
    }
    return '전체 수';
  }

  String? _cleanLabel(String? value) {
    final text = value?.trim();
    if (text == null || text.isEmpty || _looksBroken(text)) {
      return null;
    }
    return text;
  }

  bool _looksBroken(String value) {
    return RegExp(r'[\u3400-\u9FFF\uFFFD]').hasMatch(value) ||
        value.contains('??') ||
        value.contains('占');
  }

  String _columnQuestion(_AdditionColumn column) {
    return '${_placeName(column.placeIndex)} 자리에서 ${_addendText(column.digits, column.carryIn)}을 더하면 얼마인가요?';
  }

  String _addendText(List<int> digits, int carryIn) {
    final values = [
      ...digits,
      if (carryIn > 0) '받아올린 $carryIn',
    ];
    if (values.isEmpty) {
      return '받아올린 $carryIn';
    }
    return values.join('와 ');
  }

  bool _matchesNumber(String answer, int expected) {
    final normalized = answer.trim().replaceAll(',', '');
    return int.tryParse(normalized) == expected;
  }

  String _carryCode(int columnIndex) => '$_carryPrefix.$columnIndex';

  int _carryColumnIndex(String diagnosticCode) {
    final parts = diagnosticCode.split('.');
    return int.tryParse(parts.last) ?? 0;
  }

  String _placeName(int index) {
    switch (index) {
      case 0:
        return '일의';
      case 1:
        return '십의';
      case 2:
        return '백의';
      case 3:
        return '천의';
      default:
        return '${index + 1}번째';
    }
  }

  int _pow10(int exponent) {
    var value = 1;
    for (var index = 0; index < exponent; index += 1) {
      value *= 10;
    }
    return value;
  }
}

class _AdditionProblem {
  const _AdditionProblem({
    required this.expression,
    required this.terms,
    required this.answer,
    required this.columns,
  });

  final String expression;
  final List<int> terms;
  final int answer;
  final List<_AdditionColumn> columns;
}

class _AdditionColumn {
  const _AdditionColumn({
    required this.placeIndex,
    required this.digits,
    required this.carryIn,
    required this.sum,
    required this.resultDigit,
    required this.carryOut,
  });

  final int placeIndex;
  final List<int> digits;
  final int carryIn;
  final int sum;
  final int resultDigit;
  final int carryOut;
}
