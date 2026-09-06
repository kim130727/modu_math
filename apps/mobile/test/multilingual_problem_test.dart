import 'package:flutter/painting.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/models/content_models.dart';
import 'package:modu_math_app/services/content_repository.dart';
import 'package:modu_math_app/utils/problem_presentation.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('Multilingual Problem Loading & Isolation', () {
    test('loads S3_elem_3_008661 in English with zero Chinese text', () async {
      final repository = ContentRepository.bundledAssets()
        ..activeProblemLocale = 'en';

      final enSummary = ProblemSummary(
        id: 'S3_elem_3_008661',
        grade: 3,
        subject: 'math',
        unit: '1학기 2. 평면도형',
        type: 'local_json_problem',
        title: 'Find the longest line segment',
        path: 'examples/problems/en',
        filePrefix: 'S3_elem_3_008661',
        raw: const {
          'id': 'S3_elem_3_008661',
          'filePrefix': 'S3_elem_3_008661',
        },
      );

      final content = await repository.loadProblem(enSummary);

      expect(content.summary.title, equals('Which line segment is the longest?'));
      expect(content.prompt, contains('longest'));
      expect(content.choices, isNotEmpty);

      // Check choices are English line segments (AB, CD, EF, etc.)
      for (final label in content.choices) {
        // Must not contain Chinese characters
        expect(RegExp(r'[\u4e00-\u9fff]').hasMatch(label), isFalse,
            reason: 'Choice label should not contain Chinese: $label');
      }

      // Check renderer elements do not contain Chinese text
      final elements = content.renderer['elements'];
      if (elements is List) {
        for (final element in elements) {
          if (element is Map && element['text'] != null) {
            final text = element['text'].toString();
            expect(RegExp(r'[\u4e00-\u9fff]').hasMatch(text), isFalse,
                reason: 'Renderer text should not contain Chinese: $text');
          }
        }
      }
    });

    test('normalizes problem path to English even if given summary has zh path', () async {
      final repository = ContentRepository.bundledAssets()
        ..activeProblemLocale = 'en';

      // Simulate a summary that previously held a Chinese path
      final staleSummary = ProblemSummary(
        id: 'S3_elem_3_008661',
        grade: 3,
        subject: 'math',
        unit: '1학기 2. 평면도형',
        type: 'local_json_problem',
        title: '找出最长的线段',
        path: 'examples/problems/zh',
        filePrefix: 'S3_elem_3_008661',
        raw: const {
          'id': 'S3_elem_3_008661',
          'filePrefix': 'S3_elem_3_008661',
          'path': 'examples/problems/zh',
        },
      );

      final content = await repository.loadProblem(staleSummary);

      // Should be normalized to English
      expect(content.summary.path, equals('examples/problems/en'));
      expect(content.summary.title, equals('Which line segment is the longest?'));
      expect(content.prompt, contains('longest'));
      expect(RegExp(r'[\u4e00-\u9fff]').hasMatch(content.prompt), isFalse);
    });

    test('dynamically switching locale from zh to en updates loaded content and choices', () async {
      final repository = ContentRepository.bundledAssets()
        ..activeProblemLocale = 'zh';

      final summary = ProblemSummary(
        id: 'S3_elem_3_008661',
        grade: 3,
        subject: 'math',
        unit: '1학기 2. 평면도형',
        type: 'local_json_problem',
        title: '找出最长的线段',
        path: 'examples/problems/zh',
        filePrefix: 'S3_elem_3_008661',
        raw: const {
          'id': 'S3_elem_3_008661',
          'filePrefix': 'S3_elem_3_008661',
        },
      );

      // Load in Chinese
      final zhContent = await repository.loadProblem(summary);
      expect(zhContent.prompt, contains('最长'));

      // Now switch locale to English
      repository.activeProblemLocale = 'en';
      final enContent = await repository.loadProblem(summary);

      expect(enContent.summary.path, equals('examples/problems/en'));
      expect(enContent.summary.title, equals('Which line segment is the longest?'));
      expect(enContent.prompt, contains('longest'));
      expect(RegExp(r'[\u4e00-\u9fff]').hasMatch(enContent.prompt), isFalse);
    });

    test('manifest for English locale contains English titles and paths', () async {
      final repository = ContentRepository.bundledAssets()
        ..activeProblemLocale = 'en';

      final manifest = await repository.loadManifest();
      expect(manifest.problems, isNotEmpty);

      final problem = manifest.problems.firstWhere(
        (p) => p.id == 'S3_elem_3_008661',
      );
      expect(problem.path, equals('examples/problems/en'));
      expect(problem.title, equals('Which line segment is the longest?'));
    });

    test('inspect S3_elem_3_008664 in ko vs uk', () async {
      final repoKo = ContentRepository.bundledAssets()..activeProblemLocale = 'ko';
      final manifestKo = await repoKo.loadManifest();
      final summaryKo = manifestKo.problems.firstWhere((p) => p.id == 'S3_elem_3_008664');
      final contentKo = await repoKo.loadProblem(summaryKo);

      final repoUk = ContentRepository.bundledAssets()..activeProblemLocale = 'uk';
      final manifestUk = await repoUk.loadManifest();
      final summaryUk = manifestUk.problems.firstWhere((p) => p.id == 'S3_elem_3_008664');
      final contentUk = await repoUk.loadProblem(summaryUk);

      print('008664 KO prompt: ${contentKo.prompt}');
      print('008664 KO choices: ${contentKo.choices}');
      print('008664 UK prompt: ${contentUk.prompt}');
      print('008664 UK choices: ${contentUk.choices}');

      final visualKo = problemVisualRenderer(contentKo);
      final visualUk = problemVisualRenderer(contentUk);

      final elementsKo = (visualKo['elements'] as List).map((e) => '${e['id']}:${e['text']}').toList();
      final elementsUk = (visualUk['elements'] as List).map((e) => '${e['id']}:${e['text']}').toList();

      print('008664 KO visual elements: $elementsKo');
      print('008664 UK visual elements: $elementsUk');

      // Verify KO stem is removed from canvas
      expect(elementsKo.any((e) => e.startsWith('slot.question')), isFalse);
      // Verify UK labels A..E are present on canvas
      expect(elementsUk.any((e) => e.startsWith('slot.choice.lb.1:A')), isTrue);
      expect(elementsUk.any((e) => e.startsWith('slot.choice.lb.5:E')), isTrue);
    });

    test('inspect S3_elem_3_008713 in ko vs en', () async {
      final repoKo = ContentRepository.bundledAssets()..activeProblemLocale = 'ko';
      final manifestKo = await repoKo.loadManifest();
      final summaryKo = manifestKo.problems.firstWhere((p) => p.id == 'S3_elem_3_008713');
      final contentKo = await repoKo.loadProblem(summaryKo);

      final repoEn = ContentRepository.bundledAssets()..activeProblemLocale = 'en';
      final manifestEn = await repoEn.loadManifest();
      final summaryEn = manifestEn.problems.firstWhere((p) => p.id == 'S3_elem_3_008713');
      final contentEn = await repoEn.loadProblem(summaryEn);

      final visualKo = problemVisualRenderer(contentKo);
      final visualEn = problemVisualRenderer(contentEn);

      final elementsKo = (visualKo['elements'] as List).map((e) => '${e['id']}:${e['text']}').toList();
      final elementsEn = (visualEn['elements'] as List).map((e) => '${e['id']}:${e['text']}').toList();

      print('008713 KO visual elements: $elementsKo');
      print('008713 EN visual elements: $elementsEn');

      // In EN, slot.stem should be removed from canvas
      expect(elementsEn.any((e) => e.startsWith('slot.stem')), isFalse);
    });
  });
}






