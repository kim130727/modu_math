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

  String get semester => raw['semester']?.toString() ?? '1학기';
  int get unitNumber => _readInt(raw['unitNumber']) ?? 1;
  String get unitTopic => raw['unitTopic']?.toString() ?? unit;
  String get subUnit =>
      raw['subUnit']?.toString() ?? raw['subTopic']?.toString() ?? '기본 학습';

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
      final list = rawChoices.map((choice) {
        if (choice is Map<String, dynamic>) {
          return sanitizeProblemText(
            choice['value']?.toString() ??
                choice['label']?.toString() ??
                choice.toString(),
          );
        }
        return sanitizeProblemText(choice.toString());
      }).toList();
      return _mergeAlternatingMarkerChoices(list);
    }
    final rendererChoices = _choicesFromRenderer();
    if (rendererChoices.isNotEmpty) {
      return _ensureChoiceMarkers(_mergeAlternatingMarkerChoices(rendererChoices));
    }
    final svgChoices = _choicesFromSvg();
    if (svgChoices.isNotEmpty) {
      return _ensureChoiceMarkers(_mergeAlternatingMarkerChoices(svgChoices));
    }
    final givenChoices = _choicesFromSolvableGiven();
    if (givenChoices.isNotEmpty) {
      return _ensureChoiceMarkers(_mergeAlternatingMarkerChoices(givenChoices));
    }
    return const [];
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
    final textPattern = RegExp(
      r'<text\b([^>]*)>([^<]+)</text>',
    );
    final matches = textPattern.allMatches(svg);
    final rawItems = <({double x, double y, String text, String groupKey})>[];

    for (final match in matches) {
      final attrs = match.group(1) ?? '';
      final text =
          sanitizeProblemText(_decodeXmlText(match.group(2) ?? '').trim());
      if (text.isEmpty) continue;

      final idMatch = RegExp(r'id="([^"]+)"').firstMatch(attrs);
      final id = idMatch?.group(1)?.toLowerCase() ?? '';
      final isChoice = id.contains('choice') ||
          id.contains('opt') ||
          id.contains('option') ||
          id.contains('item') ||
          id.contains('.c1') ||
          id.contains('.c2') ||
          id.contains('.c3') ||
          id.contains('.c4') ||
          id.contains('.c5');

      final isCircledOrNumbered = RegExp(
        r'^(?:[①②③④⑤⑥⑦⑧⑨⑩]|\([1-9]\)|\([가-힣]\)|[1-9]\.)',
      ).hasMatch(text);

      if (!isChoice && !isCircledOrNumbered) continue;
      if (id.contains('question') ||
          id.contains('stem') ||
          id.contains('instruction')) continue;

      final xMatch = RegExp(r'x="([0-9.-]+)"').firstMatch(attrs);
      final yMatch = RegExp(r'y="([0-9.-]+)"').firstMatch(attrs);
      final x = double.tryParse(xMatch?.group(1) ?? '') ?? 0;
      final y = double.tryParse(yMatch?.group(1) ?? '') ?? 0;

      final groupKey = _extractChoiceGroupKey(id);
      rawItems.add((x: x, y: y, text: text, groupKey: groupKey));
    }

    if (rawItems.isEmpty) return const [];

    rawItems.sort((a, b) {
      final row = (a.y - b.y).abs() < 16 ? 0 : a.y.compareTo(b.y);
      return row != 0 ? row : a.x.compareTo(b.x);
    });

    final rows = <List<({double x, double y, String text, String groupKey})>>[];
    for (final item in rawItems) {
      if (rows.isEmpty) {
        rows.add([item]);
      } else {
        final lastRow = rows.last;
        if ((lastRow.first.y - item.y).abs() < 16) {
          lastRow.add(item);
        } else {
          rows.add([item]);
        }
      }
    }

    final combinedTexts = <String>[];
    for (final row in rows) {
      row.sort((a, b) => a.x.compareTo(b.x));
      final mergedRow = <String>[];
      var i = 0;
      while (i < row.length) {
        var current = row[i];
        var currentText = current.text.trim();
        while (i + 1 < row.length) {
          final next = row[i + 1];
          final dx = next.x - current.x;
          final sameGroup = current.groupKey.isNotEmpty &&
              current.groupKey == next.groupKey;
          final isShortMarker = RegExp(
            r'^(?:[①②③④⑤⑥⑦⑧⑨⑩]|\d+[.)]?|\([1-9]\)|\([가-힣]\)|[ㄱ-ㅎ가-힣][.)]?)$',
          ).hasMatch(currentText);
          final isOperator = RegExp(r'^[+\-×÷/*=<>≤≥]$').hasMatch(currentText);

          if (sameGroup ||
              (isShortMarker && dx > 0 && dx < 220) ||
              (isOperator && dx > 0 && dx < 80) ||
              (dx > 0 && dx < 50)) {
            currentText = '$currentText ${next.text.trim()}';
            current = (
              x: next.x,
              y: next.y,
              text: currentText,
              groupKey: next.groupKey.isNotEmpty ? next.groupKey : current.groupKey,
            );
            i++;
          } else {
            break;
          }
        }
        mergedRow.add(currentText);
        i++;
      }
      combinedTexts.addAll(mergedRow);
    }

    final inline = _extractInlineChoices(combinedTexts);
    return inline ?? _ensureChoiceMarkers(combinedTexts);
  }

  List<String> _choicesFromRenderer() {
    final elements = renderer['elements'];
    if (elements is! List) {
      return const [];
    }
    final choices = <({double x, double y, String text, String groupKey})>[];
    for (final element in elements.whereType<Map<String, dynamic>>()) {
      final identity = [
        element['id'],
        element['source_ref'],
        _mapAt(element, 'refs')['layout_slot_id'],
        _mapAt(element, 'metadata')['layout_slot_id'],
      ].whereType<Object>().join(' ').toLowerCase();

      final attributes = _mapAt(element, 'attributes');
      final semanticRole =
          attributes['data-semantic-role']?.toString().toLowerCase() ?? '';

      final text = sanitizeProblemText(element['text']?.toString() ?? '');
      if (text.isEmpty) {
        continue;
      }

      final isChoiceIdentifier = identity.contains('slot.choice') ||
          identity.contains('slot.opt') ||
          identity.contains('slot.c1') ||
          identity.contains('slot.c2') ||
          identity.contains('slot.c3') ||
          identity.contains('slot.c4') ||
          identity.contains('slot.c5') ||
          identity.contains('slot.option') ||
          identity.contains('slot.item') ||
          identity.contains('choice_label') ||
          identity.contains('symbol_label') ||
          semanticRole == 'symbol_label' ||
          semanticRole == 'choice_marker' ||
          semanticRole == 'choice' ||
          semanticRole == 'option';

      final isCircledOrNumbered = RegExp(
        r'^(?:[①②③④⑤⑥⑦⑧⑨⑩]|\([1-9]\)|\([가-힣]\)|[1-9]\.)',
      ).hasMatch(text.trim());

      final isExcluded = identity.contains('instruction') ||
          identity.contains('stem') ||
          identity.contains('qtext') ||
          identity.contains('question') ||
          identity.contains('slot.q.') ||
          identity.contains('slot.expr') ||
          identity.contains('slot.top') ||
          identity.contains('slot.hl') ||
          identity.contains('slot.p1') ||
          identity.contains('slot.p2') ||
          identity.contains('slot.p3') ||
          identity.contains('slot.f');

      if ((isChoiceIdentifier || isCircledOrNumbered) && !isExcluded) {
        final groupKey = _extractChoiceGroupKey(identity);
        choices.add((
          x: _numberValue(attributes['x']) ?? 0,
          y: _numberValue(attributes['y']) ?? 0,
          text: text,
          groupKey: groupKey,
        ));
      }
    }
    choices.sort((a, b) {
      final row = (a.y - b.y).abs() < 16 ? 0 : a.y.compareTo(b.y);
      return row != 0 ? row : a.x.compareTo(b.x);
    });

    final rows = <List<({double x, double y, String text, String groupKey})>>[];
    for (final item in choices) {
      if (rows.isEmpty) {
        rows.add([item]);
      } else {
        final lastRow = rows.last;
        if ((lastRow.first.y - item.y).abs() < 16) {
          lastRow.add(item);
        } else {
          rows.add([item]);
        }
      }
    }

    final combinedTexts = <String>[];
    for (final row in rows) {
      row.sort((a, b) => a.x.compareTo(b.x));
      final mergedRow = <String>[];
      var i = 0;
      while (i < row.length) {
        var current = row[i];
        var currentText = current.text.trim();
        while (i + 1 < row.length) {
          final next = row[i + 1];
          final dx = next.x - current.x;
          final sameGroup = current.groupKey.isNotEmpty &&
              current.groupKey == next.groupKey;
          final isShortMarker = RegExp(
            r'^(?:[①②③④⑤⑥⑦⑧⑨⑩]|\d+[.)]?|\([1-9]\)|\([가-힣]\)|[ㄱ-ㅎ가-힣][.)]?)$',
          ).hasMatch(currentText);
          final isOperator = RegExp(r'^[+\-×÷/*=<>≤≥]$').hasMatch(currentText);

          if (sameGroup ||
              (isShortMarker && dx > 0 && dx < 220) ||
              (isOperator && dx > 0 && dx < 80) ||
              (dx > 0 && dx < 50)) {
            currentText = '$currentText ${next.text.trim()}';
            current = (
              x: next.x,
              y: next.y,
              text: currentText,
              groupKey: next.groupKey.isNotEmpty ? next.groupKey : current.groupKey,
            );
            i++;
          } else {
            break;
          }
        }
        mergedRow.add(currentText);
        i++;
      }
      combinedTexts.addAll(mergedRow);
    }

    final inline = _extractInlineChoices(combinedTexts);
    return inline ?? _ensureChoiceMarkers(combinedTexts);
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

  List<String> _choicesFromSolvableGiven() {
    final given = solvable['given'];
    if (given is! List || given.isEmpty) {
      return const [];
    }
    final choices = <String>[];
    for (final item in given) {
      if (item is! Map<String, dynamic>) continue;
      final ref = item['ref']?.toString().toLowerCase() ?? '';
      final value = item['value'];

      if (value is Map<String, dynamic>) {
        final expr = value['expression']?.toString() ??
            value['text']?.toString() ??
            value['label']?.toString() ??
            value['name']?.toString();
        if (expr != null && expr.isNotEmpty) {
          choices.add(sanitizeProblemText(expr.trim()));
        }
      } else if (value is String && value.isNotEmpty) {
        if (ref.contains('person') ||
            ref.contains('option') ||
            ref.contains('choice') ||
            ref.contains('item') ||
            ref.contains('division') ||
            ref.contains('expr') ||
            ref.contains('candidate')) {
          choices.add(sanitizeProblemText(value.trim()));
        }
      }
    }
    return choices;
  }
}

