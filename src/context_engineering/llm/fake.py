from __future__ import annotations

from context_engineering.llm.base import LLMResult


class FakeLLM:
    """Deterministic offline model for unit tests."""

    def generate(self, *, instructions: str, input_text: str) -> LLMResult:
        # Intentionally naive: echo the input.
        return LLMResult(text=f"FAKE_MODEL_RESPONSE: {input_text}", raw=None)
