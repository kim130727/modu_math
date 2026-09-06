import 'dart:math' as math;

import '../models/content_models.dart';

final _visualCache = Expando<Map<String, dynamic>>();

/// A display-only projection. Authored data remains available for grading,
/// hints and editing. Unknown visual content is deliberately preserved.
Map<String, dynamic> problemVisualRenderer(ProblemContent content) {
  return _visualCache[content] ??= _projectVisual(content);
}

Map<String, dynamic> _projectVisual(ProblemContent content) {
  final renderer = content.renderer;
  final raw = renderer['elements'];
  if (raw is! List) return renderer;
  String normalize(String value) => value.replaceAll(RegExp(r'\s+'), '');
  final prompt = normalize(content.prompt);
  String choiceText(String value) => normalize(value)
      .replaceFirst(RegExp(r'^(?:\([1-9]\)|[①-⑩]|[1-9][.)])'), '');
  final choices = content.choices.map(choiceText).toSet();
  final removed = <Map>[];
  final kept = <dynamic>[];

  // Discover any slots explicitly designated as instruction/question or choice in layout
  final questionSlotIds = <String>{};
  final choiceSlotIds = <String>{};
  final regions = content.layout['regions'];
  if (regions is List) {
    for (final reg in regions) {
      if (reg is Map) {
        final role = reg['role']?.toString().toLowerCase();
        final slotIds = reg['slot_ids'];
        if (slotIds is List) {
          final ids = slotIds.map((id) => id.toString().toLowerCase());
          if (role == 'instruction' || role == 'question') {
            questionSlotIds.addAll(ids);
          } else if (role == 'choices' ||
              role == 'choice' ||
              role == 'options' ||
              role == 'option') {
            choiceSlotIds.addAll(ids);
          }
        }
      }
    }
  }
  final slots = content.layout['slots'];
  if (slots is List) {
    for (final slot in slots) {
      if (slot is Map) {
        final slotContent = slot['content'];
        if (slotContent is Map) {
          final styleRole =
              slotContent['style_role']?.toString().toLowerCase();
          final semanticRole =
              slotContent['semantic_role']?.toString().toLowerCase();
          final id = slot['id']?.toString().toLowerCase();
          if (id != null && id.isNotEmpty) {
            if (styleRole == 'question' ||
                styleRole == 'instruction' ||
                semanticRole == 'question' ||
                semanticRole == 'instruction') {
              questionSlotIds.add(id);
            } else if (styleRole == 'choice' ||
                styleRole == 'choices' ||
                styleRole == 'option' ||
                semanticRole == 'choice' ||
                semanticRole == 'option') {
              choiceSlotIds.add(id);
            }
          }
        }
      }
    }
  }

  for (final element in raw) {
    if (element is! Map) {
      kept.add(element);
      continue;
    }
    final attributes = element['attributes'];
    final role = attributes is Map
        ? attributes['data-semantic-role']?.toString().toLowerCase() ?? ''
        : '';
    final text = normalize(element['text']?.toString() ?? '');
    final sourceRef = (element['source_ref'] ?? '').toString().toLowerCase();
    final refs = element['refs'];
    final layoutSlotId = (refs is Map ? refs['layout_slot_id'] : '')
            ?.toString()
            .toLowerCase() ??
        '';
    final identity =
        '${element['id']} $sourceRef $layoutSlotId ${element['refs']} ${element['metadata']}'
            .toLowerCase();

    final isExplicitQuestionSlot = questionSlotIds.contains(sourceRef) ||
        questionSlotIds.contains(layoutSlotId) ||
        questionSlotIds.any((id) => identity.contains(id));

    final isPromptRole = isExplicitQuestionSlot ||
        role == 'question' ||
        role == 'instruction' ||
        RegExp(r'\b(?:instruction|question|slot\.q\d*)\b').hasMatch(identity);

    final hasLabelMarker = identity.contains('.lb.') ||
        identity.contains('.lb') ||
        identity.contains('_lb_') ||
        identity.contains('label');

    // Labels attached to diagrams, points, holes, or geometry must stay on Canvas.
    final isDiagramLabel = hasLabelMarker ||
        role == 'label' ||
        (role == 'symbol_label' &&
            !RegExp(r'\b(?:slot\.opt\d*)\b').hasMatch(identity));

    final promptMatches = prompt.isNotEmpty &&
        text.isNotEmpty &&
        (prompt == text ||
            (text.length >= 6 &&
                (prompt.contains(text) ||
                    text.contains(prompt) ||
                    (text.length >= 10 &&
                        prompt.length >= 10 &&
                        prompt.substring(0, math.min(15, prompt.length)) ==
                            text.substring(0, math.min(15, text.length))))));

    final isPrompt = text.isNotEmpty &&
        !isDiagramLabel &&
        (prompt == text ||
            (isPromptRole && (promptMatches || prompt.isEmpty)));

    final isExplicitChoiceSlot = choiceSlotIds.contains(sourceRef) ||
        choiceSlotIds.contains(layoutSlotId) ||
        choiceSlotIds.any((id) => identity.contains(id));

    final isChoiceRole = (role == 'choice' ||
            role == 'option' ||
            isExplicitChoiceSlot ||
            RegExp(r'\b(?:choice|option|slot\.c\d+|slot\.opt\d*)\b')
                .hasMatch(identity)) &&
        !hasLabelMarker;

    final isChoice = text.isNotEmpty &&
        !isDiagramLabel &&
        isChoiceRole &&
        (choices.contains(choiceText(text)) ||
            (content.choices.isNotEmpty && isExplicitChoiceSlot));

    if (isPrompt || isChoice) {
      removed.add(element);
    } else {
      kept.add(element);
    }
  }
  if (removed.isEmpty) return renderer;
  // Remove a choice frame only when it contains solely the moved text.
  kept.removeWhere((element) {
    if (element is! Map ||
        element['type'] != 'rect' ||
        !RegExp(r'choice|option')
            .hasMatch('${element['id']} ${element['source_ref']}')) {
      return false;
    }
    final box = _bounds(element);
    if (box == null) return false;
    bool inside(Map other) {
      final bounds = _bounds(other);
      return bounds != null &&
          bounds.$1 >= box.$1 &&
          bounds.$2 >= box.$2 &&
          bounds.$3 <= box.$3 &&
          bounds.$4 <= box.$4;
    }

    return removed.any(inside) &&
        !kept.any((other) =>
            other is Map && !identical(other, element) && inside(other));
  });
  final result = <String, dynamic>{...renderer, 'elements': kept};
  // Fit the remaining artwork without altering any authored coordinates.
  final bounds = kept.whereType<Map>().map(_bounds).toList();
  if (bounds.isNotEmpty && bounds.every((b) => b != null)) {
    final boxes = bounds.whereType<(double, double, double, double)>();
    final left = boxes.map((b) => b.$1).reduce(math.min) - 24;
    final top = boxes.map((b) => b.$2).reduce(math.min) - 24;
    final right = boxes.map((b) => b.$3).reduce(math.max) + 24;
    final bottom = boxes.map((b) => b.$4).reduce(math.max) + 24;
    result['presentation_viewport'] = {
      'x': left,
      'y': top,
      'width': right - left,
      'height': bottom - top,
    };
  }
  return result;
}

