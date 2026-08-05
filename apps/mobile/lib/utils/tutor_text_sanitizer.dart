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
    return _naturalizeTutorLine(text);
  }
  final stepMatch = RegExp(r'^(\d+).{0,8}:').firstMatch(text);
  if (stepMatch != null) {
    return '${stepMatch.group(1)}단계: 문제에서 필요한 값을 확인해요.';
  }
  if (text.contains('Rule Tutor')) {
    return '온셈이와 함께 한 단계씩 풀어볼게요.';
  }
  final numberMatches = RegExp(r'\d+').allMatches(text).toList();
  if (numberMatches.isNotEmpty) {
    final number = numberMatches.last.group(0);
    return '정답은 $number이에요.';
  }
  return '문제에서 필요한 값을 차례대로 확인해요.';
}

String _naturalizeTutorLine(String text) {
  return text
      .replaceAll('Rule Tutor로 단계별 풀이를 시작할게요.', '온셈이와 함께 한 단계씩 풀어볼게요.')
      .replaceAll('Rule Tutor로', '온셈이와')
      .replaceAll('Rule Tutor', '온셈이')
      .replaceAll('풀이 방법:', '방법:')
      .replaceAll('좋아요. 최종 답이 맞아요.', '좋아요. 정확히 맞았어요.')
      .replaceAll('풀이 단계도 차근차근 잘 이어졌어요.', '다음 문제로 넘어가 볼까요?');
}

bool _looksBrokenText(String value) {
  return RegExp(r'[\u3400-\u9FFF\uFFFD]').hasMatch(value) ||
      value.contains('??') ||
      value.contains('占');
}
