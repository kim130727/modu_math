import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/widgets/problem_canvas.dart';
import 'package:modu_math_app/widgets/renderer_json_canvas.dart';

void main() {
  const renderer = <String, dynamic>{
    'view_box': {'width': 928, 'height': 426},
    'presentation_viewport': {'x': 100, 'y': 100, 'width': 400, 'height': 120},
    'elements': <dynamic>[],
  };

  testWidgets('compact artwork uses its aspect ratio within a readable width',
      (tester) async {
    addTearDown(() => tester.binding.setSurfaceSize(null));
    for (final screenWidth in [1440.0, 390.0]) {
      await tester.binding.setSurfaceSize(Size(screenWidth, 900));
      await tester.pumpWidget(const MaterialApp(
        home: Scaffold(
          body: SingleChildScrollView(
            padding: EdgeInsets.all(24),
            child: ProblemCanvas(renderer: renderer),
          ),
        ),
      ));
      await tester.pump();
      final size = tester.getSize(find.byType(RendererJsonCanvas));
      final expectedWidth = screenWidth == 1440 ? 960.0 : 342.0;
      expect(size.width, expectedWidth);
      expect(size.height, closeTo(expectedWidth * 120 / 400, 0.1));
      expect(tester.takeException(), isNull);
    }
  });

  testWidgets('tall artwork is contained without an oversized scroll area',
      (tester) async {
    await tester.pumpWidget(MaterialApp(
      home: Scaffold(
        body: SingleChildScrollView(
          child: ProblemCanvas(renderer: {
            ...renderer,
            'presentation_viewport': {
              'x': 0,
              'y': 0,
              'width': 200,
              'height': 1000,
            },
          }),
        ),
      ),
    ));
    expect(tester.getSize(find.byType(RendererJsonCanvas)).height, 420);
    expect(tester.takeException(), isNull);
  });
}
