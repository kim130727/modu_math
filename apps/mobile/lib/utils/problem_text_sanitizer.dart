String sanitizeProblemText(String value) {
  return value
      .replaceAll('\u3260', '가.')
      .replaceAll('\u3261', '나.')
      .replaceAll('\u3262', '다.')
      .replaceAll('\u3263', '라.')
      .replaceAll('\u3264', '마.')
      .replaceAll('\u3265', '바.')
      .replaceAll('\u3266', '사.')
      .replaceAll('\u3267', '아.')
      .replaceAll('\u320E', '가.')
      .replaceAll('\u320F', '나.')
      .replaceAll('\u3210', '다.')
      .replaceAll('\u3211', '라.')
      .replaceAll('\u3212', '마.')
      .replaceAll('\u3213', '바.')
      .replaceAll('\u2610', '')
      .replaceAll('\u25A1', '')
      .replaceAll('\u2460', '1.')
      .replaceAll('\u2461', '2.')
      .replaceAll('\u2462', '3.')
      .replaceAll('\u2463', '4.')
      .replaceAll('\u2464', '5.')
      .replaceAll('\u2465', '6.')
      .replaceAll('\u2466', '7.')
      .replaceAll('\u2467', '8.')
      .replaceAll('\u2468', '9.')
      .replaceAll('\u3131', '\uAC00')
      .replaceAll('\u3134', '\uB098')
      .replaceAll('\u3137', '\uB2E4')
      .replaceAll('\u3139', '\uB77C')
      .replaceAll('\u3141', '\uB9C8')
      .replaceAll('\u3142', '\uBC14')
      .replaceAll('\u3145', '\uC0AC')
      .replaceAll('\u3147', '\uC544')
      .replaceAll('\u3148', '\uC790')
      .replaceAll('\u314A', '\uCC28')
      .replaceAll('\u314B', '\uCE74')
      .replaceAll('\u314C', '\uD0C0')
      .replaceAll('\u314D', '\uD30C')
      .replaceAll('\u314E', '\uD558');
}

String sanitizeProblemSvg(String value) {
  return _wrapLongSvgText(sanitizeProblemText(value));
}

String _wrapLongSvgText(String svg) {
  final textPattern = RegExp(
    r'(<text\b[^>]*\bmax_width="([0-9.]+)"[^>]*\bfont-size="([0-9.]+)"[^>]*>)([^<]+)(</text>)',
  );
  return svg.replaceAllMapped(textPattern, (match) {
    final start = match.group(1)!;
    final maxWidth = double.tryParse(match.group(2)!) ?? 0;
    final fontSize = double.tryParse(match.group(3)!) ?? 0;
    final text = match.group(4)!.trim();
    final end = match.group(5)!;
    if (maxWidth <= 0 || fontSize <= 0 || text.isEmpty) {
      return match.group(0)!;
    }

    final lines = _wrapText(text, maxWidth, fontSize);
    if (lines.length <= 1) {
      return match.group(0)!;
    }

    final x = RegExp(r'\bx="([^"]+)"').firstMatch(start)?.group(1) ?? '0';
    final y = RegExp(r'\by="([^"]+)"').firstMatch(start)?.group(1) ?? '0';
    final lineHeight = (fontSize * 1.25).toStringAsFixed(1);
    final buffer = StringBuffer(start);
    for (var index = 0; index < lines.length; index += 1) {
      buffer.write(
        '<tspan x="$x" ${index == 0 ? 'y="$y"' : 'dy="$lineHeight"'}>${lines[index]}</tspan>',
      );
    }
    buffer.write(end);
    return buffer.toString();
  });
}

List<String> _wrapText(String text, double maxWidth, double fontSize) {
  final maxChars = (maxWidth / (fontSize * 0.62)).floor().clamp(8, 80);
  final words = text.split(RegExp(r'\s+')).where((word) => word.isNotEmpty);
  final lines = <String>[];
  var current = '';

  for (final word in words) {
    if (word.length > maxChars) {
      if (current.isNotEmpty) {
        lines.add(current);
        current = '';
      }
      for (var start = 0; start < word.length; start += maxChars) {
        final end = (start + maxChars).clamp(0, word.length);
        lines.add(word.substring(start, end));
      }
      continue;
    }

    final candidate = current.isEmpty ? word : '$current $word';
    if (candidate.length > maxChars && current.isNotEmpty) {
      lines.add(current);
      current = word;
    } else {
      current = candidate;
    }
  }

  if (current.isNotEmpty) {
    lines.add(current);
  }
  return lines;
}
