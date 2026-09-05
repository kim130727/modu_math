import 'package:flutter/material.dart';

import '../l10n/app_strings.dart';
import '../models/content_models.dart';
import '../services/content_repository.dart';
import 'problem_svg_viewer.dart';
import 'renderer_json_canvas.dart';

class VerticalArithmeticExplorer extends StatelessWidget {
  const VerticalArithmeticExplorer({
    super.key,
    required this.repository,
    required this.content,
    required this.answerDraft,
    required this.onAnswerChanged,
  });

  final ContentRepository repository;
  final ProblemContent content;
  final String answerDraft;
  final ValueChanged<String> onAnswerChanged;

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(18),
        border: Border.all(color: const Color(0xFFE2E8F0)),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.04),
            blurRadius: 14,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Padding(
        padding: const EdgeInsets.fromLTRB(14, 10, 14, 10),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            _buildExplorerHeader(
              icon: Icons.explore_rounded,
              title: strings.t('explorer.standardTitle', {'topic': strings.unitTitle(content.summary.unitTopic)}),
              badgeText: content.renderer.isNotEmpty ? 'Canvas' : 'Visual',
            ),
            const SizedBox(height: 8),
            Expanded(
              child: Container(
                decoration: BoxDecoration(
                  color: const Color(0xFFF8FAFC),
                  borderRadius: BorderRadius.circular(14),
                  border: Border.all(color: const Color(0xFFE2E8F0)),
                ),
                clipBehavior: Clip.antiAlias,
                padding: const EdgeInsets.all(4),
                child: Center(
                  child: content.renderer.isNotEmpty
                      ? RendererJsonCanvas(
                          renderer: content.renderer,
                          imageLoader: (href) =>
                              repository.loadProblemAsset(content.summary, href),
                          imageCacheKey: content.summary.path,
                          inputValue: answerDraft,
                          expectedAnswer: content.correctAnswer,
                          suppressInputs: content.choices.isNotEmpty,
                          onInputChanged: onAnswerChanged,
                        )
                      : (content.svg.isNotEmpty
                          ? ProblemSvgViewer(svg: content.svg)
                          : Text(
                              strings.t('problem.noVisual'),
                              style: const TextStyle(color: Color(0xFF64748B)),
                            )),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildExplorerHeader({
    required IconData icon,
    required String title,
    String? subtitle,
    required String badgeText,
  }) {
    return Row(
      children: [
        Container(
          width: 32,
          height: 32,
          decoration: BoxDecoration(
            color: const Color(0xFFEEF2FF),
            borderRadius: BorderRadius.circular(8),
          ),
          child: Icon(icon, size: 18, color: const Color(0xFF4F46E5)),
        ),
        const SizedBox(width: 10),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                title,
                style: const TextStyle(
                  fontSize: 15,
                  fontWeight: FontWeight.w800,
                  color: Color(0xFF0F172A),
                ),
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
              ),
              if (subtitle != null && subtitle.isNotEmpty) ...[
                const SizedBox(height: 2),
                Text(
                  subtitle,
                  style: const TextStyle(
                    fontSize: 11,
                    color: Color(0xFF64748B),
                  ),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
              ],
            ],
          ),
        ),
        const SizedBox(width: 8),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
          decoration: BoxDecoration(
            color: const Color(0xFFEEF2FF),
            borderRadius: BorderRadius.circular(6),
            border: Border.all(color: const Color(0xFFC7D2FE)),
          ),
          child: Text(
            badgeText,
            style: const TextStyle(
              fontSize: 11,
              fontFamily: 'monospace',
              fontWeight: FontWeight.w700,
              color: Color(0xFF4338CA),
            ),
          ),
        ),
      ],
    );
  }
}

