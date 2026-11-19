import 'package:flutter/material.dart';
import '../l10n/assignment_strings.dart';
import '../theme/app_theme.dart';

class PracticeGoalCard extends StatelessWidget {
  const PracticeGoalCard({super.key, required this.goal});
  final Map<String, dynamic> goal;
  @override
  Widget build(BuildContext context) {
    final s = AssignmentStrings.of(context);
    final target = goal['target'] as int? ?? 5;
    final done = (goal['completed_ids'] as List? ?? []).toSet().length;
    final achieved = target > 0 && done >= target;
    return Container(
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
            color: achieved ? KidsPalette.successSoft : KidsPalette.primarySoft,
            borderRadius: BorderRadius.circular(22)),
        child:
            Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
          Row(children: [
            Icon(achieved ? Icons.emoji_events : Icons.flag_outlined,
                color: achieved ? KidsPalette.success : KidsPalette.primary,
                size: 32),
            const SizedBox(width: 12),
            Expanded(
                child: Text(s.t(achieved ? 'goalAchieved' : 'dailyGoal'),
                    style: const TextStyle(
                        fontSize: 20, fontWeight: FontWeight.bold))),
            Text('${done.clamp(0, target)} / $target',
                style:
                    const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          ]),
          const SizedBox(height: 12),
          LinearProgressIndicator(
              value: target > 0 ? (done / target).clamp(0.0, 1.0) : 0,
              minHeight: 10,
              borderRadius: BorderRadius.circular(8)),
          const SizedBox(height: 10),
          Text(s.t(achieved ? 'goalCongratulations' : 'goalHelp')),
        ]));
  }
}
