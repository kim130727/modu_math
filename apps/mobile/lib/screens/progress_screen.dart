import 'package:flutter/material.dart';

import '../services/auth_service.dart';
import '../services/content_repository.dart';
import '../services/diagnostics_service.dart';
import '../services/learning_progress_repository.dart';
import 'diagnostic_screen.dart';
import 'learning_report_screen.dart';

class ProgressScreen extends StatelessWidget {
  const ProgressScreen({
    super.key,
    required this.progressRepository,
    this.authService,
    this.diagnosticsService,
    this.contentRepository,
  });

  final LearningProgressRepository progressRepository;
  final AuthService? authService;
  final DiagnosticsClientService? diagnosticsService;
  final ContentRepository? contentRepository;

  @override
  Widget build(BuildContext context) {
    if (authService != null &&
        diagnosticsService != null &&
        contentRepository != null) {
      return DiagnosticScreen(
        authService: authService!,
        diagnosticsService: diagnosticsService!,
        contentRepository: contentRepository!,
        progressRepository: progressRepository,
      );
    }
    return LearningReportScreen(progressRepository: progressRepository);
  }
}
