import 'package:flutter/material.dart';
import '../models/assignment.dart';
import '../utils/problem_presentation.dart';
import 'problem_canvas.dart';

class StudentProblemCanvas extends StatelessWidget {
  const StudentProblemCanvas(
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
    final renderer = problemVisualRenderer(
      item.problem,
      keepCanvasChoices: item.canvasSelect,
    );
    final bindings = assignmentMap(item.presentation['canvas_bindings']);
    final bindingCounts = <dynamic, int>{};
    for (final field in bindings.values) {
      bindingCounts[field] = (bindingCounts[field] ?? 0) + 1;
    }
    final elements = (renderer['elements'] as List? ?? []).map((raw) {
      final element = assignmentMap(raw);
      final interaction = assignmentMap(element['interaction']);
      // Older assignment snapshots may still carry a three-character limit.
      // A single bound box holds a whole answer; split digit cells keep theirs.
      final field = bindings['${element['id']}'];
      if (field != null &&
          bindingCounts[field] == 1 &&
          interaction['role'] == 'answer' &&
          !const ['digit', 'digits', 'operator', 'comparison_operator']
              .contains(interaction['value_type']) &&
          interaction['keyboard'] != 'operator') {
        interaction['max_length'] = 64;
        interaction['auto_advance'] = false;
      }
      if (interaction['keyboard'] == 'number' &&
          const ['number', 'integer', 'decimal', 'fraction']
              .contains(interaction['value_type'])) {
        interaction['keyboard'] = 'decimal';
      }
      element['input_style'] = {
        ...assignmentMap(element['input_style']),
        '_value_type': interaction['value_type']
      };
      element['interaction'] = interaction;
      if (interaction['value_type'] == 'number') {
        interaction['value_type'] = 'decimal';
        if (interaction['keyboard'] == 'number') {
          interaction['keyboard'] = 'decimal';
        }
        return {...element, 'interaction': interaction};
      }
      return element;
    }).toList();
    final values = List<String>.generate(
        item.fields.length,
        (i) => item.fields.length == 1
            ? '${value ?? ''}'
            : value is List && i < value.length
                ? '${value[i] ?? ''}'
                : '');
    final selectedChoices = <String>{
      if (value is List)
        ...value.map((entry) => '$entry')
      else if (value != null && '$value'.isNotEmpty)
        '$value',
    };
    return ProblemCanvas(
        renderer: item.canvasInputs
            ? {
                ...renderer,
                'elements': elements,
                'field_bindings':
                    assignmentMap(item.presentation['canvas_bindings']),
              }
            : renderer,
        fieldValues: item.canvasInputs ? values : null,
        inputsEnabled: enabled,
        canvasChoices: item.canvasSelect ? item.canvasChoices : const [],
        selectedChoices: selectedChoices,
        onChoiceTap: item.canvasSelect
            ? (choiceValue) {
                if (!enabled) return;
                if (item.canvasSelectMulti) {
                  final next = Set<String>.from(selectedChoices);
                  if (next.contains(choiceValue)) {
                    next.remove(choiceValue);
                  } else {
                    next.add(choiceValue);
                  }
                  changed(next.isEmpty ? null : next.toList());
                } else {
                  changed(choiceValue);
                }
              }
            : null,
        onFieldsChanged: (values) =>
            changed(values.length == 1 ? values.single : values));
  }
}
