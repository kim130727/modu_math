import 'dart:async';

import 'package:flutter/material.dart';

import '../app/router.dart';
import '../l10n/app_strings.dart';
import '../models/content_models.dart';
import '../services/content_repository.dart';
import '../services/learning_progress_repository.dart';
import '../theme/app_theme.dart';
import '../widgets/onsem_loading_indicator.dart';

class CurriculumScreen extends StatefulWidget {
  const CurriculumScreen({
    super.key,
    required this.repository,
    required this.progressRepository,
    this.initialUnit,
  });

  final ContentRepository repository;
  final LearningProgressRepository progressRepository;
  final String? initialUnit;

  @override
  State<CurriculumScreen> createState() => _CurriculumScreenState();
}

class _CurriculumScreenState extends State<CurriculumScreen> {
  late Future<ProblemManifest> _manifestFuture;
  String? _activeProblemLocale;

  @override
  void initState() {
    super.initState();
    _manifestFuture = _loadManifest();
  }

  Future<ProblemManifest> _loadManifest() async {
    final manifest = await widget.repository.loadManifest();
    final count = manifest.problems.length.clamp(0, 3);
    for (var i = 0; i < count; i++) {
      unawaited(widget.repository.preloadProblem(manifest.problems[i]).catchError((_) {}));
    }
    return manifest;
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final locale = AppLocaleScope.maybeOf(context)?.locale.languageCode ?? 'ko';
    if (_activeProblemLocale == locale) {
      return;
    }
    final previousLocale = _activeProblemLocale;
    _activeProblemLocale = locale;
    widget.repository.activeProblemLocale = locale;
    if (previousLocale == null) {
      return;
    }
    setState(() {
      _manifestFuture = _loadManifest();
    });
  }

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    return Scaffold(
      backgroundColor: KidsPalette.cream,
      appBar: AppBar(
        title: Text(strings.t('curriculum.title')),
      ),
      body: SafeArea(
        child: FutureBuilder<ProblemManifest>(
          future: _manifestFuture,
          builder: (context, snapshot) {
            if (snapshot.connectionState != ConnectionState.done) {
              return const OnsemLoadingIndicator(label: '단원을 준비하고 있어요');
            }
            if (snapshot.hasError) {
              return Center(
                child: Padding(
                  padding: const EdgeInsets.all(24),
                  child: Text(
                    strings.t('curriculum.loadError', {
                      'error': snapshot.error,
                    }),
                  ),
                ),
              );
            }

            final groups = _CurriculumGroup.fromProblems(
              snapshot.data?.problems ?? const <ProblemSummary>[],
            );
            if (groups.isEmpty) {
              return Center(child: Text(strings.t('curriculum.empty')));
            }

            return ListView(
              padding: const EdgeInsets.fromLTRB(20, 12, 20, 28),
              children: [
                const _CurriculumHeader(),
                const SizedBox(height: 20),
                ...groups.map(
                  (group) => Padding(
                    padding: const EdgeInsets.only(bottom: 18),
                    child: _CurriculumSection(
                      group: group,
                      initialUnit: widget.initialUnit,
                      onOpenUnit: _openUnit,
                    ),
                  ),
                ),
              ],
            );
          },
        ),
      ),
    );
  }

  Future<void> _openUnit(String unit) async {
    await Navigator.of(context).pushNamed(
      ModuMathRoutes.learningSession,
      arguments: LearningSessionRouteArguments(unit: unit),
    );
    if (mounted) {
      setState(() {});
    }
  }
}

