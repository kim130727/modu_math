// ignore_for_file: prefer_const_literals_to_create_immutables, unnecessary_const

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/widgets/renderer_json_canvas.dart';

void main() {
  testWidgets('renders text_box elements from renderer json', (tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: SizedBox(
            width: 500,
            height: 220,
            child: RendererJsonCanvas(
              renderer: {
                'view_box': {
                  'width': 500,
                  'height': 220,
                  'background': '#FFFFFF',
                },
                'elements': [
                  {
                    'type': 'text_box',
                    'attributes': {
                      'x': 20,
                      'y': 20,
                      'width': 460,
                      'height': 120,
                      'fill': '#202124',
                      'font-size': 24,
                      'data-text-align': 'left',
                      'data-vertical-align': 'top',
                      'data-line-height': 1.45,
                    },
                    'text': 'problem text',
                  },
                ],
              },
            ),
          ),
        ),
      ),
    );

    expect(find.byType(RendererJsonCanvas), findsOneWidget);
    expect(find.text('problem text'), findsOneWidget);
    expect(
      tester.widget<Text>(find.text('problem text')).style?.fontFamily,
      contains('PoorStory'),
    );
    expect(tester.takeException(), isNull);
  });

  testWidgets('overlays input fields on empty square rects', (tester) async {
    var value = '';

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: SizedBox(
            width: 240,
            height: 120,
            child: RendererJsonCanvas(
              inputValue: value,
              onInputChanged: (next) => value = next,
              renderer: const {
                'view_box': {
                  'width': 240,
                  'height': 120,
                  'background': '#FFFFFF',
                },
                'elements': [
                  {
                    'id': 'slot.answer.1.rect',
                    'type': 'rect',
                    'attributes': {
                      'x': 20,
                      'y': 30,
                      'width': 40,
                      'height': 40,
                      'fill': 'none',
                      'stroke': '#202124',
                      'stroke-width': 2,
                    },
                  },
                  {
                    'id': 'slot.answer.2.rect',
                    'type': 'rect',
                    'attributes': {
                      'x': 70,
                      'y': 30,
                      'width': 40,
                      'height': 40,
                      'fill': 'none',
                      'stroke': '#202124',
                      'stroke-width': 2,
                    },
                  },
                ],
              },
            ),
          ),
        ),
      ),
    );

    expect(find.byType(TextField), findsNWidgets(2));

    await tester.enterText(find.byType(TextField).first, '8');
    await tester.enterText(find.byType(TextField).last, '1');

    expect(value, equals('81'));
    expect(tester.takeException(), isNull);
  });

  testWidgets('uses explicit input interaction for rectangular answer fields',
      (tester) async {
    var value = '';
    const renderer = {
      'view_box': {
        'width': 300,
        'height': 120,
        'background': '#FFFFFF',
      },
      'elements': [
        {
          'id': 'answer_box.rect',
          'type': 'rect',
          'attributes': {
            'x': 40,
            'y': 40,
            'width': 80,
            'height': 42,
            'fill': '#ffffff',
            'stroke': '#111827',
            'stroke-width': 1.2,
          },
          'interaction': {
            'type': 'input',
            'role': 'answer',
            'value_type': 'digit',
            'max_length': 3,
            'include_in_submission': true,
            'keyboard': 'number',
          },
        },
      ],
    };

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: SizedBox(
            width: 300,
            height: 120,
            child: RendererJsonCanvas(
              inputValue: value,
              onInputChanged: (next) => value = next,
              renderer: renderer,
            ),
          ),
        ),
      ),
    );

    expect(find.byType(TextField), findsOneWidget);

    await tester.enterText(find.byType(TextField), '507');

    expect(value, equals('507'));

    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: SizedBox(
            width: 300,
            height: 120,
            child: RendererJsonCanvas(
              inputValue: '507',
              renderer: renderer,
            ),
          ),
        ),
      ),
    );

    expect(find.widgetWithText(TextField, '507'), findsOneWidget);
    expect(tester.takeException(), isNull);
  });

  testWidgets('uses expected answer length for one answer slot without max',
      (tester) async {
    var value = '';

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: SizedBox(
            width: 300,
            height: 120,
            child: RendererJsonCanvas(
              inputValue: value,
              expectedAnswer: '507',
              onInputChanged: (next) => value = next,
              renderer: const {
                'view_box': const {
                  'width': 300,
                  'height': 120,
                  'background': '#FFFFFF',
                },
                'elements': [
                  {
                    'id': 'answer_box.rect',
                    'type': 'rect',
                    'attributes': {
                      'x': 40,
                      'y': 40,
                      'width': 80,
                      'height': 42,
                      'fill': '#ffffff',
                      'stroke': '#111827',
                      'stroke-width': 1.2,
                    },
                    'interaction': {
                      'type': 'input',
                      'role': 'answer',
                      'value_type': 'digit',
                      'include_in_submission': true,
                      'keyboard': 'number',
                    },
                  },
                ],
              },
            ),
          ),
        ),
      ),
    );

    await tester.enterText(find.byType(TextField), '507');

    expect(value, equals('507'));
    expect(find.widgetWithText(TextField, '507'), findsOneWidget);
    expect(tester.takeException(), isNull);
  });

  testWidgets('expands wide answer slots for multi-answer number groups',
      (tester) async {
    var value = '';

    Map<String, Object?> answerBox({
      required double x,
      required int order,
    }) {
      return {
        'type': 'rect',
        'attributes': {
          'x': x,
          'y': 60,
          'width': 84,
          'height': 34,
          'fill': '#ffffff',
          'stroke': '#111827',
        },
        'interaction': {
          'type': 'input',
          'role': 'answer',
          'value_type': 'digit',
          'max_length': 1,
          'include_in_submission': true,
          'order': order,
          'keyboard': 'number',
        },
      };
    }

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: SizedBox(
            width: 360,
            height: 140,
            child: RendererJsonCanvas(
              inputValue: value,
              expectedAnswer: '724841823',
              onInputChanged: (next) => value = next,
              renderer: {
                'view_box': {
                  'width': 360,
                  'height': 140,
                  'background': '#FFFFFF',
                },
                'elements': [
                  answerBox(x: 32, order: 0),
                  answerBox(x: 138, order: 1),
                  answerBox(x: 244, order: 2),
                ],
              },
            ),
          ),
        ),
      ),
    );

    await tester.enterText(find.byType(TextField).first, '724');

    expect(value, equals('724'));
    expect(find.widgetWithText(TextField, '724'), findsOneWidget);
    expect(tester.takeException(), isNull);
  });

  testWidgets('supports operator choice buttons on text box slots',
      (tester) async {
    var value = '';

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: SizedBox(
            width: 260,
            height: 220,
            child: RendererJsonCanvas(
              inputValue: value,
              onInputChanged: (next) => value = next,
              renderer: const {
                'view_box': {
                  'width': 260,
                  'height': 120,
                  'background': '#FFFFFF',
                },
                'elements': [
                  {
                    'id': 'slot.problem_2_blank.text',
                    'type': 'text_box',
                    'attributes': {
                      'x': 40,
                      'y': 40,
                      'width': 44,
                      'height': 40,
                    },
                    'text': '○',
                    'interaction': {
                      'type': 'input',
                      'role': 'answer',
                      'value_type': 'operator',
                      'max_length': 1,
                      'include_in_submission': true,
                      'order': 1,
                      'group_id': 'final_answer',
                      'auto_advance': true,
                      'keyboard': 'operator',
                    },
                  },
                  {
                    'id': 'slot.problem_1_blank.text',
                    'type': 'text_box',
                    'attributes': {
                      'x': 100,
                      'y': 40,
                      'width': 44,
                      'height': 40,
                    },
                    'text': '○',
                    'interaction': {
                      'type': 'input',
                      'role': 'answer',
                      'value_type': 'operator',
                      'max_length': 1,
                      'include_in_submission': true,
                      'order': 0,
                      'group_id': 'final_answer',
                      'auto_advance': true,
                      'keyboard': 'operator',
                    },
                  },
                ],
              },
            ),
          ),
        ),
      ),
    );

    expect(find.byType(TextField), findsNothing);
    expect(find.byKey(const ValueKey('operator-choice->')), findsOneWidget);
    expect(find.byKey(const ValueKey('operator-choice-=')), findsOneWidget);
    expect(find.byKey(const ValueKey('operator-choice-<')), findsOneWidget);
    expect(find.text('○'), findsNWidgets(2));

    await tester.tap(find.byKey(const ValueKey('operator-choice-=')));
    await tester.pump();
    await tester.tap(find.byKey(const ValueKey('operator-choice->')));
    await tester.pump();

    expect(value, equals('=>'));
    expect(find.text('○'), findsNWidgets(2));
    expect(tester.takeException(), isNull);
  });

  testWidgets('supports operator choice buttons on answer circle slots',
      (tester) async {
    var value = '';

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: SizedBox(
            width: 300,
            height: 220,
            child: RendererJsonCanvas(
              inputValue: value,
              expectedAnswer: '>=',
              onInputChanged: (next) => value = next,
              renderer: const {
                'view_box': {
                  'width': 300,
                  'height': 120,
                  'background': '#FFFFFF',
                },
                'elements': [
                  {
                    'id': 'slot.compare_1.circle',
                    'type': 'circle',
                    'attributes': {
                      'cx': 100,
                      'cy': 62,
                      'r': 22,
                      'stroke': '#111827',
                      'fill': '#ffffff',
                    },
                    'source_ref': 'slot.compare_1',
                    'interaction': {
                      'type': 'select',
                      'role': 'choice',
                      'value_type': 'choice',
                      'include_in_submission': true,
                      'order': 0,
                    },
                  },
                  {
                    'id': 'slot.compare_2.circle',
                    'type': 'circle',
                    'attributes': {
                      'cx': 190,
                      'cy': 62,
                      'r': 22,
                      'stroke': '#111827',
                      'fill': '#ffffff',
                    },
                    'source_ref': 'slot.compare_2',
                    'interaction': {
                      'type': 'select',
                      'role': 'choice',
                      'value_type': 'choice',
                      'include_in_submission': true,
                      'order': 1,
                    },
                  },
                ],
              },
            ),
          ),
        ),
      ),
    );

    expect(find.byType(TextField), findsNothing);
    expect(find.byKey(const ValueKey('operator-slot-0')), findsOneWidget);
    expect(find.byKey(const ValueKey('operator-slot-1')), findsOneWidget);
    expect(find.byKey(const ValueKey('operator-choice->')), findsOneWidget);

    await tester.tap(find.byKey(const ValueKey('operator-choice->')));
    await tester.pump();
    await tester.tap(find.byKey(const ValueKey('operator-choice-=')));
    await tester.pump();

    expect(value, equals('>='));
    expect(find.text('>'), findsWidgets);
    expect(find.text('='), findsWidgets);
    expect(tester.takeException(), isNull);
  });

  testWidgets('keeps input in the clicked ordered slot after parent rebuild',
      (tester) async {
    var value = '';

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: StatefulBuilder(
            builder: (context, setState) {
              return SizedBox(
                width: 260,
                height: 140,
                child: RendererJsonCanvas(
                  inputValue: value,
                  onInputChanged: (next) => setState(() => value = next),
                  renderer: const {
                    'view_box': {
                      'width': 260,
                      'height': 140,
                      'background': '#FFFFFF',
                    },
                    'elements': [
                      {
                        'id': 'carry_hundreds.rect',
                        'type': 'rect',
                        'attributes': {
                          'x': 60,
                          'y': 20,
                          'width': 28,
                          'height': 28,
                          'fill': '#ffffff',
                          'stroke': '#111827',
                        },
                        'interaction': {
                          'type': 'input',
                          'role': 'answer',
                          'value_type': 'digit',
                          'max_length': 1,
                          'include_in_submission': true,
                          'order': 0,
                          'keyboard': 'number',
                        },
                      },
                      {
                        'id': 'carry_tens.rect',
                        'type': 'rect',
                        'attributes': {
                          'x': 92,
                          'y': 20,
                          'width': 28,
                          'height': 28,
                          'fill': '#ffffff',
                          'stroke': '#111827',
                        },
                        'interaction': {
                          'type': 'input',
                          'role': 'answer',
                          'value_type': 'digit',
                          'max_length': 1,
                          'include_in_submission': true,
                          'order': 1,
                          'keyboard': 'number',
                        },
                      },
                      {
                        'id': 'answer_hundreds.rect',
                        'type': 'rect',
                        'attributes': {
                          'x': 60,
                          'y': 80,
                          'width': 28,
                          'height': 28,
                          'fill': '#ffffff',
                          'stroke': '#111827',
                        },
                        'interaction': {
                          'type': 'input',
                          'role': 'answer',
                          'value_type': 'digit',
                          'max_length': 1,
                          'include_in_submission': true,
                          'order': 2,
                          'keyboard': 'number',
                        },
                      },
                    ],
                  },
                ),
              );
            },
          ),
        ),
      ),
    );

    await tester.enterText(find.byType(TextField).at(2), '9');
    await tester.pump();

    expect(value, equals('9'));
    expect(find.widgetWithText(TextField, '9'), findsOneWidget);
    expect(
      tester.widget<TextField>(find.byType(TextField).at(0)).controller?.text,
      isEmpty,
    );
    expect(
      tester.widget<TextField>(find.byType(TextField).at(2)).controller?.text,
      equals('9'),
    );
    expect(tester.takeException(), isNull);
  });

  testWidgets('syncs only answer slots when carry slots are editable',
      (tester) async {
    var value = '';

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: SizedBox(
            width: 260,
            height: 180,
            child: RendererJsonCanvas(
              inputValue: value,
              onInputChanged: (next) => value = next,
              renderer: const {
                'view_box': {
                  'width': 260,
                  'height': 180,
                  'background': '#FFFFFF',
                },
                'elements': [
                  {
                    'id': 'slot.instruction.text',
                    'type': 'text_box',
                    'attributes': {
                      'x': 10,
                      'y': 10,
                      'width': 200,
                      'height': 40,
                    },
                    'source_ref': 'slot.instruction',
                    'text': '□ 안에 알맞은 수를 써넣으시오.',
                  },
                  {
                    'id': 'slot.carry_tens.text',
                    'type': 'text_box',
                    'attributes': {
                      'x': 40,
                      'y': 60,
                      'width': 34,
                      'height': 44,
                    },
                    'source_ref': 'slot.carry_tens',
                    'text': '□',
                  },
                  {
                    'id': 'slot.answer_tens.text',
                    'type': 'text_box',
                    'attributes': {
                      'x': 40,
                      'y': 115,
                      'width': 34,
                      'height': 44,
                    },
                    'source_ref': 'slot.answer_tens',
                    'text': '□',
                  },
                  {
                    'id': 'slot.answer_ones.text',
                    'type': 'text_box',
                    'attributes': {
                      'x': 82,
                      'y': 115,
                      'width': 34,
                      'height': 44,
                    },
                    'source_ref': 'slot.answer_ones',
                    'text': '□',
                  },
                ],
              },
            ),
          ),
        ),
      ),
    );

    expect(find.byType(TextField), findsNWidgets(3));

    await tester.enterText(find.byType(TextField).at(0), '1');
    await tester.enterText(find.byType(TextField).at(1), '8');
    await tester.enterText(find.byType(TextField).at(2), '3');

    expect(value, equals('83'));
    expect(find.textContaining('알맞은 수'), findsOneWidget);
    expect(tester.takeException(), isNull);
  });
  testWidgets('orders duplicated-order slots by visual problem groups',
      (tester) async {
    var value = '';
    Map<String, Object?> slot({
      required double x,
      required double y,
    }) {
      return {
        'type': 'rect',
        'attributes': {
          'x': x,
          'y': y,
          'width': 28,
          'height': 28,
          'fill': '#ffffff',
          'stroke': '#111827',
        },
        'interaction': {
          'type': 'input',
          'role': 'answer',
          'value_type': 'digit',
          'max_length': 1,
          'include_in_submission': true,
          'order': 9,
          'keyboard': 'number',
        },
      };
    }

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: SizedBox(
            width: 520,
            height: 220,
            child: RendererJsonCanvas(
              inputValue: value,
              onInputChanged: (next) => value = next,
              renderer: {
                'view_box': {
                  'width': 520,
                  'height': 220,
                  'background': '#FFFFFF',
                },
                'elements': [
                  slot(x: 100, y: 40),
                  slot(x: 132, y: 40),
                  slot(x: 68, y: 120),
                  slot(x: 100, y: 120),
                  slot(x: 132, y: 120),
                  slot(x: 164, y: 120),
                  slot(x: 360, y: 40),
                  slot(x: 392, y: 40),
                  slot(x: 328, y: 120),
                  slot(x: 360, y: 120),
                  slot(x: 392, y: 120),
                  slot(x: 424, y: 120),
                ],
              },
            ),
          ),
        ),
      ),
    );

    const digits = [
      '1',
      '1',
      '1',
      '3',
      '0',
      '4',
      '1',
      '1',
      '1',
      '0',
      '2',
      '6',
    ];
    for (var index = 0; index < digits.length; index += 1) {
      await tester.enterText(find.byType(TextField).at(index), digits[index]);
    }

    expect(value, equals('111304111026'));
    expect(tester.takeException(), isNull);
  });
}
