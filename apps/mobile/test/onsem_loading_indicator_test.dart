import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/l10n/app_strings.dart';
import 'package:modu_math_app/widgets/onsem_loading_indicator.dart';

void main() {
  final hangulRegex = RegExp(r'[\uac00-\ud7a3]');

  group('OnsemLoadingIndicator multilingual localization', () {
    const nonKoreanLocales = ['en', 'ja', 'zh', 'km', 'uk'];

    for (final lang in nonKoreanLocales) {
      testWidgets('renders default loading without Korean in $lang', (tester) async {
        await tester.pumpWidget(
          AppLocaleScope(
            locale: Locale(lang),
            onLocaleChanged: (_) {},
            child: const MaterialApp(
              home: Scaffold(
                body: OnsemLoadingIndicator(),
              ),
            ),
          ),
        );
        await tester.pump();

        final textFinder = find.byType(Text);
        expect(textFinder, findsOneWidget);
        final renderedText = tester.widget<Text>(textFinder).data ?? '';
        expect(renderedText, isNotEmpty);
        expect(
          hangulRegex.hasMatch(renderedText),
          isFalse,
          reason: 'Rendered text in $lang contained Korean: "$renderedText"',
        );
      });

      testWidgets('renders labelKey without Korean in $lang', (tester) async {
        await tester.pumpWidget(
          AppLocaleScope(
            locale: Locale(lang),
            onLocaleChanged: (_) {},
            child: const MaterialApp(
              home: Scaffold(
                body: OnsemLoadingIndicator(labelKey: 'home.loading'),
              ),
            ),
          ),
        );
        await tester.pump();

        final textFinder = find.byType(Text);
        expect(textFinder, findsOneWidget);
        final renderedText = tester.widget<Text>(textFinder).data ?? '';
        expect(renderedText, isNotEmpty);
        expect(
          hangulRegex.hasMatch(renderedText),
          isFalse,
          reason: 'Rendered home.loading in $lang contained Korean: "$renderedText"',
        );
      });

      testWidgets('automatically translates legacy Korean label into $lang', (tester) async {
        await tester.pumpWidget(
          AppLocaleScope(
            locale: Locale(lang),
            onLocaleChanged: (_) {},
            child: const MaterialApp(
              home: Scaffold(
                body: OnsemLoadingIndicator(label: '문제를 불러오고 있어요'),
              ),
            ),
          ),
        );
        await tester.pump();

        final textFinder = find.byType(Text);
        expect(textFinder, findsOneWidget);
        final renderedText = tester.widget<Text>(textFinder).data ?? '';
        expect(renderedText, isNotEmpty);
        expect(
          hangulRegex.hasMatch(renderedText),
          isFalse,
          reason: 'Legacy label translated in $lang contained Korean: "$renderedText"',
        );
      });
    }

    testWidgets('dynamically updates text when AppLocaleScope locale changes', (tester) async {
      Locale activeLocale = const Locale('ko');

      await tester.pumpWidget(
        StatefulBuilder(
          builder: (context, setState) {
            return AppLocaleScope(
              locale: activeLocale,
              onLocaleChanged: (newLocale) {
                setState(() => activeLocale = newLocale);
              },
              child: const MaterialApp(
                home: Scaffold(
                  body: OnsemLoadingIndicator(labelKey: 'problem.loading'),
                ),
              ),
            );
          },
        ),
      );
      await tester.pump();

      // In Korean
      expect(find.text('문제를 불러오고 있어요'), findsOneWidget);

      // Change to English
      activeLocale = const Locale('en');
      await tester.pumpWidget(
        StatefulBuilder(
          builder: (context, setState) {
            return AppLocaleScope(
              locale: activeLocale,
              onLocaleChanged: (newLocale) {
                setState(() => activeLocale = newLocale);
              },
              child: const MaterialApp(
                home: Scaffold(
                  body: OnsemLoadingIndicator(labelKey: 'problem.loading'),
                ),
              ),
            );
          },
        ),
      );
      await tester.pump();
      expect(find.text('Loading problem...'), findsOneWidget);

      // Change to Japanese
      activeLocale = const Locale('ja');
      await tester.pumpWidget(
        StatefulBuilder(
          builder: (context, setState) {
            return AppLocaleScope(
              locale: activeLocale,
              onLocaleChanged: (newLocale) {
                setState(() => activeLocale = newLocale);
              },
              child: const MaterialApp(
                home: Scaffold(
                  body: OnsemLoadingIndicator(labelKey: 'problem.loading'),
                ),
              ),
            );
          },
        ),
      );
      await tester.pump();
      expect(find.text('問題を読み込んでいます...'), findsOneWidget);

      // Change to Ukrainian
      activeLocale = const Locale('uk');
      await tester.pumpWidget(
        StatefulBuilder(
          builder: (context, setState) {
            return AppLocaleScope(
              locale: activeLocale,
              onLocaleChanged: (newLocale) {
                setState(() => activeLocale = newLocale);
              },
              child: const MaterialApp(
                home: Scaffold(
                  body: OnsemLoadingIndicator(labelKey: 'problem.loading'),
                ),
              ),
            );
          },
        ),
      );
      await tester.pump();
      expect(find.text('Завантажуємо задачу...'), findsOneWidget);
    });
  });
}
