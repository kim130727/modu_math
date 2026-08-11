import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/models/content_models.dart';
import 'package:modu_math_app/models/tutor_models.dart';
import 'package:modu_math_app/services/rule_tutor_service.dart';

void main() {
  group('RuleTutorService', () {
    test('uses solvable count values as expected step answers', () async {
      const service = RuleTutorService();
      final content = _additionContent();

      final messages = service.startSession(content);

      expect(messages.single.replyType, equals(TutorReplyType.question));
      expect(messages.single.text, contains('온셈이'));
      expect(messages.single.text, contains('1단계: 두 수를 모두 더해요.'));
      expect(messages.single.choices, contains('507'));

      final reply = await service.respondToStudent(
        content: content,
        messages: messages,
        message: '507',
        stepIndex: 0,
      );

      expect(reply.replyType, equals(TutorReplyType.correct));
      expect(reply.text, contains('정답은 507이에요.'));
    });

    test('infers addition place value feedback for unregistered wrong answer',
        () async {
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
      expect(reply.text, contains('이어 쓰면 안'));
      expect(reply.choices, contains('507'));
    });
  });
}

ProblemContent _additionContent() {
  return const ProblemContent(
    summary: ProblemSummary(
      id: 'P3_1_01_00040_00469',
      grade: 3,
      subject: 'math',
      unit: '1학기 1. 덧셈과 뺄셈',
      type: 'numeric_answer_addition_word_problem',
      title: '고구마 수 구하기',
      path: '',
      raw: {},
    ),
    svg: '<svg></svg>',
    semantic: {
      'metadata': {
        'question': '259개와 248개를 모두 더하면 몇 개인가요?',
      },
      'answer': {
        'value': 507,
        'unit': '개',
      },
    },
    solvable: {
      'method': '두 수를 덧셈으로 구한다',
      'steps': [
        {
          'id': 'step.add_counts',
          'goal': '두 수를 모두 더해요.',
          'expr': '259 + 248',
          'value': {
            'count': 507,
            'unit': '개',
            'ref': 'quantity.total',
          },
          'explanation': '259와 248을 더합니다.',
        },
      ],
      'answer': {
        'value': 507,
        'unit': '개',
      },
    },
  );
}
