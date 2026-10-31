import 'package:flutter/material.dart';

import '../l10n/app_strings.dart';
import '../l10n/assignment_strings.dart';
import '../models/assignment.dart';
import '../services/student_assignment_service.dart';
import '../utils/problem_presentation.dart';
import '../widgets/assignment_answer_input.dart';
import '../widgets/renderer_json_canvas.dart';
import 'student_assignments_screen.dart';

/// Public practice and approved classroom groups share the server access policy.
/// Content is fetched on entry and is never persisted in the offline bundle.
class ProblemLibraryScreen extends StatefulWidget {
  const ProblemLibraryScreen({super.key, required this.service});
  final StudentAssignmentService service;
  @override
  State<ProblemLibraryScreen> createState() => _ProblemLibraryScreenState();
}

class _ProblemLibraryScreenState extends State<ProblemLibraryScreen> {
  int? classroom;
  int page = 1;
  String grade = '';
  String? language;
  Future<Map<String, dynamic>>? future;
  late final groups = widget.service.classes();

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final next = AppLocaleScope.maybeOf(context)?.locale.languageCode ?? 'ko';
    if (language != next) {
      language = next;
      page = 1;
      reload();
    }
  }

  void reload() => setState(() {
        future = widget.service.library(
            page: page,
            classroom: classroom,
            language: language ?? 'ko',
            grade: grade);
      });

  @override
  Widget build(BuildContext context) {
    final strings = AssignmentStrings.of(context);
    return Scaffold(
      appBar: AppBar(title: Text(strings.t('library')), actions: [
        IconButton(
            tooltip: strings.t('refresh'),
            onPressed: reload,
            icon: const Icon(Icons.refresh)),
        const SizedBox(width: 48)
      ]),
      body: ListView(padding: const EdgeInsets.all(24), children: [
        Text(strings.t('libraryWelcome'),
            style: Theme.of(context).textTheme.titleMedium),
        const SizedBox(height: 20),
        FutureBuilder<List<Map<String, dynamic>>>(
            future: groups,
            builder: (context, snapshot) =>
                Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Wrap(spacing: 10, runSpacing: 10, children: [
                    ChoiceChip(
                        label: Text(strings.t('publicProblems')),
                        selected: classroom == null,
                        onSelected: (_) {
                          classroom = null;
                          page = 1;
                          reload();
                        }),
                    ...?snapshot.data
                        ?.where((c) => c['status'] == 'approved')
                        .map((c) => ChoiceChip(
                            label: Text('${c['name']} · ${c['teacher_name']}'),
                            selected: classroom == c['id'],
                            onSelected: (_) {
                              classroom = c['id'] as int;
                              page = 1;
                              reload();
                            })),
                  ]),
                  ...?snapshot.data?.where((c) => c['status'] == 'pending').map(
                      (c) => Padding(
                          padding: const EdgeInsets.only(top: 10),
                          child: Text(
                              '${c['name']} · ${strings.t('classPending')}'))),
                  if (snapshot.hasError)
                    Text(assignmentError(context, snapshot.error!),
                        style: const TextStyle(color: Colors.red)),
                ])),
        const SizedBox(height: 16),
        DropdownButtonFormField<String>(
            initialValue: grade,
            decoration: InputDecoration(labelText: strings.t('gradeFilter')),
            items: [
              DropdownMenuItem(value: '', child: Text(strings.t('allGrades'))),
              ...[1, 2, 3, 4, 5, 6]
                  .map((g) => DropdownMenuItem(value: '$g', child: Text('$g')))
            ],
            onChanged: (value) {
              grade = value ?? '';
              page = 1;
              reload();
            }),
        const SizedBox(height: 16),
        FutureBuilder<Map<String, dynamic>>(
            future: future,
            builder: (context, snapshot) {
              if (snapshot.connectionState != ConnectionState.done) {
                return const Center(child: CircularProgressIndicator());
              }
              if (snapshot.hasError) {
                return Column(children: [
                  Text(assignmentError(context, snapshot.error!)),
                  TextButton(onPressed: reload, child: Text(strings.t('retry')))
                ]);
              }
              final data = snapshot.data!;
              final rows =
                  (data['results'] as List? ?? []).map(assignmentMap).toList();
              return Column(children: [
                if (rows.isEmpty)
                  Padding(
                      padding: const EdgeInsets.all(24),
                      child: Text(strings.t('libraryEmpty'))),
                ...rows.map((problem) => Card(
                        child: ListTile(
                      title: Text('${problem['title']}'),
                      subtitle: Text(
                          '${problem['owner_name']} · ${problem['unit'] ?? ''}'),
                      trailing: const Icon(Icons.arrow_forward),
                      onTap: () => Navigator.of(context).push(
                          MaterialPageRoute<void>(
                              builder: (_) => _PracticeScreen(
                                  service: widget.service,
                                  id: problem['id'] as int))),
                    ))),
                Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                  TextButton(
                      onPressed: data['previous'] == null
                          ? null
                          : () {
                              page--;
                              reload();
                            },
                      child: Text(strings.t('previous'))),
                  Text('$page'),
                  TextButton(
                      onPressed: data['next'] == null
                          ? null
                          : () {
                              page++;
                              reload();
                            },
                      child: Text(strings.t('next'))),
                ]),
              ]);
            }),
      ]),
    );
  }
}

