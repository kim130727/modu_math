import 'dart:async';

import 'package:flutter/material.dart';

import '../l10n/app_strings.dart';
import '../models/content_models.dart';
import '../services/answer_diagnostic_service.dart';
import '../services/content_repository.dart';
import '../services/learning_progress_repository.dart';
import '../services/solvable_hint_service.dart';
import '../utils/answer_normalizer.dart';
import '../widgets/answer_panel.dart';
import '../widgets/hint_panel.dart';
import '../widgets/onsem_loading_indicator.dart';
import '../widgets/problem_svg_viewer.dart';
import '../widgets/renderer_json_canvas.dart';

class ProblemSolveScreen extends StatefulWidget {
  const ProblemSolveScreen({
    super.key,
    required this.repository,
    this.progressRepository,
    required this.problem,
    this.unitProblems = const [],
    this.problemIndex = 0,
  });

  final ContentRepository repository;
  final LearningProgressRepository? progressRepository;
  final ProblemSummary problem;
  final List<ProblemSummary> unitProblems;
  final int problemIndex;

  @override
  State<ProblemSolveScreen> createState() => _ProblemSolveScreenState();
}

class _ProblemSolveScreenState extends State<ProblemSolveScreen> {
  late Future<ProblemContent> contentFuture;
  final AnswerDiagnosticService answerDiagnosticService =
      const AnswerDiagnosticService();
  final SolvableHintService hintService = const SolvableHintService();
  String? submittedAnswer;
  String answerDraft = '';
  bool? isCorrect;
  int hintLevel = 0;
  String? _activeProblemLocale;
  String? _learningSessionProblemId;
  String? _learningSessionId;
  Future<String?>? _learningSessionFuture;

