import 'package:flutter/foundation.dart';

import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/services/content_repository.dart';
import 'package:modu_math_app/services/solvable_hint_service.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  
  test('verify zero Korean in hints across all 10 problems and all non-Korean locales', () async {
    final repo = ContentRepository.bundledAssets();
    final manifest = await repo.loadManifest();
    final nonKoreanLocales = ['en', 'ja', 'zh', 'km', 'uk'];
    final hangulRegex = RegExp(r'[\uac00-\ud7a3]');

    final untranslated = <String>[];
    for (final problem in manifest.problems) {
      final content = await repo.loadProblem(problem);
      for (final locale in nonKoreanLocales) {
        final hints = const SolvableHintService().buildHints(content, locale: locale);
        for (final h in hints) {
          if (hangulRegex.hasMatch(h.title)) {
            untranslated.add('[${problem.id}][$locale][title] ${h.title}');
          }
          if (hangulRegex.hasMatch(h.body)) {
            untranslated.add('[${problem.id}][$locale][body] ${h.body}');
          }
          if (hangulRegex.hasMatch(h.miniQuestion)) {
            untranslated.add('[${problem.id}][$locale][miniQuestion] ${h.miniQuestion}');
          }
          if (hangulRegex.hasMatch(h.successMessage)) {
            untranslated.add('[${problem.id}][$locale][successMessage] ${h.successMessage}');
          }
        }
      }
    }
    for (final u in untranslated) {
      debugPrint(u);
    }
    expect(untranslated, isEmpty);
  });
}
