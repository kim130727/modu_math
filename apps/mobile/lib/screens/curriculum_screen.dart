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
  String? _selectedUnit;

  @override
  void initState() {
    super.initState();
    _selectedUnit = widget.initialUnit;
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
        title: Text(
          _selectedUnit != null
              ? strings.t('curriculum.unitDetailTitle', {
                  'unit': strings.unitTitle(_extractTopic(_selectedUnit!)),
                })
              : strings.t('curriculum.title'),
        ),
        actions: [
          if (_selectedUnit != null)
            Padding(
              padding: const EdgeInsets.only(right: 8),
              child: TextButton.icon(
                onPressed: () => setState(() => _selectedUnit = null),
                icon: const Icon(Icons.list_alt_rounded, size: 18),
                label: Text(strings.t('curriculum.viewAllUnits')),
                style: TextButton.styleFrom(
                  foregroundColor: KidsPalette.ink,
                ),
              ),
            ),
        ],
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

            if (_selectedUnit != null) {
              final focused = _findUnitAndGroup(groups, _selectedUnit!);
              if (focused != null) {
                return _SingleUnitView(
                  unit: focused.unit,
                  group: focused.group,
                  onOpenUnit: _openUnit,
                  onShowAllUnits: () => setState(() => _selectedUnit = null),
                );
              }
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
                      onSelectUnit: (unit) =>
                          setState(() => _selectedUnit = unit),
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

  String _extractTopic(String unitName) {
    final dotIndex = unitName.lastIndexOf('.');
    if (dotIndex != -1 && dotIndex + 1 < unitName.length) {
      return unitName.substring(dotIndex + 1).trim();
    }
    return unitName;
  }

  _UnitWithGroup? _findUnitAndGroup(
    List<_CurriculumGroup> groups,
    String unitName,
  ) {
    for (final group in groups) {
      for (final unit in group.units) {
        if (unit.name == unitName) {
          return _UnitWithGroup(unit: unit, group: group);
        }
      }
    }
    return null;
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

class _UnitWithGroup {
  const _UnitWithGroup({required this.unit, required this.group});
  final _CurriculumUnit unit;
  final _CurriculumGroup group;
}

class _SingleUnitView extends StatelessWidget {
  const _SingleUnitView({
    required this.unit,
    required this.group,
    required this.onOpenUnit,
    required this.onShowAllUnits,
  });

  final _CurriculumUnit unit;
  final _CurriculumGroup group;
  final UnitOpener onOpenUnit;
  final VoidCallback onShowAllUnits;

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    final groupTitle = strings.t('curriculum.groupTitle', {
      'grade': group.grade,
      'semester': strings.semester(group.semester),
    });

    return ListView(
      padding: const EdgeInsets.fromLTRB(20, 16, 20, 32),
      children: [
        Row(
          children: [
            ActionChip(
              avatar: const Icon(Icons.arrow_back_rounded, size: 16, color: KidsPalette.ink),
              label: Text(strings.t('curriculum.viewAllUnits')),
              backgroundColor: KidsPalette.paper,
              side: const BorderSide(color: KidsPalette.line),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(10),
              ),
              onPressed: onShowAllUnits,
            ),
            const Spacer(),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
              decoration: BoxDecoration(
                color: const Color(0xFFECEEFF),
                borderRadius: BorderRadius.circular(20),
                border: Border.all(color: KidsPalette.line),
              ),
              child: Text(
                groupTitle,
                style: const TextStyle(
                  fontSize: 13,
                  fontWeight: FontWeight.w700,
                  color: KidsPalette.sage,
                ),
              ),
            ),
          ],
        ),
        const SizedBox(height: 16),
        Card(
          margin: EdgeInsets.zero,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(20),
            side: const BorderSide(color: KidsPalette.sage, width: 2),
          ),
          child: Padding(
            padding: const EdgeInsets.all(22),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    CircleAvatar(
                      radius: 28,
                      backgroundColor: KidsPalette.sage,
                      foregroundColor: Colors.white,
                      child: Text(
                        '${unit.number}',
                        style: const TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.w900,
                        ),
                      ),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            groupTitle,
                            style: Theme.of(context).textTheme.bodySmall?.copyWith(
                                  color: KidsPalette.cocoaSoft,
                                ),
                          ),
                          const SizedBox(height: 2),
                          Text(
                            strings.unitTitle(unit.topic),
                            style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                                  fontWeight: FontWeight.w800,
                                ),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            strings.problemCount(unit.problemCount),
                            style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                  color: KidsPalette.sage,
                                  fontWeight: FontWeight.w700,
                                ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 20),
                FilledButton.icon(
                  onPressed: () => onOpenUnit(unit.name),
                  icon: const Icon(Icons.play_arrow_rounded, size: 24),
                  label: Text(
                    strings.t('curriculum.startWholeUnit', {
                      'count': unit.problemCount,
                    }),
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w800,
                    ),
                  ),
                  style: FilledButton.styleFrom(
                    minimumSize: const Size.fromHeight(52),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(14),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
        if (unit.subUnits.isNotEmpty) ...[
          const SizedBox(height: 28),
          Text(
            strings.t('curriculum.subUnitSection'),
            style: Theme.of(context).textTheme.titleLarge?.copyWith(
                  fontWeight: FontWeight.w800,
                ),
          ),
          const SizedBox(height: 12),
          ListView.separated(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            itemCount: unit.subUnits.length,
            separatorBuilder: (context, index) => const SizedBox(height: 10),
            itemBuilder: (context, index) {
              final subUnit = unit.subUnits[index];
              return Card(
                margin: EdgeInsets.zero,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(14),
                  side: const BorderSide(color: KidsPalette.line),
                ),
                child: InkWell(
                  borderRadius: BorderRadius.circular(14),
                  onTap: () => onOpenUnit(unit.name, subUnit: subUnit.name),
                  child: Padding(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 16,
                      vertical: 14,
                    ),
                    child: Row(
                      children: [
                        Container(
                          width: 36,
                          height: 36,
                          decoration: BoxDecoration(
                            color: const Color(0xFFECEEFF),
                            borderRadius: BorderRadius.circular(10),
                          ),
                          child: const Icon(
                            Icons.bookmark_outline_rounded,
                            color: KidsPalette.sage,
                            size: 20,
                          ),
                        ),
                        const SizedBox(width: 14),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                subUnit.name,
                                style: Theme.of(context)
                                    .textTheme
                                    .titleMedium
                                    ?.copyWith(
                                      fontWeight: FontWeight.w700,
                                    ),
                              ),
                              const SizedBox(height: 2),
                              Text(
                                strings.problemCount(subUnit.problemCount),
                                style: Theme.of(context).textTheme.bodySmall?.copyWith(
                                      color: KidsPalette.cocoaSoft,
                                    ),
                              ),
                            ],
                          ),
                        ),
                        OutlinedButton.icon(
                          onPressed: () =>
                              onOpenUnit(unit.name, subUnit: subUnit.name),
                          icon: const Icon(Icons.arrow_forward_rounded, size: 16),
                          label: Text(strings.t('curriculum.subUnitSolve')),
                          style: OutlinedButton.styleFrom(
                            padding: const EdgeInsets.symmetric(
                              horizontal: 12,
                              vertical: 8,
                            ),
                            side: const BorderSide(color: KidsPalette.line),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(10),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              );
            },
          ),
        ],
        const SizedBox(height: 32),
        Container(
          padding: const EdgeInsets.all(18),
          decoration: BoxDecoration(
            color: const Color(0xFFECEEFF),
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: KidsPalette.line),
          ),
          child: Row(
            children: [
              const Icon(Icons.explore_outlined, color: KidsPalette.sage, size: 28),
              const SizedBox(width: 12),
              Expanded(
                child: Text(
                  strings.t('curriculum.exploreOtherUnits'),
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                        fontWeight: FontWeight.w600,
                      ),
                ),
              ),
              OutlinedButton(
                onPressed: onShowAllUnits,
                style: OutlinedButton.styleFrom(
                  backgroundColor: Colors.white,
                  side: const BorderSide(color: KidsPalette.line),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10),
                  ),
                ),
                child: Text(strings.t('curriculum.viewAllUnits')),
              ),
            ],
          ),
        ),
      ],
    );
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
    required this.onSelectUnit,
    required this.onOpenUnit,
  });

  final _CurriculumGroup group;
  final String? initialUnit;
  final ValueChanged<String> onSelectUnit;
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
              onTap: () => onSelectUnit(unit.name),
              onOpenUnit: () => onOpenUnit(unit.name),
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
    required this.onOpenUnit,
    required this.onOpenSubUnit,
  });

  final _CurriculumUnit unit;
  final bool selected;
  final VoidCallback onTap;
  final VoidCallback onOpenUnit;
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
                    onPressed: onOpenUnit,
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
