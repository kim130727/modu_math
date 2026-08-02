import 'package:flutter/material.dart';

import '../l10n/app_strings.dart';
import '../models/content_models.dart';

class SolutionSteps extends StatelessWidget {
  const SolutionSteps({super.key, required this.steps});

  final List<SolutionStep> steps;

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    return Padding(
      padding: const EdgeInsets.only(top: 14),
      child: Card(
        margin: EdgeInsets.zero,
        child: Padding(
          padding: const EdgeInsets.all(18),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(strings.t('solution.title'),
                  style: Theme.of(context).textTheme.titleMedium),
              const SizedBox(height: 12),
              if (steps.isEmpty)
                Text(strings.t('solution.empty'),
                    style: const TextStyle(fontSize: 17))
              else
                ...steps.indexed.map((entry) {
                  final index = entry.$1 + 1;
                  final step = entry.$2;
                  return Padding(
                    padding: const EdgeInsets.only(bottom: 12),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        CircleAvatar(
                          radius: 15,
                          child: Text('$index'),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Text(
                            step.value.isEmpty
                                ? step.explanation
                                : '${step.explanation}\n${step.value}',
                            style: const TextStyle(fontSize: 17, height: 1.35),
                          ),
                        ),
                      ],
                    ),
                  );
                }),
            ],
          ),
        ),
      ),
    );
  }
}
