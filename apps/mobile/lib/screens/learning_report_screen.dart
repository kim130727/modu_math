import 'package:flutter/material.dart';

import '../l10n/app_strings.dart';
import '../models/learning_progress.dart';
import '../models/student_profile.dart';
import '../services/learning_progress_repository.dart';
import '../theme/app_theme.dart';

class LearningReportScreen extends StatefulWidget {
  const LearningReportScreen({
    super.key,
    required this.progressRepository,
  });

  final LearningProgressRepository progressRepository;

  @override
  State<LearningReportScreen> createState() => _LearningReportScreenState();
}

class _LearningReportScreenState extends State<LearningReportScreen> {
  late final Future<StudentProfile> _profileFuture;
  late final Future<DailySummary> _dailySummaryFuture;
  late final Future<List<SkillMastery>> _skillMasteriesFuture;
  late final Future<List<StudentAttempt>> _attemptsFuture;

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  void _loadData() {
    _profileFuture = widget.progressRepository.getProfile();
    _dailySummaryFuture =
        widget.progressRepository.getDailySummary(DateTime.now());
    _skillMasteriesFuture = widget.progressRepository.getSkillMasteries();
    _attemptsFuture = widget.progressRepository.getAttempts();
  }

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    return Scaffold(
      backgroundColor: KidsPalette.cream,
      appBar: AppBar(
        title: Text(strings.t('report.title')),
        backgroundColor: Colors.transparent,
        elevation: 0,
      ),
      body: SafeArea(
        child: FutureBuilder<List<dynamic>>(
          future: Future.wait([
            _profileFuture,
            _dailySummaryFuture,
            _skillMasteriesFuture,
            _attemptsFuture,
          ]),
          builder: (context, snapshot) {
            if (snapshot.connectionState != ConnectionState.done) {
              return const Center(child: CircularProgressIndicator());
            }

            if (snapshot.hasError) {
              return Center(
                child: Text(
                  strings.t('report.loadError', {'error': snapshot.error}),
                ),
              );
            }

            final profile = snapshot.data![0] as StudentProfile;
            final dailySummary = snapshot.data![1] as DailySummary;
            final skillMasteries = snapshot.data![2] as List<SkillMastery>;
            final attempts = snapshot.data![3] as List<StudentAttempt>;

            final totalSolved = attempts.map((a) => a.problemId).toSet().length;
            final totalCorrect = attempts
                .where((a) => a.isCorrect)
                .map((a) => a.problemId)
                .toSet()
                .length;
            final overallAccuracy =
                totalSolved == 0 ? 0.0 : totalCorrect / totalSolved;

            // Error category distribution
            final errorCounts = <ErrorCategory, int>{};
            for (final attempt in attempts.where((a) => !a.isCorrect)) {
              if (attempt.errorCategory != ErrorCategory.none) {
                errorCounts[attempt.errorCategory] =
                    (errorCounts[attempt.errorCategory] ?? 0) + 1;
              }
            }

            return ListView(
              padding: const EdgeInsets.all(20),
              children: [
                _ReportOverviewCard(
                  profile: profile,
                  totalSolved: totalSolved,
                  overallAccuracy: overallAccuracy,
                  streakDays: dailySummary.streakDays,
                ),
                const SizedBox(height: 24),
                Text(
                  strings.t('report.weaknessTitle'),
                  style: Theme.of(context).textTheme.titleLarge?.copyWith(
                        fontWeight: FontWeight.bold,
                        color: KidsPalette.ink,
                      ),
                ),
                const SizedBox(height: 12),
                if (errorCounts.isEmpty)
                  Card(
                    child: Padding(
                      padding: const EdgeInsets.all(20),
                      child: Text(
                        strings.t('report.noErrors'),
                        textAlign: TextAlign.center,
                        style: const TextStyle(color: KidsPalette.cocoaSoft),
                      ),
                    ),
                  )
                else
                  ...errorCounts.entries.map((entry) {
                    return Card(
                      margin: const EdgeInsets.only(bottom: 8),
                      child: Padding(
                        padding: const EdgeInsets.all(14),
                        child: Row(
                          children: [
                            Expanded(
                              child: Text(
                                strings.errorCategory(entry.key.code),
                                style: const TextStyle(
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ),
                            Chip(
                              label: Text(
                                strings.t('report.recordCount', {
                                  'count': entry.value,
                                }),
                              ),
                              backgroundColor: KidsPalette.butter,
                            ),
                          ],
                        ),
                      ),
                    );
                  }),
                const SizedBox(height: 28),
                Text(
                  strings.t('report.masteryTitle'),
                  style: Theme.of(context).textTheme.titleLarge?.copyWith(
                        fontWeight: FontWeight.bold,
                        color: KidsPalette.ink,
                      ),
                ),
                const SizedBox(height: 12),
                if (skillMasteries.isEmpty)
                  Card(
                    child: Padding(
                      padding: const EdgeInsets.all(20),
                      child: Text(strings.t('report.noMastery')),
                    ),
                  )
                else
                  ...skillMasteries.map((mastery) {
                    final percent = (mastery.accuracy * 100).toStringAsFixed(0);
                    return Card(
                      margin: const EdgeInsets.only(bottom: 10),
                      child: Padding(
                        padding: const EdgeInsets.all(16),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Text(
                                  strings.unitTitle(mastery.unit),
                                  style: const TextStyle(
                                    fontSize: 16,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                Chip(
                                  label: Text(
                                    strings.masteryLevel(mastery.masteryLevel),
                                  ),
                                  backgroundColor: mastery.accuracy >= 0.8
                                      ? const Color(0xFFDCFCE7)
                                      : mastery.accuracy >= 0.5
                                          ? const Color(0xFFFEF3C7)
                                          : const Color(0xFFFEE2E2),
                                ),
                              ],
                            ),
                            const SizedBox(height: 8),
                            LinearProgressIndicator(
                              value: mastery.accuracy,
                              minHeight: 10,
                              borderRadius: BorderRadius.circular(5),
                              color: KidsPalette.sage,
                              backgroundColor: KidsPalette.line,
                            ),
                            const SizedBox(height: 6),
                            Text(
                              strings.t('report.masteryStats', {
                                'count': mastery.totalAttempted,
                                'percent': percent,
                              }),
                              style: const TextStyle(
                                fontSize: 13,
                                color: KidsPalette.cocoaSoft,
                              ),
                            ),
                          ],
                        ),
                      ),
                    );
                  }),
              ],
            );
          },
        ),
      ),
    );
  }
}

