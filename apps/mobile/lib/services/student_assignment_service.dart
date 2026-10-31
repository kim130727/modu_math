import 'dart:async';
import 'dart:convert';
import 'dart:math';

import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

import '../models/assignment.dart';
import 'auth_service.dart';

class AssignmentApiException implements Exception {
  const AssignmentApiException(this.message, {this.status});
  final String message;
  final int? status;
  bool get offline => status == null;
  @override
  String toString() => message;
}

class StudentAssignmentService {
  Future<List<Map<String, dynamic>>> classes() async =>
      (await _request('/api/v1/student/classes/') as List)
          .map(assignmentMap)
          .toList();

  Future<Map<String, dynamic>> library(
      {int page = 1,
      int? classroom,
      String language = 'ko',
      String grade = ''}) async {
    final query = Uri(queryParameters: {
      'scope': classroom == null ? 'public' : 'class',
      'page': '$page',
      'language': language,
      if (classroom != null) 'classroom': '$classroom',
      if (grade.isNotEmpty) 'grade': grade,
    }).query;
    return assignmentMap(await _request('/api/v1/problems/?$query'));
  }

  Future<Map<String, dynamic>> libraryProblem(int id) async =>
      assignmentMap(await _request('/api/v1/problems/$id/'));

  Future<bool> practice(int id, dynamic answer) async {
    final result = assignmentMap(
        await _request('/api/v1/attempts/', method: 'POST', body: {
      'problem': id,
      'submitted_answer': answer,
    }));
    return result['is_correct'] == true;
  }

  StudentAssignmentService(
      {required this.authService,
      http.Client? httpClient,
      this.timeout = const Duration(seconds: 12)})
      : _client = httpClient ?? http.Client();
  final AuthService authService;
  final http.Client _client;
  final Duration timeout;
  String get account =>
      '${authService.effectiveBaseUrl}|${authService.currentUser?.id ?? 'anonymous'}';
  String _key(int assignment, int item, String kind) =>
      'modu_assignment_v1:${Uri.encodeComponent(account)}:$assignment:$item:$kind';

  Future<dynamic> _request(String path,
      {String method = 'GET', dynamic body}) async {
    if (!authService.isAuthenticated || authService.currentUser == null) {
      throw const AssignmentApiException('login', status: 401);
    }
    final token = authService.token;
    final scope = account;
    try {
      final request = http.Request(
          method, Uri.parse('${authService.effectiveBaseUrl}$path'));
      request.headers.addAll(authService.authHeaders);
      if (body != null) request.body = jsonEncode(body);
      final response = await _client
          .send(request)
          .then(http.Response.fromStream)
          .timeout(timeout);
      if (account != scope || token != authService.token) {
        throw const AssignmentApiException('accountChanged', status: 401);
      }
      dynamic data;
      try {
        data = response.bodyBytes.isEmpty
            ? null
            : jsonDecode(utf8.decode(response.bodyBytes));
      } on FormatException {
        throw AssignmentApiException('response', status: response.statusCode);
      }
      if (response.statusCode == 401) {
        await authService.clearSession();
        throw const AssignmentApiException('login', status: 401);
      }
      if (response.statusCode < 200 || response.statusCode >= 300) {
        throw AssignmentApiException(_message(data),
            status: response.statusCode);
      }
      return data;
    } on AssignmentApiException {
      rethrow;
    } on TimeoutException {
      throw const AssignmentApiException('offline');
    } on http.ClientException {
      throw const AssignmentApiException('offline');
    }
  }

  static String _message(dynamic value) {
    if (value is Map) return value.values.map(_message).join(' ');
    if (value is List) return value.map(_message).join(' ');
    return value?.toString() ?? 'response';
  }

