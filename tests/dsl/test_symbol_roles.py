from modu_math.dsl.symbol_roles import localize_jamo_markers


def test_localize_jamo_markers_uses_each_language_sequence() -> None:
    source = "ㄱ, ㄴ, ㄷ / 선분 ㄷㄹ / ㉠㉡㉢"

    assert localize_jamo_markers(source, "en-US") == "A, B, C / 선분 CD / ABC"
    assert localize_jamo_markers(source, "uk") == "А, Б, В / 선분 ВГ / АБВ"
    assert localize_jamo_markers(source, "zh-CN") == "甲, 乙, 丙 / 선분 丙丁 / 甲乙丙"
    assert localize_jamo_markers(source, "ja") == "ア, イ, ウ / 선분 ウエ / アイウ"
    assert localize_jamo_markers(source, "km-KH") == "ក, ខ, គ / 선분 គឃ / កខគ"


def test_localize_jamo_markers_does_not_change_words_or_neutral_markers() -> None:
    source = "① 가나다 / ㄱ"

    assert localize_jamo_markers(source, "en") == "① 가나다 / A"
    assert localize_jamo_markers(source, "ko") == source
    assert localize_jamo_markers(source, "unknown") == source
