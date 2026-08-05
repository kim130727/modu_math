import 'dart:convert';

import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';
import 'package:modu_math_app/models/content_models.dart';
import 'package:modu_math_app/models/tutor_models.dart';
import 'package:modu_math_app/services/backend_tutor_service.dart';

void main() {
  group('BackendTutorService', () {
    test('posts tutor requests to the backend proxy', () async {
      http.Request? capturedRequest;
      Map<String, dynamic>? capturedBody;

      final service = BackendTutorService(
        baseUrl: 'http://localhost:8000',
        sessionToken: 'session-token',
        client: MockClient((request) async {
          capturedRequest = request;
          capturedBody = jsonDecode(request.body) as Map<String, dynamic>;
          return http.Response(
            jsonEncode({
              'message': {
                'role': 'tutor',
                'text': 'Check the condition first.',
                'replyType': 'hint',
                'createdAt': '2026-07-22T00:00:00Z',
              },
            }),
            200,
            headers: {'content-type': 'application/json'},
          );
        }),
      );

      final reply = await service.hint(
        content: _content(),
        messages: [
          TutorMessage(
            role: TutorMessageRole.student,
            text: 'I need help.',
            createdAt: DateTime.utc(2026, 7, 22),
          ),
        ],
        hintLevel: 1,
      );

      expect(capturedRequest?.url.path, equals('/api/v1/tutor/messages'));
      expect(capturedRequest?.headers['Authorization'],
          equals('Bearer session-token'));
      expect(capturedBody?['action'], equals('hint'));
      expect(capturedBody?['hintLevel'], equals(1));
      expect((capturedBody?['problem'] as Map)['id'], equals('P001'));
      expect((capturedBody?['messages'] as List).length, equals(1));
      expect(reply.text, equals('Check the condition first.'));
      expect(reply.replyType, equals(TutorReplyType.hint));
    });
  });
}

ProblemContent _content() {
  return const ProblemContent(
    summary: ProblemSummary(
      id: 'P001',
      grade: 3,
      subject: 'math',
      unit: 'multiplication',
      type: 'word_problem',
      title: 'Problem 1',
      path: '',
      raw: {},
    ),
    svg: '',
    semantic: {
      'metadata': {'question': 'What is 6 times 4?'},
    },
    solvable: {
      'answer': {'value': '24'},
    },
  );
}
