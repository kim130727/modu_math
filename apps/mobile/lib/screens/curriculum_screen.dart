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

  Future<void> _openUnit(String unit, {String? subUnit}) async {
    await Navigator.of(context).pushNamed(
      ModuMathRoutes.learningSession,
      arguments: LearningSessionRouteArguments(unit: unit, subUnit: subUnit),
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

typedef UnitOpener = void Function(String unit, {String? subUnit});

class _CurriculumSection extends StatelessWidget {
  const _CurriculumSection({
    required this.group,
    required this.initialUnit,
    required this.onOpenUnit,
  });

  final _CurriculumGroup group;
  final String? initialUnit;
  final UnitOpener onOpenUnit;

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
        const SizedBox(height: 12),
        ListView.separated(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          itemCount: group.units.length,
          separatorBuilder: (context, index) => const SizedBox(height: 12),
          itemBuilder: (context, index) {
            final unit = group.units[index];
            return _UnitTile(
              unit: unit,
              selected: unit.name == initialUnit,
              onTap: () => onOpenUnit(unit.name),
              onOpenSubUnit: (subUnit) =>
                  onOpenUnit(unit.name, subUnit: subUnit),
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
    required this.onOpenSubUnit,
  });

  final _CurriculumUnit unit;
  final bool selected;
  final VoidCallback onTap;
  final ValueChanged<String> onOpenSubUnit;

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
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            InkWell(
              borderRadius: BorderRadius.circular(12),
              onTap: onTap,
              child: Row(
                children: [
                  CircleAvatar(
                    backgroundColor:
                        selected ? KidsPalette.sage : const Color(0xFFECEEFF),
                    foregroundColor:
                        selected ? Colors.white : KidsPalette.sage,
                    child: Text('${unit.number}'),
                  ),
                  const SizedBox(width: 14),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          strings.unitTitle(unit.topic),
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                          style: Theme.of(context).textTheme.titleMedium,
                        ),
                        const SizedBox(height: 2),
                        Text(
                          strings.problemCount(unit.problemCount),
                          style: Theme.of(context).textTheme.bodySmall,
                        ),
                      ],
                    ),
                  ),
                  OutlinedButton.icon(
                    onPressed: onTap,
                    icon: const Icon(Icons.play_arrow_rounded, size: 18),
                    label: const Text('전체 학습'),
                    style: OutlinedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 12, vertical: 8),
                      side: const BorderSide(color: KidsPalette.line),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(10),
                      ),
                    ),
                  ),
                ],
              ),
            ),
            if (unit.subUnits.isNotEmpty) ...[
              const SizedBox(height: 12),
              const Divider(height: 1, color: KidsPalette.line),
              const SizedBox(height: 10),
              Wrap(
                spacing: 8,
                runSpacing: 8,
                children: unit.subUnits.map((subUnit) {
                  return ActionChip(
                    avatar: const Icon(Icons.bookmark_outline_rounded,
                        size: 16, color: KidsPalette.sage),
                    label: Text(
                      '${subUnit.name} (${subUnit.problemCount})',
                      style: const TextStyle(
                          fontSize: 13, fontWeight: FontWeight.w600),
                    ),
                    backgroundColor: Colors.white,
                    side: const BorderSide(color: KidsPalette.line),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(10),
                    ),
                    onPressed: () => onOpenSubUnit(subUnit.name),
                  );
                }).toList(),
              ),
            ],
          ],
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
      final semester = sample.semester.isNotEmpty ? sample.semester : unknownSemester;
      final groupKey = '${sample.grade}|$semester';

      final subBuckets = <String, int>{};
      for (final p in entry.value) {
        subBuckets.update(p.subUnit, (v) => v + 1, ifAbsent: () => 1);
      }
      final subUnits = subBuckets.entries
          .map((e) => _CurriculumSubUnit(name: e.key, problemCount: e.value))
          .toList();

      groupedUnits.putIfAbsent(groupKey, () => []).add(
            _CurriculumUnit(
              name: entry.key,
              number: sample.unitNumber,
              topic: sample.unitTopic,
              problemCount: entry.value.length,
              subUnits: subUnits,
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

class _CurriculumSubUnit {
  const _CurriculumSubUnit({
    required this.name,
    required this.problemCount,
  });

  final String name;
  final int problemCount;
}

class _CurriculumUnit {
  const _CurriculumUnit({
    required this.name,
    required this.number,
    required this.topic,
    required this.problemCount,
    required this.subUnits,
  });

  final String name;
  final int number;
  final String topic;
  final int problemCount;
  final List<_CurriculumSubUnit> subUnits;
}

int? _readInt(Object? value) {
  if (value is int) {
    return value;
  }
  return int.tryParse(value?.toString() ?? '');
}
