from __future__ import annotations


import os
from dataclasses import dataclass


from dotenv import load_dotenv




@dataclass(frozen=True)
class Settings:
    openai_model: str
    run_llm_tests: bool
    safety_identifier: str | None




def load_settings() -> Settings:
    load_dotenv()
    model = os.getenv("OPENAI_MODEL", "gpt-5").strip()
    run_llm_tests = os.getenv("RUN_LLM_TESTS", "0").strip().lower() in {"1", "true", "yes"}
    safety_identifier = os.getenv("OPENAI_SAFETY_IDENTIFIER")
    safety_identifier = safety_identifier.strip() if safety_identifier else None
    return Settings(openai_model=model, run_llm_tests=run_llm_tests, safety_identifier=safety_identifier)