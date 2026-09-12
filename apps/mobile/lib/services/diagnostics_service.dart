import 'dart:convert';
import 'package:http/http.dart' as http;

import 'auth_service.dart';

class DiagnosticSummaryData {
  const DiagnosticSummaryData({
    required this.totalProblems,
    required this.totalAttempts,
    required this.accuracy,
    required this.avgElapsedMs,
    required this.hintRate,
    required this.avgRetryCount,
    required this.strengths,
    required this.weaknesses,
    required this.insufficientData,
    required this.recentTrend,
    required this.headline,
  });

  final int totalProblems;
  final int totalAttempts;
  final double accuracy;
  final int avgElapsedMs;
  final double hintRate;
  final double avgRetryCount;
  final List<dynamic> strengths;
  final List<dynamic> weaknesses;
  final List<dynamic> insufficientData;
  final Map<String, dynamic> recentTrend;
  final String headline;

  factory DiagnosticSummaryData.fromJson(Map<String, dynamic> json) {
    return DiagnosticSummaryData(
      totalProblems: json['total_problems'] as int? ?? 0,
      totalAttempts: json['total_attempts'] as int? ?? 0,
      accuracy: (json['accuracy'] as num?)?.toDouble() ?? 0.0,
      avgElapsedMs: json['avg_elapsed_ms'] as int? ?? 0,
      hintRate: (json['hint_rate'] as num?)?.toDouble() ?? 0.0,
      avgRetryCount: (json['avg_retry_count'] as num?)?.toDouble() ?? 0.0,
      strengths: (json['strengths'] as List<dynamic>?) ?? const [],
      weaknesses: (json['weaknesses'] as List<dynamic>?) ?? const [],
      insufficientData:
          (json['insufficient_data'] as List<dynamic>?) ?? const [],
      recentTrend:
          (json['recent_trend'] as Map<String, dynamic>?) ?? const {},
      headline: json['headline'] as String? ?? '',
    );
  }
}

class DiagnosticTagMetric {
  const DiagnosticTagMetric({
    required this.key,
    required this.nameKo,
    required this.domain,
    required this.description,
    required this.score,
    required this.rawAccuracy,
    required this.attemptCount,
    required this.correctCount,
    required this.confidence,
    required this.status,
    required this.statusLabel,
    required this.statusMessage,
  });

  final String key;
  final String nameKo;
  final String domain;
  final String description;
  final double score;
  final double rawAccuracy;
  final int attemptCount;
  final int correctCount;
  final double confidence;
  final String status;
  final String statusLabel;
  final String statusMessage;

  factory DiagnosticTagMetric.fromJson(Map<String, dynamic> json) {
    return DiagnosticTagMetric(
      key: json['key'] as String? ?? '',
      nameKo: json['name_ko'] as String? ?? '',
      domain: json['domain'] as String? ?? '',
      description: json['description'] as String? ?? '',
      score: (json['score'] as num?)?.toDouble() ?? 0.0,
      rawAccuracy: (json['raw_accuracy'] as num?)?.toDouble() ?? 0.0,
      attemptCount: json['attempt_count'] as int? ?? 0,
      correctCount: json['correct_count'] as int? ?? 0,
      confidence: (json['confidence'] as num?)?.toDouble() ?? 0.0,
      status: json['status'] as String? ?? 'insufficient',
      statusLabel: json['status_label'] as String? ?? '기록 부족',
      statusMessage: json['status_message'] as String? ?? '',
    );
  }
}

class RecommendedProblemItem {
  const RecommendedProblemItem({
    required this.problemId,
    required this.dbId,
    required this.title,
    required this.grade,
    required this.problemType,
    required this.unit,
    required this.domain,
    required this.reason,
    required this.priority,
    required this.statusLabel,
  });

  final String problemId;
  final int dbId;
  final String title;
  final int? grade;
  final String problemType;
  final String unit;
  final String domain;
  final String reason;
  final int priority;
  final String statusLabel;

  factory RecommendedProblemItem.fromJson(Map<String, dynamic> json) {
    final problem = json['problem'] as Map<String, dynamic>? ?? {};
    final mastery = json['current_mastery'] as Map<String, dynamic>? ?? {};
    return RecommendedProblemItem(
      problemId: problem['problem_id'] as String? ?? '',
      dbId: problem['id'] as int? ?? 0,
      title: problem['title'] as String? ?? '',
      grade: problem['grade'] as int?,
      problemType: problem['problem_type'] as String? ?? '',
      unit: problem['unit'] as String? ?? '',
      domain: problem['domain'] as String? ?? '',
      reason: json['reason'] as String? ?? '',
      priority: json['priority'] as int? ?? 5,
      statusLabel: mastery['status_label'] as String? ?? '기록 부족',
    );
  }
}

class DiagnosticsClientService {
  DiagnosticsClientService({
    required this.authService,
    http.Client? httpClient,
  }) : _client = httpClient ?? http.Client();

  final AuthService authService;
  final http.Client _client;

  String get _baseUrl => authService.effectiveBaseUrl;

  Future<DiagnosticSummaryData?> fetchSummary() async {
    if (!authService.isAuthenticated) return null;
    final uri = Uri.parse('$_baseUrl/api/v1/diagnostics/summary/');
    try {
      final res = await _client.get(uri, headers: authService.authHeaders);
      if (res.statusCode == 200) {
        final decoded =
            jsonDecode(utf8.decode(res.bodyBytes)) as Map<String, dynamic>;
        return DiagnosticSummaryData.fromJson(decoded);
      }
    } catch (_) {}
    return null;
  }

  Future<List<DiagnosticTagMetric>> fetchConcepts() async {
    if (!authService.isAuthenticated) return [];
    final uri = Uri.parse('$_baseUrl/api/v1/diagnostics/concepts/');
    try {
      final res = await _client.get(uri, headers: authService.authHeaders);
      if (res.statusCode == 200) {
        final decoded =
            jsonDecode(utf8.decode(res.bodyBytes)) as List<dynamic>;
        return decoded
            .map((item) =>
                DiagnosticTagMetric.fromJson(item as Map<String, dynamic>))
            .toList();
      }
    } catch (_) {}
    return [];
  }

  Future<List<DiagnosticTagMetric>> fetchSkills() async {
    if (!authService.isAuthenticated) return [];
    final uri = Uri.parse('$_baseUrl/api/v1/diagnostics/skills/');
    try {
      final res = await _client.get(uri, headers: authService.authHeaders);
      if (res.statusCode == 200) {
        final decoded =
            jsonDecode(utf8.decode(res.bodyBytes)) as List<dynamic>;
        return decoded
            .map((item) =>
                DiagnosticTagMetric.fromJson(item as Map<String, dynamic>))
            .toList();
      }
    } catch (_) {}
    return [];
  }

  Future<List<RecommendedProblemItem>> fetchRecommendations() async {
    if (!authService.isAuthenticated) return [];
    final uri = Uri.parse('$_baseUrl/api/v1/recommendations/');
    try {
      final res = await _client.get(uri, headers: authService.authHeaders);
      if (res.statusCode == 200) {
        final decoded =
            jsonDecode(utf8.decode(res.bodyBytes)) as List<dynamic>;
        return decoded
            .map((item) =>
                RecommendedProblemItem.fromJson(item as Map<String, dynamic>))
            .toList();
      }
    } catch (_) {}
    return [];
  }
}
