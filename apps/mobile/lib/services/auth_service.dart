import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

import '../models/auth_user.dart';
import 'app_environment.dart';

class AuthService {
  AuthService({
    String? baseUrl,
    http.Client? httpClient,
  })  : baseUrl = (baseUrl ?? AppEnvironment.backendBaseUrl)
            .replaceAll(RegExp(r'/+$'), ''),
        _client = httpClient ?? http.Client();

  static const tokenStorageKey = 'modu_math_auth_token_v1';
  static const userStorageKey = 'modu_math_auth_user_v1';

  final String baseUrl;
  final http.Client _client;

  String? _token;
  AuthUser? _currentUser;
  final ValueNotifier<AuthUser?> userNotifier = ValueNotifier<AuthUser?>(null);

  String? get token => _token;
  AuthUser? get currentUser => _currentUser;
  bool get isAuthenticated => _token != null && _token!.isNotEmpty;

  String get effectiveBaseUrl {
    if (baseUrl == 'same-origin' && kIsWeb) {
      return Uri.base.origin;
    }
    if (baseUrl.isNotEmpty) {
      return baseUrl;
    }
    return 'http://127.0.0.1:8000';
  }

  Future<void> restoreSession() async {
    final prefs = await SharedPreferences.getInstance();
    _token = prefs.getString(tokenStorageKey);
    final userJson = prefs.getString(userStorageKey);
    if (userJson != null && userJson.isNotEmpty) {
      try {
        final decoded = jsonDecode(userJson) as Map<String, dynamic>;
        _currentUser = AuthUser.fromJson(decoded);
      } catch (_) {
        _currentUser = null;
      }
    }
    userNotifier.value = _currentUser;
  }

  Future<AuthResult> login({
    required String username,
    required String password,
  }) async {
    final uri = Uri.parse('$effectiveBaseUrl/api/v1/auth/login/');
    try {
      final response = await _client.post(
        uri,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'username': username.trim(), 'password': password}),
      );

      final body = utf8.decode(response.bodyBytes);
      final decoded = jsonDecode(body);

      if (response.statusCode == 200 && decoded is Map<String, dynamic>) {
        final tokenVal = decoded['token'] as String?;
        final userVal = decoded['user'] as Map<String, dynamic>?;

        if (tokenVal != null && userVal != null) {
          _token = tokenVal;
          _currentUser = AuthUser.fromJson(userVal);
          userNotifier.value = _currentUser;

          final prefs = await SharedPreferences.getInstance();
          await prefs.setString(tokenStorageKey, tokenVal);
          await prefs.setString(
              userStorageKey, jsonEncode(_currentUser!.toJson()));
          return const AuthResult.success();
        }
      }

      final errorMsg = _extractErrorMessage(decoded);
      return AuthResult.failure(
          errorMsg.isNotEmpty ? errorMsg : '로그인에 실패했습니다.');
    } catch (e) {
      return AuthResult.failure('서버와 통신하는 중 오류가 발생했습니다: $e');
    }
  }

  Future<AuthResult> register({
    required String username,
    required String email,
    required String password,
  }) async {
    final uri = Uri.parse('$effectiveBaseUrl/api/v1/auth/register/');
    try {
      final response = await _client.post(
        uri,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'username': username.trim(),
          'email': email.trim(),
          'password': password,
        }),
      );

      final body = utf8.decode(response.bodyBytes);
      final decoded = jsonDecode(body);

      if (response.statusCode == 201 && decoded is Map<String, dynamic>) {
        final tokenVal = decoded['token'] as String?;
        final userVal = decoded['user'] as Map<String, dynamic>?;

        if (tokenVal != null && userVal != null) {
          _token = tokenVal;
          _currentUser = AuthUser.fromJson(userVal);
          userNotifier.value = _currentUser;

          final prefs = await SharedPreferences.getInstance();
          await prefs.setString(tokenStorageKey, tokenVal);
          await prefs.setString(
              userStorageKey, jsonEncode(_currentUser!.toJson()));
          return const AuthResult.success();
        }
      }

      final errorMsg = _extractErrorMessage(decoded);
      return AuthResult.failure(
          errorMsg.isNotEmpty ? errorMsg : '회원가입에 실패했습니다.');
    } catch (e) {
      return AuthResult.failure('서버와 통신하는 중 오류가 발생했습니다: $e');
    }
  }

  Future<void> logout() async {
    _token = null;
    _currentUser = null;
    userNotifier.value = null;

    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(tokenStorageKey);
    await prefs.remove(userStorageKey);
  }

  Map<String, String> get authHeaders {
    return {
      'Content-Type': 'application/json',
      if (isAuthenticated) 'Authorization': 'Token $_token',
    };
  }

  String _extractErrorMessage(dynamic decoded) {
    if (decoded is Map<String, dynamic>) {
      for (final value in decoded.values) {
        if (value is List && value.isNotEmpty) {
          return value.first.toString();
        }
        if (value is String) {
          return value;
        }
      }
    }
    return '';
  }
}

class AuthResult {
  const AuthResult.success()
      : isSuccess = true,
        errorMessage = null;

  const AuthResult.failure(this.errorMessage) : isSuccess = false;

  final bool isSuccess;
  final String? errorMessage;
}
