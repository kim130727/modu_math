import 'dart:convert';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';
import 'package:modu_math_app/models/content_models.dart';
import 'package:modu_math_app/services/content_repository.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('ContentRepository', () {
    test('discovers bundled grade 3 problem assets', () async {
      final repository = ContentRepository.bundledAssets();

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
      final repository = ContentRepository.bundledAssets();
      final manifest = await repository.loadManifest();

      final content = await repository.loadProblem(manifest.problems.first);

      expect(content.semantic, isNotEmpty);
      expect(content.renderer, isNotEmpty);
      expect(content.solvable, isNotEmpty);
      expect(content.correctAnswer, isNotEmpty);
    });

    test('extracts duplicate slot answer key maps as one final answer',
        () async {
      final repository = ContentRepository.bundledAssets();
      final summary = _summaryWithPrefix('P3_1_01_00040_00469');

      final content = await repository.loadProblem(summary);

      expect(content.correctAnswer, equals('507'));
    });

    test('loads the first renderer prefix as a JSON preview bundle', () async {
      final repository = ContentRepository.bundledAssets();

      final prefixes = await repository.loadGrade3JsonProblemPrefixes();
      expect(prefixes, isNotEmpty);

      final bundle = await repository.loadProblemJsonBundle(prefixes.first);

      expect(bundle.filePrefix, equals(prefixes.first));
      expect(bundle.semantic, isNotEmpty);
      expect(bundle.layout, isNotEmpty);
      expect(bundle.renderer, isNotEmpty);
    });

    test('loads active locale files when localized examples exist', () async {
      final repository = ContentRepository.bundledAssets()
        ..activeProblemLocale = 'uk';
      final koreanSummary = _summaryWithPrefix('P3_1_01_00040_00469_ko');

      final content = await repository.loadProblem(koreanSummary);

      expect(
        content.semantic['metadata']['language'],
        equals('uk-UA'),
      );
      expect(content.summary.filePrefix, equals('P3_1_01_00040_00469_ko'));
    });

    test('falls back to base Korean files from a suffixed localized summary',
        () async {
      final repository = ContentRepository.bundledAssets()
        ..activeProblemLocale = 'ko';
      final ukrainianSummary = _summaryWithPrefix('P3_1_01_00040_00469_uk');

      final content = await repository.loadProblem(ukrainianSummary);

      expect(
        content.semantic['metadata']['language'],
        equals('ko-KR'),
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

    test('loads local examples problem list and files from disk', () async {
      final tempDir = await Directory.systemTemp.createTemp(
        'modu_math_problem_test_',
      );
      addTearDown(() async {
        if (await tempDir.exists()) {
          await tempDir.delete(recursive: true);
        }
      });

      const prefix = 'P3_1_01_00040_00469';
      await File('${tempDir.path}/$prefix.semantic.json').writeAsString('''
      {
        "metadata": {
          "title": "local title",
          "question": "local question"
        },
        "answer": {"value": 507}
      }
      ''');
      await File('${tempDir.path}/$prefix.renderer.json').writeAsString(
        '{"view_box": {"width": 928, "height": 426}, "elements": []}',
      );
      await File('${tempDir.path}/$prefix.layout.json').writeAsString(
        '{"layout": "ok"}',
      );
      await File('${tempDir.path}/$prefix.solvable.v1.2.json').writeAsString(
        '{"answer": {"value": 507}}',
      );
      await File('${tempDir.path}/$prefix.svg').writeAsString('<svg></svg>');

      final repository = ContentRepository.localExamples(
        localProblemsPath: tempDir.path,
      );

      final manifest = await repository.loadManifest();
      final content = await repository.loadProblem(manifest.problems.single);

      expect(manifest.raw['source'], equals('local'));
      expect(
        manifest.problems.single.path.replaceAll(r'\', '/'),
        tempDir.path.replaceAll(r'\', '/'),
      );
      expect(content.semantic, isNotEmpty);
      expect(content.renderer, isNotEmpty);
      expect(content.correctAnswer, equals('507'));
    });

    test('loads local HTTP examples problem list and files', () async {
      final repository = ContentRepository.localHttp(
        localHttpBaseUrl: 'http://localhost:8765',
        httpClient: MockClient((request) async {
          final url = request.url.toString();
          if (url == 'http://localhost:8765/api/problems') {
            return http.Response(
              '{"paths": ["P3_1_01_00040_00469.renderer.json"]}',
              200,
            );
          }
          if (url.endsWith('P3_1_01_00040_00469.semantic.json')) {
            return http.Response(
              '{"metadata": {"title": "local http"}, "answer": {"value": 507}}',
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

      expect(manifest.raw['source'], equals('local-http'));
      expect(manifest.problems.single.path, isEmpty);
      expect(content.renderer, isNotEmpty);
      expect(content.correctAnswer, equals('507'));
    });

    test('reuses loaded problem content for repeated opens', () async {
      final requestedFileUrls = <String>[];
      final repository = ContentRepository.localHttp(
        localHttpBaseUrl: 'http://localhost:8765',
        httpClient: MockClient((request) async {
          final url = request.url.toString();
          if (url == 'http://localhost:8765/api/problems') {
            return http.Response(
              '{"paths": ["P3_1_01_00040_00469.renderer.json"]}',
              200,
            );
          }
          if (url.contains('/files/')) {
            requestedFileUrls.add(url);
          }
          if (url.endsWith('P3_1_01_00040_00469.semantic.json')) {
            return http.Response(
              '{"metadata": {"title": "local http"}, "answer": {"value": 507}}',
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
          return http.Response('Not found', 404);
        }),
      );

      final manifest = await repository.loadManifest();
      final first = await repository.loadProblem(manifest.problems.single);
      final second = await repository.loadProblem(manifest.problems.single);

      expect(identical(first, second), isTrue);
      expect(
        requestedFileUrls
            .where((url) => url.endsWith('P3_1_01_00040_00469.renderer.json')),
        hasLength(1),
      );
    });

    test('strips bundled examples prefix before local HTTP file requests',
        () async {
      final requestedUrls = <String>[];
      final repository = ContentRepository.localHttp(
        localHttpBaseUrl: 'http://localhost:8765',
        httpClient: MockClient((request) async {
          final url = request.url.toString();
          requestedUrls.add(url);
          if (url == 'http://localhost:8765/api/problems') {
            return http.Response(
              '{"paths": ["examples/problems/P3_1_01_00040_00469.renderer.json"]}',
              200,
            );
          }
          if (url.endsWith('P3_1_01_00040_00469.semantic.json')) {
            return http.Response(
              '{"metadata": {"title": "local http"}, "answer": {"value": 507}}',
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

      expect(content.correctAnswer, equals('507'));
      expect(
        requestedUrls,
        contains(
          'http://localhost:8765/files/P3_1_01_00040_00469.semantic.json',
        ),
      );
      expect(
        requestedUrls,
        isNot(
          contains(
            'http://localhost:8765/files/examples%2Fproblems%2FP3_1_01_00040_00469.semantic.json',
          ),
        ),
      );
    });

    test('orders problem prefixes by numeric sequence', () async {
      final repository = ContentRepository.localHttp(
        localHttpBaseUrl: 'http://localhost:8765',
        httpClient: MockClient((request) async {
          if (request.url.toString() == 'http://localhost:8765/api/problems') {
            return http.Response(
              jsonEncode({
                'paths': [
                  'P3_1_01_00040_00470.renderer.json',
                  'P3_1_01_00040_00469.renderer.json',
                  'P3_1_01_00040_02135.renderer.json',
                ],
              }),
              200,
            );
          }
          return http.Response('Not found', 404);
        }),
      );

      final prefixes = await repository.loadGrade3JsonProblemPrefixes();

      expect(
        prefixes,
        equals([
          'P3_1_01_00040_00469',
          'P3_1_01_00040_00470',
          'P3_1_01_00040_02135',
        ]),
      );
    });

    test('normalizes list answers into submission order text', () async {
      const summary = ProblemSummary(
        id: 'list-answer',
        grade: 3,
        subject: 'math',
        unit: 'unit',
        type: 'type',
        title: 'title',
        path: ContentRepository.problemsPath,
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

    test('extracts final answer value from slot answer maps', () {
      const summary = ProblemSummary(
        id: 'slot-answer',
        grade: 3,
        subject: 'math',
        unit: 'unit',
        type: 'type',
        title: 'title',
        path: ContentRepository.problemsPath,
        raw: {},
      );
      const content = ProblemContent(
        summary: summary,
        semantic: {},
        renderer: {},
        solvable: {
          'answer': {
            'value': {
              'slot_id': 'slot.answer',
              'value': 1012,
            },
          },
        },
      );

      expect(content.correctAnswer, equals('1012'));
    });

    test('joins distinct answer key map values for multi-slot answers', () {
      const summary = ProblemSummary(
        id: 'multi-slot-answer',
        grade: 3,
        subject: 'math',
        unit: 'unit',
        type: 'type',
        title: 'title',
        path: ContentRepository.problemsPath,
        raw: {},
      );
      const content = ProblemContent(
        summary: summary,
        semantic: {},
        renderer: {},
        solvable: {
          'answer': {
            'answer_key': [
              {'slot_id': 'slot.operator.1', 'value': '>'},
              {'slot_id': 'slot.operator.2', 'value': '='},
            ],
          },
        },
      );

      expect(content.correctAnswer, equals('>='));
    });

    test('uses choice answer key value for multiple-choice answers', () {
      const summary = ProblemSummary(
        id: 'choice-answer',
        grade: 3,
        subject: 'math',
        unit: 'unit',
        type: 'type',
        title: 'title',
        path: ContentRepository.problemsPath,
        raw: {},
      );
      const content = ProblemContent(
        summary: summary,
        semantic: {},
        renderer: {},
        solvable: {
          'answer': {
            'choices': ['6 × 4', '69 × 4', '60 × 4', '600 × 4'],
            'answer_key': [
              {'id': 'choice.3', 'value': '60 × 4'},
            ],
          },
        },
      );

      expect(content.correctAnswer, equals('60 × 4'));
    });

    test('uses renderer choice slots when answer choices are missing', () {
      const summary = ProblemSummary(
        id: 'renderer-choice-answer',
        grade: 3,
        subject: 'math',
        unit: 'unit',
        type: 'type',
        title: 'title',
        path: ContentRepository.problemsPath,
        raw: {},
      );
      const content = ProblemContent(
        summary: summary,
        semantic: {},
        solvable: {
          'answer': {
            'target': {'type': 'choice_order'},
            'value': '3',
          },
        },
        renderer: {
          'elements': [
            {
              'id': 'slot.choice.2.text',
              'source_ref': 'slot.choice.2',
              'text': '\u2461 B',
              'attributes': {'x': 200, 'y': 100},
            },
            {
              'id': 'slot.choice.1.text',
              'source_ref': 'slot.choice.1',
              'text': '\u2460 A',
              'attributes': {'x': 100, 'y': 100},
            },
          ],
        },
      );

      expect(content.choices, equals(['1. A', '2. B']));
    });

    test('uses renderer instruction when semantic prompt is broken', () {
      const summary = ProblemSummary(
        id: 'broken-prompt',
        grade: 3,
        subject: 'math',
        unit: 'unit',
        type: 'type',
        title: 'title',
        path: ContentRepository.problemsPath,
        raw: {},
      );
      const content = ProblemContent(
        summary: summary,
        semantic: {
          'metadata': {
            'question': '???덉뿉 ?뚮쭪? ?섎? ?⑤꽔?쇱떆??',
          },
        },
        solvable: {},
        renderer: {
          'elements': [
            {
              'id': 'slot.instruction.text',
              'source_ref': 'slot.instruction',
              'text': '□ 안에 알맞은 수를 써넣으시오.',
            },
          ],
        },
      );

      expect(content.prompt, equals('□ 안에 알맞은 수를 써넣으시오.'));
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
