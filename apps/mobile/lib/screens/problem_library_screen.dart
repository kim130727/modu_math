import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import '../l10n/app_strings.dart';
import '../l10n/assignment_strings.dart';
import '../models/assignment.dart';
import '../services/student_assignment_service.dart';
import '../theme/app_theme.dart';
import '../widgets/practice_goal_card.dart';
import 'practice_learning_screen.dart';
import 'student_assignments_screen.dart';

class ProblemLibraryScreen extends StatefulWidget {
  const ProblemLibraryScreen(
      {super.key,
      required this.service,
      this.embedded = false,
      this.active = true});
  final StudentAssignmentService service;
  final bool embedded;
  final bool active;
  @override
  State<ProblemLibraryScreen> createState() => _ProblemLibraryScreenState();
}

class _ProblemLibraryScreenState extends State<ProblemLibraryScreen>
    with WidgetsBindingObserver {
  Timer? refreshTimer;
  bool polling = false;
  Map<String, dynamic>? catalogSnapshot;
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    refreshTimer =
        Timer.periodic(const Duration(seconds: 5), (_) => pollCatalog());
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.resumed) pollCatalog();
  }

  Future<void> pollCatalog() async {
    if (!mounted ||
        !widget.active ||
        polling ||
        catalogSnapshot == null ||
        ModalRoute.of(context)?.isCurrent == false) {
      return;
    }
    final lifecycle = WidgetsBinding.instance.lifecycleState;
    if (lifecycle != null && lifecycle != AppLifecycleState.resumed) return;
    final scope = '$classroom|$language';
    polling = true;
    try {
      final next = await widget.service
          .catalog(classroom: classroom, language: language);
      if (!mounted || scope != '$classroom|$language') return;
      final contentChanged = catalogSnapshot?['revision'] != next['revision'];
      if (jsonEncode(catalogSnapshot) != jsonEncode(next)) {
        setState(() {
          catalogSnapshot = next;
          catalogFuture = Future.value(next);
        });
        if (contentChanged && step == 2) loadProblems();
      }
    } catch (_) {
      /* Existing content remains readable while offline. */
    } finally {
      polling = false;
    }
  }

  final scroll = ScrollController();
  int? classroom;
  int step = 0;
  String grade = '';
  String? category;
  String language = '';
  int page = 1;
  Future<Map<String, dynamic>>? catalogFuture;
  Future<Map<String, dynamic>>? problemsFuture;
  late Future<List<Map<String, dynamic>>> groups = widget.service.classes();
  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final next = AppLocaleScope.maybeOf(context)?.locale.languageCode ?? 'ko';
    if (language != next) {
      language = next;
      step = 0;
      refreshCatalog();
    }
  }

  void refreshCatalog() => setState(() {
        catalogFuture = widget.service
            .catalog(classroom: classroom, language: language)
            .then((data) {
          catalogSnapshot = data;
          return data;
        });
      });
  void loadProblems() {
    setState(() {
      problemsFuture = widget.service.library(
          page: page,
          classroom: classroom,
          language: language,
          grade: grade,
          category: category);
    });
    if (scroll.hasClients) scroll.jumpTo(0);
  }

  void changeStep(int value) {
    setState(() => step = value);
    if (scroll.hasClients) scroll.jumpTo(0);
  }

  @override
  void dispose() {
    refreshTimer?.cancel();
    WidgetsBinding.instance.removeObserver(this);
    scroll.dispose();
    super.dispose();
  }

  void refresh() {
    groups = widget.service.classes();
    refreshCatalog();
    if (step == 2) loadProblems();
  }

  void chooseScope(int? id) {
    classroom = id;
    step = 0;
    grade = '';
    category = null;
    page = 1;
    refreshCatalog();
    if (scroll.hasClients) scroll.jumpTo(0);
  }

  Future<void> openPractice(List<Map<String, dynamic>> problems, int index,
      Map<String, dynamic> goal, Map<String, dynamic> list) async {
    await Navigator.of(context).push(MaterialPageRoute<void>(
        builder: (_) => PracticeLearningScreen(
            service: widget.service,
            initialProblems: problems,
            initialIndex: index,
            initialGoal: goal,
            nextPage: list['next'] == null ? null : page + 1,
            previousPage: list['previous'] == null ? null : page - 1,
            total: list['count'] as int? ?? problems.length,
            startPosition: (page - 1) * 50,
            classroom: classroom,
            grade: grade,
            category: category,
            language: language)));
    if (mounted) refreshCatalog();
  }

  Widget failure(Object error, VoidCallback retry) => Column(children: [
        Text(assignmentError(context, error)),
        TextButton(
            onPressed: retry,
            child: Text(AssignmentStrings.of(context).t('retry'))),
      ]);
  @override
  Widget build(BuildContext context) {
    final s = AssignmentStrings.of(context);
    return Scaffold(
      backgroundColor: KidsPalette.canvas,
      appBar: widget.embedded
          ? null
          : AppBar(title: Text(s.t('library')), actions: [
              IconButton(
                  tooltip: s.t('refresh'),
                  onPressed: refresh,
                  icon: const Icon(Icons.refresh)),
              const SizedBox(width: 48),
            ]),
      body: Center(
          child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 1120),
              child: ListView(
                  controller: scroll,
                  padding: const EdgeInsets.all(20),
                  children: [
                    if (widget.embedded)
                      Row(children: [
                        Expanded(
                            child: Text(s.t('library'),
                                style: Theme.of(context).textTheme.titleLarge)),
                        IconButton(
                            tooltip: s.t('refresh'),
                            onPressed: refresh,
                            icon: const Icon(Icons.refresh)),
                      ]),
                    Text(s.t('learningPathHelp'),
                        style: Theme.of(context).textTheme.bodyLarge),
                    const SizedBox(height: 16),
                    FutureBuilder<List<Map<String, dynamic>>>(
                        future: groups,
                        builder: (context, state) => Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Wrap(spacing: 8, runSpacing: 8, children: [
                                    ChoiceChip(
                                        label: Text(s.t('publicProblems')),
                                        selected: classroom == null,
                                        onSelected: (_) => chooseScope(null)),
                                    ...?state.data
                                        ?.where(
                                            (c) => c['status'] == 'approved')
                                        .map((c) => ChoiceChip(
                                            label: Text(
                                                '${c['name']} · ${c['teacher_name']}'),
                                            selected: classroom == c['id'],
                                            onSelected: (_) =>
                                                chooseScope(c['id'] as int))),
                                  ]),
                                  ...?state.data
                                      ?.where((c) => c['status'] == 'pending')
                                      .map((c) => Text(
                                          '${c['name']} · ${s.t('classPending')}')),
                                  if (state.hasError)
                                    failure(state.error!, refresh),
                                ])),
                    const SizedBox(height: 20),
                    FutureBuilder<Map<String, dynamic>>(
                        future: catalogFuture,
                        builder: (context, state) {
                          if (state.connectionState != ConnectionState.done) {
                            return const Center(
                                child: CircularProgressIndicator());
                          }
                          if (state.hasError) {
                            return failure(state.error!, refreshCatalog);
                          }
                          final catalog = state.data!;
                          final levels = (catalog['grades'] as List? ?? [])
                              .map(assignmentMap)
                              .toList();
                          final goal = assignmentMap(catalog['goal']);
                          final count = levels.fold<int>(
                              0, (n, row) => n + (row['count'] as int? ?? 0));
                          final categories = <String, int>{};
                          for (final level in levels.where((l) =>
                              grade.isEmpty || '${l['grade']}' == grade)) {
                            for (final raw
                                in level['categories'] as List? ?? []) {
                              final c = assignmentMap(raw);
                              categories['${c['key']}'] =
                                  (categories['${c['key']}'] ?? 0) +
                                      (c['count'] as int);
                            }
                          }
                          String gradeTitle() => grade.isEmpty
                              ? s.t('allGrades')
                              : grade == 'null'
                                  ? s.t('otherLevel')
                                  : s.t('gradeCard', {'grade': grade});
                          return Column(
                              crossAxisAlignment: CrossAxisAlignment.stretch,
                              children: [
                                PracticeGoalCard(goal: goal),
                                const SizedBox(height: 16),
                                Wrap(
                                    crossAxisAlignment:
                                        WrapCrossAlignment.center,
                                    children: [
                                      TextButton(
                                          onPressed: () => changeStep(0),
                                          child: Text(s.t('chooseLevel'))),
                                      if (step >= 1) ...[
                                        const Icon(Icons.chevron_right,
                                            size: 18),
                                        TextButton(
                                            onPressed: () => changeStep(1),
                                            child: Text(gradeTitle()))
                                      ],
                                      if (step == 2) ...[
                                        const Icon(Icons.chevron_right,
                                            size: 18),
                                        Padding(
                                            padding: const EdgeInsets.all(8),
                                            child: Text(category == null
                                                ? s.t('allCategories')
                                                : category!.isEmpty
                                                    ? s.t('otherCategory')
                                                    : category!))
                                      ],
                                    ]),
                                const SizedBox(height: 12),
                                Text(
                                    s.t(step == 0
                                        ? 'chooseLevel'
                                        : step == 1
                                            ? 'chooseCategory'
                                            : 'chooseLesson'),
                                    style: Theme.of(context)
                                        .textTheme
                                        .headlineSmall),
                                const SizedBox(height: 16),
                                if (step == 0)
                                  _CardGrid(children: [
                                    _PathCard(
                                        title: s.t('allGrades'),
                                        subtitle: s.t(
                                            'problemCount', {'count': count}),
                                        icon: Icons.explore,
                                        onTap: count == 0
                                            ? null
                                            : () {
                                                grade = '';
                                                changeStep(1);
                                              }),
                                    for (var g = 1; g <= 6; g++)
                                      _PathCard(
                                          title: s.t('gradeCard', {'grade': g}),
                                          subtitle: s.t('problemCount', {
                                            'count': levels
                                                .where((l) => l['grade'] == g)
                                                .fold<int>(
                                                    0,
                                                    (n, l) =>
                                                        n + (l['count'] as int))
                                          }),
                                          number: '$g',
                                          icon: Icons.school,
                                          onTap:
                                              levels.any((l) => l['grade'] == g)
                                                  ? () {
                                                      grade = '$g';
                                                      changeStep(1);
                                                    }
                                                  : null),
                                    if (levels.any((l) => l['grade'] == null))
                                      _PathCard(
                                          title: s.t('otherLevel'),
                                          subtitle: s.t('otherCategory'),
                                          icon: Icons.auto_awesome,
                                          onTap: () {
                                            grade = 'null';
                                            changeStep(1);
                                          }),
                                  ]),
                                if (step == 1)
                                  _CardGrid(children: [
                                    _PathCard(
                                        title: s.t('allCategories'),
                                        subtitle: s.t('practice'),
                                        icon: Icons.apps,
                                        onTap: () {
                                          category = null;
                                          page = 1;
                                          step = 2;
                                          loadProblems();
                                        }),
                                    for (final entry in categories.entries)
                                      _PathCard(
                                          title: entry.key.isEmpty
                                              ? s.t('otherCategory')
                                              : entry.key,
                                          subtitle: s.t('problemCount',
                                              {'count': entry.value}),
                                          icon: Icons.calculate_outlined,
                                          onTap: () {
                                            category = entry.key;
                                            page = 1;
                                            step = 2;
                                            loadProblems();
                                          }),
                                  ]),
                                if (step == 2)
                                  FutureBuilder<Map<String, dynamic>>(
                                      future: problemsFuture,
                                      builder: (context, listing) {
                                        if (listing.connectionState !=
                                            ConnectionState.done) {
                                          return const Center(
                                              child:
                                                  CircularProgressIndicator());
                                        }
                                        if (listing.hasError) {
                                          return failure(
                                              listing.error!, loadProblems);
                                        }
                                        final list = listing.data!;
                                        final rows =
                                            (list['results'] as List? ?? [])
                                                .map(assignmentMap)
                                                .toList();
                                        return Column(
                                            crossAxisAlignment:
                                                CrossAxisAlignment.stretch,
                                            children: [
                                              if (rows.isEmpty)
                                                Text(s.t('libraryEmpty')),
                                              if (rows.isNotEmpty)
                                                Padding(
                                                    padding:
                                                        const EdgeInsets.only(
                                                            bottom: 16),
                                                    child: FilledButton.icon(
                                                        icon: const Icon(
                                                            Icons.play_arrow),
                                                        label: Text(s.t(
                                                            'startLearning')),
                                                        onPressed: () =>
                                                            openPractice(
                                                                rows,
                                                                0,
                                                                goal,
                                                                list))),
                                              _CardGrid(children: [
                                                for (final row in rows)
                                                  _PathCard(
                                                      title: '${row['title']}',
                                                      subtitle:
                                                          '${row['owner_name'] ?? ''}',
                                                      icon: Icons.edit_note,
                                                      onTap: () => openPractice(
                                                          rows,
                                                          rows.indexOf(row),
                                                          goal,
                                                          list))
                                              ]),
                                              Row(
                                                  mainAxisAlignment:
                                                      MainAxisAlignment.center,
                                                  children: [
                                                    TextButton(
                                                        onPressed:
                                                            list['previous'] ==
                                                                    null
                                                                ? null
                                                                : () {
                                                                    page--;
                                                                    loadProblems();
                                                                  },
                                                        child: Text(s.t(
                                                            'previousPage'))),
                                                    Text('$page'),
                                                    TextButton(
                                                        onPressed:
                                                            list['next'] == null
                                                                ? null
                                                                : () {
                                                                    page++;
                                                                    loadProblems();
                                                                  },
                                                        child: Text(
                                                            s.t('nextPage'))),
                                                  ]),
                                            ]);
                                      }),
                                if (count == 0)
                                  Padding(
                                      padding: const EdgeInsets.all(24),
                                      child: Text(s.t('libraryEmpty'))),
                              ]);
                        }),
                  ]))),
    );
  }
}

