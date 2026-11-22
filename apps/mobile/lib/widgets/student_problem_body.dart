import 'package:flutter/material.dart';
import '../l10n/assignment_strings.dart';
import '../models/assignment.dart';
import 'assignment_answer_input.dart';
import 'student_problem_canvas.dart';

/// The same authored problem and answer controls in practice and editor preview.
class StudentProblemBody extends StatelessWidget {
  const StudentProblemBody(
      {super.key,
      required this.item,
      required this.value,
      required this.enabled,
      required this.changed});
  final AssignmentItem item;
  final dynamic value;
  final bool enabled;
  final ValueChanged<dynamic> changed;

  @override
  Widget build(BuildContext context) {
    final strings = AssignmentStrings.of(context);
    final data = item.content;
    return Semantics(
        container: true,
        explicitChildNodes: true,
        child:
            Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
          Text(item.prompt.isNotEmpty ? item.prompt : '${data['title'] ?? ''}',
              style: TextStyle(
                  fontSize: MediaQuery.sizeOf(context).width < 600 ? 20 : 24,
                  height: 1.45,
                  fontWeight: FontWeight.bold)),
          const SizedBox(height: 16),
          if (item.showCanvas && item.problem.renderer.isNotEmpty)
            StudentProblemCanvas(
                item: item, value: value, enabled: enabled, changed: changed),
          const SizedBox(height: 20),
          if (!item.canvasInputs && !item.canvasSelect)
            AssignmentAnswerInput(
                key: ValueKey('student-input-${item.id}'),
                item: item,
                value: value,
                enabled: enabled,
                changed: changed),
          if ('${data['owner_name'] ?? ''}'.isNotEmpty ||
              '${data['source_credit'] ?? ''}'.isNotEmpty ||
              '${data['rights_note'] ?? ''}'.isNotEmpty)
            Padding(
              padding: const EdgeInsets.only(top: 16),
              child: Wrap(
                alignment: WrapAlignment.end,
                spacing: 12,
                runSpacing: 4,
                children: [
                  if ('${data['owner_name'] ?? ''}'.isNotEmpty)
                    Text('${strings.t('author')}: ${data['owner_name']}',
                        style: const TextStyle(
                            fontSize: 12, color: Color(0xFF64748B))),
                  if ('${data['source_credit'] ?? ''}'.isNotEmpty)
                    Text('${strings.t('source')}: ${data['source_credit']}',
                        style: const TextStyle(
                            fontSize: 12, color: Color(0xFF64748B))),
                  if ('${data['rights_note'] ?? ''}'.isNotEmpty)
                    Text('${data['rights_note']}',
                        style: const TextStyle(
                            fontSize: 12, color: Color(0xFF64748B))),
                ],
              ),
            ),
        ]));
  }
}
