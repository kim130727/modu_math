import 'package:flutter/material.dart';
import '../l10n/assignment_strings.dart';
import '../models/assignment.dart';
import 'math_keypad.dart';

class AssignmentAnswerInput extends StatefulWidget {
  const AssignmentAnswerInput(
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
  State<AssignmentAnswerInput> createState() => _AssignmentAnswerInputState();
}

class _AssignmentAnswerInputState extends State<AssignmentAnswerInput> {
  final controllers = <TextEditingController>[];
  int active = 0;
  bool keypad = false;
  List<dynamic> get values => widget.item.fields.length > 1
      ? (widget.value is List
          ? List<dynamic>.from(widget.value as List)
          : List.filled(widget.item.fields.length, null))
      : [widget.value];
  void sync() {
    while (controllers.length < widget.item.fields.length) {
      controllers.add(TextEditingController());
    }
    for (var i = 0; i < controllers.length; i++) {
      final text = i < values.length ? values[i]?.toString() ?? '' : '';
      if (controllers[i].text != text) controllers[i].text = text;
    }
  }

  @override
  void initState() {
    super.initState();
    sync();
  }

  @override
  void didUpdateWidget(covariant AssignmentAnswerInput oldWidget) {
    super.didUpdateWidget(oldWidget);
    sync();
  }

  @override
  void dispose() {
    for (final c in controllers) {
      c.dispose();
    }
    super.dispose();
  }

  void change(int index, dynamic value) {
    final next = values;
    while (next.length < widget.item.fields.length) {
      next.add(null);
    }
    next[index] = value;
    widget.changed(widget.item.fields.length == 1 ? value : next);
  }

  @override
  Widget build(BuildContext context) {
    final strings = AssignmentStrings.of(context);
    return Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
      ...widget.item.fields.indexed.map((entry) {
        final i = entry.$1;
        final field = entry.$2;
        final label = strings.t('answer', {'number': i + 1});
        if (field.choices.isNotEmpty) {
          return Padding(
              padding: const EdgeInsets.only(bottom: 16),
              child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(label,
                        style: const TextStyle(
                            fontSize: 18, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 8),
                    Wrap(
                        spacing: 10,
                        runSpacing: 10,
                        children: field.choices
                            .map((choice) => ChoiceChip(
                                  label: Text('${choice['label']}',
                                      style: const TextStyle(fontSize: 19)),
                                  selected: field.type == 'multi_choice'
                                      ? widget.value is List &&
                                          (widget.value as List)
                                              .contains(choice['value'])
                                      : values.length > i &&
                                          values[i] == choice['value'],
                                  onSelected: widget.enabled
                                      ? (_) {
                                          if (field.type == 'multi_choice') {
                                            final selected =
                                                widget.value is List
                                                    ? List<dynamic>.from(
                                                        widget.value as List)
                                                    : <dynamic>[];
                                            selected.contains(choice['value'])
                                                ? selected
                                                    .remove(choice['value'])
                                                : selected.add(choice['value']);
                                            widget.changed(selected);
                                          } else {
                                            change(i, choice['value']);
                                          }
                                        }
                                      : null,
                                ))
                            .toList())
                  ]));
        }
        return Padding(
            padding: const EdgeInsets.only(bottom: 16),
            child: TextField(
              key: ValueKey('assignment-answer-$i'),
              controller: controllers[i],
              enabled: widget.enabled,
              onTap: () => setState(() => active = i),
              onChanged: (value) => change(i, value),
              style: const TextStyle(fontSize: 26, fontWeight: FontWeight.w600),
              keyboardType: field.type == 'number'
                  ? const TextInputType.numberWithOptions(
                      decimal: true, signed: true)
                  : TextInputType.text,
              decoration: InputDecoration(
                  labelText: label,
                  hintText: strings.t('write'),
                  suffixText: widget.item.unit,
                  border: const OutlineInputBorder(),
                  suffixIcon: IconButton(
                      tooltip: strings.t('keypad'),
                      onPressed: widget.enabled
                          ? () => setState(() {
                                active = i;
                                keypad = !keypad;
                              })
                          : null,
                      icon: const Icon(Icons.dialpad))),
            ));
      }),
      if (keypad && widget.enabled)
        MathKeypad(
            showNextButton: false,
            onKeyPressed: (text) {
              final controller = controllers[active];
              controller.text += text;
              change(active, controller.text);
            },
            onBackspace: () {
              final controller = controllers[active];
              if (controller.text.isNotEmpty) {
                controller.text =
                    controller.text.substring(0, controller.text.length - 1);
                change(active, controller.text);
              }
            },
            onClear: () {
              controllers[active].clear();
              change(active, '');
            }),
    ]);
  }
}
