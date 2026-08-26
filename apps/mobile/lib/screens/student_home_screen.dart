import 'dart:ui';
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
import 'problem_solve_screen.dart';
import 'review_note_screen.dart';

class StudentHomeScreen extends StatefulWidget {
  const StudentHomeScreen({
    super.key,
    required this.repository,
    required this.progressRepository,
  });

  final ContentRepository repository;
  final LearningProgressRepository progressRepository;

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
    _loadData();
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final locale = AppLocaleScope.maybeOf(context)?.locale.languageCode ?? 'ko';
    if (_activeProblemLocale == locale) {
      return;
    }
    final previousLocale = _activeProblemLocale;
    _activeProblemLocale = locale;
    widget.repository.activeProblemLocale = locale;
    if (previousLocale == null) {
      return;
    }
    setState(_loadData);
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
              return const OnsemLoadingIndicator(label: '오늘의 문제를 고르고 있어요');
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
                  final horizontal = wide ? 28.0 : 16.0;

                  return ListView(
                    padding:
                        EdgeInsets.fromLTRB(horizontal, 16, horizontal, 32),
                    children: [
                      _TopNavigation(
                        onReview: _openReview,
                        onProgress: _openProgress,
                      ),
                      const SizedBox(height: 18),
                      _TodayCard(
                        wide: wide,
                        profile: profile,
                        dailySummary: dailySummary,
                        nextProblem: nextProblem,
                        onStart: recommendations.isEmpty
                            ? null
                            : () => _startDailyChallenge(recommendations),
                        onCurriculum: _openCurriculum,
                      ),
                      const SizedBox(height: 22),
                      _UnitRail(
                        problems: manifest.problems,
                        onOpenUnit: (unit, {subUnit}) =>
                            _openCurriculum(initialUnit: unit, subUnit: subUnit),
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
    await Navigator.of(context).pushNamed(ModuMathRoutes.progress);
    _refresh();
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
  });

  final VoidCallback onReview;
  final VoidCallback onProgress;

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    return Container(
      height: 64,
      padding: const EdgeInsets.symmetric(horizontal: 16),
      decoration: BoxDecoration(
        color: KidsPalette.paper,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: KidsPalette.line),
      ),
      child: Row(
        children: [
          const Icon(Icons.school_rounded, color: KidsPalette.ink, size: 28),
          const SizedBox(width: 10),
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
      profile: profile,
      dailySummary: dailySummary,
      onStart: onStart,
      onCurriculum: onCurriculum,
    );
    final problemCard = _NextProblemCard(problem: nextProblem);

    return Container(
      padding: EdgeInsets.all(wide ? 28 : 20),
      decoration: BoxDecoration(
        color: const Color(0xFFF7F8FC),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: KidsPalette.line),
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
    required this.profile,
    required this.dailySummary,
    required this.onStart,
    required this.onCurriculum,
  });

  final StudentProfile profile;
  final DailySummary dailySummary;
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
              ),
        ),
        const SizedBox(height: 14),
        Text(
          strings.t('home.heroSubtitle', {
            'grade': profile.grade,
            'name': profile.name,
          }),
          style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                color: KidsPalette.cocoaSoft,
                height: 1.5,
              ),
        ),
        const SizedBox(height: 18),
        _HeroStats(
          solved: dailySummary.totalAttempted,
          target: profile.targetDailyCount,
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
                  backgroundColor: KidsPalette.paper,
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
        color: KidsPalette.paper,
        borderRadius: BorderRadius.circular(999),
        border: Border.all(color: KidsPalette.line),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(label, style: Theme.of(context).textTheme.bodySmall),
          const SizedBox(width: 8),
          Text(value, style: Theme.of(context).textTheme.labelLarge),
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
        borderRadius: BorderRadius.circular(16),
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
                  : strings.unitTitle(problem!.unit),
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 6),
            Text(
              problem?.title ?? strings.t('home.recommendationLoading'),
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

class _UnitRail extends StatefulWidget {
  const _UnitRail({
    required this.problems,
    required this.onOpenUnit,
  });

  final List<ProblemSummary> problems;
  final SubUnitOpener onOpenUnit;

  @override
  State<_UnitRail> createState() => _UnitRailState();
}

class _UnitRailState extends State<_UnitRail> {
  final ScrollController _scrollController = ScrollController();
  bool _canScrollLeft = false;
  bool _canScrollRight = true;

  @override
  void initState() {
    super.initState();
    _scrollController.addListener(_updateScrollButtons);
    WidgetsBinding.instance.addPostFrameCallback((_) => _updateScrollButtons());
  }

  void _updateScrollButtons() {
    if (!_scrollController.hasClients) return;
    final maxScroll = _scrollController.position.maxScrollExtent;
    final currentScroll = _scrollController.offset;
    final canLeft = currentScroll > 8;
    final canRight = currentScroll < maxScroll - 8;
    if (canLeft != _canScrollLeft || canRight != _canScrollRight) {
      if (mounted) {
        setState(() {
          _canScrollLeft = canLeft;
          _canScrollRight = canRight;
        });
      }
    }
  }

  void _scroll(double delta) {
    if (!_scrollController.hasClients) return;
    final target = (_scrollController.offset + delta)
        .clamp(0.0, _scrollController.position.maxScrollExtent);
    _scrollController.animateTo(
      target,
      duration: const Duration(milliseconds: 300),
      curve: Curves.easeOutCubic,
    );
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    final unitGroups = <String, List<ProblemSummary>>{};
    for (final problem in widget.problems) {
      unitGroups.putIfAbsent(problem.unit, () => []).add(problem);
    }
    final items = unitGroups.entries.map((entry) {
      final sample = entry.value.first;
      return _UnitItem(
        unit: sample.unit,
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

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              strings.t('home.unitLearning'),
              style: Theme.of(context).textTheme.titleLarge,
            ),
            Row(
              children: [
                IconButton.filledTonal(
                  icon: const Icon(Icons.chevron_left_rounded, size: 20),
                  tooltip: '이전 단원',
                  onPressed: _canScrollLeft ? () => _scroll(-300) : null,
                ),
                const SizedBox(width: 8),
                IconButton.filledTonal(
                  icon: const Icon(Icons.chevron_right_rounded, size: 20),
                  tooltip: '다음 단원',
                  onPressed: _canScrollRight ? () => _scroll(300) : null,
                ),
              ],
            ),
          ],
        ),
        const SizedBox(height: 12),
        SizedBox(
          height: 172,
          child: ScrollConfiguration(
            behavior: ScrollConfiguration.of(context).copyWith(
              dragDevices: {
                PointerDeviceKind.touch,
                PointerDeviceKind.mouse,
                PointerDeviceKind.trackpad,
                PointerDeviceKind.stylus,
              },
            ),
            child: Scrollbar(
              controller: _scrollController,
              thumbVisibility: true,
              child: ListView.separated(
                controller: _scrollController,
                scrollDirection: Axis.horizontal,
                padding: const EdgeInsets.only(bottom: 12, right: 24),
                itemCount: items.length,
                separatorBuilder: (context, index) => const SizedBox(width: 12),
                itemBuilder: (context, index) {
                  final item = items[index];
                  return _UnitTile(
                    item: item,
                    onTap: () => widget.onOpenUnit(item.unit),
                  );
                },
              ),
            ),
          ),
        ),
      ],
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
    final badgeLabel = '${item.semester} ${item.unitNumber}단원';
    final titleLabel = '${item.unitNumber}. ${item.unitTopic}';
    return SizedBox(
      width: 260,
      child: Card(
        margin: EdgeInsets.zero,
        child: InkWell(
          borderRadius: BorderRadius.circular(16),
          onTap: onTap,
          child: Padding(
            padding: const EdgeInsets.all(18),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
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
                  strings.unitTitle(titleLabel),
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
                    const Icon(Icons.chevron_right_rounded, color: KidsPalette.sage),
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
