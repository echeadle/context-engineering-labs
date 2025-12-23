from __future__ import annotations

import os

from dotenv import load_dotenv

from context_engineering.context.contract import (
    ContractError,
    build_contract_instructions,
    validate_contract,
)
from context_engineering.llm.openai_client import OpenAIResponsesLLM


def main() -> None:
    load_dotenv()

    prompt = "Explain what context engineering is in one sentence."
    instructions = build_contract_instructions()

    # If you want to run this without an API key, just hardcode a valid JSON string.
    if not os.getenv("OPENAI_API_KEY"):
        raw = '{"answer":"Context engineering is the deliberate design of what information goes into and stays in a model’s context.","assumptions":[],"sources_used":[]}'
        print("No OPENAI_API_KEY found; using offline sample output.\n")
    else:
        llm = OpenAIResponsesLLM()
        res = llm.generate(instructions=instructions, input_text=prompt)
        raw = res.text

    print("RAW MODEL OUTPUT:\n")
    print(raw)
    print("\n---\n")

    try:
        parsed = validate_contract(raw)
    except ContractError as e:
        print("CONTRACT VALIDATION FAILED:\n")
        print(e.message)
        return

    print("CONTRACT VALIDATION PASSED:\n")
    print(parsed.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
