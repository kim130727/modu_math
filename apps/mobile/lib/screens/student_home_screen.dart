import 'package:flutter/material.dart';

import '../app/router.dart';
import '../models/content_models.dart';
import '../models/learning_progress.dart';
import '../models/student_profile.dart';
import '../l10n/app_strings.dart';
import '../services/content_repository.dart';
import '../services/learning_progress_repository.dart';
import '../services/recommendation_service.dart';
import '../theme/app_theme.dart';
import '../widgets/onsem_loading_indicator.dart';
import '../services/auth_service.dart';
import '../services/backend_attempt_service.dart';
import '../services/diagnostics_service.dart';
import 'auth_screen.dart';
import 'diagnostic_screen.dart';
import 'problem_solve_screen.dart';
import 'review_note_screen.dart';

class StudentHomeScreen extends StatefulWidget {
  const StudentHomeScreen({
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
  State<StudentHomeScreen> createState() => _StudentHomeScreenState();
}

class _StudentHomeScreenState extends State<StudentHomeScreen> {
  late Future<ProblemManifest> _manifestFuture;
  late Future<StudentProfile> _profileFuture;
  late Future<DailySummary> _dailySummaryFuture;
  late Future<List<RecommendedProblem>> _recommendationsFuture;
  String? _activeProblemLocale;
  final RecommendationService _recommendationService =
      const RecommendationService();

  @override
  void initState() {
    super.initState();
    _activeProblemLocale = widget.repository.activeProblemLocale;
    _loadData();
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final locale = AppLocaleScope.maybeOf(context)?.locale.languageCode ?? 'ko';
    final localeChanged = _activeProblemLocale != locale;
    _activeProblemLocale = locale;
    widget.repository.activeProblemLocale = locale;
    if (localeChanged) {
      setState(_loadData);
    }
  }

  void _loadData() {
    _manifestFuture = widget.repository.loadManifest();
    _profileFuture = widget.progressRepository.getProfile();
    _dailySummaryFuture =
        widget.progressRepository.getDailySummary(DateTime.now());
    _recommendationsFuture = _manifestFuture.then((manifest) {
      return _recommendationService.getDailyRecommendation(
        allProblems: manifest.problems,
        progressRepository: widget.progressRepository,
      );
    });
  }

  void _refresh() {
    setState(_loadData);
  }

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    return Scaffold(
      body: SafeArea(
        child: FutureBuilder<List<dynamic>>(
          future: Future.wait([
            _profileFuture,
            _dailySummaryFuture,
            _manifestFuture,
            _recommendationsFuture,
          ]),
          builder: (context, snapshot) {
            if (snapshot.connectionState != ConnectionState.done) {
              return const OnsemLoadingIndicator(labelKey: 'home.loading');
            }

            if (snapshot.hasError) {
              return _HomeStateMessage(
                icon: Icons.cloud_off_outlined,
                title: strings.t('home.loadErrorTitle'),
                message: '${snapshot.error}',
                actionLabel: strings.t('home.retry'),
                onAction: _refresh,
              );
            }

            final profile = snapshot.data![0] as StudentProfile;
            final dailySummary = snapshot.data![1] as DailySummary;
            final manifest = snapshot.data![2] as ProblemManifest;
            final recommendations =
                snapshot.data![3] as List<RecommendedProblem>;
            final nextProblem =
                recommendations.isEmpty ? null : recommendations.first.problem;

            return RefreshIndicator(
              onRefresh: () async => _refresh(),
              child: LayoutBuilder(
                builder: (context, constraints) {
                  final wide = constraints.maxWidth >= 980;
                  final horizontal =
                      AppLayout.horizontalPadding(constraints.maxWidth);

                  return ListView(
                    padding:
                        EdgeInsets.fromLTRB(horizontal, 12, horizontal, 40),
                    children: [
                      Center(
                        child: ConstrainedBox(
                          constraints: const BoxConstraints(
                            maxWidth: AppLayout.maxContentWidth,
                          ),
                          child: Column(
                            children: [
                              _TopNavigation(
                                onReview: _openReview,
                                onProgress: _openProgress,
                                onAuth: _openAuth,
                                authService: widget.authService,
                              ),
                              const SizedBox(height: 20),
                              _TodayCard(
                                wide: wide,
                                profile: profile,
                                dailySummary: dailySummary,
                                nextProblem: nextProblem,
                                onStart: recommendations.isEmpty
                                    ? null
                                    : () =>
                                        _startDailyChallenge(recommendations),
                                onCurriculum: _openCurriculum,
                              ),
                              const SizedBox(height: 28),
                              _UnitRail(
                                problems: manifest.problems,
                                onOpenUnit: (unit, {subUnit}) =>
                                    _openCurriculum(
                                  initialUnit: unit,
                                  subUnit: subUnit,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ],
                  );
                },
              ),
            );
          },
        ),
      ),
    );
  }

  Future<void> _openReview() async {
    await Navigator.of(context).push(
      MaterialPageRoute<void>(
        builder: (context) => ReviewNoteScreen(
          repository: widget.repository,
          progressRepository: widget.progressRepository,
        ),
      ),
    );
    _refresh();
  }

  Future<void> _openProgress() async {
    if (widget.authService != null && widget.diagnosticsService != null) {
      await Navigator.of(context).push(
        MaterialPageRoute<void>(
          builder: (context) => DiagnosticScreen(
            authService: widget.authService!,
            diagnosticsService: widget.diagnosticsService!,
            contentRepository: widget.repository,
            progressRepository: widget.progressRepository,
          ),
        ),
      );
    } else {
      await Navigator.of(context).pushNamed(ModuMathRoutes.progress);
    }
    _refresh();
  }

  Future<void> _openAuth() async {
    if (widget.authService == null) return;
    if (widget.authService!.isAuthenticated) {
      await showDialog<void>(
        context: context,
        builder: (dialogContext) {
          final strings = AppStrings.of(dialogContext);
          final username = widget.authService!.currentUser?.username ??
              strings.t('auth.learner');
          return AlertDialog(
            title: Text(strings.t('auth.accountTitle', {'username': username})),
            content: Text(strings.t('auth.syncMessage')),
            actions: [
              TextButton(
                onPressed: () => Navigator.of(dialogContext).pop(),
                child: Text(strings.t('common.close')),
              ),
              TextButton(
                onPressed: () async {
                  await widget.authService!.logout();
                  if (!dialogContext.mounted) return;
                  Navigator.of(dialogContext).pop();
                  _refresh();
                },
                child: Text(
                  strings.t('auth.logout'),
                  style: const TextStyle(color: Colors.red),
                ),
              ),
            ],
          );
        },
      );
    } else {
      await Navigator.of(context).push(
        MaterialPageRoute<void>(
          builder: (context) => AuthScreen(authService: widget.authService!),
        ),
      );
      _refresh();
    }
  }

  Future<void> _startDailyChallenge(
    List<RecommendedProblem> recommendations,
  ) async {
    if (recommendations.isEmpty) {
      return;
    }
    final problems = recommendations.map((item) => item.problem).toList();
    await Navigator.of(context).push(
      MaterialPageRoute<void>(
        builder: (context) => ProblemSolveScreen(
          repository: widget.repository,
          progressRepository: widget.progressRepository,
          backendAttemptService: widget.backendAttemptService,
          problem: problems.first,
          unitProblems: problems,
          problemIndex: 0,
        ),
      ),
    );
    _refresh();
  }

  Future<void> _openCurriculum({String? initialUnit, String? subUnit}) async {
    if (subUnit != null && initialUnit != null) {
      await Navigator.of(context).pushNamed(
        ModuMathRoutes.learningSession,
        arguments: LearningSessionRouteArguments(
          unit: initialUnit,
          subUnit: subUnit,
        ),
      );
    } else {
      await Navigator.of(context).pushNamed(
        ModuMathRoutes.curriculum,
        arguments: CurriculumRouteArguments(initialUnit: initialUnit),
      );
    }
    _refresh();
  }
}

class _TopNavigation extends StatelessWidget {
  const _TopNavigation({
    required this.onReview,
    required this.onProgress,
    required this.onAuth,
    this.authService,
  });

  final VoidCallback onReview;
  final VoidCallback onProgress;
  final VoidCallback onAuth;
  final AuthService? authService;

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    final isAuthenticated = authService?.isAuthenticated ?? false;
    final username = authService?.currentUser?.username ??
        strings.t('auth.learner');

    return Container(
      height: 68,
      padding: const EdgeInsets.symmetric(horizontal: 14),
      decoration: BoxDecoration(
        color: KidsPalette.paper,
        borderRadius: BorderRadius.circular(AppRadii.medium),
        border: Border.all(color: KidsPalette.line),
      ),
      child: Row(
        children: [
          Container(
            width: 42,
            height: 42,
            decoration: BoxDecoration(
              color: KidsPalette.primary,
              borderRadius: BorderRadius.circular(13),
            ),
            child: const Icon(
              Icons.school_rounded,
              color: Colors.white,
              size: 24,
            ),
          ),
          const SizedBox(width: 12),
          Text(
            strings.t('app.title'),
            style: Theme.of(context).textTheme.titleLarge?.copyWith(
                  fontWeight: FontWeight.w900,
                ),
          ),
          const Spacer(),
          IconButton(
            tooltip: strings.t('home.reviewTooltip'),
            onPressed: onReview,
            icon: const Icon(Icons.fact_check_outlined),
          ),
          IconButton(
            tooltip: strings.t('home.reportTooltip'),
            onPressed: onProgress,
            icon: const Icon(Icons.bar_chart_rounded),
          ),
          IconButton(
            tooltip: isAuthenticated
                ? strings.t('auth.manageAccount', {'username': username})
                : strings.t('auth.login'),
            onPressed: onAuth,
            icon: Icon(
              isAuthenticated ? Icons.account_circle : Icons.account_circle_outlined,
              color: isAuthenticated ? KidsPalette.primary : KidsPalette.cocoaSoft,
            ),
          ),
          const SizedBox(width: 44),
        ],
      ),
    );
  }
}

class _TodayCard extends StatelessWidget {
  const _TodayCard({
    required this.wide,
    required this.profile,
    required this.dailySummary,
    required this.nextProblem,
    required this.onStart,
    required this.onCurriculum,
  });

  final bool wide;
  final StudentProfile profile;
  final DailySummary dailySummary;
  final ProblemSummary? nextProblem;
  final VoidCallback? onStart;
  final VoidCallback onCurriculum;

  @override
  Widget build(BuildContext context) {
    final copy = _TodayCopy(
      dailySummary: dailySummary,
      dailyTarget: profile.targetDailyCount,
      onStart: onStart,
      onCurriculum: onCurriculum,
    );
    final problemCard = _NextProblemCard(problem: nextProblem);

    return Container(
      padding: EdgeInsets.all(wide ? 36 : 22),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [Color(0xFF312E81), Color(0xFF4F46E5)],
        ),
        borderRadius: BorderRadius.circular(AppRadii.extraLarge),
        border: Border.all(color: const Color(0xFF6366F1)),
      ),
      child: wide
          ? Row(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Expanded(flex: 5, child: copy),
                const SizedBox(width: 24),
                Expanded(flex: 4, child: problemCard),
              ],
            )
          : Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                copy,
                const SizedBox(height: 16),
                problemCard,
              ],
            ),
    );
  }
}

class _TodayCopy extends StatelessWidget {
  const _TodayCopy({
    required this.dailySummary,
    required this.dailyTarget,
    required this.onStart,
    required this.onCurriculum,
  });