class _CardGrid extends StatelessWidget {
  const _CardGrid({required this.children});
  final List<Widget> children;
  @override
  Widget build(BuildContext context) => LayoutBuilder(builder: (context, c) {
        final columns = c.maxWidth >= 900
            ? 3
            : c.maxWidth >= 320
                ? 2
                : 1;
        final width = (c.maxWidth - (columns - 1) * 12) / columns;
        return Wrap(spacing: 12, runSpacing: 12, children: [
          for (final child in children) SizedBox(width: width, child: child)
        ]);
      });
}

class _PathCard extends StatelessWidget {
  const _PathCard(
      {required this.title,
      required this.subtitle,
      required this.icon,
      this.number,
      this.onTap});
  final String title;
  final String subtitle;
  final IconData icon;
  final String? number;
  final VoidCallback? onTap;
  @override
  Widget build(BuildContext context) => Card(
      clipBehavior: Clip.antiAlias,
      margin: EdgeInsets.zero,
      child: InkWell(
          onTap: onTap,
          child: Padding(
              padding: const EdgeInsets.all(16),
              child: Opacity(
                  opacity: onTap == null ? .45 : 1,
                  child: LayoutBuilder(builder: (context, constraints) {
                    final badge = Container(
                        width: 52,
                        height: 52,
                        alignment: Alignment.center,
                        decoration: BoxDecoration(
                            color: KidsPalette.primarySoft,
                            borderRadius: BorderRadius.circular(16)),
                        child: number == null
                            ? Icon(icon, color: KidsPalette.primary, size: 30)
                            : Text(number!,
                                style: const TextStyle(
                                    fontSize: 28,
                                    fontWeight: FontWeight.w800,
                                    color: KidsPalette.primary)));
                    final label = Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(title,
                              style: const TextStyle(
                                  fontSize: 18, fontWeight: FontWeight.w700)),
                          const SizedBox(height: 6),
                          Text(subtitle,
                              style:
                                  const TextStyle(color: KidsPalette.inkSoft)),
                        ]);
                    const arrow =
                        Icon(Icons.chevron_right, color: KidsPalette.primary);
                    return constraints.maxWidth < 230
                        ? Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                                Row(
                                    mainAxisAlignment:
                                        MainAxisAlignment.spaceBetween,
                                    children: [badge, arrow]),
                                const SizedBox(height: 14),
                                label,
                              ])
                        : Row(children: [
                            badge,
                            const SizedBox(width: 14),
                            Expanded(child: label),
                            arrow
                          ]);
                  })))));
}
