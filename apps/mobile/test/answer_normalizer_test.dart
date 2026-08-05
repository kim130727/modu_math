import 'package:flutter_test/flutter_test.dart';
import 'package:modu_math_app/utils/answer_normalizer.dart';

void main() {
  group('isSameAnswer', () {
    test('does not confuse expressions with the same leading digit', () {
      expect(isSameAnswer('6x4', '60 × 4'), isFalse);
    });

    test('accepts equivalent multiplication symbols and spacing', () {
      expect(isSameAnswer('60x4', '60 × 4'), isTrue);
      expect(isSameAnswer('60 * 4', '60 × 4'), isTrue);
    });

    test('keeps bare choice numbers comparable', () {
      expect(isSameAnswer('3', '3'), isTrue);
      expect(isSameAnswer('3', '4'), isFalse);
    });
  });
}
