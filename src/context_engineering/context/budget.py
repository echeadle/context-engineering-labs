from __future__ import annotations


from dataclasses import dataclass
from typing import Iterable


from context_engineering.types import Message




@dataclass(frozen=True)
class Budget:
    max_chars: int




def size_chars(messages: Iterable[Message]) -> int:
    return sum(len(m.content) for m in messages)