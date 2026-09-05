import 'package:flutter/material.dart';

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

  bool get _isMultiplicationPlaceValue {
    final type = content.summary.type.toLowerCase();
    final problemType = (content.semantic['problem_type'] ?? '').toString().toLowerCase();
    final title = content.summary.title;
    return type.contains('multiplication_place_value') ||
        problemType.contains('multiplication_place_value') ||
        (title.contains('색칠한 부분') && title.contains('곱인지')) ||
        content.summary.id.contains('008540');
  }

  @override
  Widget build(BuildContext context) {
    if (_isMultiplicationPlaceValue) {
      return _buildDecomposedMultiplication(context);
    }
    return _buildStandardExplorer(context);
  }

  Widget _buildDecomposedMultiplication(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(22),
        border: Border.all(color: const Color(0xFFE2E8F0)),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.04),
            blurRadius: 18,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Padding(
        padding: const EdgeInsets.all(22),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            _buildExplorerHeader(
              icon: Icons.calculate_rounded,
              title: '869 × 4 세로셈 분해 탐험대',
              subtitle: '세로셈 계산 과정에서 각 줄이 어떻게 만들어졌는지 살펴보세요.',
              badgeText: 'Grid View',
            ),
            const SizedBox(height: 18),
            Expanded(
              child: Container(
                decoration: BoxDecoration(
                  color: const Color(0xFFF8FAFF),
                  borderRadius: BorderRadius.circular(18),
                  border: Border.all(color: const Color(0xFFE0E7FF)),
                ),
                padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
                child: Center(
                  child: SingleChildScrollView(
                    child: ConstrainedBox(
                      constraints: const BoxConstraints(maxWidth: 420),
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          _buildPlaceValueHeader(),
                          const SizedBox(height: 8),
                          _buildCalculationBoard(),
                          const SizedBox(height: 20),
                          _buildStepCards(),
                        ],
                      ),
                    ),
                  ),
                ),
              ),
            ),
            const SizedBox(height: 14),
            _buildHintNote(
              '오른쪽 보기에서 분홍색 박스 240을 만드는 원래 식을 골라보세요!',
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildPlaceValueHeader() {
    return const Padding(
      padding: EdgeInsets.only(right: 120),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.end,
        children: [
          SizedBox(
            width: 38,
            child: Text(
              '백',
              textAlign: TextAlign.center,
              style: TextStyle(
                color: Color(0xFF6366F1),
                fontSize: 13,
                fontWeight: FontWeight.w700,
              ),
            ),
          ),
          SizedBox(width: 8),
          SizedBox(
            width: 38,
            child: Text(
              '십',
              textAlign: TextAlign.center,
              style: TextStyle(
                color: Color(0xFF6366F1),
                fontSize: 13,
                fontWeight: FontWeight.w700,
              ),
            ),
          ),
          SizedBox(width: 8),
          SizedBox(
            width: 38,
            child: Text(
              '일',
              textAlign: TextAlign.center,
              style: TextStyle(
                color: Color(0xFF6366F1),
                fontSize: 13,
                fontWeight: FontWeight.w700,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildCalculationBoard() {
    return Column(
      children: [
        // Row 1: 8 6 9
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const SizedBox(width: 44),
            _digitCell('8', isBold: true),
            const SizedBox(width: 8),
            _digitCell('6', isBold: true, color: const Color(0xFF4F46E5), isHighlighted: true),
            const SizedBox(width: 8),
            _digitCell('9', isBold: true),
            const SizedBox(width: 120),
          ],
        ),
        const SizedBox(height: 6),
        // Row 2: × 4
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const SizedBox(
              width: 44,
              child: Text(
                '×',
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 22,
                  fontWeight: FontWeight.w700,
                  color: Color(0xFF64748B),
                ),
              ),
            ),
            const SizedBox(width: 38),
            const SizedBox(width: 8),
            const SizedBox(width: 38),
            const SizedBox(width: 8),
            _digitCell('4', isBold: true, color: const Color(0xFF4F46E5), isHighlighted: true),
            const SizedBox(width: 120),
          ],
        ),
        const SizedBox(height: 8),
        Container(
          width: 340,
          height: 2,
          color: const Color(0xFF1E293B),
        ),
        const SizedBox(height: 10),
        // Row 3: 36 (9 × 4)
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const SizedBox(width: 44),
            const SizedBox(width: 38),
            const SizedBox(width: 8),
            _digitCell('3', isBold: true),
            const SizedBox(width: 8),
            _digitCell('6', isBold: true),
            const SizedBox(width: 12),
            const SizedBox(
              width: 108,
              child: Text(
                '(9 × 4)',
                style: TextStyle(
                  color: Color(0xFF64748B),
                  fontSize: 13,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ),
          ],
        ),
        const SizedBox(height: 8),
        // Row 4: 240 (Target! Highlighted in pink box with badge)
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
          decoration: BoxDecoration(
            color: const Color(0xFFFFE4E8),
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: const Color(0xFFFDA4AF), width: 1.5),
          ),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              const SizedBox(width: 24),
              _digitCell('2', isBold: true, color: const Color(0xFFE11D48)),
              const SizedBox(width: 8),
              _digitCell('4', isBold: true, color: const Color(0xFFE11D48)),
              const SizedBox(width: 8),
              _digitCell('0', isBold: true, color: const Color(0xFFE11D48)),
              const SizedBox(width: 14),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                decoration: BoxDecoration(
                  color: const Color(0xFFE11D48),
                  borderRadius: BorderRadius.circular(6),
                ),
                child: const Text(
                  '★ 정답 탐색!',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 11,
                    fontWeight: FontWeight.w800,
                  ),
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 8),
        // Row 5: 3 2 0 0 (800 × 4)
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            _digitCell('3', isBold: true),
            const SizedBox(width: 8),
            _digitCell('2', isBold: true),
            const SizedBox(width: 8),
            _digitCell('0', isBold: true),
            const SizedBox(width: 8),
            _digitCell('0', isBold: true),
            const SizedBox(width: 12),
            const SizedBox(
              width: 108,
              child: Text(
                '(800 × 4)',
                style: TextStyle(
                  color: Color(0xFF64748B),
                  fontSize: 13,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ),
          ],
        ),
        const SizedBox(height: 8),
        Container(
          width: 340,
          height: 2,
          color: const Color(0xFF1E293B),
        ),
        const SizedBox(height: 10),
        // Row 6: 3 4 7 6 종합 완료!
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            _digitCell('3', isBold: true),
            const SizedBox(width: 8),
            _digitCell('4', isBold: true),
            const SizedBox(width: 8),
            _digitCell('7', isBold: true),
            const SizedBox(width: 8),
            _digitCell('6', isBold: true),
            const SizedBox(width: 12),
            const SizedBox(
              width: 108,
              child: Text(
                '종합 완료!',
                style: TextStyle(
                  color: Color(0xFF059669),
                  fontSize: 13,
                  fontWeight: FontWeight.w800,
                ),
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _digitCell(
    String digit, {
    bool isBold = false,
    Color color = const Color(0xFF1E293B),
    bool isHighlighted = false,
  }) {
    return Container(
      width: 38,
      height: 38,
      alignment: Alignment.center,
      decoration: isHighlighted
          ? BoxDecoration(
              color: const Color(0xFFEEF2FF),
              borderRadius: BorderRadius.circular(8),
            )
          : null,
      child: Text(
        digit,
        style: TextStyle(
          fontSize: 24,
          fontWeight: isBold ? FontWeight.w800 : FontWeight.w600,
          color: color,
        ),
      ),
    );
  }

  Widget _buildStepCards() {
    return Row(
      children: [
        Expanded(
          child: _stepCard(
            title: '1단계 · 일의 자리',
            equation: '9 × 4 = 36',
            isActive: false,
          ),
        ),
        const SizedBox(width: 10),
        Expanded(
          child: _stepCard(
            title: '2단계 · 십의 자리',
            equation: '? × 4 = 240',
            isActive: true,
          ),
        ),
        const SizedBox(width: 10),
        Expanded(
          child: _stepCard(
            title: '3단계 · 백의 자리',
            equation: '800 × 4 = 3200',
            isActive: false,
          ),
        ),
      ],
    );
  }

  Widget _stepCard({
    required String title,
    required String equation,
    required bool isActive,
  }) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 12),
      decoration: BoxDecoration(
        color: isActive ? const Color(0xFFFFF1F2) : Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: isActive ? const Color(0xFFFDA4AF) : const Color(0xFFE2E8F0),
          width: isActive ? 1.5 : 1.0,
        ),
      ),
      child: Column(
        children: [
          Text(
            title,
            style: TextStyle(
              fontSize: 11,
              fontWeight: FontWeight.w700,
              color: isActive ? const Color(0xFFE11D48) : const Color(0xFF64748B),
            ),
          ),
          const SizedBox(height: 4),
          Text(
            equation,
            style: TextStyle(
              fontSize: 13,
              fontWeight: FontWeight.w800,
              color: isActive ? const Color(0xFFE11D48) : const Color(0xFF1E293B),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildStandardExplorer(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(22),
        border: Border.all(color: const Color(0xFFE2E8F0)),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.04),
            blurRadius: 18,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Padding(
        padding: const EdgeInsets.all(22),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            _buildExplorerHeader(
              icon: Icons.explore_rounded,
              title: '${content.summary.unitTopic} 개념 탐험대',
              subtitle: '주어진 그림과 조건을 꼼꼼히 살펴보고 문제를 해결해 보세요.',
              badgeText: content.renderer.isNotEmpty ? 'Canvas View' : 'Visual View',
            ),
            const SizedBox(height: 18),
            Expanded(
              child: Container(
                decoration: BoxDecoration(
                  color: const Color(0xFFF8FAFF),
                  borderRadius: BorderRadius.circular(18),
                  border: Border.all(color: const Color(0xFFE0E7FF)),
                ),
                padding: const EdgeInsets.all(16),
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
                          : const Text(
                              '시각 자료가 준비되지 않은 문제입니다.',
                              style: TextStyle(color: Color(0xFF64748B)),
                            )),
                ),
              ),
            ),
            const SizedBox(height: 14),
            _buildHintNote(
              '오른쪽 보기에서 문제의 조건에 알맞은 정답을 찾아보세요!',
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildExplorerHeader({
    required IconData icon,
    required String title,
    required String subtitle,
    required String badgeText,
  }) {
    return Row(
      children: [
        Container(
          width: 36,
          height: 36,
          decoration: BoxDecoration(
            color: const Color(0xFFEEF2FF),
            borderRadius: BorderRadius.circular(10),
          ),
          child: Icon(icon, size: 20, color: const Color(0xFF4F46E5)),
        ),
        const SizedBox(width: 12),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style: const TextStyle(
                  fontSize: 17,
                  fontWeight: FontWeight.w800,
                  color: Color(0xFF0F172A),
                ),
              ),
              const SizedBox(height: 2),
              Text(
                subtitle,
                style: const TextStyle(
                  fontSize: 12,
                  color: Color(0xFF64748B),
                ),
              ),
            ],
          ),
        ),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
          decoration: BoxDecoration(
            color: const Color(0xFFF1F5F9),
            borderRadius: BorderRadius.circular(8),
            border: Border.all(color: const Color(0xFFE2E8F0)),
          ),
          child: Text(
            badgeText,
            style: const TextStyle(
              fontSize: 11,
              fontFamily: 'monospace',
              fontWeight: FontWeight.w700,
              color: Color(0xFF475569),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildHintNote(String text) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
      decoration: BoxDecoration(
        color: const Color(0xFFF0FDF4),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: const Color(0xFFBBF7D0)),
      ),
      child: Row(
        children: [
          const Icon(Icons.check_circle_rounded, size: 16, color: Color(0xFF16A34A)),
          const SizedBox(width: 8),
          const Text(
            '힌트 노트:',
            style: TextStyle(
              fontSize: 13,
              fontWeight: FontWeight.w800,
              color: Color(0xFF15803D),
            ),
          ),
          const SizedBox(width: 6),
          Expanded(
            child: Text(
              text,
              style: const TextStyle(
                fontSize: 13,
                color: Color(0xFF166534),
                fontWeight: FontWeight.w600,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
