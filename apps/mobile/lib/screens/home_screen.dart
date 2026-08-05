import 'package:flutter/material.dart';

import '../services/content_repository.dart';
import '../services/learning_progress_repository.dart';
import 'student_home_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({
    super.key,
    required this.repository,
    required this.progressRepository,
  });

  final ContentRepository repository;
  final LearningProgressRepository progressRepository;

  @override
  Widget build(BuildContext context) {
    return StudentHomeScreen(
      repository: repository,
      progressRepository: progressRepository,
    );
  }
}
