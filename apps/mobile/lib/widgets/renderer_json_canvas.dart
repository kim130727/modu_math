import 'dart:math' as math;

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:google_fonts/google_fonts.dart';

class RendererJsonCanvas extends StatefulWidget {
  const RendererJsonCanvas({
    super.key,
    required this.renderer,
    this.inputValue = '',
    this.expectedAnswer = '',
    this.suppressInputs = false,
    this.onInputChanged,
  });

  final Map<String, dynamic> renderer;
  final String inputValue;
  final String expectedAnswer;
  final bool suppressInputs;
  final ValueChanged<String>? onInputChanged;

  @override
  State<RendererJsonCanvas> createState() => _RendererJsonCanvasState();
}

class _RendererJsonCanvasState extends State<RendererJsonCanvas> {
  final List<TextEditingController> inputControllers = [];
  String inputSignature = '';
  String? lastEmittedInputValue;
  int? activeOperatorSlotIndex;

  @override
  void initState() {
    super.initState();
    _syncInputControllers(force: true);
  }

  @override
  void didUpdateWidget(covariant RendererJsonCanvas oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.renderer != widget.renderer) {
      activeOperatorSlotIndex = null;
    }
    final inputChangedFromThisCanvas =
        widget.inputValue == lastEmittedInputValue &&
            oldWidget.renderer == widget.renderer;
    _syncInputControllers(
      force: oldWidget.renderer != widget.renderer ||
          (oldWidget.inputValue != widget.inputValue &&
              !inputChangedFromThisCanvas),
    );
  }

  @override
  void dispose() {
    for (final controller in inputControllers) {
      controller.dispose();
    }
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final viewBox = _mapAt(widget.renderer, 'view_box');
    final width = _readDouble(viewBox['width']) ?? 928;
    final height = _readDouble(viewBox['height']) ?? 426;
    final background = _readColor(viewBox['background']) ?? Colors.white;

    final inputSlots = _inputSlots(
      widget.renderer,
      expectedAnswer: widget.expectedAnswer,
      suppressInputs: widget.suppressInputs,
    );
    _ensureControllerCount(inputSlots.length);
    final hasOperatorSlots =
        inputSlots.any((slot) => slot.operatorOnly);

    return LayoutBuilder(
      builder: (context, constraints) {
        final double maxW =
            constraints.maxWidth.isFinite ? constraints.maxWidth : width;
        final double maxH =
            constraints.maxHeight.isFinite ? constraints.maxHeight : double.infinity;

        final double operatorBarReservedHeight =
            hasOperatorSlots ? 52.0 : 0.0;
        final double availableHeight =
            (maxH - operatorBarReservedHeight).clamp(0.0, double.infinity);

        double canvasWidth = maxW;
        double canvasHeight = canvasWidth * (height / width);

        if (canvasHeight > availableHeight && availableHeight > 0) {
          canvasHeight = availableHeight;
          canvasWidth = canvasHeight * (width / height);
        }

        final scale = canvasWidth / width;

        return Center(
          child: SizedBox(
            width: canvasWidth,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                DecoratedBox(
                  decoration: BoxDecoration(
                    color: background,
                    border: Border.all(
                      color: Theme.of(context).colorScheme.outlineVariant,
                    ),
                  ),
                  child: SizedBox(
                    width: canvasWidth,
                    height: canvasHeight,
                    child: Stack(
                      clipBehavior: Clip.hardEdge,
                      children: [
                        Positioned.fill(
                          child: CustomPaint(
                            painter: RendererJsonPainter(
                              renderer: widget.renderer,
                              logicalSize: Size(width, height),
                            ),
                          ),
                        ),
                        ..._textBoxLayers(widget.renderer, scale),
                        ..._inputLayers(inputSlots, scale),
                      ],
                    ),
                  ),
                ),
                if (hasOperatorSlots) ...[
                  const SizedBox(height: 10),
                  _operatorChoiceBar(inputSlots),
                ],
              ],
            ),
          ),
        );
      },
    );
  }

  List<Widget> _inputLayers(List<_InputSlot> slots, double scale) {
    final colorScheme = Theme.of(context).colorScheme;
    return slots.indexed.map((entry) {
      final index = entry.$1;
      final slot = entry.$2;
      final rect = slot.rect;
      final fontSize = _inputFontSize(slot, scale);
      final maxLength = slot.maxLength;
      final inset = (2 * scale).clamp(1.0, 3.0);
      if (slot.operatorOnly) {
        return _operatorInputLayer(
          index: index,
          slot: slot,
          scale: scale,
          inset: inset,
          fontSize: fontSize,
        );
      }
      final textColor = slot.drawPlaceholderBehind
          ? Colors.transparent
          : colorScheme.onSurface;
      return Positioned(
        left: rect.left * scale + inset,
        top: rect.top * scale + inset,
        width: rect.width * scale - inset * 2,
        height: rect.height * scale - inset * 2,
        child: Stack(
          fit: StackFit.expand,
          children: [
            if (slot.drawPlaceholderBehind)
              IgnorePointer(
                child: Center(
                  child: Text(
                    slot.placeholder!,
                    textAlign: TextAlign.center,
                    style: _problemTextStyle(
                      color: colorScheme.onSurface,
                      fontSize: (rect.height * 0.86 * scale).clamp(18.0, 52.0),
                      fontWeight: FontWeight.w500,
                      height: 1,
                    ),
                  ),
                ),
              ),
            TextField(
              controller: inputControllers[index],
              textAlign: TextAlign.center,
              textAlignVertical: TextAlignVertical.center,
              keyboardType:
                  slot.digitsOnly ? TextInputType.number : TextInputType.text,
              inputFormatters: [
                if (slot.digitsOnly) FilteringTextInputFormatter.digitsOnly,
                if (slot.operatorOnly)
                  FilteringTextInputFormatter.allow(RegExp(r'[<>=]')),
                LengthLimitingTextInputFormatter(maxLength),
              ],
              style: _problemTextStyle(
                color: textColor,
                fontSize: fontSize,
                fontWeight: FontWeight.w800,
                height: 1,
              ),
              cursorHeight: fontSize,
              cursorColor:
                  slot.drawPlaceholderBehind ? Colors.transparent : null,
              decoration: InputDecoration(
                border: InputBorder.none,
                enabledBorder: InputBorder.none,
                focusedBorder: InputBorder.none,
                disabledBorder: InputBorder.none,
                errorBorder: InputBorder.none,
                focusedErrorBorder: InputBorder.none,
                filled: false,
                hoverColor: Colors.transparent,
                hintText: slot.drawPlaceholderBehind ? null : slot.placeholder,
                hintStyle: _problemTextStyle(
                  color: colorScheme.onSurface,
                  fontSize: fontSize,
                  fontWeight: FontWeight.w800,
                  height: 1,
                ),
                counterText: '',
                contentPadding: EdgeInsets.zero,
                isCollapsed: true,
              ),
              onChanged: (value) {
                if (slot.autoAdvance &&
                    value.length >= maxLength &&
                    index + 1 < inputControllers.length) {
                  FocusScope.of(context).nextFocus();
                }
                final nextValue = _combinedInputValue();
                lastEmittedInputValue = nextValue;
                if (slot.drawPlaceholderBehind) {
                  setState(() {});
                }
                widget.onInputChanged?.call(nextValue);
              },
            ),
            if (slot.drawPlaceholderBehind)
              IgnorePointer(
                child: Center(
                  child: Text(
                    inputControllers[index].text,
                    textAlign: TextAlign.center,
                    style: _problemTextStyle(
                      color: colorScheme.onSurface,
                      fontSize: fontSize,
                      fontWeight: FontWeight.w800,
                      height: 1,
                    ),
                  ),
                ),
              ),
          ],
        ),
      );
    }).toList(growable: false);
  }

  Widget _operatorInputLayer({
    required int index,
    required _InputSlot slot,
    required double scale,
    required double inset,
    required double fontSize,
  }) {
    final colorScheme = Theme.of(context).colorScheme;
    final rect = slot.rect;
    final selected = _activeOperatorSlotIndex(_inputSlots(
          widget.renderer,
          expectedAnswer: widget.expectedAnswer,
          suppressInputs: widget.suppressInputs,
        )) ==
        index;
    return Positioned(
      left: rect.left * scale + inset,
      top: rect.top * scale + inset,
      width: rect.width * scale - inset * 2,
      height: rect.height * scale - inset * 2,
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          key: ValueKey('operator-slot-$index'),
          borderRadius: BorderRadius.circular(999),
          onTap: () => setState(() => activeOperatorSlotIndex = index),
          child: DecoratedBox(
            decoration: BoxDecoration(
              color: selected
                  ? colorScheme.primary.withValues(alpha: 0.08)
                  : Colors.transparent,
              shape: BoxShape.circle,
              border: selected
                  ? Border.all(color: colorScheme.primary, width: 1.8)
                  : null,
            ),
            child: Stack(
              fit: StackFit.expand,
              children: [
                if (slot.placeholder != null && slot.placeholder!.isNotEmpty)
                  Center(
                    child: Text(
                      slot.placeholder!,
                      textAlign: TextAlign.center,
                      style: _problemTextStyle(
                        color: colorScheme.onSurface,
                        fontSize:
                            (rect.height * 0.86 * scale).clamp(18.0, 52.0),
                        fontWeight: FontWeight.w500,
                        height: 1,
                      ),
                    ),
                  ),
                Center(
                  child: Text(
                    inputControllers[index].text,
                    textAlign: TextAlign.center,
                    style: _problemTextStyle(
                      color: colorScheme.onSurface,
                      fontSize: fontSize,
                      fontWeight: FontWeight.w800,
                      height: 1,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _operatorChoiceBar(List<_InputSlot> slots) {
    final operatorIndexes = slots.indexed
        .where((entry) => entry.$2.operatorOnly)
        .map((entry) => entry.$1)
        .toList();
    if (operatorIndexes.isEmpty) {
      return const SizedBox.shrink();
    }
    final colorScheme = Theme.of(context).colorScheme;
    final selectedIndex = _activeOperatorSlotIndex(slots);
    final selectedValue = inputControllers[selectedIndex].text;
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Align(
        alignment: Alignment.center,
        child: Material(
          color: colorScheme.surface,
          borderRadius: BorderRadius.circular(8),
          elevation: 1,
          child: Container(
            decoration: BoxDecoration(
              border: Border.all(color: colorScheme.outlineVariant),
              borderRadius: BorderRadius.circular(8),
            ),
            padding: const EdgeInsets.all(6),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: ['>', '=', '<'].map((operator) {
                final selected = selectedValue == operator;
                return Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 3),
                  child: SizedBox(
                    width: 46,
                    height: 40,
                    child: selected
                        ? FilledButton(
                            key: ValueKey('operator-choice-$operator'),
                            onPressed: () => _setOperatorValue(operator, slots),
                            style: FilledButton.styleFrom(
                              padding: EdgeInsets.zero,
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(8),
                              ),
                            ),
                            child: Text(
                              operator,
                              style: const TextStyle(fontSize: 22),
                            ),
                          )
                        : OutlinedButton(
                            key: ValueKey('operator-choice-$operator'),
                            onPressed: () => _setOperatorValue(operator, slots),
                            style: OutlinedButton.styleFrom(
                              padding: EdgeInsets.zero,
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(8),
                              ),
                            ),
                            child: Text(
                              operator,
                              style: const TextStyle(fontSize: 22),
                            ),
                          ),
                  ),
                );
              }).toList(),
            ),
          ),
        ),
      ),
    );
  }

  void _syncInputControllers({required bool force}) {
    final slots = _inputSlots(
      widget.renderer,
      expectedAnswer: widget.expectedAnswer,
      suppressInputs: widget.suppressInputs,
    );
    final signature = slots.map((slot) => slot.signature).join('|');
    if (!force && inputSignature == signature) {
      return;
    }
    inputSignature = signature;
    _ensureControllerCount(slots.length);
    final chars = widget.inputValue.characters.toList();
    for (var i = 0; i < inputControllers.length; i += 1) {
      final value = _inputValueForController(slots, chars, i);
      if (inputControllers[i].text != value) {
        inputControllers[i].text = value;
      }
    }
  }

  void _ensureControllerCount(int count) {
    while (inputControllers.length < count) {
      inputControllers.add(TextEditingController());
    }
    while (inputControllers.length > count) {
      inputControllers.removeLast().dispose();
    }
  }

  String _combinedInputValue() {
    final slots = _inputSlots(
      widget.renderer,
      expectedAnswer: widget.expectedAnswer,
      suppressInputs: widget.suppressInputs,
    );
    final answerIndexes = slots.indexed
        .where((entry) => entry.$2.contributesToAnswer)
        .map((entry) => entry.$1)
        .toList();
    final indexes = answerIndexes.isEmpty
        ? List<int>.generate(inputControllers.length, (index) => index)
        : answerIndexes;
    return indexes.map((index) => inputControllers[index].text).join().trim();
  }

  int _activeOperatorSlotIndex(List<_InputSlot> slots) {
    final operatorIndexes = slots.indexed
        .where((entry) => entry.$2.operatorOnly)
        .map((entry) => entry.$1)
        .toList();
    if (operatorIndexes.isEmpty) {
      return 0;
    }
    if (activeOperatorSlotIndex != null &&
        operatorIndexes.contains(activeOperatorSlotIndex)) {
      return activeOperatorSlotIndex!;
    }
    return operatorIndexes.firstWhere(
      (index) => inputControllers[index].text.isEmpty,
      orElse: () => operatorIndexes.first,
    );
  }

  void _setOperatorValue(String operator, List<_InputSlot> slots) {
    final index = _activeOperatorSlotIndex(slots);
    inputControllers[index].text = operator;
    final nextValue = _combinedInputValue();
    lastEmittedInputValue = nextValue;
    final operatorIndexes = slots.indexed
        .where((entry) => entry.$2.operatorOnly)
        .map((entry) => entry.$1)
        .toList();
    final currentOperatorPosition = operatorIndexes.indexOf(index);
    int? nextIndex;
    for (final item in operatorIndexes.skip(currentOperatorPosition + 1)) {
      if (inputControllers[item].text.isEmpty) {
        nextIndex = item;
        break;
      }
    }
    setState(() {
      activeOperatorSlotIndex = nextIndex ?? index;
    });
    widget.onInputChanged?.call(nextValue);
  }

  String _inputValueForController(
    List<_InputSlot> slots,
    List<String> chars,
    int controllerIndex,
  ) {
    final answerIndexes = slots.indexed
        .where((entry) => entry.$2.contributesToAnswer)
        .map((entry) => entry.$1)
        .toList();
    if (answerIndexes.isEmpty) {
      final start = slots
          .take(controllerIndex)
          .fold<int>(0, (total, slot) => total + slot.maxLength);
      return _sliceCharacters(chars, start, slots[controllerIndex].maxLength);
    }
    final answerPosition = answerIndexes.indexOf(controllerIndex);
    if (answerPosition < 0) {
      return '';
    }
    final start = answerIndexes
        .take(answerPosition)
        .fold<int>(0, (total, index) => total + slots[index].maxLength);
    return _sliceCharacters(chars, start, slots[controllerIndex].maxLength);
  }
}

class RendererJsonPainter extends CustomPainter {
  const RendererJsonPainter({
    required this.renderer,
    required this.logicalSize,
  });

  final Map<String, dynamic> renderer;
  final Size logicalSize;

  @override
  void paint(Canvas canvas, Size size) {
    final scale = (size.width / logicalSize.width)
        .clamp(0.0, size.height / logicalSize.height);
    final dx = (size.width - logicalSize.width * scale) / 2;
    final dy = (size.height - logicalSize.height * scale) / 2;

    canvas
      ..save()
      ..translate(dx, dy)
      ..scale(scale);

    final elements = renderer['elements'];
    if (elements is List) {
      for (final element in rendererVisibleElements(elements)) {
        _paintElement(canvas, element);
      }
    }

    canvas.restore();
  }

  void _paintElement(Canvas canvas, Map<String, dynamic> element) {
    final type = element['type']?.toString();
    final attributes = _mapAt(element, 'attributes');
    switch (type) {
      case 'circle':
        _paintCircle(canvas, attributes);
      case 'line':
        _paintLine(canvas, attributes);
      case 'rect':
        _paintRect(canvas, attributes);
      case 'polygon':
        _paintPolygon(canvas, attributes);
      case 'path':
        _paintPath(canvas, attributes);
      case 'text':
        _paintText(canvas, element, attributes);
    }
  }

  void _paintCircle(Canvas canvas, Map<String, dynamic> attributes) {
    final center = Offset(
      _readDouble(attributes['cx']) ?? 0,
      _readDouble(attributes['cy']) ?? 0,
    );
    final radius = _readDouble(attributes['r']) ?? 0;
    final fill = _readColor(attributes['fill']);
    final strokeAttr = attributes['stroke']?.toString().trim().toLowerCase();
    final stroke = strokeAttr == 'none'
        ? null
        : (_readColor(attributes['stroke']) ?? (strokeAttr == null ? null : Colors.black));
    final strokeWidth = _readDouble(attributes['stroke-width']) ?? 1;

    if (fill != null) {
      canvas.drawCircle(center, radius, Paint()..color = fill);
    }
    if (stroke != null && strokeWidth > 0) {
      canvas.drawCircle(
        center,
        radius,
        Paint()
          ..color = stroke
          ..style = PaintingStyle.stroke
          ..strokeWidth = strokeWidth,
      );
    }
  }

  void _paintLine(Canvas canvas, Map<String, dynamic> attributes) {
    final strokeAttr = attributes['stroke']?.toString().trim().toLowerCase();
    if (strokeAttr == 'none') {
      return;
    }
    final stroke = _readColor(attributes['stroke']) ?? Colors.black;
    final strokeWidth = _readDouble(attributes['stroke-width']) ?? 1;
    if (strokeWidth <= 0) {
      return;
    }
    final start = Offset(
      _readDouble(attributes['x1']) ?? 0,
      _readDouble(attributes['y1']) ?? 0,
    );
    final end = Offset(
      _readDouble(attributes['x2']) ?? 0,
      _readDouble(attributes['y2']) ?? 0,
    );
    final paint = Paint()
      ..color = stroke
      ..strokeWidth = strokeWidth
      ..strokeCap = StrokeCap.round;
    final dashArray = _readDashArray(attributes['stroke-dasharray']);
    if (dashArray == null) {
      canvas.drawLine(start, end, paint);
      return;
    }
    _drawDashedLine(canvas, start, end, paint, dashArray);
  }

  void _paintRect(Canvas canvas, Map<String, dynamic> attributes) {
    final rect = Rect.fromLTWH(
      _readDouble(attributes['x']) ?? 0,
      _readDouble(attributes['y']) ?? 0,
      _readDouble(attributes['width']) ?? 0,
      _readDouble(attributes['height']) ?? 0,
    );
    final fill = _readColor(attributes['fill']);
    final strokeAttr = attributes['stroke']?.toString().trim().toLowerCase();
    final stroke = strokeAttr == 'none'
        ? null
        : (_readColor(attributes['stroke']) ?? (strokeAttr == null ? null : Colors.black));
    final strokeWidth = _readDouble(attributes['stroke-width']) ?? 1;

    if (fill != null) {
      canvas.drawRect(rect, Paint()..color = fill);
    }
    if (stroke != null && strokeWidth > 0) {
      canvas.drawRect(
        rect,
        Paint()
          ..color = stroke
          ..style = PaintingStyle.stroke
          ..strokeWidth = strokeWidth,
      );
    }
  }

  void _drawDashedLine(
    Canvas canvas,
    Offset start,
    Offset end,
    Paint paint,
    List<double> dashArray,
  ) {
    final vector = end - start;
    final distance = vector.distance;
    if (distance == 0) {
      return;
    }
    final direction = vector / distance;
    var travelled = 0.0;
    var dashIndex = 0;
    var draw = true;

    while (travelled < distance) {
      final segmentLength = dashArray[dashIndex % dashArray.length];
      final nextTravelled = (travelled + segmentLength).clamp(0.0, distance);
      if (draw) {
        canvas.drawLine(
          start + direction * travelled,
          start + direction * nextTravelled,
          paint,
        );
      }
      travelled = nextTravelled;
      dashIndex += 1;
      draw = !draw;
    }
  }

  void _paintPolygon(Canvas canvas, Map<String, dynamic> attributes) {
    final path = rendererPolygonPath(attributes['points']);
    if (path == null) {
      return;
    }
    final fill = _readColor(attributes['fill']);
    final stroke = _readColor(attributes['stroke']);
    final strokeWidth = _readDouble(attributes['stroke-width']) ?? 1;

    if (fill != null) {
      canvas.drawPath(path, Paint()..color = fill);
    }
    if (stroke != null && strokeWidth > 0) {
      canvas.drawPath(
        path,
        Paint()
          ..color = stroke
          ..style = PaintingStyle.stroke
          ..strokeWidth = strokeWidth
          ..strokeCap = StrokeCap.round
          ..strokeJoin = StrokeJoin.round,
      );
    }
  }

  void _paintPath(Canvas canvas, Map<String, dynamic> attributes) {
    final path = _parseSvgPath(attributes['d']?.toString() ?? '');
    if (path == null) {
      return;
    }
    final fill = _readColor(attributes['fill']);
    final stroke = _readColor(attributes['stroke']);
    final strokeWidth = _readDouble(attributes['stroke-width']) ?? 1;

    if (fill != null) {
      canvas.drawPath(path, Paint()..color = fill);
    }
    if (stroke != null && strokeWidth > 0) {
      canvas.drawPath(
        path,
        Paint()
          ..color = stroke
          ..style = PaintingStyle.stroke
          ..strokeWidth = strokeWidth
          ..strokeCap = StrokeCap.round
          ..strokeJoin = StrokeJoin.round,
      );
    }
  }

  String _normalizeRenderText(String text) {
    var trimmed = text.replaceAll(RegExp(r'^[\r\n]+|[\r\n]+$'), '');
    final lines = trimmed.split('\n').map((l) => l.trimRight()).toList();
    return lines.join('\n');
  }

  void _paintText(
    Canvas canvas,
    Map<String, dynamic> element,
    Map<String, dynamic> attributes,
  ) {
    final rawText = element['text']?.toString() ?? '';
    final text = _normalizeRenderText(rawText);
    final fontSize = _readDouble(attributes['font-size']) ?? 18;
    final fill = _readColor(attributes['fill']) ?? Colors.black;
    final painter = TextPainter(
      text: TextSpan(
        text: text,
        style: _problemTextStyle(
          color: fill,
          fontSize: fontSize,
          fontWeight: FontWeight.w600,
          height: 1.25,
        ),
      ),
      textDirection: TextDirection.ltr,
    )..layout(maxWidth: _readDouble(attributes['max_width']) ?? 860);

    final baseline =
        painter.computeDistanceToActualBaseline(TextBaseline.alphabetic);
    final anchorWidth = _textAnchorWidth(painter);
    final offset = rendererTextPaintOffset(
      x: _readDouble(attributes['x']) ?? 0,
      y: _readDouble(attributes['y']) ?? 0,
      baseline: baseline,
      anchorWidth: anchorWidth,
      textAnchor: attributes['text-anchor'],
    );

    painter.paint(canvas, offset);
  }

  double _textAnchorWidth(TextPainter painter) {
    final lines = painter.computeLineMetrics();
    if (lines.isEmpty) {
      return painter.width;
    }
    return lines.fold<double>(
      0,
      (width, line) => line.width > width ? line.width : width,
    );
  }

  @override
  bool shouldRepaint(RendererJsonPainter oldDelegate) {
    return oldDelegate.renderer != renderer ||
        oldDelegate.logicalSize != logicalSize;
  }
}

@visibleForTesting
Path? rendererPolygonPath(Object? rawPoints) {
  if (rawPoints is! List || rawPoints.length < 2) {
    return null;
  }
  final points = <Offset>[];
  for (final rawPoint in rawPoints) {
    if (rawPoint is! List || rawPoint.length < 2) {
      continue;
    }
    final x = _readDouble(rawPoint[0]);
    final y = _readDouble(rawPoint[1]);
    if (x == null || y == null) {
      continue;
    }
    points.add(Offset(x, y));
  }
  if (points.length < 2) {
    return null;
  }
  final path = Path()..moveTo(points.first.dx, points.first.dy);
  for (final point in points.skip(1)) {
    path.lineTo(point.dx, point.dy);
  }
  path.close();
  return path;
}

@visibleForTesting
Offset rendererTextPaintOffset({
  required double x,
  required double y,
  required double baseline,
  required double anchorWidth,
  required Object? textAnchor,
}) {
  final anchor = textAnchor?.toString().trim().toLowerCase();
  final left = switch (anchor) {
    'middle' => x - anchorWidth / 2,
    'end' => x - anchorWidth,
    _ => x,
  };
  return Offset(left, y - baseline);
}

List<Widget> _textBoxLayers(Map<String, dynamic> renderer, double scale) {
  final elements = renderer['elements'];
  if (elements is! List) {
    return const [];
  }
  return rendererVisibleElements(elements)
      .where((element) => element['type']?.toString() == 'text_box')
      .where((element) => !_looksLikeInputTextBox(element))
      .map((element) {
    final attributes = _mapAt(element, 'attributes');
    final fontSize = _readDouble(attributes['font-size']) ?? 18;
    final lineHeight = _readDouble(attributes['data-line-height']) ??
        _readDouble(attributes['line-height']) ??
        1.35;
    final x = _readDouble(attributes['x']) ?? 0;
    final y = _readDouble(attributes['y']) ?? 0;
    final width = _readDouble(attributes['width']) ??
        _readDouble(attributes['max_width']) ??
        860;
    final height = _readDouble(attributes['height']) ?? fontSize * lineHeight;
    final align = _readTextAlign(attributes['data-text-align']);
    final verticalAlign = _readAlignment(
      horizontal: align,
      vertical: attributes['data-vertical-align'],
    );

    return Positioned(
      left: x * scale,
      top: y * scale,
      width: width * scale,
      height: height * scale,
      child: ClipRect(
        child: Align(
          alignment: verticalAlign,
          child: Text(
            element['text']?.toString() ?? '',
            textAlign: align,
            softWrap: true,
            overflow: TextOverflow.clip,
            style: _problemTextStyle(
              color: _readColor(attributes['fill']) ?? Colors.black,
              fontSize: fontSize * scale,
              fontWeight: FontWeight.w600,
              height: lineHeight,
            ),
          ),
        ),
      ),
    );
  }).toList(growable: false);
}

List<_InputSlot> _inputSlots(
  Map<String, dynamic> renderer, {
  String expectedAnswer = '',
  bool suppressInputs = false,
}) {
  if (suppressInputs) {
    return const [];
  }
  final elements = renderer['elements'];
  if (elements is! List) {
    return const [];
  }
  final slots = <_InputSlot>[];
  for (final element in rendererVisibleElements(elements)) {
    final type = element['type']?.toString();
    if (type == 'text_box' && _looksLikeInputTextBox(element)) {
      final attributes = _mapAt(element, 'attributes');
      final x = _readDouble(attributes['x']) ?? 0;
      final y = _readDouble(attributes['y']) ?? 0;
      final width = _readDouble(attributes['width']) ??
          _readDouble(attributes['max_width']) ??
          0;
      final height = _readDouble(attributes['height']) ?? 0;
      slots.add(
        _InputSlot(
          rect: Rect.fromLTWH(x, y, width, height),
          id: element['id']?.toString() ?? '',
          contributesToAnswer: _contributesToAnswer(element),
          maxLength: _maxLengthForInput(element),
          digitsOnly: _digitsOnlyForInput(element),
          operatorOnly: _operatorOnlyForInput(element),
          autoAdvance: _autoAdvanceForInput(element),
          order: _orderForInput(element),
          placeholder: _placeholderForInput(element),
        ),
      );
      continue;
    }
    if (type == 'circle') {
      final attributes = _mapAt(element, 'attributes');
      if (!_looksLikeInputCircle(element)) {
        continue;
      }
      final cx = _readDouble(attributes['cx']) ?? 0;
      final cy = _readDouble(attributes['cy']) ?? 0;
      final radius = _readDouble(attributes['r']) ?? 0;
      final inferredOperatorOnly = _operatorOnlyForInput(element) ||
          _looksLikeComparisonAnswer(expectedAnswer);
      slots.add(
        _InputSlot(
          rect: Rect.fromCircle(center: Offset(cx, cy), radius: radius),
          id: element['id']?.toString() ?? '',
          contributesToAnswer: _contributesToAnswer(element),
          maxLength: _maxLengthForInput(element),
          digitsOnly: _digitsOnlyForInput(element),
          operatorOnly: inferredOperatorOnly,
          autoAdvance: _autoAdvanceForInput(element),
          order: _orderForInput(element),
          placeholder: _placeholderForInput(element),
        ),
      );
      continue;
    }
    if (type == 'path') {
      if (!_looksLikeInputPath(element)) {
        continue;
      }
      final rect = _pathBounds(_mapAt(element, 'attributes')['d']?.toString());
      if (rect == null || rect.isEmpty) {
        continue;
      }
      slots.add(
        _InputSlot(
          rect: rect,
          id: element['id']?.toString() ?? '',
          contributesToAnswer: _contributesToAnswer(element),
          maxLength: _maxLengthForInput(element),
          digitsOnly: _digitsOnlyForInput(element),
          operatorOnly: _operatorOnlyForInput(element),
          autoAdvance: _autoAdvanceForInput(element),
          order: _orderForInput(element),
          placeholder: _placeholderForInput(element),
        ),
      );
      continue;
    }
    if (type != 'rect') {
      continue;
    }
    final attributes = _mapAt(element, 'attributes');
    final rect = Rect.fromLTWH(
      _readDouble(attributes['x']) ?? 0,
      _readDouble(attributes['y']) ?? 0,
      _readDouble(attributes['width']) ?? 0,
      _readDouble(attributes['height']) ?? 0,
    );
    if (!_looksLikeInputRect(element, attributes, rect)) {
      continue;
    }
    slots.add(
      _InputSlot(
        rect: rect,
        id: element['id']?.toString() ?? '',
        contributesToAnswer: _contributesToAnswer(element),
        maxLength: _maxLengthForInput(element),
        digitsOnly: _digitsOnlyForInput(element),
        operatorOnly: _operatorOnlyForInput(element),
        autoAdvance: _autoAdvanceForInput(element),
        order: _orderForInput(element),
        placeholder: _placeholderForInput(element),
      ),
    );
  }
  _sortInputSlots(slots);
  _applyExpectedAnswerLength(slots, expectedAnswer);
  return slots;
}

@visibleForTesting
List<Map<String, dynamic>> rendererVisibleElements(List<dynamic> elements) {
  final typedElements = elements.whereType<Map<String, dynamic>>().toList();
  return typedElements
      .where(
        (element) => !_isLegacyAnswerBlankInsideTextBox(element, typedElements),
      )
      .where(
        (element) => !_isPureInvisibleSlot(element),
      )
      .toList(growable: false);
}

bool _isPureInvisibleSlot(Map<String, dynamic> element) {
  final type = element['type']?.toString();
  if (type != 'rect' && type != 'circle' && type != 'line') {
    return false;
  }
  if (_mapAt(element, 'interaction').isNotEmpty) {
    return false;
  }
  final attributes = _mapAt(element, 'attributes');
  final fill = attributes['fill']?.toString().trim().toLowerCase();
  final stroke = attributes['stroke']?.toString().trim().toLowerCase();
  final isFillNone = fill == null || fill.isEmpty || fill == 'none';
  final isStrokeNone = stroke == 'none';
  return isFillNone && isStrokeNone;
}

bool _isLegacyAnswerBlankInsideTextBox(
  Map<String, dynamic> element,
  List<Map<String, dynamic>> elements,
) {
  if (element['type']?.toString() != 'rect') {
    return false;
  }
  if (_mapAt(element, 'interaction').isNotEmpty) {
    return false;
  }
  final identity = _slotIdentity(element);
  if (!identity.contains('answer') || !identity.contains('blank')) {
    return false;
  }
  final rect = _elementRect(element);
  if (rect == null || rect.isEmpty) {
    return false;
  }
  for (final other in elements) {
    if (identical(other, element) ||
        other['type']?.toString() != 'text_box' ||
        _looksLikeInputTextBox(other)) {
      continue;
    }
    final textRect = _elementRect(other);
    if (textRect == null || textRect.isEmpty) {
      continue;
    }
    final overlap = rect.intersect(textRect);
    if (overlap.isEmpty) {
      continue;
    }
    final overlapArea = overlap.width * overlap.height;
    final rectArea = rect.width * rect.height;
    if (rectArea > 0 && overlapArea / rectArea > 0.65) {
      return true;
    }
  }
  return false;
}

Rect? _elementRect(Map<String, dynamic> element) {
  final attributes = _mapAt(element, 'attributes');
  if (element['type']?.toString() == 'path') {
    final bounds = _pathBounds(attributes['d']?.toString());
    if (bounds != null) {
      return bounds;
    }
  }
  final x =
      _readDouble(attributes['x']) ?? _readDouble(attributes['data-box-x']);
  final y =
      _readDouble(attributes['y']) ?? _readDouble(attributes['data-box-y']);
  final width = _readDouble(attributes['width']) ??
      _readDouble(attributes['data-box-width']) ??
      _readDouble(attributes['max_width']);
  final height = _readDouble(attributes['height']) ??
      _readDouble(attributes['data-box-height']);
  if (x == null || y == null || width == null || height == null) {
    return null;
  }
  return Rect.fromLTWH(x, y, width, height);
}

Path? _parseSvgPath(String data) {
  final tokens = _svgPathTokens(data);
  if (tokens.isEmpty) {
    return null;
  }
  final path = Path();
  var index = 0;
  var command = '';
  Offset current = Offset.zero;
  Offset start = Offset.zero;

  bool hasNumber() => index < tokens.length && !_isPathCommand(tokens[index]);
  double? nextNumber() {
    if (!hasNumber()) {
      return null;
    }
    return double.tryParse(tokens[index++]);
  }

  while (index < tokens.length) {
    if (_isPathCommand(tokens[index])) {
      command = tokens[index++];
    }
    switch (command) {
      case 'M':
      case 'm':
        final isRelative = command == 'm';
        final x = nextNumber();
        final y = nextNumber();
        if (x == null || y == null) {
          return path;
        }
        current = isRelative ? Offset(current.dx + x, current.dy + y) : Offset(x, y);
        start = current;
        path.moveTo(current.dx, current.dy);
        command = isRelative ? 'l' : 'L';
      case 'L':
      case 'l':
        final isRelative = command == 'l';
        final x = nextNumber();
        final y = nextNumber();
        if (x == null || y == null) {
          return path;
        }
        current = isRelative ? Offset(current.dx + x, current.dy + y) : Offset(x, y);
        path.lineTo(current.dx, current.dy);
      case 'H':
      case 'h':
        final isRelative = command == 'h';
        final x = nextNumber();
        if (x == null) {
          return path;
        }
        current = Offset(isRelative ? current.dx + x : x, current.dy);
        path.lineTo(current.dx, current.dy);
      case 'V':
      case 'v':
        final isRelative = command == 'v';
        final y = nextNumber();
        if (y == null) {
          return path;
        }
        current = Offset(current.dx, isRelative ? current.dy + y : y);
        path.lineTo(current.dx, current.dy);
      case 'C':
      case 'c':
        final isRelative = command == 'c';
        final x1 = nextNumber();
        final y1 = nextNumber();
        final x2 = nextNumber();
        final y2 = nextNumber();
        final x3 = nextNumber();
        final y3 = nextNumber();
        if ([x1, y1, x2, y2, x3, y3].any((value) => value == null)) {
          return path;
        }
        final p1 = isRelative ? Offset(current.dx + x1!, current.dy + y1!) : Offset(x1!, y1!);
        final p2 = isRelative ? Offset(current.dx + x2!, current.dy + y2!) : Offset(x2!, y2!);
        final p3 = isRelative ? Offset(current.dx + x3!, current.dy + y3!) : Offset(x3!, y3!);
        current = p3;
        path.cubicTo(p1.dx, p1.dy, p2.dx, p2.dy, p3.dx, p3.dy);
      case 'Q':
      case 'q':
        final isRelative = command == 'q';
        final x1 = nextNumber();
        final y1 = nextNumber();
        final x2 = nextNumber();
        final y2 = nextNumber();
        if ([x1, y1, x2, y2].any((value) => value == null)) {
          return path;
        }
        final p1 = isRelative ? Offset(current.dx + x1!, current.dy + y1!) : Offset(x1!, y1!);
        final p2 = isRelative ? Offset(current.dx + x2!, current.dy + y2!) : Offset(x2!, y2!);
        current = p2;
        path.quadraticBezierTo(p1.dx, p1.dy, p2.dx, p2.dy);
      case 'A':
      case 'a':
        final isRelative = command == 'a';
        final rx = nextNumber();
        final ry = nextNumber();
        final xAxisRotation = nextNumber();
        final largeArcFlag = nextNumber();
        final sweepFlag = nextNumber();
        final targetX = nextNumber();
        final targetY = nextNumber();
        if (rx == null ||
            ry == null ||
            xAxisRotation == null ||
            largeArcFlag == null ||
            sweepFlag == null ||
            targetX == null ||
            targetY == null) {
          return path;
        }
        final endX = isRelative ? current.dx + targetX : targetX;
        final endY = isRelative ? current.dy + targetY : targetY;
        final end = Offset(endX, endY);
        path.arcToPoint(
          end,
          radius: Radius.elliptical(rx.abs(), ry.abs()),
          rotation: xAxisRotation * (math.pi / 180.0),
          largeArc: largeArcFlag != 0,
          clockwise: sweepFlag != 0,
        );
        current = end;
      case 'Z':
      case 'z':
        path.close();
        current = start;
        command = '';
      default:
        return path;
    }
  }
  return path;
}

Rect? _pathBounds(String? data) {
  if (data == null || data.trim().isEmpty) {
    return null;
  }
  final path = _parseSvgPath(data);
  if (path == null) {
    return null;
  }
  final bounds = path.getBounds();
  return bounds.isEmpty ? null : bounds;
}

List<String> _svgPathTokens(String data) {
  return RegExp(r'[MLHVCAQZmlhvcaqz]|[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?')
      .allMatches(data)
      .map((match) => match.group(0)!)
      .toList(growable: false);
}

bool _isPathCommand(String token) => RegExp(r'^[MLHVCAQZmlhvcaqz]$').hasMatch(token);

void _applyExpectedAnswerLength(List<_InputSlot> slots, String expectedAnswer) {
  final answerLength = expectedAnswer.characters.length;
  if (answerLength <= 1) {
    return;
  }

  final answerSlots = slots.where((slot) => slot.contributesToAnswer).toList();
  if (answerSlots.length == 1 && answerSlots.single.maxLength < answerLength) {
    final answerSlot = answerSlots.single;
    final index = slots.indexOf(answerSlot);
    slots[index] = answerSlot.copyWith(maxLength: answerLength);
    return;
  }

  if (answerSlots.length < 2 || answerLength % answerSlots.length != 0) {
    return;
  }
  final inferredLength = answerLength ~/ answerSlots.length;
  if (inferredLength <= 1) {
    return;
  }
  for (final answerSlot in answerSlots) {
    if (!_isWideNumericAnswerSlot(answerSlot, inferredLength) ||
        answerSlot.maxLength >= inferredLength) {
      continue;
    }
    final index = slots.indexOf(answerSlot);
    slots[index] = answerSlot.copyWith(maxLength: inferredLength);
  }
}

bool _isWideNumericAnswerSlot(_InputSlot slot, int inferredLength) {
  final minimumWidth = (slot.rect.height * inferredLength * 0.62).clamp(
    44.0,
    double.infinity,
  );
  return slot.digitsOnly &&
      !slot.operatorOnly &&
      slot.rect.width >= minimumWidth &&
      slot.rect.width / slot.rect.height > 1.35;
}

void _sortInputSlots(List<_InputSlot> slots) {
  final orderedSlots = slots.where((slot) => slot.order != null).toList();
  final hasMeaningfulOrder = orderedSlots.isNotEmpty &&
      orderedSlots.map((slot) => slot.order).toSet().length > 1;
  if (hasMeaningfulOrder) {
    slots.sort((a, b) {
      final orderComparison = switch ((a.order, b.order)) {
        (final int aOrder, final int bOrder) => aOrder.compareTo(bOrder),
        (final int _, null) => -1,
        (null, final int _) => 1,
        _ => 0,
      };
      if (orderComparison != 0) {
        return orderComparison;
      }
      return _compareByRowThenLeft(a, b);
    });
    return;
  }

  final clusters = _horizontalClusters(slots);
  if (clusters.length > 1) {
    slots
      ..clear()
      ..addAll(
        clusters.expand(
          (cluster) => cluster..sort(_compareByRowThenLeft),
        ),
      );
    return;
  }

  slots.sort(_compareByRowThenLeft);
}

List<List<_InputSlot>> _horizontalClusters(List<_InputSlot> slots) {
  if (slots.length < 4) {
    return [slots];
  }
  final byLeft = [...slots]..sort((a, b) => a.rect.left.compareTo(b.rect.left));
  final averageWidth =
      byLeft.fold<double>(0, (total, slot) => total + slot.rect.width) /
          byLeft.length;
  final clusters = <List<_InputSlot>>[];
  var current = <_InputSlot>[byLeft.first];
  var currentRight = byLeft.first.rect.right;
  for (final slot in byLeft.skip(1)) {
    final gap = slot.rect.left - currentRight;
    if (gap > averageWidth * 2.2) {
      clusters.add(current);
      current = [slot];
    } else {
      current.add(slot);
    }
    if (slot.rect.right > currentRight) {
      currentRight = slot.rect.right;
    }
  }
  clusters.add(current);
  return clusters;
}

int _compareByRowThenLeft(_InputSlot a, _InputSlot b) {
  final row = a.rect.top.compareTo(b.rect.top).abs() < 12
      ? 0
      : a.rect.top.compareTo(b.rect.top);
  return row != 0 ? row : a.rect.left.compareTo(b.rect.left);
}

bool _contributesToAnswer(Map<String, dynamic> element) {
  final interaction = _mapAt(element, 'interaction');
  if (interaction['include_in_submission'] == true) {
    return true;
  }
  if (interaction['role']?.toString().toLowerCase() == 'answer') {
    return true;
  }
  final slotText = _slotIdentity(element);
  return slotText.contains('answer') || slotText.contains('result');
}

bool _looksLikeInputTextBox(Map<String, dynamic> element) {
  final interaction = _mapAt(element, 'interaction');
  if (interaction['type']?.toString().toLowerCase() == 'input') {
    return true;
  }
  final text = element['text']?.toString().trim();
  if (text != '□') {
    return false;
  }
  final slotText = _slotIdentity(element);
  if (slotText.contains('instruction')) {
    return false;
  }
  return slotText.contains('answer') ||
      slotText.contains('blank') ||
      slotText.contains('carry') ||
      slotText.contains('result');
}

bool _looksLikeInputRect(
  Map<String, dynamic> element,
  Map<String, dynamic> attributes,
  Rect rect,
) {
  final interaction = _mapAt(element, 'interaction');
  if (interaction['type']?.toString().toLowerCase() == 'input') {
    return true;
  }
  if (rect.width < 24 || rect.height < 24 || rect.width > 120) {
    return false;
  }
  final ratio = rect.width / rect.height;
  if (ratio < 0.65 || ratio > 1.35) {
    return false;
  }
  final slotText = _slotIdentity(element);
  if (slotText.contains('background') || slotText.contains('circle')) {
    return false;
  }
  final stroke = attributes['stroke']?.toString().trim();
  if (stroke == null || stroke.isEmpty || stroke == 'none') {
    return false;
  }
  final fillText = attributes['fill']?.toString().trim().toLowerCase();
  return fillText == null ||
      fillText.isEmpty ||
      fillText == 'none' ||
      fillText == '#ffffff' ||
      fillText == '#fff';
}

bool _looksLikeInputCircle(Map<String, dynamic> element) {
  final interaction = _mapAt(element, 'interaction');
  final type = interaction['type']?.toString().toLowerCase();
  if (type == 'input') {
    return true;
  }
  if (type != 'select' && type != 'choice') {
    return false;
  }
  return _contributesToAnswer(element);
}

bool _looksLikeInputPath(Map<String, dynamic> element) {
  final interaction = _mapAt(element, 'interaction');
  final type = interaction['type']?.toString().toLowerCase();
  if (type == 'input') {
    return true;
  }
  if (type != 'select' && type != 'choice') {
    return false;
  }
  return _contributesToAnswer(element);
}

int _maxLengthForInput(Map<String, dynamic> element) {
  final interaction = _mapAt(element, 'interaction');
  final maxLength = _readInt(interaction['max_length']);
  if (maxLength != null && maxLength > 0) {
    return maxLength;
  }
  return 1;
}

bool _digitsOnlyForInput(Map<String, dynamic> element) {
  final interaction = _mapAt(element, 'interaction');
  final valueType = interaction['value_type']?.toString().toLowerCase();
  final keyboard = interaction['keyboard']?.toString().toLowerCase();
  return valueType == 'digit' ||
      valueType == 'digits' ||
      valueType == 'number' ||
      keyboard == 'number';
}

bool _operatorOnlyForInput(Map<String, dynamic> element) {
  final interaction = _mapAt(element, 'interaction');
  final valueType = interaction['value_type']?.toString().toLowerCase();
  final keyboard = interaction['keyboard']?.toString().toLowerCase();
  return valueType == 'operator' ||
      valueType == 'comparison_operator' ||
      keyboard == 'operator';
}

bool _looksLikeComparisonAnswer(String expectedAnswer) {
  final value = expectedAnswer.trim();
  return value.isNotEmpty && RegExp(r'^[<>=]+$').hasMatch(value);
}

bool _autoAdvanceForInput(Map<String, dynamic> element) {
  final interaction = _mapAt(element, 'interaction');
  return interaction['auto_advance'] == true;
}

double _inputFontSize(_InputSlot slot, double scale) {
  final ratio = slot.operatorOnly
      ? 0.58
      : slot.maxLength > 1
          ? 0.52
          : 0.72;
  return (slot.rect.height * ratio * scale).clamp(16.0, 52.0);
}

int? _orderForInput(Map<String, dynamic> element) {
  final interaction = _mapAt(element, 'interaction');
  return _readInt(interaction['order']);
}

String? _placeholderForInput(Map<String, dynamic> element) {
  final interaction = _mapAt(element, 'interaction');
  final explicit = interaction['placeholder']?.toString().trim();
  if (explicit != null && explicit.isNotEmpty) {
    return explicit;
  }
  final text = element['text']?.toString().trim();
  if (text != null && text.isNotEmpty) {
    return text;
  }
  return null;
}

String _slotIdentity(Map<String, dynamic> element) {
  final id = element['id']?.toString().toLowerCase() ?? '';
  final sourceRef = element['source_ref']?.toString().toLowerCase() ?? '';
  final metadataSlotId =
      _mapAt(element, 'metadata')['layout_slot_id']?.toString().toLowerCase();
  final refsSlotId =
      _mapAt(element, 'refs')['layout_slot_id']?.toString().toLowerCase();
  return '$id $sourceRef ${metadataSlotId ?? ''} ${refsSlotId ?? ''}';
}

class _InputSlot {
  const _InputSlot({
    required this.rect,
    required this.id,
    required this.contributesToAnswer,
    required this.maxLength,
    required this.digitsOnly,
    required this.operatorOnly,
    required this.autoAdvance,
    required this.order,
    required this.placeholder,
  });

  final Rect rect;
  final String id;
  final bool contributesToAnswer;
  final int maxLength;
  final bool digitsOnly;
  final bool operatorOnly;
  final bool autoAdvance;
  final int? order;
  final String? placeholder;

  bool get drawPlaceholderBehind =>
      operatorOnly && placeholder != null && placeholder!.isNotEmpty;

  String get signature =>
      '$id:${rect.left},${rect.top},${rect.width},${rect.height}:$maxLength:$order:$placeholder';

  _InputSlot copyWith({int? maxLength}) {
    return _InputSlot(
      rect: rect,
      id: id,
      contributesToAnswer: contributesToAnswer,
      maxLength: maxLength ?? this.maxLength,
      digitsOnly: digitsOnly,
      operatorOnly: operatorOnly,
      autoAdvance: autoAdvance,
      order: order,
      placeholder: placeholder,
    );
  }
}

Map<String, dynamic> _mapAt(Map<String, dynamic> map, String key) {
  final value = map[key];
  if (value is Map<String, dynamic>) {
    return value;
  }
  return const {};
}

double? _readDouble(Object? value) {
  if (value is num) {
    return value.toDouble();
  }
  return double.tryParse(value?.toString() ?? '');
}

int? _readInt(Object? value) {
  if (value is int) {
    return value;
  }
  return int.tryParse(value?.toString() ?? '');
}

String _sliceCharacters(List<String> chars, int start, int length) {
  if (start >= chars.length) {
    return '';
  }
  final end = (start + length).clamp(0, chars.length);
  return chars.sublist(start, end).join();
}

List<double>? _readDashArray(Object? value) {
  final text = value?.toString().trim();
  if (text == null || text.isEmpty) {
    return null;
  }
  final values = text
      .split(RegExp(r'[\s,]+'))
      .map(double.tryParse)
      .whereType<double>()
      .where((item) => item > 0)
      .toList();
  if (values.isEmpty) {
    return null;
  }
  return values;
}

TextAlign _readTextAlign(Object? value) {
  return switch (value?.toString()) {
    'center' => TextAlign.center,
    'right' => TextAlign.right,
    _ => TextAlign.left,
  };
}

Alignment _readAlignment({
  required TextAlign horizontal,
  required Object? vertical,
}) {
  final x = switch (horizontal) {
    TextAlign.center => 0.0,
    TextAlign.right => 1.0,
    _ => -1.0,
  };
  final y = switch (vertical?.toString()) {
    'middle' => 0.0,
    'bottom' => 1.0,
    _ => -1.0,
  };
  return Alignment(x, y);
}

Color? _readColor(Object? value) {
  final text = value?.toString().trim();
  if (text == null || text.isEmpty || text == 'none') {
    return null;
  }
  if (text.startsWith('#') && (text.length == 7 || text.length == 9)) {
    final hex = text.substring(1);
    final alpha = hex.length == 8 ? hex.substring(6, 8) : 'FF';
    final rgb = hex.length == 8 ? hex.substring(0, 6) : hex;
    return Color(int.parse('$alpha$rgb', radix: 16));
  }
  return null;
}

TextStyle _problemTextStyle({
  required Color color,
  required double fontSize,
  required FontWeight fontWeight,
  required double height,
}) {
  return GoogleFonts.poorStory(
    color: color,
    fontSize: fontSize,
    fontWeight: fontWeight,
    height: height,
  );
}