  final DailySummary dailySummary;
  final int dailyTarget;
  final VoidCallback? onStart;
  final VoidCallback onCurriculum;

  @override
  Widget build(BuildContext context) {
    final compactType = MediaQuery.sizeOf(context).width < 460;
    final strings = AppStrings.of(context);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          strings.t('home.heroTitle'),
          style: Theme.of(context).textTheme.displaySmall?.copyWith(
                fontSize: compactType ? 32 : 42,
                letterSpacing: 0,
                color: Colors.white,
              ),
        ),
        const SizedBox(height: 14),
        Text(
          strings.t('home.heroSubtitle'),
          style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                color: const Color(0xFFE0E7FF),
                height: 1.5,
              ),
        ),
        const SizedBox(height: 18),
        _HeroStats(
          solved: dailySummary.totalAttempted,
          target: dailyTarget,
          accuracy: dailySummary.accuracy,
        ),
        const SizedBox(height: 22),
        ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 420),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              FilledButton.icon(
                onPressed: onStart,
                icon: const Icon(Icons.play_arrow_rounded),
                style: FilledButton.styleFrom(
                  minimumSize: const Size.fromHeight(56),
                  backgroundColor: Colors.white,
                  foregroundColor: KidsPalette.primaryDark,
                ),
                label: Text(
                  strings.t('home.startToday'),
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.w900,
                  ),
                ),
              ),
              const SizedBox(height: 10),
              OutlinedButton.icon(
                onPressed: onCurriculum,
                icon: const Icon(Icons.list_alt_rounded),
                style: OutlinedButton.styleFrom(
                  backgroundColor: Colors.transparent,
                  foregroundColor: Colors.white,
                  side: const BorderSide(color: Color(0xFFA5B4FC)),
                  minimumSize: const Size.fromHeight(52),
                ),
                label: Text(
                  strings.t('home.chooseUnit'),
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w800,
                  ),
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }
}