  Future<List<StudentAssignment>> list() async =>
      ((await _request('/api/v1/student/assignments/')) as List)
          .map((v) => StudentAssignment.fromJson(assignmentMap(v)))
          .toList();
  Future<StudentAssignment> detail(int id) async => StudentAssignment.fromJson(
      assignmentMap(await _request('/api/v1/student/assignments/$id/')));
  Future<void> join(String code) async {
    await _request('/api/v1/student/join-class/',
        method: 'POST', body: {'invite_code': code.trim()});
  }

  Future<Map<String, dynamic>?> local(
      int assignment, int item, String kind) async {
    final scope = account;
    final key = _key(assignment, item, kind);
    final preferences = await SharedPreferences.getInstance();
    final raw = preferences.getString(key);
    if (scope != account) {
      throw const AssignmentApiException('accountChanged', status: 401);
    }
    if (raw == null) return null;
    try {
      return assignmentMap(jsonDecode(raw));
    } on FormatException {
      return null;
    }
  }

  Future<void> persistDraft(int assignment, int item, dynamic answer,
      {int elapsedMs = 0}) async {
    final key = _key(assignment, item, 'draft');
    final payload = jsonEncode({
      'answer': answer,
      'elapsed_ms': elapsedMs,
      'updated_at': DateTime.now().toUtc().toIso8601String()
    });
    final preferences = await SharedPreferences.getInstance();
    if (!await preferences.setString(key, payload)) {
      throw const AssignmentApiException('storage', status: 507);
    }
  }

  Future<bool> saveDraft(int assignment, int item, dynamic answer) async {
    try {
      await _request('/api/v1/student/assignments/$assignment/progress/',
          method: 'PUT', body: {'item_id': item, 'answer': answer});
      return true;
    } on AssignmentApiException catch (error) {
      if (error.offline) return false;
      rethrow;
    }
  }

  Future<Map<String, dynamic>?> pending(int assignment, int item) =>
      local(assignment, item, 'pending');

  Future<Map<String, dynamic>> submitAnswer(
      int assignment, int item, dynamic answer, int elapsedMs) async {
    final key = _key(assignment, item, 'pending');
    final draftKey = _key(assignment, item, 'draft');
    final scope = account;
    final preferences = await SharedPreferences.getInstance();
    final cached = preferences.getString(key);
    final Map<String, dynamic> payload;
    if (cached != null) {
      payload = assignmentMap(jsonDecode(cached));
      if (jsonEncode(payload['answer']) != jsonEncode(answer)) {
        throw const AssignmentApiException('pending', status: 409);
      }
    } else {
      final random = Random.secure();
      payload = {
        'item_id': item,
        'answer': answer,
        'elapsed_ms': elapsedMs.clamp(0, 86400000),
        'submission_key': List.generate(16,
            (_) => random.nextInt(256).toRadixString(16).padLeft(2, '0')).join()
      };
      if (!await preferences.setString(key, jsonEncode(payload))) {
        throw const AssignmentApiException('storage', status: 507);
      }
    }
    try {
      if (scope != account) {
        throw const AssignmentApiException('accountChanged', status: 401);
      }
      final response = assignmentMap(await _request(
          '/api/v1/student/assignments/$assignment/answers/',
          method: 'POST',
          body: payload));
      if (scope != account) {
        throw const AssignmentApiException('accountChanged', status: 401);
      }
      await preferences.remove(key);
      await preferences.remove(draftKey);
      return response;
    } on AssignmentApiException catch (error) {
      // A rejected request has not committed. Timeouts and 5xx are ambiguous.
      if (error.status != null &&
          error.status! >= 400 &&
          error.status! < 500 &&
          error.status != 401) {
        await preferences.remove(key);
      }
      rethrow;
    }
  }

  Future<Map<String, dynamic>> hint(
          int assignment, int item, int level) async =>
      assignmentMap(await _request(
          '/api/v1/student/assignments/$assignment/hints/',
          method: 'POST',
          body: {'item_id': item, 'level': level}));
  Future<StudentAssignment> submit(int id) async => StudentAssignment.fromJson(
      assignmentMap(await _request('/api/v1/student/assignments/$id/submit/',
          method: 'POST', body: const {})));
}
