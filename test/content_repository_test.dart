import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/services/content_repository.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('ContentRepository', () {
    test('discovers bundled grade 3 problem assets', () async {
      final repository = ContentRepository();

      final manifest = await repository.loadManifest();

      expect(manifest.problems, isNotEmpty);
      expect(manifest.problems.first.id, isNotEmpty);
      expect(
        manifest.problems.first.path,
        startsWith(ContentRepository.problemsPath),
      );
    });

    test('loads a discovered problem through json renderer and solvable files',
        () async {
      final repository = ContentRepository();
      final manifest = await repository.loadManifest();

      final content = await repository.loadProblem(manifest.problems.first);

      expect(content.semantic, isNotEmpty);
      expect(content.renderer, isNotEmpty);
      expect(content.solvable, isNotEmpty);
      expect(content.correctAnswer, isNotEmpty);
    });

    test('loads the first renderer prefix as a JSON preview bundle', () async {
      final repository = ContentRepository();

      final prefixes = await repository.loadGrade3JsonProblemPrefixes();
      expect(prefixes, isNotEmpty);

      final bundle = await repository.loadProblemJsonBundle(prefixes.first);

      expect(bundle.filePrefix, equals(prefixes.first));
      expect(bundle.semantic, isNotEmpty);
      expect(bundle.layout, isNotEmpty);
      expect(bundle.renderer, isNotEmpty);
    });
  });
}
