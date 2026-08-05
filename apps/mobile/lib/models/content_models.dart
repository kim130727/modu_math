import '../utils/problem_text_sanitizer.dart';

class ProblemManifest {
  const ProblemManifest({
    required this.version,
    required this.problems,
    required this.raw,
  });

  final String version;
  final List<ProblemSummary> problems;
  final Map<String, dynamic> raw;

  factory ProblemManifest.fromJson(Map<String, dynamic> json) {
    final rawProblems = json['problems'];
    return ProblemManifest(
      version: json['version']?.toString() ?? '0.1.0',
      problems: rawProblems is List
          ? rawProblems
              .whereType<Map<String, dynamic>>()
              .map(ProblemSummary.fromJson)
              .toList()
          : const [],
      raw: json,
    );
  }
}

class ProblemSummary {
  const ProblemSummary({
    required this.id,
    required this.grade,
    required this.subject,
    required this.unit,
    required this.type,
    required this.title,
    required this.path,
    this.filePrefix,
    required this.raw,
  });

  final String id;
  final int grade;
  final String subject;
  final String unit;
  final String type;
  final String title;
  final String path;
  final String? filePrefix;
  final Map<String, dynamic> raw;

  factory ProblemSummary.fromJson(Map<String, dynamic> json) {
    return ProblemSummary(
      id: json['id']?.toString() ?? '',
      grade: _readInt(json['grade']) ?? 0,
      subject: json['subject']?.toString() ?? 'math',
      unit: json['unit']?.toString() ?? '미분류',
      type: json['type']?.toString() ?? 'unknown',
      title: json['title']?.toString() ?? json['id']?.toString() ?? '문제',
      path: json['path']?.toString() ?? '',
      filePrefix: json['filePrefix']?.toString(),
      raw: json,
    );
  }

  String assetPath(String fileName) {
    if (filePrefix != null && filePrefix!.isNotEmpty) {
      return '$path/$filePrefix.$fileName';
    }
    return '$path/$fileName';
  }
}

class ProblemContent {
  const ProblemContent({
    required this.summary,
    this.svg = '',
    required this.semantic,
    required this.solvable,
    this.layout = const {},
    this.renderer = const {},
  });

  final ProblemSummary summary;
  final String svg;
  final Map<String, dynamic> semantic;
  final Map<String, dynamic> solvable;
  final Map<String, dynamic> layout;
  final Map<String, dynamic> renderer;

  String get prompt {
    final metadata = _mapAt(semantic, 'metadata');
    final semanticPrompt =
        metadata['question']?.toString() ?? metadata['instruction']?.toString();
    if (semanticPrompt != null && !_looksBrokenText(semanticPrompt)) {
      return semanticPrompt;
    }
    final rendererPrompt = _rendererInstructionText();
    if (rendererPrompt.isNotEmpty) {
      return rendererPrompt;
    }
    return summary.title;
  }

  List<String> get choices {
    final answer = answerMap;
    final rawChoices = answer['choices'];
    if (rawChoices is List && rawChoices.isNotEmpty) {
      return rawChoices.map((choice) {
        if (choice is Map<String, dynamic>) {
          return sanitizeProblemText(
            choice['value']?.toString() ??
                choice['label']?.toString() ??
                choice.toString(),
          );
        }
        return sanitizeProblemText(choice.toString());
      }).toList();
    }
    return _choicesFromSvg();
  }

  Map<String, dynamic> get answerMap {
    final solvableAnswer = _mapAt(solvable, 'answer');
    if (solvableAnswer.isNotEmpty) {
      return solvableAnswer;
    }
    return _mapAt(semantic, 'answer');
  }

  String get correctAnswer {
    final answer = answerMap;
    final key = answer['answer_key'];
    if (key is List && key.isNotEmpty) {
      final values = key
          .map(_answerValueText)
          .map(sanitizeProblemText)
          .where((value) => value.isNotEmpty)
          .toList();
      final uniqueValues = values.toSet();
      if (uniqueValues.length == 1) {
        return uniqueValues.single;
      }
      return values.join();
    }
    if (key is! List && key != null && key.toString().isNotEmpty) {
      return sanitizeProblemText(key.toString());
    }
    final value = answer['value'];
    if (value is Map<String, dynamic>) {
      return sanitizeProblemText(_answerValueText(value));
    }
    if (value is List) {
      return sanitizeProblemText(value.map(_answerValueText).join());
    }
    return sanitizeProblemText(value?.toString() ?? '');
  }

