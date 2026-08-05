import 'package:flutter/material.dart';

import '../l10n/app_strings.dart';
import '../models/content_models.dart';
import '../models/learning_progress.dart';
import '../services/content_repository.dart';
import '../services/learning_progress_repository.dart';
import '../widgets/onsem_loading_indicator.dart';
import '../widgets/progress_panel.dart';
import 'problem_solve_screen.dart';

class ProblemListScreen extends StatefulWidget {
  const ProblemListScreen({
    super.key,
    required this.repository,
    required this.progressRepository,
    this.initialUnit,
  });

  final ContentRepository repository;
  final LearningProgressRepository progressRepository;
  final String? initialUnit;

  @override
  State<ProblemListScreen> createState() => _ProblemListScreenState();
}

class _ProblemListScreenState extends State<ProblemListScreen> {
  late Future<_ProblemListData> dataFuture;
  String? selectedUnit;
  String? _activeProblemLocale;

  @override
  void initState() {
    super.initState();
    selectedUnit = widget.initialUnit;
    dataFuture = _loadData();
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
    setState(() {
      selectedUnit = null;
      dataFuture = _loadData();
    });
  }

  Future<_ProblemListData> _loadData() async {
    final manifest = await widget.repository.loadManifest();
    final summary = LearningProgressSummary.fromAttempts(
      problems: manifest.problems,
      attempts: await widget.progressRepository.getAttempts(),
    );
    return _ProblemListData(manifest: manifest, summary: summary);
  }

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    return Scaffold(
      appBar: AppBar(
        title: Text(
          selectedUnit == null
              ? strings.t('app.title')
              : strings.unitTitle(selectedUnit!),
        ),
        leading: selectedUnit == null
            ? null
            : IconButton(
                icon: const Icon(Icons.arrow_back),
                onPressed: () => setState(() => selectedUnit = null),
              ),
      ),
      body: FutureBuilder<_ProblemListData>(
        future: dataFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState != ConnectionState.done) {
            return const OnsemLoadingIndicator(label: '문제 목록을 모으고 있어요');
          }
          if (snapshot.hasError) {
            return Center(
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Text(
                  strings.t('problemList.loadError', {
                    'error': snapshot.error,
                  }),
                  style: Theme.of(context).textTheme.bodyLarge,
                ),
              ),
            );
          }

          final data = snapshot.data ?? const _ProblemListData.empty();
          return selectedUnit == null
              ? _UnitOverview(
                  problems: data.manifest.problems,
                  summary: data.summary,
                  onOpenUnit: (unit) => setState(() => selectedUnit = unit),
                )
              : _UnitJourney(
                  problems: data.manifest.problems
                      .where((problem) => problem.unit == selectedUnit)
                      .toList(),
                  summary: data.summary,
                  onOpenProblem: _openProblem,
                );
        },
      ),
    );
  }

  Future<void> _openProblem(ProblemSummary problem) async {
    final data = await dataFuture;
    final unitProblems = selectedUnit == null
        ? const <ProblemSummary>[]
        : (data.manifest.problems
            .where((item) => item.unit == selectedUnit)
            .toList()
          ..sort((a, b) => a.id.compareTo(b.id)));
    final problemIndex =
        unitProblems.indexWhere((item) => item.id == problem.id);
    if (!mounted) {
      return;
    }

    await Navigator.of(context).push(
      MaterialPageRoute<void>(
        builder: (context) => ProblemSolveScreen(
          repository: widget.repository,
          progressRepository: widget.progressRepository,
          problem: problem,
          unitProblems: unitProblems,
          problemIndex: problemIndex < 0 ? 0 : problemIndex,
        ),
      ),
    );
    if (mounted) {
      setState(() {
        dataFuture = _loadData();
      });
    }
  }
}

class _UnitOverview extends StatelessWidget {
  const _UnitOverview({
    required this.problems,
    required this.summary,
    required this.onOpenUnit,
  });

