import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../l10n/app_strings.dart';
import '../models/content_models.dart';
import '../models/tutor_models.dart';
import '../services/ai_tutor_service.dart';
import '../services/content_repository.dart';
import '../services/editor_host_bridge.dart';
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
  RendererCanvasMode canvasMode = RendererCanvasMode.edit;
  String? selectedRendererElementId;
  String? workingRendererProblemId;
  Map<String, dynamic>? workingRenderer;
  final Map<String, RendererElementPatch> pendingRendererPatches = {};
  late final EditorHostBridge editorHostBridge;

  @override
  void initState() {
    super.initState();
    _activeProblemLocale = widget.repository.activeProblemLocale;
    tutorService = _createTutorService();
    editorHostBridge = EditorHostBridge(
      onRenderer: (renderer) {
        if (!mounted) return;
        setState(() {
          workingRenderer = renderer;
          pendingRendererPatches.clear();
        });
      },
      onSelection: (elementId) {
        if (!mounted) return;
        setState(() => selectedRendererElementId = elementId);
      },
      onMode: (mode) {
        if (!mounted) return;
        setState(() => canvasMode = mode);
      },
    );
    WidgetsBinding.instance
        .addPostFrameCallback((_) => editorHostBridge.ready());
    prefixesFuture = widget.repository.loadGrade3JsonProblemPrefixes();
    bundleFuture = _loadInitialBundle();
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
  }

  Future<ProblemJsonBundle> _loadInitialBundle() async {
    final prefixes = await prefixesFuture;
    if (prefixes.isEmpty) {
      throw StateError(AppStrings.fallback.t('studio.noRenderableProblems'));
    }
    final requested = Uri.base.queryParameters['problem'];
    selectedFilePrefix = requested != null && prefixes.contains(requested)
        ? requested
        : prefixes.first;
    return widget.repository.loadProblemJsonBundle(selectedFilePrefix);
  }

  @override
  void dispose() {
    editorHostBridge.dispose();
    super.dispose();
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
                    return const OnsemLoadingIndicator(
                        labelKey: 'studio.loading');
                  }
                  if (snapshot.hasError) {
                    return _LoadError(error: snapshot.error);
                  }

                  final bundle = snapshot.data!;
                  _ensureWorkingRenderer(bundle);
                  final content = _problemContent(bundle);
                  _ensureTutorSession(content);
                  final renderTab = _RenderTab(
                    repository: widget.repository,
                    bundle: bundle,
                    renderer: workingRenderer ?? bundle.renderer,
                    content: content,
                    embedded: Uri.base.queryParameters['embedded'] == '1',
                    mode: canvasMode,
                    selectedElementId: selectedRendererElementId,
                    pendingPatches: pendingRendererPatches.values.toList(),
                    answerDraft: answerDraft,
                    onAnswerChanged: _updateAnswerDraft,
                    onModeChanged: _changeCanvasMode,
                    onElementSelected: _selectRendererElement,
                    onElementPatch: _applyRendererPatch,
                    onGeometryChanged: _changeSelectedGeometry,
                    onCopyPatches: _copyPendingPatches,
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
                      onSend: (message) => _sendTutorMessage(content, message),
                      onHint: () => _requestHint(content),
                      onNextStep: () => _requestNextStep(content),
                      onRestart: () => _restartTutor(content),
                      onReset: _resetTutor,
                      hasNextProblem: false,
                      onNextProblem: () {},
                    ),
                  );
                  if (Uri.base.queryParameters['embedded'] == '1') {
                    return renderTab;
                  }
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
                            renderTab,
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
      canvasMode = RendererCanvasMode.edit;
      selectedRendererElementId = null;
      workingRendererProblemId = null;
      workingRenderer = null;
      pendingRendererPatches.clear();
    });
  }

  void _ensureWorkingRenderer(ProblemJsonBundle bundle) {
    if (workingRendererProblemId == bundle.filePrefix &&
        workingRenderer != null) {
      return;
    }
    workingRendererProblemId = bundle.filePrefix;
    workingRenderer =
        jsonDecode(jsonEncode(bundle.renderer)) as Map<String, dynamic>;
    selectedRendererElementId = null;
    pendingRendererPatches.clear();
  }

  void _applyRendererPatch(RendererElementPatch patch) {
    final renderer = workingRenderer;
    final elements = renderer?['elements'];
    if (renderer == null || elements is! List) return;
    final nextElements = elements.map((raw) {
      if (raw is! Map || raw['id']?.toString() != patch.elementId) return raw;
      final element = Map<String, dynamic>.from(raw);
      final attributes = Map<String, dynamic>.from(
        element['attributes'] is Map ? element['attributes'] as Map : const {},
      );
      attributes.addAll(patch.value);
      if (attributes.containsKey('data-box-x')) {
        attributes['data-box-x'] = patch.value['x'];
      }
      if (attributes.containsKey('data-box-y')) {
        attributes['data-box-y'] = patch.value['y'];
      }
      if (attributes.containsKey('data-box-width')) {
        attributes['data-box-width'] = patch.value['width'];
      }
      if (attributes.containsKey('data-box-height')) {
        attributes['data-box-height'] = patch.value['height'];
      }
      if (attributes.containsKey('max_width')) {
        attributes['max_width'] = patch.value['width'];
      }
      element['attributes'] = attributes;
      return element;
    }).toList();
    final previous = pendingRendererPatches[patch.targetId];
    setState(() {
      workingRenderer = {...renderer, 'elements': nextElements};
      selectedRendererElementId = patch.elementId;
      pendingRendererPatches[patch.targetId] = RendererElementPatch(
        elementId: patch.elementId,
        targetId: patch.targetId,
        value: {...?previous?.value, ...patch.value},
      );
    });
    editorHostBridge.patch(patch);
  }

  void _changeCanvasMode(RendererCanvasMode mode) {
    setState(() => canvasMode = mode);
    editorHostBridge.mode(mode);
  }

  void _selectRendererElement(String? elementId) {
    setState(() => selectedRendererElementId = elementId);
    final element = _selectedElement(
      workingRenderer ?? const {},
      elementId,
    );
    editorHostBridge.selected(
      elementId,
      element == null ? null : _previewElementTargetId(element),
    );
  }

  void _changeSelectedGeometry(String field, double value) {
    final renderer = workingRenderer;
    final elements = renderer?['elements'];
    if (renderer == null ||
        elements is! List ||
        selectedRendererElementId == null) {
      return;
    }
    final raw = elements.whereType<Map>().cast<Map>().firstWhere(
          (element) => element['id']?.toString() == selectedRendererElementId,
          orElse: () => const {},
        );
    if (raw.isEmpty) return;
    final attributes = raw['attributes'] is Map
        ? Map<String, dynamic>.from(raw['attributes'] as Map)
        : <String, dynamic>{};
    double number(String key) => (attributes[key] as num?)?.toDouble() ?? 0;
    final patch = RendererElementPatch(
      elementId: selectedRendererElementId!,
      targetId: _previewElementTargetId(raw),
      value: {
        'x': field == 'x' ? value : number('x'),
        'y': field == 'y' ? value : number('y'),
        'width': field == 'width'
            ? value.clamp(12, double.infinity)
            : number('width'),
        'height': field == 'height'
            ? value.clamp(12, double.infinity)
            : number('height'),
      },
    );
    _applyRendererPatch(patch);
  }

  Future<void> _copyPendingPatches() async {
    final payload = pendingRendererPatches.values
        .map((patch) => patch.toLayoutPatch())
        .toList();
    await Clipboard.setData(
      ClipboardData(text: const JsonEncoder.withIndent('  ').convert(payload)),
    );
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('${payload.length}개 공통 레이아웃 패치를 복사했습니다.')),
    );
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
        path: bundle.basePath.contains('/')
            ? bundle.basePath.substring(0, bundle.basePath.lastIndexOf('/'))
            : '',
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
    required this.repository,
    required this.bundle,
    required this.renderer,
    required this.content,
    required this.embedded,
    required this.mode,
    required this.selectedElementId,
    required this.pendingPatches,
    required this.answerDraft,
    required this.onAnswerChanged,
    required this.onModeChanged,
    required this.onElementSelected,
    required this.onElementPatch,
    required this.onGeometryChanged,
    required this.onCopyPatches,
    required this.tutorPanel,
  });

  final ContentRepository repository;
  final ProblemJsonBundle bundle;
  final Map<String, dynamic> renderer;
  final ProblemContent content;
  final bool embedded;
  final RendererCanvasMode mode;
  final String? selectedElementId;
  final List<RendererElementPatch> pendingPatches;
  final String answerDraft;
  final ValueChanged<String> onAnswerChanged;
  final ValueChanged<RendererCanvasMode> onModeChanged;
  final ValueChanged<String?> onElementSelected;
  final ValueChanged<RendererElementPatch> onElementPatch;
  final void Function(String field, double value) onGeometryChanged;
  final VoidCallback onCopyPatches;
  final Widget tutorPanel;

  @override
  Widget build(BuildContext context) {
    return _RenderTabBody(
      repository: repository,
      bundle: bundle,
      renderer: renderer,
      content: content,
      embedded: embedded,
      mode: mode,
      selectedElementId: selectedElementId,
      pendingPatches: pendingPatches,
      answerDraft: answerDraft,
      onAnswerChanged: onAnswerChanged,
      onModeChanged: onModeChanged,
      onElementSelected: onElementSelected,
      onElementPatch: onElementPatch,
      onGeometryChanged: onGeometryChanged,
      onCopyPatches: onCopyPatches,
      tutorPanel: tutorPanel,
    );
  }
}

