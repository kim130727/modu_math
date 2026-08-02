import 'dart:math' as math;

import 'package:flutter/material.dart';
import 'package:flutter_tts/flutter_tts.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;

import '../l10n/app_strings.dart';
import '../models/content_models.dart';
import '../models/tutor_models.dart';
import '../utils/tutor_text_sanitizer.dart';

class TutorChatPanel extends StatefulWidget {
  const TutorChatPanel({
    super.key,
    required this.content,
    required this.messages,
    required this.isBusy,
    required this.answerDraft,
    required this.submittedAnswer,
    required this.isCorrect,
    required this.onAnswerChanged,
    required this.onSubmit,
    required this.onSend,
    required this.onHint,
    required this.onNextStep,
    required this.onRestart,
    required this.onReset,
    required this.hasNextProblem,
    required this.onNextProblem,
    this.allowSkipProblem = false,
  });

  final ProblemContent content;
  final List<TutorMessage> messages;
  final bool isBusy;
  final String answerDraft;
  final String? submittedAnswer;
  final bool? isCorrect;
  final ValueChanged<String> onAnswerChanged;
  final ValueChanged<String> onSubmit;
  final ValueChanged<String> onSend;
  final VoidCallback onHint;
  final VoidCallback onNextStep;
  final VoidCallback onRestart;
  final VoidCallback onReset;
  final bool hasNextProblem;
  final VoidCallback onNextProblem;
  final bool allowSkipProblem;

  @override
  State<TutorChatPanel> createState() => _TutorChatPanelState();
}

class _TutorChatPanelState extends State<TutorChatPanel> {
  final TextEditingController chatController = TextEditingController();
  final TextEditingController answerController = TextEditingController();
  final FlutterTts tts = FlutterTts();
  final stt.SpeechToText speech = stt.SpeechToText();
  String? selectedChoice;
  bool voiceEnabled = true;
  bool speechAvailable = false;
  bool isListening = false;
  int lastSpokenMessageCount = 0;

  @override
  void initState() {
    super.initState();
    answerController.text = widget.answerDraft;
    _configureVoice();
  }

