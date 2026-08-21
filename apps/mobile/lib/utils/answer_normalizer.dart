String _cleanText(String value) {
  var text = value
      .trim()
      .toLowerCase()
      .replaceAll(RegExp(r'\s+'), '')
      .replaceAll('\u00d7', '*')
      .replaceAll('\ud6de', '*')
      .replaceAll('x', '*')
      .replaceAll('\ubc88', '')
      .replaceAll(',', '')
      .replaceAll('.', '')
      .replaceAll('(', '')
      .replaceAll(')', '');

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

  return false;
}

String _stripLeadingChoiceMarker(String value) {
  final trimmed = value.trim();
  return trimmed.replaceFirst(
    RegExp(r'^(?:[①②③④⑤⑥⑦⑧⑨⑩]|\(\s*[1-9]\s*\)|\(\s*[ㄱ-ㅎ가-힣]\s*\)|\d+[.)]\s*|[ㄱ-ㅎ가-힣][.)]\s*)\s*'),
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
