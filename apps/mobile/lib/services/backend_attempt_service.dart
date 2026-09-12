import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

import 'auth_service.dart';

class AttemptSubmission {
  const AttemptSubmission({
    required this.problemId,
    this.problemDbId,
    required this.submittedAnswer,
    required this.elapsedMs,
    required this.hintCount,
    required this.retryCount,
    this.events = const [],
    required this.sessionId,
    required this.submittedAt,
  });

  final String problemId;
  final int? problemDbId;
  final dynamic submittedAnswer;
  final int elapsedMs;
  final int hintCount;
  final int retryCount;
  final List<dynamic> events;
  final String sessionId;
  final DateTime submittedAt;

  Map<String, dynamic> toJson() => {
        'problem_id': problemId,
        if (problemDbId != null) 'problem': problemDbId,
        'submitted_answer': submittedAnswer,
        'elapsed_ms': elapsedMs,
        'hint_count': hintCount,
        'retry_count': retryCount,
        'events': events,
        'session_id': sessionId,
        'submitted_at': submittedAt.toIso8601String(),
      };

  factory AttemptSubmission.fromJson(Map<String, dynamic> json) {
    return AttemptSubmission(
      problemId: json['problem_id'] as String? ?? '',
      problemDbId: json['problem'] as int?,
      submittedAnswer: json['submitted_answer'],
      elapsedMs: json['elapsed_ms'] as int? ?? 0,
      hintCount: json['hint_count'] as int? ?? 0,
      retryCount: json['retry_count'] as int? ?? 0,
      events: (json['events'] as List<dynamic>?) ?? const [],
      sessionId: json['session_id'] as String? ?? '',
      submittedAt: DateTime.tryParse(json['submitted_at'] as String? ?? '') ??
          DateTime.now(),
    );
  }
}

class AttemptResult {
  const AttemptResult({
    required this.isCorrect,
    this.serverAttemptId,
    this.isOffline = false,
  });

  final bool isCorrect;
  final int? serverAttemptId;
  final bool isOffline;
}

class BackendAttemptService {
  BackendAttemptService({
    required this.authService,
    http.Client? httpClient,
  }) : _client = httpClient ?? http.Client();

  static const offlineQueueKey = 'modu_math_offline_attempts_queue_v1';

  final AuthService authService;
  final http.Client _client;

  Future<AttemptResult> submitAttempt({
    required AttemptSubmission submission,
    required bool localJudgement,
  }) async {
    final baseUrl = authService.effectiveBaseUrl;
    final uri = Uri.parse('$baseUrl/api/v1/attempts/');

    if (authService.isAuthenticated) {
      try {
        final response = await _client.post(
          uri,
          headers: authService.authHeaders,
          body: jsonEncode(submission.toJson()),
        );

        if (response.statusCode == 201) {
          final decoded = jsonDecode(utf8.decode(response.bodyBytes))
              as Map<String, dynamic>;
          final isCorrect = decoded['is_correct'] as bool? ?? localJudgement;
          final attemptId = decoded['id'] as int?;

          // Also trigger queue sync in the background
          unawaited(syncOfflineQueue());

          return AttemptResult(
            isCorrect: isCorrect,
            serverAttemptId: attemptId,
            isOffline: false,
          );
        }
      } catch (e) {
        debugPrint('Attempt submission network error: $e');
      }
    }

    // If offline or network failed, save to offline queue
    await _enqueueOffline(submission);
    return AttemptResult(
      isCorrect: localJudgement,
      isOffline: true,
    );
  }

  Future<void> _enqueueOffline(AttemptSubmission submission) async {
    final prefs = await SharedPreferences.getInstance();
    final queueJson = prefs.getStringList(offlineQueueKey) ?? [];
    queueJson.add(jsonEncode(submission.toJson()));
    await prefs.setStringList(offlineQueueKey, queueJson);
  }

  Future<int> syncOfflineQueue() async {
    if (!authService.isAuthenticated) {
      return 0;
    }

    final prefs = await SharedPreferences.getInstance();
    final queueJson = prefs.getStringList(offlineQueueKey) ?? [];
    if (queueJson.isEmpty) {
      return 0;
    }

    final baseUrl = authService.effectiveBaseUrl;
    final uri = Uri.parse('$baseUrl/api/v1/attempts/');
    final remaining = <String>[];
    var synced = 0;

    for (final item in queueJson) {
      try {
        final data = jsonDecode(item) as Map<String, dynamic>;
        final response = await _client.post(
          uri,
          headers: authService.authHeaders,
          body: jsonEncode(data),
        );

        if (response.statusCode == 201) {
          synced++;
        } else {
          remaining.add(item);
        }
      } catch (_) {
        remaining.add(item);
      }
    }

    await prefs.setStringList(offlineQueueKey, remaining);
    return synced;
  }
}

void unawaited(Future<void> future) {}