class _HeroStats extends StatelessWidget {
  const _HeroStats({
    required this.solved,
    required this.target,
    required this.accuracy,
  });

  final int solved;
  final int target;
  final double accuracy;

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    return Wrap(
      spacing: 10,
      runSpacing: 10,
      children: [
        _StatPill(label: strings.t('home.today'), value: '$solved/$target'),
        _StatPill(
          label: strings.t('home.accuracy'),
          value: '${(accuracy * 100).round()}%',
        ),
      ],
    );
  }
}

class _StatPill extends StatelessWidget {
  const _StatPill({
    required this.label,
    required this.value,
  });

  final String label;
  final String value;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
      decoration: BoxDecoration(
        color: Colors.white.withValues(alpha: 0.12),
        borderRadius: BorderRadius.circular(999),
        border: Border.all(color: Colors.white.withValues(alpha: 0.22)),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(
            label,
            style: Theme.of(context).textTheme.bodySmall?.copyWith(
                  color: const Color(0xFFE0E7FF),
                ),
          ),
          const SizedBox(width: 8),
          Text(
            value,
            style: Theme.of(context).textTheme.labelLarge?.copyWith(
                  color: Colors.white,
                ),
          ),
        ],
      ),
    );
  }
}

class _NextProblemCard extends StatelessWidget {
  const _NextProblemCard({required this.problem});

