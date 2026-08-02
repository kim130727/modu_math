import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

import '../services/content_repository.dart';
import '../services/learning_progress_repository.dart';
import '../services/persistent_progress_repository.dart';
import '../l10n/app_strings.dart';
import '../theme/app_theme.dart';
import '../widgets/language_toggle_button.dart';
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
  Locale _locale = const Locale('ko');

  @override
  void initState() {
    super.initState();
    _contentRepository = widget.contentRepository ?? ContentRepository();
    _contentRepository.activeProblemLocale = _locale.languageCode;
    _progressRepository =
        widget.progressRepository ?? PersistentProgressRepository();
    _router = ModuMathRouter(
      contentRepository: _contentRepository,
      progressRepository: _progressRepository,
    );
  }

  @override
  Widget build(BuildContext context) {
    _contentRepository.activeProblemLocale = _locale.languageCode;
    return AppLocaleScope(
      locale: _locale,
      onLocaleChanged: (locale) {
        setState(() {
          _locale = locale;
          _contentRepository.activeProblemLocale = locale.languageCode;
        });
      },
      child: MaterialApp(
        title: 'Modu Math',
        debugShowCheckedModeBanner: false,
        theme: buildKidsTheme(),
        locale: _locale,
        localizationsDelegates: const [
          AppStringsDelegate(),
          GlobalMaterialLocalizations.delegate,
          GlobalCupertinoLocalizations.delegate,
          GlobalWidgetsLocalizations.delegate,
        ],
        supportedLocales: AppStrings.supportedLocales,
        initialRoute: ModuMathRoutes.home,
        onGenerateRoute: _router.onGenerateRoute,
        builder: (context, child) {
          return Stack(
            children: [
              if (child != null) child,
              const PositionedDirectional(
                top: 8,
                end: 8,
                child: SafeArea(
                  child: LanguageToggleButton(),
                ),
              ),
            ],
          );
        },
      ),
    );
  }
}
