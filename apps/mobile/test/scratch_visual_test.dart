import 'dart:io';
import 'dart:convert';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:google_fonts/google_fonts.dart';
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
      if (el['type'] == 'text') {
        final a = el['attributes'] as Map;
        final rawText = el['text']?.toString() ?? '';
        final fontSize = (a['font-size'] as num?)?.toDouble() ?? 18.0;
        final x = (a['x'] as num?)?.toDouble() ?? 0.0;
        final y = (a['y'] as num?)?.toDouble() ?? 0.0;
        final anchor = a['text-anchor']?.toString();

        final painter = TextPainter(
          text: TextSpan(
            text: rawText,
            style: TextStyle(
              color: const Color(0xFF111111),
              fontSize: fontSize,
              fontWeight: FontWeight.w600,
              height: 1.25,
            ),
          ),
          textDirection: TextDirection.ltr,
        )..layout();

        final baseline = painter.computeDistanceToActualBaseline(TextBaseline.alphabetic);
        final offset = rendererTextPaintOffset(
          x: x,
          y: y,
          baseline: baseline,
          anchorWidth: painter.width,
          textAnchor: anchor,
        );
        print('TEXT [${el["id"]}] "$rawText": size=${painter.size}, baseline=$baseline, offset=$offset');
      }
    }
  });


  test('render to image', () async {
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
    final viewBox = visual['view_box'] as Map;
    final w = (viewBox['width'] as num).toDouble();
    final h = (viewBox['height'] as num).toDouble();

    final recorder = ui.PictureRecorder();
    final canvas = Canvas(recorder, Rect.fromLTWH(0, 0, w, h));
    final painter = RendererJsonPainter(
      renderer: visual,
      logicalSize: Size(w, h),
    );
    painter.paint(canvas, Size(w, h));
    final picture = recorder.endRecording();
    final img = await picture.toImage(w.toInt(), h.toInt());
    final byteData = await img.toByteData(format: ui.ImageByteFormat.png);
    File('test_ladder.png').writeAsBytesSync(byteData!.buffer.asUint8List());
    print('WROTE test_ladder.png, size: ${byteData.lengthInBytes}');
  });
}