  final ProblemSummary? problem;

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    return DecoratedBox(
      decoration: BoxDecoration(
        color: KidsPalette.paper,
        borderRadius: BorderRadius.circular(AppRadii.large),
        border: Border.all(color: KidsPalette.line),
      ),
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisSize: MainAxisSize.min,
          children: [
            Row(
              children: [
                const SizedBox(
                  width: 48,
                  height: 48,
                  child: DecoratedBox(
                    decoration: BoxDecoration(
                      color: KidsPalette.sage,
                      borderRadius: BorderRadius.all(Radius.circular(12)),
                    ),
                    child: Icon(Icons.functions_rounded, color: Colors.white),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Text(
                    strings.t('home.nextProblem'),
                    style: Theme.of(context).textTheme.labelLarge?.copyWith(
                          color: KidsPalette.sage,
                        ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 14),
            Text(
              problem == null
                  ? strings.t('home.todayProblem')
                  : '${strings.domainTitle(problem!.unitTopic)} · ${strings.unitTitle(problem!.unitTopic)}',
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 6),
            Text(
              problem == null
                  ? strings.t('home.recommendationLoading')
                  : strings.problemTitleById(problem!.id, problem!.title),
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    color: KidsPalette.cocoaSoft,
                  ),
            ),
          ],
        ),
      ),
    );
  }
}

typedef SubUnitOpener = void Function(String unit, {String? subUnit});

class _UnitItem {
  const _UnitItem({
    required this.unit,
    required this.unitTopic,
    required this.semester,
    required this.unitNumber,
    required this.count,
  });