  final List<ProblemSummary> problems;
  final LearningProgressSummary summary;
  final ValueChanged<String> onOpenUnit;

  @override
  Widget build(BuildContext context) {
    final unitGroups = <String, List<ProblemSummary>>{};
    for (final problem in problems) {
      unitGroups.putIfAbsent(problem.unit, () => []).add(problem);
    }
    final units = unitGroups.keys.toList()..sort();

    return LayoutBuilder(
      builder: (context, constraints) {
        final wide = constraints.maxWidth >= 900;
        final grid = GridView.builder(
          padding: const EdgeInsets.all(16),
          itemCount: units.length,
          gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: wide ? 3 : 1,
            mainAxisSpacing: 12,
            crossAxisSpacing: 12,
            childAspectRatio: wide ? 2.4 : 3.2,
          ),
          itemBuilder: (context, index) {
            final unit = units[index];
            final unitProblems = unitGroups[unit] ?? const <ProblemSummary>[];
            return _UnitCard(
              unit: unit,
              count: unitProblems.length,
              onTap: () => onOpenUnit(unit),
            );
          },
        );

        if (!wide) {
          return Column(
            children: [
              ProgressPanel(summary: summary),
              Expanded(child: grid),
            ],
          );
        }

        return Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            SizedBox(
              width: 280,
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: ProgressPanel(summary: summary),
              ),
            ),
            Expanded(child: grid),
          ],
        );
      },
    );
  }
}

class _UnitJourney extends StatelessWidget {
  const _UnitJourney({
    required this.problems,
    required this.summary,
    required this.onOpenProblem,
  });

  final List<ProblemSummary> problems;
  final LearningProgressSummary summary;
  final ValueChanged<ProblemSummary> onOpenProblem;

  @override
  Widget build(BuildContext context) {
    final orderedProblems = [...problems]..sort((a, b) => a.id.compareTo(b.id));
    final firstUnsolved = orderedProblems.indexWhere(
      (problem) => summary.resultFor(problem.id) == null,
    );
    final startIndex = firstUnsolved == -1 ? 0 : firstUnsolved;

    return LayoutBuilder(
      builder: (context, constraints) {
        final wide = constraints.maxWidth >= 900;
        final content = ListView(
          padding: const EdgeInsets.all(16),
          children: [
            _JourneyHeader(
              unit: orderedProblems.isEmpty ? '' : orderedProblems.first.unit,
              count: orderedProblems.length,
              onStart: orderedProblems.isEmpty
                  ? null
                  : () => onOpenProblem(orderedProblems[startIndex]),
              isComplete: firstUnsolved == -1 && orderedProblems.isNotEmpty,
            ),
            const SizedBox(height: 14),
            ...orderedProblems.indexed.map((entry) {
              final index = entry.$1;
              final problem = entry.$2;
              return Padding(
                padding: const EdgeInsets.only(bottom: 10),
                child: _JourneyStepTile(
                  stepNumber: index + 1,
                  problem: problem,
                  result: summary.resultFor(problem.id),
                  onTap: () => onOpenProblem(problem),
                ),
              );
            }),
          ],
        );

        if (!wide) {
          return Column(
            children: [
              ProgressPanel(summary: summary),
              Expanded(child: content),
            ],
          );
        }

        return Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            SizedBox(
              width: 280,
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: ProgressPanel(summary: summary),
              ),
            ),
            Expanded(child: content),
          ],
        );
      },
    );
  }
}

class _JourneyHeader extends StatelessWidget {
  const _JourneyHeader({
    required this.unit,
    required this.count,
    required this.onStart,
    required this.isComplete,
  });

  final String unit;
  final int count;
  final VoidCallback? onStart;
  final bool isComplete;

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    final textTheme = Theme.of(context).textTheme;
    final colorScheme = Theme.of(context).colorScheme;

