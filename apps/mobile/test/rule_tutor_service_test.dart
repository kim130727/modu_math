import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/models/content_models.dart';
import 'package:modu_math_app/models/learning_progress.dart';
import 'package:modu_math_app/models/tutor_models.dart';
import 'package:modu_math_app/services/local_progress_repository.dart';
import 'package:modu_math_app/services/rule_tutor_service.dart';

void main() {
  group('RuleTutorService', () {
    test('uses solvable count values as expected step answers', () async {
      const service = RuleTutorService();
      final content = _additionContent();

      final messages = service.startSession(content);

      expect(messages.single.replyType, equals(TutorReplyType.question));
      expect(messages.single.choices, isEmpty);

      final reply = await service.respondToStudent(
        content: content,
        messages: messages,
        message: '507',
        stepIndex: 0,
      );

      expect(reply.replyType, equals(TutorReplyType.correct));
    });

    test('accepts the correct submitted answer immediately', () async {
      const service = RuleTutorService();
      final reply = await service.reviewAnswer(
        content: _additionContent(),
        messages: const [],
        answer: '507',
      );

      expect(reply.replyType, equals(TutorReplyType.correct));
    });

    test('compacts vertical addition micro steps from direct quantities',
        () async {
      const service = RuleTutorService();
      final content = _verticalAdditionContent();

      final messages = service.startSession(content);
      final next = await service.nextQuestion(
        content: content,
        messages: messages,
        stepIndex: 0,
      );

      expect(messages.single.text, contains('1단계'));
      expect(messages.single.text, contains('4 + 7'));
      expect(next.text, contains('2단계'));
      expect(next.text, contains('6 + 5'));
    });

    test('uses only the matching suffixed vertical addition subproblem',
        () async {
      const service = RuleTutorService();
      final content = _suffixedVerticalAdditionContent();

      final messages = service.startSession(content);
      final next = await service.nextQuestion(
        content: content,
        messages: messages,
        stepIndex: 0,
      );

      expect(messages.single.text, contains('9 + 5'));
      expect(next.text, contains('4 + 7'));
      expect(messages.single.text, isNot(contains('373')));
      expect(messages.single.text, isNot(contains('468')));
      expect(next.text, isNot(contains('373')));
      expect(next.text, isNot(contains('468')));
    });

    test('asks target confirmation without problem-specific names', () async {
      const service = RuleTutorService();
      final reply = await service.reviewAnswer(
        content: _genericAdditionContent(),
        messages: const [],
        answer: '36',
      );

      expect(reply.replyType, equals(TutorReplyType.question));
      expect(reply.text, contains('1번째 부분의 수'));
      expect(reply.text, contains('2번째 부분의 수'));
      expect(reply.text, contains('전체 수'));
      expect(reply.choices, isEmpty);
      expect(reply.pendingDiagnosticCode, equals('plan.copy_one_part'));
    });

    test('uses diagnostic rules without enumerating representative answers',
        () async {
      const service = RuleTutorService();
      final reply = await service.reviewAnswer(
        content: _ruleBasedAdditionContent(),
        messages: const [],
        answer: '259',
      );

      expect(reply.replyType, equals(TutorReplyType.question));
      expect(reply.text, contains('1번째 부분의 수'));
      expect(reply.pendingDiagnosticCode, equals('plan.copy_one_part'));
    });

    test('asks carry confirmation from the expression digits', () async {
      const service = RuleTutorService();
      final reply = await service.reviewAnswer(
        content: _additionContent(),
        messages: const [],
        answer: '497',
      );

      expect(reply.replyType, equals(TutorReplyType.question));
      expect(reply.text, contains('일의 자리에서 9와 8을 더하면 얼마인가요?'));
      expect(reply.choices, isEmpty);
      expect(reply.pendingDiagnosticCode, equals('execute.add_carry.0'));
      expect(reply.errorCategory, equals(ErrorCategory.none));
    });

    test('classifies target and carry confirmation answers', () async {
      const service = RuleTutorService();
      final content = _additionContent();
      final targetPrompt = await service.reviewAnswer(
        content: content,
        messages: const [],
        answer: '248',
      );
      final targetFeedback = await service.respondToStudent(
        content: content,
        messages: [targetPrompt, service.student('두 가족이 캔 전체 수')],
        message: '두 가족이 캔 전체 수',
        stepIndex: 0,
      );
      final carryPrompt = await service.reviewAnswer(
        content: content,
        messages: const [],
        answer: '497',
      );
      final carryFeedback = await service.respondToStudent(
        content: content,
        messages: [carryPrompt, service.student('17')],
        message: '17',
        stepIndex: 0,
      );

      expect(
        targetFeedback.errorCategory,
        equals(ErrorCategory.planningOperation),
      );
      expect(
        carryFeedback.errorCategory,
        equals(ErrorCategory.executionCalculation),
      );
    });

    test('walks carry diagnosis one place at a time', () async {
      const service = RuleTutorService();
      final content = _additionContent();
      final onesPrompt = await service.reviewAnswer(
        content: content,
        messages: const [],
        answer: '497',
      );
      final tensPrompt = await service.respondToStudent(
        content: content,
        messages: [onesPrompt, service.student('17')],
        message: '17',
        stepIndex: 0,
      );
      final hundredsPrompt = await service.respondToStudent(
        content: content,
        messages: [
          onesPrompt,
          service.student('17'),
          tensPrompt,
          service.student('10'),
        ],
        message: '10',
        stepIndex: 0,
      );
      final finalFeedback = await service.respondToStudent(
        content: content,
        messages: [
          onesPrompt,
          service.student('17'),
          tensPrompt,
          service.student('10'),
          hundredsPrompt,
          service.student('5'),
        ],
        message: '5',
        stepIndex: 0,
      );

      expect(tensPrompt.text, contains('십의 자리만 볼게요'));
      expect(tensPrompt.text, contains('5와 4와 받아올린 1'));
      expect(
        tensPrompt.pendingDiagnosticCode,
        equals('execute.add_carry.1'),
      );
      expect(hundredsPrompt.text, contains('백의 자리'));
      expect(hundredsPrompt.text, contains('2와 2와 받아올린 1'));
      expect(
        hundredsPrompt.pendingDiagnosticCode,
        equals('execute.add_carry.2'),
      );
      expect(finalFeedback.text, contains('507'));
      expect(finalFeedback.pendingDiagnosticCode, isNull);
    });

    test('walks carry diagnosis for a different addition expression', () async {
      const service = RuleTutorService();
      final content = _genericAdditionContent();
      final onesPrompt = await service.reviewAnswer(
        content: content,
        messages: const [],
        answer: '53',
      );
      final tensPrompt = await service.respondToStudent(
        content: content,
        messages: [onesPrompt, service.student('13')],
        message: '13',
        stepIndex: 0,
      );
      final finalFeedback = await service.respondToStudent(
        content: content,
        messages: [
          onesPrompt,
          service.student('13'),
          tensPrompt,
          service.student('6')
        ],
        message: '6',
        stepIndex: 0,
      );

      expect(onesPrompt.text, contains('6와 7'));
      expect(tensPrompt.text, contains('3와 2와 받아올린 1'));
      expect(finalFeedback.text, contains('63'));
    });

    test('starts place diagnosis for an unregistered wrong answer', () async {
      const service = RuleTutorService();
      final reply = await service.reviewAnswer(
        content: _additionContent(),
        messages: const [],
        answer: '300',
      );

      expect(reply.replyType, equals(TutorReplyType.question));
      expect(reply.text, contains('일의 자리'));
      expect(reply.text, contains('9'));
      expect(reply.text, contains('8'));
      expect(reply.pendingDiagnosticCode, equals('execute.add_carry.0'));
      expect(reply.errorCategory, equals(ErrorCategory.none));
    });

    test('stores the confirmed error category in the learning record',
        () async {
      const service = RuleTutorService();
      final content = _additionContent();
      final repository = LocalProgressRepository();

      await repository.recordAttempt(
        problem: content.summary,
        answer: '259',
        isCorrect: false,
      );
      final prompt = await service.reviewAnswer(
        content: content,
        messages: const [],
        answer: '259',
      );
      final feedback = await service.respondToStudent(
        content: content,
        messages: [prompt, service.student('두 가족이 캔 전체 수')],
        message: '두 가족이 캔 전체 수',
        stepIndex: 0,
      );

      await repository.updateAttemptErrorCategory(
        attemptId: '',
        category: feedback.errorCategory,
      );
      final attempts = await repository.getAttempts();

      expect(feedback.errorCategory, equals(ErrorCategory.planningOperation));
      expect(
        attempts.single.errorCategory,
        equals(ErrorCategory.planningOperation),
      );
    });
  });
}

