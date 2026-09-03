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

    test('matches arithmetic expression against calculated value and formula choices (S3_elem_3_008578)', () {
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

    test('matches container and bottle comparison labels flexibly (S3_elem_3_008750)', () {
      expect(isSameAnswer('가 병', '가 병'), isTrue);
      expect(isSameAnswer('가', '가 병'), isTrue);
      expect(isSameAnswer('가병', '가 병'), isTrue);
      expect(isSameAnswer('가 병', '가 물병'), isTrue);
      expect(isSameAnswer('가 물병', '가 병'), isTrue);
      expect(isSameAnswer('㉮', '가 병'), isTrue);
      expect(isSameAnswer('㉮ 병', '가 병'), isTrue);
      expect(isSameAnswer('ㄱ', '가 병'), isTrue);
      expect(isSameAnswer('나 병', '가 병'), isFalse);
      expect(isSameAnswer('나', '가 병'), isFalse);
      expect(isSameAnswer('나 물병', '나 병'), isTrue);
      expect(isSameAnswer('나', '나 물병'), isTrue);
    });

    test('matches commutative multi-numeric addends regardless of order (P3_1_01_00040_15472)', () {
      expect(isSameAnswer('415 / 334', '334 / 415'), isTrue);
      expect(isSameAnswer('415 / 334', '334415'), isTrue);
      expect(isSameAnswer('415, 334', '334, 415'), isTrue);
      expect(isSameAnswer('415 334', '334 415'), isTrue);
      expect(isSameAnswer('415334', '334415'), isTrue);
      expect(isSameAnswer('334 / 415', '334415'), isTrue);
      expect(isSameAnswer('415 / 325', '334 / 415'), isFalse);
    });

    test('matches expanded vertical addition partial sums (P3_1_01_00040_15598_1, P3_1_01_00040_15598_2)', () {
      expect(isSameAnswer('9 / 50 / 700 / 759', '950700759'), isTrue);
      expect(isSameAnswer('9, 50, 700, 759', '950700759'), isTrue);
      expect(isSameAnswer('9 50 700 759', '950700759'), isTrue);
      expect(isSameAnswer('950700759', '950700759'), isTrue);
      expect(isSameAnswer('9 / 50 / 700 / 759', '9 / 50 / 700 / 759'), isTrue);

      expect(isSameAnswer('7 / 90 / 500 / 597', '790500597'), isTrue);
      expect(isSameAnswer('7, 90, 500, 597', '790500597'), isTrue);
      expect(isSameAnswer('7 90 500 597', '790500597'), isTrue);
      expect(isSameAnswer('790500597', '790500597'), isTrue);
      expect(isSameAnswer('7 / 90 / 500 / 597', '7 / 90 / 500 / 597'), isTrue);
    });

    test('matches multi-blank partial sums and sequential addition answers (P3_1_01_00040_15621, P3_1_01_00040_02159, P3_1_01_00040_07644)', () {
      expect(isSameAnswer('60 / 2 / 90 / 7 / 697', '602907697'), isTrue);
      expect(isSameAnswer('60, 2, 90, 7, 697', '602907697'), isTrue);
      expect(isSameAnswer('434 / 1131', '4341131'), isTrue);
      expect(isSameAnswer('11 / 9', '119'), isTrue);
      expect(isSameAnswer('7 / 9', '79'), isTrue);
      expect(isSameAnswer('4 / 7', '47'), isTrue);
      expect(isSameAnswer('5 / 2 / 1 / 7', '5217'), isTrue);
      expect(isSameAnswer('5, 2, 1, 7', '5217'), isTrue);
      expect(isSameAnswer('5 2 1 7', '5217'), isTrue);
      expect(isSameAnswer('5217', '5217'), isTrue);
      expect(isSameAnswer('5 / 2 / 1 / 7', '5, 2, 1, 7'), isTrue);
    });
  });
}
