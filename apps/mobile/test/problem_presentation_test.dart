import 'dart:convert';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:flutter/material.dart';
import 'package:modu_math_app/screens/problem_solve_screen.dart';
import 'package:modu_math_app/services/content_repository.dart';
import 'package:modu_math_app/widgets/renderer_json_canvas.dart';
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

  test('separates supplied multiplication example in every language', () {
    for (final locale in ['ko', 'en', 'ja', 'km', 'uk', 'zh']) {
      final content = load('${root.path}/$locale/S3_elem_3_008540');
      final before = jsonEncode(content.renderer);
      final visual = problemVisualRenderer(content);
      final elements = visual['elements'] as List;
      expect(elements.any((e) => e['id'] == 'slot.q1.text'), isFalse,
          reason: locale);
      expect(
          elements.any((e) => '${e['id']}'.startsWith('slot.choice')), isFalse,
          reason: locale);
      expect(elements.any((e) => e['id'] == 'slot.mul.highlight.rect'), isTrue);
      expect(elements.any((e) => e['text'] == '3   4   7   6'), isTrue);
      expect(visual['presentation_viewport'], isNotNull);
      expect(jsonEncode(content.renderer), before);
      expect(identical(problemVisualRenderer(content), visual), isTrue);
    }
  });

  test('keeps expression cards in ordering problem S3_elem_3_008541', () {
    for (final locale in ['ko', 'en', 'ja', 'km', 'uk', 'zh']) {
      final content = load('${root.path}/$locale/S3_elem_3_008541');
      final visual = problemVisualRenderer(content);
      final elements = visual['elements'] as List;
      expect(elements.any((e) => e['id'] == 'slot.box.rect'), isTrue);
      expect(elements.any((e) => e['id'] == 'slot.expr1.text'), isTrue,
          reason: 'expr1 should be visible in $locale');
      expect(elements.any((e) => e['id'] == 'slot.expr2.text'), isTrue,
          reason: 'expr2 should be visible in $locale');
    }
  });

  test('removes text choices from canvas for S3_elem_3_008661', () {
    for (final locale in ['ko', 'en', 'ja', 'km', 'uk', 'zh']) {
      final content = load('${root.path}/$locale/S3_elem_3_008661');
      final visual = problemVisualRenderer(content);
      final elements = visual['elements'] as List;
      // Diagram labels like ㄱ, ㄴ, etc. must remain
      expect(elements.any((e) => e['id'] == 'slot.lb.giyeok.text'), isTrue);
      // Choices like slot.opt1, slot.opt2, etc. must be removed from canvas
      expect(elements.any((e) => '${e['id']}'.contains('opt')), isFalse,
          reason: 'Choices should be removed from canvas in $locale');
    }
  });

  test('keeps diagram labels, visual choices, input boxes and unknown shapes',
      () {
    final content = ProblemContent(
      summary: ProblemSummary.fromJson({'id': 'future-problem'}),
      semantic: const {
        'metadata': {'question': 'Choose the matching figure.'}
      },
      solvable: const {
        'answer': {
          'choices': ['(1) A', '(2) B']
        }
      },
      renderer: const {
        'elements': [
          {
            'id': 'instruction',
            'type': 'text',
            'text': 'Choose the matching figure.'
          },
          {'id': 'diagram.label', 'type': 'text', 'text': '(1) A'},
          {
            'id': 'choice.figure',
            'type': 'path',
            'attributes': {'d': 'M0 0 L10 10'}
          },
          {'id': 'answer.blank', 'type': 'rect'},
        ],
      },
    );
    final visual = problemVisualRenderer(content);
    expect((visual['elements'] as List).map((e) => e['id']),
        containsAll(['diagram.label', 'choice.figure', 'answer.blank']));
    expect(visual['presentation_viewport'], isNull);
  });
  for (final width in [1200.0, 390.0]) {
    testWidgets('shows separated prompt and artwork at width $width',
        (tester) async {
      await tester.binding.setSurfaceSize(Size(width, 1000));
      addTearDown(() => tester.binding.setSurfaceSize(null));
      final content = load('${root.path}/ko/S3_elem_3_008540');
      await tester.pumpWidget(MaterialApp(
          home: ProblemSolveScreen(
        repository: _Repository(content),
        problem: content.summary,
      )));
      await tester.pumpAndSettle();
      expect(find.text(content.prompt), findsOneWidget);
      final canvas =
          tester.widget<RendererJsonCanvas>(find.byType(RendererJsonCanvas));
      expect(canvas.renderer, same(problemVisualRenderer(content)));
      expect(tester.takeException(), isNull);
    });
  }

  test('projects existing renderer corpus without mutating authored data', () {
    var checked = 0;
    for (final file in Directory('../../examples')
        .listSync(recursive: true)
        .whereType<File>()) {
      if (!file.path.endsWith('.renderer.json')) continue;
      final prefix =
          file.path.substring(0, file.path.length - '.renderer.json'.length);
      final content = load(prefix);
      final before = jsonEncode(content.renderer);
      final visual = problemVisualRenderer(content);
      expect(jsonEncode(content.renderer), before, reason: prefix);
      expect((visual['elements'] as List).length,
          lessThanOrEqualTo((content.renderer['elements'] as List).length));
      checked++;
    }
    expect(checked, greaterThan(100));
    // ignore: avoid_print
    print('Checked $checked authored renderers.');
  });
}

class _Repository extends ContentRepository {
  _Repository(this.content);
  final ProblemContent content;
  @override
  Future<ProblemContent> loadProblem(ProblemSummary summary) async => content;
}
