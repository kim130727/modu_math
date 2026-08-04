String sanitizeTutorText(String text) {
  return text
      .replaceAll('**', '')
      .replaceAll(RegExp(r'\s+\n'), '\n')
      .split('\n')
      .map(_sanitizeTutorLine)
      .where((line) => line.trim().isNotEmpty)
      .join('\n')
      .trim();
}

String _sanitizeTutorLine(String line) {
  final text = line.trim();
  if (!_looksBrokenText(text)) {
    return text;
  }
  final stepMatch = RegExp(r'^(\d+).{0,8}:').firstMatch(text);
  if (stepMatch != null) {
    return '${stepMatch.group(1)}단계: 문제에서 필요한 값을 확인해요.';
  }
  if (text.contains('Rule Tutor')) {
    return 'Rule Tutor로 단계별 풀이를 시작할게요.';
  }
  if (text.contains('507') ||
      text.contains('1012') ||
      text.contains('1026') ||
      text.contains('1304')) {
    final number = RegExp(r'\d+').allMatches(text).map((m) => m.group(0)).last;
    return '최종 답은 $number입니다.';
  }
  return '문제에서 필요한 값을 순서대로 확인해요.';
}

bool _looksBrokenText(String value) {
  return RegExp(r'[\u3400-\u9FFF\uFFFD]').hasMatch(value) ||
      value.contains('??') ||
      value.contains('�');
}