(double, double, double, double)? _bounds(Map element) {
  final a = element['attributes'];
  if (a is! Map || a.containsKey('transform')) return null;
  double n(String key, [double fallback = 0]) =>
      double.tryParse('${a[key]}') ?? fallback;
  final x = n('x'), y = n('y');
  switch (element['type']) {
    case 'rect':
    case 'image':
      return (x, y, x + n('width'), y + n('height'));
    case 'line':
      return (
        math.min(n('x1'), n('x2')),
        math.min(n('y1'), n('y2')),
        math.max(n('x1'), n('x2')),
        math.max(n('y1'), n('y2'))
      );
    case 'circle':
      return (
        n('cx') - n('r'),
        n('cy') - n('r'),
        n('cx') + n('r'),
        n('cy') + n('r')
      );
    case 'text':
      final size = n('font-size', 16);
      final lines = '${element['text'] ?? ''}'.split('\n');
      final width = lines
              .map((s) => s.runes.fold<double>(
                  0, (sum, rune) => sum + (rune < 128 ? 0.65 : 1.05)))
              .reduce(math.max) *
          size;
      final anchor = a['text-anchor'];
      final left = x -
          (anchor == 'middle'
              ? width / 2
              : anchor == 'end'
                  ? width
                  : 0);
      return (left, y - size * 1.3, left + width, y + size * lines.length);
    default:
      return null;
  }
}
