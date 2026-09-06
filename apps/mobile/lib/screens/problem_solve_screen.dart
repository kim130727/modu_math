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
import '../widgets/vertical_arithmetic_explorer.dart';
import '../theme/app_theme.dart';

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
    _activeProblemLocale = widget.repository.activeProblemLocale;
    contentFuture = _loadContent();
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
  }

  Future<ProblemContent> _loadContent() {
    final future = widget.repository.loadProblem(widget.problem);
    _preloadUpcomingProblems();
    return future;
  }

  void _preloadUpcomingProblems() {
    if (!_hasNextProblem) {
      return;
    }
    final end = (widget.problemIndex + 6).clamp(0, widget.unitProblems.length);
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
    final strings = AppStrings.of(context);
    final rawSubUnit = widget.problem.subUnit;
    final subTopic = rawSubUnit.isNotEmpty &&
            rawSubUnit != '__basicLearning__' &&
            rawSubUnit != '기본 학습' &&
            rawSubUnit != 'Basic Learning'
        ? strings.subUnitName(rawSubUnit)
        : strings.t('problem.defaultSubTopic');

    final screenWidth = MediaQuery.sizeOf(context).width;
    final isWide = screenWidth >= 960;

    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        automaticallyImplyLeading: false,
        backgroundColor: Colors.white,
        elevation: 0,
        titleSpacing: 12,
        leadingWidth: isWide ? 176 : 56,
        leading: Padding(
          padding: EdgeInsetsDirectional.only(
            start: 16,
            top: 8,
            bottom: 8,
            end: isWide ? 0 : 8,
          ),
          child: isWide
              ? OutlinedButton.icon(
                  onPressed: () => Navigator.of(context).pop(),
                  icon: const Icon(Icons.arrow_back_rounded, size: 16),
                  label: Text(strings.t('common.backToBriefingRoom')),
                  style: OutlinedButton.styleFrom(
                    foregroundColor: const Color(0xFF0F172A),
                    side: const BorderSide(color: Color(0xFFE2E8F0)),
                    backgroundColor: Colors.white,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(999),
                    ),
                    padding:
                        const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                  ),
                )
              : IconButton(
                  onPressed: () => Navigator.of(context).pop(),
                  icon: const Icon(Icons.arrow_back_rounded, size: 20),
                  tooltip: strings.t('common.backToBriefingRoom'),
                ),
        ),
        title: Row(
          children: [
            if (isWide) ...[
              Container(
                padding:
                    const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(
                  color: const Color(0xFFEEF2FF),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(
                  strings.t('common.mathGrade', {
                    'grade':
                        widget.problem.grade > 0 ? widget.problem.grade : 3,
                  }),
                  style: const TextStyle(
                    color: Color(0xFF4F46E5),
                    fontSize: 12,
                    fontWeight: FontWeight.w800,
                  ),
                ),
              ),
              const SizedBox(width: 10),
            ],
            Expanded(
              child: Text(
                '${strings.t('common.unitNumberWithTopic', {
                      'unit': widget.problem.unitNumber,
                      'topic': strings.unitTitle(widget.problem.unitTopic),
                    })} · $subTopic',
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
                style: const TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.w800,
                  color: Color(0xFF0F172A),
                ),
              ),
            ),
            const SizedBox(width: 10),
            Text(
              widget.problem.id,
              style: const TextStyle(
                fontSize: 12,
                color: Color(0xFF94A3B8),
                fontWeight: FontWeight.w600,
              ),
            ),
          ],
        ),
        actions: [
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
            decoration: BoxDecoration(
              color: const Color(0xFFEEF2FF),
              borderRadius: BorderRadius.circular(999),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Container(
                  width: 6,
                  height: 6,
                  decoration: const BoxDecoration(
                    color: Color(0xFF4F46E5),
                    shape: BoxShape.circle,
                  ),
                ),
                const SizedBox(width: 6),
                Text(
                  strings.t('common.problemProgress', {
                    'current': widget.problemIndex + 1,
                    'total': widget.unitProblems.isNotEmpty
                        ? widget.unitProblems.length
                        : 1,
                  }),
                  style: const TextStyle(
                    color: Color(0xFF4F46E5),
                    fontSize: 12,
                    fontWeight: FontWeight.w800,
                  ),
                ),
              ],
            ),
          ),
          if (isWide) ...[
            const SizedBox(width: 8),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
              decoration: BoxDecoration(
                color: const Color(0xFFFFF7ED),
                borderRadius: BorderRadius.circular(999),
                border: Border.all(color: const Color(0xFFFFEDD5)),
              ),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Text('🔥', style: TextStyle(fontSize: 13)),
                  const SizedBox(width: 4),
                  Text(
                    strings.t('common.streakDays', {'days': 5}),
                    style: const TextStyle(
                      color: Color(0xFFC2410C),
                      fontSize: 12,
                      fontWeight: FontWeight.w800,
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(width: 8),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
              decoration: BoxDecoration(
                color: const Color(0xFFFEFCE8),
                borderRadius: BorderRadius.circular(999),
                border: Border.all(color: const Color(0xFFFEF08A)),
              ),
              child: const Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text('★',
                      style: TextStyle(color: Color(0xFFF59E0B), fontSize: 13)),
                  SizedBox(width: 4),
                  Text(
                    '420 P',
                    style: TextStyle(
                      color: Color(0xFF854D0E),
                      fontSize: 12,
                      fontWeight: FontWeight.w800,
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(width: 8),
            const Padding(
              padding: EdgeInsets.symmetric(horizontal: 6),
              child: Center(
                child: Text(
                  '❤️❤️❤️',
                  style: TextStyle(fontSize: 14),
                ),
              ),
            ),
            const SizedBox(width: 64),
          ] else
            const SizedBox(width: 16),
        ],
      ),
      body: FutureBuilder<ProblemContent>(
        future: contentFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState != ConnectionState.done) {
            return const OnsemLoadingIndicator(labelKey: 'problem.loading');
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
              final problemViewer = VerticalArithmeticExplorer(
                repository: widget.repository,
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
              final activeLocale =
                  AppLocaleScope.maybeOf(context)?.locale.languageCode ??
                      widget.repository.activeProblemLocale;
              final hintPanel = HintPanel(
                hints: hintService.buildHints(
                  content,
                  locale: activeLocale,
                  strings: strings,
                ),
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
                      constraints: const BoxConstraints(
                        maxWidth: 1600.0,
                      ),
                      child: Padding(
                        padding: const EdgeInsets.fromLTRB(20, 10, 20, 16),
                        child: Column(
                          children: [
                            _MissionHeroBanner(content: content),
                            const SizedBox(height: 12),
                            Expanded(
                              child: Row(
                                crossAxisAlignment: CrossAxisAlignment.stretch,
                                children: [
                                  Expanded(flex: 6, child: problemViewer),
                                  const SizedBox(width: 18),
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
                          ],
                        ),
                      ),
                    ),
                  ),
                );
              }

              return SafeArea(
                child: ListView(
                  padding: const EdgeInsets.fromLTRB(16, 10, 16, 20),
                  children: [
                    _MissionHeroBanner(content: content),
                    const SizedBox(height: 12),
                    SizedBox(height: 580, child: problemViewer),
                    const SizedBox(height: 14),
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

// Kept for compatibility with deep links that may restore a legacy title.
// ignore: unused_element
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
  return value.contains('\uFFFD') ||
      value.contains('??') ||
      value.contains('占');
}

bool _hasCanvasQuestion(ProblemContent content) {
  final elements = content.renderer['elements'];
  if (elements is List && elements.isNotEmpty) {
    for (final el in elements) {
      if (el is! Map) continue;
      final id = (el['id'] ?? '').toString().toLowerCase();
      final type = (el['type'] ?? '').toString().toLowerCase();
      final text = (el['text'] ?? '').toString().trim();
      final sourceRef = (el['source_ref'] ?? '').toString().toLowerCase();

      if (id.contains('question') ||
          id.contains('q_text') ||
          id.contains('stem') ||
          id.contains('header.text') ||
          id.startsWith('slot.q') ||
          sourceRef.contains('question') ||
          sourceRef.contains('q1') ||
          sourceRef.contains('stem')) {
        if (text.isNotEmpty) return true;
      }
      if (type == 'text' && text.isNotEmpty && content.prompt.isNotEmpty) {
        final normPrompt = content.prompt.replaceAll(RegExp(r'\s+'), '');
        final normText = text.replaceAll(RegExp(r'\s+'), '');
        if (normPrompt.contains(normText) && normText.length >= 6) {
          return true;
        }
      }
    }
  }
  return false;
}

class _MissionHeroBanner extends StatelessWidget {
  const _MissionHeroBanner({required this.content});

  final ProblemContent content;

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    final prompt = content.prompt.trim();

    String? targetHighlight;
    final objects = content.semantic['domain']?['objects'];
    if (objects is List) {
      for (final obj in objects) {
        if (obj is Map && (obj['id'] == 'obj.highlighted_value' || obj['type'] == 'value')) {
          targetHighlight = obj['text']?.toString();
          break;
        }
      }
    }
    if (targetHighlight == null && (content.summary.id.contains('008540') || prompt.contains('240'))) {
      targetHighlight = '240';
    }

    final tutorQuote = strings.t('problem.tutorDefaultQuote');
    final hasCanvasQuestion = _hasCanvasQuestion(content);

    return Container(
      width: double.infinity,
      padding: EdgeInsets.symmetric(
        horizontal: 16,
        vertical: hasCanvasQuestion ? 8 : 10,
      ),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [
            Color(0xFF4338CA),
            Color(0xFF4F46E5),
            Color(0xFF6366F1),
          ],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: const Color(0xFF4F46E5).withValues(alpha: 0.20),
            blurRadius: 12,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: LayoutBuilder(
        builder: (context, constraints) {
          final isNarrow = constraints.maxWidth < 740;
          final leftContent = Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              Wrap(
                spacing: 8,
                runSpacing: 6,
                crossAxisAlignment: WrapCrossAlignment.center,
                children: [
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 9, vertical: 3),
                    decoration: BoxDecoration(
                      color: Colors.white.withValues(alpha: 0.18),
                      borderRadius: BorderRadius.circular(999),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Container(
                          width: 7,
                          height: 7,
                          decoration: const BoxDecoration(
                            color: Color(0xFF34D399),
                            shape: BoxShape.circle,
                          ),
                        ),
                        const SizedBox(width: 6),
                        Text(
                          strings.t('problem.missionCode', {'code': content.summary.id}),
                          style: const TextStyle(
                            color: Colors.white,
                            fontSize: 11,
                            fontWeight: FontWeight.w700,
                          ),
                        ),
                      ],
                    ),
                  ),
                  if (hasCanvasQuestion && content.summary.unitTopic.isNotEmpty)
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 9, vertical: 3),
                      decoration: BoxDecoration(
                        color: Colors.white.withValues(alpha: 0.14),
                        borderRadius: BorderRadius.circular(999),
                        border: Border.all(color: Colors.white.withValues(alpha: 0.2)),
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          const Icon(Icons.menu_book_rounded, size: 12, color: Colors.white70),
                          const SizedBox(width: 5),
                          Text(
                            strings.unitTitle(content.summary.unitTopic),
                            style: const TextStyle(
                              color: Colors.white,
                              fontSize: 11,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                        ],
                      ),
                    ),
                ],
              ),
              if (!hasCanvasQuestion) ...[
                const SizedBox(height: 8),
                _buildHighlightedPrompt(prompt, targetHighlight),
              ],
            ],
          );

          final rightContent = Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
            decoration: BoxDecoration(
              color: Colors.white.withValues(alpha: 0.16),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: Colors.white.withValues(alpha: 0.25)),
            ),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Container(
                  width: 32,
                  height: 32,
                  decoration: BoxDecoration(
                    color: Colors.white.withValues(alpha: 0.2),
                    shape: BoxShape.circle,
                  ),
                  child: ClipOval(
                    child: Image.asset(
                      'assets/characters/onsem_tutor.png',
                      fit: BoxFit.cover,
                      errorBuilder: (context, error, stackTrace) =>
                          const Center(child: Text('🧚', style: TextStyle(fontSize: 18))),
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(
                        strings.t('problem.fairyWhisper'),
                        style: const TextStyle(
                          color: Color(0xFFFDE047),
                          fontWeight: FontWeight.w800,
                          fontSize: 11,
                        ),
                      ),
                      const SizedBox(height: 1),
                      Text(
                        tutorQuote,
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 11,
                          height: 1.25,
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          );

          if (isNarrow) {
            return Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                leftContent,
                const SizedBox(height: 8),
                rightContent,
              ],
            );
          }

          return Row(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Expanded(flex: hasCanvasQuestion ? 5 : 6, child: leftContent),
              const SizedBox(width: 14),
              Expanded(flex: hasCanvasQuestion ? 5 : 4, child: rightContent),
            ],
          );
        },
      ),
    );
  }

  Widget _buildHighlightedPrompt(String prompt, String? highlight) {
    if (highlight == null || !prompt.contains(highlight)) {
      return Text(
        prompt,
        style: const TextStyle(
          fontSize: 18,
          fontWeight: FontWeight.w800,
          color: Colors.white,
          height: 1.3,
        ),
      );
    }

    final parts = prompt.split(highlight);
    return RichText(
      text: TextSpan(
        style: const TextStyle(
          fontSize: 18,
          fontWeight: FontWeight.w800,
          color: Colors.white,
          height: 1.3,
          fontFamily: 'Pretendard',
        ),
        children: [
          TextSpan(text: parts[0]),
          WidgetSpan(
            alignment: PlaceholderAlignment.middle,
            child: Container(
              margin: const EdgeInsets.symmetric(horizontal: 5),
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
              decoration: BoxDecoration(
                color: const Color(0xFFFF4B6E),
                borderRadius: BorderRadius.circular(6),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withValues(alpha: 0.15),
                    blurRadius: 4,
                    offset: const Offset(0, 2),
                  ),
                ],
              ),
              child: Text(
                highlight,
                style: const TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.w900,
                  fontSize: 17,
                ),
              ),
            ),
          ),
          if (parts.length > 1) TextSpan(text: parts.sublist(1).join(highlight)),
        ],
      ),
    );
  }
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

    final previousButton = OutlinedButton.icon(
      onPressed: canOpenPreviousProblem ? onPreviousProblem : null,
      icon: const Icon(Icons.navigate_before, size: 20),
      label: Text(strings.t('common.previousProblem')),
      style: OutlinedButton.styleFrom(
        foregroundColor: const Color(0xFF475569),
        side: const BorderSide(color: Color(0xFFE2E8F0)),
        backgroundColor: Colors.white,
        disabledForegroundColor: const Color(0xFFCBD5E1),
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 14),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
        ),
      ),
    );

    final retryButton = OutlinedButton.icon(
      onPressed: onRetry,
      icon: const Icon(Icons.refresh, size: 18),
      label: Text(strings.t('common.retry')),
      style: OutlinedButton.styleFrom(
        foregroundColor: const Color(0xFF475569),
        side: const BorderSide(color: Color(0xFFE2E8F0)),
        backgroundColor: Colors.white,
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 14),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
        ),
      ),
    );

    final nextButton = FilledButton.icon(
      onPressed: canOpenNextProblem ? onNextProblem : null,
      icon: const Icon(Icons.navigate_next, size: 20),
      iconAlignment: IconAlignment.end,
      label: Text(strings.t('common.nextProblem')),
      style: FilledButton.styleFrom(
        backgroundColor: const Color(0xFF059669),
        foregroundColor: Colors.white,
        disabledBackgroundColor: const Color(0xFFE2E8F0),
        disabledForegroundColor: const Color(0xFF94A3B8),
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 14),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
        ),
        elevation: 1,
      ),
    );

    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: const Color(0xFFE2E8F0)),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.03),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      padding: const EdgeInsets.all(12),
      child: Row(
        children: [
          if (canOpenPreviousProblem) ...[
            Expanded(child: previousButton),
            const SizedBox(width: 8),
          ],
          Expanded(child: retryButton),
          const SizedBox(width: 8),
          Expanded(child: nextButton),
        ],
      ),
    );
  }
}

class _ProblemVisual extends StatelessWidget {
  const _ProblemVisual({
    required this.repository,
    required this.content,
    required this.answerDraft,
    required this.onAnswerChanged,
  });

  final ContentRepository repository;
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
            imageLoader: (href) =>
                repository.loadProblemAsset(content.summary, href),
            imageCacheKey: content.summary.path,
            inputValue: answerDraft,
            expectedAnswer: content.correctAnswer,
            suppressInputs: content.choices.isNotEmpty,
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
