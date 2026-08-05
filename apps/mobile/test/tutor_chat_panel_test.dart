import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/models/content_models.dart';
import 'package:modu_math_app/models/tutor_models.dart';
import 'package:modu_math_app/widgets/tutor_chat_panel.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  const ttsChannel = MethodChannel('flutter_tts');

  setUp(() {
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
        .setMockMethodCallHandler(ttsChannel, (_) async => 1);
  });

  tearDown(() {
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
        .setMockMethodCallHandler(ttsChannel, null);
  });

  testWidgets('shows a next problem button before the answer is solved',
      (tester) async {
    var openedNextProblem = false;

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: SingleChildScrollView(
            child: TutorChatPanel(
              content: _problemContent,
              messages: const [],
              isBusy: false,
              answerDraft: '',
              submittedAnswer: null,
              isCorrect: null,
              onAnswerChanged: (_) {},
              onSubmit: (_) {},
              onSend: (_) {},
              onHint: () {},
              onNextStep: () {},
              onRestart: () {},
              onReset: () {},
              hasNextProblem: true,
              onNextProblem: () => openedNextProblem = true,
              allowSkipProblem: true,
            ),
          ),
        ),
      ),
    );

    await tester.tap(find.byIcon(Icons.navigate_next));

    expect(find.byIcon(Icons.navigate_next), findsOneWidget);
    expect(openedNextProblem, isTrue);
  });

  testWidgets('keeps the solved state compact', (tester) async {
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: SingleChildScrollView(
            child: TutorChatPanel(
              content: _problemContent,
              messages: [
                TutorMessage(
                  role: TutorMessageRole.tutor,
                  text: '좋아요. 최종 답이 맞아요.',
                  createdAt: DateTime(2026),
                ),
              ],
              isBusy: false,
              answerDraft: '42',
              submittedAnswer: '42',
              isCorrect: true,
              onAnswerChanged: (_) {},
              onSubmit: (_) {},
              onSend: (_) {},
              onHint: () {},
              onNextStep: () {},
              onRestart: () {},
              onReset: () {},
              hasNextProblem: true,
              onNextProblem: () {},
            ),
          ),
        ),
      ),
    );

    expect(find.text('내 답'), findsOneWidget);
    expect(find.text('42'), findsOneWidget);
    expect(find.text('풀이 과정 보기'), findsOneWidget);
    expect(find.byIcon(Icons.check), findsNothing);
    expect(find.byIcon(Icons.lightbulb_outline), findsNothing);
    expect(find.byIcon(Icons.send), findsNothing);
  });
}

const _problemSummary = ProblemSummary(
  id: 'P001',
  grade: 3,
  subject: 'math',
  unit: 'unit',
  type: 'type',
  title: 'title',
  path: '',
  raw: {},
);

const _problemContent = ProblemContent(
  summary: _problemSummary,
  semantic: {},
  solvable: {
    'answer': {'value': 42},
  },
  renderer: {},
);
