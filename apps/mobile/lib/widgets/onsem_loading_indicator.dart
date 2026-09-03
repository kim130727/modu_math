import 'package:flutter/material.dart';

import '../l10n/app_strings.dart';

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
    this.label,
    this.labelKey,
  });

  final String? label;
  final String? labelKey;

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

  String _resolveLabel(BuildContext context) {
    final activeLocale =
        AppLocaleScope.maybeOf(context)?.locale ?? const Locale('ko');
    final strings = AppStrings.forLocale(activeLocale, context: context);

    if (widget.labelKey != null && widget.labelKey!.isNotEmpty) {
      return strings.t(widget.labelKey!);
    }

    final raw = widget.label;
    if (raw == null || raw.trim().isEmpty) {
      return strings.t('loading.default');
    }

    if (raw.contains('.') && strings.hasKey(raw)) {
      return strings.t(raw);
    }

    if (activeLocale.languageCode != 'ko') {
      final mapped = switch (raw.trim()) {
        '오늘의 문제를 고르고 있어요' => strings.t('home.loading'),
        '단원을 준비하고 있어요' => strings.t('curriculum.loading'),
        '학습 세션을 준비하고 있어요' => strings.t('session.loading'),
        '문제를 불러오고 있어요' || '문제를 준비하고 있어요' => strings.t('problem.loading'),
        '문제 목록을 모으고 있어요' => strings.t('problemList.loading'),
        '노트를 살펴보고 있어요' => strings.t('review.loading'),
        '학습 리포트를 정리하고 있어요' => strings.t('report.loading'),
        '미리보기를 준비하고 있어요' => strings.t('studio.loading'),
        '추천 문제를 준비하고 있어요.' || '추천 문제를 준비하고 있어요' =>
          strings.t('home.recommendationLoading'),
        _ => null,
      };
      if (mapped != null) {
        return mapped;
      }
    }

    return raw;
  }

  @override
  Widget build(BuildContext context) {
    final activeLocale =
        AppLocaleScope.maybeOf(context)?.locale ?? const Locale('ko');
    final strings = AppStrings.forLocale(activeLocale, context: context);
    final colorScheme = Theme.of(context).colorScheme;
    final displayLabel = _resolveLabel(context);
    final semanticLabel = strings.t('tutor.title');

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
                  semanticLabel: semanticLabel,
                ),
              ),
              const SizedBox(height: 10),
              Text(
                displayLabel,
                textAlign: TextAlign.center,
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
