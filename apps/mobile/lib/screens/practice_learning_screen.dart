import 'dart:async';
import 'package:flutter/material.dart';
import '../l10n/assignment_strings.dart';
import '../models/assignment.dart';
import '../services/student_assignment_service.dart';
import '../theme/app_theme.dart';
import '../widgets/student_problem_body.dart';
import '../widgets/practice_goal_card.dart';
import 'student_assignments_screen.dart';

class PracticeLearningScreen extends StatefulWidget {
  const PracticeLearningScreen(
      {super.key,
      required this.service,
      required this.initialProblems,
      required this.initialIndex,
      required this.initialGoal,
      required this.nextPage,
      this.previousPage,
      required this.total,
      required this.startPosition,
      required this.classroom,
      required this.grade,
      required this.category,
      required this.language});
  final StudentAssignmentService service;
  final List<Map<String, dynamic>> initialProblems;
  final int initialIndex;
  final Map<String, dynamic> initialGoal;
  final int? nextPage;
  final int? previousPage;
  final int total;
  final int startPosition;
  final int? classroom;
  final String grade;
  final String? category;
  final String language;
  @override
  State<PracticeLearningScreen> createState() => _PracticeLearningScreenState();
}

class _PracticeLearningScreenState extends State<PracticeLearningScreen>
    with WidgetsBindingObserver {
  Timer? versionTimer;
  bool checkingVersion = false;
  final revisions = <int, String>{};
  final pendingRevisions = <int, String>{};
  late final int? expectedUser = widget.service.authService.currentUser?.id;
  late final problems = List<Map<String, dynamic>>.from(widget.initialProblems);
  late int index = widget.initialIndex;
  late int? nextPage = widget.nextPage;
  late int? previousPage = widget.previousPage;
  late int positionOffset = widget.startPosition;
  late Map<String, dynamic> goal = widget.initialGoal;
  final answers = <int, dynamic>{};
  final feedback = <int, bool>{};
  final details = <int, Future<Map<String, dynamic>>>{};
  final scroll = ScrollController();
  bool busy = false;
  String? error;
  int get id => problems[index]['id'] as int;
  Future<Map<String, dynamic>> get future =>
      details.putIfAbsent(id, () => loadProblem(id));
  Future<Map<String, dynamic>> loadProblem(int problemId) async {
    final data = await widget.service.libraryProblem(problemId);
    if (data['revision'] is String) {
      revisions[problemId] = data['revision'] as String;
    }
    return data;
  }

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    versionTimer =
        Timer.periodic(const Duration(seconds: 5), (_) => checkVersion());
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.resumed) checkVersion();
  }

  Future<void> checkVersion() async {
    final lifecycle = WidgetsBinding.instance.lifecycleState;
    if (!mounted ||
        busy ||
        checkingVersion ||
        !revisions.containsKey(id) ||
        (lifecycle != null && lifecycle != AppLifecycleState.resumed)) {
      return;
    }
    final problemId = id;
    checkingVersion = true;
    try {
      final revision = await widget.service.problemVersion(problemId);
      if (!mounted || id != problemId || revision == revisions[problemId]) {
        return;
      }
      if (answers[problemId] != null) {
        setState(() => pendingRevisions[problemId] = revision);
      } else {
        applyUpdate();
      }
    } on AssignmentApiException catch (e) {
      if (mounted && id == problemId && (e.status == 403 || e.status == 404)) {
        applyUpdate();
      }
    } finally {
      checkingVersion = false;
    }
  }

  void applyUpdate() {
    setState(() {
      details.remove(id);
      revisions.remove(id);
      pendingRevisions.remove(id);
      answers.remove(id);
      feedback.remove(id);
      error = null;
    });
  }

  @override
  void dispose() {
    versionTimer?.cancel();
    WidgetsBinding.instance.removeObserver(this);
    scroll.dispose();
    super.dispose();
  }

  Future<void> move(int delta) async {
    if (busy) return;
    final loadPrevious = index == 0 && delta < 0 && previousPage != null;
    if (loadPrevious ||
        (index + delta == problems.length && nextPage != null)) {
      setState(() {
        busy = true;
        error = null;
      });
      try {
        final listing = await widget.service.library(
            page: loadPrevious ? previousPage! : nextPage!,
            classroom: widget.classroom,
            grade: widget.grade,
            category: widget.category,
            language: widget.language);
        if (!mounted) return;
        final existing = problems.map((p) => p['id']).toSet();
        final added = (listing['results'] as List? ?? [])
            .map(assignmentMap)
            .where((p) => existing.add(p['id']))
            .toList();
        if (loadPrevious) {
          problems.insertAll(0, added);
          index += added.length;
          positionOffset -= added.length;
          previousPage = listing['previous'] == null ? null : previousPage! - 1;
        } else {
          problems.addAll(added);
          nextPage = listing['next'] == null ? null : nextPage! + 1;
        }
      } catch (e) {
        if (mounted) setState(() => error = assignmentError(context, e));
        return;
      } finally {
        if (mounted) setState(() => busy = false);
      }
    }
    if (mounted && index + delta >= 0 && index + delta < problems.length) {
      setState(() {
        index += delta;
        error = null;
      });
      if (scroll.hasClients) scroll.jumpTo(0);
      checkVersion();
    }
  }

  Future<void> submit() async {
    if (busy || answers[id] == null) return;
    final problemId = id;
    setState(() {
      busy = true;
      error = null;
    });
    try {
      final correct = await widget.service.practice(
          problemId, answers[problemId],
          revision: revisions[problemId]);
      if (!mounted) return;
      setState(() => feedback[problemId] = correct);
      if (correct) {
        try {
          final catalog = await widget.service
              .catalog(classroom: widget.classroom, language: widget.language);
          if (mounted) {
            final nextGoal = assignmentMap(catalog['goal']);
            final target = nextGoal['target'] as int? ?? 5;
            final before =
                (goal['completed_ids'] as List? ?? []).toSet().length;
            final after =
                (nextGoal['completed_ids'] as List? ?? []).toSet().length;
            setState(() => goal = nextGoal);
            if (target > 0 && before < target && after >= target) {
              ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                backgroundColor: KidsPalette.success,
                content: Text(AssignmentStrings.of(context)
                    .t('goalToast', {'count': target})),
              ));
            }
          }
        } catch (_) {
          if (mounted) {
            setState(() =>
                error = AssignmentStrings.of(context).t('goalSyncFailed'));
          }
        }
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          error = assignmentError(context, e);
          if (e is AssignmentApiException && e.status == 409) {
            pendingRevisions[problemId] = '';
          }
        });
      }
    } finally {
      if (mounted) setState(() => busy = false);
    }
  }

  @override
  Widget build(BuildContext context) => AssignmentAccountGate(
      auth: widget.service.authService,
      expectedUser: expectedUser,
      builder: (_) => buildPractice(context));

  Widget buildPractice(BuildContext context) {
    final s = AssignmentStrings.of(context);
    return Scaffold(
        appBar: AppBar(title: Text(s.t('practice'))),
        body: FutureBuilder<Map<String, dynamic>>(
            future: future,
            builder: (context, state) {
              if (state.connectionState != ConnectionState.done) {
                return const Center(child: CircularProgressIndicator());
              }
              if (state.hasError) {
                return Center(
                    child: Column(mainAxisSize: MainAxisSize.min, children: [
                  Text(assignmentError(context, state.error!)),
                  TextButton(
                      onPressed: () => setState(() => details.remove(id)),
                      child: Text(s.t('retry'))),
                ]));
              }
              final data = state.data!;
              final item = AssignmentItem.fromJson({'id': id, 'content': data});
              final result = feedback[id];
              return Center(
                  child: ConstrainedBox(
                      constraints: const BoxConstraints(maxWidth: 1040),
                      child: ListView(
                          controller: scroll,
                          padding: const EdgeInsets.all(24),
                          children: [
                            if (pendingRevisions.containsKey(id))
                              Card(
                                  child: Padding(
                                      padding: const EdgeInsets.all(16),
                                      child: Column(children: [
                                        Text(s.t('problemUpdated')),
                                        TextButton(
                                            onPressed:
                                                busy ? null : applyUpdate,
                                            child: Text(
                                                s.t('applyProblemUpdate'))),
                                      ]))),
                            PracticeGoalCard(goal: goal),
                            const SizedBox(height: 20),
                            Text(
                                s.t('lessonPosition', {
                                  'current': positionOffset + index + 1,
                                  'total': widget.total
                                }),
                                style: const TextStyle(
                                    color: KidsPalette.primary,
                                    fontWeight: FontWeight.bold)),
                            const SizedBox(height: 12),
                            StudentProblemBody(
                                key: ValueKey('practice-problem-$id'),
                                item: item,
                                value: answers[id],
                                enabled: !busy && result != true,
                                changed: (value) => setState(() {
                                      answers[id] = value;
                                      feedback.remove(id);
                                    })),
                            const SizedBox(height: 16),
                            if (result != null)
                              Padding(
                                  padding: const EdgeInsets.only(bottom: 16),
                                  child: Text(
                                      s.t(result ? 'correct' : 'incorrect'),
                                      style: TextStyle(
                                          fontSize: 22,
                                          fontWeight: FontWeight.bold,
                                          color: result
                                              ? KidsPalette.success
                                              : KidsPalette.error))),
                            FilledButton(
                                onPressed: busy ||
                                        pendingRevisions.containsKey(id) ||
                                        answers[id] == null ||
                                        result == true
                                    ? null
                                    : submit,
                                child: Text(s.t(busy ? 'waiting' : 'send'))),
                            if (error != null)
                              Padding(
                                  padding: const EdgeInsets.only(top: 12),
                                  child: Text(error!,
                                      style: const TextStyle(
                                          color: KidsPalette.error))),
                            const SizedBox(height: 20),
                            Row(children: [
                              Expanded(
                                  child: OutlinedButton.icon(
                                      onPressed: busy ||
                                              (index == 0 &&
                                                  previousPage == null)
                                          ? null
                                          : () => move(-1),
                                      icon: const Icon(Icons.arrow_back),
                                      label: Text(s.t('previous')))),
                              const SizedBox(width: 12),
                              Expanded(
                                  child: FilledButton.icon(
                                      onPressed: busy ||
                                              (index == problems.length - 1 &&
                                                  nextPage == null)
                                          ? null
                                          : () => move(1),
                                      icon: const Icon(Icons.arrow_forward),
                                      label: Text(s.t('next')))),
                            ]),
                            const SizedBox(height: 12),
                            TextButton(
                                onPressed:
                                    busy ? null : () => Navigator.pop(context),
                                child: Text(s.t('backToCategories'))),
                          ])));
            }));
  }
}
