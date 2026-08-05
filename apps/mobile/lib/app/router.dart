import 'package:flutter/material.dart';

import '../screens/curriculum_screen.dart';
import '../screens/home_screen.dart';
import '../screens/json_renderer_preview_screen.dart';
import '../screens/learning_session_screen.dart';
import '../screens/progress_screen.dart';
import '../services/content_repository.dart';
import '../services/learning_progress_repository.dart';

abstract final class ModuMathRoutes {
  static const home = '/';
  static const curriculum = '/curriculum';
  static const learningSession = '/session';
  static const progress = '/progress';
  static const developerStudio = '/dev/studio';
}

class CurriculumRouteArguments {
  const CurriculumRouteArguments({this.initialUnit});

  final String? initialUnit;
}

class LearningSessionRouteArguments {
  const LearningSessionRouteArguments({required this.unit});

  final String unit;
}

class ModuMathRouter {
  const ModuMathRouter({
    required this.contentRepository,
    required this.progressRepository,
  });

  final ContentRepository contentRepository;
  final LearningProgressRepository progressRepository;

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
              )
            : LearningSessionScreen(
                repository: contentRepository,
                progressRepository: progressRepository,
                unit: sessionArguments.unit,
              ),
        ModuMathRoutes.progress => ProgressScreen(
            progressRepository: progressRepository,
          ),
        ModuMathRoutes.developerStudio => JsonRendererPreviewScreen(
            repository: contentRepository,
            progressRepository: progressRepository,
          ),
        _ => HomeScreen(
            repository: contentRepository,
            progressRepository: progressRepository,
          ),
      },
    );
  }
}
