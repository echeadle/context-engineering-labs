#!/usr/bin/env bash
set -euo pipefail
RUN_LLM_TESTS=${RUN_LLM_TESTS:-1}
uv run python examples/week08_redteam_suite.py --openai