  @override
  void initState() {
    super.initState();
    contentFuture = _loadContent();
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
      contentFuture = _loadContent();
      submittedAnswer = null;
      answerDraft = '';
      isCorrect = null;
      hintLevel = 0;
      _learningSessionProblemId = null;
      _learningSessionId = null;
      _learningSessionFuture = null;
    });
  }

  Future<ProblemContent> _loadContent() {
    final future = widget.repository.loadProblem(widget.problem);
    unawaited(
      future.then((_) => _preloadUpcomingProblems()).catchError((_) {}),
    );
    return future;
  }

  void _preloadUpcomingProblems() {
    if (!_hasNextProblem) {
      return;
    }
    final end = (widget.problemIndex + 3).clamp(0, widget.unitProblems.length);
    for (var index = widget.problemIndex + 1; index < end; index += 1) {
      unawaited(
        widget.repository
            .preloadProblem(widget.unitProblems[index])
            .catchError((_) {}),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: FutureBuilder<ProblemContent>(
          future: contentFuture,
          builder: (context, snapshot) {
            final strings = AppStrings.of(context);
            return Text(
              snapshot.hasData
                  ? _problemScreenTitle(snapshot.data!, strings)
                  : _problemTitleWithPrefix(
                      widget.problem.id,
                      strings.problemTitle(widget.problem.title),
                    ),
            );
          },
        ),
        toolbarHeight: 72,
      ),
      body: FutureBuilder<ProblemContent>(
        future: contentFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState != ConnectionState.done) {
            return const OnsemLoadingIndicator(label: '다음 문제로 달려가고 있어요');
          }
          if (snapshot.hasError) {
            return _ProblemLoadError(
              error: snapshot.error,
              canOpenPreviousProblem: _hasPreviousProblem,
              canOpenNextProblem: _hasNextProblem,
              onRetry: () {
                setState(() {
                  contentFuture = _loadContent();
                });
              },
              onPreviousProblem:
                  _hasPreviousProblem ? _openPreviousProblem : null,
              onNextProblem: _hasNextProblem ? _openNextProblem : null,
              onBack: () => Navigator.of(context).pop(),
            );
          }

          final content = snapshot.data!;
          unawaited(_ensureLearningSession(content));
          return LayoutBuilder(
            builder: (context, constraints) {
              final wide = constraints.maxWidth >= 960;
              final problemViewer = _ProblemVisual(
                content: content,
                answerDraft: answerDraft,
                onAnswerChanged: _updateAnswerDraft,
              );
              final answerPanel = AnswerPanel(
                content: content,
                answerDraft: answerDraft,
                isCorrect: isCorrect,
                diagnosticFeedback: isCorrect == false
                    ? answerDiagnosticService.feedbackFor(
                        content: content,
                        answer: submittedAnswer ?? answerDraft,
                      )
                    : null,
                onAnswerChanged: _updateAnswerDraft,
                onSubmit: (answer) => _submit(content, answer),
              );
              final hintPanel = HintPanel(
                hints: hintService.buildHints(content),
                visibleLevel: hintLevel,
                onRevealNext: () => _revealNextHint(content),
              );
              final controls = _ProblemControls(
                canOpenPreviousProblem: _hasPreviousProblem,
                canOpenNextProblem: _hasNextProblem,
                onRetry: () => _restartProblem(content),
                onPreviousProblem: _openPreviousProblem,
                onNextProblem: _openNextProblem,
              );

              if (wide) {
                return SafeArea(
                  child: Center(
                    child: ConstrainedBox(
                      constraints: const BoxConstraints(maxWidth: 1480),
                      child: Padding(
                        padding: const EdgeInsets.fromLTRB(24, 8, 24, 28),
                        child: Row(
                          crossAxisAlignment: CrossAxisAlignment.stretch,
                          children: [
                            Expanded(flex: 5, child: problemViewer),
                            const SizedBox(width: 20),
                            Expanded(
                              flex: 4,
                              child: ListView(
                                children: [
                                  answerPanel,
                                  const SizedBox(height: 14),
                                  hintPanel,
                                  const SizedBox(height: 14),
                                  controls,
                                ],
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                );
              }

              return SafeArea(
                child: ListView(
                  padding: const EdgeInsets.fromLTRB(16, 8, 16, 24),
                  children: [
                    SizedBox(height: 340, child: problemViewer),
                    const SizedBox(height: 16),
                    answerPanel,
                    const SizedBox(height: 14),
                    hintPanel,
                    const SizedBox(height: 14),
                    controls,
                  ],
                ),
              );
            },
          );
        },
      ),
    );
  }

  Future<void> _submit(ProblemContent content, String answer) async {
    final correct = isSameAnswer(answer, content.correctAnswer);
    final sessionId = await _ensureLearningSession(content);
    if (sessionId != null) {
      await widget.progressRepository?.recordSessionSubmission(
        sessionId: sessionId,
        answer: answer,
        isCorrect: correct,
      );
    }
    await widget.progressRepository?.recordAttempt(
      problem: content.summary,
      answer: answer,
      isCorrect: correct,
      hintLevelUsed: hintLevel,
    );
    setState(() {
      answerDraft = answer;
      submittedAnswer = answer;
      isCorrect = correct;
    });
  }

  void _restartProblem(ProblemContent content) {
    setState(() {
      submittedAnswer = null;
      answerDraft = '';
      isCorrect = null;
      hintLevel = 0;
      _learningSessionProblemId = null;
      _learningSessionId = null;
      _learningSessionFuture = null;
    });
    unawaited(_ensureLearningSession(content));
  }

  void _updateAnswerDraft(String value) {
    if (answerDraft == value) {
      return;
    }
    setState(() => answerDraft = value);
  }

  Future<String?> _ensureLearningSession(ProblemContent content) async {
    if (widget.progressRepository == null) {
      return null;
    }
    if (_learningSessionProblemId == content.summary.id &&
        _learningSessionId != null) {
      return _learningSessionId;
    }
    final existingFuture = _learningSessionFuture;
    if (_learningSessionProblemId == content.summary.id &&
        existingFuture != null) {
      return existingFuture;
    }
    _learningSessionProblemId = content.summary.id;
    _learningSessionFuture = widget.progressRepository!
        .startLearningSession(
      problem: content.summary,
      skillIds: _skillIdsFromSolvable(content.solvable),
    )
        .then<String?>((session) {
      _learningSessionId = session.sessionId;
      return session.sessionId;
    }).catchError((_) {
      _learningSessionProblemId = null;
      _learningSessionFuture = null;
      return null;
    });
    return _learningSessionFuture;
  }

  Future<void> _revealNextHint(ProblemContent content) async {
    if (hintLevel >= 4) {
      return;
    }
    final nextLevel = hintLevel + 1;
    setState(() => hintLevel = nextLevel);
    final sessionId = await _ensureLearningSession(content);
    if (sessionId != null) {
      await widget.progressRepository?.recordSessionHint(
        sessionId: sessionId,
        level: nextLevel,
      );
    }
  }

  bool get _hasNextProblem {
    return widget.unitProblems.isNotEmpty &&
        widget.problemIndex + 1 < widget.unitProblems.length;
  }

  bool get _hasPreviousProblem {
    return widget.unitProblems.isNotEmpty && widget.problemIndex > 0;
  }

  Future<void> _openPreviousProblem() async {
    if (!_hasPreviousProblem) {
      return;
    }
    final previousIndex = widget.problemIndex - 1;
    _preloadProblemInBackground(widget.unitProblems[previousIndex]);
    Navigator.of(context).pushReplacement(
      MaterialPageRoute<void>(
        builder: (context) => ProblemSolveScreen(
          repository: widget.repository,
          progressRepository: widget.progressRepository,
          problem: widget.unitProblems[previousIndex],
          unitProblems: widget.unitProblems,
          problemIndex: previousIndex,
        ),
      ),
    );
  }

  Future<void> _openNextProblem() async {
    if (!_hasNextProblem) {
      Navigator.of(context).pop();
      return;
    }
    final nextIndex = widget.problemIndex + 1;
    _preloadProblemInBackground(widget.unitProblems[nextIndex]);
    Navigator.of(context).pushReplacement(
      MaterialPageRoute<void>(
        builder: (context) => ProblemSolveScreen(
          repository: widget.repository,
          progressRepository: widget.progressRepository,
          problem: widget.unitProblems[nextIndex],
          unitProblems: widget.unitProblems,
          problemIndex: nextIndex,
        ),
      ),
    );
  }

  void _preloadProblemInBackground(ProblemSummary problem) {
    unawaited(widget.repository.preloadProblem(problem).catchError((_) {}));
  }
}

String _problemScreenTitle(ProblemContent content, AppStrings strings) {
  final fallbackTitle = strings.problemTitle(content.summary.title);
  var title = fallbackTitle;
  final metadata = content.semantic['metadata'];
  if (metadata is Map<String, dynamic>) {
    final metadataTitle = metadata['title']?.toString().trim() ?? '';
    if (metadataTitle.isNotEmpty && !_looksBrokenText(metadataTitle)) {
      title = metadataTitle;
    }
  } else if (content.prompt.isNotEmpty && !_looksBrokenText(content.prompt)) {
    title = content.prompt;
  } else if (content.summary.id.isNotEmpty) {
    title = content.summary.id;
  }
  return _problemTitleWithPrefix(content.summary.id, title);
}

String _problemTitleWithPrefix(String problemId, String title) {
  final normalizedId = problemId.trim();
  final normalizedTitle = title.trim();
  if (normalizedId.isEmpty) {
    return normalizedTitle;
  }
  if (normalizedTitle.isEmpty || normalizedTitle == normalizedId) {
    return normalizedId;
  }
  return '$normalizedId · $normalizedTitle';
}

bool _looksBrokenText(String value) {
  return RegExp(r'[\u3400-\u9FFF\uFFFD]').hasMatch(value) ||
      value.contains('??') ||
      value.contains('�');
}

List<String> _skillIdsFromSolvable(Map<String, dynamic> solvable) {
  final diagnostics = solvable['diagnostics'];
  if (diagnostics is! Map<String, dynamic>) {
    return const [];
  }
  final skills = diagnostics['skills'];
  if (skills is! List) {
    return const [];
  }
  return skills
      .map((skill) => skill.toString().trim())
      .where((skill) => skill.isNotEmpty)
      .toList();
}

class _ProblemControls extends StatelessWidget {
  const _ProblemControls({
    required this.canOpenPreviousProblem,
    required this.canOpenNextProblem,
    required this.onRetry,
    required this.onPreviousProblem,
    required this.onNextProblem,
  });

  final bool canOpenPreviousProblem;
  final bool canOpenNextProblem;
  final VoidCallback onRetry;
  final VoidCallback onPreviousProblem;
  final VoidCallback onNextProblem;

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    return Card(
      margin: EdgeInsets.zero,
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: LayoutBuilder(
          builder: (context, constraints) {
            final previousButton = OutlinedButton.icon(
              onPressed: canOpenPreviousProblem ? onPreviousProblem : null,
              icon: const Icon(Icons.navigate_before),
              label: Text(strings.t('common.previousProblem')),
            );
            final retryButton = OutlinedButton.icon(
              onPressed: onRetry,
              icon: const Icon(Icons.refresh),
              label: Text(strings.t('common.retry')),
            );
            final nextButton = FilledButton.icon(
              onPressed: canOpenNextProblem ? onNextProblem : null,
              icon: const Icon(Icons.navigate_next),
              label: Text(strings.t('common.nextProblem')),
            );
            if (constraints.maxWidth < 520) {
              return Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  previousButton,
                  const SizedBox(height: 10),
                  retryButton,
                  const SizedBox(height: 10),
                  nextButton,
                ],
              );
            }
            return Row(
              children: [
                Expanded(child: previousButton),
                const SizedBox(width: 10),
                Expanded(child: retryButton),
                const SizedBox(width: 10),
                Expanded(child: nextButton),
              ],
            );
          },
        ),
      ),
    );
  }
}

