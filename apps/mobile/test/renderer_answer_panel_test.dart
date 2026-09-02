import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/models/content_models.dart';
import 'package:modu_math_app/widgets/answer_panel.dart';

void main() {
  testWidgets(
    'renderer answer slots replace choices and submit the unformatted draft',
    (tester) async {
      var submitted = '';

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: AnswerPanel(
              content: _rendererInputContent,
              answerDraft: '1613141436',
              isCorrect: null,
              onAnswerChanged: (_) {},
              onSubmit: (value) => submitted = value,
            ),
          ),
        ),
      );

      expect(_rendererInputContent.hasRendererAnswerInputs, isTrue);
      expect(_rendererInputContent.choices, isEmpty);
      expect(find.byType(ChoiceChip), findsNothing);
      expect(find.byType(TextField), findsNothing);
      expect(find.text('문제의 빈칸에 정답을 입력하세요'), findsOneWidget);
      expect(
        find.text('왼쪽 문제의 빈칸을 순서대로 입력한 뒤 정답을 확인하세요.'),
        findsOneWidget,
      );

      await tester.tap(find.byType(FilledButton));
      await tester.pump();

      expect(submitted, '1613141436');
    },
  );
}

const _rendererInputContent = ProblemContent(
  summary: ProblemSummary(
    id: 'P3_1_01_00040_02152_1',
    grade: 3,
    subject: 'math',
    unit: 'addition',
    type: 'multi_answer_base_ten_model_addition',
    title: '수 모형으로 알아보는 세 자리 수의 덧셈',
    path: '',
    raw: {},
  ),
  semantic: {},
  renderer: {
    'elements': [
      {
        'id': 'slot.answer.ones_to_tens.rect',
        'type': 'rect',
        'interaction': {
          'type': 'input',
          'role': 'answer',
          'order': 0,
        },
      },
    ],
  },
  solvable: {
    'answer': {
      'value': [1, 6, 1, 3, 1, 4, 1436],
      'answer_key': [
        {'slot_id': 'slot.answer.ones_to_tens', 'value': 1},
        {'slot_id': 'slot.answer.remaining_ones', 'value': 6},
        {'slot_id': 'slot.answer.tens_to_hundreds', 'value': 1},
        {'slot_id': 'slot.answer.remaining_tens', 'value': 3},
        {'slot_id': 'slot.answer.hundreds_to_thousands', 'value': 1},
        {'slot_id': 'slot.answer.remaining_hundreds', 'value': 4},
        {'slot_id': 'slot.answer.total_books', 'value': 1436},
      ],
    },
  },
);