class _ReportOverviewCard extends StatelessWidget {
  const _ReportOverviewCard({
    required this.profile,
    required this.totalSolved,
    required this.overallAccuracy,
    required this.streakDays,
  });

  final StudentProfile profile;
  final int totalSolved;
  final double overallAccuracy;
  final int streakDays;

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    final accuracyPercent = (overallAccuracy * 100).toStringAsFixed(0);

    return Container(
      padding: const EdgeInsets.all(22),
      decoration: BoxDecoration(
        color: KidsPalette.butter,
        borderRadius: BorderRadius.circular(20),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                strings.t('report.overviewTitle', {'name': profile.name}),
                style: const TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  color: KidsPalette.ink,
                ),
              ),
              Container(
                padding:
                    const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Row(
                  children: [
                    const Icon(
                      Icons.local_fire_department,
                      color: Colors.orange,
                      size: 18,
                    ),
                    const SizedBox(width: 4),
                    Text(
                      strings.t('report.streak', {'days': streakDays}),
                      style: const TextStyle(fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 18),
          Row(
            children: [
              Expanded(
                child: _ReportMetric(
                  label: strings.t('report.totalSolved'),
                  value: strings.itemCount(totalSolved),
                ),
              ),
              Expanded(
                child: _ReportMetric(
                  label: strings.t('report.overallAccuracy'),
                  value: '$accuracyPercent%',
                ),
              ),
              Expanded(
                child: _ReportMetric(
                  label: strings.t('report.grade'),
                  value: strings.grade(profile.grade),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class _ReportMetric extends StatelessWidget {
  const _ReportMetric({required this.label, required this.value});

  final String label;
  final String value;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          label,
          style: const TextStyle(fontSize: 13, color: KidsPalette.cocoaSoft),
        ),
        const SizedBox(height: 4),
        Text(
          value,
          style: const TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
            color: KidsPalette.ink,
          ),
        ),
      ],
    );
  }
}
