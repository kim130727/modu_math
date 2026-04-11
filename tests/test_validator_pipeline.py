from modu_semantic.validator import validate_all_examples


def test_fixture_bundles_validate_cleanly() -> None:
    failures = validate_all_examples("tests/fixtures/bundles")
    assert failures == {}