class _RenderTabBody extends StatelessWidget {
  const _RenderTabBody({
    required this.repository,
    required this.bundle,
    required this.renderer,
    required this.content,
    required this.embedded,
    required this.mode,
    required this.selectedElementId,
    required this.pendingPatches,
    required this.answerDraft,
    required this.onAnswerChanged,
    required this.onModeChanged,
    required this.onElementSelected,
    required this.onElementPatch,
    required this.onGeometryChanged,
    required this.onCopyPatches,
    required this.tutorPanel,
  });

  final ContentRepository repository;
  final ProblemJsonBundle bundle;
  final Map<String, dynamic> renderer;
  final ProblemContent content;
  final bool embedded;
  final RendererCanvasMode mode;
  final String? selectedElementId;
  final List<RendererElementPatch> pendingPatches;
  final String answerDraft;
  final ValueChanged<String> onAnswerChanged;
  final ValueChanged<RendererCanvasMode> onModeChanged;
  final ValueChanged<String?> onElementSelected;
  final ValueChanged<RendererElementPatch> onElementPatch;
  final void Function(String field, double value) onGeometryChanged;
  final VoidCallback onCopyPatches;
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
              _CanvasModeToolbar(mode: mode, onChanged: onModeChanged),
              const SizedBox(height: 10),
              Expanded(
                child: _CanvasShell(
                  child: RendererJsonCanvas(
                    renderer: renderer,
                    mode: mode,
                    selectedElementId: selectedElementId,
                    onElementSelected: onElementSelected,
                    onElementPatch: onElementPatch,
                    inputValue: answerDraft,
                    onInputChanged: onAnswerChanged,
                    imageLoader: (href) =>
                        repository.loadProblemAsset(content.summary, href),
                    imageCacheKey: content.summary.path,
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
            children: [
              if (mode == RendererCanvasMode.edit)
                _FlutterEditorPanel(
                  renderer: renderer,
                  selectedElementId: selectedElementId,
                  pendingPatches: pendingPatches,
                  onGeometryChanged: onGeometryChanged,
                  onCopyPatches: onCopyPatches,
                )
              else
                tutorPanel,
            ],
          ),
        );

        if (embedded) return preview;

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

class _CanvasModeToolbar extends StatelessWidget {
  const _CanvasModeToolbar({required this.mode, required this.onChanged});

  final RendererCanvasMode mode;
  final ValueChanged<RendererCanvasMode> onChanged;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        SegmentedButton<RendererCanvasMode>(
          segments: const [
            ButtonSegment(
              value: RendererCanvasMode.edit,
              icon: Icon(Icons.edit_outlined),
              label: Text('편집 모드'),
            ),
            ButtonSegment(
              value: RendererCanvasMode.studentTest,
              icon: Icon(Icons.school_outlined),
              label: Text('학생 테스트'),
            ),
          ],
          selected: {mode},
          onSelectionChanged: (selection) => onChanged(selection.first),
        ),
        const SizedBox(width: 12),
        Expanded(
          child: Text(
            mode == RendererCanvasMode.edit
                ? '요소를 선택해 이동하거나 오른쪽 아래 손잡이로 크기를 조절하세요.'
                : '실제 학생 화면처럼 답을 입력하고 동작을 확인하세요.',
            overflow: TextOverflow.ellipsis,
          ),
        ),
      ],
    );
  }
}

