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
      print('=== LOCALE $loc ===');
      print('PROMPT: "${content.prompt}"');
      print('CHOICES: ${content.choices}');

      final originalTexts = (renderer['elements'] as List)
          .whereType<Map>()
          .where((e) => e['type'] == 'text')
          .map((e) => '${e["id"]}: "${e["text"]}"')
          .toList();
      print('ORIGINAL TEXTS: $originalTexts');

      final visual = problemVisualRenderer(content);
      final visualTexts = (visual['elements'] as List)
          .whereType<Map>()
          .where((e) => e['type'] == 'text')
          .map((e) => '${e["id"]}: "${e["text"]}"')
          .toList();
      print('VISUAL TEXTS: $visualTexts');
    }
  });


}
