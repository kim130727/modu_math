import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/models/content_models.dart';
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
