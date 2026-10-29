import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/models/content_models.dart';
import 'package:modu_math_app/utils/problem_presentation.dart';
import 'package:modu_math_app/widgets/answer_panel.dart';

void main() {
  const sentence = '누름 못이 꽂힌 점에서 원 위의 한 점까지의 길이는 모두';
  final content = ProblemContent(
    summary: ProblemSummary.fromJson({'id': 'circle', 'type': 'choice'}),
    semantic: const {
      'metadata': {'question': '그림을 보고 알맞은 말을 선택하세요.'},
    },
    solvable: const {
      'answer': {
        'type': 'choice',
        'choices': ['같습니다', '다릅니다'],
        'value': '같습니다',
      },
    },
    layout: const {
      'slots': [
        {
          'id': 'slot.sentence',
          'kind': 'text_box',
          'content': {
            'text': sentence,
            'semantic_role': 'answer_prompt',
            'semantic_role_source': 'explicit',
          },
        },
      ],
    },
    renderer: const {
      'width': 500,
      'height': 500,
      'elements': [
        {
          'id': 'sentence.text',
          'source_ref': 'slot.sentence',
          'type': 'text',
          'text': sentence,
          'attributes': {'x': 0, 'y': 400},
        },
        {
          'id': 'circle',
          'type': 'circle',
          'attributes': {'cx': 100, 'cy': 100, 'r': 50},
        },
      ],
    },
  );

  test('projects the answer sentence out of the visual layer', () {
    expect(content.answerPrompt, sentence);
    expect(content.prompt, isNot(contains(sentence)));
    final visual = problemVisualRenderer(content);
    final elements = visual['elements'] as List;
    expect(elements.map((e) => e['id']), ['circle']);
    expect(content.renderer['elements'], hasLength(2));
    expect(content.correctAnswer, '같습니다');
  });

  testWidgets(
      'displays the sentence above choices and submits the selected answer',
      (tester) async {
    String? submitted;
    await tester.pumpWidget(MaterialApp(
      home: Scaffold(
        body: SingleChildScrollView(
          child: AnswerPanel(
            content: content,
            answerDraft: '',
            isCorrect: null,
            onAnswerChanged: (_) {},
            onSubmit: (value) => submitted = value,
          ),
        ),
      ),
    ));
    expect(find.text(sentence), findsOneWidget);
    final choice = find.byType(ChoiceChip).first;
    expect(tester.getTopLeft(find.text(sentence)).dy,
        lessThan(tester.getTopLeft(choice).dy));
    await tester.tap(choice);
    await tester.pump();
    await tester.ensureVisible(find.byType(FilledButton));
    await tester.tap(find.byType(FilledButton));
    await tester.pump();
    expect(submitted, contains('같습니다'));
    expect(tester.takeException(), isNull);
  });
}
