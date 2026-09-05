import 'package:flutter/material.dart';

import '../l10n/app_strings.dart';

class LanguageToggleButton extends StatelessWidget {
  const LanguageToggleButton({
    super.key,
    this.compact = false,
  });

  final bool compact;

  static const languageFlags = {
    'ko': '🇰🇷',
    'uk': '🇺🇦',
    'en': '🇺🇸',
    'zh': '🇨🇳',
    'ja': '🇯🇵',
    'km': '🇰🇭',
  };

  void _showLanguageDialog(
    BuildContext context,
    AppLocaleScope scope,
    AppStrings strings,
  ) {
    final selectedCode = scope.locale.languageCode;
    showDialog<void>(
      context: context,
      builder: (dialogContext) {
        return AlertDialog(
          title: Text(strings.t('language.tooltip')),
          content: SingleChildScrollView(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: AppStrings.supportedLocales.map((locale) {
                final code = locale.languageCode;
                final flag = languageFlags[code] ?? '';
                final name = strings.t('language.$code');
                final isSelected = code == selectedCode;
                return ListTile(
                  leading: Text(flag, style: const TextStyle(fontSize: 24)),
                  title: Text(
                    name,
                    style: TextStyle(
                      fontWeight:
                          isSelected ? FontWeight.bold : FontWeight.normal,
                      color: isSelected
                          ? Theme.of(context).colorScheme.primary
                          : null,
                    ),
                  ),
                  trailing: isSelected
                      ? Icon(
                          Icons.check_rounded,
                          color: Theme.of(context).colorScheme.primary,
                        )
                      : null,
                  onTap: () {
                    Navigator.of(dialogContext).pop();
                    scope.onLocaleChanged(locale);
                  },
                );
              }).toList(),
            ),
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    final scope = AppLocaleScope.maybeOf(context);
    final selected = scope?.locale.languageCode ?? 'ko';

    const supported = AppStrings.supportedLocales;
    final currentIndex =
        supported.indexWhere((l) => l.languageCode == selected);
    final nextIndex =
        currentIndex < 0 ? 0 : (currentIndex + 1) % supported.length;
    final nextLocale = supported[nextIndex];

    return Semantics(
      button: true,
      label: strings.t('language.tooltip'),
      child: Material(
        color: compact
            ? Colors.transparent
            : Theme.of(context).colorScheme.surface.withValues(alpha: 0.92),
        shape: const CircleBorder(),
        elevation: 0,
        child: IconButton(
          style: IconButton.styleFrom(
            backgroundColor: compact
                ? Colors.transparent
                : Theme.of(context).colorScheme.surface,
            side: compact
                ? BorderSide.none
                : BorderSide(
                    color: Theme.of(context).colorScheme.outlineVariant,
                  ),
          ),
          visualDensity: VisualDensity.compact,
          tooltip: null,
          onPressed:
              scope == null ? null : () => scope.onLocaleChanged(nextLocale),
          onLongPress: scope == null
              ? null
              : () => _showLanguageDialog(context, scope, strings),
          icon: const Icon(Icons.language_rounded),
        ),
      ),
    );
  }
}
