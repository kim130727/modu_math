import 'package:flutter/material.dart';

import '../l10n/app_strings.dart';
import '../models/learning_progress.dart';

class ProgressPanel extends StatelessWidget {
  const ProgressPanel({super.key, required this.summary});

  final LearningProgressSummary summary;

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;
    final percent = (summary.accuracy * 100).round();
    final strings = AppStrings.of(context);

    return Card(
      margin: EdgeInsets.zero,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(strings.t('progress.title'),
                style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 12),
            Row(
              children: [
                Expanded(
                  child: _Metric(
                      label: strings.t('progress.solved'),
                      value: '${summary.solvedCount}'),
                ),
                Expanded(
                  child: _Metric(
                    label: strings.t('progress.correct'),
                    value: '${summary.correctCount}',
                  ),
                ),
                Expanded(
                    child: _Metric(
                        label: strings.t('home.accuracy'), value: '$percent%')),
              ],
            ),
            if (summary.wrongResults.isNotEmpty) ...[
              const SizedBox(height: 14),
              Text(
                strings.t('progress.reviewAgain'),
                style: Theme.of(context).textTheme.titleSmall?.copyWith(
                      fontSize: 16,
                      fontWeight: FontWeight.w800,
                    ),
              ),
              const SizedBox(height: 6),
              ...summary.wrongResults.map(
                (result) => Text(
                  result.problem.title,
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: TextStyle(color: colorScheme.onSurfaceVariant),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}

class _Metric extends StatelessWidget {
  const _Metric({required this.label, required this.value});

  final String label;
  final String value;

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          label,
          style: TextStyle(fontSize: 13, color: colorScheme.onSurfaceVariant),
        ),
        const SizedBox(height: 3),
        Text(
          value,
          style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w900),
        ),
      ],
    );
  }
}
