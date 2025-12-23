from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from context_engineering.context.budget import Budget, size_chars
from context_engineering.types import Message


@dataclass(frozen=True)
class PackResult:
    packed: list[Message]
    dropped: list[Message]
    final_chars: int


def pack_recency_first(messages: Iterable[Message], budget: Budget) -> PackResult:
    """Keep newest non-system messages first, but always keep the first system message."""

    msgs = list(messages)
    system = [m for m in msgs if m.role == "system"]
    rest = [m for m in msgs if m.role != "system"]

    packed_rev: list[Message] = []
    dropped: list[Message] = []

    if system:
        packed_rev.append(system[0])

    # Try to add from newest->oldest
    for m in reversed(rest):
        candidate = packed_rev + [m]
        if size_chars(candidate) <= budget.max_chars:
            packed_rev.append(m)
        else:
            dropped.append(m)

    # Restore chronological ordering
    if packed_rev and packed_rev[0].role == "system":
        sys0 = packed_rev[0]
        others = list(reversed(packed_rev[1:]))
        packed = [sys0] + others
    else:
        packed = list(reversed(packed_rev))

    return PackResult(packed=packed, dropped=dropped, final_chars=size_chars(packed))


def pack_priority_first(messages: Iterable[Message], budget: Budget) -> PackResult:
    """Pack by priority groups, then fill remaining space with recency.

    Priority order:
      1) first system message (always attempted)
      2) all developer messages (in order)
      3) latest user message
      4) all tool messages (in order)
      5) everything else (newest first)

    Notes:
    - This is a *context engineering* policy, not a "best" policy.
    - All decisions are budget-driven using a simple char counter.
    """

    msgs = list(messages)
    n = len(msgs)

    idx_system0 = next((i for i, m in enumerate(msgs) if m.role == "system"), None)
    developer_idxs = [i for i, m in enumerate(msgs) if m.role == "developer"]
    tool_idxs = [i for i, m in enumerate(msgs) if m.role == "tool"]

    user_idxs = [i for i, m in enumerate(msgs) if m.role == "user"]
    latest_user_idx = max(user_idxs) if user_idxs else None

    selected: list[int] = []

    def try_add(i: int) -> bool:
        nonlocal selected
        if i in selected:
            return True
        candidate = [msgs[j] for j in selected] + [msgs[i]]
        if size_chars(candidate) <= budget.max_chars:
            selected.append(i)
            return True
        return False

    # 1) system (first)
    if idx_system0 is not None:
        try_add(idx_system0)

    # 2) developer
    for i in developer_idxs:
        try_add(i)

    # 3) latest user
    if latest_user_idx is not None:
        try_add(latest_user_idx)

    # 4) tools
    for i in tool_idxs:
        try_add(i)

    # 5) fill remainder newest->oldest, skipping system (already attempted)
    remaining = [i for i in range(n) if i not in selected]
    remaining.sort(reverse=True)
    for i in remaining:
        # Don’t re-attempt system if it wasn’t selected (budget too small)
        if idx_system0 is not None and i == idx_system0:
            continue
        try_add(i)

    packed_idxs = sorted(selected)
    packed = [msgs[i] for i in packed_idxs]
    dropped = [msgs[i] for i in range(n) if i not in packed_idxs]

    return PackResult(packed=packed, dropped=dropped, final_chars=size_chars(packed))
