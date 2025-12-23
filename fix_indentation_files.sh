#!/usr/bin/env bash
set -euo pipefail

# Run this from the repo root (context-engineering-labs/)

mkdir -p tests
mkdir -p src/context_engineering/llm

cat > tests/test_budget_and_packing.py <<'PY'
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
        Message(role="user", content="old" * 120),
        Message(role="user", content="new" * 120),
    ]

    budget = Budget(max_chars=220)
    result = pack_recency_first(msgs, budget)

    packed_text = " ".join(m.content for m in result.packed)
    assert "new" in packed_text
PY

cat > src/context_engineering/llm/fake.py <<'PY'
from __future__ import annotations

from context_engineering.llm.base import LLMResult


class FakeLLM:
    """Deterministic offline model for unit tests."""

    def generate(self, *, instructions: str, input_text: str) -> LLMResult:
        # Intentionally naive: echo the input.
        return LLMResult(text=f"FAKE_MODEL_RESPONSE: {input_text}", raw=None)
PY

cat > tests/test_openai_smoke.py <<'PY'
import os

import pytest

from context_engineering.llm.openai_client import OpenAIResponsesLLM


@pytest.mark.requires_llm
def test_openai_smoke() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY not set")

    llm = OpenAIResponsesLLM()
    res = llm.generate(
        instructions="Reply with exactly OK.",
        input_text="Return OK",
    )
    assert "OK" in res.text
PY

echo "Wrote: tests/test_budget_and_packing.py"
echo "Wrote: src/context_engineering/llm/fake.py"
echo "Wrote: tests/test_openai_smoke.py"
