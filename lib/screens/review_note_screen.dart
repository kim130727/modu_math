import 'package:flutter/material.dart';

import '../l10n/app_strings.dart';
import '../models/content_models.dart';
import '../models/learning_progress.dart';
import '../services/content_repository.dart';
import '../services/learning_progress_repository.dart';
import '../theme/app_theme.dart';
import 'problem_solve_screen.dart';

class ReviewNoteScreen extends StatefulWidget {
  const ReviewNoteScreen({
    super.key,
    required this.repository,
    required this.progressRepository,
  });

  final ContentRepository repository;
  final LearningProgressRepository progressRepository;

  @override
  State<ReviewNoteScreen> createState() => _ReviewNoteScreenState();
}

class _ReviewNoteScreenState extends State<ReviewNoteScreen> {
  late final Future<ProblemManifest> _manifestFuture;
  late final Future<List<StudentAttempt>> _attemptsFuture;
  ErrorCategory? _selectedCategory;

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  void _loadData() {
    _manifestFuture = widget.repository.loadManifest();
    _attemptsFuture = widget.progressRepository.getAttempts();
  }

  void _refresh() {
    setState(() {
      _loadData();
    });
  }

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    return Scaffold(
      backgroundColor: KidsPalette.cream,
      appBar: AppBar(
        title: Text(strings.t('review.title')),
        backgroundColor: Colors.transparent,
        elevation: 0,
      ),
      body: SafeArea(
        child: FutureBuilder<List<dynamic>>(
          future: Future.wait([_manifestFuture, _attemptsFuture]),
          builder: (context, snapshot) {
            if (snapshot.connectionState != ConnectionState.done) {
              return const Center(child: CircularProgressIndicator());
            }

            if (snapshot.hasError) {
              return Center(
                child: Text(
                  strings.t('review.loadError', {'error': snapshot.error}),
                ),
              );
            }

            final manifest = snapshot.data![0] as ProblemManifest;
            final attempts = snapshot.data![1] as List<StudentAttempt>;

            final wrongAttempts = attempts.where((a) => !a.isCorrect).toList();
            final filteredAttempts = _selectedCategory == null
                ? wrongAttempts
                : wrongAttempts
                    .where((a) => a.errorCategory == _selectedCategory)
                    .toList();

            return RefreshIndicator(
              onRefresh: () async => _refresh(),
              child: ListView(
                padding: const EdgeInsets.all(20),
                children: [
                  _ReviewHeaderCard(totalWrongCount: wrongAttempts.length),
                  const SizedBox(height: 20),
                  Text(
                    strings.t('review.filterTitle'),
                    style: Theme.of(context).textTheme.titleSmall?.copyWith(
                          fontWeight: FontWeight.bold,
                        ),
                  ),
                  const SizedBox(height: 10),
                  SingleChildScrollView(
                    scrollDirection: Axis.horizontal,
                    child: Row(
                      children: [
                        FilterChip(
                          label: Text(strings.t('review.all')),
                          selected: _selectedCategory == null,
                          onSelected: (selected) {
                            setState(() => _selectedCategory = null);
                          },
                        ),
                        const SizedBox(width: 8),
                        ...ErrorCategory.values
                            .where((c) => c != ErrorCategory.none)
                            .map((category) {
                          return Padding(
                            padding: const EdgeInsets.only(right: 8),
                            child: FilterChip(
                              label: Text(strings.errorCategory(category.code)),
                              selected: _selectedCategory == category,
                              onSelected: (selected) {
                                setState(() {
                                  _selectedCategory =
                                      selected ? category : null;
                                });
                              },
                            ),
                          );
                        }),
                      ],
                    ),
                  ),
                  const SizedBox(height: 24),
                  if (filteredAttempts.isEmpty)
                    Center(
                      child: Padding(
                        padding: const EdgeInsets.symmetric(vertical: 40),
                        child: Text(
                          strings.t('review.empty'),
                          textAlign: TextAlign.center,
                          style: const TextStyle(
                            fontSize: 16,
                            color: KidsPalette.cocoaSoft,
                          ),
                        ),
                      ),
                    )
                  else
                    ...filteredAttempts.map((attempt) {
                      final problem = manifest.problems.firstWhere(
                        (p) => p.id == attempt.problemId,
                        orElse: () => ProblemSummary(
                          id: attempt.problemId,
                          grade: 3,
                          subject: 'math',
                          unit: attempt.unit,
                          type: 'calc',
                          title: attempt.problemId,
                          path: '',
                          raw: const {},
                        ),
                      );

                      return Card(
                        margin: const EdgeInsets.only(bottom: 12),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(16),
                        ),
                        child: Padding(
                          padding: const EdgeInsets.all(16),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Row(
                                children: [
                                  Chip(
                                    label:
                                        Text(strings.unitTitle(attempt.unit)),
                                    backgroundColor: KidsPalette.paper,
                                    side: const BorderSide(
                                      color: KidsPalette.line,
                                    ),
                                  ),
                                  const SizedBox(width: 8),
                                  Chip(
                                    label: Text(
                                      strings.errorCategory(
                                        attempt.errorCategory.code,
                                      ),
                                    ),
                                    backgroundColor: KidsPalette.butter,
                                    side: BorderSide.none,
                                  ),
                                ],
                              ),
                              const SizedBox(height: 8),
                              Text(
                                problem.title,
                                style: const TextStyle(
                                  fontSize: 17,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              const SizedBox(height: 12),
                              Row(
                                mainAxisAlignment:
                                    MainAxisAlignment.spaceBetween,
                                children: [
                                  Text(
                                    strings.t('review.submittedAnswer', {
                                      'answer': attempt.answer,
                                    }),
                                    style: const TextStyle(
                                      color: KidsPalette.cocoaSoft,
                                    ),
                                  ),
                                  FilledButton.icon(
                                    onPressed: () async {
                                      await Navigator.of(context).push(
                                        MaterialPageRoute<void>(
                                          builder: (context) =>
                                              ProblemSolveScreen(
                                            repository: widget.repository,
                                            progressRepository:
                                                widget.progressRepository,
                                            problem: problem,
                                          ),
                                        ),
                                      );
                                      _refresh();
                                    },
                                    icon: const Icon(Icons.replay, size: 18),
                                    label: Text(strings.t('session.retry')),
                                  ),
                                ],
                              ),
                            ],
                          ),
                        ),
                      );
                    }),
                ],
              ),
            );
          },
        ),
      ),
    );
  }
}

class _ReviewHeaderCard extends StatelessWidget {
  const _ReviewHeaderCard({required this.totalWrongCount});

  final int totalWrongCount;

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: KidsPalette.butter,
        borderRadius: BorderRadius.circular(20),
      ),
      child: Row(
        children: [
          const Icon(
            Icons.fact_check_outlined,
            size: 36,
            color: KidsPalette.cocoa,
          ),
          const SizedBox(width: 14),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  strings.t('review.headerTitle', {
                    'count': totalWrongCount,
                  }),
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: KidsPalette.ink,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  strings.t('review.headerDescription'),
                  style: const TextStyle(
                    fontSize: 13,
                    color: KidsPalette.cocoaSoft,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
