import 'package:flutter/material.dart';

import '../l10n/app_strings.dart';
import '../models/content_models.dart';

class AnswerPanel extends StatefulWidget {
  const AnswerPanel({
    super.key,
    required this.content,
    required this.answerDraft,
    required this.isCorrect,
    this.diagnosticFeedback,
    required this.onAnswerChanged,
    required this.onSubmit,
  });

  final ProblemContent content;
  final String answerDraft;
  final bool? isCorrect;
  final String? diagnosticFeedback;
  final ValueChanged<String> onAnswerChanged;
  final ValueChanged<String> onSubmit;

  @override
  State<AnswerPanel> createState() => _AnswerPanelState();
}

class _AnswerPanelState extends State<AnswerPanel> {
  final TextEditingController controller = TextEditingController();
  int? selectedChoiceIndex;
  Set<int> selectedChoiceIndexes = {};
  Map<int, int> selectedGroupChoices = {};

  @override
  void initState() {
    super.initState();
    controller.text = widget.answerDraft;
  }

  @override
  void didUpdateWidget(covariant AnswerPanel oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.answerDraft == controller.text) {
      return;
    }
    controller.text = widget.answerDraft;
    controller.selection = TextSelection.collapsed(
      offset: controller.text.length,
    );
  }

  @override
  void dispose() {
    controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final choiceGroups = widget.content.choiceGroups;
    final choices = widget.content.choices;
    final strings = AppStrings.of(context);
    final allowsMultipleChoices = _allowsMultipleChoices(widget.content);
    final hasVisual = widget.content.renderer.isNotEmpty ||
        widget.content.svg.isNotEmpty;

    final String titleText;
    if (!hasVisual) {
      titleText = widget.content.prompt;
    } else if (choiceGroups.isNotEmpty) {
      titleText = '각 항목에 알맞은 정답을 선택하세요';
    } else if (choices.isNotEmpty) {
      titleText = allowsMultipleChoices
          ? '알맞은 정답을 모두 선택하세요'
          : '알맞은 정답을 선택하세요';
    } else {
      titleText = '정답을 입력하세요';
    }

    final targetUnit = _targetUnit(widget.content);

    return Card(
      margin: EdgeInsets.zero,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: const BorderSide(color: Color(0xFFE5E7EB)),
      ),
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Row(
              children: [
                Icon(
                  choices.isNotEmpty
                      ? Icons.check_circle_outline_rounded
                      : Icons.edit_note_rounded,
                  color: const Color(0xFF5C6AC4),
                  size: 22,
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    titleText,
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(
                          fontWeight: FontWeight.bold,
                        ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            if (choiceGroups.isNotEmpty) ...[
              for (var (groupIndex, group) in choiceGroups.indexed) ...[
                if (group.label.isNotEmpty) ...[
                  Padding(
                    padding: const EdgeInsets.only(bottom: 8),
                    child: Text(
                      group.label,
                      style: const TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                        color: Color(0xFF374151),
                      ),
                    ),
                  ),
                ],
                Wrap(
                  spacing: 10,
                  runSpacing: 10,
                  children: group.choices.indexed.map((entry) {
                    final choiceIndex = entry.$1;
                    final choiceText = entry.$2;
                    final selected =
                        selectedGroupChoices[groupIndex] == choiceIndex;
                    return ChoiceChip(
                      selected: selected,
                      label:
                          Text(choiceText, style: const TextStyle(fontSize: 18)),
                      onSelected: (isSelected) {
                        setState(() {
                          if (isSelected) {
                            selectedGroupChoices[groupIndex] = choiceIndex;
                          } else {
                            selectedGroupChoices.remove(groupIndex);
                          }
                        });
                        final combinedAnswer = _combinedGroupAnswer(
                          choiceGroups,
                          selectedGroupChoices,
                        );
                        widget.onAnswerChanged(combinedAnswer);
                      },
                    );
                  }).toList(),
                ),
                if (groupIndex < choiceGroups.length - 1)
                  const SizedBox(height: 16),
              ],
            ] else if (choices.isEmpty)
              TextField(
                controller: controller,
                style: const TextStyle(
                    fontSize: 20, fontWeight: FontWeight.w600),
                decoration: InputDecoration(
                  labelText: targetUnit != null
                      ? '${strings.t('answer.inputLabel')} ($targetUnit)'
                      : strings.t('answer.inputLabel'),
                  suffixText: targetUnit,
                  suffixStyle: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: Color(0xFF4B5563),
                  ),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
                onChanged: widget.onAnswerChanged,
                onSubmitted: widget.onSubmit,
              )
            else
              Wrap(
                spacing: 10,
                runSpacing: 10,
                children: choices.indexed.map((entry) {
                  final choiceIndex = entry.$1;
                  final choice = entry.$2;
                  final selected = allowsMultipleChoices
                      ? selectedChoiceIndexes.contains(choiceIndex)
                      : selectedChoiceIndex == choiceIndex;
                  return ChoiceChip(
                    selected: selected,
                    label: Text(choice, style: const TextStyle(fontSize: 18)),
                    onSelected: (_) {
                      setState(() {
                        if (allowsMultipleChoices) {
                          selectedChoiceIndexes = {...selectedChoiceIndexes};
                          if (selectedChoiceIndexes.contains(choiceIndex)) {
                            selectedChoiceIndexes.remove(choiceIndex);
                          } else {
                            selectedChoiceIndexes.add(choiceIndex);
                          }
                          selectedChoiceIndex = null;
                        } else {
                          selectedChoiceIndex = choiceIndex;
                          selectedChoiceIndexes = {};
                        }
                      });
                      widget.onAnswerChanged(
                        allowsMultipleChoices
                            ? _selectedChoiceAnswer(
                                choices,
                                selectedChoiceIndexes,
                              )
                            : choice,
                      );
                    },
                  );
                }).toList(),
              ),
            const SizedBox(height: 16),
            FilledButton(
              onPressed: () {
                final String? answer;
                if (choiceGroups.isNotEmpty) {
                  if (selectedGroupChoices.length < choiceGroups.length) {
                    return;
                  }
                  answer = _combinedGroupAnswer(
                    choiceGroups,
                    selectedGroupChoices,
                  );
                } else if (choices.isEmpty) {
                  answer = controller.text;
                } else if (allowsMultipleChoices) {
                  answer =
                      _selectedChoiceAnswer(choices, selectedChoiceIndexes);
                } else {
                  answer = selectedChoiceIndex == null
                      ? null
                      : choices[selectedChoiceIndex!];
                }

                if (answer == null || answer.trim().isEmpty) {
                  return;
                }
                widget.onSubmit(answer);
              },
              child: Padding(
                padding: const EdgeInsets.symmetric(vertical: 12),
                child: Text(strings.t('answer.check'),
                    style: const TextStyle(fontSize: 18)),
              ),
            ),
            if (widget.isCorrect != null) ...[
              const SizedBox(height: 14),
              _ResultBanner(
                isCorrect: widget.isCorrect!,
                diagnosticFeedback: widget.diagnosticFeedback,
              ),
            ],
          ],
        ),
      ),
    );
  }
}

