from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, Field, ValidationError


class ResponseContract(BaseModel):
    """A strict, machine-validated response shape.

    This is the core idea of a "context contract": your downstream code can rely
    on a stable schema instead of guessing what the model meant.
    """

    answer: str = Field(min_length=1)
    assumptions: list[str] = Field(default_factory=list)
    sources_used: list[str] = Field(default_factory=list)


@dataclass(frozen=True)
class ContractError(Exception):
    """Raised when model output is not valid for the contract."""

    message: str
    raw_text: str

    def __str__(self) -> str:  # pragma: no cover
        return self.message


def build_contract_instructions() -> str:
    """Instructions to force JSON-only output matching ResponseContract."""

    # Keep it short and strict on purpose.
    return (
        "Return ONLY valid JSON. No prose. No markdown. No code fences. "
        "The JSON must match this schema exactly:\n"
        "{\n"
        "  \"answer\": string,\n"
        "  \"assumptions\": [string, ...],\n"
        "  \"sources_used\": [string, ...]\n"
        "}\n"
    )


def _parse_json_object(raw_text: str) -> Any:
    """Parse JSON; raise ContractError with good diagnostics."""

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError as e:
        raise ContractError(
            message=f"Output is not valid JSON: {e}",
            raw_text=raw_text,
        )


def validate_contract(raw_text: str) -> ResponseContract:
    """Validate raw model output against the ResponseContract schema."""

    obj = _parse_json_object(raw_text)

    try:
        return ResponseContract.model_validate(obj)
    except ValidationError as e:
        raise ContractError(
            message=f"JSON does not match contract schema: {e}",
            raw_text=raw_text,
        )
