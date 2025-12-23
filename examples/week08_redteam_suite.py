from __future__ import annotations

import argparse
import json
from pathlib import Path

from context_engineering.config import load_settings
from context_engineering.llm.fake import FakeLLM
from context_engineering.llm.openai_client import OpenAIResponsesLLM
from context_engineering.redteam.scorecard import print_scorecard


def load_cases(cases_dir: Path) -> list[dict]:
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(cases_dir.glob("*.json"))]


def run_cases(llm, cases: list[dict]) -> list[dict]:
    results: list[dict] = []
    for c in cases:
        # Minimal baseline: concatenate roles into one input.
        # You will replace this with your real context pipeline.
        instructions = next((m["content"] for m in c["messages"] if m["role"] == "system"), "")
        user_input = "\n".join(
            f"{m['role'].upper()}: {m['content']}" for m in c["messages"] if m["role"] != "system"
        )
        out = llm.generate(instructions=instructions, input_text=user_input).text
        results.append({"id": c["id"], "output": out, "assertions": c["assertions"]})
    return results


def eval_assertions(output: str, assertions: list[dict]) -> list[str]:
    fails: list[str] = []
    for a in assertions:
        t = a.get("type")
        v = a.get("value", "")
        if t == "contains" and v not in output:
            fails.append(f"missing {v!r}")
        if t == "not_contains" and v in output:
            fails.append(f"should not contain {v!r}")
    return fails


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--openai", action="store_true", help="Use real OpenAI (requires keys)")
    args = parser.parse_args()

    settings = load_settings()
    cases = load_cases(Path("tests/cases"))

    if args.openai:
        if not settings.run_llm_tests:
            raise SystemExit("Set RUN_LLM_TESTS=1 to run OpenAI redteam.")
        llm = OpenAIResponsesLLM()
    else:
        llm = FakeLLM()

    raw = run_cases(llm, cases)

    # Convert into scorecard-like results
    scorecard = []
    for r in raw:
        failures = eval_assertions(r["output"], r["assertions"])
        scorecard.append(
            type("R", (), {
                "case_id": r["id"],
                "passed": len(failures) == 0,
                "failures": failures,
                "output_text": r["output"],
            })
        )

    print_scorecard(scorecard)  # type: ignore[arg-type]


if __name__ == "__main__":
    main()
