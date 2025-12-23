from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

# Ensure "src" is on the import path even if the project isn't installed.
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def llm_enabled() -> bool:
    return os.getenv("RUN_LLM_TESTS", "0").strip().lower() in {"1", "true", "yes"}


def pytest_runtest_setup(item):
    if "requires_llm" in item.keywords and not llm_enabled():
        pytest.skip("RUN_LLM_TESTS!=1")
