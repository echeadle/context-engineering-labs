from __future__ import annotations

import pytest

from context_engineering.context.contract import ContractError, validate_contract


def test_contract_valid_json_parses() -> None:
    raw = '{"answer":"ok","assumptions":["a"],"sources_used":["s1"]}'
    parsed = validate_contract(raw)
    assert parsed.answer == "ok"
    assert parsed.assumptions == ["a"]
    assert parsed.sources_used == ["s1"]


def test_contract_rejects_non_json() -> None:
    raw = "not json"
    with pytest.raises(ContractError) as e:
        validate_contract(raw)
    assert "not valid JSON" in str(e.value)


def test_contract_rejects_missing_required_field() -> None:
    raw = '{"assumptions":[],"sources_used":[]}'
    with pytest.raises(ContractError) as e:
        validate_contract(raw)
    assert "does not match contract schema" in str(e.value)


def test_contract_rejects_wrong_type() -> None:
    raw = '{"answer":123,"assumptions":[],"sources_used":[]}'
    with pytest.raises(ContractError):
        validate_contract(raw)
