import 'dart:convert';

import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';
import 'package:modu_math_app/models/content_models.dart';
import 'package:modu_math_app/services/content_repository.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('ContentRepository', () {
    test('discovers bundled grade 3 problem assets', () async {
      final repository = ContentRepository();

      final manifest = await repository.loadManifest();

      expect(manifest.problems, isNotEmpty);
      expect(manifest.problems.first.id, isNotEmpty);
      expect(
        manifest.problems.first.path,
        startsWith(ContentRepository.problemsPath),
      );
    });

    test('loads a discovered problem through json renderer and solvable files',
        () async {
      final repository = ContentRepository();
      final manifest = await repository.loadManifest();

      final content = await repository.loadProblem(manifest.problems.first);

      expect(content.semantic, isNotEmpty);
      expect(content.renderer, isNotEmpty);
      expect(content.solvable, isNotEmpty);
      expect(content.correctAnswer, isNotEmpty);
    });

    test('loads the first renderer prefix as a JSON preview bundle', () async {
      final repository = ContentRepository();

      final prefixes = await repository.loadGrade3JsonProblemPrefixes();
      expect(prefixes, isNotEmpty);

      final bundle = await repository.loadProblemJsonBundle(prefixes.first);

      expect(bundle.filePrefix, equals(prefixes.first));
      expect(bundle.semantic, isNotEmpty);
      expect(bundle.layout, isNotEmpty);
      expect(bundle.renderer, isNotEmpty);
    });

    test('loads Ukrainian files from a Korean summary after locale switch',
        () async {
      final repository = ContentRepository()..activeProblemLocale = 'uk';
      final koreanSummary = _summaryWithPrefix('P3_1_01_00040_00469_ko');

      final content = await repository.loadProblem(koreanSummary);

      expect(
        content.semantic['metadata']['title'],
        equals('Скільки бататів зібрали дві родини?'),
      );
      expect(content.summary.filePrefix, equals('P3_1_01_00040_00469_ko'));
    });

    test('loads Korean files from a suffixed localized summary', () async {
      final repository = ContentRepository()..activeProblemLocale = 'ko';
      final ukrainianSummary = _summaryWithPrefix('P3_1_01_00040_00469_uk');

      final content = await repository.loadProblem(ukrainianSummary);

      expect(
        content.semantic['metadata']['title'],
        equals('두 가족이 캔 고구마의 수'),
      );
      expect(content.summary.filePrefix, equals('P3_1_01_00040_00469_uk'));
    });

    test('loads GitHub examples problem list and files from raw URLs',
        () async {
      final repository = ContentRepository.githubExamples(
        httpClient: MockClient((request) async {
          final url = request.url.toString();
          if (url.contains('/git/trees/main')) {
            return http.Response(
              '''
              {
                "tree": [
                  {
                    "path": "examples/problems/P3_1_01_00040_00469.renderer.json",
                    "type": "blob"
                  }
                ]
              }
              ''',
              200,
            );
          }
          if (url.endsWith('P3_1_01_00040_00469.semantic.json')) {
            return http.Response.bytes(
              utf8.encode('''
              {
                "metadata": {
                  "title": "두 가족이 캔 고구마의 수",
                  "question": "모두 몇 개입니까?"
                },
                "answer": {"value": 507}
              }
              '''),
              200,
            );
          }
          if (url.endsWith('P3_1_01_00040_00469.renderer.json')) {
            return http.Response(
              '{"view_box": {"width": 928, "height": 426}, "elements": []}',
              200,
            );
          }
          if (url.endsWith('P3_1_01_00040_00469.layout.json')) {
            return http.Response('{"layout": "ok"}', 200);
          }
          if (url.endsWith('P3_1_01_00040_00469.solvable.v1.2.json')) {
            return http.Response('{"answer": {"value": 507}}', 200);
          }
          if (url.endsWith('P3_1_01_00040_00469.svg')) {
            return http.Response('<svg></svg>', 200);
          }
          return http.Response('Not found', 404);
        }),
      );

      final manifest = await repository.loadManifest();
      final content = await repository.loadProblem(manifest.problems.single);

      expect(manifest.problems.single.path, equals('examples/problems'));
      expect(content.semantic, isNotEmpty);
      expect(content.renderer, isNotEmpty);
      expect(content.correctAnswer, equals('507'));
    });

    test('normalizes list answers into submission order text', () async {
      const summary = ProblemSummary(
        id: 'list-answer',
        grade: 3,
        subject: 'math',
        unit: 'unit',
        type: 'type',
        title: 'title',
        path: 'assets/content/problems',
        raw: {},
      );

      const operatorContent = ProblemContent(
        summary: summary,
        semantic: {},
        renderer: {},
        solvable: {
          'answer': {
            'value': ['>', '='],
          },
        },
      );
      const digitContent = ProblemContent(
        summary: summary,
        semantic: {},
        renderer: {},
        solvable: {
          'answer': {
            'value': [1, 1, 9, 2, 1],
          },
        },
      );

      expect(operatorContent.correctAnswer, equals('>='));
      expect(digitContent.correctAnswer, equals('11921'));
    });
  });
}

ProblemSummary _summaryWithPrefix(String filePrefix) {
  return ProblemSummary(
    id: filePrefix,
    grade: 3,
    subject: 'math',
    unit: '1학기 1. 덧셈과 뺄셈',
    type: 'local_json_problem',
    title: '덧셈과 뺄셈 문제',
    path: '${ContentRepository.problemsPath}/ko',
    filePrefix: filePrefix,
    raw: {
      'filePrefix': filePrefix,
    },
  );
}
