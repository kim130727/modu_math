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
    final renderer = problemVisualRenderer(item.problem);
    final elements = (renderer['elements'] as List? ?? []).map((raw) {
      final element = assignmentMap(raw);
      final interaction = assignmentMap(element['interaction']);
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
        onFieldsChanged: (values) =>
            changed(values.length == 1 ? values.single : values));
  }
}