class _ProblemVisual extends StatelessWidget {
  const _ProblemVisual({
    required this.content,
    required this.answerDraft,
    required this.onAnswerChanged,
  });

  final ProblemContent content;
  final String answerDraft;
  final ValueChanged<String> onAnswerChanged;

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    if (content.renderer.isNotEmpty) {
      return Card(
        margin: EdgeInsets.zero,
        child: Padding(
          padding: const EdgeInsets.all(12),
          child: RendererJsonCanvas(
            renderer: content.renderer,
            inputValue: answerDraft,
            expectedAnswer: content.correctAnswer,
            onInputChanged: onAnswerChanged,
          ),
        ),
      );
    }
    if (content.svg.isNotEmpty) {
      return ProblemSvgViewer(svg: content.svg);
    }
    return Card(
      margin: EdgeInsets.zero,
      child: Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Text(strings.t('problem.noVisual')),
        ),
      ),
    );
  }
}

class _ProblemLoadError extends StatelessWidget {
  const _ProblemLoadError({
    required this.error,
    required this.canOpenPreviousProblem,
    required this.canOpenNextProblem,
    required this.onRetry,
    required this.onPreviousProblem,
    required this.onNextProblem,
    required this.onBack,
  });

  final Object? error;
  final bool canOpenPreviousProblem;
  final bool canOpenNextProblem;
  final VoidCallback onRetry;
  final VoidCallback? onPreviousProblem;
  final VoidCallback? onNextProblem;
  final VoidCallback onBack;

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    final textTheme = Theme.of(context).textTheme;
    final colorScheme = Theme.of(context).colorScheme;

