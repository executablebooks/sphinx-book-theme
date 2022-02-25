from sphinx_book_theme.translations._convert import convert_json


def test_convert(tmp_path, monkeypatch):
    (tmp_path / "jsons").mkdir()
    (tmp_path / "jsons" / "test.json").write_text(
        '[{"language":"English","symbol":"en","text":"Text"},'
        '{"language":"Other","symbol":"ot","text":"Translate"}]'
    )
    monkeypatch.setattr("subprocess.check_call", lambda args: None)
    convert_json(tmp_path)
    assert (tmp_path / "locales" / "ot").exists()
    path = tmp_path / "locales" / "ot" / "LC_MESSAGES"
    assert (path / "booktheme.po").exists()
    # assert (path / "booktheme.mo").exists()
    assert "Translate" in (path / "booktheme.po").read_text("utf8")
