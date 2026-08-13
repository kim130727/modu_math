import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/models/content_models.dart';
import 'package:modu_math_app/services/solvable_hint_service.dart';

void main() {
  const service = SolvableHintService();

  test('builds multiple-choice column addition hints by place value', () {
    final hints = service.buildHints(_columnAdditionContent);

    expect(hints, hasLength(4));
    expect(hints[0].title, equals('1단계: 일의 자리 더하기'));
    expect(hints[0].miniQuestion, equals('9 + 8은 얼마인가요?'));
    expect(_correctChoice(hints[0]), equals('17'));

    expect(hints[1].title, equals('2단계: 일의 자리 쓰기'));
    expect(hints[1].miniQuestion, equals('일의 자리에는 어떤 숫자를 쓰나요?'));
    expect(_correctChoice(hints[1]), equals('7'));

    expect(hints[2].title, equals('3단계: 십의 자리 더하기'));
    expect(hints[2].miniQuestion, equals('십의 자리 계산으로 알맞은 것은 무엇인가요?'));
    expect(_correctChoice(hints[2]), equals('5 + 4 + 1'));

    expect(hints[3].title, equals('4단계: 백의 자리와 답'));
    expect(hints[3].miniQuestion, equals('백의 자리까지 계산하면 알맞은 답은 무엇인가요?'));
    expect(_correctChoice(hints[3]), equals('507'));
  });

  test('uses elementary multiple-choice fallback hints', () {
    final hints = service.buildHints(_simpleContent);

    expect(hints, hasLength(4));
    expect(hints[0].miniQuestion, equals('무엇을 구하는 문제인가요?'));
    expect(hints[0].choices.map((choice) => choice.label), contains('전체 수'));
    expect(_correctChoice(hints[0]), equals('전체 수'));
    expect(hints[1].choices.map((choice) => choice.label), contains('더하기'));
  });

  test('keeps authored student hints when column addition cannot be detected',
      () {
    final hints = service.buildHints(_contentWithStudentHints);

    expect(hints, hasLength(2));
    expect(hints[0].title, equals('1단계: 문제 이해'));
    expect(hints[0].body, contains('전체를 구하는 문제예요.'));
    expect(hints[1].body, isNot(contains('507')));
  });
}

String _correctChoice(SolvableHint hint) {
  return hint.choices.singleWhere((choice) => choice.isCorrect).label;
}

const _summary = ProblemSummary(
  id: 'P-hint',
  grade: 3,
  subject: 'math',
  unit: 'addition',
  type: 'calc',
  title: '덧셈 문제',
  path: '',
  raw: {},
);

const _columnAdditionContent = ProblemContent(
  summary: _summary,
  semantic: {
    'metadata': {
      'question': '상현이네 259개와 용진이네 248개를 더해요.',
    },
  },
  solvable: {
    'method': 'vertical_addition_with_carry',
    'plan': '259 + 248을 일의 자리부터 더한다.',
    'answer': {'value': 507},
  },
);

const _simpleContent = ProblemContent(
  summary: _summary,
  semantic: {},
  solvable: {
    'target': {'text': '사과의 전체 개수'},
    'method': 'add_parts',
    'answer': {'value': 7},
  },
);

const _contentWithStudentHints = ProblemContent(
  summary: _summary,
  semantic: {},
  solvable: {
    'student_hints': [
      {
        'level': 1,
        'title': '1단계: 문제 이해',
        'text': '두 묶음을 모두 더해 전체를 구하는 문제예요.',
      },
      {
        'level': 2,
        'title': '2단계: 계산 방법',
        'text': '259와 248을 더해요. 답은 507이에요.',
      },
    ],
    'answer': {'value': 507},
  },
);
