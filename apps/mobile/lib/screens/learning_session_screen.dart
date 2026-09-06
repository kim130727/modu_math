import 'package:flutter/material.dart';

import '../l10n/app_strings.dart';
import '../models/content_models.dart';
import '../models/learning_progress.dart';
import '../services/content_repository.dart';
import '../services/learning_progress_repository.dart';
import '../theme/app_theme.dart';
import '../widgets/onsem_loading_indicator.dart';
import '../widgets/content_frame.dart';
import 'problem_solve_screen.dart';

class LearningSessionScreen extends StatefulWidget {
  const LearningSessionScreen({
    super.key,
    required this.repository,
    required this.progressRepository,
    required this.unit,
    this.subUnit,
  });

  final ContentRepository repository;
  final LearningProgressRepository progressRepository;
  final String unit;
  final String? subUnit;

  @override
  State<LearningSessionScreen> createState() => _LearningSessionScreenState();
}

class _LearningSessionScreenState extends State<LearningSessionScreen> {
  late Future<_SessionData> _sessionFuture;
  String? _activeProblemLocale;

  @override
  void initState() {
    super.initState();
    _activeProblemLocale = widget.repository.activeProblemLocale;
    _sessionFuture = _loadSession();
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final locale = AppLocaleScope.maybeOf(context)?.locale.languageCode ?? 'ko';
    final localeChanged = _activeProblemLocale != locale;
    _activeProblemLocale = locale;
    widget.repository.activeProblemLocale = locale;
    if (localeChanged) {
      setState(() {
        _sessionFuture = _loadSession();
      });
    }
  }

  bool _matchesUnit(ProblemSummary problem, String targetUnit) {
    final cleanTarget = targetUnit.trim();
    final cleanUnit = problem.unit.trim();
    final cleanTopic = problem.unitTopic.trim();
    if (cleanTarget.isEmpty) return true;
    if (cleanUnit == cleanTarget || cleanTopic == cleanTarget) {
      return true;
    }
    String stripPrefix(String s) {
      return s
          .replaceAll(RegExp(r'^\d+학기\s*'), '')
          .replaceAll(RegExp(r'^\d+[._\s]+'), '')
          .trim();
    }
    final strippedUnit = stripPrefix(cleanUnit);
    final strippedTarget = stripPrefix(cleanTarget);
    if (strippedUnit == strippedTarget ||
        strippedUnit == cleanTarget ||
        cleanTopic == strippedTarget) {
      return true;
    }
    if (cleanUnit.contains(cleanTarget) ||
        cleanTarget.contains(cleanTopic) ||
        cleanTopic.contains(cleanTarget) ||
        strippedUnit.contains(strippedTarget)) {
      return true;
    }
    return false;
  }

  bool _matchesSubUnit(ProblemSummary problem, String? targetSubUnit) {
    if (targetSubUnit == null || targetSubUnit.trim().isEmpty) {
      return true;
    }
    final cleanTarget = targetSubUnit.trim();
    final cleanSub = problem.subUnit.trim();
    if (cleanSub == cleanTarget) {
      return true;
    }
    final isWidgetDefault = cleanTarget == '__basicLearning__' ||
        cleanTarget == '기본 학습' ||
        cleanTarget == 'Basic Learning';
    final isProblemDefault = cleanSub == '__basicLearning__' ||
        cleanSub == '기본 학습' ||
        cleanSub == 'Basic Learning';
    if (isWidgetDefault && isProblemDefault) {
      return true;
    }
    if (isWidgetDefault) {
      return true;
    }
    return cleanSub.contains(cleanTarget) || cleanTarget.contains(cleanSub);
  }

