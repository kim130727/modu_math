import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/models/content_models.dart';
import 'package:modu_math_app/services/content_repository.dart';
import 'package:modu_math_app/utils/problem_presentation.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('Korean and Ukrainian problem loading', () {
    test('loads and normalizes S3_elem_3_008661 in Ukrainian', () async {
      final repository = ContentRepository.bundledAssets()
        ..activeProblemLocale = 'uk';

      const staleKoreanSummary = ProblemSummary(
        id: 'S3_elem_3_008661',
        grade: 3,
        subject: 'math',
        unit: '1학기 2. 평면도형',
        type: 'local_json_problem',
        title: '길이가 가장 긴 선분 찾기',
        path: 'examples/problems/ko',
        filePrefix: 'S3_elem_3_008661',
        raw: {
          'id': 'S3_elem_3_008661',
          'filePrefix': 'S3_elem_3_008661',
        },
      );

      final content = await repository.loadProblem(staleKoreanSummary);

      expect(content.summary.path, 'examples/problems/uk');
      expect(content.summary.title, 'Який відрізок найдовший?');
      expect(content.prompt, contains('найдовший'));
      expect(RegExp(r'[\uac00-\ud7a3]').hasMatch(content.prompt), isFalse);
      expect(content.choices, isNotEmpty);
    });

    test('switching from Korean to Ukrainian reloads localized content',
        () async {
      final repository = ContentRepository.bundledAssets();
      final manifest = await repository.loadManifest();
      final summary = manifest.problems.firstWhere(
        (problem) => problem.id == 'S3_elem_3_008661',
      );

      final korean = await repository.loadProblem(summary);
      expect(korean.prompt, contains('선분'));

      repository.activeProblemLocale = 'uk';
      final ukrainian = await repository.loadProblem(summary);
      expect(ukrainian.summary.path, 'examples/problems/uk');
      expect(ukrainian.prompt, contains('найдовший'));
    });

    test('retains Ukrainian diagram labels and separates prompt text',
        () async {
      final repository = ContentRepository.bundledAssets()
        ..activeProblemLocale = 'uk';
      final manifest = await repository.loadManifest();

      final circleSummary = manifest.problems.firstWhere(
        (problem) => problem.id == 'S3_elem_3_008664',
      );
      final circle = await repository.loadProblem(circleSummary);
      final circleElements = (problemVisualRenderer(circle)['elements'] as List)
          .map((element) => '${element['id']}:${element['text']}')
          .toList();
      expect(circleElements.any((e) => e.startsWith('slot.question')), isFalse);
      expect(circleElements.any((e) => e.startsWith('slot.choice.lb.1.text:A')),
          isTrue);
      expect(circle.prompt, contains('Накресліть коло'));

      final sequenceSummary = manifest.problems.firstWhere(
        (problem) => problem.id == 'S3_elem_3_008713',
      );
      final sequence = await repository.loadProblem(sequenceSummary);
      final sequenceElements =
          (problemVisualRenderer(sequence)['elements'] as List)
              .map((element) => '${element['id']}:${element['text']}')
              .toList();
      expect(sequenceElements.any((e) => e.startsWith('slot.stem')), isFalse);
      expect(sequence.prompt, contains('креслення кола'));
      expect(sequence.choices, hasLength(5));
    });
  });
}
