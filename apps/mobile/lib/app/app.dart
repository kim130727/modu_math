import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

import '../l10n/app_strings.dart';
import '../services/auth_service.dart';
import '../services/backend_attempt_service.dart';
import '../services/content_repository.dart';
import '../services/diagnostics_service.dart';
import '../services/learning_progress_repository.dart';
import '../services/persistent_progress_repository.dart';
import '../theme/app_theme.dart';
import '../widgets/language_toggle_button.dart';
import 'router.dart';

class ModuMathApp extends StatefulWidget {
  const ModuMathApp({
    super.key,
    this.contentRepository,
    this.progressRepository,
    this.authService,
    this.diagnosticsService,
    this.backendAttemptService,
  });

  final ContentRepository? contentRepository;
  final LearningProgressRepository? progressRepository;
  final AuthService? authService;
  final DiagnosticsClientService? diagnosticsService;
  final BackendAttemptService? backendAttemptService;

  @override
  State<ModuMathApp> createState() => _ModuMathAppState();
}

class _ModuMathAppState extends State<ModuMathApp> {
  late final ContentRepository _contentRepository;
  late final LearningProgressRepository _progressRepository;
  late final AuthService _authService;
  late final DiagnosticsClientService _diagnosticsService;
  late final BackendAttemptService _backendAttemptService;
  late final ModuMathRouter _router;
  Locale _locale = const Locale('ko');

  @override
  void initState() {
    super.initState();
    _contentRepository = widget.contentRepository ?? ContentRepository();
    _contentRepository.activeProblemLocale = _locale.languageCode;
    _progressRepository =
        widget.progressRepository ?? PersistentProgressRepository();
    _authService = widget.authService ?? AuthService();
    _authService.restoreSession();
    _backendAttemptService = widget.backendAttemptService ??
        BackendAttemptService(authService: _authService);
    _backendAttemptService.syncOfflineQueue();
    _diagnosticsService = widget.diagnosticsService ??
        DiagnosticsClientService(authService: _authService);

    _router = ModuMathRouter(
      contentRepository: _contentRepository,
      progressRepository: _progressRepository,
      authService: _authService,
      diagnosticsService: _diagnosticsService,
      backendAttemptService: _backendAttemptService,
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
