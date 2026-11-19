import 'dart:math' as math;

import 'package:flutter/material.dart';

import 'renderer_json_canvas.dart';

/// Size the presentation around its fitted artwork, rather than reserving a
/// fixed-height canvas for every question. Authored coordinates stay intact.
class ProblemCanvas extends StatelessWidget {
  const ProblemCanvas({super.key, required this.renderer});

  final Map<String, dynamic> renderer;

  @override
  Widget build(BuildContext context) => Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 960),
          child: LayoutBuilder(builder: (context, constraints) {
            final viewport = renderer['presentation_viewport'];
            final box = viewport is Map ? viewport : renderer['view_box'];
            double dimension(String name, double fallback) {
              final value = box is Map ? box[name] : null;
              return value is num && value.isFinite && value > 0
                  ? value.toDouble()
                  : fallback;
            }

            final width = dimension('width', 928);
            final height = dimension('height', 426);
            final availableWidth =
                constraints.maxWidth.isFinite ? constraints.maxWidth : width;
            final displayHeight =
                (availableWidth * height / width).clamp(96.0, 420.0);
            return SizedBox(
              width: math.min(960, availableWidth),
              height: displayHeight,
              child: RendererJsonCanvas(
                renderer: renderer,
                suppressInputs: true,
              ),
            );
          }),
        ),
      );
}
