String normalizeAnswer(String value) {
  final compact = value
      .trim()
      .toLowerCase()
      .replaceAll(RegExp(r'\s+'), '')
      .replaceAll('×', '*')
      .replaceAll('횞', '*')
      .replaceAll('x', '*')
      .replaceAll('번', '')
      .replaceAll(',', '');

  final leadingChoice = _leadingChoiceNumber(compact);
  if (leadingChoice != null) {
    return leadingChoice;
  }

  return compact
      .replaceAll('가', 'ㄱ')
      .replaceAll('나', 'ㄴ')
      .replaceAll('다', 'ㄷ')
      .replaceAll('라', 'ㄹ')
      .replaceAll('마', 'ㅁ')
      .replaceAll('바', 'ㅂ')
      .replaceAll('사', 'ㅅ');
}

bool isSameAnswer(String submitted, String correct) {
  return normalizeAnswer(submitted) == normalizeAnswer(correct);
}

String? _leadingChoiceNumber(String value) {
  if (value.isEmpty) {
    return null;
  }

  const circled = {
    '①': '1',
    '②': '2',
    '③': '3',
    '④': '4',
    '⑤': '5',
    '⑥': '6',
    '⑦': '7',
    '⑧': '8',
    '⑨': '9',
  };

  final first = value.substring(0, 1);
  if (circled.containsKey(first)) {
    return circled[first];
  }

  final match = RegExp(r'^[1-9]$').firstMatch(value);
  return match?.group(0);
}
