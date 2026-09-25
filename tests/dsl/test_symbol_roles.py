from modu_math.dsl.symbol_roles import is_symbol_marker_text, localize_jamo_markers


def test_localize_jamo_markers_uses_ukrainian_sequence() -> None:
    source = "ㄱ, ㄴ, ㄷ / 선분 ㄷㄹ / ㉠㉡㉢ / ㉮㉯㉰ / ㈀㈁㈂ / ㈎㈏㈐"

    assert localize_jamo_markers(source, "uk") == "А, Б, В / 선분 ВГ / АБВ / АБВ / АБВ / АБВ"


def test_all_korean_special_choice_markers_are_recognized() -> None:
    marker_sets = (
        "ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎ",
        "㉠㉡㉢㉣㉤㉥㉦㉧㉨㉩㉪㉫㉬㉭",
        "㉮㉯㉰㉱㉲㉳㉴㉵㉶㉷㉸㉹㉺㉻",
        "㈀㈁㈂㈃㈄㈅㈆㈇㈈㈉㈊㈋㈌㈍",
        "㈎㈏㈐㈑㈒㈓㈔㈕㈖㈗㈘㈙㈚㈛",
    )

    assert all(is_symbol_marker_text(markers) for markers in marker_sets)
    assert localize_jamo_markers(marker_sets[1], "uk") == "АБВГҐДЕЄЖЗИІЇЙ"


def test_localize_jamo_markers_does_not_change_words_or_neutral_markers() -> None:
    source = "① 가나다 / ㄱ"

    assert localize_jamo_markers(source, "uk") == "① 가나다 / А"
    assert localize_jamo_markers(source, "ko") == source
    assert localize_jamo_markers(source, "unknown") == source
