import 'package:flutter/material.dart';

import '../l10n/assignment_strings.dart';
import '../models/assignment.dart';
import '../models/auth_user.dart';
import '../services/auth_service.dart';
import '../services/student_assignment_service.dart';
import '../theme/app_theme.dart';
import 'assignment_solve_screen.dart';
import 'auth_screen.dart';

String assignmentError(BuildContext context, Object error) {
  final strings = AssignmentStrings.of(context);
  if (error is AssignmentApiException) {
    if (error.status == 401) return strings.t('loginExpired');
    if (['offline', 'pending', 'accountChanged', 'response', 'storage']
        .contains(error.message)) {
      return strings.t(error.message);
    }
    return error.message;
  }
  return strings.t('error');
}

class AssignmentAccountGate extends StatelessWidget {
  const AssignmentAccountGate(
      {super.key,
      required this.auth,
      required this.builder,
      this.expectedUser});
  final AuthService auth;
  final Widget Function(AuthUser user) builder;
  final int? expectedUser;
  @override
  Widget build(BuildContext context) => FutureBuilder<void>(
        future: auth.restoreSession(),
        builder: (context, ready) {
          if (ready.connectionState != ConnectionState.done) {
            return const Scaffold(
                body: Center(child: CircularProgressIndicator()));
          }
          return ValueListenableBuilder<AuthUser?>(
              valueListenable: auth.userNotifier,
              builder: (context, user, _) {
                final strings = AssignmentStrings.of(context);
                if (user != null &&
                    auth.isAuthenticated &&
                    (expectedUser == null || expectedUser == user.id)) {
                  return builder(user);
                }
                return Scaffold(
                    appBar: AppBar(title: Text(strings.t('title'))),
                    body: Center(
                        child: Padding(
                      padding: const EdgeInsets.all(24),
                      child: Column(mainAxisSize: MainAxisSize.min, children: [
                        const Icon(Icons.assignment_outlined,
                            size: 72, color: KidsPalette.primary),
                        const SizedBox(height: 24),
                        Text(
                            strings
                                .t(user != null ? 'accountChanged' : 'login'),
                            textAlign: TextAlign.center,
                            style: const TextStyle(fontSize: 22)),
                        const SizedBox(height: 20),
                        FilledButton(
                            onPressed: () async {
                              if (user != null && expectedUser != null) {
                                Navigator.of(context).pop();
                                return;
                              }
                              await Navigator.of(context).push(
                                  MaterialPageRoute<void>(
                                      builder: (_) =>
                                          AuthScreen(authService: auth)));
                            },
                            child: Text(strings
                                .t(user != null ? 'back' : 'loginButton'))),
                      ]),
                    )));
              });
        },
      );
}

class StudentAssignmentsScreen extends StatelessWidget {
  const StudentAssignmentsScreen(
      {super.key, required this.authService, this.service});
  final AuthService authService;
  final StudentAssignmentService? service;
  @override
  Widget build(BuildContext context) => AssignmentAccountGate(
      auth: authService,
      builder: (user) => _AssignmentList(
            key: ValueKey(user.id),
            auth: authService,
            service:
                service ?? StudentAssignmentService(authService: authService),
          ));
}

class _AssignmentList extends StatefulWidget {
  const _AssignmentList({super.key, required this.auth, required this.service});
  final AuthService auth;
  final StudentAssignmentService service;
  @override
  State<_AssignmentList> createState() => _AssignmentListState();
}

class _AssignmentListState extends State<_AssignmentList> {
  late Future<List<StudentAssignment>> future = widget.service.list();
  Future<void> refresh() async {
    final next = widget.service.list();
    setState(() {
      future = next;
    });
    try {
      await next;
    } catch (_) {}
  }