ProblemContent _additionContent() {
  return const ProblemContent(
    summary: ProblemSummary(
      id: 'P3_1_01_00040_00469',
      grade: 3,
      subject: 'math',
      unit: '3-1 addition',
      type: 'numeric_answer_addition_word_problem',
      title: 'Sweet potatoes',
      path: '',
      raw: {},
    ),
    svg: '<svg></svg>',
    semantic: {
      'metadata': {
        'question': '259 and 248 altogether',
      },
      'answer': {
        'value': 507,
        'unit': '개',
      },
    },
    solvable: {
      'method': 'add_parts',
      'steps': [
        {
          'id': 'step.add_counts',
          'goal': 'Find the total count.',
          'expr': '259 + 248',
          'value': {
            'count': 507,
            'unit': '개',
            'ref': 'quantity.total',
          },
          'explanation': 'Add 259 and 248.',
        },
      ],
      'answer': {
        'value': 507,
        'unit': '개',
      },
      'target': {
        'id': 'total',
        'label': '두 가족이 캔 전체 수',
      },
      'diagnostics': {
        'skills': [
          'add.part_part_whole',
          'add.three_digit',
        ],
        'errors': {
          '497': 'execute.add_carry',
          '259': 'plan.copy_one_part',
          '248': 'plan.copy_one_part',
        },
      },
    },
  );
}

