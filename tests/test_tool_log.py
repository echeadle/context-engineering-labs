from __future__ import annotations

from context_engineering.context.tool_log import ToolEvent, redact_secrets, render_tool_transcript


def test_redact_openai_key_like_strings() -> None:
    raw = "api_key=sk-THISISFAKEKEY1234567890"
    out = redact_secrets(raw)
    assert "sk-" not in out
    assert "<OPENAI_API_KEY_REDACTED>" in out


def test_render_transcript_bounded() -> None:
    events = [
        ToolEvent(tool_name="t1", tool_input="i" * 200, tool_output="o" * 200),
        ToolEvent(tool_name="t2", tool_input="i" * 200, tool_output="o" * 200),
        ToolEvent(tool_name="t3", tool_input="i" * 200, tool_output="o" * 200),
    ]

    out = render_tool_transcript(events, max_chars=250)
    assert len(out) <= 250


def test_render_transcript_prefers_newest_events() -> None:
    events = [
        ToolEvent(tool_name="old", tool_input="old", tool_output="old" * 200),
        ToolEvent(tool_name="new", tool_input="new", tool_output="new"),
    ]

    out = render_tool_transcript(events, max_chars=220)
    assert "tool=new" in out
    # Under a tight budget, the older big output should be dropped.
    assert "tool=old" not in out
