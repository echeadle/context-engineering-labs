from __future__ import annotations

import argparse

from context_engineering.context.budget import Budget
from context_engineering.context.inspector import print_context
from context_engineering.context.packer import pack_recency_first
from context_engineering.types import Message


def build_demo_messages(mult: int) -> list[Message]:
    return [
        Message(role="system", content="SYSTEM: policy must always remain."),
        Message(role="user", content="Old message " + ("old " * mult)),
        Message(role="user", content="Middle message " + ("mid " * mult)),
        Message(role="user", content="Newest message " + ("new " * mult)),
    ]


def main() -> None:
    ap = argparse.ArgumentParser(description="Week 2: budget + packer demo (chars-based).")
    ap.add_argument("--max-chars", type=int, default=220, help="Max total characters allowed.")
    ap.add_argument("--mult", type=int, default=60, help="Controls message length.")
    args = ap.parse_args()

    msgs = build_demo_messages(args.mult)
    budget = Budget(max_chars=args.max_chars)

    print("\n=== ORIGINAL ===")
    print_context(msgs)

    result = pack_recency_first(msgs, budget)
    print("\n=== DROP REASONS (chars) ===")
    for m in result.dropped:
        print(f"- {m.role}: {len(m.content)} chars | preview={m.content[:50]!r}")
        print(f"System chars: {len(result.packed[0].content)}")

    print("\n=== PACKED ===")
    print_context(result.packed)
    print(f"\nFinal chars: {result.final_chars} (budget={budget.max_chars})")

    if result.dropped:
        print("\n=== DROPPED ===")
        print_context(list(reversed(result.dropped)))  # show in chronological-ish order
    else:
        print("\nDropped: none")


if __name__ == "__main__":
    main()