ProblemContent _verticalAdditionContent() {
  return const ProblemContent(
    summary: ProblemSummary(
      id: 'P3_1_01_00040_02135',
      grade: 3,
      subject: 'math',
      unit: 'addition',
      type: 'multi_blank_vertical_addition',
      title: 'Column addition',
      path: '',
      raw: {},
    ),
    svg: '<svg></svg>',
    semantic: {},
    solvable: {
      'problem_type': 'multi_blank_vertical_addition',
      'inputs': {
        'answer_type': 'digit_list',
        'quantities': {
          'first_addend': 664,
          'second_addend': 257,
        },
      },
      'target': {'type': 'digit_list'},
      'steps': [
        {'id': 'step.add_ones', 'expr': '4 + 7', 'value': 11},
        {
          'id': 'step.write_ones_and_carry',
          'expr': '11 = 1 x 10 + 1',
          'value': {'carry': 1, 'digit': 1},
        },
        {'id': 'step.add_tens', 'expr': '6 + 5 + 1', 'value': 12},
        {
          'id': 'step.write_tens_and_carry',
          'expr': '12 = 1 x 10 + 2',
          'value': {'carry': 1, 'digit': 2},
        },
        {'id': 'step.add_hundreds', 'expr': '6 + 2 + 1', 'value': 9},
        {'id': 'step.compose_answer', 'expr': '900 + 20 + 1', 'value': 921},
      ],
      'answer': {
        'value': [1, 1, 9, 2, 1]
      },
    },
  );
}

ProblemContent _suffixedVerticalAdditionContent() {
  return const ProblemContent(
    summary: ProblemSummary(
      id: 'P3_1_01_00040_02151_1',
      grade: 3,
      subject: 'math',
      unit: 'addition',
      type: 'multi_answer_vertical_addition',
      title: 'Column addition',
      path: '',
      raw: {},
    ),
    svg: '<svg></svg>',
    semantic: {},
    solvable: {
      'problem_type': 'multi_answer_vertical_addition',
      'inputs': {
        'answer_type': 'number_list',
        'quantities': {
          'problem_1': {
            'first_addend': 449,
            'second_addend': 275,
          },
          'problem_2': {
            'first_addend': 373,
            'second_addend': 468,
          },
          'problem_3': {
            'first_addend': 536,
            'second_addend': 287,
          },
        },
      },
      'steps': [
        {'id': 'step.problem_1.compose_sum', 'expr': '449 + 275', 'value': 724},
        {'id': 'step.problem_2.compose_sum', 'expr': '373 + 468', 'value': 841},
        {'id': 'step.problem_3.compose_sum', 'expr': '536 + 287', 'value': 823},
      ],
      'answer': {
        'answer_key': [
          {'value': 724},
        ],
      },
    },
  );
}

ProblemContent _genericAdditionContent() {
  return const ProblemContent(
    summary: ProblemSummary(
      id: 'P_ADD_GENERIC',
      grade: 2,
      subject: 'math',
      unit: 'addition',
      type: 'numeric_answer_addition_word_problem',
      title: 'Generic addition',
      path: '',
      raw: {},
    ),
    svg: '<svg></svg>',
    semantic: {
      'answer': {
        'value': 63,
      },
    },
    solvable: {
      'method': 'add_parts',
      'given': [
        {
          'id': 'first',
          'value': 36,
        },
        {
          'id': 'second',
          'value': 27,
        },
      ],
      'target': {
        'id': 'total',
      },
      'steps': [
        {
          'id': 'step.add_counts',
          'goal': 'Find the total count.',
          'expr': '36 + 27',
          'value': 63,
        },
      ],
      'answer': {
        'value': 63,
      },
      'diagnostics': {
        'skills': [
          'add.part_part_whole',
          'add.two_digit',
        ],
        'errors': {
          '36': 'plan.copy_one_part',
          '53': 'execute.add_carry',
        },
      },
    },
  );
}

ProblemContent _ruleBasedAdditionContent() {
  return const ProblemContent(
    summary: ProblemSummary(
      id: 'P_ADD_RULE',
      grade: 3,
      subject: 'math',
      unit: 'addition',
      type: 'numeric_answer_addition_word_problem',
      title: 'Rule addition',
      path: '',
      raw: {},
    ),
    svg: '<svg></svg>',
    semantic: {
      'answer': {
        'value': 507,
      },
    },
    solvable: {
      'method': 'add_parts',
      'given': [
        {
          'id': 'first',
          'value': 259,
        },
        {
          'id': 'second',
          'value': 248,
        },
      ],
      'target': {
        'id': 'total',
      },
      'steps': [
        {
          'id': 'step.add_counts',
          'goal': 'Find the total count.',
          'expr': '259 + 248',
          'value': 507,
        },
      ],
      'answer': {
        'value': 507,
      },
      'diagnostics': {
        'skills': [
          'plan.add_parts',
          'execute.add_carry',
        ],
        'rules': [
          {
            'condition': 'answer_equals_given_value',
            'code': 'plan.copy_one_part',
          },
          {
            'condition': 'addition_with_carry_wrong_answer',
            'code': 'execute.add_carry',
          },
        ],
      },
    },
  );
}
