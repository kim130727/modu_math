import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/widgets/renderer_json_canvas.dart';

void main() {
  testWidgets('answer font scales with the problem canvas', (tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: SizedBox(
            width: 600,
            height: 500,
            child: RendererJsonCanvas(renderer: _representativeRenderer),
          ),
        ),
      ),
    );

    final input = tester.widget<TextField>(find.byType(TextField));
    // 33.237 logical slot height × 0.84 × 2x canvas scale.
    expect(input.style?.fontSize, closeTo(55.84, 0.1));
    expect(input.style?.fontWeight, FontWeight.w700);
  });

  testWidgets('answer font shrinks together with a downscaled canvas',
      (tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: SizedBox(
            width: 150,
            height: 125,
            child: RendererJsonCanvas(renderer: _representativeRenderer),
          ),
        ),
      ),
    );

    final input = tester.widget<TextField>(find.byType(TextField));
    expect(input.style?.fontSize, closeTo(13.96, 0.1));
  });
}

const _representativeRenderer = <String, dynamic>{
  'view_box': {
    'width': 300,
    'height': 250,
    'background': '#FFFFFF',
  },
  'elements': [
    {
      'id': 'slot.answer.rect',
      'type': 'rect',
      'attributes': {
        'x': 106.238,
        'y': 174.665,
        'width': 92.919,
        'height': 33.237,
        'fill': '#ffffff',
        'stroke': '#111827',
      },
      'interaction': {
        'type': 'input',
        'role': 'answer',
        'value_type': 'integer',
        'max_length': 4,
      },
      'input_style': {
        'font_size': 32,
        'font_size_mode': 'auto',
        'font_weight': 700,
        'horizontal_align': 'center',
        'vertical_align': 'middle',
      },
    },
  ],
};
