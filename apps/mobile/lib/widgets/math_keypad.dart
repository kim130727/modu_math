import 'package:flutter/material.dart';

import '../theme/app_theme.dart';

enum MathKeypadMode {
  digits,
  comparison,
  arithmetic,
}

class MathKeypad extends StatelessWidget {
  const MathKeypad({
    super.key,
    this.mode = MathKeypadMode.digits,
    this.onKeyPressed,
    this.onBackspace,
    this.onClear,
    this.onNext,
    this.onSubmit,
    this.submitLabel = '확인',
    this.showNextButton = true,
  });

  final MathKeypadMode mode;
  final ValueChanged<String>? onKeyPressed;
  final VoidCallback? onBackspace;
  final VoidCallback? onClear;
  final VoidCallback? onNext;
  final VoidCallback? onSubmit;
  final String submitLabel;
  final bool showNextButton;

  @override
  Widget build(BuildContext context) {
    switch (mode) {
      case MathKeypadMode.comparison:
        return _buildComparisonKeypad(context);
      case MathKeypadMode.arithmetic:
        return _buildArithmeticKeypad(context);
      case MathKeypadMode.digits:
        return _buildDigitsKeypad(context);
    }
  }

  Widget _buildDigitsKeypad(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: const Color(0xFFF3F4F6),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: KidsPalette.line),
      ),
      padding: const EdgeInsets.all(10),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Row(
            children: [
              _keyButton(context, '1'),
              const SizedBox(width: 8),
              _keyButton(context, '2'),
              const SizedBox(width: 8),
              _keyButton(context, '3'),
              const SizedBox(width: 8),
              _actionButton(
                context,
                icon: Icons.backspace_outlined,
                onTap: onBackspace,
                tooltip: '지우기',
              ),
            ],
          ),
          const SizedBox(height: 8),
          Row(
            children: [
              _keyButton(context, '4'),
              const SizedBox(width: 8),
              _keyButton(context, '5'),
              const SizedBox(width: 8),
              _keyButton(context, '6'),
              const SizedBox(width: 8),
              _textActionButton(
                context,
                label: 'C',
                onTap: onClear,
                tooltip: '전체 지우기',
              ),
            ],
          ),
          const SizedBox(height: 8),
          Row(
            children: [
              _keyButton(context, '7'),
              const SizedBox(width: 8),
              _keyButton(context, '8'),
              const SizedBox(width: 8),
              _keyButton(context, '9'),
              const SizedBox(width: 8),
              if (showNextButton && onNext != null)
                _textActionButton(
                  context,
                  label: '다음',
                  onTap: onNext,
                  tooltip: '다음 빈칸',
                  highlight: true,
                )
              else
                _keyButton(context, '0'),
            ],
          ),
          if (showNextButton && onNext != null) ...[
            const SizedBox(height: 8),
            Row(
              children: [
                const Spacer(),
                const SizedBox(width: 8),
                _keyButton(context, '0'),
                const SizedBox(width: 8),
                const Spacer(),
                const SizedBox(width: 8),
                if (onSubmit != null)
                  _submitButton(context)
                else
                  const Spacer(),
              ],
            ),
          ] else if (onSubmit != null) ...[
            const SizedBox(height: 8),
            SizedBox(
              width: double.infinity,
              height: 46,
              child: _submitButton(context),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildComparisonKeypad(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: const Color(0xFFF3F4F6),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: KidsPalette.line),
      ),
      padding: const EdgeInsets.all(10),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          _keyButton(context, '>', fontSize: 24),
          const SizedBox(width: 10),
          _keyButton(context, '=', fontSize: 24),
          const SizedBox(width: 10),
          _keyButton(context, '<', fontSize: 24),
          const SizedBox(width: 10),
          _actionButton(
            context,
            icon: Icons.backspace_outlined,
            onTap: onBackspace,
            tooltip: '지우기',
          ),
          if (onClear != null) ...[
            const SizedBox(width: 10),
            _textActionButton(
              context,
              label: 'C',
              onTap: onClear,
              tooltip: '초기화',
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildArithmeticKeypad(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: const Color(0xFFF3F4F6),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: KidsPalette.line),
      ),
      padding: const EdgeInsets.all(10),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Row(
            children: [
              _keyButton(context, '+', fontSize: 22, isOperator: true),
              const SizedBox(width: 8),
              _keyButton(context, '-', fontSize: 22, isOperator: true),
              const SizedBox(width: 8),
              _keyButton(context, '×', fontSize: 22, isOperator: true),
              const SizedBox(width: 8),
              _keyButton(context, '÷', fontSize: 22, isOperator: true),
            ],
          ),
          const SizedBox(height: 8),
          Row(
            children: [
              _keyButton(context, '1'),
              const SizedBox(width: 8),
              _keyButton(context, '2'),
              const SizedBox(width: 8),
              _keyButton(context, '3'),
              const SizedBox(width: 8),
              _actionButton(
                context,
                icon: Icons.backspace_outlined,
                onTap: onBackspace,
                tooltip: '지우기',
              ),
            ],
          ),
          const SizedBox(height: 8),
          Row(
            children: [
              _keyButton(context, '4'),
              const SizedBox(width: 8),
              _keyButton(context, '5'),
              const SizedBox(width: 8),
              _keyButton(context, '6'),
              const SizedBox(width: 8),
              _keyButton(context, '=', fontSize: 22, isOperator: true),
            ],
          ),
          const SizedBox(height: 8),
          Row(
            children: [
              _keyButton(context, '7'),
              const SizedBox(width: 8),
              _keyButton(context, '8'),
              const SizedBox(width: 8),
              _keyButton(context, '9'),
              const SizedBox(width: 8),
              _keyButton(context, '0'),
            ],
          ),
        ],
      ),
    );
  }

  Widget _keyButton(
    BuildContext context,
    String text, {
    double fontSize = 20,
    bool isOperator = false,
  }) {
    return Expanded(
      child: SizedBox(
        height: 48,
        child: ElevatedButton(
          onPressed: () => onKeyPressed?.call(text),
          style: ElevatedButton.styleFrom(
            backgroundColor: isOperator ? const Color(0xFFECEEFF) : Colors.white,
            foregroundColor: isOperator ? KidsPalette.sage : KidsPalette.ink,
            elevation: 1,
            padding: EdgeInsets.zero,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(10),
              side: BorderSide(
                color: isOperator ? const Color(0xFFC7D2FE) : KidsPalette.line,
              ),
            ),
          ),
          child: Text(
            text,
            style: TextStyle(
              fontSize: fontSize,
              fontWeight: FontWeight.w700,
            ),
          ),
        ),
      ),
    );
  }

  Widget _actionButton(
    BuildContext context, {
    required IconData icon,
    required VoidCallback? onTap,
    String? tooltip,
  }) {
    return Expanded(
      child: SizedBox(
        height: 48,
        child: ElevatedButton(
          onPressed: onTap,
          style: ElevatedButton.styleFrom(
            backgroundColor: const Color(0xFFF9FAFB),
            foregroundColor: KidsPalette.cocoaSoft,
            elevation: 0,
            padding: EdgeInsets.zero,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(10),
              side: const BorderSide(color: KidsPalette.line),
            ),
          ),
          child: Icon(icon, size: 20),
        ),
      ),
    );
  }

  Widget _textActionButton(
    BuildContext context, {
    required String label,
    required VoidCallback? onTap,
    String? tooltip,
    bool highlight = false,
  }) {
    return Expanded(
      child: SizedBox(
        height: 48,
        child: ElevatedButton(
          onPressed: onTap,
          style: ElevatedButton.styleFrom(
            backgroundColor:
                highlight ? const Color(0xFFECEEFF) : const Color(0xFFF9FAFB),
            foregroundColor:
                highlight ? KidsPalette.sage : KidsPalette.cocoaSoft,
            elevation: 0,
            padding: EdgeInsets.zero,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(10),
              side: BorderSide(
                color: highlight ? const Color(0xFFC7D2FE) : KidsPalette.line,
              ),
            ),
          ),
          child: Text(
            label,
            style: const TextStyle(
              fontSize: 15,
              fontWeight: FontWeight.w700,
            ),
          ),
        ),
      ),
    );
  }

  Widget _submitButton(BuildContext context) {
    return Expanded(
      child: SizedBox(
        height: 48,
        child: FilledButton(
          onPressed: onSubmit,
          style: FilledButton.styleFrom(
            padding: EdgeInsets.zero,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(10),
            ),
          ),
          child: Text(
            submitLabel,
            style: const TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
      ),
    );
  }
}
