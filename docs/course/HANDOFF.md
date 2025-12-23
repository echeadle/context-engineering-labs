# Course Handoff Summary — Context Engineering Labs

This repo (`context-engineering-labs`) contains a **code-first, test-driven** set of labs for learning **context engineering** in Python. The code is built with `uv` and currently passes:

```bash
uv run python -m compileall -q src tests examples
uv run pytest
```

Current test status: **15 passed, 1 skipped** (the skip is an optional LLM-gated test).

## What’s implemented (Weeks 0–6)

### Week 00 — OpenAI smoke

-   Demo: `examples/week00_openai_smoke.py`
-   Purpose: confirm environment wiring and a basic OpenAI call path.

### Week 01 — Context inspection

-   Demo: `examples/week01_context_inspector.py`
-   Purpose: make message lists visible (role + character counts) so “context cost” is measurable.

### Week 02 — Budgets + packing

-   Demo: `examples/week02_context_packer.py`
-   Core: `src/context_engineering/context/budget.py`, `src/context_engineering/context/packer.py`
-   Purpose: fit messages under a fixed budget using explicit policies (priority-first vs recency-first).

### Week 03 — Contracts (schema validation)

-   Demo: `examples/week03_contract_demo.py`
-   Core: `src/context_engineering/context/contract.py`
-   Tests: `tests/test_contracts.py`
-   Purpose: constrain model output shape with Pydantic validation; fail fast on invalid outputs.

### Week 04 — Retrieval injection defense

-   Demo: `examples/week04_injection_demo.py`
-   Core: `src/context_engineering/context/injection.py`, `src/context_engineering/context/retrieval_bundle.py`
-   Tests: `tests/test_injection.py`
-   Purpose: treat retrieved text as untrusted; label as DATA; scan/sanitize common injection patterns.

### Week 05 — Deterministic digestion

-   Demo: `examples/week05_digest_demo.py`
-   Core: `src/context_engineering/context/digest.py`
-   Tests: `tests/test_digest.py`
-   Purpose: compress text deterministically (no LLM) while preserving headings/bullets and marking lossy compression with an ellipsis.

### Week 06 — Tool logs as context

-   Demo: `examples/week06_tool_log_demo.py`
-   Core: `src/context_engineering/context/tool_log.py`
-   Tests: `tests/test_tool_log.py`
-   Purpose: include tool output safely via a bounded transcript with secret redaction and newest-first retention.

## What we’re doing next

The **code track for Weeks 0–6 is complete**. Next work is writing the **course material** week-by-week:

-   Course index: `docs/course/README.md`
-   Lessons to write: `docs/course/week00.md` … `docs/course/week06.md`

Each lesson should include:

-   objective + key terms
-   exact run commands
-   walkthrough tied directly to the demo/test code
-   exercises and a “definition of done” checklist