double? _numberValue(Object? value) {
  if (value is num) {
    return value.toDouble();
  }
  return double.tryParse(value?.toString() ?? '');
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

List<String> _mergeAlternatingMarkerChoices(List<String> list) {
  if (list.length < 4 || list.length.isOdd) {
    return list;
  }
  var allEvensAreMarkers = true;
  for (var i = 0; i < list.length; i += 2) {
    final text = list[i].trim();
    final isMarker = RegExp(
      r'^(?:[①②③④⑤⑥⑦⑧⑨⑩]|\d+[.)]?|\([1-9]\)|\([가-힣]\)|[가-힣][.)]?)$',
    ).hasMatch(text);
    if (!isMarker) {
      allEvensAreMarkers = false;
      break;
    }
  }
  if (!allEvensAreMarkers) {
    return list;
  }
  final merged = <String>[];
  for (var i = 0; i < list.length; i += 2) {
    merged.add('${list[i].trim()} ${list[i + 1].trim()}');
  }
  return merged;
}

String _extractChoiceGroupKey(String identity) {
  final match = RegExp(
    r'(slot\.(?:choice[_\.]?\d+|opt[_\.]?\d+|c\d+|option[_\.]?\d+|item[_\.]?\d+))',
  ).firstMatch(identity);
  return match?.group(1) ?? '';
}

List<String> _ensureChoiceMarkers(List<String> choices) {
  if (choices.isEmpty) return choices;
  final markerPattern = RegExp(
    r'^(?:[①②③④⑤⑥⑦⑧⑨⑩]|\d+[.)]|\([1-9]\)|\([가-힣]\)|\([ㄱ-ㅎ]\)|[ㄱ-ㅎ가-힣][.)])',
  );
  final alreadyHasMarkers =
      choices.every((c) => markerPattern.hasMatch(c.trim()));

  if (alreadyHasMarkers) {
    return choices;
  }

  final noneHasMarkers = !choices.any((c) => markerPattern.hasMatch(c.trim()));

  if (noneHasMarkers && choices.length <= 10) {
    return choices.indexed
        .map((entry) => '${entry.$1 + 1}. ${entry.$2}')
        .toList();
  }

  return choices;
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
