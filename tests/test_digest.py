from __future__ import annotations

from context_engineering.context.digest import digest_text_deterministic


def test_digest_respects_max_chars() -> None:
    text = "x" * 1000
    d = digest_text_deterministic(text, max_chars=120)
    assert len(d.text) <= 120


def test_digest_keeps_headings_and_bullets_when_possible() -> None:
    text = (
        "# Title\n"
        "intro line\n"
        "- bullet one\n"
        "- bullet two\n"
        + ("filler\n" * 50)
    )
    d = digest_text_deterministic(text, max_chars=200)
    assert "# Title" in d.text
    assert "- bullet one" in d.text
    assert "- bullet two" in d.text


def test_digest_truncates_with_ellipsis_when_needed() -> None:
    text = "# Title\n" + ("line\n" * 200)
    d = digest_text_deterministic(text, max_chars=80)
    assert d.text.endswith("…")
    assert len(d.text) <= 80
