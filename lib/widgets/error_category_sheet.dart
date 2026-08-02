import 'package:flutter/material.dart';

import '../l10n/app_strings.dart';
import '../models/learning_progress.dart';
import '../theme/app_theme.dart';

class ErrorCategorySheet extends StatelessWidget {
  const ErrorCategorySheet({
    super.key,
    required this.onCategorySelected,
  });

  final ValueChanged<ErrorCategory> onCategorySelected;

  static const _categoryOptions = [
    _CategoryOption(
      category: ErrorCategory.understandingTarget,
      color: Color(0xFFEFF6FF),
    ),
    _CategoryOption(
      category: ErrorCategory.understandingGiven,
      color: Color(0xFFF0FDF4),
    ),
    _CategoryOption(
      category: ErrorCategory.planningConcept,
      color: Color(0xFFFEF3C7),
    ),
    _CategoryOption(
      category: ErrorCategory.planningOperation,
      color: Color(0xFFFEE2E2),
    ),
    _CategoryOption(
      category: ErrorCategory.executionCalculation,
      color: Color(0xFFF3E8FF),
    ),
    _CategoryOption(
      category: ErrorCategory.reviewUnit,
      color: Color(0xFFECFDF5),
    ),
  ];

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    return Container(
      padding: const EdgeInsets.fromLTRB(20, 16, 20, 24),
      decoration: const BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Center(
            child: Container(
              width: 44,
              height: 5,
              decoration: BoxDecoration(
                color: Colors.grey[300],
                borderRadius: BorderRadius.circular(99),
              ),
            ),
          ),
          const SizedBox(height: 16),
          Row(
            children: [
              const Icon(Icons.psychology, color: KidsPalette.cocoa, size: 28),
              const SizedBox(width: 10),
              Expanded(
                child: Text(
                  strings.t('errorSheet.title'),
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                        fontWeight: FontWeight.bold,
                        color: KidsPalette.ink,
                      ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 6),
          Text(
            strings.t('errorSheet.description'),
            style: Theme.of(context).textTheme.bodySmall?.copyWith(
                  color: KidsPalette.cocoaSoft,
                ),
          ),
          const SizedBox(height: 16),
          Flexible(
            child: ListView.separated(
              shrinkWrap: true,
              itemCount: _categoryOptions.length,
              separatorBuilder: (context, index) => const SizedBox(height: 8),
              itemBuilder: (context, index) {
                final option = _categoryOptions[index];
                return InkWell(
                  onTap: () {
                    onCategorySelected(option.category);
                    Navigator.of(context).pop();
                  },
                  borderRadius: BorderRadius.circular(12),
                  child: Container(
                    padding: const EdgeInsets.all(14),
                    decoration: BoxDecoration(
                      color: option.color,
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: KidsPalette.line),
                    ),
                    child: Row(
                      children: [
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                strings.t(
                                  'errorSheet.${option.category.code}.title',
                                ),
                                style: const TextStyle(
                                  fontSize: 15,
                                  fontWeight: FontWeight.bold,
                                  color: KidsPalette.ink,
                                ),
                              ),
                              const SizedBox(height: 3),
                              Text(
                                strings.t(
                                  'errorSheet.${option.category.code}.description',
                                ),
                                style: TextStyle(
                                  fontSize: 13,
                                  color: Colors.grey[700],
                                ),
                              ),
                            ],
                          ),
                        ),
                        const Icon(Icons.arrow_forward_ios,
                            size: 16, color: KidsPalette.cocoaSoft),
                      ],
                    ),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}

class _CategoryOption {
  const _CategoryOption({
    required this.category,
    required this.color,
  });

  final ErrorCategory category;
  final Color color;
}
