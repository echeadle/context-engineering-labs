from __future__ import annotations


from dataclasses import dataclass
from typing import Any, Literal


Role = Literal["system", "developer", "user", "assistant", "tool"]




@dataclass(frozen=True)
class Message:
    role: Role
    content: str
    name: str | None = None
    meta: dict[str, Any] | None = None