  @override
  void didUpdateWidget(covariant TutorChatPanel oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.content.summary.id != widget.content.summary.id) {
      selectedChoice = null;
      answerController.clear();
      chatController.clear();
    } else if (oldWidget.answerDraft != widget.answerDraft &&
        answerController.text != widget.answerDraft) {
      answerController.text = widget.answerDraft;
      answerController.selection = TextSelection.collapsed(
        offset: answerController.text.length,
      );
    }
    final newestMessage = widget.messages.lastOrNull;
    if (voiceEnabled &&
        newestMessage?.isTutor == true &&
        widget.messages.length > lastSpokenMessageCount) {
      _speakLatestTutorMessage();
    }
  }

  @override
  void dispose() {
    speech.cancel();
    tts.stop();
    chatController.dispose();
    answerController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final strings = AppStrings.of(context);
    final choices = widget.content.choices;
    final tutorChoices = widget.messages.lastWhereOrNull((message) {
          return message.isTutor && message.choices.isNotEmpty;
        })?.choices ??
        const <String>[];
    final colorScheme = Theme.of(context).colorScheme;
    final tutorActive = widget.messages.isNotEmpty;

    return Card(
      margin: EdgeInsets.zero,
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Row(
              children: [
                _AnimatedTutorAvatar(isBusy: widget.isBusy),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        strings.t('tutor.title'),
                        style: Theme.of(context).textTheme.titleMedium,
                      ),
                      Text(
                        strings.t('tutor.subtitle'),
                        style: Theme.of(context).textTheme.bodySmall?.copyWith(
                              color: colorScheme.onSurfaceVariant,
                            ),
                      ),
                    ],
                  ),
                ),
                IconButton(
                  tooltip: voiceEnabled
                      ? strings.t('tutor.voiceOffTooltip')
                      : strings.t('tutor.voiceOnTooltip'),
                  onPressed: _toggleVoice,
                  icon: Icon(
                    voiceEnabled
                        ? Icons.volume_up_outlined
                        : Icons.volume_off_outlined,
                  ),
                ),
                IconButton(
                  tooltip: strings.t('tutor.replayTooltip'),
                  onPressed: _speakLatestTutorMessage,
                  icon: const Icon(Icons.record_voice_over_outlined),
                ),
              ],
            ),
            const SizedBox(height: 12),
            _TutorActivityStrip(
              isBusy: widget.isBusy,
              latestText: _latestTutorText,
              tutorActive: tutorActive,
              strings: strings,
            ),
            const SizedBox(height: 14),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                FilledButton.tonalIcon(
                  onPressed: widget.isBusy ? null : widget.onRestart,
                  icon: const Icon(Icons.play_arrow_outlined),
                  label: Text(
                    tutorActive
                        ? strings.t('tutor.restart')
                        : strings.t('tutor.start'),
                  ),
                ),
                OutlinedButton.icon(
                  onPressed: widget.isBusy || widget.messages.isEmpty
                      ? null
                      : widget.onNextStep,
                  icon: const Icon(Icons.arrow_forward),
                  label: Text(strings.t('tutor.nextStep')),
                ),
                OutlinedButton.icon(
                  onPressed: widget.isBusy || widget.messages.isEmpty
                      ? null
                      : widget.onReset,
                  icon: const Icon(Icons.refresh),
                  label: Text(strings.t('tutor.reset')),
                ),
              ],
            ),
            const SizedBox(height: 14),
            if (choices.isEmpty)
              TextField(
                controller: answerController,
                style: const TextStyle(fontSize: 18),
                textInputAction: TextInputAction.done,
                decoration: InputDecoration(
                  labelText: strings.t('answer.inputLabel'),
                  border: const OutlineInputBorder(),
                ),
                onChanged: widget.onAnswerChanged,
                onSubmitted: _submitAnswer,
              )
            else
              Wrap(
                spacing: 10,
                runSpacing: 10,
                children: choices.map((choice) {
                  final selected = selectedChoice == choice;
                  return ChoiceChip(
                    selected: selected,
                    showCheckmark: false,
                    avatar: Icon(
                      selected
                          ? Icons.radio_button_checked
                          : Icons.radio_button_unchecked,
                      size: 19,
                    ),
                    label: Text(
                      choice,
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight:
                            selected ? FontWeight.w800 : FontWeight.w600,
                      ),
                    ),
                    labelPadding: const EdgeInsets.only(right: 8),
                    padding: const EdgeInsets.symmetric(
                      horizontal: 10,
                      vertical: 10,
                    ),
                    selectedColor: colorScheme.primaryContainer,
                    side: BorderSide(
                      color: selected
                          ? colorScheme.primary
                          : colorScheme.outlineVariant,
                    ),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8),
                    ),
                    onSelected: widget.isBusy
                        ? null
                        : (_) => setState(() => selectedChoice = choice),
                  );
                }).toList(),
              ),
            const SizedBox(height: 14),
            FilledButton.icon(
              onPressed: widget.isBusy ? null : _submitSelectedAnswer,
              icon: const Icon(Icons.check),
              label: Padding(
                padding: const EdgeInsets.symmetric(vertical: 14),
                child: Text(
                  strings.t('answer.check'),
                  style: const TextStyle(fontSize: 18),
                ),
              ),
            ),
            if (widget.isCorrect != null) ...[
              const SizedBox(height: 12),
              _ResultBanner(isCorrect: widget.isCorrect!, strings: strings),
            ],
            if (widget.allowSkipProblem || widget.isCorrect == true) ...[
              const SizedBox(height: 12),
              FilledButton.icon(
                onPressed: widget.isBusy ? null : widget.onNextProblem,
                icon: Icon(
                  widget.hasNextProblem
                      ? Icons.navigate_next
                      : Icons.check_circle_outline,
                ),
                label: Padding(
                  padding: const EdgeInsets.symmetric(vertical: 12),
                  child: Text(
                    widget.hasNextProblem
                        ? strings.t('tutor.nextProblem')
                        : strings.t('tutor.finishUnit'),
                    style: const TextStyle(fontSize: 17),
                  ),
                ),
              ),
            ],
            const SizedBox(height: 14),
            ConstrainedBox(
              constraints: const BoxConstraints(maxHeight: 390),
              child: DecoratedBox(
                decoration: BoxDecoration(
                  color: colorScheme.surfaceContainerLowest,
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: colorScheme.outlineVariant),
                ),
                child: widget.messages.isEmpty
                    ? Center(
                        child: Padding(
                          padding: const EdgeInsets.all(22),
                          child: Text(
                            strings.t('tutor.emptyConversation'),
                            textAlign: TextAlign.center,
                            style: TextStyle(
                              color: colorScheme.onSurfaceVariant,
                              fontWeight: FontWeight.w700,
                            ),
                          ),
                        ),
                      )
                    : ListView.separated(
                        padding: const EdgeInsets.all(12),
                        shrinkWrap: true,
                        itemCount: widget.messages.length,
                        separatorBuilder: (_, __) => const SizedBox(height: 10),
                        itemBuilder: (context, index) {
                          return _MessageBubble(
                            message: widget.messages[index],
                          );
                        },
                      ),
              ),
            ),
            if (widget.isBusy) ...[
              const SizedBox(height: 10),
              ClipRRect(
                borderRadius: BorderRadius.circular(8),
                child: const LinearProgressIndicator(minHeight: 4),
              ),
            ],
            if (tutorChoices.isNotEmpty) ...[
              const SizedBox(height: 12),
              Wrap(
                spacing: 8,
                runSpacing: 8,
                children: tutorChoices.indexed.map((entry) {
                  final index = entry.$1 + 1;
                  final choice = entry.$2;
                  return OutlinedButton.icon(
                    onPressed: widget.isBusy ? null : () => _send(choice),
                    icon: CircleAvatar(
                      radius: 11,
                      child: Text(
                        '$index',
                        style: const TextStyle(fontSize: 12),
                      ),
                    ),
                    label: Text(choice),
                  );
                }).toList(),
              ),
            ],
            const SizedBox(height: 14),
            Row(
              children: [
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed:
                        widget.isBusy || !tutorActive ? null : widget.onHint,
                    icon: const Icon(Icons.lightbulb_outline),
                    label: Text(strings.t('tutor.hint')),
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: widget.isBusy || !tutorActive
                        ? null
                        : widget.onNextStep,
                    icon: const Icon(Icons.arrow_forward),
                    label: Text(strings.t('tutor.nextStep')),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Row(
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                Expanded(
                  child: TextField(
                    controller: chatController,
                    enabled: tutorActive && !widget.isBusy,
                    minLines: 1,
                    maxLines: 1,
                    textInputAction: TextInputAction.send,
                    decoration: InputDecoration(
                      labelText: strings.t('tutor.chatInput'),
                      border: const OutlineInputBorder(),
                    ),
                    onSubmitted: _send,
                  ),
                ),
                const SizedBox(width: 10),
                IconButton.filledTonal(
                  tooltip: isListening
                      ? strings.t('tutor.stopListeningTooltip')
                      : strings.t('tutor.speakTooltip'),
                  onPressed:
                      widget.isBusy || !tutorActive ? null : _toggleListening,
                  icon: Icon(isListening ? Icons.mic : Icons.mic_none),
                ),
                const SizedBox(width: 8),
                IconButton.filled(
                  tooltip: strings.t('tutor.sendTooltip'),
                  onPressed: widget.isBusy || !tutorActive
                      ? null
                      : () => _send(chatController.text),
                  icon: const Icon(Icons.send),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  String get _latestTutorText {
    final text = widget.messages.where((message) => message.isTutor).lastOrNull;
    if (text == null) {
      return AppStrings.fallback.t('tutor.defaultLatest');
    }
    return sanitizeTutorText(text.text).replaceAll(RegExp(r'\s+'), ' ');
  }

  void _submitSelectedAnswer() {
    final answer = widget.content.choices.isEmpty
        ? answerController.text.trim()
        : selectedChoice;
    if (answer == null || answer.trim().isEmpty) {
      return;
    }
    widget.onAnswerChanged(answer);
    widget.onSubmit(answer);
  }

  void _submitAnswer(String value) {
    final answer = value.trim();
    if (answer.isEmpty) {
      return;
    }
    widget.onAnswerChanged(answer);
    widget.onSubmit(answer);
  }

  void _send(String value) {
    final text = sanitizeTutorText(value);
    if (text.isEmpty) {
      return;
    }
    widget.onSend(text);
    chatController.clear();
  }

  Future<void> _configureVoice() async {
    await tts.awaitSpeakCompletion(false);
    await _setVoiceLanguage();
    await tts.setSpeechRate(1);
    await tts.setVolume(1);
    await tts.setPitch(1.1);
  }

  Future<void> _setVoiceLanguage() {
    final languageCode =
        AppLocaleScope.maybeOf(context)?.locale.languageCode ?? 'ko';
    return tts.setLanguage(languageCode == 'uk' ? 'uk-UA' : 'ko-KR');
  }

  Future<void> _toggleVoice() async {
    setState(() => voiceEnabled = !voiceEnabled);
    if (voiceEnabled) {
      await _speakLatestTutorMessage();
    } else {
      await tts.stop();
    }
  }

  Future<void> _speakLatestTutorMessage() async {
    final noTextToReadMessage = AppStrings.of(context).t('tutor.noTextToRead');
    final voiceUnavailableMessage =
        AppStrings.of(context).t('tutor.voiceUnavailable');
    await _setVoiceLanguage();
    final latestTutorMessage = widget.messages.where((message) {
      return message.isTutor && sanitizeTutorText(message.text).isNotEmpty;
    }).lastOrNull;
    if (latestTutorMessage == null) {
      _showVoiceMessage(noTextToReadMessage);
      return;
    }
    final text = sanitizeTutorText(latestTutorMessage.text)
        .replaceAll(RegExp(r'\s*\n+\s*'), ' ');
    lastSpokenMessageCount = widget.messages.length;
    try {
      await tts.stop();
      await tts.speak(text);
    } catch (_) {
      _showVoiceMessage(voiceUnavailableMessage);
    }
  }

  void _showVoiceMessage(String message) {
    if (!mounted) {
      return;
    }
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message)),
    );
  }

  Future<void> _toggleListening() async {
    if (isListening) {
      await speech.stop();
      setState(() => isListening = false);
      final text = chatController.text.trim();
      if (text.isNotEmpty) {
        _send(text);
      }
      return;
    }

    if (!speechAvailable) {
      final available = await speech.initialize(
        onStatus: (status) {
          if (!mounted) {
            return;
          }
          setState(() => isListening = status == 'listening');
        },
        onError: (_) {
          if (!mounted) {
            return;
          }
          setState(() => isListening = false);
        },
      );
      if (!mounted) {
        return;
      }
      setState(() => speechAvailable = available);
      if (!available) {
        return;
      }
    }

    final speechLocaleId =
        AppLocaleScope.maybeOf(context)?.locale.languageCode == 'uk'
            ? 'uk_UA'
            : 'ko_KR';
    await tts.stop();
    await speech.listen(
      listenOptions: stt.SpeechListenOptions(
        localeId: speechLocaleId,
        partialResults: true,
        listenFor: const Duration(seconds: 12),
        pauseFor: const Duration(seconds: 3),
      ),
      onResult: (result) {
        final text = sanitizeTutorText(result.recognizedWords);
        chatController.text = text;
        chatController.selection = TextSelection.collapsed(offset: text.length);
        if (result.finalResult && text.isNotEmpty) {
          speech.stop();
          setState(() => isListening = false);
          _send(text);
        }
      },
    );
    if (mounted) {
      setState(() => isListening = true);
    }
  }
}

