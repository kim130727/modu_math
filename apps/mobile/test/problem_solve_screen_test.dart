import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/models/content_models.dart';
import 'package:modu_math_app/models/learning_progress.dart';
import 'package:modu_math_app/models/student_profile.dart';
import 'package:modu_math_app/screens/problem_solve_screen.dart';
import 'package:modu_math_app/services/content_repository.dart';
import 'package:modu_math_app/services/learning_progress_repository.dart';
import 'package:modu_math_app/widgets/tutor_chat_panel.dart';

void main() {
  setUp(() {
    TestWidgetsFlutterBinding.ensureInitialized();
  });

  testWidgets('hides tutor UI and starts one learning session across rebuilds',
      (tester) async {
    await tester.binding.setSurfaceSize(const Size(1200, 900));
    addTearDown(() => tester.binding.setSurfaceSize(null));
    final progressRepository = _FakeProgressRepository();

    await tester.pumpWidget(
      MaterialApp(
        home: ProblemSolveScreen(
          repository: _FakeContentRepository(),
          progressRepository: progressRepository,
          problem: _summary,
        ),
      ),
    );
    await tester.pumpAndSettle();

    expect(find.byType(TutorChatPanel), findsNothing);
    expect(find.text('힌트 보기'), findsOneWidget);
    expect(find.text('풀이 보기'), findsNothing);
    expect(progressRepository.startedSessions, equals(1));
    expect(progressRepository.sessions.single.skillIds, equals(['skill.add']));

    await tester.pumpWidget(
      MaterialApp(
        home: ProblemSolveScreen(
          repository: _FakeContentRepository(),
          progressRepository: progressRepository,
          problem: _summary,
        ),
      ),
    );
    await tester.pumpAndSettle();

    expect(progressRepository.startedSessions, equals(1));
  });

  testWidgets('records hint usage and keeps attempt review behavior',
      (tester) async {
    await tester.binding.setSurfaceSize(const Size(1200, 900));
    addTearDown(() => tester.binding.setSurfaceSize(null));
    final progressRepository = _FakeProgressRepository();

    await tester.pumpWidget(
      MaterialApp(
        home: ProblemSolveScreen(
          repository: _FakeContentRepository(),
          progressRepository: progressRepository,
          problem: _summary,
        ),
      ),
    );
    await tester.pumpAndSettle();

    await tester.tap(find.text('힌트 보기'));
    await tester.pumpAndSettle();
    await tester.tap(find.text('5'));
    await tester.tap(find.byType(FilledButton).first);
    await tester.pumpAndSettle();

    expect(progressRepository.hints.single.level, equals(1));
    expect(progressRepository.submissions.single.answer, equals('5'));
    expect(progressRepository.submissions.single.isCorrect, isFalse);
    expect(progressRepository.attempts.single.isCorrect, isFalse);
    expect(await progressRepository.getReviewQueue(), hasLength(1));
    expect(find.textContaining('정답: 7'), findsNothing);
    expect(find.textContaining('힌트를 보고 한 번 더 생각'), findsOneWidget);
  });

  testWidgets('shows authored diagnostic feedback from condition rules',
      (tester) async {
    await tester.binding.setSurfaceSize(const Size(1200, 900));
    addTearDown(() => tester.binding.setSurfaceSize(null));

    await tester.pumpWidget(
      MaterialApp(
        home: ProblemSolveScreen(
          repository: _FakeContentRepository(content: _diagnosticContent),
          progressRepository: _FakeProgressRepository(),
          problem: _summary,
        ),
      ),
    );
    await tester.pumpAndSettle();

    await tester.enterText(find.byType(TextField), '259');
    await tester.tap(find.byType(FilledButton).first);
    await tester.pumpAndSettle();

    expect(find.textContaining('한 가족이 캔 수만 쓰면 안 돼요'), findsOneWidget);
    expect(find.textContaining('정답:'), findsNothing);
  });

  testWidgets('shows range diagnostic feedback for unlisted wrong numbers',
      (tester) async {
    await tester.binding.setSurfaceSize(const Size(1200, 900));
    addTearDown(() => tester.binding.setSurfaceSize(null));

    await tester.pumpWidget(
      MaterialApp(
        home: ProblemSolveScreen(
          repository: _FakeContentRepository(content: _diagnosticContent),
          progressRepository: _FakeProgressRepository(),
          problem: _summary,
        ),
      ),
    );
    await tester.pumpAndSettle();

    await tester.enterText(find.byType(TextField), '300');
    await tester.tap(find.byType(FilledButton).first);
    await tester.pumpAndSettle();

    expect(find.textContaining('자리'), findsOneWidget);
    expect(find.textContaining('정답:'), findsNothing);
  });

  testWidgets('shows place-specific feedback for carry mistakes',
      (tester) async {
    await tester.binding.setSurfaceSize(const Size(1200, 900));
    addTearDown(() => tester.binding.setSurfaceSize(null));

    await tester.pumpWidget(
      MaterialApp(
        home: ProblemSolveScreen(
          repository: _FakeContentRepository(content: _diagnosticContent),
          progressRepository: _FakeProgressRepository(),
          problem: _summary,
        ),
      ),
    );
    await tester.pumpAndSettle();

    await tester.enterText(find.byType(TextField), '607');
    await tester.tap(find.byType(FilledButton).first);
    await tester.pumpAndSettle();

    expect(find.textContaining('백의 자리'), findsOneWidget);
    expect(find.textContaining('두 번 더하면'), findsOneWidget);
    expect(find.textContaining('정답:'), findsNothing);
  });

  testWidgets('syncs renderer answer slot input into the answer panel',
      (tester) async {
    await tester.binding.setSurfaceSize(const Size(1200, 900));
    addTearDown(() => tester.binding.setSurfaceSize(null));

    await tester.pumpWidget(
      MaterialApp(
        home: ProblemSolveScreen(
          repository: _FakeContentRepository(content: _rendererContent),
          progressRepository: _FakeProgressRepository(),
          problem: _summary,
        ),
      ),
    );
    await tester.pumpAndSettle();

    final textFields = find.byType(TextField);
    expect(textFields, findsNWidgets(2));

    await tester.enterText(textFields.first, '507');
    await tester.pumpAndSettle();

    final answerField = tester.widget<TextField>(textFields.last);
    expect(answerField.controller?.text, equals('507'));
  });

  testWidgets('opens next problem even when preload fails', (tester) async {
    await tester.binding.setSurfaceSize(const Size(1200, 900));
    addTearDown(() => tester.binding.setSurfaceSize(null));
    const nextSummary = ProblemSummary(
      id: 'P-next',
      grade: 3,
      subject: 'math',
      unit: 'addition',
      type: 'calc',
      title: 'Next problem',
      path: '',
      raw: {},
    );
    final repository = _FakeContentRepository(
      preloadFailureIds: {nextSummary.id},
    );

    await tester.pumpWidget(
      MaterialApp(
        home: ProblemSolveScreen(
          repository: repository,
          progressRepository: _FakeProgressRepository(),
          problem: _summary,
          unitProblems: [_summary, nextSummary],
          problemIndex: 0,
        ),
      ),
    );
    await tester.pumpAndSettle();

    await tester.tap(find.byIcon(Icons.navigate_next));
    await tester.pumpAndSettle();

    expect(repository.preloadedProblemIds, contains(nextSummary.id));
    expect(find.textContaining(nextSummary.id), findsOneWidget);
  });

  testWidgets('opens previous problem from problem controls', (tester) async {
    await tester.binding.setSurfaceSize(const Size(1200, 900));
    addTearDown(() => tester.binding.setSurfaceSize(null));
    const previousSummary = ProblemSummary(
      id: 'P-previous',
      grade: 3,
      subject: 'math',
      unit: 'addition',
      type: 'calc',
      title: 'Previous problem',
      path: '',
      raw: {},
    );
    final repository = _FakeContentRepository();

    await tester.pumpWidget(
      MaterialApp(
        home: ProblemSolveScreen(
          repository: repository,
          progressRepository: _FakeProgressRepository(),
          problem: _summary,
          unitProblems: [previousSummary, _summary],
          problemIndex: 1,
        ),
      ),
    );
    await tester.pumpAndSettle();

    await tester.tap(find.byIcon(Icons.navigate_before));
    await tester.pumpAndSettle();

    expect(repository.preloadedProblemIds, contains(previousSummary.id));
    expect(find.textContaining(previousSummary.id), findsOneWidget);
  });
}

