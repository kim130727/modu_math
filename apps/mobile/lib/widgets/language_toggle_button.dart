import 'package:flutter/material.dart';

import '../l10n/app_strings.dart';

class LanguageToggleButton extends StatelessWidget {
  const LanguageToggleButton({
    super.key,
    this.compact = false,
  });

  final bool compact;

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    final scope = AppLocaleScope.maybeOf(context);
    final selected = scope?.locale.languageCode ?? 'ko';
    final nextLocale =
        selected == 'uk' ? const Locale('ko') : const Locale('uk');

    return Semantics(
      button: true,
      label: strings.t('language.tooltip'),
      child: Material(
        color: compact
            ? Colors.transparent
            : Theme.of(context).colorScheme.surface.withValues(alpha: 0.92),
        shape: const CircleBorder(),
        elevation: compact ? 0 : 3,
        child: IconButton(
          visualDensity: VisualDensity.compact,
          tooltip: null,
          onPressed:
              scope == null ? null : () => scope.onLocaleChanged(nextLocale),
          icon: const Icon(Icons.language_rounded),
        ),
      ),
    );
  }
}
