import 'dart:convert';

import 'package:http/http.dart' as http;

import '../models/content_models.dart';
import '../models/tutor_models.dart';
import '../utils/tutor_text_sanitizer.dart';
import 'ai_tutor_service.dart';

class BackendTutorService extends AiTutorService {
  BackendTutorService({
    required String baseUrl,
    this.sessionToken,
    http.Client? client,
  })  : baseUri = Uri.parse(baseUrl.replaceFirst(RegExp(r'/+$'), '')),
        client = client ?? http.Client();

  final Uri baseUri;
  final String? sessionToken;
  final http.Client client;

  @override
  TutorMode get mode => TutorMode.backend;

  @override
  String get label => 'Backend';

  @override
  List<TutorMessage> startSession(ProblemContent content) {
    return [
      _tutor(
        '문제를 같이 읽고 한 단계씩 생각해 볼게요. 먼저 무엇을 구해야 하는지 말해 볼까요?',
        TutorReplyType.greeting,
      ),
    ];
  }

  @override
  Future<TutorMessage> hint({
    required ProblemContent content,
    required List<TutorMessage> messages,
    required int hintLevel,
  }) {
    return _requestTutorMessage(
      action: 'hint',
      content: content,
      messages: messages,
      payload: {'hintLevel': hintLevel},
      fallbackType: TutorReplyType.hint,
    );
  }

  @override
  Future<TutorMessage> nextQuestion({
    required ProblemContent content,
    required List<TutorMessage> messages,
    required int stepIndex,
  }) {
    return _requestTutorMessage(
      action: 'next_question',
      content: content,
      messages: messages,
      payload: {'stepIndex': stepIndex},
      fallbackType: TutorReplyType.question,
    );
  }

  @override
  Future<TutorMessage> respondToStudent({
    required ProblemContent content,
    required List<TutorMessage> messages,
    required String message,
    required int stepIndex,
  }) {
    return _requestTutorMessage(
      action: 'respond',
      content: content,
      messages: messages,
      payload: {
        'message': message,
        'stepIndex': stepIndex,
      },
      fallbackType: TutorReplyType.question,
    );
  }

  @override
  Future<TutorMessage> reviewAnswer({
    required ProblemContent content,
    required List<TutorMessage> messages,
    required String answer,
  }) {
    return _requestTutorMessage(
      action: 'review_answer',
      content: content,
      messages: messages,
      payload: {'answer': answer},
      fallbackType: TutorReplyType.retry,
    );
  }

  Future<TutorMessage> _requestTutorMessage({
    required String action,
    required ProblemContent content,
    required List<TutorMessage> messages,
    required Map<String, Object?> payload,
    required TutorReplyType fallbackType,
  }) async {
    if (baseUri.toString().trim().isEmpty) {
      return _tutor(
        '튜터 서버 주소가 아직 설정되지 않았어요. BACKEND_API_BASE_URL을 확인해 주세요.',
        TutorReplyType.retry,
      );
    }

    final response = await client.post(
      baseUri.resolve('/api/v1/tutor/messages'),
      headers: {
        'Content-Type': 'application/json',
        if (sessionToken != null && sessionToken!.isNotEmpty)
          'Authorization': 'Bearer $sessionToken',
      },
      body: jsonEncode({
        'action': action,
        'problem': _problemPayload(content),
        'messages': messages.takeLast(12).map(_messagePayload).toList(),
        ...payload,
      }),
    );

    if (response.statusCode < 200 || response.statusCode >= 300) {
      return _tutor(
        '튜터 서버와 연결하는 중 문제가 생겼어요. 잠시 뒤 다시 시도해 주세요.',
        TutorReplyType.retry,
      );
    }

    final decoded = jsonDecode(utf8.decode(response.bodyBytes));
    final text = sanitizeTutorText(_extractText(decoded));
    return _tutor(
      text.isEmpty ? '좋아요. 다음으로 무엇을 생각하면 좋을까요?' : text,
      _extractReplyType(decoded) ?? fallbackType,
    );
  }

  Map<String, Object?> _problemPayload(ProblemContent content) {
    return {
      'id': content.summary.id,
      'grade': content.summary.grade,
      'subject': content.summary.subject,
      'unit': content.summary.unit,
      'type': content.summary.type,
      'title': content.summary.title,
      'prompt': content.prompt,
      'choices': content.choices,
      'correctAnswer': content.correctAnswer,
      'answerMap': content.answerMap,
      'semantic': content.semantic,
      'solvable': content.solvable,
    };
  }

  Map<String, Object?> _messagePayload(TutorMessage message) {
    return {
      'role': message.isTutor ? 'tutor' : 'student',
      'text': sanitizeTutorText(message.text),
      'replyType': message.replyType?.name,
      'createdAt': message.createdAt.toIso8601String(),
    };
  }

  String _extractText(Object? decoded) {
    if (decoded is! Map<String, dynamic>) {
      return '';
    }
    final message = decoded['message'];
    if (message is Map<String, dynamic>) {
      final text = message['text'];
      if (text is String) {
        return text;
      }
    }
    final text = decoded['text'];
    return text is String ? text : '';
  }

  TutorReplyType? _extractReplyType(Object? decoded) {
    if (decoded is! Map<String, dynamic>) {
      return null;
    }
    final message = decoded['message'];
    final value = message is Map<String, dynamic>
        ? message['replyType']?.toString()
        : decoded['replyType']?.toString();
    if (value == null) {
      return null;
    }
    return TutorReplyType.values.firstWhere(
      (type) => type.name == value,
      orElse: () => TutorReplyType.question,
    );
  }

  TutorMessage _tutor(String text, TutorReplyType type) {
    return TutorMessage(
      role: TutorMessageRole.tutor,
      text: sanitizeTutorText(text),
      replyType: type,
      createdAt: DateTime.now(),
    );
  }
}

extension _TakeLast<T> on List<T> {
  Iterable<T> takeLast(int count) {
    if (length <= count) {
      return this;
    }
    return skip(length - count);
  }
}
