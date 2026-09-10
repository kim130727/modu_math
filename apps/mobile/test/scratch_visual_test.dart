import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:modu_math_app/models/content_models.dart';
import 'package:modu_math_app/utils/problem_presentation.dart';
import 'package:modu_math_app/widgets/renderer_json_canvas.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  setUpAll(() {
    GoogleFonts.config.allowRuntimeFetching = false;
    for (final loc in ['en', 'km']) {
      final file = File('test_circle_$loc.png');
      if (file.existsSync()) {
        file.deleteSync();
      }
    }
  });

  testWidgets('renders circle problem visual canvas for en and km', (tester) async {
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

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: SizedBox(
              width: w,
              height: h,
              child: RendererJsonCanvas(
                renderer: visual,
              ),
            ),
          ),
        ),
      );
      expect(find.byType(RendererJsonCanvas), findsOneWidget);
    }
  });
}
