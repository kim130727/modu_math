import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'package:http/http.dart' as http;

import '../models/content_models.dart';
import 'problem_file_loader.dart'
    if (dart.library.io) 'problem_file_loader_io.dart';

enum ContentRepositorySource {
  localExamples,
  localHttp,
  bundledAssets,
  githubExamples,
}

class ContentRepository {
  ContentRepository({
    ContentRepositorySource? source,
    http.Client? httpClient,
    this.githubOwner = 'kim130727',
    this.githubRepo = 'modu_math',
    this.githubRef = 'main',
    this.githubProblemsPath = 'examples/problems',
    this.localProblemsPath = r'..\..\examples\problems',
    this.localHttpBaseUrl = 'http://localhost:8765',
  })  : source = source ??
            (kIsWeb
                ? ContentRepositorySource.localHttp
                : ContentRepositorySource.localExamples),
        _httpClient = httpClient ?? http.Client();

  ContentRepository.githubExamples({http.Client? httpClient})
      : this(
          source: ContentRepositorySource.githubExamples,
          httpClient: httpClient,
        );

  ContentRepository.bundledAssets()
      : this(source: ContentRepositorySource.bundledAssets);

  ContentRepository.localExamples({String? localProblemsPath})
      : this(
          source: ContentRepositorySource.localExamples,
          localProblemsPath: localProblemsPath ?? r'..\..\examples\problems',
        );

  ContentRepository.localHttp({
    http.Client? httpClient,
    String localHttpBaseUrl = 'http://localhost:8765',
  }) : this(
          source: ContentRepositorySource.localHttp,
          httpClient: httpClient,
          localHttpBaseUrl: localHttpBaseUrl,
        );

  static const String problemsPath = 'examples/problems';
  static const String manifestPath = '$problemsPath/manifest.json';
  static const String grade3Path = '$problemsPath/grade3';
  static const String generatedPath = '$problemsPath/generated';
  static const Set<String> localizedProblemLocales = {'ko', 'uk'};

  final ContentRepositorySource source;
  final http.Client _httpClient;
  final String githubOwner;
  final String githubRepo;
  final String githubRef;
  final String githubProblemsPath;
  final String localProblemsPath;
  final String localHttpBaseUrl;
  List<String>? _rendererPathCache;
  final Map<String, Future<ProblemContent>> _problemCache = {};
  String activeProblemLocale = 'ko';

  Future<ProblemManifest> loadManifest() async {
    if (source == ContentRepositorySource.localHttp) {
      final localProblems = await _loadBundledProblems();
      return ProblemManifest(
        version: 'local-http',
        problems: localProblems,
        raw: {
          'version': 'local-http',
          'source': 'local-http',
          'baseUrl': localHttpBaseUrl,
          'problems': localProblems.map((problem) => problem.raw).toList(),
        },
      );
    }

    if (source == ContentRepositorySource.localExamples) {
      final localProblems = await _loadBundledProblems();
      return ProblemManifest(
        version: 'local',
        problems: localProblems,
        raw: {
          'version': 'local',
          'source': 'local',
          'path': localProblemsPath,
          'problems': localProblems.map((problem) => problem.raw).toList(),
        },
      );
    }

    if (source == ContentRepositorySource.githubExamples) {
      final githubProblems = await _loadBundledProblems();
      return ProblemManifest(
        version: githubRef,
        problems: githubProblems,
        raw: {
          'version': githubRef,
          'source': 'github',
          'repository': '$githubOwner/$githubRepo',
          'ref': githubRef,
          'path': githubProblemsPath,
          'problems': githubProblems.map((problem) => problem.raw).toList(),
        },
      );
    }

    final bundledProblems = await _loadBundledProblems();
    final decoded = await _loadOptionalManifest();
    if (decoded == null) {
      return ProblemManifest(
        version: 'examples',
        problems: bundledProblems,
        raw: {
          'version': 'examples',
          'source': 'bundled-examples',
          'path': problemsPath,
          'problems': bundledProblems.map((problem) => problem.raw).toList(),
        },
      );
    }
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
    final cacheKey = _problemCacheKey(summary);
    final cached = _problemCache[cacheKey];
    if (cached != null) {
      return cached;
    }
    final future = _loadProblemUncached(summary);
    _problemCache[cacheKey] = future;
    try {
      return await future;
    } on Object {
      _problemCache.remove(cacheKey);
      rethrow;
    }
  }

