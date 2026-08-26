import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/widgets/math_keypad.dart';

void main() {
  testWidgets('renders digits keypad and fires callbacks', (tester) async {
    String? pressedKey;
    var backspaceFired = false;
    var clearFired = false;
    var nextFired = false;
    var submitFired = false;

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: MathKeypad(
            mode: MathKeypadMode.digits,
            onKeyPressed: (key) => pressedKey = key,
            onBackspace: () => backspaceFired = true,
            onClear: () => clearFired = true,
            onNext: () => nextFired = true,
            onSubmit: () => submitFired = true,
          ),
        ),
      ),
    );

    expect(find.text('1'), findsOneWidget);
    expect(find.text('9'), findsOneWidget);
    expect(find.text('0'), findsOneWidget);
    expect(find.text('C'), findsOneWidget);
    expect(find.text('다음'), findsOneWidget);
    expect(find.text('확인'), findsOneWidget);

    await tester.tap(find.text('7'));
    expect(pressedKey, equals('7'));

    await tester.tap(find.byIcon(Icons.backspace_outlined));
    expect(backspaceFired, isTrue);

    await tester.tap(find.text('C'));
    expect(clearFired, isTrue);

    await tester.tap(find.text('다음'));
    expect(nextFired, isTrue);

    await tester.tap(find.text('확인'));
    expect(submitFired, isTrue);
  });

  testWidgets('renders comparison keypad and fires operator callbacks', (tester) async {
    String? pressedKey;
    var backspaceFired = false;

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: MathKeypad(
            mode: MathKeypadMode.comparison,
            onKeyPressed: (key) => pressedKey = key,
            onBackspace: () => backspaceFired = true,
          ),
        ),
      ),
    );

    expect(find.text('>'), findsOneWidget);
    expect(find.text('='), findsOneWidget);
    expect(find.text('<'), findsOneWidget);

    await tester.tap(find.text('>'));
    expect(pressedKey, equals('>'));

    await tester.tap(find.byIcon(Icons.backspace_outlined));
    expect(backspaceFired, isTrue);
  });
}
