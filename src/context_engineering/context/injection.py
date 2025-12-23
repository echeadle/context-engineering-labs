from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class InjectionFinding:
    kind: str
    snippet: str


# Heuristic patterns. These are intentionally simple for a course.
_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    (
        "override-instructions",
        re.compile(r"\b(ignore|disregard|override)\b.{0,80}\b(instruction|system|developer|previous)\b", re.I | re.S),
    ),
    (
        "roleplay-system",
        re.compile(r"\byou are (now|no longer)\b.{0,60}\b(system|developer)\b", re.I | re.S),
    ),
    (
        "exfiltrate-secrets",
        re.compile(r"\b(api\s*key|secret|password|token)\b", re.I),
    ),
    (
        "tool-abuse",
        re.compile(r"\b(call|use|invoke)\b.{0,40}\b(tool|function)\b", re.I | re.S),
    ),
]


def scan_for_injection(text: str) -> list[InjectionFinding]:
    findings: list[InjectionFinding] = []
    for kind, pat in _PATTERNS:
        m = pat.search(text)
        if m:
            snippet = text[m.start() : min(len(text), m.end() + 40)]
            findings.append(InjectionFinding(kind=kind, snippet=snippet.strip()))
    return findings


def sanitize_retrieved_text(text: str) -> str:
    """Remove common injection lines from retrieved text.

    This is NOT a security solution. It's a teaching primitive:
    - show that retrieved context often contains instruction-like strings
    - demonstrate a defensive cleaning step

    Strategy:
    - drop lines containing high-risk phrases
    - preserve everything else
    """

    drop_line = re.compile(
        r"(ignore|disregard|override|system prompt|developer message|api\s*key|password|secret|token)",
        re.I,
    )

    cleaned_lines: list[str] = []
    for line in text.splitlines():
        if drop_line.search(line):
            continue
        cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()
