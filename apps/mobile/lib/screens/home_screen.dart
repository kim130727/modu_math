import 'package:flutter/material.dart';

import '../services/auth_service.dart';
import '../services/backend_attempt_service.dart';
import '../services/content_repository.dart';
import '../services/diagnostics_service.dart';
import '../services/learning_progress_repository.dart';
import 'student_home_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({
    super.key,
    required this.repository,
    required this.progressRepository,
    this.authService,
    this.diagnosticsService,
    this.backendAttemptService,
  });

  final ContentRepository repository;
  final LearningProgressRepository progressRepository;
  final AuthService? authService;
  final DiagnosticsClientService? diagnosticsService;
  final BackendAttemptService? backendAttemptService;

  @override
  Widget build(BuildContext context) {
    return StudentHomeScreen(
      repository: repository,
      progressRepository: progressRepository,
      authService: authService,
      diagnosticsService: diagnosticsService,
      backendAttemptService: backendAttemptService,
    );
  }
}