class _PracticeScreen extends StatefulWidget {
  const _PracticeScreen({required this.service, required this.id});
  final StudentAssignmentService service;
  final int id;
  @override
  State<_PracticeScreen> createState() => _PracticeScreenState();
}

class _PracticeScreenState extends State<_PracticeScreen> {
  late Future<Map<String, dynamic>> future =
      widget.service.libraryProblem(widget.id);
  dynamic answer;
  bool busy = false;
  bool? correct;
  String? error;

  Future<void> submit() async {
    if (busy || answer == null) return;
    setState(() {
      busy = true;
      error = null;
    });
    try {
      final result = await widget.service.practice(widget.id, answer);
      if (mounted) setState(() => correct = result);
    } catch (e) {
      if (mounted) setState(() => error = assignmentError(context, e));
    } finally {
      if (mounted) setState(() => busy = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final strings = AssignmentStrings.of(context);
    return Scaffold(
        appBar: AppBar(title: Text(strings.t('practice'))),
        body: FutureBuilder<Map<String, dynamic>>(
          future: future,
          builder: (context, snapshot) {
            if (snapshot.connectionState != ConnectionState.done) {
              return const Center(child: CircularProgressIndicator());
            }
            if (snapshot.hasError) {
              return Center(
                  child: Column(mainAxisSize: MainAxisSize.min, children: [
                Text(assignmentError(context, snapshot.error!)),
                TextButton(
                    onPressed: () => setState(() =>
                        future = widget.service.libraryProblem(widget.id)),
                    child: Text(strings.t('retry')))
              ]));
            }
            final data = snapshot.data!;
            final item =
                AssignmentItem.fromJson({'id': widget.id, 'content': data});
            return ListView(padding: const EdgeInsets.all(24), children: [
              Text(item.prompt.isNotEmpty ? item.prompt : '${data['title']}',
                  style: const TextStyle(
                      fontSize: 24, fontWeight: FontWeight.bold)),
              Text('${strings.t('author')}: ${data['owner_name'] ?? ''}'),
              if ('${data['source_credit'] ?? ''}'.isNotEmpty)
                Text('${strings.t('source')}: ${data['source_credit']}'),
              if ('${data['rights_note'] ?? ''}'.isNotEmpty)
                Text('${data['rights_note']}'),
              const SizedBox(height: 16),
              if (item.problem.renderer.isNotEmpty)
                SizedBox(
                    height: 340,
                    child: RendererJsonCanvas(
                        renderer: problemVisualRenderer(item.problem),
                        suppressInputs: true)),
              AssignmentAnswerInput(
                  item: item,
                  value: answer,
                  enabled: !busy,
                  changed: (value) => setState(() {
                        answer = value;
                        correct = null;
                      })),
              const SizedBox(height: 20),
              FilledButton(
                  onPressed: busy || answer == null ? null : submit,
                  child: Text(strings.t(busy ? 'waiting' : 'send'))),
              if (correct != null)
                Padding(
                    padding: const EdgeInsets.all(16),
                    child: Text(strings.t(correct! ? 'correct' : 'incorrect'),
                        style: const TextStyle(fontSize: 22))),
              if (error != null)
                Text(error!, style: const TextStyle(color: Colors.red)),
            ]);
          },
        ));
  }
}
