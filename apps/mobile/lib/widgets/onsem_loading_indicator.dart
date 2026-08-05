import 'package:flutter/material.dart';

const _onsemRunFrames = [
  'assets/characters/onsem_run_0.png',
  'assets/characters/onsem_run_1.png',
  'assets/characters/onsem_run_2.png',
  'assets/characters/onsem_run_3.png',
  'assets/characters/onsem_run_4.png',
  'assets/characters/onsem_run_5.png',
];

class OnsemLoadingIndicator extends StatefulWidget {
  const OnsemLoadingIndicator({
    super.key,
    this.label = '문제를 준비하고 있어요',
  });

  final String label;

  @override
  State<OnsemLoadingIndicator> createState() => _OnsemLoadingIndicatorState();
}

class _OnsemLoadingIndicatorState extends State<OnsemLoadingIndicator>
    with SingleTickerProviderStateMixin {
  late final AnimationController controller;

  @override
  void initState() {
    super.initState();
    controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 720),
    )..repeat();
  }

  @override
  void dispose() {
    controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;
    return Center(
      child: AnimatedBuilder(
        animation: controller,
        builder: (context, _) {
          final frameIndex =
              (controller.value * _onsemRunFrames.length).floor() %
                  _onsemRunFrames.length;
          return Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              SizedBox(
                width: 96,
                height: 96,
                child: Image.asset(
                  _onsemRunFrames[frameIndex],
                  gaplessPlayback: true,
                  semanticLabel: '온셈이',
                ),
              ),
              const SizedBox(height: 10),
              Text(
                widget.label,
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                      color: colorScheme.onSurfaceVariant,
                      fontWeight: FontWeight.w700,
                    ),
              ),
            ],
          );
        },
      ),
    );
  }
}
