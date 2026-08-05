import 'dart:convert';
import 'package:flutter/material.dart';

import '../l10n/app_strings.dart';
import '../models/content_models.dart';
import '../models/tutor_models.dart';
import '../services/ai_tutor_service.dart';
import '../services/content_repository.dart';
import '../services/rule_tutor_service.dart';
import '../theme/app_theme.dart';
import '../utils/answer_normalizer.dart';
import '../widgets/onsem_loading_indicator.dart';
import '../widgets/renderer_json_canvas.dart';
import '../widgets/tutor_chat_panel.dart';
import '../services/learning_progress_repository.dart';
import 'problem_list_screen.dart';

class JsonRendererPreviewScreen extends StatefulWidget {
  const JsonRendererPreviewScreen({
    super.key,
    required this.repository,
    required this.progressRepository,
  });

  final ContentRepository repository;
  final LearningProgressRepository progressRepository;

  @override
  State<JsonRendererPreviewScreen> createState() =>
      _JsonRendererPreviewScreenState();
}

class _JsonRendererPreviewScreenState extends State<JsonRendererPreviewScreen> {
  late Future<List<String>> prefixesFuture;
  late Future<ProblemJsonBundle> bundleFuture;
  late AiTutorService tutorService;
  final List<TutorMessage> tutorMessages = [];
  String selectedFilePrefix = '';
  String? tutorProblemId;
  String answerDraft = '';
  String? submittedAnswer;
  bool? isCorrect;
  bool tutorBusy = false;
  int hintLevel = 0;
  int tutorStepIndex = 0;
  String? _activeProblemLocale;

