import 'dart:io';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/models/content_models.dart';
import 'package:modu_math_app/utils/problem_presentation.dart';
import 'package:modu_math_app/widgets/renderer_json_canvas.dart';

void main() {
  test('scratch', () {
    final layout = jsonDecode(File('../../examples/problems/ko/S3_elem_3_008732.layout.json').readAsStringSync());
    final renderer = jsonDecode(File('../../examples/problems/ko/S3_elem_3_008732.renderer.json').readAsStringSync());
    final semantic = jsonDecode(File('../../examples/problems/ko/S3_elem_3_008732.semantic.json').readAsStringSync());
    final solvable = jsonDecode(File('../../examples/problems/ko/S3_elem_3_008732.solvable.v1.1.json').readAsStringSync());
    final summary = ProblemSummary(
      id: 'S3_elem_3_008732',
      grade: 3,
      subject: 'math',
      unit: 'fraction',
      type: 'ox_choice',
      title: '사다리를 타고 내려가 도착한 곳이 참이면 ○표, 거짓이면 X표하세요.',
      path: '',
      raw: {},
    );
    final content = ProblemContent(
      summary: summary,
      layout: layout,
      renderer: renderer,
      semantic: semantic,
      solvable: solvable,
    );
    print('content.prompt: ${content.prompt}');
    print('content.choices: ${content.choices}');
    final visual = problemVisualRenderer(content);
    print('viewport: ${visual["presentation_viewport"]}');
    for (final el in visual['elements']) {
      print('${el["id"]} - ${el["text"]}');
    }
  });

  testWidgets('pump S3_elem_3_008732', (tester) async {
    final layout = jsonDecode(File('../../examples/problems/ko/S3_elem_3_008732.layout.json').readAsStringSync());
    final renderer = jsonDecode(File('../../examples/problems/ko/S3_elem_3_008732.renderer.json').readAsStringSync());
    final semantic = jsonDecode(File('../../examples/problems/ko/S3_elem_3_008732.semantic.json').readAsStringSync());
    final solvable = jsonDecode(File('../../examples/problems/ko/S3_elem_3_008732.solvable.v1.1.json').readAsStringSync());
    final summary = ProblemSummary(
      id: 'S3_elem_3_008732',
      grade: 3,
      subject: 'math',
      unit: 'fraction',
      type: 'ox_choice',
      title: '사다리를 타고 내려가 도착한 곳이 참이면 ○표, 거짓이면 X표하세요.',
      path: '',
      raw: {},
    );
    final content = ProblemContent(
      summary: summary,
      layout: layout,
      renderer: renderer,
      semantic: semantic,
      solvable: solvable,
    );
    final visual = problemVisualRenderer(content);

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: SizedBox(
            width: 800,
            height: 600,
            child: RendererJsonCanvas(
              renderer: visual,
            ),
          ),
        ),
      ),
    );
    await tester.pumpAndSettle();
    expect(tester.takeException(), isNull);
  });
}
