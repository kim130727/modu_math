String normalizeAnswer(String value) {
  var compact = value
      .trim()
      .toLowerCase()
      .replaceAll(RegExp(r'\s+'), '')
      .replaceAll('○', 'o')
      .replaceAll('✕', 'x')
      .replaceAll('\u00d7', '*')
      .replaceAll('\ud6de', '*')
      .replaceAll('\ubc88', '')
      .replaceAll(',', '');

  if (compact == 'o표' || compact == 'o') {
    return 'o';
  }
  if (compact == 'x표' || compact == 'x' || compact == '*표' || compact == '*') {
    return 'x';
  }

  compact = compact.replaceAll('x', '*');

  final leadingChoice = _leadingChoiceNumber(compact);
  if (leadingChoice != null) {
    return leadingChoice;
  }

  return compact;
}

bool isSameAnswer(String submitted, String correct) {
  final normSubmitted = normalizeAnswer(submitted);
  final normCorrect = normalizeAnswer(correct);
  if (normSubmitted == normCorrect) {
    return true;
  }
  final withoutMarker = submitted.replaceFirst(
    RegExp(r'^(?:[①②③④⑤⑥⑦⑧⑨⑩㉠-㉭]|\d+[.)]?|\([1-9]\)|\([가-힣]\)|\([ㄱ-ㅎ]\)|[ㄱ-ㅎ가-힣][.)]?)\s*'),
    '',
  );
  if (withoutMarker != submitted) {
    if (normalizeAnswer(withoutMarker) == normCorrect) {
      return true;
    }
  }
  return false;
}

String? _leadingChoiceNumber(String value) {
  if (value.isEmpty) {
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

  final first = value.substring(0, 1);
  if (circled.containsKey(first)) {
    return circled[first];
  }

  final bare = RegExp(r'^(?:[1-9]|[ㄱ-ㅎ]|[가-힣])$').firstMatch(value);
  if (bare != null) {
    return bare.group(0);
  }

  final parenthesized = RegExp(r'^\((.+?)\)').firstMatch(value);
  if (parenthesized != null) {
    return parenthesized.group(1);
  }

  final marked = RegExp(r'^([0-9ㄱ-ㅎ가-힣])[.)]').firstMatch(value);
  return marked?.group(1);
}
