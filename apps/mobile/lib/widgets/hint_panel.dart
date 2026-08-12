import 'package:flutter/material.dart';

import '../services/solvable_hint_service.dart';

class HintPanel extends StatelessWidget {
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
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;
    final visibleHints = hints.where((hint) => hint.level <= visibleLevel);
    final canRevealMore = visibleLevel < hints.length;

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
            FilledButton.icon(
              onPressed: canRevealMore ? onRevealNext : null,
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
                            hint.title,
                            style: const TextStyle(
                              fontWeight: FontWeight.w800,
                            ),
                          ),
                          const SizedBox(height: 6),
                          Text(hint.body),
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
}