  List<SolutionStep> get steps {
    final rawSteps = solvable['steps'];
    if (rawSteps is! List) {
      return const [];
    }
    return rawSteps
        .whereType<Map<String, dynamic>>()
        .map(SolutionStep.fromJson)
        .toList();
  }

  List<String> _choicesFromSvg() {
    final matches = RegExp(
      r'<text[^>]*id="slot\.(?:c\d+|opt|choice)[^"]*"[^>]*>([^<]+)</text>',
    ).allMatches(svg);
    final choices = matches
        .map(
          (match) => sanitizeProblemText(
            _decodeXmlText(match.group(1) ?? '').trim(),
          ),
        )
        .where((choice) => choice.isNotEmpty)
        .toList();
    return _extractInlineChoices(choices) ?? choices;
  }

  String _rendererInstructionText() {
    final elements = renderer['elements'];
    if (elements is! List) {
      return '';
    }
    for (final element in elements.whereType<Map<String, dynamic>>()) {
      final identity = [
        element['id'],
        element['source_ref'],
        _mapAt(element, 'refs')['layout_slot_id'],
        _mapAt(element, 'metadata')['layout_slot_id'],
      ].whereType<Object>().join(' ').toLowerCase();
      if (!identity.contains('instruction')) {
        continue;
      }
      final text = element['text']?.toString().trim() ?? '';
      if (text.isNotEmpty && !_looksBrokenText(text)) {
        return text;
      }
    }
    return '';
  }
}

List<String>? _extractInlineChoices(List<String> choices) {
  for (final choice in choices) {
    final match = RegExp(r'[\(（]([^()（）]+)[\)）]').firstMatch(choice);
    if (match == null) {
      continue;
    }

    final inlineChoices = match
        .group(1)!
        .split(RegExp(r'[,，/]'))
        .map((item) => item.replaceAll('.', '').trim())
        .where((item) => item.isNotEmpty)
        .toList();
    if (inlineChoices.length >= 2) {
      return inlineChoices;
    }
  }
  return null;
}

class SolutionStep {
  const SolutionStep({
    required this.id,
    required this.explanation,
    required this.value,
    required this.raw,
  });

  final String id;
  final String explanation;
  final String value;
  final Map<String, dynamic> raw;

  factory SolutionStep.fromJson(Map<String, dynamic> json) {
    return SolutionStep(
      id: json['id']?.toString() ?? '',
      explanation: json['explanation']?.toString() ??
          json['expr']?.toString() ??
          json['description']?.toString() ??
          '풀이 단계',
      value: json['value']?.toString() ?? '',
      raw: json,
    );
  }
}

Map<String, dynamic> _mapAt(Map<String, dynamic> map, String key) {
  final value = map[key];
  if (value is Map<String, dynamic>) {
    return value;
  }
  return const {};
}

int? _readInt(Object? value) {
  if (value is int) {
    return value;
  }
  return int.tryParse(value?.toString() ?? '');
}

String _decodeXmlText(String value) {
  return value
      .replaceAll('&lt;', '<')
      .replaceAll('&gt;', '>')
      .replaceAll('&amp;', '&')
      .replaceAll('&quot;', '"')
      .replaceAll('&apos;', "'");
}

String _answerValueText(Object? value) {
  if (value is Map<String, dynamic>) {
    for (final key in const ['result', 'value', 'answer', 'count']) {
      if (value.containsKey(key)) {
        return _answerValueText(value[key]);
      }
    }
  }
  if (value is List) {
    return value.map(_answerValueText).join();
  }
  return value?.toString() ?? '';
}

bool _looksBrokenText(String value) {
  return RegExp(r'[\u3400-\u9FFF\uFFFD]').hasMatch(value) ||
      value.contains('??') ||
      value.contains('�');
}
