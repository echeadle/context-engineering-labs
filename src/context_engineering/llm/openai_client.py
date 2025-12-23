from __future__ import annotations

from dataclasses import dataclass

from openai import OpenAI

from context_engineering.config import load_settings
from context_engineering.llm.base import LLMResult


@dataclass
class OpenAIResponsesLLM:
    model: str | None = None

    def __post_init__(self) -> None:
        s = load_settings()
        self.model = self.model or s.openai_model
        self._client = OpenAI()
        self._safety_identifier = s.safety_identifier

    def generate(self, *, instructions: str, input_text: str) -> LLMResult:
        resp = self._client.responses.create(
            model=self.model,
            instructions=instructions,
            input=input_text,
            safety_identifier=self._safety_identifier,
        )
        return LLMResult(text=resp.output_text, raw=resp)
