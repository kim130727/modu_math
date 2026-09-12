import 'package:flutter/material.dart';

import '../l10n/app_strings.dart';
import '../models/content_models.dart';
import '../theme/app_theme.dart';
import '../utils/answer_normalizer.dart';
import 'math_keypad.dart';

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
  final List<TextEditingController> multiControllers = [];
  int? selectedChoiceIndex;
  Set<int> selectedChoiceIndexes = {};
  Map<int, int> selectedGroupChoices = {};
  bool _showKeypad = false;

  void _syncMultiControllers() {
    final fields = widget.content.multiAnswerFields;
    if (fields.isEmpty) {
      if (multiControllers.isNotEmpty) {
        for (final c in multiControllers) {
          c.dispose();
        }
        multiControllers.clear();
      }
      return;
    }
    while (multiControllers.length < fields.length) {
      multiControllers.add(TextEditingController());
    }
    while (multiControllers.length > fields.length) {
      multiControllers.removeLast().dispose();
    }
    final tokens = _extractTokensFromFormattedInput(widget.answerDraft);
    if (tokens.isNotEmpty) {
      for (var i = 0; i < fields.length; i++) {
        final token = i < tokens.length ? tokens[i] : '';
        if (multiControllers[i].text != token) {
          multiControllers[i].text = token;
        }
      }
    }
  }

  static List<String> _extractTokensFromFormattedInput(String raw) {
    final trimmed = raw.trim();
    if (trimmed.isEmpty) return const [];
    if (RegExp(r'[/,;|\s]').hasMatch(trimmed)) {
      final tokens = trimmed
          .split(RegExp(r'[/,;|\s]+'))
          .map((t) => t.trim())
          .where((t) => t.isNotEmpty)
          .toList();
      if (tokens.length > 1) {
        return tokens;
      }
    }
    return const [];
  }

  /// Returns a human-readable version of [raw] by splitting it into segments
  /// whose lengths match the answer_key values in [content].
  /// e.g. "4341131" with answer_key values ["434","1131"] → "434 / 1131"
  /// Falls back to [raw] unchanged if the lengths don't match or there is only
  /// one segment.
  static String _formatAnswerDraft(String raw, ProblemContent content) {
    if (raw.isEmpty) return raw;
    if (raw.contains('/') || raw.contains(',')) return raw;

    final answerMap = content.answerMap;
    final key = answerMap['answer_key'];
    if (key is! List || key.length < 2) return raw;

    // Collect per-blank string lengths from the answer_key values.
    final segments = <String>[];
    for (final entry in key) {
      final v = entry is Map ? (entry['value'] ?? entry['expected']) : entry;
      if (v == null) return raw;
      segments.add(v.toString().trim());
    }

    // All segments equal → single repeated answer (e.g. carry digits); display as-is.
    if (segments.toSet().length == 1) return raw;

    // Try to reconstruct the raw string from segment lengths.
    int cursor = 0;
    final parts = <String>[];
    for (final seg in segments) {
      final len = seg.length;
      if (cursor + len > raw.length) return raw; // mismatch – fall back
      parts.add(raw.substring(cursor, cursor + len));
      cursor += len;
    }
    if (cursor != raw.length) return raw; // leftover chars – fall back

    return parts.join(' / ');
  }

  static String _choiceExplanation(
    String choice,
    ProblemContent content,
    AppStrings strings,
  ) {
    final match = RegExp(r'(\d+)\s*[×x*]\s*(\d+)').firstMatch(choice);
    if (match != null) {
      final a = int.tryParse(match.group(1)!);
      final b = int.tryParse(match.group(2)!);
      if (a != null && b != null) {
        if (a < 10 && b < 10) {
          return strings.t('answer.onesPlaceProduct', {'val': a * b});
        } else if (a >= 10 && a < 100 && a % 10 != 0) {
          return strings.t('answer.totalTwoDigitProduct');
        } else if (a >= 100) {
          return strings.t('answer.hundredsPlaceProduct', {'val': a * b});
        } else if (a >= 10 && a % 10 == 0) {
          return strings.t('answer.tensPlaceProduct', {'val': a * b});
        }
      }
    }
    return '';
  }

  void _syncSelectedChoice() {
    final choices = widget.content.choices;
    if (choices.isNotEmpty && widget.answerDraft.isNotEmpty) {
      final draft = widget.answerDraft.trim();
      var idx = choices.indexOf(draft);
      if (idx < 0) {
        for (var i = 0; i < choices.length; i++) {
          if (isSameAnswer(choices[i], draft)) {
            idx = i;
            break;
          }
        }
      }
      if (idx >= 0 && selectedChoiceIndex != idx) {
        selectedChoiceIndex = idx;
      }
    } else if (widget.answerDraft.isEmpty && selectedChoiceIndex != null) {
      selectedChoiceIndex = null;
    }
  }

  void _syncSelectedGroupChoices() {
    final groups = widget.content.choiceGroups;
    if (groups.isEmpty) {
      if (selectedGroupChoices.isNotEmpty) {
        selectedGroupChoices.clear();
      }
      return;
    }
    if (widget.answerDraft.isEmpty) {
      if (selectedGroupChoices.isNotEmpty) {
        selectedGroupChoices.clear();
      }
      return;
    }
    final parts = widget.answerDraft
        .split(RegExp(r'[,/]+'))
        .map((s) => s.trim())
        .where((s) => s.isNotEmpty)
        .toList();
    if (parts.length == groups.length) {
      for (var i = 0; i < groups.length; i++) {
        final choiceList = groups[i].choices;
        final part = parts[i];
        final idx = choiceList.indexWhere((c) => isSameAnswer(c, part));
        if (idx >= 0) {
          selectedGroupChoices[i] = idx;
        }
      }
    }
  }

  @override
  void initState() {
    super.initState();
    controller.text = _formatAnswerDraft(widget.answerDraft, widget.content);
    _syncSelectedChoice();
    _syncSelectedGroupChoices();
    _syncMultiControllers();
  }

  @override
  void didUpdateWidget(covariant AnswerPanel oldWidget) {
    super.didUpdateWidget(oldWidget);
    _syncSelectedChoice();
    _syncSelectedGroupChoices();
    _syncMultiControllers();
    final formatted = _formatAnswerDraft(widget.answerDraft, widget.content);
    if (formatted == controller.text) {
      return;
    }
    controller.text = formatted;
    controller.selection = TextSelection.collapsed(
      offset: controller.text.length,
    );
  }

  @override
  void dispose() {
    controller.dispose();
    for (final c in multiControllers) {
      c.dispose();
    }
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final choiceGroups = widget.content.choiceGroups;
    final choices = widget.content.choices;
    final strings = AppStrings.of(context);
    final allowsMultipleChoices = _allowsMultipleChoices(widget.content);
    final hasVisual =
        widget.content.renderer.isNotEmpty || widget.content.svg.isNotEmpty;
    final hasRendererAnswerInputs = widget.content.hasRendererAnswerInputs;
    final oxChoices =
        choices.isNotEmpty && !allowsMultipleChoices && choiceGroups.isEmpty
            ? _detectOxChoices(choices, strings)
            : null;
    final isOxChoiceGroup = choiceGroups.isNotEmpty &&
        choiceGroups.every(
          (g) =>
              g.choices.isNotEmpty &&
              g.choices.every(
                (c) => _isPositiveChoice(c) || _isNegativeChoice(c),
              ),
        );

    final String titleText;
    if (!hasVisual) {
      titleText = widget.content.prompt;
    } else if (oxChoices != null) {
      titleText = strings.t('answer.promptOx');
    } else if (choiceGroups.isNotEmpty) {
      titleText = strings.t('answer.promptChoiceGroups');
    } else if (choices.isNotEmpty) {
      titleText = allowsMultipleChoices
          ? strings.t('answer.promptMultipleChoices')
          : strings.t('answer.promptSingleChoice');
    } else if (hasRendererAnswerInputs) {
      titleText = strings.t('answer.promptBlanks');
    } else if (widget.content.multiAnswerFields.isNotEmpty) {
      titleText = strings.t('answer.promptMultiAnswer');
    } else {
      titleText = strings.t('answer.promptDefault');
    }

    final targetUnit = _targetUnit(widget.content);

    return Card(
      margin: EdgeInsets.zero,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(AppRadii.large),
        side: const BorderSide(color: KidsPalette.line),
      ),
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Row(
              children: [
                Container(
                  width: 26,
                  height: 26,
                  decoration: const BoxDecoration(
                    color: Color(0xFF4F46E5),
                    shape: BoxShape.circle,
                  ),
                  alignment: Alignment.center,
                  child: const Text(
                    'Q',
                    style: TextStyle(
                      color: Colors.white,
                      fontWeight: FontWeight.w900,
                      fontSize: 14,
                    ),
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: Text(
                    titleText,
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(
                          fontWeight: FontWeight.w800,
                          color: const Color(0xFF0F172A),
                        ),
                  ),
                ),
                if (choices.isNotEmpty)
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 10,
                      vertical: 4,
                    ),
                    decoration: BoxDecoration(
                      color: const Color(0xFFEEF2FF),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Text(
                      oxChoices != null || isOxChoiceGroup
                          ? strings.t('answer.oxTag')
                          : (allowsMultipleChoices
                              ? strings.t('answer.multipleChoiceTag')
                              : strings.t('answer.singleChoiceTag')),
                      style: const TextStyle(
                        color: Color(0xFF4F46E5),
                        fontSize: 11,
                        fontWeight: FontWeight.w800,
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
                    final isPos = _isPositiveChoice(choiceText);
                    final isNeg = _isNegativeChoice(choiceText);
                    final String displayLabel;
                    if (isPos) {
                      displayLabel = '○  ${strings.t('answer.oxTrue')}';
                    } else if (isNeg) {
                      displayLabel = '✕  ${strings.t('answer.oxFalse')}';
                    } else {
                      displayLabel = choiceText;
                    }
                    Color? selectedBgColor;
                    if (selected) {
                      if (isPos) {
                        selectedBgColor = const Color(0xFFEFF6FF);
                      } else if (isNeg) {
                        selectedBgColor = const Color(0xFFFEF2F2);
                      }
                    }
                    final borderColor = selected
                        ? (isPos
                            ? const Color(0xFF3B82F6)
                            : (isNeg
                                ? const Color(0xFFEF4444)
                                : KidsPalette.primary))
                        : KidsPalette.line;
                    return ChoiceChip(
                      selected: selected,
                      selectedColor: selectedBgColor,
                      labelPadding: const EdgeInsets.symmetric(
                        horizontal: 14,
                        vertical: 10,
                      ),
                      padding: const EdgeInsets.symmetric(
                        horizontal: 6,
                        vertical: 4,
                      ),
                      materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(AppRadii.medium),
                        side: BorderSide(
                          color: borderColor,
                          width: selected ? 2 : 1.5,
                        ),
                      ),
                      label: Text(
                        displayLabel,
                        style: TextStyle(
                          fontSize: 18,
                          height: 1.3,
                          fontWeight:
                              selected ? FontWeight.bold : FontWeight.w500,
                          color: selected
                              ? (isPos
                                  ? const Color(0xFF1D4ED8)
                                  : (isNeg
                                      ? const Color(0xFFB91C1C)
                                      : KidsPalette.primary))
                              : const Color(0xFF374151),
                          leadingDistribution: TextLeadingDistribution.even,
                        ),
                      ),
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
            ] else if (choices.isEmpty) ...[
              if (widget.content.hasMultipleRendererAnswerInputs)
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 14,
                    vertical: 12,
                  ),
                  decoration: BoxDecoration(
                    color: const Color(0xFFF5F7FF),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: const Color(0xFFD9DFFF)),
                  ),
                  child: Row(
                    children: [
                      const Icon(
                        Icons.touch_app_outlined,
                        color: Color(0xFF5C6AC4),
                        size: 21,
                      ),
                      const SizedBox(width: 10),
                      Expanded(
                        child: Text(
                          strings.t('answer.checkAllBlanks'),
                          style: const TextStyle(
                            color: Color(0xFF4B5563),
                            fontSize: 15,
                            height: 1.4,
                          ),
                        ),
                      ),
                    ],
                  ),
                )
              else if (widget.content.multiAnswerFields.isNotEmpty) ...[
                for (final (i, field)
                    in widget.content.multiAnswerFields.indexed) ...[
                  TextField(
                    key: ValueKey('multi-input-field-$i'),
                    controller: multiControllers[i],
                    style: const TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.w600,
                    ),
                    decoration: InputDecoration(
                      labelText: field.unit.isNotEmpty
                          ? '${field.label} (${field.unit})'
                          : field.label,
                      suffixText: field.unit.isNotEmpty ? field.unit : null,
                      suffixStyle: const TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                        color: Color(0xFF4B5563),
                      ),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                      contentPadding: const EdgeInsets.symmetric(
                        horizontal: 14,
                        vertical: 12,
                      ),
                    ),
                    onChanged: (text) {
                      final combined = multiControllers
                          .map((c) => c.text.trim())
                          .join(' / ');
                      widget.onAnswerChanged(combined);
                    },
                  ),
                  if (i < widget.content.multiAnswerFields.length - 1)
                    const SizedBox(height: 12),
                ],
              ] else ...[
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
                    suffixIcon: IconButton(
                      icon: Icon(
                        _showKeypad
                            ? Icons.keyboard_hide_rounded
                            : Icons.dialpad_rounded,
                        color: const Color(0xFF5C6AC4),
                      ),
                      tooltip: strings.t('answer.keypadTooltip'),
                      onPressed: () =>
                          setState(() => _showKeypad = !_showKeypad),
                    ),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  onChanged: widget.onAnswerChanged,
                  onSubmitted: widget.onSubmit,
                ),
                if (_showKeypad) ...[
                  const SizedBox(height: 12),
                  MathKeypad(
                    mode: MathKeypadMode.digits,
                    showNextButton: false,
                    onKeyPressed: (digit) {
                      final current = controller.text;
                      final next = '$current$digit';
                      controller.text = next;
                      controller.selection =
                          TextSelection.collapsed(offset: next.length);
                      widget.onAnswerChanged(next);
                    },
                    onBackspace: () {
                      final current = controller.text;
                      if (current.isNotEmpty) {
                        final next = current.substring(0, current.length - 1);
                        controller.text = next;
                        controller.selection =
                            TextSelection.collapsed(offset: next.length);
                        widget.onAnswerChanged(next);
                      }
                    },
                    onClear: () {
                      controller.clear();
                      widget.onAnswerChanged('');
                    },
                    onSubmit: () {
                      if (controller.text.trim().isNotEmpty) {
                        widget.onSubmit(controller.text.trim());
                      }
                    },
                  ),
                ],
              ],
            ] else if (oxChoices != null)
              _buildOxChoices(context, oxChoices, strings)
            else
              Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: choices.indexed.map((entry) {
                  final choiceIndex = entry.$1;
                  final choice = entry.$2;
                  final selected = allowsMultipleChoices
                      ? selectedChoiceIndexes.contains(choiceIndex)
                      : selectedChoiceIndex == choiceIndex;
                  final explanation = widget.isCorrect != null
                      ? _choiceExplanation(choice, widget.content, strings)
                      : '';

                  return Padding(
                    padding: const EdgeInsets.only(bottom: 10),
                    child: ChoiceChip(
                      selected: selected,
                      showCheckmark: false,
                      avatar: Container(
                        width: 22,
                        height: 22,
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          border: Border.all(
                            color: selected
                                ? const Color(0xFF4F46E5)
                                : const Color(0xFFCBD5E1),
                            width: 2.0,
                          ),
                        ),
                        child: selected
                            ? Center(
                                child: Container(
                                  width: 10,
                                  height: 10,
                                  decoration: const BoxDecoration(
                                    shape: BoxShape.circle,
                                    color: Color(0xFF4F46E5),
                                  ),
                                ),
                              )
                            : null,
                      ),
                      label: SizedBox(
                        width: double.infinity,
                        child: Row(
                          children: [
                            Expanded(
                              child: Text(
                                choice,
                                style: TextStyle(
                                  fontSize: 16,
                                  fontWeight: selected
                                      ? FontWeight.w800
                                      : FontWeight.w600,
                                  color: selected
                                      ? const Color(0xFF4F46E5)
                                      : const Color(0xFF0F172A),
                                ),
                              ),
                            ),
                            if (selected) ...[
                              const SizedBox(width: 8),
                              Container(
                                padding: const EdgeInsets.symmetric(
                                  horizontal: 10,
                                  vertical: 4,
                                ),
                                decoration: BoxDecoration(
                                  color: const Color(0xFF4F46E5),
                                  borderRadius: BorderRadius.circular(8),
                                ),
                                child: Text(
                                  strings.t('answer.candidateSelected'),
                                  style: const TextStyle(
                                    color: Colors.white,
                                    fontSize: 12,
                                    fontWeight: FontWeight.w700,
                                  ),
                                ),
                              ),
                            ] else if (explanation.isNotEmpty) ...[
                              const SizedBox(width: 8),
                              Flexible(
                                child: Text(
                                  explanation,
                                  overflow: TextOverflow.ellipsis,
                                  style: const TextStyle(
                                    fontSize: 12,
                                    color: Color(0xFF94A3B8),
                                    fontWeight: FontWeight.w500,
                                  ),
                                ),
                              ),
                            ],
                          ],
                        ),
                      ),
                      backgroundColor: Colors.white,
                      selectedColor: const Color(0xFFEEF2FF),
                      padding: const EdgeInsets.symmetric(
                        horizontal: 12,
                        vertical: 12,
                      ),
                      materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(14),
                        side: BorderSide(
                          color: selected
                              ? const Color(0xFF4F46E5)
                              : const Color(0xFFE2E8F0),
                          width: selected ? 2.0 : 1.0,
                        ),
                      ),
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
                    ),
                  );
                }).toList(),
              ),
            const SizedBox(height: 16),
            FilledButton(
              style: FilledButton.styleFrom(
                backgroundColor: const Color(0xFF4F46E5),
                minimumSize: const Size.fromHeight(52),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16),
                ),
                elevation: 2,
              ),
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
                  if (widget.content.hasMultipleRendererAnswerInputs) {
                    answer = widget.answerDraft;
                  } else if (widget.content.multiAnswerFields.isNotEmpty) {
                    answer =
                        multiControllers.map((c) => c.text.trim()).join(' / ');
                  } else {
                    answer = controller.text;
                  }
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
              child: FittedBox(
                fit: BoxFit.scaleDown,
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(
                      strings.t('answer.check'),
                      style: const TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.w800,
                        color: Colors.white,
                      ),
                    ),
                    if (strings.t('answer.andEarnStar').isNotEmpty) ...[
                      const SizedBox(width: 4),
                      Text(
                        strings.t('answer.andEarnStar'),
                        style: const TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.w800,
                          color: Colors.white,
                        ),
                      ),
                    ],
                  ],
                ),
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

  Widget _buildOxChoices(
    BuildContext context,
    OxChoicePair pair,
    AppStrings strings,
  ) {
    final isOSelected = selectedChoiceIndex == pair.oChoice.originalIndex;
    final isXSelected = selectedChoiceIndex == pair.xChoice.originalIndex;

    return Row(
      children: [
        Expanded(
          child: _OxCard(
            item: pair.oChoice,
            isSelected: isOSelected,
            onTap: () {
              setState(() {
                selectedChoiceIndex = pair.oChoice.originalIndex;
                selectedChoiceIndexes = {};
              });
              widget.onAnswerChanged(pair.oChoice.rawValue);
            },
          ),
        ),
        const SizedBox(width: 14),
        Expanded(
          child: _OxCard(
            item: pair.xChoice,
            isSelected: isXSelected,
            onTap: () {
              setState(() {
                selectedChoiceIndex = pair.xChoice.originalIndex;
                selectedChoiceIndexes = {};
              });
              widget.onAnswerChanged(pair.xChoice.rawValue);
            },
          ),
        ),
      ],
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
      (targetType.contains('multiple') || targetType.contains('multi'))) {
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
      .join(' / ');
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

enum OxChoiceType { o, x }

class OxChoiceItem {
  const OxChoiceItem({
    required this.originalIndex,
    required this.rawValue,
    required this.type,
    required this.displaySymbol,
    required this.subLabel,
  });

  final int originalIndex;
  final String rawValue;
  final OxChoiceType type;
  final String displaySymbol;
  final String subLabel;
}

class OxChoicePair {
  const OxChoicePair({
    required this.oChoice,
    required this.xChoice,
  });

  final OxChoiceItem oChoice;
  final OxChoiceItem xChoice;
}

bool _isPositiveChoice(String text) {
  final cleaned = text
      .trim()
      .toLowerCase()
      .replaceAll(RegExp(r'[\s\(\)\[\]\.\,]'), '');
  const positiveTokens = {
    '○', 'o', '0', '⭕', 'o표', '○표', '참', '맞음', '맞다', '맞아요', '바름', '바르다',
    '옳음', '옳다', '예', '네', 'true', 't', 'yes', 'y', 'correct', 'tak', 'так',
    'правильно', '正しい', 'マル', 'まる', '对', '正確', '正确', '是'
  };
  return positiveTokens.contains(cleaned);
}

bool _isNegativeChoice(String text) {
  final cleaned = text
      .trim()
      .toLowerCase()
      .replaceAll(RegExp(r'[\s\(\)\[\]\.\,]'), '');
  const negativeTokens = {
    'x', '✕', '×', '❌', 'x표', '×표', '✕표', '거짓', '틀림', '틀리다', '틀려요',
    '그름', '그르다', '아니오', '아니요', 'false', 'f', 'no', 'n', 'incorrect',
    'wrong', 'ні', 'ni', 'неправильно', '違う', 'バツ', 'ばつ', '错', '錯誤',
    '错误', '否'
  };
  return negativeTokens.contains(cleaned);
}

String _resolveSubLabel(String raw, bool isPositive, AppStrings strings) {
  final cleaned = raw.trim().replaceAll(RegExp(r'[\(\)\[\]\.\,]'), '').trim();
  final isSymbolOnly = RegExp(
    r'^(?:○|o|0|⭕|x|✕|×|❌|o표|○표|x표|×표|✕표)$',
    caseSensitive: false,
  ).hasMatch(cleaned);
  if (isSymbolOnly) {
    return isPositive
        ? strings.t('answer.oxTrue')
        : strings.t('answer.oxFalse');
  }
  return cleaned;
}

OxChoicePair? _detectOxChoices(List<String> choices, AppStrings strings) {
  if (choices.length != 2) {
    return null;
  }
  final c0 = choices[0];
  final c1 = choices[1];

  final is0Pos = _isPositiveChoice(c0);
  final is0Neg = _isNegativeChoice(c0);
  final is1Pos = _isPositiveChoice(c1);
  final is1Neg = _isNegativeChoice(c1);

  if (is0Pos && is1Neg) {
    return OxChoicePair(
      oChoice: OxChoiceItem(
        originalIndex: 0,
        rawValue: c0,
        type: OxChoiceType.o,
        displaySymbol: '○',
        subLabel: _resolveSubLabel(c0, true, strings),
      ),
      xChoice: OxChoiceItem(
        originalIndex: 1,
        rawValue: c1,
        type: OxChoiceType.x,
        displaySymbol: '✕',
        subLabel: _resolveSubLabel(c1, false, strings),
      ),
    );
  } else if (is1Pos && is0Neg) {
    return OxChoicePair(
      oChoice: OxChoiceItem(
        originalIndex: 1,
        rawValue: c1,
        type: OxChoiceType.o,
        displaySymbol: '○',
        subLabel: _resolveSubLabel(c1, true, strings),
      ),
      xChoice: OxChoiceItem(
        originalIndex: 0,
        rawValue: c0,
        type: OxChoiceType.x,
        displaySymbol: '✕',
        subLabel: _resolveSubLabel(c0, false, strings),
      ),
    );
  }

  return null;
}

class _OxCard extends StatelessWidget {
  const _OxCard({
    required this.item,
    required this.isSelected,
    required this.onTap,
  });

  final OxChoiceItem item;
  final bool isSelected;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final isO = item.type == OxChoiceType.o;
    final primaryColor =
        isO ? const Color(0xFF2563EB) : const Color(0xFFDC2626);
    final selectedBorderColor =
        isO ? const Color(0xFF3B82F6) : const Color(0xFFEF4444);
    final selectedBgColor =
        isO ? const Color(0xFFEFF6FF) : const Color(0xFFFEF2F2);
    final textColor = isSelected
        ? (isO ? const Color(0xFF1D4ED8) : const Color(0xFFB91C1C))
        : const Color(0xFF64748B);

    return Material(
      color: Colors.transparent,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(18),
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 180),
          curve: Curves.easeInOut,
          constraints: const BoxConstraints(minHeight: 110),
          decoration: BoxDecoration(
            color: isSelected ? selectedBgColor : Colors.white,
            borderRadius: BorderRadius.circular(18),
            border: Border.all(
              color: isSelected
                  ? selectedBorderColor
                  : const Color(0xFFE2E8F0),
              width: isSelected ? 2.5 : 1.5,
            ),
            boxShadow: isSelected
                ? [
                    BoxShadow(
                      color: selectedBorderColor.withValues(alpha: 0.18),
                      blurRadius: 10,
                      offset: const Offset(0, 4),
                    ),
                  ]
                : [
                    BoxShadow(
                      color: Colors.black.withValues(alpha: 0.02),
                      blurRadius: 4,
                      offset: const Offset(0, 1),
                    ),
                  ],
          ),
          child: Stack(
            children: [
              Positioned(
                top: 10,
                right: 10,
                child: Container(
                  width: 22,
                  height: 22,
                  decoration: BoxDecoration(
                    color: isSelected ? primaryColor : Colors.transparent,
                    shape: BoxShape.circle,
                    border: isSelected
                        ? null
                        : Border.all(
                            color: const Color(0xFFCBD5E1),
                            width: 1.5,
                          ),
                  ),
                  alignment: Alignment.center,
                  child: isSelected
                      ? const Icon(
                          Icons.check,
                          size: 14,
                          color: Colors.white,
                        )
                      : null,
                ),
              ),
              Padding(
                padding: const EdgeInsets.symmetric(
                  vertical: 18,
                  horizontal: 12,
                ),
                child: Center(
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(
                        item.displaySymbol,
                        style: TextStyle(
                          fontSize: 48,
                          height: 1.0,
                          fontWeight: FontWeight.w900,
                          color: textColor,
                        ),
                      ),
                      if (item.subLabel.isNotEmpty) ...[
                        const SizedBox(height: 6),
                        Text(
                          item.subLabel,
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: isSelected
                                ? FontWeight.w800
                                : FontWeight.w600,
                            color: isSelected
                                ? textColor
                                : const Color(0xFF475569),
                          ),
                        ),
                      ],
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

