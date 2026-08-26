import 'package:flutter/material.dart';

import '../services/solvable_hint_service.dart';

class HintPanel extends StatefulWidget {
  const HintPanel({
    super.key,
    required this.hints,
    required this.visibleLevel,
    required this.onRevealNext,
  });

  final List<SolvableHint> hints;
  final int visibleLevel;
  final VoidCallback onRevealNext;

  @override
  State<HintPanel> createState() => _HintPanelState();
}

class _HintPanelState extends State<HintPanel> {
  final Map<String, TextEditingController> _controllers = {};
  final Map<String, bool> _results = {};
  final Map<String, String> _selectedChoices = {};
  final Map<String, int> _visibleLevelsByGroup = {};
  String? _selectedGroupKey;

  @override
  void didUpdateWidget(covariant HintPanel oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.hints == widget.hints) {
      return;
    }
    _results.clear();
    _selectedChoices.clear();
    final keys = widget.hints.map(_hintKey).toSet();
    for (final entry in _controllers.entries.toList()) {
      if (!keys.contains(entry.key)) {
        entry.value.dispose();
        _controllers.remove(entry.key);
      }
    }
    final groupKeys =
        _hintGroups(widget.hints).map((group) => group.key).toSet();
    _visibleLevelsByGroup.removeWhere((key, _) => !groupKeys.contains(key));
    if (_selectedGroupKey != null && !groupKeys.contains(_selectedGroupKey)) {
      _selectedGroupKey = null;
    }
  }

  @override
  void dispose() {
    for (final controller in _controllers.values) {
      controller.dispose();
    }
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;
    final groups = _hintGroups(widget.hints);
    final hasSubproblemTabs = groups.length > 1;
    final activeGroup = groups.isEmpty
        ? null
        : groups.firstWhere(
            (group) => group.key == _selectedGroupKey,
            orElse: () => groups.first,
          );
    final activeVisibleLevel = activeGroup == null
        ? 0
        : hasSubproblemTabs
            ? _visibleLevelsByGroup[activeGroup.key] ?? 0
            : widget.visibleLevel;
    final visibleHints = activeGroup?.hints
            .where((hint) => hint.level <= activeVisibleLevel)
            .toList() ??
        const <SolvableHint>[];
    final canRevealMore =
        activeGroup != null && activeVisibleLevel < activeGroup.maxLevel;

    return Card(
      margin: EdgeInsets.zero,
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Row(
              children: [
                Icon(Icons.lightbulb_outline, color: colorScheme.primary),
                const SizedBox(width: 8),
                Text(
                  '단계별 힌트',
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                        fontWeight: FontWeight.w800,
                      ),
                ),
              ],
            ),
            const SizedBox(height: 14),
            if (hasSubproblemTabs && activeGroup != null) ...[
              _SubproblemTabs(
                groups: groups,
                selectedKey: activeGroup.key,
                onSelect: (key) => setState(() => _selectedGroupKey = key),
              ),
              const SizedBox(height: 12),
            ],
            FilledButton.icon(
              onPressed: canRevealMore && activeGroup != null
                  ? () => _revealNext(activeGroup)
                  : null,
              icon: const Icon(Icons.visibility_outlined),
              label: Text(canRevealMore ? '힌트 보기' : '모든 힌트를 봤어요'),
            ),
            if (visibleHints.isEmpty) ...[
              const SizedBox(height: 12),
              Text(
                '막히면 힌트를 한 단계씩 열어 보세요.',
                style: TextStyle(color: colorScheme.onSurfaceVariant),
              ),
            ] else ...[
              const SizedBox(height: 14),
              ...visibleHints.map((hint) {
                final hintKey = _hintKey(hint);
                final title = hasSubproblemTabs
                    ? _titleWithoutGroup(hint.title)
                    : hint.title;
                return Padding(
                  padding: const EdgeInsets.only(bottom: 12),
                  child: DecoratedBox(
                    decoration: BoxDecoration(
                      color: colorScheme.surfaceContainerHighest,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Padding(
                      padding: const EdgeInsets.all(14),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            title,
                            style: const TextStyle(
                              fontWeight: FontWeight.w800,
                            ),
                          ),
                          if (hint.body.trim().isNotEmpty &&
                              hint.body.trim() != hint.miniQuestion.trim()) ...[
                            const SizedBox(height: 6),
                            Text(hint.body),
                          ],
                          if (hint.miniQuestion.trim().isNotEmpty &&
                              (hint.choices.isNotEmpty ||
                                  hint.acceptedAnswers.isNotEmpty)) ...[
                            const SizedBox(height: 12),
                            _MiniHintProblem(
                              hint: hint,
                              controller: _controllerFor(hintKey),
                              result: _results[hintKey],
                              selectedChoice: _selectedChoices[hintKey],
                              onSelectChoice: (choice) =>
                                  _checkChoice(hintKey, choice),
                              onCheck: () => _checkMiniProblem(hintKey, hint),
                            ),
                          ],
                        ],
                      ),
                    ),
                  ),
                );
              }),
            ],
          ],
        ),
      ),
    );
  }

  TextEditingController _controllerFor(String key) {
    return _controllers.putIfAbsent(key, TextEditingController.new);
  }

  void _checkMiniProblem(String key, SolvableHint hint) {
    final answer = _normalizeMiniAnswer(_controllerFor(key).text);
    final correct = hint.acceptedAnswers
        .map(_normalizeMiniAnswer)
        .any((expected) => expected == answer);
    setState(() => _results[key] = correct);
  }

  void _checkChoice(String key, HintChoice choice) {
    setState(() {
      _selectedChoices[key] = choice.label;
      _results[key] = choice.isCorrect;
    });
  }

  String _hintKey(SolvableHint hint) {
    return '${hint.level}|${hint.title}|${hint.miniQuestion}';
  }

  void _revealNext(_HintGroup group) {
    setState(() {
      _visibleLevelsByGroup[group.key] =
          (_visibleLevelsByGroup[group.key] ?? 0) + 1;
    });
    widget.onRevealNext();
  }
}

