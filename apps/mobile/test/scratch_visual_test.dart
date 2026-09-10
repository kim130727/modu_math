import 'dart:io';
import 'dart:convert';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/models/content_models.dart';
import 'package:modu_math_app/utils/problem_presentation.dart';
import 'package:modu_math_app/widgets/renderer_json_canvas.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test('scratch', () async {
    for (final loc in ['en', 'km']) {
      final layout = jsonDecode(File('../../examples/problems/$loc/S3_elem_3_008664.layout.json').readAsStringSync());
      final renderer = jsonDecode(File('../../examples/problems/$loc/S3_elem_3_008664.renderer.json').readAsStringSync());
      final semantic = jsonDecode(File('../../examples/problems/$loc/S3_elem_3_008664.semantic.json').readAsStringSync());
      final solvable = jsonDecode(File('../../examples/problems/$loc/S3_elem_3_008664.solvable.v1.1.json').readAsStringSync());
      final summary = ProblemSummary(
        id: 'S3_elem_3_008664',
        grade: 3,
        subject: 'math',
        unit: 'circle',
        type: 'choice_selection',
        title: semantic['metadata']?['title'] ?? 'test',
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
      debugPrint('=== LOCALE $loc ===');
      debugPrint('PROMPT: "${content.prompt}"');
      debugPrint('CHOICES: ${content.choices}');

      final originalTexts = (renderer['elements'] as List)
          .whereType<Map>()
          .where((e) => e['type'] == 'text')
          .map((e) => '${e["id"]}: "${e["text"]}"')
          .toList();
      debugPrint('ORIGINAL TEXTS: $originalTexts');

      final visual = problemVisualRenderer(content);
      final visualTexts = (visual['elements'] as List)
          .whereType<Map>()
          .where((e) => e['type'] == 'text')
          .map((e) => '${e["id"]}: "${e["text"]}"')
          .toList();
      debugPrint('VISUAL TEXTS: $visualTexts');

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
      File('test_circle_$loc.png').writeAsBytesSync(byteData!.buffer.asUint8List());
      debugPrint('WROTE test_circle_$loc.png, size: ${byteData.lengthInBytes}');
    }
  });
}
