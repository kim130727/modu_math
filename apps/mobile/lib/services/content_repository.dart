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
    this.localHttpBaseUrl = 'http://127.0.0.1:8765',
  })  : source = source ??
            (kIsWeb
                ? ContentRepositorySource.localHttp
                : ContentRepositorySource.bundledAssets),
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
    String localHttpBaseUrl = 'http://127.0.0.1:8765',
  }) : this(
          source: ContentRepositorySource.localHttp,
          httpClient: httpClient,
          localHttpBaseUrl: localHttpBaseUrl,
        );

  static const String problemsPath = 'examples/problems';
  static const String manifestPath = '$problemsPath/manifest.json';
  static const String grade3Path = '$problemsPath/grade3';
  static const String generatedPath = '$problemsPath/generated';
  static const Set<String> localizedProblemLocales = {'ko'};

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
  final Map<String, ProblemContent> _completedProblemCache = {};
  String _activeProblemLocale = 'ko';

  ProblemManifest? _cachedManifest;

  String get activeProblemLocale => _activeProblemLocale;

  set activeProblemLocale(String locale) {
    if (_activeProblemLocale == locale) {
      return;
    }
    _activeProblemLocale = locale;
    _rendererPathCache = null;
    _cachedManifest = null;
  }

  Future<ProblemManifest> loadManifest() async {
    if (_cachedManifest != null) {
      return SynchronousFuture(_cachedManifest!);
    }
    final manifest = await _loadManifestUncached();
    _cachedManifest = manifest;
    return manifest;
  }

  bool _localHttpFailed = false;

  Future<ProblemManifest> _loadManifestUncached() async {
    if (source == ContentRepositorySource.localHttp && !_localHttpFailed) {
      try {
        final localProblems = await _loadBundledProblems()
            .timeout(const Duration(milliseconds: 1500));
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
      } catch (_) {
        _localHttpFailed = true;
      }
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

    final decoded = await _loadOptionalManifest();
    if (decoded != null && decoded['problems'] is List) {
      final manifest = ProblemManifest.fromJson(decoded);
      if (manifest.problems.isNotEmpty) {
        return manifest;
      }
    }

    final bundledProblems = await _loadBundledProblems();
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

  Future<ProblemContent> loadProblem(ProblemSummary summary) {
    final cacheKey = _problemCacheKey(summary);
    final completed = _completedProblemCache[cacheKey];
    if (completed != null) {
      return SynchronousFuture(completed);
    }
    final cached = _problemCache[cacheKey];
    if (cached != null) {
      return cached;
    }
    return _cacheProblemLoad(summary, cacheKey);
  }

  Future<ProblemContent> _cacheProblemLoad(
    ProblemSummary summary,
    String cacheKey,
  ) async {
    final future = _loadProblemUncached(summary);
    _problemCache[cacheKey] = future;
    try {
      final content = await future;
      _completedProblemCache[cacheKey] = content;
      return content;
    } on Object {
      _problemCache.remove(cacheKey);
      rethrow;
    }
  }

  Future<void> preloadProblem(ProblemSummary summary) async {
    await loadProblem(summary);
  }

  Future<ProblemContent> _loadProblemUncached(ProblemSummary summary) async {
    if (source == ContentRepositorySource.localHttp) {
      final bundle = await _tryLoadLocalHttpProblemBundle(summary);
      if (bundle != null) {
        return bundle;
      }
    }

    final filePrefix = summary.filePrefix ?? summary.id;
    final basePath = await _basePathForPrefix(filePrefix);
    final results = await Future.wait<dynamic>([
      _loadJson('$basePath.semantic.json'),
      _loadJson('$basePath.renderer.json'),
      _loadOptionalJson('$basePath.layout.json'),
      _loadSolvable(basePath),
    ]);

    return ProblemContent(
      summary: summary,
      semantic: results[0] as Map<String, dynamic>,
      renderer: results[1] as Map<String, dynamic>,
      layout: results[2] as Map<String, dynamic>,
      solvable: results[3] as Map<String, dynamic>,
    );
  }

  Future<ProblemContent?> _tryLoadLocalHttpProblemBundle(
    ProblemSummary summary,
  ) async {
    final filePrefix = summary.filePrefix ?? summary.id;
    try {
      final response = await _httpClient.get(
        _localHttpUri('/api/problem-bundle/${Uri.encodeComponent(filePrefix)}'),
      );
      if (response.statusCode != 200) {
        return null;
      }
      final decoded =
          jsonDecode(utf8.decode(response.bodyBytes)) as Map<String, dynamic>;
      if (decoded['ok'] != true) {
        return null;
      }
      return ProblemContent(
        summary: summary,
        semantic: _asMap(decoded['semantic']),
        renderer: _asMap(decoded['renderer']),
        layout: _asMap(decoded['layout']),
        solvable: _asMap(decoded['solvable']),
        svg: decoded['svg']?.toString() ?? '',
      );
    } catch (_) {
      return null;
    }
  }

  static Map<String, dynamic> _asMap(dynamic value) {
    if (value is Map<String, dynamic>) {
      return value;
    }
    if (value is Map) {
      return Map<String, dynamic>.from(value);
    }
    return const {};
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
    final solvableV13Future = _loadOptionalJson(
      '$basePath.solvable.v1.3.json',
    );

    final solvableV13 = await solvableV13Future;
    final solvableV12 = await solvableV12Future;
    return ProblemJsonBundle(
      filePrefix: filePrefix,
      semantic: await semanticFuture,
      layout: await layoutFuture,
      renderer: await rendererFuture,
      solvable: solvableV13.isNotEmpty
          ? solvableV13
          : solvableV12.isEmpty
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
      'solvable.v1.3.json',
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
            _findRendererPath(rendererPaths, baseFilePrefix) ??
            _findRendererPath(rendererPaths, filePrefix) ??
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
    if (source == ContentRepositorySource.localHttp) {
      final summaries = await _tryLoadLocalHttpProblemSummaries();
      if (summaries != null && summaries.isNotEmpty) {
        return summaries;
      }
    }

    final rendererPaths = await _loadRendererPaths();

    final problems = await Future.wait(rendererPaths.map((rendererPath) {
      final filePrefix = rendererPath
          .split('/')
          .last
          .replaceFirst(RegExp(r'\.renderer\.json$'), '');
      final path = rendererPath
          .split('/')
          .sublist(0, rendererPath.split('/').length - 1)
          .join('/');
      return _summaryFromPrefix(path: path, filePrefix: filePrefix);
    }))
      ..sort((a, b) =>
          _compareProblemPrefixes(a.filePrefix ?? a.id, b.filePrefix ?? b.id));
    return problems;
  }

  Future<List<ProblemSummary>?> _tryLoadLocalHttpProblemSummaries() async {
    try {
      final response = await _httpClient.get(_localHttpUri('/api/problems'));
      if (response.statusCode != 200) {
        return null;
      }
      final decoded =
          jsonDecode(utf8.decode(response.bodyBytes)) as Map<String, dynamic>;
      final paths = decoded['paths'];
      if (paths is List) {
        _rendererPathCache = paths
            .map((path) => path.toString())
            .where((path) => path.endsWith('.renderer.json'))
            .map((path) => path.replaceAll(r'\', '/'))
            .toList()
          ..sort();
      }
      final problems = decoded['problems'];
      if (problems is List && problems.isNotEmpty) {
        return problems
            .whereType<Map<String, dynamic>>()
            .map(ProblemSummary.fromJson)
            .toList()
          ..sort((a, b) =>
              _compareProblemPrefixes(a.filePrefix ?? a.id, b.filePrefix ?? b.id));
      }
    } catch (_) {}
    return null;
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

  Future<ProblemSummary> _summaryFromPrefix({
    required String path,
    required String filePrefix,
  }) async {
    final basePath = path.isEmpty ? filePrefix : '$path/$filePrefix';
    final semantic = await _loadOptionalJson('$basePath.semantic.json');
    final metadata = _mapAt(semantic, 'metadata');

    final unitInfo = resolveUnitInfo(
      path: path,
      filePrefix: filePrefix,
      semantic: semantic,
    );

    final grade = unitInfo.grade;
    final semester = unitInfo.semester;
    final unitNumber = unitInfo.unitNumber;
    final unitTopic = unitInfo.unitTopic;

    final title = _summaryTitle(metadata, unitTopic);
    final problemType = _problemTypeLabel(
      semantic?['problem_type']?.toString(),
    );
    final raw = <String, dynamic>{
      'id': filePrefix,
      'grade': grade,
      'subject': 'math',
      'unit': '$semester학기 $unitNumber. $unitTopic',
      'type': problemType,
      'title': title,
      'path': path,
      'filePrefix': filePrefix,
      'semester': '$semester학기',
      'unitNumber': unitNumber,
      'unitTopic': unitTopic,
      if (semantic?['problem_type'] != null)
        'problemType': semantic!['problem_type'].toString(),
      if (metadata['topic'] != null) 'topic': metadata['topic'].toString(),
    };
    return ProblemSummary.fromJson(raw);
  }

  static ParsedUnitInfo resolveUnitInfo({
    required String path,
    required String filePrefix,
    Map<String, dynamic>? semantic,
  }) {
    // 1. Folder path check (e.g. 3-1/1_덧셈과_뺄셈, 3-2/3_원, 들이와_무게 등)
    final normalizedPath = path.replaceAll(r'\', '/');
    final segments =
        normalizedPath.split('/').where((s) => s.isNotEmpty).toList();

    int? detectedGrade;
    int? detectedSemester;
    int? detectedUnitNumber;
    String? detectedUnitTopic;

    for (final segment in segments) {
      if (segment == '3-1' || segment == '3_1' || segment == '1학기') {
        detectedGrade = 3;
        detectedSemester = 1;
      } else if (segment == '3-2' || segment == '3_2' || segment == '2학기') {
        detectedGrade = 3;
        detectedSemester = 2;
      }

      final matchNumbered = RegExp(r'^(\d+)[._\s]+(.+)$').firstMatch(segment);
      if (matchNumbered != null) {
        final num = int.tryParse(matchNumbered.group(1)!);
        final topicName = matchNumbered.group(2)!.replaceAll('_', ' ').trim();
        if (num != null && num >= 1 && num <= 6) {
          detectedUnitNumber = num;
          detectedUnitTopic = topicName;
        }
      } else if (segment.contains('덧셈') ||
          segment.contains('뺄셈') ||
          segment.contains('평면도형') ||
          segment.contains('나눗셈') ||
          segment.contains('곱셈') ||
          segment.contains('길이') ||
          segment.contains('시간') ||
          segment.contains('분수') ||
          segment.contains('소수') ||
          segment.contains('원') ||
          segment.contains('들이') ||
          segment.contains('무게') ||
          segment.contains('자료')) {
        detectedUnitTopic = segment.replaceAll('_', ' ').trim();
      }
    }

    // 2. Metadata & problem_type & title & tags check
    final metadata = semantic != null
        ? _mapAt(semantic, 'metadata')
        : const <String, dynamic>{};
    final problemType =
        semantic?['problem_type']?.toString().toLowerCase() ?? '';
    final metaTitle = metadata['title']?.toString() ?? '';
    final metaInstruction = metadata['instruction']?.toString() ?? '';
    final metaTopic = metadata['topic']?.toString() ?? '';
    final tags = (metadata['tags'] is List
            ? (metadata['tags'] as List).join(' ')
            : '')
        .toLowerCase();
    final metaCombined =
        '$problemType $metaTitle $metaInstruction $metaTopic $tags'
            .toLowerCase();

    if (detectedUnitTopic == null) {
      if (metaCombined.contains('원') ||
          metaCombined.contains('circle') ||
          metaCombined.contains('지름') ||
          metaCombined.contains('반지름') ||
          metaCombined.contains('중심') ||
          metaCombined.contains('컴퍼스')) {
        detectedGrade = 3;
        detectedSemester = 2;
        detectedUnitNumber = 3;
        detectedUnitTopic = '원';
      } else if (metaCombined.contains('들이') ||
          metaCombined.contains('무게') ||
          metaCombined.contains('capacity') ||
          metaCombined.contains('weight') ||
          metaCombined.contains('어림') ||
          metaCombined.contains('저울') ||
          metaCombined.contains('생수병') ||
          metaCombined.contains('물병') ||
          metaCombined.contains('리터') ||
          metaCombined.contains('그램')) {
        detectedGrade = 3;
        detectedSemester = 2;
        detectedUnitNumber = 5;
        detectedUnitTopic = '들이와 무게';
      } else if (metaCombined.contains('곱셈') ||
          metaCombined.contains('multiplication') ||
          metaCombined.contains('product')) {
        detectedGrade = 3;
        detectedSemester = 1;
        detectedUnitNumber = 4;
        detectedUnitTopic = '곱셈';
      } else if (metaCombined.contains('나눗셈') ||
          metaCombined.contains('division') ||
          metaCombined.contains('remainder') ||
          metaCombined.contains('몫') ||
          metaCombined.contains('나머지')) {
        detectedGrade = 3;
        detectedSemester = 1;
        detectedUnitNumber = 3;
        detectedUnitTopic = '나눗셈';
      } else if (metaCombined.contains('평면도형') ||
          metaCombined.contains('직각') ||
          metaCombined.contains('삼각형') ||
          metaCombined.contains('직사각형') ||
          metaCombined.contains('정사각형') ||
          metaCombined.contains('geometry') ||
          metaCombined.contains('도형')) {
        detectedGrade = 3;
        detectedSemester = 1;
        detectedUnitNumber = 2;
        detectedUnitTopic = '평면도형';
      } else if (metaCombined.contains('분수') ||
          metaCombined.contains('fraction') ||
          metaCombined.contains('소수')) {
        detectedGrade = 3;
        detectedSemester = 1;
        detectedUnitNumber = 6;
        detectedUnitTopic = '분수와 소수';
      } else if (metaCombined.contains('길이') ||
          metaCombined.contains('시간') ||
          metaCombined.contains('거리') ||
          metaCombined.contains('초')) {
        detectedGrade = 3;
        detectedSemester = 1;
        detectedUnitNumber = 5;
        detectedUnitTopic = '길이와 시간';
      } else if (metaCombined.contains('덧셈') ||
          metaCombined.contains('뺄셈') ||
          metaCombined.contains('addition') ||
          metaCombined.contains('subtraction') ||
          metaCombined.contains('세로셈') ||
          metaCombined.contains('받아올림') ||
          metaCombined.contains('수 모형')) {
        detectedGrade = 3;
        detectedSemester = 1;
        detectedUnitNumber = 1;
        detectedUnitTopic = '덧셈과 뺄셈';
      }
    }

    // 3. Fallback to standard filePrefix parsing
    final fallbackGrade = _gradeFromPrefix(filePrefix);
    final fallbackSemester = _semesterFromPrefix(filePrefix);
    final fallbackUnitNumber = _unitNumberFromPrefix(filePrefix);

    final grade = detectedGrade ?? fallbackGrade;
    final semester = detectedSemester ?? fallbackSemester;
    final unitNumber = detectedUnitNumber ?? fallbackUnitNumber;
    final unitTopic =
        detectedUnitTopic ?? _unitTopicFor(grade, semester, unitNumber);

    return ParsedUnitInfo(
      grade: grade,
      semester: semester,
      unitNumber: unitNumber,
      unitTopic: unitTopic,
    );
  }

  static String _unitTopicFor(int grade, int semester, int unitNumber) {
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

  String _summaryTitle(Map<String, dynamic> metadata, String unitTopic) {
    final metadataTitle = metadata['title']?.toString().trim() ?? '';
    if (metadataTitle.isNotEmpty) {
      return metadataTitle;
    }
    final topic = metadata['topic']?.toString().trim() ?? '';
    if (topic.isNotEmpty) {
      return topic;
    }
    return _titleForUnit(unitTopic);
  }

  String _problemTypeLabel(String? rawProblemType) {
    final raw = rawProblemType?.trim() ?? '';
    if (raw.isEmpty) {
      return '문제';
    }
    if (_hasKorean(raw)) {
      return raw.replaceAll('_', ' ');
    }

    final type = raw.toLowerCase();
    final labels = <String>[];
    void add(String label) {
      if (!labels.contains(label)) {
        labels.add(label);
      }
    }

    if (type.contains('word')) add('문장제');
    if (type.contains('vertical')) add('세로셈');
    if (type.contains('base_ten')) add('수 모형');
    if (type.contains('expression')) add('식');
    if (type.contains('comparison') || type.contains('compare')) add('비교');
    if (type.contains('ordering') || type.contains('order')) add('순서');
    if (type.contains('unit')) add('단위');
    if (type.contains('weight')) add('무게');
    if (type.contains('capacity')) add('들이');
    if (type.contains('circle')) add('원');
    if (type.contains('fraction')) add('분수');
    if (type.contains('perimeter')) add('둘레');
    if (type.contains('route') || type.contains('distance')) add('거리');
    if (type.contains('choice') || type.contains('selection')) add('선택형');
    if (type.contains('blank') || type.contains('fill')) add('빈칸');
    if (type.contains('multi')) add('여러 답');
    if (type.contains('numeric')) add('수 답');
    if (type.contains('stepwise') || type.contains('sequential')) add('단계형');
    if (type.contains('addition')) add('덧셈');
    if (type.contains('subtraction')) add('뺄셈');
    if (type.contains('multiplication')) add('곱셈');
    if (type.contains('division')) add('나눗셈');

    if (labels.isEmpty) {
      return raw.replaceAll('_', ' ');
    }
    return labels.join(' · ');
  }

  bool _hasKorean(String value) {
    return RegExp(r'[가-힣]').hasMatch(value);
  }

  Future<Map<String, dynamic>> _loadJson(String assetPath) async {
    final source = switch (this.source) {
      ContentRepositorySource.localExamples => await loadLocalText(assetPath),
      ContentRepositorySource.localHttp => _localHttpFailed
          ? await rootBundle.loadString(_bundledProblemPath(assetPath))
          : await _loadLocalHttpText(assetPath),
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

Map<String, dynamic> _mapAt(Map<String, dynamic> map, String key) {
  final value = map[key];
  if (value is Map<String, dynamic>) {
    return value;
  }
  return const {};
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

class ParsedUnitInfo {
  const ParsedUnitInfo({
    required this.grade,
    required this.semester,
    required this.unitNumber,
    required this.unitTopic,
  });

  final int grade;
  final int semester;
  final int unitNumber;
  final String unitTopic;
}
