import 'package:flutter/material.dart';

import '../l10n/app_strings.dart';
import '../models/content_models.dart';
import '../models/tutor_models.dart';
import '../services/ai_tutor_service.dart';
import '../services/content_repository.dart';
import '../services/learning_progress_repository.dart';
import '../services/rule_tutor_service.dart';
import '../utils/answer_normalizer.dart';
import '../widgets/problem_svg_viewer.dart';
import '../widgets/renderer_json_canvas.dart';
import '../widgets/tutor_chat_panel.dart';

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
  late AiTutorService tutorService;
  final List<TutorMessage> tutorMessages = [];
  bool tutorBusy = false;
  String? tutorProblemId;
  String? submittedAnswer;
  String answerDraft = '';
  bool? isCorrect;
  int hintLevel = 0;
  int tutorStepIndex = 0;
  String? _activeProblemLocale;

  @override
  void initState() {
    super.initState();
    tutorService = _createTutorService();
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
      tutorProblemId = null;
      tutorMessages.clear();
      submittedAnswer = null;
      answerDraft = '';
      isCorrect = null;
      hintLevel = 0;
      tutorStepIndex = 0;
    });
  }

  Future<ProblemContent> _loadContent() {
    return widget.repository.loadProblem(widget.problem);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.problem.title),
        toolbarHeight: 72,
      ),
      body: FutureBuilder<ProblemContent>(
        future: contentFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState != ConnectionState.done) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            return _ProblemLoadError(
              error: snapshot.error,
              canOpenNextProblem: _hasNextProblem,
              onRetry: () {
                setState(() {
                  contentFuture = _loadContent();
                });
              },
              onNextProblem: _hasNextProblem ? _openNextProblem : null,
              onBack: () => Navigator.of(context).pop(),
            );
          }

          final content = snapshot.data!;
          _ensureTutorSession(content);
          return LayoutBuilder(
            builder: (context, constraints) {
              final wide = constraints.maxWidth >= 960;
              final problemViewer = _ProblemVisual(
                content: content,
                answerDraft: answerDraft,
                onAnswerChanged: _updateAnswerDraft,
              );
              final tutorPanel = TutorChatPanel(
                content: content,
                messages: tutorMessages,
                isBusy: tutorBusy,
                answerDraft: answerDraft,
                submittedAnswer: submittedAnswer,
                isCorrect: isCorrect,
                onAnswerChanged: _updateAnswerDraft,
                onSubmit: (answer) => _submit(content, answer),
                onSend: (message) => _sendTutorMessage(content, message),
                onHint: () => _requestHint(content),
                onNextStep: () => _requestNextStep(content),
                onRestart: () => _restartTutor(content),
                onReset: _resetTutor,
                hasNextProblem: _hasNextProblem,
                onNextProblem: _openNextProblem,
                allowSkipProblem: true,
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
                              child: ListView(children: [tutorPanel]),
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
                    tutorPanel,
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
      if (tutorMessages.isEmpty) {
        tutorMessages.addAll(tutorService.startSession(content));
      }
      tutorMessages.add(tutorService.student(answer));
    });
    await _addTutorReply(
      () => tutorService.reviewAnswer(
        content: content,
        messages: tutorMessages,
        answer: answer,
      ),
    );
  }

  void _ensureTutorSession(ProblemContent content) {
    if (tutorProblemId == content.summary.id) {
      return;
    }
    tutorProblemId = content.summary.id;
    tutorMessages.clear();
    hintLevel = 0;
    tutorStepIndex = 0;
  }

  void _restartTutor(ProblemContent content) {
    setState(() {
      submittedAnswer = null;
      answerDraft = '';
      isCorrect = null;
      tutorMessages.clear();
      tutorMessages.addAll(tutorService.startSession(content));
      tutorProblemId = content.summary.id;
      hintLevel = 0;
      tutorStepIndex = 0;
    });
  }

  void _resetTutor() {
    setState(() {
      tutorMessages.clear();
      tutorProblemId = null;
      submittedAnswer = null;
      answerDraft = '';
      isCorrect = null;
      hintLevel = 0;
      tutorStepIndex = 0;
    });
  }

  void _updateAnswerDraft(String value) {
    if (answerDraft == value) {
      return;
    }
    setState(() => answerDraft = value);
  }

  Future<void> _sendTutorMessage(ProblemContent content, String message) async {
    setState(() {
      tutorMessages.add(tutorService.student(message));
    });
    await _addTutorReply(
      () => tutorService.respondToStudent(
        content: content,
        messages: tutorMessages,
        message: message,
        stepIndex: tutorStepIndex,
      ),
    );
  }

  Future<void> _requestHint(ProblemContent content) async {
    final currentHintLevel = hintLevel;
    setState(() => hintLevel += 1);
    await _addTutorReply(
      () => tutorService.hint(
        content: content,
        messages: tutorMessages,
        hintLevel: currentHintLevel,
      ),
    );
  }

  Future<void> _requestNextStep(ProblemContent content) async {
    final currentStepIndex = tutorStepIndex;
    setState(() => tutorStepIndex += 1);
    await _addTutorReply(
      () => tutorService.nextQuestion(
        content: content,
        messages: tutorMessages,
        stepIndex: currentStepIndex,
      ),
    );
  }

  Future<void> _addTutorReply(Future<TutorMessage> Function() request) async {
    if (tutorBusy) {
      return;
    }
    setState(() => tutorBusy = true);
    try {
      final reply = await request();
      if (!mounted) {
        return;
      }
      setState(() {
        tutorMessages.add(reply);
        tutorBusy = false;
      });
    } catch (_) {
      if (!mounted) {
        return;
      }
      setState(() {
        tutorMessages.add(
          TutorMessage(
            role: TutorMessageRole.tutor,
            text: AppStrings.of(context).t('problem.loadErrorTutor'),
            replyType: TutorReplyType.retry,
            createdAt: DateTime.now(),
          ),
        );
        tutorBusy = false;
      });
    }
  }

  AiTutorService _createTutorService() {
    return const RuleTutorService();
  }

  bool get _hasNextProblem {
    return widget.unitProblems.isNotEmpty &&
        widget.problemIndex + 1 < widget.unitProblems.length;
  }

  void _openNextProblem() {
    if (!_hasNextProblem) {
      Navigator.of(context).pop();
      return;
    }
    final nextIndex = widget.problemIndex + 1;
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
    required this.canOpenNextProblem,
    required this.onRetry,
    required this.onNextProblem,
    required this.onBack,
  });

  final Object? error;
  final bool canOpenNextProblem;
  final VoidCallback onRetry;
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
