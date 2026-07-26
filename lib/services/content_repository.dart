import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';

import '../models/content_models.dart';

class ContentRepository {
  static const String manifestPath = 'assets/content/problems/manifest.json';
  static const String problemsPath = 'assets/content/problems';
  static const String grade3Path = 'assets/content/problems/grade3';

  Future<ProblemManifest> loadManifest() async {
    final source = await rootBundle.loadString(manifestPath);
    final decoded = jsonDecode(source) as Map<String, dynamic>;
    final bundledProblems = await _loadBundledProblems();
    if (bundledProblems.isEmpty) {
      return ProblemManifest.fromJson(decoded);
    }
    return ProblemManifest(
      version: decoded['version']?.toString() ?? '0.1.0',
      problems: bundledProblems,
      raw: {
        ...decoded,
        'problems': bundledProblems.map((problem) => problem.raw).toList(),
      },
    );
  }

  Future<ProblemContent> loadProblem(ProblemSummary summary) async {
    final filePrefix = summary.filePrefix ?? summary.id;
    final basePath = await _basePathForPrefix(filePrefix);
    final semantic = await _loadJson('$basePath.semantic.json');
    final renderer = await _loadJson('$basePath.renderer.json');
    final layout = await _loadOptionalJson('$basePath.layout.json');
    final solvable = await _loadSolvable(basePath);
    final svg = await _loadOptionalText('$basePath.svg');
    return ProblemContent(
      summary: summary,
      svg: svg,
      semantic: semantic,
      solvable: solvable,
      layout: layout,
      renderer: renderer,
    );
  }

  Future<ProblemJsonBundle> loadProblemJsonBundle(String filePrefix) async {
    final basePath = await _basePathForPrefix(filePrefix);
    final solvableV12 = await _loadOptionalJson('$basePath.solvable.v1.2.json');
    return ProblemJsonBundle(
      filePrefix: filePrefix,
      semantic: await _loadJson('$basePath.semantic.json'),
      layout: await _loadJson('$basePath.layout.json'),
      renderer: await _loadJson('$basePath.renderer.json'),
      solvable: solvableV12.isEmpty
          ? await _loadOptionalJson('$basePath.solvable.v1.1.json')
          : solvableV12,
    );
  }

  Future<List<String>> loadGrade3JsonProblemPrefixes() async {
    final rendererPaths = await _loadRendererPaths();
    final prefixes = rendererPaths
        .map((path) {
          final fileName = path.split('/').last;
          return fileName.replaceFirst('.renderer.json', '');
        })
        .toSet()
        .toList()
      ..sort();
    return prefixes;
  }

  Future<Map<String, dynamic>> _loadSolvable(String basePath) async {
    for (final fileName in const [
      'solvable.json',
      'solvable.v1.2.json',
      'solvable.v1.1.json',
      'solvable.v1.json',
    ]) {
      try {
        return await _loadJson('$basePath.$fileName');
      } on FlutterError {
        continue;
      }
    }
    return const {};
  }

  Future<String> _basePathForPrefix(String filePrefix) async {
    final rendererPaths = await _loadRendererPaths();
    final rendererPath = rendererPaths.firstWhere(
      (path) =>
          path.endsWith('/$filePrefix.renderer.json') ||
          path == '$problemsPath/$filePrefix.renderer.json',
      orElse: () => '',
    );
    if (rendererPath.isEmpty) {
      return '$problemsPath/$filePrefix';
    }
    return rendererPath.substring(
      0,
      rendererPath.length - '.renderer.json'.length,
    );
  }

  Future<List<ProblemSummary>> _loadBundledProblems() async {
    final rendererPaths = await _loadRendererPaths();

    return rendererPaths.map((rendererPath) {
      final filePrefix = rendererPath
          .split('/')
          .last
          .replaceFirst(RegExp(r'\.renderer\.json$'), '');
      final path = rendererPath
          .split('/')
          .sublist(0, rendererPath.split('/').length - 1)
          .join('/');
      return _summaryFromPrefix(path: path, filePrefix: filePrefix);
    }).toList();
  }

