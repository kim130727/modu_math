import builtins

from modu_semantic.rag.ocr import extract_ocr_features, merge_ocr_result_into_meta


def test_extract_ocr_features_returns_unavailable_when_dependency_missing(monkeypatch, tmp_path) -> None:
    real_import = builtins.__import__

    def _fake_import(name, *args, **kwargs):
        if name in {"PIL", "PIL.Image", "pytesseract"}:
            raise ImportError(f"mock missing: {name}")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", _fake_import)

    image_path = tmp_path / "img.png"
    image_path.write_bytes(b"not_a_real_png")

    result = extract_ocr_features(image_path)
    assert result.available is False
    assert "OCR dependency not available" in result.error


def test_merge_ocr_result_into_meta_writes_status_only_on_unavailable() -> None:
    result = extract_ocr_features("non_existent.png")
    merged = merge_ocr_result_into_meta({"tags": ["base"]}, result)
    assert merged["ocr_available"] is False
    assert merged["tags"] == ["base"]
