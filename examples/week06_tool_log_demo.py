from __future__ import annotations

from context_engineering.context.budget import Budget
from context_engineering.context.inspector import print_context
from context_engineering.context.packer import pack_priority_first
from context_engineering.context.tool_log import ToolEvent, render_tool_transcript
from context_engineering.types import Message


def main() -> None:
    # Order matters because the transcript keeps newest-first.
    # Put the huge output first (oldest), so it gets dropped/truncated if needed,
    # and keep the redaction example in a newer event so you can see it.
    events = [
        ToolEvent(
            tool_name="web.search",
            tool_input="q=wheelchair rental denver",
            tool_output=("lots of results\n" * 40),
        ),
        ToolEvent(
            tool_name="db.query",
            tool_input="SELECT * FROM prefs WHERE user_id=1; token=abc123",
            tool_output="rows=1; api_key=sk-THISISFAKEKEY1234567890",
        ),
        ToolEvent(
            tool_name="web.search",
            tool_input="q=denver accessible hotels",
            tool_output="found: Hotel A, Hotel B",
        ),
    ]

    transcript = render_tool_transcript(events, max_chars=400)

    msgs = [
        Message(role="system", content="SYSTEM: output JSON. Follow safety policy."),
        Message(role="developer", content="DEV: keep it concise."),
        Message(role="user", content="Plan a 2-day accessible Denver trip."),
        Message(role="tool", content=transcript),
        Message(role="user", content="Give me two hotel options and a packing list."),
    ]

    budget = Budget(max_chars=650)

    print("\n=== ORIGINAL ===")
    print_context(msgs)

    packed = pack_priority_first(msgs, budget)

    print("\n=== PACKED ===")
    print_context(packed.packed)
    print(f"\nFinal chars: {packed.final_chars} (budget={budget.max_chars})")

    print("\n=== TOOL TRANSCRIPT (rendered) ===\n")
    print(transcript)


if __name__ == "__main__":
    main()
