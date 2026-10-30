import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';
import 'package:modu_math_app/services/auth_service.dart';
import 'package:modu_math_app/services/student_assignment_service.dart';

http.Response assignmentJson(dynamic body, [int status = 200]) =>
    http.Response(jsonEncode(body), status,
        headers: {'content-type': 'application/json; charset=utf-8'});

class AssignmentFixture {
  bool submitted = false;
  bool released = false;
  bool loseResponse = false;
  bool offlineDraft = false;
  int hints = 0;
  final drafts = <int, dynamic>{};
  final answers = <int, dynamic>{};
  final keys = <String, int>{};
  final posts = <Map<String, dynamic>>[];
  late final MockClient client = MockClient(handle);
  late final AuthService auth =
      AuthService(baseUrl: 'https://assignments.test', httpClient: client);
  late final StudentAssignmentService service =
      StudentAssignmentService(authService: auth, httpClient: client);
  Future<void> login([int user = 1]) async {
    await auth.login(username: 'student$user', password: 'password-123');
  }

  Map<String, dynamic> detail({bool includeItems = true}) => {
        'id': 1,
        'recipient_id': 1,
        'title': '두 문제 과제',
        'status': 'active',
        'max_attempts': 2,
        'can_work': !submitted,
        'results_released': released,
        'total': 2,
        'completed': answers.length,
        'submitted_at': submitted ? '2026-10-30T00:00:00Z' : null,
        if (released) ...{
          'correct': answers.values.where((v) => v == '42').length,
          'accuracy': .5
        },
        if (includeItems)
          'items': [1, 2]
              .map((id) => {
                    'id': id,
                    'position': id - 1,
                    'attempt_count': keys.values.where((v) => v == id).length,
                    'draft_answer': drafts[id],
                    if (answers.containsKey(id))
                      'submitted_answer': answers[id],
                    'hint_total': 2,
                    'revealed_hints': List.generate(
                        hints, (i) => {'text': '일의 자리부터 생각해 보세요.'}),
                    if (released && answers.containsKey(id)) ...{
                      'is_correct': answers[id] == '42',
                      'answer': {'value': 42},
                      'solution': {
                        'steps': [
                          {'expr': '20 + 22', 'value': 42}
                        ]
                      }
                    },
                    'content': {
                      'id': id,
                      'problem_id': 'assignment-$id',
                      'prompt': '20개와 22개는 모두 몇 개인가요?',
                      'semantic_data': {
                        'metadata': {'question': '20개와 22개는 모두 몇 개인가요?'}
                      },
                      'input_schema': {
                        'fields': [
                          {'id': 'field-1', 'type': 'number', 'choices': []}
                        ],
                        'unit': '개'
                      },
                      'renderer_data': {
                        'view_box': {'width': 600, 'height': 160},
                        'elements': [
                          {
                            'id': 'expression',
                            'type': 'text_box',
                            'text': '20 + 22 = □',
                            'attributes': {
                              'x': 30,
                              'y': 30,
                              'width': 500,
                              'height': 70,
                              'font-size': 36
                            }
                          }
                        ]
                      },
                    },
                  })
              .toList(),
      };
  Future<http.Response> handle(http.Request request) async {
    final path = request.url.path;
    final body = request.body.isEmpty
        ? <String, dynamic>{}
        : jsonDecode(request.body) as Map<String, dynamic>;
    if (path.endsWith('/auth/login/')) {
      final id = body['username'] == 'student2' ? 2 : 1;
      return assignmentJson({
        'token': 'token-$id',
        'user': {'id': id, 'username': 'student$id', 'role': 'student'}
      });
    }
    if (path.endsWith('/auth/logout/')) return http.Response('', 204);
    if (path == '/api/v1/student/assignments/') {
      return assignmentJson([detail(includeItems: false)]);
    }
    if (path == '/api/v1/student/assignments/1/') {
      return assignmentJson(detail());
    }
    if (path.endsWith('/progress/')) {
      if (offlineDraft) throw http.ClientException('offline');
      drafts[body['item_id'] as int] = body['answer'];
      return assignmentJson({'saved': true});
    }
    if (path.endsWith('/answers/')) {
      posts.add(body);
      final key = body['submission_key'] as String;
      final id = body['item_id'] as int;
      final replay = keys.containsKey(key);
      keys[key] = id;
      answers[id] = body['answer'];
      if (loseResponse) {
        loseResponse = false;
        throw http.ClientException('response lost after commit');
      }
      return assignmentJson({
        'attempt_id': keys.length,
        'item_id': id,
        'attempt_number': keys.values.where((v) => v == id).length,
        if (released) 'is_correct': body['answer'] == '42'
      }, replay ? 200 : 201);
    }
    if (path.endsWith('/hints/')) {
      hints = body['level'] as int;
      return assignmentJson({
        'level': hints,
        'hint': {'text': '일의 자리부터 생각해 보세요.'}
      });
    }
    if (path.endsWith('/submit/')) {
      submitted = true;
      released = true;
      return assignmentJson(detail());
    }
    if (path.endsWith('/join-class/')) {
      return assignmentJson({'status': 'pending'}, 201);
    }
    return assignmentJson({'detail': 'not found'}, 404);
  }
}