    return Center(
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 520),
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Card(
            child: Padding(
              padding: const EdgeInsets.all(22),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Icon(
                    Icons.broken_image_outlined,
                    size: 42,
                    color: colorScheme.primary,
                  ),
                  const SizedBox(height: 14),
                  Text(
                    strings.t('problem.loadErrorTitle'),
                    textAlign: TextAlign.center,
                    style: textTheme.titleMedium,
                  ),
                  const SizedBox(height: 8),
                  Text(
                    strings.t('problem.loadErrorDescription'),
                    textAlign: TextAlign.center,
                    style: textTheme.bodyMedium?.copyWith(
                      color: colorScheme.onSurfaceVariant,
                    ),
                  ),
                  const SizedBox(height: 18),
                  FilledButton.icon(
                    onPressed: onRetry,
                    icon: const Icon(Icons.refresh),
                    label: Text(strings.t('common.reload')),
                  ),
                  if (canOpenPreviousProblem && onPreviousProblem != null) ...[
                    const SizedBox(height: 10),
                    OutlinedButton.icon(
                      onPressed: onPreviousProblem,
                      icon: const Icon(Icons.navigate_before),
                      label: Text(strings.t('common.previousProblem')),
                    ),
                  ],
                  if (canOpenNextProblem && onNextProblem != null) ...[
                    const SizedBox(height: 10),
                    OutlinedButton.icon(
                      onPressed: onNextProblem,
                      icon: const Icon(Icons.navigate_next),
                      label: Text(strings.t('common.nextProblem')),
                    ),
                  ],
                  const SizedBox(height: 10),
                  TextButton(
                    onPressed: onBack,
                    child: Text(strings.t('common.back')),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    '$error',
                    maxLines: 3,
                    overflow: TextOverflow.ellipsis,
                    textAlign: TextAlign.center,
                    style: textTheme.bodySmall,
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
