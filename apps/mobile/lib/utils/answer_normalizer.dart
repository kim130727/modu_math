String _cleanText(String value) {
  var text = value
      .trim()
      .toLowerCase()
      .replaceAll(RegExp(r'\s+'), '')
      .replaceAll('○', 'o')
      .replaceAll('✕', 'x')
      .replaceAll('\u00d7', '*')
      .replaceAll('\ud6de', '*')
      .replaceAll('\ubc88', '')
      .replaceAll(',', '')
      .replaceAll('.', '')
      .replaceAll('(', '')
      .replaceAll(')', '');

  if (text == 'o표' || text == 'o') {
    return 'o';
  }
  if (text == 'x표' || text == 'x' || text == '*표' || text == '*') {
    return 'x';
  }

  text = text.replaceAll('x', '*');

  const replacements = {
    '\u2460': '1',
    '\u2461': '2',
    '\u2462': '3',
    '\u2463': '4',
    '\u2464': '5',
    '\u2465': '6',
    '\u2466': '7',
    '\u2467': '8',
    '\u2468': '9',
    '\u3260': '\u3131', // ㉠ -> ㄱ
    '\u3261': '\u3134', // ㉡ -> ㄴ
    '\u3262': '\u3137', // ㉢ -> ㄷ
    '\u3263': '\u3139', // ㉣ -> ㄹ
    '\u3264': '\u3141', // ㉤ -> ㅁ
    '\u3265': '\u3142', // ㉥ -> ㅂ
    '\u3266': '\u3145', // ㉦ -> ㅅ
    '\u3267': '\u3147', // ㉧ -> ㅇ
    '\u326E': '\uAC00', // ㉮ -> 가
    '\u326F': '\uB098', // ㉯ -> 나
    '\u3270': '\uB2E4', // ㉰ -> 다
    '\u3271': '\uB77C', // ㉱ -> 라
    '\u3272': '\uB9C8', // ㉲ -> 마
    '\u3273': '\uBC14', // ㉳ -> 바
    '\u3274': '\uC0AC', // ㉴ -> 사
    '\u3275': '\uC544', // ㉵ -> 아
  };

  for (final entry in replacements.entries) {
    text = text.replaceAll(entry.key, entry.value);
  }

  return text;
}

String normalizeAnswer(String value) {
  final clean = _cleanText(value);
  final leadingChoice = _leadingChoiceNumber(value);
  if (leadingChoice != null) {
    return leadingChoice;
  }
  return clean;
}

bool isSameAnswer(String submitted, String correct) {
  final cleanSub = _cleanText(submitted);
  final cleanCor = _cleanText(correct);
  if (cleanSub == cleanCor) {
    return true;
  }

  // 1) 한국어 맞춤법/어휘 변형 대응 ("그을" vs "그릴")
  if (cleanSub.replaceAll('그릴', '그을') == cleanCor.replaceAll('그릴', '그을')) {
    return true;
  }

  // 2) 앞 번호/기호 마커 제거 후 본문 텍스트 비교
  final withoutMarkerSub = _stripLeadingChoiceMarker(submitted);
  final withoutMarkerCor = _stripLeadingChoiceMarker(correct);
  final cleanWithoutSub = _cleanText(withoutMarkerSub);
  final cleanWithoutCor = _cleanText(withoutMarkerCor);

  if (cleanWithoutSub.isNotEmpty &&
      (cleanWithoutSub == cleanCor ||
          cleanWithoutSub == cleanWithoutCor ||
          cleanWithoutSub.replaceAll('그릴', '그을') ==
              cleanWithoutCor.replaceAll('그릴', '그을') ||
          cleanWithoutSub.replaceAll('그릴', '그을') ==
              cleanCor.replaceAll('그릴', '그을'))) {
    return true;
  }

  // 3) 번호 마커 비교 (예: submitted="1. ~", correct="1" 또는 submitted="① ~", correct="1")
  final subMarker = _extractLeadingChoiceMarker(submitted);
  final corMarker = _extractLeadingChoiceMarker(correct);

  if (subMarker != null) {
    if (subMarker == cleanCor || (corMarker != null && subMarker == corMarker)) {
      return true;
    }
  }
  if (corMarker != null && corMarker == cleanSub) {
    return true;
  }

  // 4) 산술식 계산 결과와 비교 (예: submitted="752 × 3", correct="2256" 또는 submitted="2256", correct="752 × 3")
  final subCalc = _tryEvalSimpleArithmetic(cleanWithoutSub.isNotEmpty ? cleanWithoutSub : cleanSub);
  final corCalc = _tryEvalSimpleArithmetic(cleanWithoutCor.isNotEmpty ? cleanWithoutCor : cleanCor);
  if (subCalc != null && corCalc != null && subCalc == corCalc) {
    return true;
  }
  if (subCalc != null && (subCalc == cleanCor || subCalc == cleanWithoutCor)) {
    return true;
  }
  if (corCalc != null && (corCalc == cleanSub || corCalc == cleanWithoutSub)) {
    return true;
  }

  // 5) 용기/물체 접미사 및 한글 라벨 정규화 비교 (예: "가 병" vs "가", "가 물병" vs "가 병", "ㄱ" vs "가 병")
  final canonSub = _canonicalLabel(cleanWithoutSub.isNotEmpty ? cleanWithoutSub : cleanSub);
  final canonCor = _canonicalLabel(cleanWithoutCor.isNotEmpty ? cleanWithoutCor : cleanCor);
  if (canonSub.isNotEmpty && canonSub == canonCor) {
    return true;
  }

  // 6) 다중 입력 / 덧셈 항 순서 무관 비교 (예: "415 / 334" vs "334 / 415", "415334" vs "334415", "415, 334" vs "334415")
  if (_matchesUnorderedTokens(submitted, correct)) {
    return true;
  }

  // 7) 다중 선택형 보기 마커/내용 비교 (예: submitted="2. 565. 70" vs correct="25" 또는 "2 / 5")
  if (_matchesMultipleChoiceSelections(submitted, correct) ||
      _matchesMultipleChoiceSelections(correct, submitted)) {
    return true;
  }

  return false;
}

