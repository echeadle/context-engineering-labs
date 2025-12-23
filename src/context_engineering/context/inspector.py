from __future__ import annotations


from dataclasses import dataclass
from typing import Iterable


from rich.console import Console
from rich.table import Table


from context_engineering.types import Message




@dataclass(frozen=True)
class ContextStats:
    num_messages: int
    num_chars: int




def compute_stats(messages: Iterable[Message]) -> ContextStats:
    msgs = list(messages)
    return ContextStats(
        num_messages=len(msgs),
        num_chars=sum(len(m.content) for m in msgs),
    )




def print_context(messages: Iterable[Message]) -> None:
    table = Table(title="Context Inspector")
    table.add_column("#", justify="right")
    table.add_column("role")
    table.add_column("chars", justify="right")
    table.add_column("content")


    for i, m in enumerate(messages):
        preview = (m.content[:160] + "…") if len(m.content) > 160 else m.content
        table.add_row(str(i), m.role, str(len(m.content)), preview)


    stats = compute_stats(messages)
    console = Console()
    console.print(table)
    console.print(f"\nMessages: {stats.num_messages} | Characters: {stats.num_chars}")