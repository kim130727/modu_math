import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/services/app_environment.dart';

void main() {
  tearDown(dotenv.clean);

  test('uses safe defaults before dotenv is initialized', () {
    dotenv.clean();

    expect(AppEnvironment.aiTutorMode, equals('rule'));
    expect(AppEnvironment.backendBaseUrl, isEmpty);
    expect(AppEnvironment.backendSessionToken, isNull);
  });

  test('reads configured environment values after dotenv is initialized', () {
    dotenv.loadFromString(
      envString: [
        'AI_TUTOR_MODE=backend',
        'BACKEND_API_BASE_URL=https://api.example.test',
        'BACKEND_SESSION_TOKEN=session-token',
      ].join('\n'),
    );

    expect(AppEnvironment.aiTutorMode, equals('rule'));
    expect(AppEnvironment.backendBaseUrl, equals('https://api.example.test'));
    expect(AppEnvironment.backendSessionToken, equals('session-token'));
  });
}
