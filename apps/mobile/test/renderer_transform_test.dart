import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/widgets/renderer_json_canvas.dart';

void main() {
  test('parses SVG translation and rotation transforms', () {
    final translated = rendererElementTransform(
      'translate(10, 20)',
      coordinateScale: 2,
    );
    expect(
      MatrixUtils.transformPoint(translated, const Offset(5, 10)),
      const Offset(25, 50),
    );

    final rotated = rendererElementTransform('rotate(90 10 10)');
    final rotatedPoint =
        MatrixUtils.transformPoint(rotated, const Offset(20, 10));
    expect(rotatedPoint.dx, closeTo(10, 0.0001));
    expect(rotatedPoint.dy, closeTo(20, 0.0001));
  });

  test('parses SVG matrix, scale, and skew transforms', () {
    final matrix = rendererElementTransform('matrix(1 0 0 1 12 8)');
    expect(
      MatrixUtils.transformPoint(matrix, const Offset(3, 4)),
      const Offset(15, 12),
    );

    final scaled = rendererElementTransform('scale(2 3)');
    expect(
      MatrixUtils.transformPoint(scaled, const Offset(3, 4)),
      const Offset(6, 12),
    );

    final skewed = rendererElementTransform('skewX(45)');
    final skewedPoint = MatrixUtils.transformPoint(skewed, const Offset(2, 3));
    expect(skewedPoint.dx, closeTo(5, 0.0001));
    expect(skewedPoint.dy, closeTo(3, 0.0001));
  });

  testWidgets('applies transforms to positioned text box layers',
      (tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: SizedBox(
            width: 200,
            height: 100,
            child: RendererJsonCanvas(
              renderer: {
                'view_box': {
                  'width': 200,
                  'height': 100,
                  'background': '#FFFFFF',
                },
                'elements': [
                  {
                    'type': 'text_box',
                    'attributes': {
                      'x': 10,
                      'y': 10,
                      'width': 100,
                      'height': 30,
                      'font-size': 18,
                      'transform': 'translate(1000 0)',
                    },
                    'text': 'off canvas',
                  },
                ],
              },
            ),
          ),
        ),
      ),
    );

    expect(tester.getTopLeft(find.text('off canvas')).dx, greaterThan(900));
    expect(tester.takeException(), isNull);
  });

  test('uses transformed bounds when filtering overlapping answer blanks', () {
    final visible = rendererVisibleElements([
      {
        'id': 'slot.question.text',
        'type': 'text_box',
        'attributes': {
          'x': 20,
          'y': 20,
          'width': 200,
          'height': 80,
          'transform': 'translate(1000 0)',
        },
        'text': 'hidden helper text',
      },
      {
        'id': 'slot.answer.blank.rect',
        'type': 'rect',
        'attributes': {
          'x': 40,
          'y': 40,
          'width': 80,
          'height': 30,
          'fill': '#ffffff',
          'stroke': '#111111',
        },
      },
    ]);

    expect(
      visible.map((element) => element['id']),
      ['slot.question.text', 'slot.answer.blank.rect'],
    );
  });
}
