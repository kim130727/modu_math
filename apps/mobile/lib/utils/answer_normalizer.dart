String normalizeAnswer(String value) {
  final compact = value
      .trim()
      .toLowerCase()
      .replaceAll(RegExp(r'\s+'), '')
      .replaceAll('\u00d7', '*')
      .replaceAll('\ud6de', '*')
      .replaceAll('x', '*')
      .replaceAll('\ubc88', '')
      .replaceAll(',', '');

  final leadingChoice = _leadingChoiceNumber(compact);
  if (leadingChoice != null) {
    return leadingChoice;
  }

  return compact
      .replaceAll('\uac00', '\u3131')
      .replaceAll('\ub098', '\u3134')
      .replaceAll('\ub2e4', '\u3137')
      .replaceAll('\ub77c', '\u3139')
      .replaceAll('\ub9c8', '\u3141')
      .replaceAll('\ubc14', '\u3142')
      .replaceAll('\uc0ac', '\u3145');
}

bool isSameAnswer(String submitted, String correct) {
  return normalizeAnswer(submitted) == normalizeAnswer(correct);
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
    '\u3260': '1',
    '\u3261': '2',
    '\u3262': '3',
    '\u3263': '4',
    '\u3264': '5',
  };

  final first = value.substring(0, 1);
  if (circled.containsKey(first)) {
    return circled[first];
  }

  final bare = RegExp(r'^[1-9]$').firstMatch(value);
  if (bare != null) {
    return bare.group(0);
  }

  final parenthesized = RegExp(r'^\(([1-9])\)').firstMatch(value);
  if (parenthesized != null) {
    return parenthesized.group(1);
  }

  final marked = RegExp(r'^([1-9])[.)]').firstMatch(value);
  return marked?.group(1);
}
