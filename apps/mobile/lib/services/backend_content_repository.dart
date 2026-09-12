import 'dart:convert';
import 'dart:typed_data';

import 'package:http/http.dart' as http;

import '../models/content_models.dart';
import 'content_repository.dart';

/// Loads the published problem catalog and JSON contracts from Django.
/// Bundled assets remain an offline fallback and provide legacy local assets.
class BackendContentRepository extends ContentRepository {
  BackendContentRepository({
    required String baseUrl,
    http.Client? httpClient,
  })  : baseUrl = baseUrl.replaceAll(RegExp(r'/+$'), ''),
        _client = httpClient ?? http.Client(),
        _fallback = ContentRepository.bundledAssets(),
        super(source: ContentRepositorySource.bundledAssets);

  final String baseUrl;
  final http.Client _client;
  final ContentRepository _fallback;
  final Map<String, ProblemContent> _contentCache = {};
  ProblemManifest? _manifestCache;

  @override
  set activeProblemLocale(String locale) {
    if (locale == super.activeProblemLocale) return;
    super.activeProblemLocale = locale;
    _fallback.activeProblemLocale = locale;
    _manifestCache = null;
    _contentCache.clear();
  }

  Uri _uri(String path, [Map<String, String>? query]) {
    final root = baseUrl.isEmpty ? 'http://127.0.0.1:8000' : baseUrl;
    return Uri.parse('$root$path').replace(queryParameters: query);
  }

  @override
  Future<ProblemManifest> loadManifest() async {
    if (_manifestCache != null) return _manifestCache!;
    try {
      final problems = <ProblemSummary>[];
      Uri? next = _uri('/api/v1/problems/', {
        'language': activeProblemLocale,
        'grade': '3',
      });
      while (next != null) {
        final response = await _client.get(next);
        if (response.statusCode != 200) {
          throw StateError('Problem API returned ${response.statusCode}');
        }
        final decoded =
            jsonDecode(utf8.decode(response.bodyBytes)) as Map<String, dynamic>;
        final results = decoded['results'] as List<dynamic>? ?? const [];
        problems
            .addAll(results.whereType<Map<String, dynamic>>().map(_summary));
        final nextValue = decoded['next']?.toString() ?? '';
        next = nextValue.isEmpty ? null : Uri.parse(nextValue);
      }
      problems.sort((a, b) => a.id.compareTo(b.id));
      return _manifestCache = ProblemManifest(
        version: 'django-api-v1',
        problems: problems,
        raw: {
          'version': 'django-api-v1',
          'source': 'django-api',
          'problems': problems.map((problem) => problem.raw).toList(),
        },
      );
    } catch (_) {
      return _fallback.loadManifest();
    }
  }

  ProblemSummary _summary(Map<String, dynamic> item) {
    return ProblemSummary.fromJson({
      ...item,
      'id': item['problem_id'],
      'dbId': item['id'],
      'type': item['problem_type'],
      'filePrefix': item['file_prefix'] ?? item['problem_id'],
      'unitNumber': item['unit_number'],
      'unitTopic': item['unit_topic'],
      'subUnit': item['sub_unit'],
    });
  }

  @override
  Future<ProblemContent> loadProblem(ProblemSummary summary) async {
    final cacheKey = '${summary.dbId}:${summary.language}';
    final cached = _contentCache[cacheKey];
    if (cached != null) return cached;
    final dbId = summary.dbId;
    if (dbId == null) return _fallback.loadProblem(summary);
    try {
      final response = await _client.get(_uri('/api/v1/problems/$dbId/'));
      if (response.statusCode != 200) {
        throw StateError('Problem detail API returned ${response.statusCode}');
      }
      final data =
          jsonDecode(utf8.decode(response.bodyBytes)) as Map<String, dynamic>;
      final content = ProblemContent(
        summary: _summary(data),
        svg: await _loadSvg(data),
        semantic: _map(data['semantic_data']),
        solvable: _map(data['solvable_data']),
        layout: _map(data['layout_data']),
        renderer: _map(data['renderer_data']),
      );
      _contentCache[cacheKey] = content;
      return content;
    } catch (_) {
      return _fallback.loadProblem(summary);
    }
  }

  @override
  Future<ProblemContent> refreshProblem(ProblemSummary summary) {
    _contentCache.remove('${summary.dbId}:${summary.language}');
    return loadProblem(summary);
  }

  Future<String> _loadSvg(Map<String, dynamic> data) async {
    final dbId = data['id'];
    final prefix = data['file_prefix'] ?? data['problem_id'];
    if (dbId == null || prefix == null) return '';
    final response = await _client.get(
      _uri('/api/v1/problems/$dbId/asset/', {'filename': '$prefix.svg'}),
    );
    return response.statusCode == 200 ? utf8.decode(response.bodyBytes) : '';
  }

  @override
  Future<Uint8List> loadProblemAsset(
    ProblemSummary summary,
    String relativePath,
  ) async {
    final dbId = summary.dbId;
    if (dbId != null &&
        !relativePath.contains('/') &&
        !relativePath.contains(r'\')) {
      try {
        final response = await _client.get(
          _uri('/api/v1/problems/$dbId/asset/', {'filename': relativePath}),
        );
        if (response.statusCode == 200) return response.bodyBytes;
      } catch (_) {}
    }
    return _fallback.loadProblemAsset(summary, relativePath);
  }

  static Map<String, dynamic> _map(dynamic value) {
    return value is Map ? Map<String, dynamic>.from(value) : const {};
  }
}
