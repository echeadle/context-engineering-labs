import os
import pytest
from dotenv import load_dotenv

from context_engineering.llm.openai_client import OpenAIResponsesLLM


@pytest.mark.requires_llm
def test_openai_smoke() -> None:
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY not set")

    llm = OpenAIResponsesLLM()
    res = llm.generate(
        instructions="Reply with exactly OK.",
        input_text="Return OK",
    )
    assert "OK" in res.text
