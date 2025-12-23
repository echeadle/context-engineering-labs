from __future__ import annotations


from dataclasses import dataclass
from typing import Any, Protocol




@dataclass(frozen=True)
class LLMResult:
    text: str
    raw: Any


class LLM(Protocol):
    def generate(self, *, instructions: str, input_text: str) -> LLMResult: ...
    pass