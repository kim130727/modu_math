import 'package:flutter/material.dart';

import '../l10n/app_strings.dart';
import '../models/content_models.dart';
import '../services/auth_service.dart';
import '../services/content_repository.dart';
import '../services/diagnostics_service.dart';
import '../services/learning_progress_repository.dart';
import '../theme/app_theme.dart';
import '../widgets/onsem_loading_indicator.dart';
import 'auth_screen.dart';
import 'problem_solve_screen.dart';

class DiagnosticScreen extends StatefulWidget {
  const DiagnosticScreen({
    super.key,
    required this.authService,
    required this.diagnosticsService,
    required this.contentRepository,
    required this.progressRepository,
  });

  final AuthService authService;
  final DiagnosticsClientService diagnosticsService;
  final ContentRepository contentRepository;
  final LearningProgressRepository progressRepository;

  @override
  State<DiagnosticScreen> createState() => _DiagnosticScreenState();
}

class _DiagnosticScreenState extends State<DiagnosticScreen> {
  late Future<DiagnosticSummaryData?> _summaryFuture;
  late Future<List<DiagnosticTagMetric>> _conceptsFuture;
  late Future<List<DiagnosticTagMetric>> _skillsFuture;
  late Future<List<RecommendedProblemItem>> _recommendationsFuture;

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  void _loadData() {
    _summaryFuture = widget.diagnosticsService.fetchSummary();
    _conceptsFuture = widget.diagnosticsService.fetchConcepts();
    _skillsFuture = widget.diagnosticsService.fetchSkills();
    _recommendationsFuture = widget.diagnosticsService.fetchRecommendations();
  }

