import 'dart:async';

import 'package:flutter/material.dart';

import '../l10n/assignment_strings.dart';
import '../models/assignment.dart';
import '../services/assignment_session.dart';
import '../services/auth_service.dart';
import '../services/student_assignment_service.dart';
import '../theme/app_theme.dart';
import '../utils/problem_presentation.dart';
import '../widgets/assignment_answer_input.dart';
import '../widgets/renderer_json_canvas.dart';
import 'student_assignments_screen.dart';

class AssignmentSolveScreen extends StatefulWidget {
  const AssignmentSolveScreen(
      {super.key,
      required this.assignmentId,
      required this.auth,
      required this.service});
  final int assignmentId;
  final AuthService auth;
  final StudentAssignmentService service;
  @override
  State<AssignmentSolveScreen> createState() => _AssignmentSolveScreenState();
}

class _AssignmentSolveScreenState extends State<AssignmentSolveScreen>
    with WidgetsBindingObserver {
  late final int? user = widget.auth.currentUser?.id;
  late final AssignmentSession session = AssignmentSession(
      service: widget.service, assignmentId: widget.assignmentId);
  bool wrongOnly = false;
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    unawaited(session.load());
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.resumed) {
      session.resume();
    } else {
      session.pause();
      if (!session.busy) unawaited(session.flush());
    }
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    session.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => AssignmentAccountGate(
      auth: widget.auth,
      expectedUser: user,
      builder: (_) => AnimatedBuilder(
          animation: session,
          builder: (context, _) {
            final strings = AssignmentStrings.of(context);
            final assignment = session.assignment;
            return PopScope(
                canPop: !session.busy,
                child: Scaffold(
                  backgroundColor: KidsPalette.canvas,
                  appBar: AppBar(
                      title: Text(assignment?.title ?? strings.t('title'),
                          overflow: TextOverflow.ellipsis),
                      actions: [
                        IconButton(
                            tooltip: strings.t('refresh'),
                            onPressed: session.busy
                                ? null
                                : () async {
                                    await session.flush();
                                    await session.load();
                                  },
                            icon: const Icon(Icons.refresh)),
                        const SizedBox(width: 52)
                      ]),
                  body: session.loading
                      ? const Center(child: CircularProgressIndicator())
                      : assignment == null
                          ? Center(
                              child: Padding(
                                  padding: const EdgeInsets.all(24),
                                  child: Column(
                                      mainAxisSize: MainAxisSize.min,
                                      children: [
                                        Text(
                                            session.error == null
                                                ? strings.t('unavailable')
                                                : assignmentError(
                                                    context, session.error!),
                                            textAlign: TextAlign.center),
                                        TextButton(
                                            onPressed: session.load,
                                            child: Text(strings.t('retry'))),
                                      ])))
                          : SingleChildScrollView(
                              padding: const EdgeInsets.all(20),
                              child: Center(
                                  child: ConstrainedBox(
                                      constraints:
                                          const BoxConstraints(maxWidth: 1200),
                                      child: Column(
                                          crossAxisAlignment:
                                              CrossAxisAlignment.stretch,
                                          children: [
                                            if (session.error != null)
                                              _ErrorBox(
                                                  message: assignmentError(
                                                      context, session.error!)),
                                            if (assignment.submittedAt != null)
                                              ..._results(context, assignment)
                                            else
                                              ..._work(context, assignment),
                                          ])))),
                ));
          }));

  List<Widget> _work(BuildContext context, StudentAssignment assignment) {
    final strings = AssignmentStrings.of(context);
    final item = session.item;
    if (item == null) {
      return [
        Text(strings.t('unavailable'), style: const TextStyle(fontSize: 22))
      ];
    }
    final submitted =
        session.count(item) > 0 && !session.retrying.contains(item.id);
    final correctness = session.feedback.containsKey(item.id)
        ? session.feedback[item.id]
        : item.isCorrect;
    final card = _Paper(
        child:
            Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
      Text(strings.t('question', {'number': item.position + 1}),
          style: const TextStyle(
              color: KidsPalette.primary,
              fontWeight: FontWeight.bold,
              fontSize: 18)),
      const SizedBox(height: 14),
      Text(item.prompt.isNotEmpty ? item.prompt : item.problem.prompt,
          style: const TextStyle(
              fontSize: 24, height: 1.5, fontWeight: FontWeight.w600)),
      const SizedBox(height: 18),
      if (item.problem.renderer.isNotEmpty)
        SizedBox(
            height: 280,
            child: RendererJsonCanvas(
                key: ValueKey('assignment-canvas-${item.id}'),
                renderer: problemVisualRenderer(item.problem),
                suppressInputs: true)),
    ]));
    final controls = _Paper(
        child:
            Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
      Text(
          strings.t('attempts',
              {'count': session.count(item), 'max': assignment.maxAttempts}),
          style: const TextStyle(fontSize: 16)),
      const SizedBox(height: 18),
      if (session.busy)
        const Padding(
            padding: EdgeInsets.only(bottom: 16),
            child: Center(child: CircularProgressIndicator())),
      AssignmentAnswerInput(
          key: ValueKey(item.id),
          item: item,
          value: session.answers[item.id],
          enabled: session.canEdit,
          changed: session.change),
      if (session.pending.contains(item.id))
        _ErrorBox(message: strings.t('pending')),
      if (submitted && !session.pending.contains(item.id))
        Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
                color: correctness == false
                    ? KidsPalette.warningSoft
                    : KidsPalette.successSoft,
                borderRadius: BorderRadius.circular(16)),
            child: Text(
                strings.t(correctness == true
                    ? 'correct'
                    : correctness == false
                        ? 'incorrect'
                        : 'saved'),
                style: const TextStyle(
                    fontSize: 20, fontWeight: FontWeight.bold))),
      const SizedBox(height: 16),
      if (session.canEdit || session.pending.contains(item.id))
        FilledButton(
            onPressed: session.canSend ? session.send : null,
            child: Padding(
                padding: const EdgeInsets.symmetric(vertical: 8),
                child: Text(
                    strings.t(session.busy
                        ? 'waiting'
                        : session.pending.contains(item.id)
                            ? 'resend'
                            : 'send'),
                    style: const TextStyle(fontSize: 20)))),
      if (submitted &&
          !session.pending.contains(item.id) &&
          assignment.canWork &&
          session.count(item) < assignment.maxAttempts)
        OutlinedButton(
            onPressed: session.busy ? null : session.retry,
            child: Text(strings.t('again'))),
      if (session.count(item) >= assignment.maxAttempts)
        Padding(
            padding: const EdgeInsets.only(top: 12),
            child: Text(strings.t('limit'))),
      if (!assignment.canWork)
        Text(strings.t('closed'),
            style: const TextStyle(color: KidsPalette.inkSoft)),
      if (session.draftStatus[item.id] != null)
        Padding(
            padding: const EdgeInsets.only(top: 12),
            child: Text(strings.t(session.draftStatus[item.id]!))),
      if (session.draftStatus[item.id] == 'localSaved')
        TextButton(
            onPressed: session.busy ? null : session.flush,
            child: Text(strings.t('save'))),
      if (item.hintTotal > 0) ...[
        const Divider(height: 32),
        OutlinedButton.icon(
            onPressed: !session.busy &&
                    assignment.canWork &&
                    (session.hintLists[item.id]?.length ?? 0) < item.hintTotal
                ? session.nextHint
                : null,
            icon: const Icon(Icons.lightbulb_outline),
            label: Text(strings.t('hint'))),
        ...?session.hintLists[item.id]?.indexed.map((h) => Padding(
            padding: const EdgeInsets.only(top: 12),
            child: Text(
                '${strings.t('hintTitle', {
                      'number': h.$1 + 1
                    })}\n${h.$2['text']}',
                style: const TextStyle(fontSize: 18, height: 1.5)))),
      ],
      if (item.answer != null && assignment.released)
        ..._explanation(context, item),
    ]));
    return [
      Text(
          strings.t('progress',
              {'done': session.completed, 'total': assignment.total}),
          style: const TextStyle(fontSize: 19, fontWeight: FontWeight.bold)),
      const SizedBox(height: 10),
      LinearProgressIndicator(
          value:
              assignment.total == 0 ? 0 : session.completed / assignment.total),
      const SizedBox(height: 20),
      LayoutBuilder(
          builder: (context, constraints) => constraints.maxWidth >= 850
              ? Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Expanded(flex: 3, child: card),
                  const SizedBox(width: 20),
                  Expanded(flex: 2, child: controls)
                ])
              : Column(children: [card, const SizedBox(height: 16), controls])),
      const SizedBox(height: 20),
      OverflowBar(
          alignment: MainAxisAlignment.spaceBetween,
          spacing: 12,
          overflowSpacing: 12,
          children: [
            OutlinedButton.icon(
                onPressed: !session.busy && session.index > 0
                    ? () => session.move(session.index - 1)
                    : null,
                icon: const Icon(Icons.arrow_back),
                label: Text(strings.t('previous'))),
            FilledButton.icon(
                onPressed:
                    !session.busy && session.index < assignment.items.length - 1
                        ? () => session.move(session.index + 1)
                        : null,
                icon: const Icon(Icons.arrow_forward),
                label: Text(strings.t('next'))),
          ]),
      const SizedBox(height: 24),
      Text(strings.t('finishHelp'), textAlign: TextAlign.center),
      const SizedBox(height: 12),
      FilledButton.icon(
          key: const ValueKey('finish-assignment'),
          onPressed: session.canSubmit ? session.finish : null,
          icon: const Icon(Icons.task_alt),
          label: Padding(
              padding: const EdgeInsets.all(10),
              child: Text(strings.t('finish'),
                  style: const TextStyle(fontSize: 20)))),
    ];
  }

  List<Widget> _results(BuildContext context, StudentAssignment assignment) {
    final strings = AssignmentStrings.of(context);
    return [
      _Paper(
          child: Column(children: [
        const Icon(Icons.verified_outlined,
            size: 64, color: KidsPalette.success),
        const SizedBox(height: 16),
        Text(strings.t('finished'),
            style: const TextStyle(fontSize: 25, fontWeight: FontWeight.bold),
            textAlign: TextAlign.center),
        const SizedBox(height: 16),
        Text(
            assignment.released
                ? strings.t('score', {
                    'correct': assignment.correct ?? 0,
                    'total': assignment.total
                  })
                : strings.t('withheld'),
            style: const TextStyle(fontSize: 20),
            textAlign: TextAlign.center),
      ])),
      const SizedBox(height: 20),
      if (assignment.released)
        SwitchListTile(
            title: Text(strings.t('wrong')),
            value: wrongOnly,
            onChanged: (v) => setState(() => wrongOnly = v)),
      ...assignment.items
          .where((item) => !wrongOnly || item.isCorrect == false)
          .map((item) => Padding(
              padding: const EdgeInsets.only(bottom: 16),
              child: _Paper(
                  child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                    Text(strings.t('question', {'number': item.position + 1}),
                        style: const TextStyle(
                            fontSize: 18, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 10),
                    Text(item.prompt,
                        style: const TextStyle(fontSize: 20, height: 1.5)),
                    const SizedBox(height: 12),
                    Text(
                        '${strings.t('myAnswer')}: ${displaySubmittedAnswer(item, strings)}',
                        style: const TextStyle(fontSize: 19)),
                    if (assignment.released) ...[
                      Text(
                          strings.t(
                              item.isCorrect == true ? 'correct' : 'incorrect'),
                          style: TextStyle(
                              color: item.isCorrect == true
                                  ? KidsPalette.success
                                  : KidsPalette.error,
                              fontWeight: FontWeight.bold)),
                      ..._explanation(context, item)
                    ],
                  ])))),
      OutlinedButton(
          onPressed: () => Navigator.of(context).pop(),
          child: Text(strings.t('back'))),
    ];
  }

  List<Widget> _explanation(BuildContext context, AssignmentItem item) {
    final strings = AssignmentStrings.of(context);
    return [
      const Divider(height: 28),
      Text(
          '${strings.t('expected')}: ${displayAssignmentAnswer(item.answer, strings)}',
          style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
      ...(item.solution['steps'] as List? ?? []).map((raw) {
        final step = assignmentMap(raw);
        return Padding(
            padding: const EdgeInsets.only(top: 10),
            child: Text(
                '${step['explanation'] ?? step['expr'] ?? step['goal'] ?? ''}${step['value'] == null ? '' : '\n${step['value']}'}',
                style: const TextStyle(fontSize: 18, height: 1.5)));
      }),
    ];
  }
}

