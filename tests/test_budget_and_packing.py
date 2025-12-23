from __future__ import annotations

from context_engineering.context.budget import Budget
from context_engineering.context.packer import pack_recency_first
from context_engineering.types import Message


def test_packer_keeps_system_message() -> None:
    msgs = [
        Message(role="system", content="SYS" * 50),
        Message(role="user", content="A" * 200),
        Message(role="user", content="B" * 200),
    ]

    budget = Budget(max_chars=260)
    result = pack_recency_first(msgs, budget)

    assert result.packed[0].role == "system"
    assert result.final_chars <= 260


def test_packer_prefers_newest() -> None:
    msgs = [
        Message(role="system", content="SYS"),
        Message(role="user", content="old" * 30),
        Message(role="user", content="new" * 30),
    ]

    budget = Budget(max_chars=220)
    result = pack_recency_first(msgs, budget)

    packed_text = " ".join(m.content for m in result.packed)
    assert "new" in packed_text
