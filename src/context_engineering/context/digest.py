from __future__ import annotations

import re
from dataclasses import dataclass

from context_engineering.types import Message


@dataclass(frozen=True)
class DigestResult:
    text: str
    original_chars: int
    digest_chars: int


_heading = re.compile(r"^\s{0,3}#{1,6}\s+.+")
_bullet = re.compile(r"^\s{0,8}([-*]|\d+\.)\s+.+")


def digest_text_deterministic(text: str, *, max_chars: int) -> DigestResult:
    """Deterministically compress text to <= max_chars.

    Teaching goals:
    - fully inspectable (no LLM)
    - biased toward keeping structure (headings/bullets) and early lines

    Heuristic:
    1) Keep the first 6 non-empty lines
    2) Keep all headings and bullet lines (in order)
    3) If any content was dropped, append an ellipsis marker (…)
    4) If still too long, hard truncate to max_chars and end with …

    This is intentionally naive but stable.
    """

    original_chars = len(text)

    lines = [ln.rstrip() for ln in text.splitlines()]
    non_empty = [ln for ln in lines if ln.strip()]

    keep: list[str] = []

    # First 6 non-empty lines preserve the "opening" context.
    keep.extend(non_empty[:6])

    # Headings + bullets preserve structured content.
    for ln in lines:
        if _heading.match(ln) or _bullet.match(ln):
            if ln not in keep:
                keep.append(ln)

    out = "\n".join(keep).strip()

    # If we dropped anything (lossy digest), mark it clearly.
    # This helps students see "compression happened" even when under budget.
    if original_chars > len(out) and max_chars > 0:
        if len(out) >= max_chars:
            out = out[: max(0, max_chars - 1)].rstrip() + "…"
        elif not out.endswith("…"):
            if len(out) + 1 <= max_chars:
                out = out + "…"
            else:
                out = out[: max(0, max_chars - 1)].rstrip() + "…"

    # Final hard cap safety.
    if len(out) > max_chars and max_chars > 0:
        out = out[: max(0, max_chars - 1)].rstrip() + "…"
    elif max_chars == 0:
        out = ""

    return DigestResult(text=out, original_chars=original_chars, digest_chars=len(out))


def digest_messages(messages: list[Message], *, max_chars_per_message: int) -> list[Message]:
    """Return a message list where each message content is deterministically digested."""

    out: list[Message] = []
    for m in messages:
        d = digest_text_deterministic(m.content, max_chars=max_chars_per_message)
        out.append(
            Message(
                role=m.role,
                content=d.text,
                name=m.name,
                meta={
                    **(m.meta or {}),
                    "digest": {
                        "original_chars": d.original_chars,
                        "digest_chars": d.digest_chars,
                    },
                },
            )
        )
    return out