String _combinedGroupAnswer(
  List<ChoiceGroup> groups,
  Map<int, int> selectedGroupChoices,
) {
  return groups.indexed
      .map((entry) {
        final groupIndex = entry.$1;
        final group = entry.$2;
        final selectedIndex = selectedGroupChoices[groupIndex];
        return selectedIndex != null ? group.choices[selectedIndex] : '';
      })
      .where((s) => s.isNotEmpty)
      .join(', ');
}

bool _allowsMultipleChoices(ProblemContent content) {
  final answer = content.answerMap;
  final target = answer['target'];
  final targetType = target is Map<String, dynamic>
      ? target['type']?.toString().toLowerCase()
      : null;
  if (targetType != null &&
      (targetType.contains('multiple') ||
          targetType.contains('multi') ||
          targetType.contains('selected_'))) {
    return true;
  }
  final answerKey = answer['answer_key'];
  if (answerKey is List && answerKey.length > 1 && content.choices.isNotEmpty) {
    return true;
  }
  final value = answer['value'];
  return value is List && value.length > 1 && content.choices.isNotEmpty;
}

String _selectedChoiceAnswer(List<String> choices, Set<int> selectedIndexes) {
  return choices.indexed
      .where((entry) => selectedIndexes.contains(entry.$1))
      .map((entry) => entry.$2)
      .join();
}

class _ResultBanner extends StatelessWidget {
  const _ResultBanner({
    required this.isCorrect,
    this.diagnosticFeedback,
  });

  final bool isCorrect;
  final String? diagnosticFeedback;

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    final colorScheme = Theme.of(context).colorScheme;
    final backgroundColor =
        isCorrect ? const Color(0xFFDCFCE7) : colorScheme.errorContainer;
    final textColor =
        isCorrect ? const Color(0xFF166534) : colorScheme.onErrorContainer;

    final feedback = diagnosticFeedback?.trim() ?? '';
    final message = isCorrect
        ? strings.t('answer.correct')
        : feedback.isNotEmpty
            ? feedback
            : strings.t('answer.incorrectWithAnswer');

    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: backgroundColor,
        borderRadius: BorderRadius.circular(8),
      ),
      child: Text(
        message,
        style: TextStyle(
          color: textColor,
          fontSize: 18,
          fontWeight: FontWeight.w800,
        ),
      ),
    );
  }
}

String? _targetUnit(ProblemContent content) {
  final target = _mapAt(content.solvable, 'target');
  final unit = target['unit']?.toString() ??
      target['label']?.toString() ??
      _mapAt(content.solvable, 'inputs')['target_unit']?.toString();
  if (unit != null && unit.trim().isNotEmpty && unit.trim().length <= 5) {
    return unit.trim();
  }
  final match =
      RegExp(r'몇\s*([가-힣a-zA-Z]+)(?:입니까|\?|인지|인가요)').firstMatch(content.prompt);
  if (match != null) {
    final candidate = match.group(1);
    if (candidate != null && candidate.isNotEmpty && candidate.length <= 4) {
      return candidate;
    }
  }
  return null;
}

Map<String, dynamic> _mapAt(Object? value, Object? key) {
  final target = key == null
      ? value
      : value is Map
          ? value[key]
          : null;
  if (target is Map<String, dynamic>) {
    return target;
  }
  if (target is Map) {
    return target.map((k, v) => MapEntry(k.toString(), v));
  }
  return const {};
}
