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

  test('positions svg text using baseline and text-anchor', () {
    expect(
      rendererTextPaintOffset(
        x: 120,
        y: 80,
        baseline: 18,
        anchorWidth: 42,
        textAnchor: null,
      ),
      equals(const Offset(120, 62)),
    );
    expect(
      rendererTextPaintOffset(
        x: 120,
        y: 80,
        baseline: 18,
        anchorWidth: 42,
        textAnchor: 'middle',
      ),
      equals(const Offset(99, 62)),
    );
    expect(
      rendererTextPaintOffset(
        x: 120,
        y: 80,
        baseline: 18,
        anchorWidth: 42,
        textAnchor: 'end',
      ),
      equals(const Offset(78, 62)),
    );
  });

  test('builds a closed path for polygon renderer elements', () {
    final path = rendererPolygonPath([
      [10, 20],
      [70, 20],
      [70, 80],
      [10, 80],
    ]);

    expect(path, isNotNull);
    expect(path!.getBounds(), equals(const Rect.fromLTWH(10, 20, 60, 60)));
  });

  test('hides legacy answer blank rectangles that overlap question text', () {
    final visible = rendererVisibleElements([
      {
        'id': 'slot.question.text',
        'type': 'text_box',
        'attributes': {
          'x': 24,
          'y': 24,
          'width': 407,
          'height': 149,
        },
        'text': 'word problem',
      },
      {
        'id': 'slot.answer.blank',
        'type': 'rect',
        'attributes': {
          'x': 64,
          'y': 56,
          'width': 120,
          'height': 32,
          'fill': '#ffffff',
          'stroke': '#111111',
        },
      },
    ]);

    expect(visible.map((element) => element['id']), ['slot.question.text']);
  });

  test('keeps answer blank rectangles outside question text', () {
    final visible = rendererVisibleElements([
      {
        'id': 'slot.question.text',
        'type': 'text_box',
        'attributes': {
          'x': 24,
          'y': 24,
          'width': 407,
          'height': 149,
        },
        'text': 'word problem',
      },
      {
        'id': 'slot.answer.blank',
        'type': 'rect',
        'attributes': {
          'x': 64,
          'y': 188,
          'width': 120,
          'height': 32,
          'fill': '#ffffff',
          'stroke': '#111111',
        },
      },
    ]);

    expect(
      visible.map((element) => element['id']),
      ['slot.question.text', 'slot.answer.blank'],
    );
  });

  testWidgets('renders path answer blanks as interactive slots',
      (tester) async {
    var value = '';

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: SizedBox(
            width: 365,
            height: 125,
            child: RendererJsonCanvas(
              inputValue: value,
              expectedAnswer: '12',
              onInputChanged: (next) => value = next,
              renderer: {
                'view_box': {
                  'width': 365,
                  'height': 125,
                  'background': '#FFFFFF',
                },
                'elements': [
                  {
                    'id': 'slot.answer_1_oval.path',
                    'type': 'path',
                    'attributes': {
                      'd':
                          'M 146 96 C 146 81 202 81 202 96 C 202 111 146 111 146 96 Z',
                      'stroke': '#111111',
                      'stroke-width': 1.2,
                      'fill': '#ffffff',
                    },
                    'interaction': {
                      'type': 'select',
                      'role': 'choice',
                      'value_type': 'digit',
                      'include_in_submission': true,
                      'order': 0,
                      'keyboard': 'number',
                    },
                  },
                  {
                    'id': 'slot.answer_2_oval.path',
                    'type': 'path',
                    'attributes': {
                      'd':
                          'M 270 96 C 270 81 326 81 326 96 C 326 111 270 111 270 96 Z',
                      'stroke': '#111111',
                      'stroke-width': 1.2,
                      'fill': '#ffffff',
                    },
                    'interaction': {
                      'type': 'select',
                      'role': 'choice',
                      'value_type': 'digit',
                      'include_in_submission': true,
                      'order': 1,
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

    expect(find.byType(TextField), findsNWidgets(2));

    await tester.enterText(find.byType(TextField).first, '1');
    await tester.enterText(find.byType(TextField).last, '2');

    expect(value, equals('12'));
    expect(tester.takeException(), isNull);
  });

  testWidgets('sizes multi-digit answer text to match surrounding problem text',
      (tester) async {
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: SizedBox(
            width: 365,
            height: 125,
            child: RendererJsonCanvas(
              inputValue: '434',
              expectedAnswer: '4341131',
              renderer: {
                'view_box': {
                  'width': 365,
                  'height': 125,
                  'background': '#FFFFFF',
                },
                'elements': [
                  {
                    'id': 'slot.answer_1_oval.path',
                    'type': 'path',
                    'attributes': {
                      'd':
                          'M 146 96 C 146 81 202 81 202 96 C 202 111 146 111 146 96 Z',
                      'stroke': '#111111',
                      'stroke-width': 1.2,
                      'fill': '#ffffff',
                    },
                    'interaction': {
                      'type': 'input',
                      'role': 'answer',
                      'value_type': 'integer',
                      'include_in_submission': true,
                      'order': 0,
                      'max_length': 4,
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

    final field = tester.widget<TextField>(find.byType(TextField));

    expect(field.style?.fontSize, lessThanOrEqualTo(18));
  });

  testWidgets('suppresses renderer input slots for choice problems',
      (tester) async {
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: SizedBox(
            width: 240,
            height: 160,
            child: RendererJsonCanvas(
              suppressInputs: true,
              renderer: {
                'view_box': {
                  'width': 240,
                  'height': 160,
                  'background': '#FFFFFF',
                },
                'elements': [
                  {
                    'id': 'slot.answer.rect',
                    'type': 'rect',
                    'attributes': {
                      'x': 40,
                      'y': 60,
                      'width': 80,
                      'height': 40,
                      'stroke': '#111111',
                      'fill': '#ffffff',
                    },
                    'interaction': {
                      'type': 'input',
                      'role': 'answer',
                      'include_in_submission': true,
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
  });

  testWidgets('fits height-constrained vertical canvas without overflow',
      (tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: Center(
            child: SizedBox(
              width: 600,
              height: 300,
              child: Card(
                margin: EdgeInsets.zero,
                child: Padding(
                  padding: EdgeInsets.all(12),
                  child: RendererJsonCanvas(
                    renderer: {
                      'view_box': {
                        'width': 300,
                        'height': 260,
                        'background': '#FFFFFF',
                      },
                      'elements': [
                        {
                          'type': 'text',
                          'attributes': {
                            'x': 25,
                            'y': 28,
                            'font-size': 24,
                            'fill': '#111111',
                          },
                          'text': '다음 계산을 하시오.',
                        },
                      ],
                    },
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );

    expect(find.byType(RendererJsonCanvas), findsOneWidget);
    expect(find.byType(CustomPaint), findsWidgets);
    expect(tester.takeException(), isNull);
  });

  testWidgets('ignores invisible slots with fill=none and stroke=none',
      (tester) async {
    final elements = [
      {
        'id': 'slot.answer_blank.rect',
        'type': 'rect',
        'attributes': {
          'x': 72.0,
          'y': 269.0,
          'width': 22.0,
          'height': 22.0,
          'fill': 'none',
          'stroke': 'none',
        },
      },
      {
        'id': 'slot.qtext.text',
        'type': 'text',
        'attributes': {
          'x': 100.0,
          'y': 50.0,
          'font-size': 20,
          'fill': '#111111',
        },
        'text': '원의 중심을 찾아 선택해 보세요.',
      },
    ];

    final visible = rendererVisibleElements(elements);
    expect(visible.length, 1);
    expect(visible.first['id'], 'slot.qtext.text');
  });

  testWidgets('allows inputting multi-digit partial sums 7, 90, 500, 597 for 15598_2', (tester) async {
    String emitted = '';

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: SizedBox(
            width: 350,
            height: 350,
            child: RendererJsonCanvas(
              onInputChanged: (value) => emitted = value,
              renderer: {
                'view_box': {'width': 350, 'height': 350, 'background': '#FFFFFF'},
                'elements': [
                  {
                    'id': 'slot.calculation.2.box.ones.rect',
                    'type': 'rect',
                    'attributes': {'x': 192.395, 'y': 169.077, 'width': 21.89, 'height': 27.0},
                    'interaction': {
                      'type': 'input',
                      'role': 'answer',
                      'value_type': 'digit',
                      'max_length': 1,
                      'include_in_submission': true,
                      'order': 0,
                    },
                  },
                  {
                    'id': 'slot.calculation.2.box.tens.rect',
                    'type': 'rect',
                    'attributes': {'x': 179.616, 'y': 210.077, 'width': 34.68, 'height': 27.0},
                    'interaction': {
                      'type': 'input',
                      'role': 'answer',
                      'value_type': 'integer',
                      'max_length': 2,
                      'include_in_submission': true,
                      'order': 1,
                    },
                  },
                  {
                    'id': 'slot.calculation.2.box.hundreds.rect',
                    'type': 'rect',
                    'attributes': {'x': 161.285, 'y': 251.077, 'width': 53.0, 'height': 27.0},
                    'interaction': {
                      'type': 'input',
                      'role': 'answer',
                      'value_type': 'integer',
                      'max_length': 3,
                      'include_in_submission': true,
                      'order': 2,
                    },
                  },
                  {
                    'id': 'slot.calculation.2.box.total.rect',
                    'type': 'rect',
                    'attributes': {'x': 159.064, 'y': 303.077, 'width': 55.22, 'height': 29.0},
                    'interaction': {
                      'type': 'input',
                      'role': 'answer',
                      'value_type': 'integer',
                      'max_length': 3,
                      'include_in_submission': true,
                      'order': 3,
                    },
                  },
                ],
              },
            ),
          ),
        ),
      ),
    );

    final textFields = find.byType(TextField);
    expect(textFields, findsNWidgets(4));

    await tester.enterText(textFields.at(0), '7');
    await tester.enterText(textFields.at(1), '90');
    await tester.enterText(textFields.at(2), '500');
    await tester.enterText(textFields.at(3), '597');
    await tester.pump();

    expect(emitted, equals('790500597'));
  });

  testWidgets('renders comparison operator buttons for P3_1_01_00040_15604', (tester) async {
    String emitted = '';

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: SizedBox(
            width: 500,
            height: 180,
            child: RendererJsonCanvas(
              expectedAnswer: '<',
              onInputChanged: (value) => emitted = value,
              renderer: {
                'view_box': {'width': 500, 'height': 180, 'background': '#FFFFFF'},
                'elements': [
                  {
                    'id': 'slot.comparison.circle.circle',
                    'type': 'circle',
                    'attributes': {'cx': 154.196, 'cy': 100.95, 'r': 16.0},
                    'interaction': {
                      'type': 'select',
                      'role': 'choice',
                      'value_type': 'comparison_operator',
                      'choice_value': 'slot.comparison.circle',
                      'include_in_submission': true,
                      'order': 0,
                    },
                  },
                ],
              },
            ),
          ),
        ),
      ),
    );

    expect(find.byKey(const ValueKey('operator-choice->')), findsOneWidget);
    expect(find.byKey(const ValueKey('operator-choice-=')), findsOneWidget);
    expect(find.byKey(const ValueKey('operator-choice-<')), findsOneWidget);

    await tester.tap(find.byKey(const ValueKey('operator-choice-<')));
    await tester.pump();

    expect(emitted, equals('<'));
  });

  testWidgets('renders comparison operator buttons for P3_1_01_00040_15610', (tester) async {
    String emitted = '';

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: SizedBox(
            width: 400,
            height: 180,
            child: RendererJsonCanvas(
              expectedAnswer: '>',
              onInputChanged: (value) => emitted = value,
              renderer: {
                'view_box': {'width': 400, 'height': 150, 'background': '#FFFFFF'},
                'elements': [
                  {
                    'id': 'slot.comparison.circle.circle',
                    'type': 'circle',
                    'attributes': {'cx': 203.458, 'cy': 81.614, 'r': 15.0},
                    'interaction': {
                      'type': 'select',
                      'role': 'choice',
                      'value_type': 'comparison_operator',
                      'choice_value': 'slot.comparison.circle',
                      'include_in_submission': true,
                      'order': 0,
                    },
                  },
                ],
              },
            ),
          ),
        ),
      ),
    );

    expect(find.byKey(const ValueKey('operator-choice->')), findsOneWidget);
    expect(find.byKey(const ValueKey('operator-choice-=')), findsOneWidget);
    expect(find.byKey(const ValueKey('operator-choice-<')), findsOneWidget);

    await tester.tap(find.byKey(const ValueKey('operator-choice->')));
    await tester.pump();

    expect(emitted, equals('>'));
  });

  testWidgets('creates input slots only for answer blanks and not number cards for P3_1_01_00040_15611', (tester) async {
    String emitted = '';

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: SizedBox(
            width: 500,
            height: 220,
            child: RendererJsonCanvas(
              onInputChanged: (value) => emitted = value,
              renderer: {
                'view_box': {'width': 500, 'height': 220, 'background': '#FFFFFF'},
                'elements': [
                  {
                    'id': 'slot.card1.rect.rect',
                    'type': 'rect',
                    'attributes': {'x': 22.0, 'y': 48.0, 'width': 28.0, 'height': 32.0, 'fill': '#ffffff', 'stroke': '#111111'},
                  },
                  {
                    'id': 'slot.card5.rect.rect',
                    'type': 'rect',
                    'attributes': {'x': 58.0, 'y': 48.0, 'width': 28.0, 'height': 32.0, 'fill': '#ffffff', 'stroke': '#111111'},
                  },
                  {
                    'id': 'slot.card2.rect.rect',
                    'type': 'rect',
                    'attributes': {'x': 94.0, 'y': 48.0, 'width': 28.0, 'height': 32.0, 'fill': '#ffffff', 'stroke': '#111111'},
                  },
                  {
                    'id': 'slot.card7.rect.rect',
                    'type': 'rect',
                    'attributes': {'x': 130.0, 'y': 48.0, 'width': 28.0, 'height': 32.0, 'fill': '#ffffff', 'stroke': '#111111'},
                  },
                  {
                    'id': 'slot.top.blank_tens.rect.rect',
                    'type': 'rect',
                    'attributes': {'x': 235.0, 'y': 48.0, 'width': 22.0, 'height': 28.0, 'fill': '#ffffff', 'stroke': '#111111'},
                    'interaction': {
                      'type': 'input',
                      'role': 'answer',
                      'value_type': 'digit',
                      'max_length': 1,
                      'include_in_submission': true,
                      'order': 0,
                    },
                  },
                  {
                    'id': 'slot.top.blank_ones.rect.rect',
                    'type': 'rect',
                    'attributes': {'x': 261.0, 'y': 48.0, 'width': 22.0, 'height': 28.0, 'fill': '#ffffff', 'stroke': '#111111'},
                    'interaction': {
                      'type': 'input',
                      'role': 'answer',
                      'value_type': 'digit',
                      'max_length': 1,
                      'include_in_submission': true,
                      'order': 1,
                    },
                  },
                  {
                    'id': 'slot.bottom.blank_hundreds.rect.rect',
                    'type': 'rect',
                    'attributes': {'x': 209.0, 'y': 84.0, 'width': 22.0, 'height': 28.0, 'fill': '#ffffff', 'stroke': '#111111'},
                    'interaction': {
                      'type': 'input',
                      'role': 'answer',
                      'value_type': 'digit',
                      'max_length': 1,
                      'include_in_submission': true,
                      'order': 2,
                    },
                  },
                  {
                    'id': 'slot.result.blank_ones.rect.rect',
                    'type': 'rect',
                    'attributes': {'x': 261.0, 'y': 128.0, 'width': 22.0, 'height': 28.0, 'fill': '#ffffff', 'stroke': '#111111'},
                    'interaction': {
                      'type': 'input',
                      'role': 'answer',
                      'value_type': 'digit',
                      'max_length': 1,
                      'include_in_submission': true,
                      'order': 3,
                    },
                  },
                ],
              },
            ),
          ),
        ),
      ),
    );

    final textFields = find.byType(TextField);
    expect(textFields, findsNWidgets(4));

    await tester.enterText(textFields.at(0), '5');
    await tester.enterText(textFields.at(1), '2');
    await tester.enterText(textFields.at(2), '1');
    await tester.enterText(textFields.at(3), '7');
    await tester.pump();

    expect(emitted, equals('5217'));
  });

  testWidgets('allows multi-digit inputs 60, 2, 90, 7, 697 for P3_1_01_00040_15621', (tester) async {
    String emitted = '';

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: SizedBox(
            width: 400,
            height: 120,
            child: RendererJsonCanvas(
              onInputChanged: (value) => emitted = value,
              renderer: {
                'view_box': {'width': 400.0, 'height': 107.746, 'background': '#FFFFFF'},
                'elements': [
                  {
                    'id': 'slot.line1.blank1_box.rect',
                    'type': 'rect',
                    'attributes': {'x': 160.4, 'y': 33.0, 'width': 47.6, 'height': 24.0, 'fill': '#ffffff'},
                    'interaction': {
                      'type': 'input',
                      'role': 'answer',
                      'value_type': 'integer',
                      'max_length': 2,
                      'include_in_submission': true,
                      'order': 0,
                    },
                  },
                  {
                    'id': 'slot.line1.blank2_box.rect',
                    'type': 'rect',
                    'attributes': {'x': 269.0, 'y': 33.0, 'width': 28.0, 'height': 24.0, 'fill': '#ffffff'},
                    'interaction': {
                      'type': 'input',
                      'role': 'answer',
                      'value_type': 'digit',
                      'max_length': 1,
                      'include_in_submission': true,
                      'order': 1,
                    },
                  },
                  {
                    'id': 'slot.line2.blank3_box.rect',
                    'type': 'rect',
                    'attributes': {'x': 117.0, 'y': 62.0, 'width': 37.0, 'height': 24.0, 'fill': '#ffffff'},
                    'interaction': {
                      'type': 'input',
                      'role': 'answer',
                      'value_type': 'integer',
                      'max_length': 2,
                      'include_in_submission': true,
                      'order': 2,
                    },
                  },
                  {
                    'id': 'slot.line2.blank4_box.rect',
                    'type': 'rect',
                    'attributes': {'x': 166.0, 'y': 62.0, 'width': 28.0, 'height': 24.0, 'fill': '#ffffff'},
                    'interaction': {
                      'type': 'input',
                      'role': 'answer',
                      'value_type': 'digit',
                      'max_length': 1,
                      'include_in_submission': true,
                      'order': 3,
                    },
                  },
                  {
                    'id': 'slot.line2.blank5_box.rect',
                    'type': 'rect',
                    'attributes': {'x': 205.0, 'y': 62.0, 'width': 42.0, 'height': 24.0, 'fill': '#ffffff'},
                    'interaction': {
                      'type': 'input',
                      'role': 'answer',
                      'value_type': 'integer',
                      'max_length': 3,
                      'include_in_submission': true,
                      'order': 4,
                    },
                  },
                ],
              },
            ),
          ),
        ),
      ),
    );

    final textFields = find.byType(TextField);
    expect(textFields, findsNWidgets(5));

    await tester.enterText(textFields.at(0), '60');
    await tester.enterText(textFields.at(1), '2');
    await tester.enterText(textFields.at(2), '90');
    await tester.enterText(textFields.at(3), '7');
    await tester.enterText(textFields.at(4), '697');
    await tester.pump();

    expect(emitted, equals('602907697'));
  });

  testWidgets('renders image elements from renderer json', (tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: SizedBox(
            width: 500,
            height: 300,
            child: RendererJsonCanvas(
              renderer: {
                'view_box': {
                  'width': 500,
                  'height': 300,
                  'background': '#FFFFFF',
                },
                'elements': [
                  {
                    'type': 'image',
                    'attributes': {
                      'x': 50,
                      'y': 50,
                      'width': 100,
                      'height': 100,
                      'href':
                          'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==',
                    },
                  },
                ],
              },
            ),
          ),
        ),
      ),
    );

    expect(find.byType(RendererJsonCanvas), findsOneWidget);
    expect(find.byType(Image), findsOneWidget);
  });
}