    return Card(
      margin: EdgeInsets.zero,
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Row(
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(strings.unitTitle(unit), style: textTheme.titleLarge),
                  const SizedBox(height: 8),
                  Text(
                    strings.t('problemList.journeyDescription', {
                      'count': count,
                    }),
                    style: textTheme.bodyMedium?.copyWith(
                      color: colorScheme.onSurfaceVariant,
                    ),
                  ),
                ],
              ),
            ),
            FilledButton.icon(
              onPressed: onStart,
              icon: Icon(isComplete ? Icons.replay : Icons.play_arrow),
              label: Text(
                isComplete
                    ? strings.t('session.retry')
                    : strings.t('session.resume'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _JourneyStepTile extends StatelessWidget {
  const _JourneyStepTile({
    required this.stepNumber,
    required this.problem,
    required this.result,
    required this.onTap,
  });

  final int stepNumber;
  final ProblemSummary problem;
  final LearningProblemResult? result;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    final colorScheme = Theme.of(context).colorScheme;
    final solved = result != null;
    final color = !solved
        ? colorScheme.secondaryContainer
        : result!.isCorrect
            ? const Color(0xFFDCFCE7)
            : const Color(0xFFFFEDD5);
    final icon = !solved
        ? Icons.radio_button_unchecked
        : result!.isCorrect
            ? Icons.check_circle
            : Icons.refresh;
    final label = !solved
        ? strings.t('problemList.solve')
        : result!.isCorrect
            ? strings.t('problemList.done')
            : strings.t('session.retry');

    return Card(
      margin: EdgeInsets.zero,
      child: InkWell(
        borderRadius: BorderRadius.circular(8),
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              CircleAvatar(
                backgroundColor: color,
                foregroundColor: colorScheme.onSurface,
                child: Text('$stepNumber'),
              ),
              const SizedBox(width: 14),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '$stepNumber. ${_problemName(problem)}',
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                      style: Theme.of(context).textTheme.titleMedium,
                    ),
                    const SizedBox(height: 6),
                    Text(
                      problem.title,
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                      style: TextStyle(
                        color: colorScheme.onSurfaceVariant,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(width: 12),
              Chip(
                avatar: Icon(icon, size: 18),
                label: Text(label),
                backgroundColor: color,
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _UnitCard extends StatelessWidget {
  const _UnitCard({
    required this.unit,
    required this.count,
    required this.onTap,
  });

  final String unit;
  final int count;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    final colorScheme = Theme.of(context).colorScheme;

    return Card(
      margin: EdgeInsets.zero,
      child: InkWell(
        borderRadius: BorderRadius.circular(8),
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(18),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                strings.unitTitle(unit),
                style: Theme.of(context).textTheme.titleLarge,
              ),
              const Spacer(),
              Text(
                strings.problemCount(count),
                style: TextStyle(
                  color: colorScheme.onSurfaceVariant,
                  fontSize: 16,
                  fontWeight: FontWeight.w700,
                ),
              ),
              const SizedBox(height: 10),
              Row(
                children: [
                  Icon(
                    Icons.forum_outlined,
                    color: colorScheme.primary,
                    size: 18,
                  ),
                  const SizedBox(width: 6),
                  Text(
                    strings.t('problemList.startWithTutor'),
                    style: TextStyle(
                      color: colorScheme.onSurfaceVariant,
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}

String _problemName(ProblemSummary problem) {
  final filePrefix = problem.filePrefix?.trim();
  if (filePrefix != null && filePrefix.isNotEmpty) {
    return filePrefix;
  }
  return problem.id;
}

class _ProblemListData {
  const _ProblemListData({
    required this.manifest,
    required this.summary,
  });

  const _ProblemListData.empty()
      : manifest = const ProblemManifest(
          version: '0.0.0',
          problems: [],
          raw: {},
        ),
        summary = const LearningProgressSummary(
          results: [],
        );

  final ProblemManifest manifest;
  final LearningProgressSummary summary;
}