List<String> _extractMultiTokens(String value) {
  final trimmed = value.trim();
  if (RegExp(r'[/,;|\s]').hasMatch(trimmed)) {
    final parts = trimmed
        .split(RegExp(r'[/,;|\s]+'))
        .map(_cleanText)
        .where((p) => p.isNotEmpty)
        .toList();
    if (parts.length > 1) {
      return parts;
    }
  }
  return [];
}

bool _isPermutationConcatenation(List<String> tokens, String raw) {
  final totalLen = tokens.fold<int>(0, (sum, t) => sum + t.length);
  if (totalLen != raw.length) return false;

  bool helper(List<String> remaining, String currentRaw) {
    if (remaining.isEmpty) return currentRaw.isEmpty;
    for (var i = 0; i < remaining.length; i++) {
      final token = remaining[i];
      if (currentRaw.startsWith(token)) {
        final nextRemaining = List<String>.from(remaining)..removeAt(i);
        final nextRaw = currentRaw.substring(token.length);
        if (helper(nextRemaining, nextRaw)) return true;
      }
    }
    return false;
  }

  return helper(tokens, raw);
}

bool _matchesUnorderedTokens(String submitted, String correct) {
  final subTokens = _extractMultiTokens(submitted);
  final corTokens = _extractMultiTokens(correct);

  // Both have delimiters (e.g. "415 / 334" vs "334 / 415" or "415, 334" vs "334, 415")
  if (subTokens.isNotEmpty && corTokens.isNotEmpty) {
    if (subTokens.length == corTokens.length) {
      final s = List<String>.from(subTokens)..sort();
      final c = List<String>.from(corTokens)..sort();
      if (_listsEqual(s, c)) return true;
    }
  }

  // submitted has delimiters, correct is concatenated (e.g. "415 / 334" vs "334415")
  if (subTokens.isNotEmpty && corTokens.isEmpty) {
    if (_isPermutationConcatenation(subTokens, _cleanText(correct))) {
      return true;
    }
  }

  // correct has delimiters, submitted is concatenated (e.g. "415334" vs "334 / 415")
  if (corTokens.isNotEmpty && subTokens.isEmpty) {
    if (_isPermutationConcatenation(corTokens, _cleanText(submitted))) {
      return true;
    }
  }

  // Both are raw concatenated strings (e.g. "415334" vs "334415")
  final cleanSub = _cleanText(submitted);
  final cleanCor = _cleanText(correct);
  if (cleanSub.length == cleanCor.length && cleanSub.length >= 4) {
    for (var chunkSize = 2; chunkSize <= cleanSub.length ~/ 2; chunkSize++) {
      if (cleanSub.length % chunkSize == 0) {
        final subChunks = _toChunks(cleanSub, chunkSize)..sort();
        final corChunks = _toChunks(cleanCor, chunkSize)..sort();
        if (_listsEqual(subChunks, corChunks)) {
          return true;
        }
      }
    }
  }

  return false;
}

