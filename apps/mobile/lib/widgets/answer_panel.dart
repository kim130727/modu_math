import 'package:flutter/material.dart';

import '../l10n/app_strings.dart';
import '../models/content_models.dart';

class AnswerPanel extends StatefulWidget {
  const AnswerPanel({
    super.key,
    required this.content,
    required this.answerDraft,
    required this.isCorrect,
    this.diagnosticFeedback,
    required this.onAnswerChanged,
    required this.onSubmit,
  });

  final ProblemContent content;
  final String answerDraft;
  final bool? isCorrect;
  final String? diagnosticFeedback;
  final ValueChanged<String> onAnswerChanged;
  final ValueChanged<String> onSubmit;

  @override
  State<AnswerPanel> createState() => _AnswerPanelState();
}

class _AnswerPanelState extends State<AnswerPanel> {
  final TextEditingController controller = TextEditingController();
  String? selectedChoice;

  @override
  void initState() {
    super.initState();
    controller.text = widget.answerDraft;
  }

  @override
  void didUpdateWidget(covariant AnswerPanel oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.answerDraft == controller.text) {
      return;
    }
    controller.text = widget.answerDraft;
    controller.selection = TextSelection.collapsed(
      offset: controller.text.length,
    );
  }

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
                onChanged: widget.onAnswerChanged,
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
                    onSelected: (_) {
                      setState(() => selectedChoice = choice);
                      widget.onAnswerChanged(choice);
                    },
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
            if (widget.isCorrect != null) ...[
              const SizedBox(height: 14),
              _ResultBanner(
                isCorrect: widget.isCorrect!,
                diagnosticFeedback: widget.diagnosticFeedback,
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
    this.diagnosticFeedback,
  });

  final bool isCorrect;
  final String? diagnosticFeedback;

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    final colorScheme = Theme.of(context).colorScheme;
    final backgroundColor =
        isCorrect ? const Color(0xFFDCFCE7) : colorScheme.errorContainer;
    final textColor =
        isCorrect ? const Color(0xFF166534) : colorScheme.onErrorContainer;

    final feedback = diagnosticFeedback?.trim() ?? '';
    final message = isCorrect
        ? strings.t('answer.correct')
        : feedback.isNotEmpty
            ? feedback
            : strings.t('answer.incorrectWithAnswer');

    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: backgroundColor,
        borderRadius: BorderRadius.circular(8),
      ),
      child: Text(
        message,
        style: TextStyle(
          color: textColor,
          fontSize: 18,
          fontWeight: FontWeight.w800,
        ),
      ),
    );
  }
}
