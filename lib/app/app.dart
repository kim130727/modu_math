import 'package:flutter/material.dart';

import '../services/content_repository.dart';
import '../services/learning_progress_repository.dart';
import '../services/persistent_progress_repository.dart';
import '../theme/app_theme.dart';
import 'router.dart';

class ModuMathApp extends StatefulWidget {
  const ModuMathApp({
    super.key,
    this.contentRepository,
    this.progressRepository,
  });

  final ContentRepository? contentRepository;
  final LearningProgressRepository? progressRepository;

  @override
  State<ModuMathApp> createState() => _ModuMathAppState();
}

class _ModuMathAppState extends State<ModuMathApp> {
  late final ContentRepository _contentRepository;
  late final LearningProgressRepository _progressRepository;
  late final ModuMathRouter _router;

  @override
  void initState() {
    super.initState();
    _contentRepository =
        widget.contentRepository ?? ContentRepository.githubExamples();
    _progressRepository =
        widget.progressRepository ?? PersistentProgressRepository();
    _router = ModuMathRouter(
      contentRepository: _contentRepository,
      progressRepository: _progressRepository,
    );
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Modu Math',
      debugShowCheckedModeBanner: false,
      theme: buildKidsTheme(),
      initialRoute: ModuMathRoutes.home,
      onGenerateRoute: _router.onGenerateRoute,
    );
  }
}
