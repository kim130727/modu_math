import 'dart:convert';

import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';
import 'package:modu_math_app/services/backend_content_repository.dart';

void main() {
  test('loads problem catalog and JSON contracts from Django API', () async {
    final requests = <Uri>[];
    final client = MockClient((request) async {
      requests.add(request.url);
      if (request.url.path == '/api/v1/problems/') {
        return http.Response(
          jsonEncode({
            'count': 1,
            'next': null,
            'previous': null,
            'results': [_problemJson(includeContracts: false)],
          }),
          200,
          headers: {'content-type': 'application/json; charset=utf-8'},
        );
      }
      if (request.url.path == '/api/v1/problems/31/') {
        return http.Response(
          jsonEncode(_problemJson(includeContracts: true)),
          200,
          headers: {'content-type': 'application/json; charset=utf-8'},
        );
      }
      if (request.url.path == '/api/v1/problems/31/asset/') {
        return http.Response('<svg></svg>', 200);
      }
      return http.Response('Not found', 404);
    });

    final repository = BackendContentRepository(
      baseUrl: 'http://backend.test',
      httpClient: client,
    );
    repository.activeProblemLocale = 'ko';

    final manifest = await repository.loadManifest();
    expect(manifest.version, 'django-api-v1');
    expect(manifest.problems, hasLength(1));
    expect(manifest.problems.single.id, 'S3_elem_3_008540');
    expect(manifest.problems.single.dbId, 31);
    expect(manifest.problems.single.language, 'ko');

    final content = await repository.loadProblem(manifest.problems.single);
    expect(content.semantic['problem_id'], 'S3_elem_3_008540');
    expect(content.layout['schema'], 'modu.layout.v1');
    expect(content.renderer['schema'], 'modu.renderer.v1');
    expect(content.svg, isEmpty);
    expect(
      requests.any((uri) => uri.path == '/api/v1/problems/31/asset/'),
      isFalse,
    );
    expect(requests.first.queryParameters['language'], 'ko');
  });

  test(
      'reloads the localized problem after changing language on an open problem',
      () async {
    final requests = <Uri>[];
    final client = MockClient((request) async {
      requests.add(request.url);
      if (request.url.path == '/api/v1/problems/') {
        final language = request.url.queryParameters['language'] ?? 'ko';
        final item = _localizedProblemJson(
          language: language,
          dbId: language == 'uk' ? 60 : 40,
          includeContracts: false,
        );
        return http.Response(
          jsonEncode({
            'count': 1,
            'next': null,
            'previous': null,
            'results': [item],
          }),
          200,
          headers: {'content-type': 'application/json; charset=utf-8'},
        );
      }
      if (request.url.path == '/api/v1/problems/40/') {
        return http.Response(
          jsonEncode(_localizedProblemJson(
            language: 'ko',
            dbId: 40,
            includeContracts: true,
          )),
          200,
          headers: {'content-type': 'application/json; charset=utf-8'},
        );
      }
      if (request.url.path == '/api/v1/problems/60/') {
        return http.Response(
          jsonEncode(_localizedProblemJson(
            language: 'uk',
            dbId: 60,
            includeContracts: true,
          )),
          200,
          headers: {'content-type': 'application/json; charset=utf-8'},
        );
      }
      if (request.url.path.endsWith('/asset/')) {
        return http.Response('<svg></svg>', 200);
      }
      return http.Response('Not found', 404);
    });

    final repository = BackendContentRepository(
      baseUrl: 'http://backend.test',
      httpClient: client,
    );
    final koManifest = await repository.loadManifest();
    final staleKoSummary = koManifest.problems.single;
    final koContent = await repository.loadProblem(staleKoSummary);
    expect(koContent.renderer['elements'].single['text'], '물병');

    repository.activeProblemLocale = 'uk';
    final ukContent = await repository.loadProblem(staleKoSummary);

    expect(ukContent.summary.language, 'uk');
    expect(ukContent.summary.dbId, 60);
    expect(ukContent.renderer['elements'].single['text'], 'Пляшка');
    expect(
      requests
          .where((uri) => uri.path == '/api/v1/problems/')
          .last
          .queryParameters['language'],
      'uk',
    );
    expect(requests.any((uri) => uri.path == '/api/v1/problems/60/'), isTrue);
  });
}

Map<String, dynamic> _localizedProblemJson({
  required String language,
  required int dbId,
  required bool includeContracts,
}) {
  final label = language == 'uk' ? 'Пляшка' : '물병';
  return {
    'id': dbId,
    'problem_id': 'S3_elem_3_008751',
    'language': language,
    'grade': 3,
    'problem_type': 'ox',
    'concepts': const [],
    'skills': const [],
    'title': label,
    'subject': 'math',
    'unit': 'measurement',
    'domain': 'measurement',
    'semester': '2',
    'unit_number': 5,
    'unit_topic': 'measurement',
    'sub_unit': 'comparison',
    'topic': 'measurement',
    'file_prefix': 'S3_elem_3_008751',
    'path': 'examples/problems/$language',
    if (includeContracts) ...{
      'semantic_data': {
        'problem_id': 'S3_elem_3_008751',
        'metadata': {'question': label},
      },
      'solvable_data': const {},
      'layout_data': const {'schema': 'modu.layout.v1'},
      'renderer_data': {
        'schema': 'modu.renderer.v1',
        'elements': [
          {'id': 'slot.label.water.text', 'text': label},
        ],
      },
    },
  };
}

Map<String, dynamic> _problemJson({required bool includeContracts}) {
  return {
    'id': 31,
    'problem_id': 'S3_elem_3_008540',
    'language': 'ko',
    'grade': 3,
    'problem_type': 'multiple_choice',
    'concepts': ['곱셈'],
    'skills': ['자리값'],
    'title': '곱셈 문제',
    'subject': 'math',
    'unit': '곱셈',
    'domain': '수와 연산',
    'semester': '1학기',
    'unit_number': 4,
    'unit_topic': '곱셈',
    'sub_unit': '기본 학습',
    'topic': '곱셈',
    'file_prefix': 'S3_elem_3_008540',
    'path': 'examples/problems/ko',
    if (includeContracts) ...{
      'semantic_data': {
        'problem_id': 'S3_elem_3_008540',
        'answer': {'value': 2},
      },
      'solvable_data': {'method': 'place_value'},
      'layout_data': {'schema': 'modu.layout.v1'},
      'renderer_data': {'schema': 'modu.renderer.v1'},
    },
  };
}