  final String unit;
  final String unitTopic;
  final String semester;
  final int unitNumber;
  final int count;
}

class _UnitRail extends StatelessWidget {
  const _UnitRail({
    required this.problems,
    required this.onOpenUnit,
  });

  final List<ProblemSummary> problems;
  final SubUnitOpener onOpenUnit;

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    final unitGroups = <String, List<ProblemSummary>>{};
    for (final problem in problems) {
      unitGroups.putIfAbsent(problem.unitTopic, () => []).add(problem);
    }
    final items = unitGroups.entries.map((entry) {
      final sample = entry.value.first;
      return _UnitItem(
        unit: sample.unitTopic,
        unitTopic: sample.unitTopic,
        semester: sample.semester,
        unitNumber: sample.unitNumber,
        count: entry.value.length,
      );
    }).toList()
      ..sort((a, b) {
        final semCmp = a.semester.compareTo(b.semester);
        if (semCmp != 0) {
          return semCmp;
        }
        return a.unitNumber.compareTo(b.unitNumber);
      });

    return LayoutBuilder(
      builder: (context, constraints) {
        final columns = constraints.maxWidth >= 900
            ? 3
            : constraints.maxWidth >= 600
                ? 2
                : 1;
        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              strings.t('home.unitLearning'),
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            const SizedBox(height: 16),
            GridView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: columns,
                mainAxisExtent: 176,
                crossAxisSpacing: 16,
                mainAxisSpacing: 16,
              ),
              itemCount: items.length,
              itemBuilder: (context, index) {
                final item = items[index];
                return _UnitTile(
                  item: item,
                  onTap: () => onOpenUnit(item.unit),
                );
              },
            ),
          ],
        );
      },
    );
  }
}

class _UnitTile extends StatelessWidget {
  const _UnitTile({
    required this.item,
    required this.onTap,
  });

  final _UnitItem item;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    final badgeLabel = strings.domainTitle(item.unitTopic);
    final titleLabel = strings.unitTitle(item.unitTopic);
    return SizedBox(
      width: 260,
      child: Card(
        margin: EdgeInsets.zero,
        child: InkWell(
          borderRadius: BorderRadius.circular(AppRadii.large),
          onTap: onTap,
          child: Padding(
            padding: const EdgeInsets.all(18),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: const Color(0xFFECEEFF),
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: Text(
                    badgeLabel,
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: const TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.w700,
                      color: KidsPalette.sage,
                    ),
                  ),
                ),
                const SizedBox(height: 10),
                Text(
                  titleLabel,
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                ),
                const Spacer(),
                Row(
                  children: [
                    Text(
                      strings.t('home.problemCount', {'count': item.count}),
                      style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                            color: KidsPalette.cocoaSoft,
                            fontWeight: FontWeight.w600,
                          ),
                    ),
                    const Spacer(),
                    const Icon(Icons.chevron_right_rounded,
                        color: KidsPalette.sage),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _HomeStateMessage extends StatelessWidget {
  const _HomeStateMessage({
    required this.icon,
    required this.title,
    required this.message,
    required this.actionLabel,
    required this.onAction,
  });

  final IconData icon;
  final String title;
  final String message;
  final String actionLabel;
  final VoidCallback onAction;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, size: 42, color: KidsPalette.cocoaSoft),
            const SizedBox(height: 12),
            Text(title, style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 6),
            Text(
              message,
              textAlign: TextAlign.center,
              style: Theme.of(context).textTheme.bodySmall,
            ),
            const SizedBox(height: 16),
            OutlinedButton(onPressed: onAction, child: Text(actionLabel)),
          ],
        ),
      ),
    );
  }
}
