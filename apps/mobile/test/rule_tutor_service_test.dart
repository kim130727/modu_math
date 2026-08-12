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
      expect(messages.single.choices, contains('507'));

      final reply = await service.respondToStudent(
        content: content,
        messages: messages,
        message: '507',
        stepIndex: 0,
      );

      expect(reply.replyType, equals(TutorReplyType.correct));
    });

    test('infers addition feedback during step tutoring', () async {
      const service = RuleTutorService();
      final content = _additionContent();
      final messages = service.startSession(content);

      final reply = await service.respondToStudent(
        content: content,
        messages: messages,
        message: '1111',
        stepIndex: 0,
      );

      expect(reply.replyType, equals(TutorReplyType.question));
      expect(reply.text, contains('받아올림'));
      expect(reply.choices, contains('507'));
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

    test('asks target confirmation for copied part answers', () async {
      const service = RuleTutorService();
      final content = _additionContent();

      for (final answer in const ['259', '248']) {
        final reply = await service.reviewAnswer(
          content: content,
          messages: const [],
          answer: answer,
        );

        expect(reply.replyType, equals(TutorReplyType.question));
        expect(reply.text, contains('이 문제에서 구해야 하는 것은'));
        expect(reply.text, contains('상현이네 가족의 수'));
        expect(reply.text, contains('용진이네 가족의 수'));
        expect(reply.text, contains('두 가족이 캔 전체 수'));
        expect(reply.choices, isEmpty);
        expect(reply.pendingDiagnosticCode, equals('plan.copy_one_part'));
        expect(reply.errorCategory, equals(ErrorCategory.none));
      }
    });

    test('asks carry confirmation for the representative carry answer',
        () async {
      const service = RuleTutorService();
      final reply = await service.reviewAnswer(
        content: _additionContent(),
        messages: const [],
        answer: '497',
      );

      expect(reply.replyType, equals(TutorReplyType.question));
      expect(reply.text, contains('일의 자리에서 9와 8을 더하면 얼마인가요?'));
      expect(reply.choices, isEmpty);
      expect(reply.pendingDiagnosticCode, equals('execute.add_carry'));
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
        messages: [targetPrompt, service.student('용진이네 가족의 수')],
        message: '용진이네 가족의 수',
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
        equals(ErrorCategory.understandingTarget),
      );
      expect(
        carryFeedback.errorCategory,
        equals(ErrorCategory.executionCalculation),
      );
    });

    test('does not immediately classify an unregistered wrong answer',
        () async {
      const service = RuleTutorService();
      final reply = await service.reviewAnswer(
        content: _additionContent(),
        messages: const [],
        answer: '506',
      );

      expect(reply.replyType, equals(TutorReplyType.question));
      expect(reply.text, contains('어느 자리에서 달라졌는지 하나씩 확인해 볼게요.'));
      expect(reply.text, isNot(contains('받아올림')));
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
      final messages = [
        prompt,
        service.student('두 가족이 캔 전체 수'),
      ];
      final feedback = await service.respondToStudent(
        content: content,
        messages: messages,
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
