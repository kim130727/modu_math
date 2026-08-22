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

    test('compares marked choice labels by their leading number', () {
      expect(isSameAnswer('\u2462 \u3137, \u3131, \u3134', '3'), isTrue);
      expect(isSameAnswer('(3) \u3137, \u3131, \u3134', '3'), isTrue);
      expect(isSameAnswer('3. \u3137, \u3131, \u3134', '3'), isTrue);
    });

    test('compares Hangul consonant choice markers accurately', () {
      expect(isSameAnswer('㉠ 16 ÷ 3', 'ㄱ'), isTrue);
      expect(isSameAnswer('ㄱ. 16 ÷ 3', 'ㄱ'), isTrue);
      expect(isSameAnswer('(ㄱ) 16 ÷ 3', 'ㄱ'), isTrue);
      expect(isSameAnswer('㉡ 49 ÷ 7', 'ㄴ'), isTrue);
      expect(isSameAnswer('ㄴ. 49 ÷ 7', 'ㄴ'), isTrue);
      expect(isSameAnswer('ㄱ. 16 ÷ 3', 'ㄴ'), isFalse);
    });

    test('matches full choice text against correct answer regardless of punctuation or synonyms', () {
      expect(isSameAnswer('1. 무수히 많이 그릴 수 있습니다', '무수히 많이 그을 수 있습니다.'), isTrue);
      expect(isSameAnswer('1. 무수히 많이 그을 수 있습니다.', '무수히 많이 그을 수 있습니다.'), isTrue);
      expect(isSameAnswer('무수히 많이 그을 수 있습니다', '무수히 많이 그을 수 있습니다.'), isTrue);
      expect(isSameAnswer('2. 3개', '무수히 많이 그을 수 있습니다.'), isFalse);
    });

    test('handles multi-select Hangul syllable choice answers accurately', () {
      expect(isSameAnswer('나, 다, 라', '나, 다, 라'), isTrue);
      expect(isSameAnswer('㉯, ㉰, ㉱', '나, 다, 라'), isTrue);
      expect(isSameAnswer('나다라', '나, 다, 라'), isTrue);
      expect(isSameAnswer('가, 나', '나, 다, 라'), isFalse);
    });

    test('handles multi-group choice answers accurately', () {
      expect(isSameAnswer('ㄴㄹ, 지름', 'ㄴㄹ, 지름'), isTrue);
      expect(isSameAnswer('ㄴㄹ 지름', 'ㄴㄹ, 지름'), isTrue);
      expect(isSameAnswer('ㄴㄹ지름', 'ㄴㄹ, 지름'), isTrue);
      expect(isSameAnswer('ㄱㄹ, 지름', 'ㄴㄹ, 지름'), isFalse);
    });

    test('matches arithmetic expression against calculated value and formula choices (S3_초등_3_008578)', () {
      expect(isSameAnswer('752 × 3', '752 × 3'), isTrue);
      expect(isSameAnswer('752 * 3', '752 × 3'), isTrue);
      expect(isSameAnswer('752x3', '752 × 3'), isTrue);
      expect(isSameAnswer('3. 752 × 3', '752 × 3'), isTrue);
      expect(isSameAnswer('3', '3. 752 × 3'), isTrue);
      expect(isSameAnswer('2256', '752 × 3'), isTrue);
      expect(isSameAnswer('752 × 3', '2256'), isTrue);
      expect(isSameAnswer('328 × 8', '752 × 3'), isFalse);
      expect(isSameAnswer('2624', '752 × 3'), isFalse);
    });
  });
}
