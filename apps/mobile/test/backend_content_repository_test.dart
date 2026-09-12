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
    expect(content.svg, '<svg></svg>');
    expect(requests.first.queryParameters['language'], 'ko');
  });
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