class _FakeContentRepository extends ContentRepository {
  _FakeContentRepository({
    this.content = _content,
    this.preloadFailureIds = const {},
  });

  final ProblemContent content;
  final Set<String> preloadFailureIds;
  final List<String> preloadedProblemIds = [];

  @override
  Future<ProblemContent> loadProblem(ProblemSummary summary) async {
    if (content.summary.id == summary.id) {
      return content;
    }
    return ProblemContent(
      summary: summary,
      svg: content.svg,
      semantic: content.semantic,
      solvable: content.solvable,
      layout: content.layout,
      renderer: content.renderer,
    );
  }

  @override
  Future<void> preloadProblem(ProblemSummary summary) async {
    preloadedProblemIds.add(summary.id);
    if (preloadFailureIds.contains(summary.id)) {
      throw StateError('preload failed for ${summary.id}');
    }
  }
}

class _FakeProgressRepository implements LearningProgressRepository {
  int startedSessions = 0;
  final List<LearningSession> sessions = [];
  final List<LearningHintUsage> hints = [];
  final List<LearningSubmission> submissions = [];
  final List<StudentAttempt> attempts = [];

  @override
  Future<void> clearAll() async {
    sessions.clear();
    hints.clear();
    submissions.clear();
    attempts.clear();
  }

  @override
  Future<List<StudentAttempt>> getAttempts() async => attempts;

  @override
  Future<List<LearningSession>> getLearningSessions() async => sessions;

  @override
  Future<DailySummary> getDailySummary(DateTime date) async {
    return DailySummary(
      date: date,
      totalAttempted: attempts.length,
      totalCorrect: attempts.where((attempt) => attempt.isCorrect).length,
      streakDays: 0,
    );
  }