  Future<void> join() async {
    final joined = await showDialog<bool>(
        context: context,
        builder: (_) => AssignmentJoinDialog(service: widget.service));
    if (joined == true && mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(AssignmentStrings.of(context).t('joined'))));
    }
  }

  @override
  Widget build(BuildContext context) {
    final strings = AssignmentStrings.of(context);
    return Scaffold(
        backgroundColor: KidsPalette.canvas,
        appBar: AppBar(title: Text(strings.t('title')), actions: [
          IconButton(
              tooltip: strings.t('refresh'),
              onPressed: refresh,
              icon: const Icon(Icons.refresh)),
          IconButton(
              tooltip: strings.t('logout'),
              onPressed: widget.auth.logout,
              icon: const Icon(Icons.logout)),
          const SizedBox(width: 52),
        ]),
        body: RefreshIndicator(
            onRefresh: refresh,
            child: FutureBuilder<List<StudentAssignment>>(
                future: future,
                builder: (context, state) {
                  return ListView(
                      padding: const EdgeInsets.all(20),
                      physics: const AlwaysScrollableScrollPhysics(),
                      children: [
                        Center(
                            child: ConstrainedBox(
                                constraints:
                                    const BoxConstraints(maxWidth: 950),
                                child: Column(
                                    crossAxisAlignment:
                                        CrossAxisAlignment.stretch,
                                    children: [
                                      Container(
                                          padding: const EdgeInsets.all(24),
                                          decoration: BoxDecoration(
                                              color: KidsPalette.primarySoft,
                                              borderRadius:
                                                  BorderRadius.circular(24)),
                                          child: Column(
                                              crossAxisAlignment:
                                                  CrossAxisAlignment.start,
                                              children: [
                                                Text(
                                                    '${widget.auth.currentUser?.username ?? ''} 👋',
                                                    style: const TextStyle(
                                                        fontSize: 26,
                                                        fontWeight:
                                                            FontWeight.bold)),
                                                const SizedBox(height: 10),
                                                Text(strings.t('welcome'),
                                                    style: const TextStyle(
                                                        fontSize: 18,
                                                        height: 1.5)),
                                                const SizedBox(height: 16),
                                                OutlinedButton.icon(
                                                    onPressed: join,
                                                    icon: const Icon(Icons
                                                        .group_add_outlined),
                                                    label: Text(
                                                        strings.t('join'))),
                                              ])),
                                      const SizedBox(height: 24),
                                      if (state.connectionState !=
                                          ConnectionState.done)
                                        Padding(
                                            padding: const EdgeInsets.all(30),
                                            child: Column(children: [
                                              const CircularProgressIndicator(),
                                              const SizedBox(height: 16),
                                              Text(strings.t('loading'))
                                            ]))
                                      else if (state.hasError)
                                        Column(children: [
                                          Text(
                                              assignmentError(
                                                  context, state.error!),
                                              textAlign: TextAlign.center),
                                          TextButton(
                                              onPressed: refresh,
                                              child: Text(strings.t('retry')))
                                        ])
                                      else if (state.data!.isEmpty)
                                        Padding(
                                            padding: const EdgeInsets.all(40),
                                            child: Text(strings.t('empty'),
                                                textAlign: TextAlign.center,
                                                style: const TextStyle(
                                                    fontSize: 20)))
                                      else
                                        ...state.data!.map((assignment) => Card(
                                            margin: const EdgeInsets.only(
                                                bottom: 16),
                                            child: Padding(
                                                padding:
                                                    const EdgeInsets.all(22),
                                                child: Column(
                                                    crossAxisAlignment:
                                                        CrossAxisAlignment
                                                            .start,
                                                    children: [
                                                      Text(assignment.title,
                                                          style: const TextStyle(
                                                              fontSize: 22,
                                                              fontWeight:
                                                                  FontWeight
                                                                      .bold)),
                                                      const SizedBox(
                                                          height: 12),
                                                      Text(assignment
                                                                  .submittedAt !=
                                                              null
                                                          ? strings
                                                              .t('submitted')
                                                          : assignment.canWork
                                                              ? strings
                                                                  .t('ready')
                                                              : strings
                                                                  .t('closed')),
                                                      if (assignment.startsAt !=
                                                          null)
                                                        Text(
                                                            '${strings.t('start')}: ${assignmentDate(assignment.startsAt!)}'),
                                                      Text(assignment.dueAt ==
                                                              null
                                                          ? strings
                                                              .t('noDeadline')
                                                          : '${strings.t('due')}: ${assignmentDate(assignment.dueAt!)}'),
                                                      const SizedBox(
                                                          height: 14),
                                                      LinearProgressIndicator(
                                                          value: assignment
                                                              .progress),
                                                      const SizedBox(height: 8),
                                                      Text(strings.t(
                                                          'progress', {
                                                        'done': assignment
                                                            .completed,
                                                        'total':
                                                            assignment.total
                                                      })),
                                                      const SizedBox(
                                                          height: 14),
                                                      FilledButton.icon(
                                                          onPressed: () async {
                                                            await Navigator.of(context).push(MaterialPageRoute<
                                                                    void>(
                                                                builder: (_) => AssignmentSolveScreen(
                                                                    assignmentId:
                                                                        assignment
                                                                            .id,
                                                                    auth: widget
                                                                        .auth,
                                                                    service: widget
                                                                        .service)));
                                                            if (mounted) {
                                                              await refresh();
                                                            }
                                                          },
                                                          icon: Icon(assignment
                                                                      .submittedAt !=
                                                                  null
                                                              ? Icons
                                                                  .fact_check_outlined
                                                              : Icons
                                                                  .edit_outlined),
                                                          label: Text(strings.t(
                                                              assignment.submittedAt !=
                                                                      null
                                                                  ? 'results'
                                                                  : 'open'))),
                                                    ])))),
                                    ])))
                      ]);
                })));
  }
}

