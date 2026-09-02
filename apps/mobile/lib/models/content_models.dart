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
  String get subUnit {
    final candidate = raw['subUnit']?.toString() ??
        raw['subTopic']?.toString() ??
        raw['topic']?.toString();
    if (candidate != null && candidate.trim().isNotEmpty) {
      return candidate.trim();
    }
    return '기본 학습';
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

  List<ChoiceGroup> get choiceGroups {
    final answer = answerMap;
    final rawGroups = answer['choice_groups'];
    if (rawGroups is List && rawGroups.isNotEmpty) {
      return rawGroups
          .map((group) {
            if (group is Map<String, dynamic>) {
              final label = group['label']?.toString() ?? '';
              final rawChoices = group['choices'];
              final choices = rawChoices is List
                  ? rawChoices
                      .map((c) => sanitizeProblemText(c.toString()))
                      .toList()
                  : <String>[];
              return ChoiceGroup(label: label, choices: choices);
            } else if (group is List) {
              final choices =
                  group.map((c) => sanitizeProblemText(c.toString())).toList();
              return ChoiceGroup(label: '', choices: choices);
            }
            return const ChoiceGroup(label: '', choices: []);
          })
          .where((g) => g.choices.isNotEmpty)
          .toList();
    }
    return const [];
  }

  List<String> get choices {
    if (choiceGroups.isNotEmpty) {
      return choiceGroups.expand((g) => g.choices).toList();
    }
    if (_isComparisonOperatorProblem) {
      return const ['>', '=', '<'];
    }
    final answer = answerMap;
    final explicitChoices = answer['choices'];
    if (explicitChoices is List && explicitChoices.isNotEmpty) {
      final list = explicitChoices.map(_choiceText).toList();
      return _sortChoicesByLeadingMarker(
        _mergeAlternatingMarkerChoices(list),
      );
    }
    if (_isNumberedOptionChoiceProblem) {
      return _numberedOptionChoices;
    }
    if (hasRendererAnswerInputs) {
      return const [];
    }
    final answerType = answer['type']?.toString().toLowerCase() ?? '';
    if (answerType == 'numeric' || answerType == 'multi_numeric') {
      return const [];
    }
    final rawOptions = answer['options'] ??
        (answerType == 'choice' ? _mapAt(solvable, 'inputs')['options'] : null);
    if (rawOptions is List && rawOptions.isNotEmpty) {
      final list = rawOptions.map(_choiceText).toList();
      return _sortChoicesByLeadingMarker(
        _ensureChoiceMarkers(
          _mergeAlternatingMarkerChoices(list),
        ),
      );
    }
    if (_isOxJudgmentProblem) {
      return const ['O', 'X'];
    }
    if (_isPersonChoiceProblem) {
      final givenChoices = _choicesFromSolvableGiven();
      if (givenChoices.isNotEmpty) {
        return _ensureChoiceMarkers(
            _mergeAlternatingMarkerChoices(givenChoices));
      }
    }
    final rendererChoices = _choicesFromRenderer();
    if (rendererChoices.isNotEmpty) {
      return _sortChoicesByLeadingMarker(
        _ensureChoiceMarkers(
          _mergeAlternatingMarkerChoices(rendererChoices),
        ),
      );
    }
    final svgChoices = _choicesFromSvg();
    if (svgChoices.isNotEmpty) {
      return _sortChoicesByLeadingMarker(
        _ensureChoiceMarkers(_mergeAlternatingMarkerChoices(svgChoices)),
      );
    }
    final givenChoices = _choicesFromSolvableGiven();
    if (givenChoices.isNotEmpty) {
      return _sortChoicesByLeadingMarker(
        _ensureChoiceMarkers(_mergeAlternatingMarkerChoices(givenChoices)),
      );
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
    if (choiceGroups.isNotEmpty) {
      final value = answer['value'];
      if (value is String && value.isNotEmpty) {
        return sanitizeProblemText(value);
      }
      final key = answer['answer_key'];
      if (key is List && key.isNotEmpty) {
        return key
            .map(_answerValueText)
            .map(sanitizeProblemText)
            .where((v) => v.isNotEmpty)
            .join(', ');
      }
    }
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
          RegExp(r'(?:^|[._])c[1-5](?:[._]|$)').hasMatch(id);

      final isCircledOrNumbered = RegExp(
        r'^(?:[①②③④⑤⑥⑦⑧⑨⑩㉠-㉭]|\([1-9]\)|\([가-힣]\)|\([ㄱ-ㅎ]\)|[1-9]\.)',
      ).hasMatch(text);

      if (text.contains('<보기>') || text.contains('< 보기 >')) continue;
      if (!isChoice && !isCircledOrNumbered) continue;
      if (id.contains('question') ||
          id.contains('stem') ||
          id.contains('instruction') ||
          id.contains('given') ||
          id.contains('example') ||
          id.contains('options') ||
          id.contains('card') ||
          id.contains('result')) {
        continue;
      }

      final xMatch = RegExp(r'x="([0-9.-]+)"').firstMatch(attrs);
      final yMatch = RegExp(r'y="([0-9.-]+)"').firstMatch(attrs);
      final x = double.tryParse(xMatch?.group(1) ?? '') ?? 0;
      final y = double.tryParse(yMatch?.group(1) ?? '') ?? 0;

      final groupKey = _extractChoiceGroupKey(id);
      rawItems.add((x: x, y: y, text: text, groupKey: groupKey));
    }

    final rectPattern = RegExp(r'<rect\b([^>]*)/?>');
    final rectMatches = rectPattern.allMatches(svg);
    for (final match in rectMatches) {
      final attrs = match.group(1) ?? '';
      final idMatch = RegExp(r'id="([^"]+)"').firstMatch(attrs);
      final id = idMatch?.group(1)?.toLowerCase() ?? '';
      final isChoiceBlank = (id.contains('choice') ||
              id.contains('opt') ||
              id.contains('option')) &&
          (id.contains('blank') || id.contains('box'));
      if (!isChoiceBlank) continue;
      final widthMatch = RegExp(r'width="([0-9.-]+)"').firstMatch(attrs);
      final heightMatch = RegExp(r'height="([0-9.-]+)"').firstMatch(attrs);
      final width = double.tryParse(widthMatch?.group(1) ?? '') ?? 0;
      final height = double.tryParse(heightMatch?.group(1) ?? '') ?? 0;
      if (width <= 0 || width > 60 || height <= 0 || height > 60) continue;
      final xMatch = RegExp(r'x="([0-9.-]+)"').firstMatch(attrs);
      final yMatch = RegExp(r'y="([0-9.-]+)"').firstMatch(attrs);
      final x = double.tryParse(xMatch?.group(1) ?? '') ?? 0;
      final y = double.tryParse(yMatch?.group(1) ?? '') ?? 0;
      final groupKey = _extractChoiceGroupKey(id);
      rawItems.add((x: x, y: y, text: '□', groupKey: groupKey));
    }

    if (rawItems.isEmpty) return const [];

    rawItems.sort((a, b) {
      final row = (a.y - b.y).abs() < 36 ? 0 : a.y.compareTo(b.y);
      return row != 0 ? row : a.x.compareTo(b.x);
    });

    final rows = <List<({double x, double y, String text, String groupKey})>>[];
    for (final item in rawItems) {
      if (rows.isEmpty) {
        rows.add([item]);
      } else {
        final lastRow = rows.last;
        if ((lastRow.first.y - item.y).abs() < 36) {
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
          final sameGroup =
              current.groupKey.isNotEmpty && current.groupKey == next.groupKey;
          final isShortMarker = RegExp(
            r'^(?:[①②③④⑤⑥⑦⑧⑨⑩㉠-㉭]|\d+[.)]?|\([1-9]\)|\([가-힣]\)|\([ㄱ-ㅎ]\)|[ㄱ-ㅎ가-힣][.)]?)$',
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
              groupKey:
                  next.groupKey.isNotEmpty ? next.groupKey : current.groupKey,
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
      final type = element['type']?.toString().toLowerCase() ?? '';

      var text = sanitizeProblemText(element['text']?.toString() ?? '');
      if (text.isEmpty && type == 'rect') {
        final isChoiceBlank = (identity.contains('choice') ||
                identity.contains('opt') ||
                identity.contains('option')) &&
            (identity.contains('blank') ||
                identity.contains('box') ||
                semanticRole == 'blank' ||
                semanticRole == 'answer_blank');
        final width = _numberValue(attributes['width']) ?? 0;
        final height = _numberValue(attributes['height']) ?? 0;
        if (isChoiceBlank &&
            width > 0 &&
            width <= 60 &&
            height > 0 &&
            height <= 60) {
          text = '□';
        }
      }
      if (text.isEmpty) {
        continue;
      }

      final isChoiceIdentifier = identity.contains('slot.choice') ||
          (_isPersonChoiceProblem &&
              (identity.contains('slot.name') ||
                  identity.contains('person_name') ||
                  identity.contains('name.text'))) ||
          RegExp(r'slot\.c[1-5](?:[._]|$)').hasMatch(identity) ||
          RegExp(r'slot\.(?:choice|opt|option|v|item)[_.]?\d+')
              .hasMatch(identity) ||
          identity.contains('choice_label') ||
          identity.contains('symbol_label') ||
          semanticRole == 'symbol_label' ||
          semanticRole == 'choice_marker' ||
          semanticRole == 'choice' ||
          semanticRole == 'option';

      final isPersonName = identity.contains('name') ||
          identity.contains('person') ||
          semanticRole.contains('name');

      if (_isPersonChoiceProblem && !isPersonName) {
        continue;
      }

      final isCircledOrNumbered = RegExp(
        r'^(?:[①②③④⑤⑥⑦⑧⑨⑩㉠-㉭]|\([1-9]\)|\([가-힣]\)|\([ㄱ-ㅎ]\)|[1-9]\.|[ㄱ-ㅎ가-힣]\.)',
      ).hasMatch(text.trim());

      final isExcluded = identity.contains('instruction') ||
          identity.contains('stem') ||
          identity.contains('qtext') ||
          identity.contains('question') ||
          identity.contains('given') ||
          identity.contains('example') ||
          identity.contains('options') ||
          identity.contains('card') ||
          text.contains('<보기>') ||
          text.contains('< 보기 >') ||
          semanticRole == 'card' ||
          semanticRole == 'given_value' ||
          semanticRole == 'example_label' ||
          semanticRole == 'example_result' ||
          semanticRole == 'example_container' ||
          semanticRole == 'addition_rule_diagram' ||
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
      final row = (a.y - b.y).abs() < 36 ? 0 : a.y.compareTo(b.y);
      return row != 0 ? row : a.x.compareTo(b.x);
    });

    final rows = <List<({double x, double y, String text, String groupKey})>>[];
    for (final item in choices) {
      if (rows.isEmpty) {
        rows.add([item]);
      } else {
        final lastRow = rows.last;
        if ((lastRow.first.y - item.y).abs() < 36) {
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
          final sameGroup =
              current.groupKey.isNotEmpty && current.groupKey == next.groupKey;
          final isShortMarker = RegExp(
            r'^(?:[①②③④⑤⑥⑦⑧⑨⑩㉠-㉭]|\d+[.)]?|\([1-9]\)|\([가-힣]\)|\([ㄱ-ㅎ]\)|[ㄱ-ㅎ가-힣][.)]?)$',
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
              groupKey:
                  next.groupKey.isNotEmpty ? next.groupKey : current.groupKey,
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

  bool get _isChoiceProblem {
    final type = summary.type.toLowerCase();
    final semanticType =
        semantic['problem_type']?.toString().toLowerCase() ?? '';
    final solvableType =
        solvable['problem_type']?.toString().toLowerCase() ?? '';
    final targetType =
        _mapAt(solvable, 'target')['type']?.toString().toLowerCase() ?? '';
    return type.contains('choice') ||
        type.contains('selection') ||
        type.contains('ordering') ||
        semanticType.contains('choice') ||
        semanticType.contains('selection') ||
        semanticType.contains('ordering') ||
        solvableType.contains('choice') ||
        solvableType.contains('selection') ||
        solvableType.contains('ordering') ||
        targetType.contains('choice') ||
        targetType.contains('selection') ||
        targetType.contains('candidate');
  }

  bool get _isPersonChoiceProblem {
    final targetType =
        _mapAt(solvable, 'target')['type']?.toString().toLowerCase() ?? '';
    final targetDesc =
        _mapAt(solvable, 'target')['description']?.toString().toLowerCase() ??
            '';
    final problemType =
        solvable['problem_type']?.toString().toLowerCase() ?? '';
    final semanticType =
        semantic['problem_type']?.toString().toLowerCase() ?? '';
    final promptText = prompt.toLowerCase();
    final titleText = summary.title.toLowerCase();
    return targetType.contains('person') ||
        targetDesc.contains('사람') ||
        problemType.contains('person') ||
        semanticType.contains('person') ||
        promptText.contains('사람') ||
        titleText.contains('사람');
  }

  bool get _isOxJudgmentProblem {
    final targetType =
        _mapAt(solvable, 'target')['type']?.toString().toLowerCase() ?? '';
    final targetDesc =
        _mapAt(solvable, 'target')['description']?.toString().toLowerCase() ??
            '';
    final problemType =
        solvable['problem_type']?.toString().toLowerCase() ?? '';
    final semanticType =
        semantic['problem_type']?.toString().toLowerCase() ?? '';
    final promptText = prompt.toLowerCase();
    final titleText = summary.title.toLowerCase();
    final answerVal = correctAnswer.toLowerCase().trim();

    final isOxTarget = targetType.contains('ox') ||
        targetType.contains('boolean') ||
        targetType.contains('judgment') ||
        targetDesc.contains('ox') ||
        targetDesc.contains('o표') ||
        targetDesc.contains('x표') ||
        targetDesc.contains('o/x') ||
        targetDesc.contains('o, x') ||
        targetDesc.contains('o 또는 x');

    final isOxProblemType = problemType.contains('judgment') ||
        problemType.contains('ox') ||
        problemType.contains('boolean') ||
        semanticType.contains('judgment') ||
        semanticType.contains('ox');

    final isOxPrompt = promptText.contains('o표') ||
        promptText.contains('x표') ||
        promptText.contains('o, x') ||
        promptText.contains('o / x') ||
        promptText.contains('o 또는 x') ||
        titleText.contains('o표') ||
        titleText.contains('x표') ||
        titleText.contains('o, x') ||
        titleText.contains('o / x') ||
        titleText.contains('o 또는 x');

    final isOxAnswer = answerVal == 'o' ||
        answerVal == 'x' ||
        answerVal == 'o표' ||
        answerVal == 'x표' ||
        answerVal == '○' ||
        answerVal == '✕';

    return (isOxTarget || isOxProblemType || isOxPrompt) &&
        (isOxAnswer || isOxPrompt);
  }

  bool get _isComparisonOperatorProblem {
    final answer = answerMap;
    final value = answer['value'];
    if (value == '>' ||
        value == '<' ||
        value == '=' ||
        (value is List &&
            value.length == 1 &&
            (value.first == '>' || value.first == '<' || value.first == '='))) {
      return true;
    }
    final answerType = answer['type']?.toString().toLowerCase() ?? '';
    if (answerType == 'comparison_operator') {
      return true;
    }
    final metadataMap = _mapAt(semantic, 'metadata');
    final question = (metadataMap['question'] ?? prompt).toString();
    if (question.contains('○') &&
        (question.contains('>') ||
            question.contains('<') ||
            question.contains('='))) {
      return true;
    }
    final problemType =
        (semantic['problem_type'] ?? '').toString().toLowerCase();
    if (problemType.contains('comparison') || problemType.contains('compare')) {
      final correct = correctAnswer.trim();
      if (correct == '>' || correct == '<' || correct == '=') {
        return true;
      }
    }
    return false;
  }

  bool get _isNumberedOptionChoiceProblem {
    final answer = answerMap;
    final targetLabel =
        (_mapAt(solvable, 'inputs')['target_label'] ?? '').toString();
    final targetType =
        (_mapAt(solvable, 'target')['type'] ?? '').toString().toLowerCase();
    final value = answer['value'];
    final isIntVal = value is int ||
        (value is String &&
            int.tryParse(value) != null &&
            int.parse(value) >= 1 &&
            int.parse(value) <= 10);

    if (targetLabel.contains('번호') ||
        targetType == 'choice_number' ||
        targetType == 'choice_order') {
      return true;
    }
    if (targetType == 'choice' && isIntVal) {
      return true;
    }
    return false;
  }

  List<String> get _numberedOptionChoices {
    final rawOptions = answerMap['options'] ??
        (_mapAt(solvable, 'inputs')['options']);
    int count = 5;
    if (rawOptions is List && rawOptions.isNotEmpty) {
      count = rawOptions.length;
    } else {
      final domainObjects = _mapAt(semantic, 'domain')['objects'];
      if (domainObjects is List && domainObjects.isNotEmpty) {
        final choiceObjs = domainObjects
            .where((obj) =>
                obj is Map &&
                obj['id']?.toString().contains('choice') == true)
            .toList();
        if (choiceObjs.isNotEmpty) count = choiceObjs.length;
      }
    }
    const markers = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩'];
    return markers.take(count.clamp(2, 10)).toList();
  }

  bool get hasRendererAnswerInputs {
    final elements = renderer['elements'];
    if (elements is! List) return false;
    for (final element in elements.whereType<Map<String, dynamic>>()) {
      final interaction = _mapAt(element, 'interaction');
      final role = interaction['role']?.toString().toLowerCase();
      if (role == 'answer') return true;
      final type = element['type']?.toString();
      if (type == 'rect' && interaction['type']?.toString() == 'input') {
        return true;
      }
    }
    return false;
  }

  bool get hasMultipleRendererAnswerInputs {
    final answerMap = this.answerMap;
    final answerKey = answerMap['answer_key'];
    if (answerKey is List && answerKey.length >= 2) {
      return true;
    }
    final elements = renderer['elements'];
    if (elements is! List) return false;
    int count = 0;
    for (final element in elements.whereType<Map<String, dynamic>>()) {
      final interaction = _mapAt(element, 'interaction');
      final role = interaction['role']?.toString().toLowerCase();
      final type = element['type']?.toString();
      if (role == 'answer' ||
          (type == 'rect' && interaction['type']?.toString() == 'input')) {
        count++;
      }
    }
    return count >= 2;
  }

  List<AnswerInputField> get multiAnswerFields {
    if (hasRendererAnswerInputs || choices.isNotEmpty) return const [];

    final answer = answerMap;
    final answerValues = answer['values'];
    final unknowns =
        _mapAt(solvable, 'inputs')['unknowns'] ?? solvable['unknowns'];

    if (answerValues is List && answerValues.length >= 2) {
      final fields = <AnswerInputField>[];
      for (var i = 0; i < answerValues.length; i++) {
        final valEntry = answerValues[i];
        final unit =
            (valEntry is Map ? valEntry['unit'] : null)?.toString() ?? '';
        final targetRef =
            (valEntry is Map ? valEntry['target_ref'] : null)?.toString() ?? '';

        String label = '';
        if (unknowns is List) {
          for (final unk in unknowns) {
            if (unk is Map && (unk['ref'] == targetRef)) {
              label = unk['label']?.toString() ?? '';
              break;
            }
          }
        }
        if (label.isEmpty) {
          label = '문제 (${i + 1})';
        }
        fields.add(AnswerInputField(
          id: 'field_$i',
          label: label,
          unit: unit,
        ));
      }
      return fields;
    }

    if (unknowns is List && unknowns.length >= 2) {
      final fields = <AnswerInputField>[];
      for (var i = 0; i < unknowns.length; i++) {
        final unk = unknowns[i];
        if (unk is Map) {
          fields.add(AnswerInputField(
            id: 'field_$i',
            label: unk['label']?.toString() ?? '문제 (${i + 1})',
            unit: unk['unit']?.toString() ?? '',
          ));
        }
      }
      return fields;
    }

    final val = answer['value'];
    if (val is List && val.length >= 2) {
      return val.indexed.map((entry) {
        return AnswerInputField(
          id: 'field_${entry.$1}',
          label: '문제 (${entry.$1 + 1})',
        );
      }).toList();
    }

    return const [];
  }

  List<String> _choicesFromSolvableGiven() {
    final given = solvable['given'];
    if (given is! List || given.isEmpty) {
      return const [];
    }

    final answer = answerMap;
    final blanks = answer['blanks'];
    if (blanks is List && blanks.isNotEmpty) {
      return const [];
    }
    if (hasRendererAnswerInputs && !_isChoiceProblem) {
      return const [];
    }

    final choices = <String>[];
    for (final item in given) {
      if (item is! Map<String, dynamic>) continue;
      final ref = item['ref']?.toString().toLowerCase() ?? '';
      final value = item['value'];

      final isChoiceRef = ref.contains('choice') ||
          ref.contains('option') ||
          ref.contains('opt') ||
          ref.contains('div') ||
          ref.contains('expr') ||
          ref.contains('candidate') ||
          ref.contains('person') ||
          ref.contains('speaker') ||
          ref.contains('name');

      final isPersonRef = ref.contains('person') ||
          ref.contains('speaker') ||
          ref.contains('name');

      if (_isPersonChoiceProblem && !isPersonRef) {
        continue;
      }

      if (!isChoiceRef && !_isChoiceProblem && !_isPersonChoiceProblem) {
        continue;
      }

      if (value is Map<String, dynamic>) {
        final expr = value['expression']?.toString();
        if (expr != null && expr.trim().isNotEmpty) {
          choices.add(sanitizeProblemText(expr.trim()));
        }
      } else if (value is String &&
          value.trim().isNotEmpty &&
          (isChoiceRef || _isPersonChoiceProblem)) {
        choices.add(sanitizeProblemText(value.trim()));
      }
    }
    return choices;
  }
}

String _choiceText(Object? choice) {
  if (choice is! Map) {
    return sanitizeProblemText(choice?.toString() ?? '');
  }

  final text = choice['text']?.toString().trim() ?? '';
  final label = choice['label']?.toString().trim() ?? '';
  final expression = choice['expression']?.toString().trim() ?? '';
  final number = choice['number']?.toString().trim() ?? '';
  final value = choice['value']?.toString().trim() ?? '';

  final mainText = text.isNotEmpty
      ? text
      : expression.isNotEmpty
          ? expression
          : value.isNotEmpty
              ? value
              : '';

  final marker = label.isNotEmpty
      ? label
      : number.isNotEmpty
          ? number
          : '';

  if (mainText.isNotEmpty) {
    final trimmedMain = mainText.trim();
    bool alreadyHasMarker = false;
    if (marker.isNotEmpty) {
      if (trimmedMain == marker) {
        alreadyHasMarker = true;
      } else if (RegExp(r'^[0-9]+$').hasMatch(marker)) {
        alreadyHasMarker = trimmedMain.startsWith('$marker.') ||
            trimmedMain.startsWith('$marker)') ||
            trimmedMain.startsWith('($marker)') ||
            trimmedMain.startsWith('$marker ');
      } else if (RegExp(r'^[①②③④⑤⑥⑦⑧⑨⑩㉠-㉭]$').hasMatch(marker)) {
        alreadyHasMarker = trimmedMain.startsWith(marker);
      } else if (RegExp(r'^\([1-9]\)$').hasMatch(marker)) {
        alreadyHasMarker = trimmedMain.startsWith(marker);
      } else {
        alreadyHasMarker = trimmedMain.startsWith('$marker.') ||
            trimmedMain.startsWith('$marker)') ||
            trimmedMain.startsWith('($marker)') ||
            trimmedMain.startsWith('$marker ');
      }
    }

    if (marker.isNotEmpty &&
        !alreadyHasMarker &&
        marker.toLowerCase() != 'choices') {
      if (RegExp(r'^[0-9]+$').hasMatch(marker)) {
        return sanitizeProblemText('$marker. $mainText');
      } else if (RegExp(r'^[①②③④⑤⑥⑦⑧⑨⑩㉠-㉭]$').hasMatch(marker)) {
        return sanitizeProblemText('$marker $mainText');
      } else if (RegExp(r'^\([1-9]\)$').hasMatch(marker)) {
        return sanitizeProblemText('$marker $mainText');
      } else {
        return sanitizeProblemText('$marker. $mainText');
      }
    }
    return sanitizeProblemText(mainText);
  }

  if (marker.isNotEmpty) {
    return sanitizeProblemText(marker);
  }

  if (value.isNotEmpty) {
    return sanitizeProblemText(value);
  }

  return sanitizeProblemText(choice.toString());
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
  final markerPattern = RegExp(
    r'^(?:[①②③④⑤⑥⑦⑧⑨⑩㉠-㉭]|\d+[.)]?|\([1-9]\)|\([가-힣]\)|\([ㄱ-ㅎ]\)|[ㄱ-ㅎ가-힣][.)]?)$',
  );
  var allEvensAreMarkers = true;
  for (var i = 0; i < list.length; i += 2) {
    final text = list[i].trim();
    if (!markerPattern.hasMatch(text)) {
      allEvensAreMarkers = false;
      break;
    }
  }
  if (!allEvensAreMarkers) {
    return list;
  }
  // A list such as [ㄱ, ㄴ, ㄷ, ㄹ] contains four complete symbolic choices.
  // Merge only when every odd item is actual choice content, not another
  // standalone marker.
  final oddsContainOnlyChoiceContent = list.indexed
      .where((entry) => entry.$1.isOdd)
      .every((entry) => !markerPattern.hasMatch(entry.$2.trim()));
  if (!oddsContainOnlyChoiceContent) {
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
    r'(slot\.(?:choice[_\.]?\d+|opt[_\.]?\d+|c\d+|v\d+|item\d+|option[_\.]?\d+))',
  ).firstMatch(identity);
  return match?.group(1) ?? '';
}

List<String> _ensureChoiceMarkers(List<String> choices) {
  if (choices.isEmpty) return choices;
  final markerPattern = RegExp(
    r'^(?:[①②③④⑤⑥⑦⑧⑨⑩㉠-㉭]|\d+[.)]|\([1-9]\)|\([가-힣]\)|\([ㄱ-ㅎ]\)|[ㄱ-ㅎ가-힣][.)])',
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

int? _extractLeadingMarkerNumber(String s) {
  final trimmed = s.trim();
  if (trimmed.isEmpty) return null;
  const circledMap = {
    '①': 1, '②': 2, '③': 3, '④': 4, '⑤': 5,
    '⑥': 6, '⑦': 7, '⑧': 8, '⑨': 9, '⑩': 10,
    '㉠': 1, '㉡': 2, '㉢': 3, '㉣': 4, '㉤': 5,
    '㉥': 6, '㉦': 7, '㉧': 8, '㉨': 9, '㉩': 10,
    '가': 1, '나': 2, '다': 3, '라': 4, '마': 5,
    '바': 6, '사': 7, '아': 8, '자': 9, '차': 10,
    'ㄱ': 1, 'ㄴ': 2, 'ㄷ': 3, 'ㄹ': 4, 'ㅁ': 5,
    'ㅂ': 6, 'ㅅ': 7, 'ㅇ': 8, 'ㅈ': 9, 'ㅊ': 10,
  };
  final firstChar = trimmed[0];
  if (circledMap.containsKey(firstChar)) {
    if (trimmed.length == 1 ||
        trimmed[1] == ' ' ||
        trimmed[1] == '.' ||
        trimmed[1] == ')') {
      return circledMap[firstChar];
    }
  }
  final match = RegExp(
    r'^(?:(?:\(([1-9]|10|[가-힣]|[ㄱ-ㅎ])\))|([1-9]|10)[.)]|([①②③④⑤⑥⑦⑧⑨⑩㉠-㉭]))',
  ).firstMatch(trimmed);
  if (match != null) {
    final numStr = match.group(2);
    if (numStr != null) {
      return int.tryParse(numStr);
    }
    final parenStr = match.group(1);
    if (parenStr != null) {
      if (circledMap.containsKey(parenStr)) return circledMap[parenStr];
      return int.tryParse(parenStr);
    }
    final cStr = match.group(3);
    if (cStr != null && circledMap.containsKey(cStr)) {
      return circledMap[cStr];
    }
  }
  return null;
}

List<String> _sortChoicesByLeadingMarker(List<String> choices) {
  if (choices.length < 2) return choices;
  final markers = choices.map(_extractLeadingMarkerNumber).toList();
  final nonNullMarkers = markers.whereType<int>().toList();
  if (nonNullMarkers.length == choices.length &&
      nonNullMarkers.toSet().length == choices.length) {
    final indexed = choices.indexed.toList();
    indexed.sort((a, b) => markers[a.$1]!.compareTo(markers[b.$1]!));
    return indexed.map((e) => e.$2).toList();
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
      value.contains('\uFFFD');
}

class ChoiceGroup {
  const ChoiceGroup({
    required this.label,
    required this.choices,
  });

  final String label;
  final List<String> choices;
}

class AnswerInputField {
  const AnswerInputField({
    required this.id,
    required this.label,
    this.unit = '',
    this.placeholder = '',
  });

  final String id;
  final String label;
  final String unit;
  final String placeholder;
}
