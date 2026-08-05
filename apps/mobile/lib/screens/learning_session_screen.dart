import 'package:flutter/material.dart';

import '../l10n/app_strings.dart';
import '../models/content_models.dart';
import '../models/learning_progress.dart';
import '../services/content_repository.dart';
import '../services/learning_progress_repository.dart';
import '../theme/app_theme.dart';
import '../widgets/onsem_loading_indicator.dart';
import 'problem_solve_screen.dart';

class LearningSessionScreen extends StatefulWidget {
  const LearningSessionScreen({
    super.key,
    required this.repository,
    required this.progressRepository,
    required this.unit,
  });

  final ContentRepository repository;
  final LearningProgressRepository progressRepository;
  final String unit;

  @override
  State<LearningSessionScreen> createState() => _LearningSessionScreenState();
}

class _LearningSessionScreenState extends State<LearningSessionScreen> {
  late Future<_SessionData> _sessionFuture;
  String? _activeProblemLocale;

  @override
  void initState() {
    super.initState();
    _sessionFuture = _loadSession();
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
      _sessionFuture = _loadSession();
    });
  }

  Future<_SessionData> _loadSession() async {
    final manifest = await widget.repository.loadManifest();
    final attempts = await widget.progressRepository.getAttempts();
    final problems = manifest.problems
        .where((problem) => problem.unit == widget.unit)
        .toList()
      ..sort((a, b) => a.id.compareTo(b.id));
    return _SessionData(problems: problems, attempts: attempts);
  }

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    return Scaffold(
      backgroundColor: KidsPalette.cream,
      appBar: AppBar(
        title: Text(strings.t('session.title')),
      ),
      body: SafeArea(
        child: FutureBuilder<_SessionData>(
          future: _sessionFuture,
          builder: (context, snapshot) {
            if (snapshot.connectionState != ConnectionState.done) {
              return const OnsemLoadingIndicator(label: '학습 순서를 정리하고 있어요');
            }
            if (snapshot.hasError) {
              return Center(
                child: Padding(
                  padding: const EdgeInsets.all(24),
                  child: Text(
                    strings.t('session.loadError', {
                      'error': snapshot.error,
                    }),
                  ),
                ),
              );
            }

            final data = snapshot.data ?? const _SessionData.empty();
            if (data.problems.isEmpty) {
              return Center(child: Text(strings.t('session.empty')));
            }

            final nextIndex = data.nextProblemIndex;
            final nextProblem = data.problems[nextIndex];
            return ListView(
              padding: const EdgeInsets.fromLTRB(20, 16, 20, 28),
              children: [
                _SessionHeader(
                  unit: widget.unit,
                  totalCount: data.problems.length,
                  solvedCount: data.correctProblemIds.length,
                  nextTitle: nextProblem.title,
                  nextProblemName: _problemName(nextProblem),
                  complete: data.isComplete,
                  onStart: () => _startProblem(data, nextIndex),
                ),
                const SizedBox(height: 18),
                _ProblemPreviewList(
                  problems: data.problems,
                  correctProblemIds: data.correctProblemIds,
                  nextProblemId: nextProblem.id,
                  onOpenProblem: (index) => _startProblem(data, index),
                ),
              ],
            );
          },
        ),
      ),
    );
  }

  Future<void> _startProblem(_SessionData data, int problemIndex) async {
    await Navigator.of(context).push(
      MaterialPageRoute<void>(
        builder: (context) => ProblemSolveScreen(
          repository: widget.repository,
          progressRepository: widget.progressRepository,
          problem: data.problems[problemIndex],
          unitProblems: data.problems,
          problemIndex: problemIndex,
        ),
      ),
    );
    if (mounted) {
      setState(() {
        _sessionFuture = _loadSession();
      });
    }
  }
}

class _SessionHeader extends StatelessWidget {
  const _SessionHeader({
    required this.unit,
    required this.totalCount,
    required this.solvedCount,
    required this.nextTitle,
    required this.nextProblemName,
    required this.complete,
    required this.onStart,
  });