  @override
  void initState() {
    super.initState();
    tutorService = _createTutorService();
    prefixesFuture = widget.repository.loadGrade3JsonProblemPrefixes();
    bundleFuture = _loadInitialBundle();
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
      prefixesFuture = widget.repository.loadGrade3JsonProblemPrefixes();
      bundleFuture = _loadInitialBundle();
      selectedFilePrefix = '';
      tutorProblemId = null;
      tutorMessages.clear();
      submittedAnswer = null;
      answerDraft = '';
      isCorrect = null;
      hintLevel = 0;
      tutorStepIndex = 0;
    });
  }

  Future<ProblemJsonBundle> _loadInitialBundle() async {
    final prefixes = await prefixesFuture;
    if (prefixes.isEmpty) {
      throw StateError(AppStrings.fallback.t('studio.noRenderableProblems'));
    }
    selectedFilePrefix = prefixes.first;
    return widget.repository.loadProblemJsonBundle(selectedFilePrefix);
  }

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 4,
      child: Scaffold(
        body: Stack(
          children: [
            const Positioned.fill(child: _StudioBackdrop()),
            SafeArea(
              child: FutureBuilder<ProblemJsonBundle>(
                future: bundleFuture,
                builder: (context, snapshot) {
                  if (snapshot.connectionState != ConnectionState.done) {
                    return const OnsemLoadingIndicator(label: '미리보기를 준비하고 있어요');
                  }
                  if (snapshot.hasError) {
                    return _LoadError(error: snapshot.error);
                  }

                  final bundle = snapshot.data!;
                  final content = _problemContent(bundle);
                  _ensureTutorSession(content);
                  return Column(
                    children: [
                      _TopBar(
                        bundle: bundle,
                        prefixesFuture: prefixesFuture,
                        selectedFilePrefix: selectedFilePrefix,
                        onSelectPrefix: _selectPrefix,
                        onOpenList: () => Navigator.of(context).push(
                          MaterialPageRoute<void>(
                            builder: (context) => ProblemListScreen(
                              repository: widget.repository,
                              progressRepository: widget.progressRepository,
                            ),
                          ),
                        ),
                      ),
                      const _StudioTabs(),
                      Expanded(
                        child: TabBarView(
                          children: [
                            _RenderTab(
                              bundle: bundle,
                              content: content,
                              tutorPanel: TutorChatPanel(
                                key: ValueKey(bundle.filePrefix),
                                content: content,
                                messages: tutorMessages,
                                isBusy: tutorBusy,
                                answerDraft: answerDraft,
                                submittedAnswer: submittedAnswer,
                                isCorrect: isCorrect,
                                onAnswerChanged: _updateAnswerDraft,
                                onSubmit: (answer) => _submit(content, answer),
                                onSend: (message) =>
                                    _sendTutorMessage(content, message),
                                onHint: () => _requestHint(content),
                                onNextStep: () => _requestNextStep(content),
                                onRestart: () => _restartTutor(content),
                                onReset: _resetTutor,
                                hasNextProblem: false,
                                onNextProblem: () {},
                              ),
                            ),
                            _JsonTab(
                                title: 'semantic.json', data: bundle.semantic),
                            _JsonTab(title: 'layout.json', data: bundle.layout),
                            _JsonTab(
                                title: 'renderer.json', data: bundle.renderer),
                          ],
                        ),
                      ),
                    ],
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _selectPrefix(String prefix) {
    if (prefix == selectedFilePrefix) {
      return;
    }
    setState(() {
      selectedFilePrefix = prefix;
      bundleFuture = widget.repository.loadProblemJsonBundle(prefix);
      tutorProblemId = null;
      tutorMessages.clear();
      submittedAnswer = null;
      answerDraft = '';
      isCorrect = null;
      hintLevel = 0;
      tutorStepIndex = 0;
    });
  }

  ProblemContent _problemContent(ProblemJsonBundle bundle) {
    final metadata = _mapAt(bundle.semantic, 'metadata');
    final type = bundle.semantic['problem_type']?.toString() ?? 'unknown';
    return ProblemContent(
      summary: ProblemSummary(
        id: bundle.filePrefix,
        grade: 3,
        subject: 'math',
        unit: type,
        type: type,
        title: metadata['title']?.toString() ?? bundle.filePrefix,
        path:
            '${ContentRepository.problemsPath}/${widget.repository.activeProblemLocale}',
        filePrefix: bundle.filePrefix,
        raw: bundle.semantic,
      ),
      svg: '',
      semantic: bundle.semantic,
      solvable: bundle.solvable,
    );
  }

  void _ensureTutorSession(ProblemContent content) {
    if (tutorProblemId == content.summary.id) {
      return;
    }
    tutorProblemId = content.summary.id;
    tutorMessages.clear();
  }

  void _restartTutor(ProblemContent content) {
    setState(() {
      tutorMessages.clear();
      tutorMessages.addAll(tutorService.startSession(content));
      tutorProblemId = content.summary.id;
      submittedAnswer = null;
      answerDraft = '';
      isCorrect = null;
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

  Future<void> _submit(ProblemContent content, String answer) async {
    final correct = isSameAnswer(answer, content.correctAnswer);
    await widget.progressRepository.recordAttempt(
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

  void _updateAnswerDraft(String value) {
    if (answerDraft == value) {
      return;
    }
    setState(() => answerDraft = value);
  }

  Future<void> _sendTutorMessage(
    ProblemContent content,
    String message,
  ) async {
    setState(() => tutorMessages.add(tutorService.student(message)));
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

  Future<void> _addTutorReply(
    Future<TutorMessage> Function() request,
  ) async {
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
            text: AppStrings.of(context).t('studio.tutorLoadError'),
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
}

class _TopBar extends StatelessWidget {
  const _TopBar({
    required this.bundle,
    required this.prefixesFuture,
    required this.selectedFilePrefix,
    required this.onSelectPrefix,
    required this.onOpenList,
  });

  final ProblemJsonBundle bundle;
  final Future<List<String>> prefixesFuture;
  final String selectedFilePrefix;
  final ValueChanged<String> onSelectPrefix;
  final VoidCallback onOpenList;

  @override
  Widget build(BuildContext context) {
    final textTheme = Theme.of(context).textTheme;
    final strings = AppStrings.of(context);

    return Padding(
      padding: const EdgeInsets.fromLTRB(24, 18, 24, 10),
      child: Row(
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Modu Math Studio', style: textTheme.displaySmall),
                const SizedBox(height: 6),
                Text(
                  strings.t('studio.description'),
                  style: textTheme.bodyMedium?.copyWith(
                    color: KidsPalette.olive,
                    fontWeight: FontWeight.w700,
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(width: 16),
          _ProblemPrefixPicker(
            prefixesFuture: prefixesFuture,
            selectedFilePrefix: selectedFilePrefix,
            onSelectPrefix: onSelectPrefix,
          ),
          const SizedBox(width: 12),
          _RoundIconButton(
            tooltip: strings.t('studio.problemListTooltip'),
            icon: Icons.list_alt,
            onPressed: onOpenList,
          ),
        ],
      ),
    );
  }
}

class _ProblemPrefixPicker extends StatelessWidget {
  const _ProblemPrefixPicker({
    required this.prefixesFuture,
    required this.selectedFilePrefix,
    required this.onSelectPrefix,
  });

  final Future<List<String>> prefixesFuture;
  final String selectedFilePrefix;
  final ValueChanged<String> onSelectPrefix;

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<String>>(
      future: prefixesFuture,
      builder: (context, snapshot) {
        final prefixes = snapshot.data ?? <String>[selectedFilePrefix];
        final values = prefixes.contains(selectedFilePrefix)
            ? prefixes
            : <String>[selectedFilePrefix, ...prefixes];
        return DecoratedBox(
          decoration: BoxDecoration(
            color: KidsPalette.paper,
            borderRadius: BorderRadius.circular(8),
            border: Border.all(color: KidsPalette.line),
          ),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 12),
            child: DropdownButtonHideUnderline(
              child: DropdownButton<String>(
                value: selectedFilePrefix,
                borderRadius: BorderRadius.circular(8),
                icon: const Icon(Icons.expand_more),
                items: values
                    .map(
                      (prefix) => DropdownMenuItem<String>(
                        value: prefix,
                        child: Text(prefix),
                      ),
                    )
                    .toList(),
                onChanged: (value) {
                  if (value != null) {
                    onSelectPrefix(value);
                  }
                },
              ),
            ),
          ),
        );
      },
    );
  }
}

class _StudioTabs extends StatelessWidget {
  const _StudioTabs();

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 24),
      child: DecoratedBox(
        decoration: BoxDecoration(
          color: const Color(0xFFF1E5C8),
          borderRadius: BorderRadius.circular(999),
        ),
        child: const TabBar(
          indicatorSize: TabBarIndicatorSize.tab,
          dividerColor: Colors.transparent,
          indicator: BoxDecoration(
            color: KidsPalette.butter,
            borderRadius: BorderRadius.all(Radius.circular(999)),
          ),
          tabs: [
            Tab(icon: Icon(Icons.preview), text: 'Render'),
            Tab(icon: Icon(Icons.account_tree_outlined), text: 'Semantic'),
            Tab(icon: Icon(Icons.dashboard_customize_outlined), text: 'Layout'),
            Tab(icon: Icon(Icons.code), text: 'Renderer'),
          ],
        ),
      ),
    );
  }
}

class _RenderTab extends StatelessWidget {
  const _RenderTab({
    required this.bundle,
    required this.content,
    required this.tutorPanel,
  });

  final ProblemJsonBundle bundle;
  final ProblemContent content;
  final Widget tutorPanel;

  @override
  Widget build(BuildContext context) {
    return _RenderTabBody(
      bundle: bundle,
      content: content,
      tutorPanel: tutorPanel,
    );
  }
}

class _RenderTabBody extends StatelessWidget {
  const _RenderTabBody({
    required this.bundle,
    required this.content,
    required this.tutorPanel,
  });

  final ProblemJsonBundle bundle;
  final ProblemContent content;
  final Widget tutorPanel;

  @override
  Widget build(BuildContext context) {
    final metadata = _mapAt(bundle.semantic, 'metadata');

    return LayoutBuilder(
      builder: (context, constraints) {
        final wide = constraints.maxWidth >= 1100;
        final preview = Padding(
          padding: const EdgeInsets.fromLTRB(24, 18, 16, 24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              _HeroPanel(bundle: bundle, instruction: metadata['instruction']),
              const SizedBox(height: 14),
              Expanded(
                child: _CanvasShell(
                  child: RendererJsonCanvas(
                    renderer: bundle.renderer,
                    expectedAnswer: content.correctAnswer,
                  ),
                ),
              ),
            ],
          ),
        );

        final details = Padding(
          padding: EdgeInsets.fromLTRB(wide ? 8 : 24, 18, 24, 24),
          child: ListView(
            children: [tutorPanel],
          ),
        );

        if (!wide) {
          return Column(
            children: [
              Expanded(flex: 3, child: preview),
              Expanded(flex: 2, child: details),
            ],
          );
        }

        return Row(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Expanded(flex: 7, child: preview),
            SizedBox(width: 540, child: details),
          ],
        );
      },
    );
  }
}

class _HeroPanel extends StatelessWidget {
  const _HeroPanel({
    required this.bundle,
    required this.instruction,
  });

  final ProblemJsonBundle bundle;
  final Object? instruction;

  @override
  Widget build(BuildContext context) {
    final textTheme = Theme.of(context).textTheme;
    final strings = AppStrings.of(context);
    return DecoratedBox(
      decoration: BoxDecoration(
        color: KidsPalette.butter,
        borderRadius: BorderRadius.circular(8),
        boxShadow: [
          BoxShadow(
            color: KidsPalette.cocoa.withValues(alpha: 0.08),
            blurRadius: 22,
            offset: const Offset(0, 12),
          ),
        ],
      ),
      child: Padding(
        padding: const EdgeInsets.fromLTRB(20, 18, 20, 18),
        child: Row(
          children: [
            const _LeafBadge(),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(bundle.filePrefix, style: textTheme.titleLarge),
                  const SizedBox(height: 5),
                  Text(
                    instruction?.toString() ??
                        strings.t('studio.defaultInstruction'),
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                    style: textTheme.bodyMedium?.copyWith(
                      color: KidsPalette.cocoaSoft,
                      fontWeight: FontWeight.w800,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _CanvasShell extends StatelessWidget {
  const _CanvasShell({required this.child});

  final Widget child;

  @override
  Widget build(BuildContext context) {
    return DecoratedBox(
      decoration: BoxDecoration(
        color: KidsPalette.paper,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: KidsPalette.line, width: 1.4),
        boxShadow: [
          BoxShadow(
            color: KidsPalette.cocoa.withValues(alpha: 0.08),
            blurRadius: 28,
            offset: const Offset(0, 16),
          ),
        ],
      ),
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: child,
      ),
    );
  }
}

class _JsonTab extends StatelessWidget {
  const _JsonTab({
    required this.title,
    required this.data,
  });

  final String title;
  final Map<String, dynamic> data;

  @override
  Widget build(BuildContext context) {
    const encoder = JsonEncoder.withIndent('  ');
    return SelectionArea(
      child: ListView(
        padding: const EdgeInsets.fromLTRB(24, 18, 24, 24),
        children: [
          Text(title, style: Theme.of(context).textTheme.titleLarge),
          const SizedBox(height: 12),
          DecoratedBox(
            decoration: BoxDecoration(
              color: KidsPalette.paper,
              borderRadius: BorderRadius.circular(8),
              border: Border.all(color: KidsPalette.line),
            ),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Text(
                encoder.convert(data),
                style: const TextStyle(
                  color: KidsPalette.ink,
                  fontFamily: 'monospace',
                  fontSize: 13,
                  height: 1.35,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _LoadError extends StatelessWidget {
  const _LoadError({required this.error});

  final Object? error;

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: DecoratedBox(
          decoration: BoxDecoration(
            color: KidsPalette.paper,
            borderRadius: BorderRadius.circular(8),
            border: Border.all(color: KidsPalette.line),
          ),
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Text(
              strings.t('studio.loadError', {'error': error}),
              style: Theme.of(context).textTheme.bodyLarge,
            ),
          ),
        ),
      ),
    );
  }
}

class _RoundIconButton extends StatelessWidget {
  const _RoundIconButton({
    required this.tooltip,
    required this.icon,
    required this.onPressed,
  });

  final String tooltip;
  final IconData icon;
  final VoidCallback onPressed;

  @override
  Widget build(BuildContext context) {
    return Tooltip(
      message: tooltip,
      child: Material(
        color: KidsPalette.butter,
        shape: const CircleBorder(),
        child: InkWell(
          customBorder: const CircleBorder(),
          onTap: onPressed,
          child: SizedBox(
            width: 54,
            height: 54,
            child: Icon(icon, color: KidsPalette.ink),
          ),
        ),
      ),
    );
  }
}

class _LeafBadge extends StatelessWidget {
  const _LeafBadge();

  @override
  Widget build(BuildContext context) {
    return const DecoratedBox(
      decoration: BoxDecoration(
        color: KidsPalette.sage,
        shape: BoxShape.circle,
      ),
      child: SizedBox(
        width: 52,
        height: 52,
        child: Icon(Icons.auto_awesome, color: Colors.white),
      ),
    );
  }
}

class _StudioBackdrop extends StatelessWidget {
  const _StudioBackdrop();

  @override
  Widget build(BuildContext context) {
    return CustomPaint(painter: _StudioBackdropPainter());
  }
}

class _StudioBackdropPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawColor(KidsPalette.cream, BlendMode.src);

    final gridPaint = Paint()
      ..color = Colors.white.withValues(alpha: 0.34)
      ..strokeWidth = 1;
    for (double x = 28; x < size.width; x += 56) {
      canvas.drawLine(Offset(x, 0), Offset(x, size.height), gridPaint);
    }
    for (double y = 32; y < size.height; y += 56) {
      canvas.drawLine(Offset(0, y), Offset(size.width, y), gridPaint);
    }

    final formulaPaint = Paint()
      ..color = KidsPalette.cocoa.withValues(alpha: 0.045)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.2;
    for (double x = 18; x < size.width; x += 180) {
      for (double y = 90; y < size.height; y += 150) {
        canvas.drawCircle(Offset(x, y), 22, formulaPaint);
        canvas.drawLine(
            Offset(x - 16, y + 30), Offset(x + 28, y + 30), formulaPaint);
      }
    }

    final glowPaint = Paint()
      ..color = KidsPalette.butter.withValues(alpha: 0.22)
      ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 44);
    canvas.drawOval(
      Rect.fromCenter(
        center: Offset(size.width * 0.82, size.height * 0.18),
        width: size.width * 0.28,
        height: size.height * 0.20,
      ),
      glowPaint,
    );
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}

Map<String, dynamic> _mapAt(Map<String, dynamic> map, String key) {
  final value = map[key];
  if (value is Map<String, dynamic>) {
    return value;
  }
  return const {};
}