class _FlutterEditorPanel extends StatelessWidget {
  const _FlutterEditorPanel({
    required this.renderer,
    required this.selectedElementId,
    required this.pendingPatches,
    required this.onGeometryChanged,
    required this.onCopyPatches,
  });

  final Map<String, dynamic> renderer;
  final String? selectedElementId;
  final List<RendererElementPatch> pendingPatches;
  final void Function(String field, double value) onGeometryChanged;
  final VoidCallback onCopyPatches;

  @override
  Widget build(BuildContext context) {
    final element = _selectedElement(renderer, selectedElementId);
    final attributes = element == null
        ? const <String, dynamic>{}
        : _mapAt(element, 'attributes');
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text('Flutter 직접 편집',
                style: Theme.of(context).textTheme.titleLarge),
            const SizedBox(height: 8),
            Text(
              element == null
                  ? '캔버스에서 텍스트, 사각형 또는 정답 칸을 선택하세요.'
                  : _previewElementTargetId(element),
            ),
            if (element != null) ...[
              const SizedBox(height: 16),
              Wrap(
                spacing: 10,
                runSpacing: 10,
                children: ['x', 'y', 'width', 'height'].map((field) {
                  final value = (attributes[field] as num?)?.toDouble() ?? 0;
                  return SizedBox(
                    width: 110,
                    child: TextFormField(
                      key: ValueKey('$selectedElementId-$field-$value'),
                      initialValue: _compactNumber(value),
                      keyboardType: const TextInputType.numberWithOptions(
                        decimal: true,
                        signed: true,
                      ),
                      decoration: InputDecoration(labelText: field),
                      onFieldSubmitted: (raw) {
                        final next = double.tryParse(raw);
                        if (next != null) onGeometryChanged(field, next);
                      },
                    ),
                  );
                }).toList(),
              ),
            ],
            const SizedBox(height: 18),
            Text('저장 대기 변경: ${pendingPatches.length}개'),
            const SizedBox(height: 8),
            FilledButton.icon(
              onPressed: pendingPatches.isEmpty ? null : onCopyPatches,
              icon: const Icon(Icons.copy_all_outlined),
              label: const Text('공통 Layout 패치 복사'),
            ),
            const SizedBox(height: 8),
            const Text(
              '변경은 Flutter 전용 값이 아니라 target + x/y/width/height 형식으로 생성되어 다른 렌더러에서도 사용할 수 있습니다.',
            ),
          ],
        ),
      ),
    );
  }
}

Map<String, dynamic>? _selectedElement(
  Map<String, dynamic> renderer,
  String? selectedElementId,
) {
  if (selectedElementId == null) return null;
  final elements = renderer['elements'];
  if (elements is! List) return null;
  for (final raw in elements) {
    if (raw is Map && raw['id']?.toString() == selectedElementId) {
      return Map<String, dynamic>.from(raw);
    }
  }
  return null;
}

String _previewElementTargetId(Map<dynamic, dynamic> element) {
  final refs = element['refs'];
  if (refs is Map) {
    final slotId = refs['layout_slot_id']?.toString().trim() ?? '';
    if (slotId.isNotEmpty) return slotId;
  }
  final sourceRef = element['source_ref']?.toString().trim() ?? '';
  if (sourceRef.isNotEmpty) return sourceRef;
  return element['id']?.toString().replaceFirst(
            RegExp(r'\.(text|rect|image)$'),
            '',
          ) ??
      '';
}

String _compactNumber(double value) {
  if (value == value.roundToDouble()) return value.toInt().toString();
  return value.toStringAsFixed(3).replaceFirst(RegExp(r'0+$'), '');
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
