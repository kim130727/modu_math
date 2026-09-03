from modu_math.dsl.symbol_roles import is_symbol_marker_text, localize_jamo_markers


def test_localize_jamo_markers_uses_each_language_sequence() -> None:
    source = "ㄱ, ㄴ, ㄷ / 선분 ㄷㄹ / ㉠㉡㉢ / ㉮㉯㉰ / ㈀㈁㈂ / ㈎㈏㈐"

    assert localize_jamo_markers(source, "en-US") == "A, B, C / 선분 CD / ABC / ABC / ABC / ABC"
    assert localize_jamo_markers(source, "uk") == "А, Б, В / 선분 ВГ / АБВ / АБВ / АБВ / АБВ"
    assert localize_jamo_markers(source, "zh-CN") == "甲, 乙, 丙 / 선분 丙丁 / 甲乙丙 / 甲乙丙 / 甲乙丙 / 甲乙丙"
    assert localize_jamo_markers(source, "ja") == "ア, イ, ウ / 선분 ウエ / アイウ / アイウ / アイウ / アイウ"
    assert localize_jamo_markers(source, "km-KH") == "ក, ខ, គ / 선분 គឃ / កខគ / កខគ / កខគ / កខគ"


def test_all_korean_special_choice_markers_are_recognized() -> None:
    marker_sets = (
        "ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎ",
        "㉠㉡㉢㉣㉤㉥㉦㉧㉨㉩㉪㉫㉬㉭",
        "㉮㉯㉰㉱㉲㉳㉴㉵㉶㉷㉸㉹㉺㉻",
        "㈀㈁㈂㈃㈄㈅㈆㈇㈈㈉㈊㈋㈌㈍",
        "㈎㈏㈐㈑㈒㈓㈔㈕㈖㈗㈘㈙㈚㈛",
    )

    assert all(is_symbol_marker_text(markers) for markers in marker_sets)
    assert localize_jamo_markers(marker_sets[1], "en") == "ABCDEFGHIJKLMN"
    assert localize_jamo_markers(marker_sets[3], "zh") == "甲乙丙丁戊己庚辛壬癸子丑寅卯"


def test_localize_jamo_markers_does_not_change_words_or_neutral_markers() -> None:
    source = "① 가나다 / ㄱ"

    assert localize_jamo_markers(source, "en") == "① 가나다 / A"
    assert localize_jamo_markers(source, "ko") == source
    assert localize_jamo_markers(source, "unknown") == source
