import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/services/content_repository.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  const locales = ['ko', 'en', 'zh', 'ja', 'km', 'uk'];
  const expectedProblemIds = [
    'S3_elem_3_008540',
    'S3_elem_3_008541',
    'S3_elem_3_008631',
    'S3_elem_3_008661',
    'S3_elem_3_008664',
    'S3_elem_3_008713',
    'S3_elem_3_008728',
    'S3_elem_3_008732',
    'S3_elem_3_008745',
    'S3_elem_3_008751',
  ];

  group('Multilingual 10 MVP Problems', () {
    for (final locale in locales) {
      test('loads all 10 problems in ' + locale, () async {
        final repository = ContentRepository.bundledAssets();
        repository.activeProblemLocale = locale;

        final manifest = await repository.loadManifest();
        expect(
          manifest.problems.length,
          equals(10),
          reason: 'Should discover exactly 10 problems for locale ' + locale,
        );

        final discoveredIds = manifest.problems.map((p) => p.id).toList();
        for (final id in expectedProblemIds) {
          expect(discoveredIds, contains(id));
        }

        final firstSummary = manifest.problems.first;
        final firstContent = await repository.loadProblem(firstSummary);
        expect(firstContent.semantic, isNotEmpty);
        expect(firstContent.renderer, isNotEmpty);
        expect(firstContent.solvable, isNotEmpty);
      });
    }

    test('switches problem locale dynamically', () async {
      final repository = ContentRepository.bundledAssets();

      // 1. Korean
      repository.activeProblemLocale = 'ko';
      var manifest = await repository.loadManifest();
      expect(manifest.problems.length, equals(10));
      var summary = manifest.problems.firstWhere((p) => p.id == 'S3_elem_3_008540');
      var content = await repository.loadProblem(summary);
      expect(content.semantic['metadata']['title'], isNotEmpty);

      // 2. English
      repository.activeProblemLocale = 'en';
      manifest = await repository.loadManifest();
      expect(manifest.problems.length, equals(10));
      summary = manifest.problems.firstWhere((p) => p.id == 'S3_elem_3_008540');
      content = await repository.loadProblem(summary);
      expect(content.semantic['metadata']['title'], isNotEmpty);

      // 3. Japanese
      repository.activeProblemLocale = 'ja';
      manifest = await repository.loadManifest();
      expect(manifest.problems.length, equals(10));
      summary = manifest.problems.firstWhere((p) => p.id == 'S3_elem_3_008540');
      content = await repository.loadProblem(summary);
      expect(content.semantic['metadata']['title'], isNotEmpty);

      // 4. Chinese
      repository.activeProblemLocale = 'zh';
      manifest = await repository.loadManifest();
      expect(manifest.problems.length, equals(10));
      summary = manifest.problems.firstWhere((p) => p.id == 'S3_elem_3_008540');
      content = await repository.loadProblem(summary);
      expect(content.semantic['metadata']['title'], isNotEmpty);

      // 5. Khmer
      repository.activeProblemLocale = 'km';
      manifest = await repository.loadManifest();
      expect(manifest.problems.length, equals(10));
      summary = manifest.problems.firstWhere((p) => p.id == 'S3_elem_3_008540');
      content = await repository.loadProblem(summary);
      expect(content.semantic['metadata']['title'], isNotEmpty);

      // 6. Ukrainian
      repository.activeProblemLocale = 'uk';
      manifest = await repository.loadManifest();
      expect(manifest.problems.length, equals(10));
      summary = manifest.problems.firstWhere((p) => p.id == 'S3_elem_3_008540');
      content = await repository.loadProblem(summary);
      expect(content.semantic['metadata']['title'], isNotEmpty);
    });

    test('uses Latin alphabet notation for points and geometric segments in Ukrainian', () async {
      final repository = ContentRepository.bundledAssets();
      repository.activeProblemLocale = 'uk';
      final manifest = await repository.loadManifest();

      // S3_elem_3_008661: geometry segment comparison (AB, CD, EF, GI)
      final geomProblem = manifest.problems.firstWhere((p) => p.id == 'S3_elem_3_008661');
      final geomContent = await repository.loadProblem(geomProblem);
      final choices = (geomContent.semantic['answer']['choices'] as List).cast<String>();
      expect(choices, contains('1. Відрізок AB'));
      expect(choices, contains('2. Відрізок CD'));
      expect(choices, contains('3. Відрізок EF'));
      expect(choices, contains('4. Відрізок GI'));
      expect(geomContent.semantic['answer']['value'], '2. Відрізок CD');

      // S3_elem_3_008664: geometry circle hole points (A, B, C, D, E)
      final circleProblem = manifest.problems.firstWhere((p) => p.id == 'S3_elem_3_008664');
      final circleContent = await repository.loadProblem(circleProblem);
      final holeChoices = (circleContent.semantic['answer']['choices'] as List).cast<String>();
      expect(holeChoices, containsAll(['A', 'B', 'C', 'D', 'E']));
      expect(circleContent.semantic['answer']['value'], 'E');
    });

    test('verifies zero Korean in prompt, title, and choices for en, zh, ja', () async {
      final repository = ContentRepository.bundledAssets();
      final koreanRegex = RegExp(r'[\uAC00-\uD7A3]');

      for (final locale in ['en', 'zh', 'ja']) {
        repository.activeProblemLocale = locale;
        final manifest = await repository.loadManifest();
        final problem = manifest.problems.firstWhere((p) => p.id == 'S3_elem_3_008540');
        final content = await repository.loadProblem(problem);

        expect(koreanRegex.hasMatch(content.prompt), isFalse,
            reason: 'content.prompt should have no Korean in ' + locale);
        expect(koreanRegex.hasMatch(content.summary.title), isFalse,
            reason: 'content.summary.title should have no Korean in ' + locale);
        for (final choice in content.choices) {
          expect(koreanRegex.hasMatch(choice), isFalse,
              reason: 'choice should have no Korean in ' + locale);
        }
      }
    });
  });
}