  Future<void> preloadProblem(ProblemSummary summary) async {
    await loadProblem(summary);
  }

  Future<ProblemContent> _loadProblemUncached(ProblemSummary summary) async {
    final filePrefix = summary.filePrefix ?? summary.id;
    final basePath = await _basePathForPrefix(filePrefix);
    final semanticFuture = _loadJson('$basePath.semantic.json');
    final rendererFuture = _loadJson('$basePath.renderer.json');
    final layoutFuture = _loadOptionalJson('$basePath.layout.json');
    final solvableFuture = _loadSolvable(basePath);

    final semantic = await semanticFuture;
    final renderer = await rendererFuture;
    final layout = await layoutFuture;
    final solvable = await solvableFuture;
    return ProblemContent(
      summary: summary,
      semantic: semantic,
      solvable: solvable,
      layout: layout,
      renderer: renderer,
    );
  }

  String _problemCacheKey(ProblemSummary summary) {
    return [
      source.name,
      activeProblemLocale,
      summary.filePrefix ?? summary.id,
    ].join('|');
  }

  Future<ProblemJsonBundle> loadProblemJsonBundle(String filePrefix) async {
    final basePath = await _basePathForPrefix(filePrefix);
    final semanticFuture = _loadJson('$basePath.semantic.json');
    final layoutFuture = _loadJson('$basePath.layout.json');
    final rendererFuture = _loadJson('$basePath.renderer.json');
    final solvableV12Future = _loadOptionalJson(
      '$basePath.solvable.v1.2.json',
    );

    final solvableV12 = await solvableV12Future;
    return ProblemJsonBundle(
      filePrefix: filePrefix,
      semantic: await semanticFuture,
      layout: await layoutFuture,
      renderer: await rendererFuture,
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
      ..sort(_compareProblemPrefixes);
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
      } on Object catch (error) {
        if (_isMissingContent(error)) {
          continue;
        }
        rethrow;
      }
    }
    return const {};
  }

  Future<String> _basePathForPrefix(String filePrefix) async {
    final rendererPaths = await _loadRendererPaths();
    final baseFilePrefix = _baseProblemPrefix(filePrefix);
    final localizedFilePrefix = _localizedFilePrefix(filePrefix);
    final rendererPath =
        _findRendererPath(rendererPaths, localizedFilePrefix) ??
            _findRendererPath(rendererPaths, filePrefix) ??
            _findRendererPath(rendererPaths, baseFilePrefix) ??
            '';
    if (rendererPath.isEmpty) {
      return '$problemsPath/$localizedFilePrefix';
    }
    return rendererPath.substring(
      0,
      rendererPath.length - '.renderer.json'.length,
    );
  }

  String? _findRendererPath(List<String> rendererPaths, String filePrefix) {
    for (final path in rendererPaths) {
      if (path.endsWith('/$filePrefix.renderer.json') ||
          path == '$filePrefix.renderer.json' ||
          path == '$problemsPath/$filePrefix.renderer.json') {
        return path;
      }
    }
    return null;
  }

  String _localizedFilePrefix(String filePrefix) {
    final basePrefix = _baseProblemPrefix(filePrefix);
    final locale = localizedProblemLocales.contains(activeProblemLocale)
        ? activeProblemLocale
        : 'ko';
    return '${basePrefix}_$locale';
  }

  Future<List<ProblemSummary>> _loadBundledProblems() async {
    final rendererPaths = await _loadRendererPaths();

    final problems = rendererPaths.map((rendererPath) {
      final filePrefix = rendererPath
          .split('/')
          .last
          .replaceFirst(RegExp(r'\.renderer\.json$'), '');
      final path = rendererPath
          .split('/')
          .sublist(0, rendererPath.split('/').length - 1)
          .join('/');
      return _summaryFromPrefix(path: path, filePrefix: filePrefix);
    }).toList()
      ..sort((a, b) =>
          _compareProblemPrefixes(a.filePrefix ?? a.id, b.filePrefix ?? b.id));
    return problems;
  }

  Future<List<String>> _loadRendererPaths() async {
    if (source == ContentRepositorySource.localExamples) {
      return _rendererPathCache ??= await loadLocalRendererPaths(
        localProblemsPath,
      );
    }

    if (source == ContentRepositorySource.localHttp) {
      try {
        return _rendererPathCache ??= await _loadLocalHttpRendererPaths();
      } on Object {
        final manifest = await AssetManifest.loadFromAssetBundle(rootBundle);
        return manifest
            .listAssets()
            .where((path) => _isBundledRendererPathForActiveLocale(path))
            .toList()
          ..sort();
      }
    }

    if (source == ContentRepositorySource.githubExamples) {
      return _rendererPathCache ??= await _loadGithubRendererPaths();
    }

    final manifest = await AssetManifest.loadFromAssetBundle(rootBundle);
    return manifest
        .listAssets()
        .where((path) => _isBundledRendererPathForActiveLocale(path))
        .toList()
      ..sort();
  }

  bool _isBundledRendererPathForActiveLocale(String path) {
    if (!path.startsWith('$problemsPath/') ||
        !path.endsWith('.renderer.json')) {
      return false;
    }
    final locale = localizedProblemLocales.contains(activeProblemLocale)
        ? activeProblemLocale
        : 'ko';
    if (_isProblemPathAtRoot(path, problemsPath)) {
      return true;
    }
    final localizedPrefix = '$problemsPath/$locale/';
    if (path.startsWith(localizedPrefix)) {
      return true;
    }
    if (path.startsWith('$generatedPath/')) {
      return true;
    }
    return false;
  }

  Future<Map<String, dynamic>?> _loadOptionalManifest() async {
    try {
      final manifestSource = await rootBundle.loadString(manifestPath);
      return jsonDecode(manifestSource) as Map<String, dynamic>;
    } on Object catch (error) {
      if (_isMissingContent(error)) {
        return null;
      }
      rethrow;
    }
  }

  bool _isProblemPathAtRoot(String path, String rootPath) {
    if (!path.startsWith('$rootPath/')) {
      return false;
    }
    final relativePath = path.substring(rootPath.length + 1);
    return !relativePath.contains('/');
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
    final source = switch (this.source) {
      ContentRepositorySource.localExamples => await loadLocalText(assetPath),
      ContentRepositorySource.localHttp => await _loadLocalHttpText(assetPath),
      ContentRepositorySource.githubExamples => await _loadGithubText(
          assetPath,
        ),
      ContentRepositorySource.bundledAssets => await rootBundle.loadString(
          assetPath,
        ),
    };
    return jsonDecode(source) as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> _loadOptionalJson(String assetPath) async {
    try {
      return await _loadJson(assetPath);
    } on Object catch (error) {
      if (_isMissingContent(error)) {
        return const {};
      }
      rethrow;
    }
  }

  Future<List<String>> _loadGithubRendererPaths() async {
    final response = await _httpClient.get(
      Uri.https(
        'api.github.com',
        '/repos/$githubOwner/$githubRepo/git/trees/$githubRef',
        {'recursive': '1'},
      ),
      headers: const {'Accept': 'application/vnd.github+json'},
    );
    if (response.statusCode != 200) {
      throw StateError(
        'GitHub problem tree load failed: ${response.statusCode}',
      );
    }
    final decoded = jsonDecode(response.body) as Map<String, dynamic>;
    final tree = decoded['tree'];
    if (tree is! List) {
      return const [];
    }
    final prefix = githubProblemsPath.endsWith('/')
        ? githubProblemsPath
        : '$githubProblemsPath/';
    return tree
        .whereType<Map<String, dynamic>>()
        .where((item) => item['type']?.toString() == 'blob')
        .map((item) => item['path']?.toString() ?? '')
        .where(
          (path) => path.startsWith(prefix) && path.endsWith('.renderer.json'),
        )
        .toList()
      ..sort();
  }

  Future<List<String>> _loadLocalHttpRendererPaths() async {
    final response = await _httpClient.get(_localHttpUri('/api/problems'));
    if (response.statusCode != 200) {
      throw StateError(
        'Local problem server list load failed: ${response.statusCode}',
      );
    }
    final decoded =
        jsonDecode(utf8.decode(response.bodyBytes)) as Map<String, dynamic>;
    final paths = decoded['paths'];
    if (paths is! List) {
      return const [];
    }
    return paths
        .map((path) => path.toString())
        .where((path) => path.endsWith('.renderer.json'))
        .map((path) => path.replaceAll(r'\', '/'))
        .toList()
      ..sort();
  }

  Future<String> _loadLocalHttpText(String path) async {
    final serverPath = _serverRelativeProblemPath(path);
    try {
      final response = await _httpClient.get(
        _localHttpUri('/files/${Uri.encodeComponent(serverPath)}'),
      );
      if (response.statusCode == 404) {
        throw _MissingContent(path);
      }
      if (response.statusCode != 200) {
        throw StateError(
          'Local problem server file load failed: ${response.statusCode} $path',
        );
      }
      return utf8.decode(response.bodyBytes);
    } on _MissingContent {
      rethrow;
    } on Object {
      return rootBundle.loadString(_bundledProblemPath(path));
    }
  }

  String _serverRelativeProblemPath(String path) {
    final normalized = path.replaceAll(r'\', '/');
    const prefix = '$problemsPath/';
    if (normalized.startsWith(prefix)) {
      return normalized.substring(prefix.length);
    }
    return normalized;
  }

  String _bundledProblemPath(String path) {
    final normalized = path.replaceAll(r'\', '/');
    if (normalized.startsWith('$problemsPath/')) {
      return normalized;
    }
    return '$problemsPath/$normalized';
  }

  Uri _localHttpUri(String path) {
    final base = localHttpBaseUrl.endsWith('/')
        ? localHttpBaseUrl
        : '$localHttpBaseUrl/';
    final normalizedPath = path.startsWith('/') ? path.substring(1) : path;
    return Uri.parse('$base$normalizedPath');
  }

  Future<String> _loadGithubText(String path) async {
    final response = await _httpClient.get(_githubRawUri(path));
    if (response.statusCode == 404) {
      throw _MissingContent(path);
    }
    if (response.statusCode != 200) {
      throw StateError(
        'GitHub problem file load failed: ${response.statusCode} $path',
      );
    }
    return utf8.decode(response.bodyBytes);
  }

  Uri _githubRawUri(String path) {
    return Uri.https(
      'raw.githubusercontent.com',
      '/$githubOwner/$githubRepo/$githubRef/$path',
    );
  }
}

bool _isMissingContent(Object error) {
  return error is FlutterError ||
      error is MissingLocalContent ||
      error is _MissingContent;
}

class _MissingContent implements Exception {
  const _MissingContent(this.path);

  final String path;

  @override
  String toString() => 'Missing content: $path';
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

String _baseProblemPrefix(String filePrefix) {
  for (final locale in ContentRepository.localizedProblemLocales) {
    final suffix = '_$locale';
    if (filePrefix.endsWith(suffix)) {
      return filePrefix.substring(0, filePrefix.length - suffix.length);
    }
  }
  return filePrefix;
}

int _compareProblemPrefixes(String a, String b) {
  final aParts = _tokenizeForNaturalSort(a);
  final bParts = _tokenizeForNaturalSort(b);
  final length = aParts.length < bParts.length ? aParts.length : bParts.length;
  for (var i = 0; i < length; i += 1) {
    final aPart = aParts[i];
    final bPart = bParts[i];
    final aNumber = int.tryParse(aPart);
    final bNumber = int.tryParse(bPart);
    if (aNumber != null && bNumber != null) {
      final numberComparison = aNumber.compareTo(bNumber);
      if (numberComparison != 0) {
        return numberComparison;
      }
      final lengthComparison = aPart.length.compareTo(bPart.length);
      if (lengthComparison != 0) {
        return lengthComparison;
      }
      continue;
    }
    final textComparison = aPart.compareTo(bPart);
    if (textComparison != 0) {
      return textComparison;
    }
  }
  return aParts.length.compareTo(bParts.length);
}

List<String> _tokenizeForNaturalSort(String value) {
  return RegExp(r'\d+|\D+')
      .allMatches(value)
      .map((match) => match.group(0) ?? '')
      .toList();
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