class _ExtractedChoiceItem {
  final String marker;
  final String content;
  _ExtractedChoiceItem(this.marker, this.content);
}

List<_ExtractedChoiceItem> _extractMultipleChoiceTokens(String input) {
  final items = <_ExtractedChoiceItem>[];
  if (RegExp(r'[/,;|\n]').hasMatch(input)) {
    final parts = input
        .split(RegExp(r'[/,;|\n]+'))
        .map((p) => p.trim())
        .where((p) => p.isNotEmpty);
    for (final part in parts) {
      final marker = _extractLeadingChoiceMarker(part);
      final body = _stripLeadingChoiceMarker(part);
      if (marker != null || body != part) {
        items.add(_ExtractedChoiceItem(marker ?? '', _cleanText(body)));
      }
    }
    if (items.length >= 2) return items;
  }

  final pattern = RegExp(
    r'(?:^|(?<=\S|\b))([①②③④⑤⑥⑦⑧⑨⑩㉠-㉭]|(?:\b|^)([1-9]|10)[.)]\s*|(?:\b|^)\(([1-9]|10|[ㄱ-ㅎ가-힣])\)\s*)([^\d\s①②③④⑤⑥⑦⑧⑨⑩㉠-㉭]+|\d+)?',
  );
  for (final match in pattern.allMatches(input)) {
    final fullMarker = match.group(1) ?? '';
    final marker =
        _extractLeadingChoiceMarker(fullMarker) ?? _cleanText(fullMarker);
    final content = _cleanText(match.group(4) ?? '');
    if (marker.isNotEmpty) {
      items.add(_ExtractedChoiceItem(marker, content));
    }
  }
  return items;
}

bool _matchesMultipleChoiceSelections(String submitted, String correct) {
  final items = _extractMultipleChoiceTokens(submitted);
  if (items.length < 2) return false;

  final markers = items.map((i) => i.marker).where((m) => m.isNotEmpty).toList();
  final contents = items.map((i) => i.content).where((c) => c.isNotEmpty).toList();
  final cleanCor = _cleanText(correct);
  final corTokens = _extractMultiTokens(correct);

  if (markers.isNotEmpty) {
    final joinedMarkers = markers.join();
    if (joinedMarkers == cleanCor ||
        _isPermutationConcatenation(markers, cleanCor)) {
      return true;
    }
    if (corTokens.isNotEmpty &&
        Set.from(markers).containsAll(corTokens) &&
        Set.from(corTokens).containsAll(markers)) {
      return true;
    }
  }

  if (contents.isNotEmpty) {
    final joinedContents = contents.join();
    if (joinedContents == cleanCor ||
        _isPermutationConcatenation(contents, cleanCor)) {
      return true;
    }
    if (corTokens.isNotEmpty &&
        Set.from(contents).containsAll(corTokens) &&
        Set.from(corTokens).containsAll(contents)) {
      return true;
    }
  }

  return false;
}

List<String> _toChunks(String s, int size) {
  final chunks = <String>[];
  for (var i = 0; i < s.length; i += size) {
    chunks.add(s.substring(i, i + size));
  }
  return chunks;
}

bool _listsEqual(List<String> a, List<String> b) {
  if (a.length != b.length) return false;
  for (var i = 0; i < a.length; i++) {
    if (a[i] != b[i]) return false;
  }
  return true;
}

String _stripContainerSuffix(String text) {
  var s = text.trim();
  const suffixes = ['물병', '주전자', '그릇', '상자', '도형', '병', '컵'];
  for (final suf in suffixes) {
    if (s.endsWith(suf) && s.length > suf.length) {
      s = s.substring(0, s.length - suf.length).trim();
      break;
    }
  }
  return s;
}

String _canonicalLabel(String text) {
  var s = _stripContainerSuffix(text);
  const map = {
    'ㄱ': '가',
    'ㄴ': '나',
    'ㄷ': '다',
    'ㄹ': '라',
    'ㅁ': '마',
  };
  return map[s] ?? s;
}