class _HintGroup {
  const _HintGroup({
    required this.key,
    required this.label,
    required this.hints,
  });

  final String key;
  final String label;
  final List<SolvableHint> hints;

  int get maxLevel {
    if (hints.isEmpty) {
      return 0;
    }
    return hints.map((hint) => hint.level).reduce((a, b) => a > b ? a : b);
  }
}

class _SubproblemTabs extends StatelessWidget {
  const _SubproblemTabs({
    required this.groups,
    required this.selectedKey,
    required this.onSelect,
  });

  final List<_HintGroup> groups;
  final String selectedKey;
  final ValueChanged<String> onSelect;

  @override
  Widget build(BuildContext context) {
    return SegmentedButton<String>(
      segments: [
        for (final group in groups)
          ButtonSegment<String>(
            value: group.key,
            label: Text(group.label),
          ),
      ],
      selected: {selectedKey},
      onSelectionChanged: (selection) => onSelect(selection.first),
      showSelectedIcon: false,
    );
  }
}

List<_HintGroup> _hintGroups(List<SolvableHint> hints) {
  final grouped = <String, List<SolvableHint>>{};
  for (final hint in hints) {
    final key = hint.groupKey ?? _groupKeyForTitle(hint.title);
    grouped.putIfAbsent(key, () => []).add(hint);
  }
  return grouped.entries
      .map(
        (entry) => _HintGroup(
          key: entry.key,
          label: entry.key == 'all' ? '전체' : '(${entry.key})',
          hints: entry.value,
        ),
      )
      .toList();
}

String _groupKeyForTitle(String title) {
  final afterStep = RegExp(r'^\s*\d+[^:]*:\s*\((\d+)\)').firstMatch(title);
  if (afterStep != null) {
    return afterStep.group(1)!;
  }
  final atStart = RegExp(r'^\s*\((\d+)\)').firstMatch(title);
  if (atStart != null) {
    return atStart.group(1)!;
  }
  return 'all';
}

String _titleWithoutGroup(String title) {
  final withoutStepGroup = title.replaceFirst(
    RegExp(r'^(\s*\d+[^:]*:\s*)\(\d+\)\s*'),
    r'$1',
  );
  if (withoutStepGroup != title) {
    return withoutStepGroup;
  }
  return title.replaceFirst(RegExp(r'^\s*\(\d+\)\s*'), '');
}

class _MiniHintProblem extends StatelessWidget {
  const _MiniHintProblem({
    required this.hint,
    required this.controller,
    required this.result,
    required this.selectedChoice,
    required this.onSelectChoice,
    required this.onCheck,
  });

  final SolvableHint hint;
  final TextEditingController controller;
  final bool? result;
  final String? selectedChoice;
  final ValueChanged<HintChoice> onSelectChoice;
  final VoidCallback onCheck;

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;
    return DecoratedBox(
      decoration: BoxDecoration(
        color: colorScheme.surface,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: colorScheme.outlineVariant),
      ),
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(
              hint.miniQuestion,
              style: const TextStyle(fontWeight: FontWeight.w700),
            ),
            const SizedBox(height: 8),
            if (hint.choices.isNotEmpty)
              Wrap(
                spacing: 8,
                runSpacing: 8,
                children: hint.choices.map((choice) {
                  return ChoiceChip(
                    label: Text(choice.label),
                    selected: selectedChoice == choice.label,
                    onSelected: (_) => onSelectChoice(choice),
                  );
                }).toList(),
              )
            else
              Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: controller,
                      decoration: const InputDecoration(
                        isDense: true,
                        border: OutlineInputBorder(),
                        labelText: '작은 답',
                      ),
                      onSubmitted: (_) => onCheck(),
                    ),
                  ),
                  const SizedBox(width: 8),
                  OutlinedButton(
                    onPressed: onCheck,
                    child: const Text('확인'),
                  ),
                ],
              ),
            if (result != null) ...[
              const SizedBox(height: 8),
              Text(
                result!
                    ? hint.successMessage
                    : '조금 달라요. 질문을 다시 보고 한 번 더 골라 보세요.',
                style: TextStyle(
                  color: result! ? const Color(0xFF166534) : colorScheme.error,
                  fontWeight: FontWeight.w700,
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}

String _normalizeMiniAnswer(String value) {
  return value
      .trim()
      .toLowerCase()
      .replaceAll(' ', '')
      .replaceAll('→', '+')
      .replaceAll('=', '')
      .replaceAll('입니다', '')
      .replaceAll('이에요', '')
      .replaceAll('예요', '');
}