String assignmentDate(DateTime date) {
  // Dates in the learning platform are displayed in Korea Standard Time.
  final local = date.toUtc().add(const Duration(hours: 9));
  String two(int v) => v.toString().padLeft(2, '0');
  return '${local.year}-${two(local.month)}-${two(local.day)} ${two(local.hour)}:${two(local.minute)} (KST)';
}

class AssignmentJoinDialog extends StatefulWidget {
  const AssignmentJoinDialog({super.key, required this.service});
  final StudentAssignmentService service;
  @override
  State<AssignmentJoinDialog> createState() => _AssignmentJoinDialogState();
}

class _AssignmentJoinDialogState extends State<AssignmentJoinDialog> {
  final input = TextEditingController();
  final form = GlobalKey<FormState>();
  bool busy = false;
  Object? error;
  @override
  void dispose() {
    input.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final strings = AssignmentStrings.of(context);
    return PopScope(
        canPop: !busy,
        child: AlertDialog(
          title: Text(strings.t('join')),
          content: Form(
              key: form,
              child: Column(mainAxisSize: MainAxisSize.min, children: [
                TextFormField(
                    controller: input,
                    enabled: !busy,
                    decoration: InputDecoration(labelText: strings.t('code')),
                    validator: (value) => value == null || value.trim().isEmpty
                        ? strings.t('code')
                        : null),
                if (error != null)
                  Text(assignmentError(context, error!),
                      style: const TextStyle(color: KidsPalette.error)),
              ])),
          actions: [
            TextButton(
                onPressed: busy ? null : () => Navigator.pop(context),
                child: Text(strings.t('cancel'))),
            FilledButton(
                onPressed: busy
                    ? null
                    : () async {
                        if (!form.currentState!.validate()) return;
                        setState(() {
                          busy = true;
                          error = null;
                        });
                        try {
                          await widget.service.join(input.text);
                          if (context.mounted) Navigator.pop(context, true);
                        } catch (e) {
                          if (mounted) {
                            setState(() {
                              busy = false;
                              error = e;
                            });
                          }
                        }
                      },
                child: Text(strings.t('joinButton'))),
          ],
        ));
  }
}
