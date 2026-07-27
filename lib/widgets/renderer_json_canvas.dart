import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:google_fonts/google_fonts.dart';

class RendererJsonCanvas extends StatefulWidget {
  const RendererJsonCanvas({
    super.key,
    required this.renderer,
    this.inputValue = '',
    this.expectedAnswer = '',
    this.onInputChanged,
  });

  final Map<String, dynamic> renderer;
  final String inputValue;
  final String expectedAnswer;
  final ValueChanged<String>? onInputChanged;

  @override
  State<RendererJsonCanvas> createState() => _RendererJsonCanvasState();
}

class _RendererJsonCanvasState extends State<RendererJsonCanvas> {
  final List<TextEditingController> inputControllers = [];
  String inputSignature = '';
  String? lastEmittedInputValue;

  @override
  void initState() {
    super.initState();
    _syncInputControllers(force: true);
  }

  @override
  void didUpdateWidget(covariant RendererJsonCanvas oldWidget) {
    super.didUpdateWidget(oldWidget);
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

    return LayoutBuilder(
      builder: (context, constraints) {
        return Center(
          child: AspectRatio(
            aspectRatio: width / height,
            child: DecoratedBox(
              decoration: BoxDecoration(
                color: background,
                border: Border.all(
                  color: Theme.of(context).colorScheme.outlineVariant,
                ),
              ),
              child: LayoutBuilder(
                builder: (context, canvasConstraints) {
                  final scale = canvasConstraints.maxWidth / width;
                  final inputSlots = _inputSlots(
                    widget.renderer,
                    expectedAnswer: widget.expectedAnswer,
                  );
                  _ensureControllerCount(inputSlots.length);

                  return Stack(
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
                  );
                },
              ),
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

  void _syncInputControllers({required bool force}) {
    final slots = _inputSlots(
      widget.renderer,
      expectedAnswer: widget.expectedAnswer,
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
      for (final element in elements.whereType<Map<String, dynamic>>()) {
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
    final stroke = _readColor(attributes['stroke']) ?? Colors.black;
    final strokeWidth = _readDouble(attributes['stroke-width']) ?? 1;

    if (fill != null) {
      canvas.drawCircle(center, radius, Paint()..color = fill);
    }
    canvas.drawCircle(
      center,
      radius,
      Paint()
        ..color = stroke
        ..style = PaintingStyle.stroke
        ..strokeWidth = strokeWidth,
    );
  }

  void _paintLine(Canvas canvas, Map<String, dynamic> attributes) {
    final start = Offset(
      _readDouble(attributes['x1']) ?? 0,
      _readDouble(attributes['y1']) ?? 0,
    );
    final end = Offset(
      _readDouble(attributes['x2']) ?? 0,
      _readDouble(attributes['y2']) ?? 0,
    );
    final paint = Paint()
      ..color = _readColor(attributes['stroke']) ?? Colors.black
      ..strokeWidth = _readDouble(attributes['stroke-width']) ?? 1
      ..strokeCap = StrokeCap.round;
    final dashArray = _readDashArray(attributes['stroke-dasharray']);
    if (dashArray == null) {
      canvas.drawLine(start, end, paint);
      return;
    }
    _drawDashedLine(canvas, start, end, paint, dashArray);
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

  void _paintRect(Canvas canvas, Map<String, dynamic> attributes) {
    final rect = Rect.fromLTWH(
      _readDouble(attributes['x']) ?? 0,
      _readDouble(attributes['y']) ?? 0,
      _readDouble(attributes['width']) ?? 0,
      _readDouble(attributes['height']) ?? 0,
    );
    final fill = _readColor(attributes['fill']);
    final stroke = _readColor(attributes['stroke']) ?? Colors.black;
    final strokeWidth = _readDouble(attributes['stroke-width']) ?? 1;

    if (fill != null) {
      canvas.drawRect(rect, Paint()..color = fill);
    }
    canvas.drawRect(
      rect,
      Paint()
        ..color = stroke
        ..style = PaintingStyle.stroke
        ..strokeWidth = strokeWidth,
    );
  }

  void _paintText(
    Canvas canvas,
    Map<String, dynamic> element,
    Map<String, dynamic> attributes,
  ) {
    final text = element['text']?.toString() ?? '';
    final fontSize = _readDouble(attributes['font-size']) ?? 18;
    final fill = _readColor(attributes['fill']) ?? Colors.black;
    final painter = TextPainter(
      text: TextSpan(
        text: text,
        style: _problemTextStyle(
          color: fill,
          fontSize: fontSize,
          fontWeight: FontWeight.w600,
          height: 1,
        ),
      ),
      textDirection: TextDirection.ltr,
      maxLines: 3,
    )..layout(maxWidth: _readDouble(attributes['max_width']) ?? 860);

    painter.paint(
      canvas,
      Offset(
        _readDouble(attributes['x']) ?? 0,
        (_readDouble(attributes['y']) ?? 0) - fontSize,
      ),
    );
  }

  @override
  bool shouldRepaint(RendererJsonPainter oldDelegate) {
    return oldDelegate.renderer != renderer ||
        oldDelegate.logicalSize != logicalSize;
  }
}

List<Widget> _textBoxLayers(Map<String, dynamic> renderer, double scale) {
  final elements = renderer['elements'];
  if (elements is! List) {
    return const [];
  }
  return elements
      .whereType<Map<String, dynamic>>()
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
}) {
  final elements = renderer['elements'];
  if (elements is! List) {
    return const [];
  }
  final slots = <_InputSlot>[];
  for (final element in elements.whereType<Map<String, dynamic>>()) {
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
    final row = a.rect.top.compareTo(b.rect.top).abs() < 12
        ? 0
        : a.rect.top.compareTo(b.rect.top);
    return row != 0 ? row : a.rect.left.compareTo(b.rect.left);
  });
  final answerLength = expectedAnswer.characters.length;
  final answerSlots = slots.where((slot) => slot.contributesToAnswer).toList();
  if (answerLength > 1 &&
      answerSlots.length == 1 &&
      answerSlots.single.maxLength < answerLength) {
    final answerSlot = answerSlots.single;
    final index = slots.indexOf(answerSlot);
    slots[index] = answerSlot.copyWith(maxLength: answerLength);
  }
  return slots;
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

bool _autoAdvanceForInput(Map<String, dynamic> element) {
  final interaction = _mapAt(element, 'interaction');
  return interaction['auto_advance'] == true;
}

double _inputFontSize(_InputSlot slot, double scale) {
  final ratio = slot.operatorOnly ? 0.58 : 0.72;
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
  final slotId =
      _mapAt(element, 'metadata')['layout_slot_id']?.toString().toLowerCase();
  return '$id $sourceRef ${slotId ?? ''}';
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