class _CurriculumHeader extends StatelessWidget {
  const _CurriculumHeader();

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    return DecoratedBox(
      decoration: BoxDecoration(
        color: const Color(0xFFECEEFF),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: KidsPalette.line),
      ),
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Row(
          children: [
            const Icon(Icons.map_outlined, color: KidsPalette.sage, size: 32),
            const SizedBox(width: 14),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    strings.t('curriculum.headerTitle'),
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                  const SizedBox(height: 4),
                  Text(
                    strings.t('curriculum.headerDescription'),
                    style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                          color: KidsPalette.cocoaSoft,
                        ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _CurriculumSection extends StatelessWidget {
  const _CurriculumSection({
    required this.group,
    required this.initialUnit,
    required this.onOpenUnit,
  });

  final _CurriculumGroup group;
  final String? initialUnit;
  final ValueChanged<String> onOpenUnit;

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          strings.t('curriculum.groupTitle', {
            'grade': group.grade,
            'semester': strings.semester(group.semester),
          }),
          style: Theme.of(context).textTheme.titleMedium,
        ),
        const SizedBox(height: 10),
        LayoutBuilder(
          builder: (context, constraints) {
            final wide = constraints.maxWidth >= 760;
            return GridView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: group.units.length,
              gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: wide ? 2 : 1,
                mainAxisSpacing: 10,
                crossAxisSpacing: 10,
                childAspectRatio: wide ? 3.1 : 3.5,
              ),
              itemBuilder: (context, index) {
                final unit = group.units[index];
                return _UnitTile(
                  unit: unit,
                  selected: unit.name == initialUnit,
                  onTap: () => onOpenUnit(unit.name),
                );
              },
            );
          },
        ),
      ],
    );
  }
}

class _UnitTile extends StatelessWidget {
  const _UnitTile({
    required this.unit,
    required this.selected,
    required this.onTap,
  });

  final _CurriculumUnit unit;
  final bool selected;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    return Card(
      margin: EdgeInsets.zero,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: BorderSide(
          color: selected ? KidsPalette.sage : KidsPalette.line,
          width: selected ? 2 : 1,
        ),
      ),
      child: InkWell(
        borderRadius: BorderRadius.circular(16),
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              CircleAvatar(
                backgroundColor:
                    selected ? KidsPalette.sage : const Color(0xFFECEEFF),
                foregroundColor: selected ? Colors.white : KidsPalette.sage,
                child: Text('${unit.number}'),
              ),
              const SizedBox(width: 14),
              Expanded(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      strings.unitTitle(unit.topic),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                      style: Theme.of(context).textTheme.titleMedium,
                    ),
                    const SizedBox(height: 4),
                    Text(
                      strings.problemCount(unit.problemCount),
                      style: Theme.of(context).textTheme.bodySmall,
                    ),
                  ],
                ),
              ),
              const Icon(Icons.chevron_right, color: KidsPalette.sage),
            ],
          ),
        ),
      ),
    );
  }
}

class _CurriculumGroup {
  const _CurriculumGroup({
    required this.grade,
    required this.semester,
    required this.units,
  });

  final int grade;
  final String semester;
  final List<_CurriculumUnit> units;

  static List<_CurriculumGroup> fromProblems(List<ProblemSummary> problems) {
    const unknownSemester = '__unknown_semester__';
    final unitBuckets = <String, List<ProblemSummary>>{};
    for (final problem in problems) {
      unitBuckets.putIfAbsent(problem.unit, () => []).add(problem);
    }

    final groupedUnits = <String, List<_CurriculumUnit>>{};
    for (final entry in unitBuckets.entries) {
      final sample = entry.value.first;
      final semester = sample.raw['semester']?.toString() ?? unknownSemester;
      final groupKey = '${sample.grade}|$semester';
      groupedUnits.putIfAbsent(groupKey, () => []).add(
            _CurriculumUnit(
              name: entry.key,
              number: _readInt(sample.raw['unitNumber']) ?? 0,
              topic: sample.raw['unitTopic']?.toString() ?? entry.key,
              problemCount: entry.value.length,
            ),
          );
    }

    final groups = groupedUnits.entries.map((entry) {
      final parts = entry.key.split('|');
      final units = entry.value
        ..sort((a, b) {
          final byNumber = a.number.compareTo(b.number);
          return byNumber == 0 ? a.name.compareTo(b.name) : byNumber;
        });
      return _CurriculumGroup(
        grade: int.tryParse(parts.first) ?? 0,
        semester: parts.length > 1 ? parts[1] : unknownSemester,
        units: units,
      );
    }).toList()
      ..sort((a, b) {
        final byGrade = a.grade.compareTo(b.grade);
        return byGrade == 0 ? a.semester.compareTo(b.semester) : byGrade;
      });

    return groups;
  }
}

class _CurriculumUnit {
  const _CurriculumUnit({
    required this.name,
    required this.number,
    required this.topic,
    required this.problemCount,
  });

  final String name;
  final int number;
  final String topic;
  final int problemCount;
}

int? _readInt(Object? value) {
  if (value is int) {
    return value;
  }
  return int.tryParse(value?.toString() ?? '');
}
