import 'package:flutter/material.dart';
import '../l10n/assignment_strings.dart';
import '../models/assignment.dart';
import '../services/student_preview_bridge.dart';
import '../theme/app_theme.dart';
import '../widgets/student_problem_body.dart';

class StudentPreviewScreen extends StatefulWidget {
  const StudentPreviewScreen({super.key});
  @override
  State<StudentPreviewScreen> createState() => _StudentPreviewScreenState();
}

class _StudentPreviewScreenState extends State<StudentPreviewScreen> {
  late final StudentPreviewBridge bridge;
  AssignmentItem? item;
  dynamic answer;
  bool busy = false;
  bool? correct;
  String? error;
  @override
  void initState() {
    super.initState();
    bridge = StudentPreviewBridge(onContent: (content) {
      if (!mounted) return;
      setState(() {
        item = AssignmentItem.fromJson({'id': 0, 'content': content});
        answer = null;
        correct = null;
        busy = false;
        error = null;
      });
    }, onResult: (result) {
      if (mounted) {
        setState(() {
          busy = false;
          correct = result;
        });
      }
    }, onError: (message) {
      if (mounted) {
        setState(() {
          busy = false;
          error = message;
        });
      }
    });
    WidgetsBinding.instance.addPostFrameCallback((_) => bridge.ready());
  }

  @override
  void dispose() {
    bridge.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final strings = AssignmentStrings.of(context);
    final current = item;
    return Scaffold(
        body: current == null
            ? const Center(child: CircularProgressIndicator())
            : Center(
                child: ConstrainedBox(
                    constraints: const BoxConstraints(maxWidth: 1040),
                    child:
                        ListView(padding: const EdgeInsets.all(24), children: [
                      StudentProblemBody(
                          item: current,
                          value: answer,
                          enabled: !busy && correct != true,
                          changed: (value) => setState(() {
                                answer = value;
                                correct = null;
                                error = null;
                              })),
                      const SizedBox(height: 16),
                      if (correct != null)
                        Padding(
                            padding: const EdgeInsets.only(bottom: 16),
                            child: Text(
                                strings.t(correct! ? 'correct' : 'incorrect'),
                                style: TextStyle(
                                    fontSize: 22,
                                    fontWeight: FontWeight.bold,
                                    color: correct!
                                        ? KidsPalette.success
                                        : KidsPalette.error))),
                      FilledButton(
                          onPressed: busy || answer == null || correct == true
                              ? null
                              : () {
                                  setState(() {
                                    busy = true;
                                    error = null;
                                  });
                                  bridge.submit(
                                      answer, '${current.content['revision']}');
                                },
                          child: Text(strings.t(busy ? 'waiting' : 'send'))),
                      if (error != null)
                        Padding(
                            padding: const EdgeInsets.only(top: 12),
                            child: Text(error!,
                                style:
                                    const TextStyle(color: KidsPalette.error))),
                    ]))));
  }
}