class _AnimatedTutorAvatar extends StatefulWidget {
  const _AnimatedTutorAvatar({required this.isBusy});

  final bool isBusy;

  @override
  State<_AnimatedTutorAvatar> createState() => _AnimatedTutorAvatarState();
}

class _AnimatedTutorAvatarState extends State<_AnimatedTutorAvatar>
    with SingleTickerProviderStateMixin {
  late final AnimationController controller;

  @override
  void initState() {
    super.initState();
    controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1600),
    )..repeat();
  }

  @override
  void dispose() {
    controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;
    return AnimatedBuilder(
      animation: controller,
      builder: (context, child) {
        final wave = math.sin(controller.value * math.pi * 2);
        final bounce = -3.0 + wave * 3.0;
        final tilt = widget.isBusy ? wave * 0.12 : wave * 0.06;
        return Transform.translate(
          offset: Offset(0, bounce),
          child: Transform.rotate(angle: tilt, child: child),
        );
      },
      child: SizedBox(
        width: 54,
        height: 54,
        child: Stack(
          clipBehavior: Clip.none,
          children: [
            Positioned.fill(
              child: DecoratedBox(
                decoration: BoxDecoration(
                  color: colorScheme.primaryContainer,
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(
                    color: colorScheme.primary.withValues(alpha: 0.22),
                  ),
                ),
                child: Icon(
                  Icons.smart_toy_outlined,
                  color: colorScheme.onPrimaryContainer,
                  size: 31,
                ),
              ),
            ),
            Positioned(
              right: -2,
              top: -3,
              child: _PulseDot(active: widget.isBusy),
            ),
          ],
        ),
      ),
    );
  }
}