String displaySubmittedAnswer(AssignmentItem item, AssignmentStrings strings) {
  String label(AssignmentField field, dynamic value) {
    if (value is List) return value.map((v) => label(field, v)).join(', ');
    for (final choice in field.choices) {
      if (choice['value'] == value) return '${choice['label']}';
    }
    return displayAssignmentAnswer(value, strings);
  }

  if (item.fields.length == 1) {
    return label(item.fields.first, item.submittedAnswer);
  }
  final values =
      item.submittedAnswer is List ? item.submittedAnswer as List : const [];
  return item.fields.indexed
      .map((f) => label(f.$2, f.$1 < values.length ? values[f.$1] : null))
      .join(', ');
}

String displayAssignmentAnswer(dynamic value, AssignmentStrings strings) {
  if (value == null) return strings.t('noResponse');
  if (value is bool) return value ? 'O' : 'X';
  if (value is List) {
    return value.map((v) => displayAssignmentAnswer(v, strings)).join(', ');
  }
  if (value is Map) {
    if (value.containsKey('value')) {
      return displayAssignmentAnswer(value['value'], strings);
    }
    if (value.containsKey('answer_key')) {
      return displayAssignmentAnswer(value['answer_key'], strings);
    }
    return value.values
        .map((v) => displayAssignmentAnswer(v, strings))
        .join(', ');
  }
  return '$value';
}

class _Paper extends StatelessWidget {
  const _Paper({required this.child});
  final Widget child;
  @override
  Widget build(BuildContext context) => Container(
      width: double.infinity,
      padding: const EdgeInsets.all(22),
      decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(24),
          border: Border.all(color: KidsPalette.line)),
      child: child);
}

class _ErrorBox extends StatelessWidget {
  const _ErrorBox({required this.message});
  final String message;
  @override
  Widget build(BuildContext context) => Container(
      padding: const EdgeInsets.all(16),
      margin: const EdgeInsets.only(bottom: 16),
      color: KidsPalette.warningSoft,
      child: Text(message, style: const TextStyle(fontSize: 17)));
}
