import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';
import 'package:modu_math_app/models/auth_user.dart';
import 'package:modu_math_app/screens/diagnostic_screen.dart';
import 'package:modu_math_app/services/auth_service.dart';
import 'package:modu_math_app/services/backend_attempt_service.dart';
import 'package:modu_math_app/services/content_repository.dart';
import 'package:modu_math_app/services/diagnostics_service.dart';
import 'package:modu_math_app/services/local_progress_repository.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  setUp(() {
    SharedPreferences.setMockInitialValues({});
  });

  group('AuthService Tests', () {
    test('login stores token and user in SharedPreferences', () async {
      final mockClient = MockClient((request) async {
        if (request.url.path == '/api/v1/auth/login/') {
          return http.Response(
            jsonEncode({
              'token': 'test_token_123',
              'user': {
                'id': 1,
                'username': 'student_alice',
                'email': 'alice@example.com',
                'is_staff': false,
              },
            }),
            200,
          );
        }
        return http.Response('Not Found', 404);
      });

      final authService = AuthService(
        baseUrl: 'http://test-server',
        httpClient: mockClient,
      );

      final result = await authService.login(
        username: 'student_alice',
        password: 'password123',
      );

      expect(result.isSuccess, isTrue);
      expect(authService.isAuthenticated, isTrue);
      expect(authService.token, equals('test_token_123'));
      expect(authService.currentUser?.username, equals('student_alice'));

      // Test session restoration
      final restoredService = AuthService(
        baseUrl: 'http://test-server',
        httpClient: mockClient,
      );
      await restoredService.restoreSession();
      expect(restoredService.isAuthenticated, isTrue);
      expect(restoredService.currentUser?.username, equals('student_alice'));

      // Test logout
      await restoredService.logout();
      expect(restoredService.isAuthenticated, isFalse);
      expect(restoredService.token, isNull);
    });

    test('register failure returns error message', () async {
      final mockClient = MockClient((request) async {
        return http.Response(
          jsonEncode({'username': ['이미 존재하는 아이디입니다.']}),
          400,
        );
      });

      final authService = AuthService(
        baseUrl: 'http://test-server',
        httpClient: mockClient,
      );

      final result = await authService.register(
        username: 'existing_user',
        email: 'exist@example.com',
        password: 'password123',
      );

      expect(result.isSuccess, isFalse);
      expect(result.errorMessage, contains('이미 존재하는 아이디입니다.'));
    });
  });

  group('BackendAttemptService Tests', () {
    test('online submission returns server authoritative is_correct', () async {
      final mockClient = MockClient((request) async {
        if (request.url.path == '/api/v1/attempts/') {
          return http.Response(
            jsonEncode({
              'id': 101,
              'is_correct': true,
              'submitted_answer': '42',
            }),
            201,
          );
        }
        return http.Response('Error', 500);
      });

      final authService = AuthService(
        baseUrl: 'http://test-server',
        httpClient: mockClient,
      );
      // Simulate logged in
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString(AuthService.tokenStorageKey, 'valid_token');
      await authService.restoreSession();

      final attemptService = BackendAttemptService(
        authService: authService,
        httpClient: mockClient,
      );

      final result = await attemptService.submitAttempt(
        submission: AttemptSubmission(
          problemId: 'P123',
          submittedAnswer: '42',
          elapsedMs: 3500,
          hintCount: 0,
          retryCount: 0,
          sessionId: 'sess_1',
          submittedAt: DateTime.now(),
        ),
        localJudgement: false, // server will override to true
      );

      expect(result.isCorrect, isTrue);
      expect(result.serverAttemptId, equals(101));
      expect(result.isOffline, isFalse);
    });

    test('offline submission queues attempt and syncs when online', () async {
      var requestCount = 0;
      final mockClient = MockClient((request) async {
        requestCount++;
        if (requestCount == 1) {
          // Simulate network failure on first try
          throw http.ClientException('Network down');
        }
        return http.Response(jsonEncode({'id': 102, 'is_correct': true}), 201);
      });

      final authService = AuthService(
        baseUrl: 'http://test-server',
        httpClient: mockClient,
      );
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString(AuthService.tokenStorageKey, 'valid_token');
      await authService.restoreSession();

      final attemptService = BackendAttemptService(
        authService: authService,
        httpClient: mockClient,
      );

      // Attempt submission during network drop
      final result = await attemptService.submitAttempt(
        submission: AttemptSubmission(
          problemId: 'P_OFFLINE',
          submittedAnswer: '10',
          elapsedMs: 1200,
          hintCount: 0,
          retryCount: 0,
          sessionId: 'sess_offline',
          submittedAt: DateTime.now(),
        ),
        localJudgement: true,
      );

      expect(result.isOffline, isTrue);
      expect(result.isCorrect, isTrue);

      // Verify queued in SharedPreferences
      final queued = prefs.getStringList(BackendAttemptService.offlineQueueKey);
      expect(queued?.length, equals(1));

      // Now sync queue when online
      final syncedCount = await attemptService.syncOfflineQueue();
      expect(syncedCount, equals(1));

      final remaining = prefs.getStringList(BackendAttemptService.offlineQueueKey);
      expect(remaining?.isEmpty, isTrue);
    });
  });

  group('DiagnosticScreen & DiagnosticsClientService Tests', () {
    testWidgets('renders unauthenticated prompt when user is not logged in',
        (tester) async {
      final authService = AuthService(baseUrl: 'http://test-server');
      final diagnosticsService = DiagnosticsClientService(authService: authService);
      final contentRepository = ContentRepository.bundledAssets();
      final progressRepository = LocalProgressRepository();

      await tester.pumpWidget(
        MaterialApp(
          home: DiagnosticScreen(
            authService: authService,
            diagnosticsService: diagnosticsService,
            contentRepository: contentRepository,
            progressRepository: progressRepository,
          ),
        ),
      );

      expect(find.textContaining('로그인하고 나만의 수학 진단을 받아보세요'), findsOneWidget);
      expect(find.byType(FilledButton), findsOneWidget);
    });

    testWidgets('renders diagnostic metrics and recommendations when authenticated',
        (tester) async {
      http.Response jsonResponse(dynamic data, int status) {
        return http.Response.bytes(
          utf8.encode(jsonEncode(data)),
          status,
          headers: {'content-type': 'application/json; charset=utf-8'},
        );
      }

      final mockClient = MockClient((request) async {
        if (request.url.path == '/api/v1/diagnostics/summary/') {
          return jsonResponse({
            'total_problems': 5,
            'total_attempts': 8,
            'accuracy': 0.85,
            'avg_elapsed_ms': 12000,
            'hint_rate': 0.25,
            'avg_retry_count': 0.5,
            'strengths': [
              {'key': 'arithmetic.multiplication', 'name_ko': '곱셈', 'score': 0.90}
            ],
            'weaknesses': [
              {'key': 'arithmetic.division', 'name_ko': '나눗셈', 'score': 0.50}
            ],
            'insufficient_data': [],
            'recent_trend': {
              'direction': 'improving',
              'message': '최근 정답률이 크게 오르고 있어요!',
            },
            'headline': "'곱셈' 개념에 강점을 보이고 있어요!",
          }, 200);
        } else if (request.url.path == '/api/v1/diagnostics/concepts/') {
          return jsonResponse([
            {
              'key': 'arithmetic.multiplication',
              'name_ko': '곱셈',
              'domain': '수와 연산',
              'description': '곱셈의 기본 개념',
              'score': 0.90,
              'raw_accuracy': 0.90,
              'attempt_count': 5,
              'correct_count': 4,
              'confidence': 1.0,
              'status': 'stable',
              'status_label': '혼자서도 척척',
              'status_message': '개념을 깊이 이해하고 스스로 잘 해결해요.',
            }
          ], 200);
        } else if (request.url.path == '/api/v1/diagnostics/skills/') {
          return jsonResponse([
            {
              'key': 'skill.calculate',
              'name_ko': '계산 수행',
              'domain': '수와 연산',
              'description': '사칙연산 계산하기',
              'score': 0.88,
              'raw_accuracy': 0.88,
              'attempt_count': 5,
              'correct_count': 4,
              'confidence': 1.0,
              'status': 'stable',
              'status_label': '혼자서도 척척',
              'status_message': '스스로 계산을 잘 수행해요.',
            }
          ], 200);
        } else if (request.url.path == '/api/v1/recommendations/') {
          return jsonResponse([
            {
              'problem': {
                'id': 1,
                'problem_id': 'P_REC_1',
                'title': '나눗셈 연습 문제',
                'grade': 3,
                'problem_type': 'choice',
                'unit': '나눗셈',
                'domain': '수와 연산',
              },
              'reason': '취약했던 나눗셈 개념을 보완하는 문제예요.',
              'priority': 1,
              'current_mastery': {'status_label': '도움이 필요해요'},
            }
          ], 200);
        }
        return http.Response('Not Found', 404);
      });

      final authService = AuthService(
        baseUrl: 'http://test-server',
        httpClient: mockClient,
      );
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString(AuthService.tokenStorageKey, 'valid_token');
      await prefs.setString(
        AuthService.userStorageKey,
        jsonEncode(const AuthUser(id: 1, username: 'test_user', email: 'test@example.com').toJson()),
      );
      await authService.restoreSession();

      final diagnosticsService = DiagnosticsClientService(
        authService: authService,
        httpClient: mockClient,
      );
      final contentRepository = ContentRepository.bundledAssets();
      final progressRepository = LocalProgressRepository();

      await tester.pumpWidget(
        MaterialApp(
          home: DiagnosticScreen(
            authService: authService,
            diagnosticsService: diagnosticsService,
            contentRepository: contentRepository,
            progressRepository: progressRepository,
          ),
        ),
      );

      await tester.pumpAndSettle();

      expect(find.textContaining("'곱셈' 개념에 강점을 보이고 있어요!"), findsOneWidget);
      expect(find.text('85%'), findsOneWidget); // accuracy
      expect(find.text('12초'), findsOneWidget); // solve time
      expect(find.textContaining('나의 강점 개념'), findsOneWidget);
      expect(find.textContaining('보완하면 좋은 개념'), findsOneWidget);
      expect(find.text('개념별 숙련도 분석'), findsOneWidget);
      expect(find.text('문제해결 역량·기능 분석'), findsOneWidget);
      expect(find.text('진단 기반 맞춤 추천 문제'), findsOneWidget);
      expect(find.text('바로 풀기'), findsOneWidget);
    });
  });
}
