from __future__ import annotations

import argparse

from context_engineering.context.budget import Budget
from context_engineering.context.inspector import print_context
from context_engineering.context.packer import pack_priority_first, pack_recency_first
from context_engineering.types import Message


def build_demo_messages(mult: int) -> list[Message]:
    return [
        Message(role="system", content="SYSTEM: policy must always remain."),
        Message(role="developer", content="DEV: Answer concisely. Use bullet points if helpful."),
        Message(role="user", content="Old user request " + ("old " * mult)),
        Message(role="assistant", content="Old assistant reply " + ("ok " * mult)),
        Message(role="tool", content="TOOL DIGEST: retrieved chunks " + ("chunk " * mult)),
        Message(role="user", content="Newest user request " + ("new " * mult)),
    ]


def show_result(title: str, msgs: list[Message], budget: Budget) -> None:
    print(f"\n\n==================== {title} ====================")
    result = (
        pack_recency_first(msgs, budget)
        if title.lower().startswith("recency")
        else pack_priority_first(msgs, budget)
    )

    print("\n--- PACKED ---")
    print_context(result.packed)
    print(f"\nFinal chars: {result.final_chars} (budget={budget.max_chars})")

    print("\n--- DROPPED (why) ---")
    if not result.dropped:
        print("Dropped: none")
        return

    for m in result.dropped:
        preview = (m.content[:60] + "…") if len(m.content) > 60 else m.content
        print(f"- {m.role:9s} | {len(m.content):4d} chars | {preview!r}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Compare recency-first vs priority-first packing.")
    ap.add_argument("--max-chars", type=int, default=300, help="Max total characters allowed.")
    ap.add_argument("--mult", type=int, default=40, help="Controls message length.")
    args = ap.parse_args()

    msgs = build_demo_messages(args.mult)
    budget = Budget(max_chars=args.max_chars)

    print("\n=== ORIGINAL ===")
    print_context(msgs)

    show_result("Recency-first", msgs, budget)
    show_result("Priority-first", msgs, budget)


if __name__ == "__main__":
    main()
