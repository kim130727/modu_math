import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';

import '../utils/problem_text_sanitizer.dart';

class ProblemSvgViewer extends StatelessWidget {
  const ProblemSvgViewer({super.key, required this.svg});

  final String svg;

  @override
  Widget build(BuildContext context) {
    final displaySvg = sanitizeProblemSvg(svg);
    final svgSize = _SvgSize.parse(svg);
    return Card(
      margin: EdgeInsets.zero,
      clipBehavior: Clip.antiAlias,
      child: ClipRRect(
        borderRadius: BorderRadius.circular(8),
        child: LayoutBuilder(
          builder: (context, constraints) {
            return Padding(
              padding: const EdgeInsets.all(18),
              child: InteractiveViewer(
                minScale: 0.6,
                maxScale: 4,
                boundaryMargin: const EdgeInsets.all(80),
                child: Center(
                  child: AspectRatio(
                    aspectRatio: svgSize.aspectRatio,
                    child: SvgPicture.string(displaySvg, fit: BoxFit.contain),
                  ),
                ),
              ),
            );
          },
        ),
      ),
    );
  }
}

class _SvgSize {
  const _SvgSize(this.width, this.height);

  final double width;
  final double height;

  double get aspectRatio {
    if (width <= 0 || height <= 0) {
      return 4 / 3;
    }
    return width / height;
  }

  static _SvgSize parse(String svg) {
    final viewBox = RegExp(r'\bviewBox="([^"]+)"').firstMatch(svg)?.group(1);
    if (viewBox != null) {
      final parts = viewBox
          .split(RegExp(r'[\s,]+'))
          .map(double.tryParse)
          .whereType<double>()
          .toList();
      if (parts.length == 4 && parts[2] > 0 && parts[3] > 0) {
        return _SvgSize(parts[2], parts[3]);
      }
    }

    final width = _readLength(svg, 'width');
    final height = _readLength(svg, 'height');
    if (width != null && height != null && width > 0 && height > 0) {
      return _SvgSize(width, height);
    }
    return const _SvgSize(4, 3);
  }

  static double? _readLength(String svg, String name) {
    final match = RegExp('\\b$name="([0-9.]+)').firstMatch(svg);
    return double.tryParse(match?.group(1) ?? '');
  }
}