class _PulseDot extends StatelessWidget {
  const _PulseDot({required this.active});

  final bool active;

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;
    return Container(
      width: 14,
      height: 14,
      decoration: BoxDecoration(
        color: active ? colorScheme.tertiary : const Color(0xFF22C55E),
        shape: BoxShape.circle,
        border: Border.all(color: colorScheme.surface, width: 2),
      ),
    );
  }
}

class _TutorActivityStrip extends StatelessWidget {
  const _TutorActivityStrip({
    required this.isBusy,
    required this.latestText,
    required this.tutorActive,
    required this.strings,
  });

  final bool isBusy;
  final String latestText;
  final bool tutorActive;
  final AppStrings strings;

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;
    final text = isBusy
        ? strings.t('tutor.thinking')
        : tutorActive
            ? latestText
            : strings.t('tutor.firstQuestionPlaceholder');
    return DecoratedBox(
      decoration: BoxDecoration(
        color: colorScheme.secondaryContainer.withValues(alpha: 0.42),
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: colorScheme.outlineVariant),
      ),
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Row(
          children: [
            Icon(
              isBusy ? Icons.more_horiz : Icons.chat_bubble_outline,
              color: colorScheme.onSecondaryContainer,
            ),
            const SizedBox(width: 10),
            Expanded(
              child: Text(
                text,
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
                style: TextStyle(
                  color: colorScheme.onSecondaryContainer,
                  fontWeight: FontWeight.w800,
                  height: 1.35,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _ResultBanner extends StatelessWidget {
  const _ResultBanner({required this.isCorrect, required this.strings});

  final bool isCorrect;
  final AppStrings strings;

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;
    final backgroundColor =
        isCorrect ? const Color(0xFFDCFCE7) : colorScheme.tertiaryContainer;
    final textColor =
        isCorrect ? const Color(0xFF166534) : colorScheme.onTertiaryContainer;

    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: backgroundColor,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(
          color: isCorrect ? const Color(0xFF86EFAC) : colorScheme.tertiary,
        ),
      ),
      child: Text(
        isCorrect
            ? strings.t('tutor.correctReview')
            : strings.t('tutor.incorrectReview'),
        style: TextStyle(
          color: textColor,
          fontSize: 16,
          fontWeight: FontWeight.w800,
        ),
      ),
    );
  }
}

class _MessageBubble extends StatelessWidget {
  const _MessageBubble({required this.message});

  final TutorMessage message;

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;
    final isTutor = message.isTutor;
    final bubbleColor =
        isTutor ? colorScheme.surface : colorScheme.primaryContainer;
    final textColor =
        isTutor ? colorScheme.onSurface : colorScheme.onPrimaryContainer;

    return Align(
      alignment: isTutor ? Alignment.centerLeft : Alignment.centerRight,
      child: Container(
        constraints: const BoxConstraints(maxWidth: 520),
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 11),
        decoration: BoxDecoration(
          color: bubbleColor,
          borderRadius: BorderRadius.circular(8),
          border: Border.all(
            color: isTutor ? colorScheme.outlineVariant : colorScheme.primary,
          ),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(
                  isTutor ? Icons.smart_toy_outlined : Icons.face_outlined,
                  size: 15,
                  color: textColor.withValues(alpha: 0.72),
                ),
                const SizedBox(width: 5),
                Text(
                  isTutor
                      ? AppStrings.of(context).t('tutor.title')
                      : AppStrings.of(context).t('tutor.student'),
                  style: TextStyle(
                    color: textColor.withValues(alpha: 0.72),
                    fontSize: 12,
                    fontWeight: FontWeight.w700,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 4),
            Text(
              sanitizeTutorText(message.text),
              style: TextStyle(
                color: textColor,
                fontSize: 15.5,
                height: 1.35,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

extension _IterableLastOrNull<T> on Iterable<T> {
  T? get lastOrNull {
    T? value;
    for (final item in this) {
      value = item;
    }
    return value;
  }

  T? lastWhereOrNull(bool Function(T item) test) {
    T? value;
    for (final item in this) {
      if (test(item)) {
        value = item;
      }
    }
    return value;
  }
}