  void _refresh() {
    setState(_loadData);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: KidsPalette.cream,
      appBar: AppBar(
        title: const Text('학습 종합 진단 리포트'),
        backgroundColor: Colors.transparent,
        elevation: 0,
        actions: [
          IconButton(
            tooltip: '새로고침',
            onPressed: _refresh,
            icon: const Icon(Icons.refresh_rounded),
          ),
          const SizedBox(width: 8),
        ],
      ),
      body: SafeArea(
        child: !widget.authService.isAuthenticated
            ? _buildUnauthenticatedView()
            : FutureBuilder<List<dynamic>>(
                future: Future.wait([
                  _summaryFuture,
                  _conceptsFuture,
                  _skillsFuture,
                  _recommendationsFuture,
                ]),
                builder: (context, snapshot) {
                  if (snapshot.connectionState != ConnectionState.done) {
                    return const OnsemLoadingIndicator(
                      labelKey: '진단 데이터를 분석하고 있어요...',
                    );
                  }

                  if (snapshot.hasError) {
                    return Center(
                      child: Padding(
                        padding: const EdgeInsets.all(24),
                        child: Column(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            const Icon(Icons.cloud_off_outlined,
                                size: 48, color: KidsPalette.cocoaSoft),
                            const SizedBox(height: 12),
                            const Text(
                              '진단 데이터를 불러오지 못했어요.',
                              style: TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            const SizedBox(height: 8),
                            Text(
                              '${snapshot.error}',
                              textAlign: TextAlign.center,
                              style: const TextStyle(
                                  fontSize: 12, color: Colors.grey),
                            ),
                            const SizedBox(height: 16),
                            FilledButton(
                              onPressed: _refresh,
                              child: const Text('다시 시도'),
                            ),
                          ],
                        ),
                      ),
                    );
                  }

                  final summary = snapshot.data![0] as DiagnosticSummaryData?;
                  final concepts =
                      snapshot.data![1] as List<DiagnosticTagMetric>;
                  final skills = snapshot.data![2] as List<DiagnosticTagMetric>;
                  final recommendations =
                      snapshot.data![3] as List<RecommendedProblemItem>;

                  if (summary == null || summary.totalAttempts == 0) {
                    return _buildEmptyDataView();
                  }

                  return RefreshIndicator(
                    onRefresh: () async => _refresh(),
                    child: ListView(
                      padding: const EdgeInsets.fromLTRB(20, 10, 20, 40),
                      children: [
                        Center(
                          child: ConstrainedBox(
                            constraints: const BoxConstraints(
                              maxWidth: AppLayout.maxContentWidth,
                            ),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.stretch,
                              children: [
                                _buildHeadlineCard(summary),
                                const SizedBox(height: 18),
                                _buildMetricsGrid(summary),
                                const SizedBox(height: 24),
                                _buildStrengthsAndWeaknesses(summary),
                                const SizedBox(height: 24),
                                _buildConceptMasterySection(concepts),
                                const SizedBox(height: 24),
                                _buildSkillMasterySection(skills),
                                const SizedBox(height: 24),
                                _buildRecommendedProblemsSection(
                                    recommendations),
                              ],
                            ),
                          ),
                        ),
                      ],
                    ),
                  );
                },
              ),
      ),
    );
  }

  Widget _buildUnauthenticatedView() {
    final strings = AppStrings.of(context);
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.lock_person_outlined,
                size: 64, color: KidsPalette.primary),
            const SizedBox(height: 16),
            Text(
              strings.t('diagnostic.unauthenticatedTitle'),
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Text(
              strings.t('diagnostic.unauthenticatedDescription'),
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 14, color: KidsPalette.cocoaSoft),
            ),
            const SizedBox(height: 24),
            FilledButton.icon(
              onPressed: () async {
                await Navigator.of(context).push(
                  MaterialPageRoute<void>(
                    builder: (context) =>
                        AuthScreen(authService: widget.authService),
                  ),
                );
                _refresh();
              },
              icon: const Icon(Icons.login),
              label: Text(strings.t('diagnostic.loginOrRegister')),
              style: FilledButton.styleFrom(
                minimumSize: const Size(200, 48),
                backgroundColor: KidsPalette.primary,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildEmptyDataView() {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.school_outlined,
                size: 64, color: KidsPalette.sage),
            const SizedBox(height: 16),
            const Text(
              '아직 풀이 기록이 부족해요!',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            const Text(
              '문제를 2~3개 이상 풀면 학생의 개념 이해도와\n풀이 습관(힌트·재시도·시간)을 분석한 맞춤 진단이 시작됩니다.',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 14, color: KidsPalette.cocoaSoft),
            ),
            const SizedBox(height: 24),
            FilledButton.icon(
              onPressed: () => Navigator.of(context).pop(),
              icon: const Icon(Icons.play_arrow_rounded),
              label: const Text('오늘의 문제 풀러 가기'),
              style: FilledButton.styleFrom(
                backgroundColor: KidsPalette.primary,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildHeadlineCard(DiagnosticSummaryData summary) {
    return Container(
      padding: const EdgeInsets.all(22),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [Color(0xFF312E81), Color(0xFF4F46E5)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(AppRadii.large),
        boxShadow: const [
          BoxShadow(
            color: Color(0x224F46E5),
            blurRadius: 12,
            offset: Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding:
                    const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(
                  color: Colors.white.withValues(alpha: 0.18),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(
                  summary.recentTrend['direction'] == 'improving'
                      ? '📈 상승세'
                      : '✨ 실시간 학습 진단',
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              const Spacer(),
              Text(
                '${summary.totalProblems}개 문제 완료',
                style: const TextStyle(
                  color: Color(0xFFE0E7FF),
                  fontSize: 13,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Text(
            summary.headline,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 20,
              fontWeight: FontWeight.w900,
              height: 1.3,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            summary.recentTrend['message']?.toString() ?? '',
            style: const TextStyle(
              color: Color(0xFFE0E7FF),
              fontSize: 14,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMetricsGrid(DiagnosticSummaryData summary) {
    final avgSec = (summary.avgElapsedMs / 1000).round();
    return LayoutBuilder(
      builder: (context, constraints) {
        final wide = constraints.maxWidth >= 600;
        return GridView.count(
          crossAxisCount: wide ? 4 : 2,
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          crossAxisSpacing: 12,
          mainAxisSpacing: 12,
          childAspectRatio: 1.5,
          children: [
            _buildMetricTile(
              label: '전체 정답률',
              value: '${(summary.accuracy * 100).round()}%',
              icon: Icons.check_circle_outline,
              color: KidsPalette.primary,
            ),
            _buildMetricTile(
              label: '평균 풀이 시간',
              value: '$avgSec초',
              icon: Icons.timer_outlined,
              color: const Color(0xFF0284C7),
            ),
            _buildMetricTile(
              label: '힌트 열람율',
              value: '${(summary.hintRate * 100).round()}%',
              icon: Icons.lightbulb_outline,
              color: const Color(0xFFD97706),
            ),
            _buildMetricTile(
              label: '평균 재시도',
              value: '${summary.avgRetryCount}회',
              icon: Icons.replay_rounded,
              color: const Color(0xFF059669),
            ),
          ],
        );
      },
    );
  }

  Widget _buildMetricTile({
    required String label,
    required String value,
    required IconData icon,
    required Color color,
  }) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(AppRadii.medium),
        border: Border.all(color: KidsPalette.line),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Row(
            children: [
              Icon(icon, size: 18, color: color),
              const SizedBox(width: 6),
              Text(
                label,
                style: const TextStyle(
                  fontSize: 12,
                  color: KidsPalette.cocoaSoft,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ],
          ),
          const SizedBox(height: 6),
          Text(
            value,
            style: TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.w900,
              color: color,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildStrengthsAndWeaknesses(DiagnosticSummaryData summary) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Expanded(
          child: Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: const Color(0xFFECFDF5),
              borderRadius: BorderRadius.circular(AppRadii.medium),
              border: Border.all(color: const Color(0xFFA7F3D0)),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Row(
                  children: [
                    Icon(Icons.thumb_up_alt_rounded,
                        size: 18, color: Color(0xFF059669)),
                    SizedBox(width: 6),
                    Text(
                      '나의 강점 개념',
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        fontSize: 14,
                        color: Color(0xFF065F46),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 10),
                if (summary.strengths.isEmpty)
                  const Text(
                    '더 많은 문제를 풀면 강점이 분석돼요.',
                    style: TextStyle(fontSize: 12, color: Color(0xFF047857)),
                  )
                else
                  ...summary.strengths.map(
                    (s) => Padding(
                      padding: const EdgeInsets.only(bottom: 6),
                      child: Text(
                        '• ${s['name_ko'] ?? s['key']} (${((s['score'] as num? ?? 0) * 100).round()}점)',
                        style: const TextStyle(
                          fontSize: 13,
                          fontWeight: FontWeight.w600,
                          color: Color(0xFF065F46),
                        ),
                      ),
                    ),
                  ),
              ],
            ),
          ),
        ),
        const SizedBox(width: 12),
        Expanded(
          child: Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: const Color(0xFFFFFBEB),
              borderRadius: BorderRadius.circular(AppRadii.medium),
              border: Border.all(color: const Color(0xFFFDE68A)),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Row(
                  children: [
                    Icon(Icons.flag_rounded,
                        size: 18, color: Color(0xFFD97706)),
                    SizedBox(width: 6),
                    Text(
                      '보완하면 좋은 개념',
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        fontSize: 14,
                        color: Color(0xFF92400E),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 10),
                if (summary.weaknesses.isEmpty)
                  const Text(
                    '취약 개념 없이 고르게 잘 풀고 있어요!',
                    style: TextStyle(fontSize: 12, color: Color(0xFFB45309)),
                  )
                else
                  ...summary.weaknesses.map(
                    (w) => Padding(
                      padding: const EdgeInsets.only(bottom: 6),
                      child: Text(
                        '• ${w['name_ko'] ?? w['key']} (연습 추천)',
                        style: const TextStyle(
                          fontSize: 13,
                          fontWeight: FontWeight.w600,
                          color: Color(0xFF92400E),
                        ),
                      ),
                    ),
                  ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildConceptMasterySection(List<DiagnosticTagMetric> concepts) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          '개념별 숙련도 분석',
          style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 6),
        const Text(
          '정답률뿐 아니라 힌트 사용과 재시도를 종합하여 숙련도를 계산합니다.',
          style: TextStyle(fontSize: 12, color: KidsPalette.cocoaSoft),
        ),
        const SizedBox(height: 12),
        ListView.separated(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          itemCount: concepts.take(6).length,
          separatorBuilder: (_, __) => const SizedBox(height: 8),
          itemBuilder: (context, index) {
            final item = concepts[index];
            return _buildTagRow(item);
          },
        ),
      ],
    );
  }

  Widget _buildSkillMasterySection(List<DiagnosticTagMetric> skills) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          '문제해결 역량·기능 분석',
          style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 6),
        const Text(
          '문제 조건 파악, 연산 선택, 계산 수행 등 수학적 문제해결 과정의 숙련도입니다.',
          style: TextStyle(fontSize: 12, color: KidsPalette.cocoaSoft),
        ),
        const SizedBox(height: 12),
        ListView.separated(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          itemCount: skills.take(5).length,
          separatorBuilder: (_, __) => const SizedBox(height: 8),
          itemBuilder: (context, index) {
            final item = skills[index];
            return _buildTagRow(item);
          },
        ),
      ],
    );
  }

  Widget _buildTagRow(DiagnosticTagMetric item) {
    final statusColor = switch (item.status) {
      'stable' => const Color(0xFF059669),
      'developing' => KidsPalette.primary,
      'needs_support' => const Color(0xFFDC2626),
      _ => KidsPalette.cocoaSoft,
    };

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(AppRadii.medium),
        border: Border.all(color: KidsPalette.line),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Expanded(
                child: Text(
                  item.nameKo,
                  style: const TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                decoration: BoxDecoration(
                  color: statusColor.withValues(alpha: 0.12),
                  borderRadius: BorderRadius.circular(6),
                ),
                child: Text(
                  item.statusLabel,
                  style: TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.w700,
                    color: statusColor,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          LinearProgressIndicator(
            value: item.score.clamp(0.0, 1.0),
            backgroundColor: const Color(0xFFE2E8F0),
            color: statusColor,
            minHeight: 6,
            borderRadius: BorderRadius.circular(3),
          ),
          const SizedBox(height: 6),
          Row(
            children: [
              Text(
                item.statusMessage,
                style: const TextStyle(
                  fontSize: 12,
                  color: KidsPalette.cocoaSoft,
                ),
              ),
              const Spacer(),
              Text(
                '${item.attemptCount}회 풀이 (신뢰도 ${(item.confidence * 100).round()}%)',
                style: const TextStyle(
                  fontSize: 11,
                  color: Color(0xFF94A3B8),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildRecommendedProblemsSection(
      List<RecommendedProblemItem> recommendations) {
    if (recommendations.isEmpty) return const SizedBox.shrink();

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          '진단 기반 맞춤 추천 문제',
          style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 6),
        const Text(
          '취약 개념과 힌트가 잦았던 역량을 우선 보완할 수 있도록 추천합니다.',
          style: TextStyle(fontSize: 12, color: KidsPalette.cocoaSoft),
        ),
        const SizedBox(height: 12),
        ListView.separated(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          itemCount: recommendations.take(3).length,
          separatorBuilder: (_, __) => const SizedBox(height: 10),
          itemBuilder: (context, index) {
            final rec = recommendations[index];
            return _buildRecommendationCard(rec);
          },
        ),
      ],
    );
  }

  Widget _buildRecommendationCard(RecommendedProblemItem rec) {
    return Card(
      elevation: 1,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(AppRadii.medium),
        side: const BorderSide(color: Color(0xFFC7D2FE)),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Container(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                  decoration: BoxDecoration(
                    color: KidsPalette.primary.withValues(alpha: 0.12),
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: Text(
                    rec.unit.isNotEmpty ? rec.unit : '수학',
                    style: const TextStyle(
                      fontSize: 11,
                      fontWeight: FontWeight.bold,
                      color: KidsPalette.primary,
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                Text(
                  '우선순위 ${rec.priority}단계',
                  style: const TextStyle(
                    fontSize: 11,
                    color: KidsPalette.cocoaSoft,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 8),
            Text(
              rec.title.isNotEmpty ? rec.title : rec.problemId,
              style: const TextStyle(
                fontSize: 15,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              '💡 ${rec.reason}',
              style: const TextStyle(
                fontSize: 13,
                color: KidsPalette.primaryDark,
                fontWeight: FontWeight.w500,
              ),
            ),
            const SizedBox(height: 12),
            Align(
              alignment: Alignment.centerRight,
              child: FilledButton.icon(
                onPressed: () => _openProblem(rec.problemId, rec.title),
                icon: const Icon(Icons.edit_note_rounded, size: 18),
                label: const Text('바로 풀기'),
                style: FilledButton.styleFrom(
                  backgroundColor: KidsPalette.primary,
                  padding:
                      const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Future<void> _openProblem(String problemId, String title) async {
    final manifest = await widget.contentRepository.loadManifest();
    final problem = manifest.problems.firstWhere(
      (p) => p.id == problemId,
      orElse: () => ProblemSummary.fromJson({
        'id': problemId,
        'grade': 3,
        'subject': 'math',
        'unit': '추천 문제',
        'type': 'choice',
        'title': title,
        'path': 'examples/problems/ko',
      }),
    );

    if (!mounted) return;
    await Navigator.of(context).push(
      MaterialPageRoute<void>(
        builder: (context) => ProblemSolveScreen(
          repository: widget.contentRepository,
          progressRepository: widget.progressRepository,
          problem: problem,
        ),
      ),
    );
    _refresh();
  }
}
