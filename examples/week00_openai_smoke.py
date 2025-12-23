from __future__ import annotations

from dotenv import load_dotenv

from context_engineering.llm.openai_client import OpenAIResponsesLLM


def main() -> None:
    load_dotenv()
    llm = OpenAIResponsesLLM()
    res = llm.generate(
        instructions="Reply with exactly one token: OK",
        input_text="Return OK",
    )
    print(res.text)


if __name__ == "__main__":
    main()
