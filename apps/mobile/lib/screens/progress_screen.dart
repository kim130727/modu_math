import 'package:flutter/material.dart';

import '../services/learning_progress_repository.dart';
import 'learning_report_screen.dart';

class ProgressScreen extends StatelessWidget {
  const ProgressScreen({
    super.key,
    required this.progressRepository,
  });

  final LearningProgressRepository progressRepository;

  @override
  Widget build(BuildContext context) {
    return LearningReportScreen(progressRepository: progressRepository);
  }
}
