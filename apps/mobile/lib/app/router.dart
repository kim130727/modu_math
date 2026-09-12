import 'package:flutter/material.dart';

import '../screens/auth_screen.dart';
import '../screens/curriculum_screen.dart';
import '../screens/diagnostic_screen.dart';
import '../screens/home_screen.dart';
import '../screens/json_renderer_preview_screen.dart';
import '../screens/learning_session_screen.dart';
import '../screens/progress_screen.dart';
import '../services/auth_service.dart';
import '../services/backend_attempt_service.dart';
import '../services/content_repository.dart';
import '../services/diagnostics_service.dart';
import '../services/learning_progress_repository.dart';

abstract final class ModuMathRoutes {
  static const home = '/';
  static const curriculum = '/curriculum';
  static const learningSession = '/session';
  static const progress = '/progress';
  static const diagnostics = '/diagnostics';
  static const auth = '/auth';
  static const developerStudio = '/dev/studio';
}

class CurriculumRouteArguments {
  const CurriculumRouteArguments({this.initialUnit});

  final String? initialUnit;
}

class LearningSessionRouteArguments {
  const LearningSessionRouteArguments({
    required this.unit,
    this.subUnit,
  });

  final String unit;
  final String? subUnit;
}

class ModuMathRouter {
  const ModuMathRouter({
    required this.contentRepository,
    required this.progressRepository,
    this.authService,
    this.diagnosticsService,
    this.backendAttemptService,
  });

  final ContentRepository contentRepository;
  final LearningProgressRepository progressRepository;
  final AuthService? authService;
  final DiagnosticsClientService? diagnosticsService;
  final BackendAttemptService? backendAttemptService;

  Route<void> onGenerateRoute(RouteSettings settings) {
    final curriculumArguments = settings.arguments is CurriculumRouteArguments
        ? settings.arguments as CurriculumRouteArguments
        : const CurriculumRouteArguments();
    final sessionArguments = settings.arguments is LearningSessionRouteArguments
        ? settings.arguments as LearningSessionRouteArguments
        : null;

    return MaterialPageRoute<void>(
      settings: settings,
      builder: (context) => switch (settings.name) {
        ModuMathRoutes.home => HomeScreen(
            repository: contentRepository,
            progressRepository: progressRepository,
            authService: authService,
            diagnosticsService: diagnosticsService,
            backendAttemptService: backendAttemptService,
          ),
        ModuMathRoutes.curriculum => CurriculumScreen(
            repository: contentRepository,
            progressRepository: progressRepository,
            initialUnit: curriculumArguments.initialUnit,
          ),
        ModuMathRoutes.learningSession => sessionArguments == null
            ? HomeScreen(
                repository: contentRepository,
                progressRepository: progressRepository,
                authService: authService,
                diagnosticsService: diagnosticsService,
                backendAttemptService: backendAttemptService,
              )
            : LearningSessionScreen(
                repository: contentRepository,
                progressRepository: progressRepository,
                unit: sessionArguments.unit,
                subUnit: sessionArguments.subUnit,
              ),
        ModuMathRoutes.progress => ProgressScreen(
            progressRepository: progressRepository,
            authService: authService,
            diagnosticsService: diagnosticsService,
            contentRepository: contentRepository,
          ),
        ModuMathRoutes.diagnostics => (authService != null &&
                diagnosticsService != null)
            ? DiagnosticScreen(
                authService: authService!,
                diagnosticsService: diagnosticsService!,
                contentRepository: contentRepository,
                progressRepository: progressRepository,
              )
            : ProgressScreen(
                progressRepository: progressRepository,
                authService: authService,
                diagnosticsService: diagnosticsService,
                contentRepository: contentRepository,
              ),
        ModuMathRoutes.auth => authService != null
            ? AuthScreen(authService: authService!)
            : HomeScreen(
                repository: contentRepository,
                progressRepository: progressRepository,
                authService: authService,
                diagnosticsService: diagnosticsService,
                backendAttemptService: backendAttemptService,
              ),
        ModuMathRoutes.developerStudio => JsonRendererPreviewScreen(
            repository: contentRepository,
            progressRepository: progressRepository,
          ),
        _ => HomeScreen(
            repository: contentRepository,
            progressRepository: progressRepository,
            authService: authService,
            diagnosticsService: diagnosticsService,
            backendAttemptService: backendAttemptService,
          ),
      },
    );
  }
}