  @override
  Future<StudentProfile> getProfile() async {
    return StudentProfile.defaultProfile();
  }

  @override
  Future<List<StudentAttempt>> getReviewQueue() async {
    return attempts.where((attempt) => !attempt.isCorrect).toList();
  }

  @override
  Future<List<SkillMastery>> getSkillMasteries() async => const [];

  @override
  Future<void> recordAttempt({
    required ProblemSummary problem,
    required String answer,
    required bool isCorrect,
    int hintLevelUsed = 0,
    int timeSpentSeconds = 0,
    ErrorCategory errorCategory = ErrorCategory.none,
  }) async {
    attempts.add(
      StudentAttempt(
        id: 'attempt_${attempts.length}',
        problemId: problem.id,
        unit: problem.unit,
        answer: answer,
        isCorrect: isCorrect,
        timestamp: DateTime.now(),
        hintLevelUsed: hintLevelUsed,
        timeSpentSeconds: timeSpentSeconds,
        errorCategory: errorCategory,
      ),
    );
  }

  @override
  Future<void> recordSessionHint({
    required String sessionId,
    required int level,
  }) async {
    hints.add(LearningHintUsage(level: level, usedAt: DateTime.now()));
  }

  @override
  Future<void> recordSessionSubmission({
    required String sessionId,
    required String answer,
    required bool isCorrect,
  }) async {
    submissions.add(
      LearningSubmission(
        answer: answer,
        isCorrect: isCorrect,
        submittedAt: DateTime.now(),
      ),
    );
  }

  @override
  Future<void> saveProfile(StudentProfile profile) async {}

  @override
  Future<LearningSession> startLearningSession({
    required ProblemSummary problem,
    required List<String> skillIds,
  }) async {
    startedSessions += 1;
    if (sessions.isNotEmpty) {
      return sessions.single;
    }
    final session = LearningSession(
      sessionId: 'session_1',
      problemId: problem.id,
      unit: problem.unit,
      skillIds: skillIds,
      startedAt: DateTime.now(),
      finishedAt: null,
      hints: const [],
      submissions: const [],
    );
    sessions.add(session);
    return session;
  }

  @override
  Future<void> updateAttemptErrorCategory({
    required String attemptId,
    required ErrorCategory category,
  }) async {}
}

const _summary = ProblemSummary(
  id: 'P-screen',
  grade: 3,
  subject: 'math',
  unit: 'addition',
  type: 'calc',
  title: 'Screen problem',
  path: '',
  raw: {},
);

const _content = ProblemContent(
  summary: _summary,
  semantic: {
    'metadata': {'question': '3 + 4는 얼마일까요?'},
  },
  solvable: {
    'target': '합',
    'method': '덧셈',
    'plan': '더한다',
    'steps': [
      {'explanation': '3 + 4', 'value': '7'},
    ],
    'diagnostics': {
      'skills': ['skill.add'],
    },
    'answer': {
      'value': 7,
      'choices': ['5', '7'],
    },
  },
);

const _diagnosticContent = ProblemContent(
  summary: _summary,
  svg: '<svg></svg>',
  semantic: {
    'answer': {
      'value': 507,
      'unit': '개',
    },
  },
  solvable: {
    'given': [
      {
        'id': 'first',
        'value': 259,
      },
      {
        'id': 'second',
        'value': 248,
      },
    ],
    'answer': {
      'value': 507,
      'unit': '개',
      'answer_key': [
        {
          'slot_id': 'answer',
          'value': 507,
          'diagnostics': [
            {
              'id': 'diag.answer_equals_given_value',
              'condition': 'answer_equals_given_value',
              'concept': '구해야 할 것',
              'reason': '주어진 한 가족의 수만 답으로 씀',
              'feedback': '한 가족이 캔 수만 쓰면 안 돼요. 두 가족이 캔 고구마를 모두 더해 보세요.',
            },
            {
              'id': 'diag.addition_with_carry_wrong_answer',
              'condition': 'addition_with_carry_wrong_answer',
              'concept': '받아올림',
              'reason': '받아올림이 있는 덧셈에서 정답과 다른 숫자를 입력함',
              'feedback': '일의 자리부터 다시 계산해요. 10이 넘으면 올린 1을 다음 자리 계산에 꼭 넣어 보세요.',
            },
          ],
        },
      ],
    },
    'steps': [
      {
        'expr': '259 + 248',
        'value': 507,
      },
    ],
  },
);

const _rendererContent = ProblemContent(
  summary: _summary,
  semantic: {
    'metadata': {'question': '259 + 248은 얼마일까요?'},
  },
  renderer: {
    'view_box': {
      'width': 240,
      'height': 120,
    },
    'elements': [
      {
        'id': 'answer_box.rect',
        'type': 'rect',
        'attributes': {
          'x': 40,
          'y': 40,
          'width': 80,
          'height': 40,
        },
        'interaction': {
          'type': 'input',
          'role': 'answer',
          'value_type': 'digit',
          'max_length': 3,
          'include_in_submission': true,
        },
      },
    ],
  },
  solvable: {
    'target': '합',
    'method': '덧셈',
    'answer': {'value': 507},
  },
);