  final String unit;
  final int totalCount;
  final int solvedCount;
  final String nextTitle;
  final String nextProblemName;
  final bool complete;
  final VoidCallback onStart;

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    final progress =
        totalCount == 0 ? 0.0 : (solvedCount / totalCount).clamp(0.0, 1.0);

    return DecoratedBox(
      decoration: BoxDecoration(
        color: const Color(0xFFECEEFF),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: KidsPalette.line),
      ),
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Expanded(
                  child: Text(
                    strings.unitTitle(unit),
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                ),
                const SizedBox(width: 12),
                FilledButton.icon(
                  onPressed: onStart,
                  icon: Icon(complete ? Icons.replay : Icons.play_arrow),
                  label: Text(
                    complete
                        ? strings.t('session.retry')
                        : strings.t('session.resume'),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 10),
            LinearProgressIndicator(
              value: progress,
              minHeight: 10,
              borderRadius: BorderRadius.circular(8),
              backgroundColor: KidsPalette.paper,
              color: KidsPalette.sage,
            ),
            const SizedBox(height: 10),
            Text(
              strings.t('session.completedCount', {
                'solved': solvedCount,
                'total': totalCount,
              }),
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    color: KidsPalette.cocoaSoft,
                    fontWeight: FontWeight.w700,
                  ),
            ),
            const SizedBox(height: 14),
            Text(
              complete
                  ? strings.t('session.allComplete')
                  : strings.t('session.nextProblemLabel'),
              style: Theme.of(context).textTheme.labelLarge?.copyWith(
                    color: KidsPalette.sage,
                  ),
            ),
            const SizedBox(height: 4),
            Text(
              nextProblemName,
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 2),
            Text(
              nextTitle,
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    color: KidsPalette.cocoaSoft,
                    fontWeight: FontWeight.w700,
                  ),
            ),
          ],
        ),
      ),
    );
  }
}

class _ProblemPreviewList extends StatelessWidget {
  const _ProblemPreviewList({
    required this.problems,
    required this.correctProblemIds,
    required this.nextProblemId,
    required this.onOpenProblem,
  });

  final List<ProblemSummary> problems;
  final Set<String> correctProblemIds;
  final String nextProblemId;
  final ValueChanged<int> onOpenProblem;

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    return Card(
      margin: EdgeInsets.zero,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: ListView.separated(
        padding: const EdgeInsets.all(8),
        shrinkWrap: true,
        physics: const NeverScrollableScrollPhysics(),
        itemCount: problems.length,
        separatorBuilder: (context, index) => const Divider(height: 1),
        itemBuilder: (context, index) {
          final problem = problems[index];
          final correct = correctProblemIds.contains(problem.id);
          final next = problem.id == nextProblemId;
          return ListTile(
            onTap: () => onOpenProblem(index),
            leading: CircleAvatar(
              backgroundColor: correct
                  ? KidsPalette.mint
                  : next
                      ? const Color(0xFFECEEFF)
                      : KidsPalette.paper,
              foregroundColor: correct
                  ? KidsPalette.success
                  : next
                      ? KidsPalette.sage
                      : KidsPalette.olive,
              child: Icon(
                correct
                    ? Icons.check
                    : next
                        ? Icons.play_arrow
                        : Icons.radio_button_unchecked,
                size: 20,
              ),
            ),
            title: Text(
              '${index + 1}. ${_problemName(problem)}',
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
            subtitle: Text(
              next
                  ? strings.t('session.nextProblemSubtitle', {
                      'title': problem.title,
                    })
                  : problem.title,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
          );
        },
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

class _SessionData {
  const _SessionData({
    required this.problems,
    required this.attempts,
  });

  const _SessionData.empty()
      : problems = const [],
        attempts = const [];

  final List<ProblemSummary> problems;
  final List<StudentAttempt> attempts;

  Set<String> get correctProblemIds {
    return attempts.where((attempt) => attempt.isCorrect).map((attempt) {
      return attempt.problemId;
    }).toSet();
  }

  bool get isComplete {
    return problems.isNotEmpty &&
        problems.every((problem) => correctProblemIds.contains(problem.id));
  }

  int get nextProblemIndex {
    final index = problems.indexWhere((problem) {
      return !correctProblemIds.contains(problem.id);
    });
    return index == -1 ? 0 : index;
  }
}
