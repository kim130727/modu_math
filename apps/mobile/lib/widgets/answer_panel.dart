import 'package:flutter/material.dart';

import '../l10n/app_strings.dart';
import '../models/content_models.dart';

class AnswerPanel extends StatefulWidget {
  const AnswerPanel({
    super.key,
    required this.content,
    required this.submittedAnswer,
    required this.isCorrect,
    required this.onSubmit,
    required this.onShowSolution,
  });

  final ProblemContent content;
  final String? submittedAnswer;
  final bool? isCorrect;
  final ValueChanged<String> onSubmit;
  final VoidCallback onShowSolution;

  @override
  State<AnswerPanel> createState() => _AnswerPanelState();
}

class _AnswerPanelState extends State<AnswerPanel> {
  final TextEditingController controller = TextEditingController();
  String? selectedChoice;

  @override
  void dispose() {
    controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final choices = widget.content.choices;
    final strings = AppStrings.of(context);

    return Card(
      margin: EdgeInsets.zero,
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(
              widget.content.prompt,
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 16),
            if (choices.isEmpty)
              TextField(
                controller: controller,
                style: const TextStyle(fontSize: 20),
                decoration: InputDecoration(
                  labelText: strings.t('answer.inputLabel'),
                  border: const OutlineInputBorder(),
                ),
                onSubmitted: widget.onSubmit,
              )
            else
              Wrap(
                spacing: 10,
                runSpacing: 10,
                children: choices.map((choice) {
                  final selected = selectedChoice == choice;
                  return ChoiceChip(
                    selected: selected,
                    label: Text(choice, style: const TextStyle(fontSize: 18)),
                    onSelected: (_) => setState(() => selectedChoice = choice),
                  );
                }).toList(),
              ),
            const SizedBox(height: 16),
            FilledButton(
              onPressed: () {
                final answer =
                    choices.isEmpty ? controller.text : selectedChoice;
                if (answer == null || answer.trim().isEmpty) {
                  return;
                }
                widget.onSubmit(answer);
              },
              child: Padding(
                padding: const EdgeInsets.symmetric(vertical: 12),
                child: Text(strings.t('answer.check'),
                    style: const TextStyle(fontSize: 18)),
              ),
            ),
            const SizedBox(height: 10),
            OutlinedButton(
              onPressed: widget.onShowSolution,
              child: Padding(
                padding: const EdgeInsets.symmetric(vertical: 12),
                child: Text(strings.t('answer.showSolution'),
                    style: const TextStyle(fontSize: 18)),
              ),
            ),
            if (widget.isCorrect != null) ...[
              const SizedBox(height: 14),
              _ResultBanner(
                isCorrect: widget.isCorrect!,
                answer: widget.submittedAnswer ?? '',
                correctAnswer: widget.content.correctAnswer,
              ),
            ],
          ],
        ),
      ),
    );
  }
}

class _ResultBanner extends StatelessWidget {
  const _ResultBanner({
    required this.isCorrect,
    required this.answer,
    required this.correctAnswer,
  });

  final bool isCorrect;
  final String answer;
  final String correctAnswer;

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    final colorScheme = Theme.of(context).colorScheme;
    final backgroundColor =
        isCorrect ? const Color(0xFFDCFCE7) : colorScheme.errorContainer;
    final textColor =
        isCorrect ? const Color(0xFF166534) : colorScheme.onErrorContainer;

    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: backgroundColor,
        borderRadius: BorderRadius.circular(8),
      ),
      child: Text(
        isCorrect
            ? strings.t('answer.correct')
            : strings.t('answer.incorrectWithAnswer', {
                'answer': correctAnswer,
              }),
        style: TextStyle(
          color: textColor,
          fontSize: 18,
          fontWeight: FontWeight.w800,
        ),
      ),
    );
  }
}