String? _tryEvalSimpleArithmetic(String expr) {
  final clean = expr.trim();
  final match = RegExp(r'^(\d+)\s*([\*\+\-\/])\s*(\d+)$').firstMatch(clean);
  if (match == null) return null;
  final a = int.tryParse(match.group(1)!);
  final op = match.group(2)!;
  final b = int.tryParse(match.group(3)!);
  if (a == null || b == null) return null;
  switch (op) {
    case '*':
      return (a * b).toString();
    case '+':
      return (a + b).toString();
    case '-':
      return (a - b).toString();
    case '/':
      return b != 0 ? (a ~/ b).toString() : null;
    default:
      return null;
  }
}

String _stripLeadingChoiceMarker(String value) {
  final trimmed = value.trim();
  return trimmed.replaceFirst(
    RegExp(r'^(?:[①②③④⑤⑥⑦⑧⑨⑩㉠-㉭]|\(\s*[1-9]\s*\)|\(\s*[ㄱ-ㅎ가-힣]\s*\)|\d+[.)]\s*|[ㄱ-ㅎ가-힣][.)]\s*)\s*'),
    '',
  );
}

String? _extractLeadingChoiceMarker(String value) {
  final trimmed = value.trim();
  if (trimmed.isEmpty) return null;

  const circled = {
    '\u2460': '1',
    '\u2461': '2',
    '\u2462': '3',
    '\u2463': '4',
    '\u2464': '5',
    '\u2465': '6',
    '\u2466': '7',
    '\u2467': '8',
    '\u2468': '9',
    '\u3260': '\u3131', // ㉠ -> ㄱ
    '\u3261': '\u3134', // ㉡ -> ㄴ
    '\u3262': '\u3137', // ㉢ -> ㄷ
    '\u3263': '\u3139', // ㉣ -> ㄹ
    '\u3264': '\u3141', // ㉤ -> ㅁ
    '\u3265': '\u3142', // ㉥ -> ㅂ
    '\u3266': '\u3145', // ㉦ -> ㅅ
    '\u3267': '\u3147', // ㉧ -> ㅇ
    '\u326E': '\uAC00', // ㉮ -> 가
    '\u326F': '\uB098', // ㉯ -> 나
    '\u3270': '\uB2E4', // ㉰ -> 다
    '\u3271': '\uB77C', // ㉱ -> 라
    '\u3272': '\uB9C8', // ㉲ -> 마
  };

  final first = trimmed.substring(0, 1);
  if (circled.containsKey(first)) {
    return circled[first];
  }

  final marked = RegExp(r'^(\d+|[ㄱ-ㅎ가-힣])[.)]').firstMatch(trimmed);
  if (marked != null) {
    return marked.group(1);
  }

  final parenthesized = RegExp(r'^\(([0-9ㄱ-ㅎ가-힣])\)').firstMatch(trimmed);
  if (parenthesized != null) {
    return parenthesized.group(1);
  }

  return null;
}

String? _leadingChoiceNumber(String value) {
  final trimmed = value.trim();
  if (trimmed.isEmpty) {
    return null;
  }

  const circled = {
    '\u2460': '1',
    '\u2461': '2',
    '\u2462': '3',
    '\u2463': '4',
    '\u2464': '5',
    '\u2465': '6',
    '\u2466': '7',
    '\u2467': '8',
    '\u2468': '9',
    '\u3260': '\u3131',
    '\u3261': '\u3134',
    '\u3262': '\u3137',
    '\u3263': '\u3139',
    '\u3264': '\u3141',
    '\u3265': '\u3142',
    '\u3266': '\u3145',
    '\u3267': '\u3147',
    '\u326E': '\uAC00',
    '\u326F': '\uB098',
    '\u3270': '\uB2E4',
    '\u3271': '\uB77C',
    '\u3272': '\uB9C8',
  };

  final first = trimmed.substring(0, 1);
  if (circled.containsKey(first) && trimmed.length == 1) {
    return circled[first];
  }

  final bare = RegExp(r'^(?:[1-9]|[ㄱ-ㅎ]|[가-힣])$').firstMatch(trimmed);
  if (bare != null) {
    return bare.group(0);
  }

  final parenthesized = RegExp(r'^\(([0-9ㄱ-ㅎ가-힣])\)$').firstMatch(trimmed);
  if (parenthesized != null) {
    return parenthesized.group(1);
  }

  final marked = RegExp(r'^([0-9ㄱ-ㅎ가-힣])[.)]$').firstMatch(trimmed);
  if (marked != null) {
    return marked.group(1);
  }

  return null;
}

