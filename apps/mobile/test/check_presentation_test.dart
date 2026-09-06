import 'dart:convert';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/models/content_models.dart';
import 'package:modu_math_app/utils/problem_presentation.dart';

void main() {
  final root = Directory('../../examples/problems');
  Map<String, dynamic> read(String path) => File(path).existsSync()
      ? jsonDecode(File(path).readAsStringSync()) as Map<String, dynamic>
      : <String, dynamic>{};
  ProblemContent load(String prefix) => ProblemContent(
        summary: ProblemSummary.fromJson({'id': prefix, 'type': 'choice'}),
        semantic: read('$prefix.semantic.json'),
        solvable: read(File('$prefix.solvable.v1.2.json').existsSync()
            ? '$prefix.solvable.v1.2.json'
            : '$prefix.solvable.v1.1.json'),
        renderer: read('$prefix.renderer.json'),
        layout: read('$prefix.layout.json'),
      );

  test('debug 008713 presentation in all locales', () {
    for (final loc in ['ko', 'en', 'uk', 'km', 'ja', 'zh']) {
      final content = load('${root.path}/$loc/S3_elem_3_008713');
      final visual = problemVisualRenderer(content);
      final elements = visual['elements'] as List;
      print('=== $loc ===');
      print('content.choices: ${content.choices}');
      print('viewport: ${visual['presentation_viewport']}');
      for (final el in elements) {
        if ('${el['id']}'.contains('option')) {
          print('  KEPT: ${el['id']} -> ${el['text']}');
        }
      }
    }
  });
}