  Future<_SessionData> _loadSession() async {
    final manifest = await widget.repository.loadManifest();
    final attempts = await widget.progressRepository.getAttempts();
    final problems = manifest.problems.where((problem) {
      if (!_matchesUnit(problem, widget.unit)) return false;
      return _matchesSubUnit(problem, widget.subUnit);
    }).toList()
      ..sort(_compareProblemSummaries);
    return _SessionData(problems: problems, attempts: attempts);
  }

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    return Scaffold(
      backgroundColor: KidsPalette.cream,
      appBar: AppBar(
        title: Text(
          widget.subUnit != null
              ? '${strings.unitTitle(widget.unit)} · ${strings.subUnitName(widget.subUnit!)}'
              : strings.unitTitle(widget.unit),
        ),
      ),
      body: SafeArea(
        child: ContentFrame(
          child: FutureBuilder<_SessionData>(
            future: _sessionFuture,
            builder: (context, snapshot) {
              if (snapshot.connectionState != ConnectionState.done) {
                return const OnsemLoadingIndicator(labelKey: 'session.loading');
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
              final localStrings = AppStrings.of(context);
              return ListView(
                padding: const EdgeInsets.fromLTRB(20, 16, 20, 28),
                children: [
                  _SessionHeader(
                    unit: widget.unit,
                    totalCount: data.problems.length,
                    solvedCount: data.correctProblemIds.length,
                    nextTitle: localStrings.problemTitleById(
                        nextProblem.id, nextProblem.title),
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
        gradient: const LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [Color(0xFF312E81), Color(0xFF4F46E5)],
        ),
        borderRadius: BorderRadius.circular(AppRadii.large),
        border: Border.all(color: const Color(0xFF6366F1)),
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
                    style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                          color: Colors.white,
                        ),
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
                  style: FilledButton.styleFrom(
                    backgroundColor: Colors.white,
                    foregroundColor: KidsPalette.primaryDark,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 10),
            ClipRRect(
              borderRadius: BorderRadius.circular(999),
              child: LinearProgressIndicator(
                value: progress,
                minHeight: 12,
                backgroundColor: Colors.white.withValues(alpha: 0.18),
                color: const Color(0xFFA5B4FC),
              ),
            ),
            const SizedBox(height: 10),
            Text(
              strings.t('session.completedCount', {
                'solved': solvedCount,
                'total': totalCount,
              }),
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    color: const Color(0xFFC7D2FE),
                    fontWeight: FontWeight.w700,
                  ),
            ),
            const SizedBox(height: 14),
            Text(
              complete
                  ? strings.t('session.allComplete')
                  : strings.t('session.nextProblemLabel'),
              style: Theme.of(context).textTheme.labelLarge?.copyWith(
                    color: const Color(0xFFA5B4FC),
                  ),
            ),
            const SizedBox(height: 4),
            Text(
              nextProblemName,
              style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    color: Colors.white,
                  ),
            ),
            const SizedBox(height: 2),
            Text(
              nextTitle,
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    color: const Color(0xFFE0E7FF),
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
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(AppRadii.large),
      ),
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
                      'title':
                          strings.problemTitleById(problem.id, problem.title),
                    })
                  : strings.problemTitleById(problem.id, problem.title),
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

int _compareProblemSummaries(ProblemSummary a, ProblemSummary b) {
  return _compareProblemPrefixes(_problemName(a), _problemName(b));
}

int _compareProblemPrefixes(String a, String b) {
  final aParts = _tokenizeForNaturalSort(a);
  final bParts = _tokenizeForNaturalSort(b);
  final length = aParts.length < bParts.length ? aParts.length : bParts.length;
  for (var i = 0; i < length; i += 1) {
    final aPart = aParts[i];
    final bPart = bParts[i];
    final aNumber = int.tryParse(aPart);
    final bNumber = int.tryParse(bPart);
    if (aNumber != null && bNumber != null) {
      final numberComparison = aNumber.compareTo(bNumber);
      if (numberComparison != 0) {
        return numberComparison;
      }
      final lengthComparison = aPart.length.compareTo(bPart.length);
      if (lengthComparison != 0) {
        return lengthComparison;
      }
      continue;
    }
    final textComparison = aPart.compareTo(bPart);
    if (textComparison != 0) {
      return textComparison;
    }
  }
  return aParts.length.compareTo(bParts.length);
}

List<String> _tokenizeForNaturalSort(String value) {
  return RegExp(r'\d+|\D+')
      .allMatches(value)
      .map((match) => match.group(0) ?? '')
      .toList();
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