  Future<List<String>> _loadRendererPaths() async {
    final manifest = await AssetManifest.loadFromAssetBundle(rootBundle);
    return manifest
        .listAssets()
        .where(
          (path) =>
              path.startsWith('$problemsPath/') &&
              path.endsWith('.renderer.json'),
        )
        .toList()
      ..sort();
  }

  ProblemSummary _summaryFromPrefix({
    required String path,
    required String filePrefix,
  }) {
    final grade = _gradeFromPrefix(filePrefix);
    final semester = _semesterFromPrefix(filePrefix);
    final unitNumber = _unitNumberFromPrefix(filePrefix);
    final unitTopic = _unitTopicFor(grade, semester, unitNumber);
    final raw = <String, dynamic>{
      'id': filePrefix,
      'grade': grade,
      'subject': 'math',
      'unit': '$semester학기 $unitNumber. $unitTopic',
      'type': 'local_json_problem',
      'title': _titleForUnit(unitTopic),
      'path': path,
      'filePrefix': filePrefix,
      'semester': '$semester학기',
      'unitNumber': unitNumber,
      'unitTopic': unitTopic,
    };
    return ProblemSummary.fromJson(raw);
  }

  String _unitTopicFor(int grade, int semester, int unitNumber) {
    if (grade == 3 && semester == 1) {
      return switch (unitNumber) {
        1 => '덧셈과 뺄셈',
        2 => '평면도형',
        3 => '나눗셈',
        4 => '곱셈',
        5 => '길이와 시간',
        6 => '분수와 소수',
        _ => '수학',
      };
    }
    if (grade == 3 && semester == 2) {
      return switch (unitNumber) {
        1 => '곱셈',
        2 => '나눗셈',
        3 => '원',
        4 => '분수',
        5 => '들이와 무게',
        6 => '자료의 정리',
        _ => '수학',
      };
    }
    return '수학';
  }

  String _titleForUnit(String unitTopic) {
    return switch (unitTopic) {
      '덧셈과 뺄셈' => '덧셈과 뺄셈 문제',
      '곱셈' => '곱셈 문제',
      '나눗셈' => '나눗셈 문제',
      '평면도형' => '도형 문제',
      '원' => '원 문제',
      '분수' => '분수 문제',
      '분수와 소수' => '분수와 소수 문제',
      '길이와 시간' => '길이와 시간 문제',
      '들이와 무게' => '들이와 무게 문제',
      '자료의 정리' => '자료 정리 문제',
      _ => '수학 문제',
    };
  }

  Future<Map<String, dynamic>> _loadJson(String assetPath) async {
    final source = await rootBundle.loadString(assetPath);
    return jsonDecode(source) as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> _loadOptionalJson(String assetPath) async {
    try {
      return await _loadJson(assetPath);
    } on FlutterError {
      return const {};
    }
  }

  Future<String> _loadOptionalText(String assetPath) async {
    try {
      return await rootBundle.loadString(assetPath);
    } on FlutterError {
      return '';
    }
  }
}

int _gradeFromPrefix(String filePrefix) {
  final match = RegExp(r'^P(\d+)_').firstMatch(filePrefix);
  return int.tryParse(match?.group(1) ?? '') ?? 3;
}

int _semesterFromPrefix(String filePrefix) {
  final parts = filePrefix.split('_');
  return parts.length > 1 ? int.tryParse(parts[1]) ?? 1 : 1;
}

int _unitNumberFromPrefix(String filePrefix) {
  final parts = filePrefix.split('_');
  return parts.length > 2 ? int.tryParse(parts[2]) ?? 1 : 1;
}

class ProblemJsonBundle {
  const ProblemJsonBundle({
    required this.filePrefix,
    required this.semantic,
    required this.layout,
    required this.renderer,
    required this.solvable,
  });

  final String filePrefix;
  final Map<String, dynamic> semantic;
  final Map<String, dynamic> layout;
  final Map<String, dynamic> renderer;
  final Map<String, dynamic> solvable;
}
