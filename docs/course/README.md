# Context Engineering Labs — Course Index

This folder contains the **course material** for the `context-engineering-labs` repo.

## Who this is for

You’re an intermediate Python programmer who has built basic agents/RAG prototypes and wants to learn **context engineering** as a practical, test-driven discipline.

## What “context engineering” means in this course

**Context engineering** is the deliberate design of:

-   **What** goes into the model’s context (messages, retrieved text, tool logs)
-   **In what order** it appears
-   **How much** is allowed (budgets)
-   **How it’s labeled** (data vs instructions)
-   **How outputs are constrained** (contracts)

This course is intentionally **code-first** and **inspectable**.

## Repo baseline

From repo root:

```bash
uv run python -m compileall -q src tests examples
uv run pytest
```

Expected: all deterministic tests pass; one LLM-marked test may be skipped unless you enable it.

## Course structure

Each week has:

-   A lesson doc: `docs/course/weekXX.md`
-   A runnable demo: `examples/weekXX_*.py`
-   Tests that lock behavior: `tests/test_*.py`

## Weeks

### Week 00 — OpenAI smoke (wiring + env)

**Goal:** Verify local environment + OpenAI call path.

-   Demo: `examples/week00_openai_smoke.py`
-   Skills:

    -   `.env` loading
    -   basic LLM call sanity check

### Week 01 — Context inspection (measure what you’re sending)

**Goal:** Make context visible: roles + character counts.

-   Demo: `examples/week01_context_inspector.py`
-   Skills:

    -   inspecting message lists
    -   understanding “context cost”

### Week 02 — Budgets + packing strategies

**Goal:** Fit messages under a budget with explicit policies.

-   Demo: `examples/week02_context_packer.py`
-   Core code: `src/context_engineering/context/budget.py`, `src/context_engineering/context/packer.py`
-   Skills:

    -   budgets as first-class constraints
    -   packing policies (priority-first vs recency-first)

### Week 03 — Context contracts (shape, not hope)

**Goal:** Validate model outputs against a strict schema.

-   Demo: `examples/week03_contract_demo.py`
-   Core code: `src/context_engineering/context/contract.py`
-   Tests: `tests/test_contracts.py`
-   Skills:

    -   JSON-only outputs
    -   schema validation
    -   failing fast on invalid responses

### Week 04 — Retrieval injection defense (data ≠ instructions)

**Goal:** Treat retrieved text as hostile; label and sanitize it.

-   Demo: `examples/week04_injection_demo.py`
-   Core code:

    -   `src/context_engineering/context/injection.py`
    -   `src/context_engineering/context/retrieval_bundle.py`

-   Tests: `tests/test_injection.py`
-   Skills:

    -   scanning for injection patterns
    -   bundling retrieved chunks with a “DATA” header
    -   simple sanitization step

### Week 05 — Deterministic digestion (compress without an LLM)

**Goal:** Shrink context while keeping structure and leaving a visible “compression happened” marker.

-   Demo: `examples/week05_digest_demo.py`
-   Core code: `src/context_engineering/context/digest.py`
-   Tests: `tests/test_digest.py`
-   Skills:

    -   deterministic summarization heuristics
    -   keeping headings/bullets
    -   ellipsis markers for lossy compression

### Week 06 — Tool logs as context (bounded + redacted)

**Goal:** Include tool output safely via a bounded transcript with secret redaction.

-   Demo: `examples/week06_tool_log_demo.py`
-   Core code: `src/context_engineering/context/tool_log.py`
-   Tests: `tests/test_tool_log.py`
-   Skills:

    -   transcript formatting as a context primitive
    -   redaction patterns
    -   newest-first retention under tight budgets

## How to work through the course

For each week:

1. Read `docs/course/weekXX.md`
2. Run the demo script
3. Run the tests
4. Do the exercises (and optionally add your own tests)

## Course-wide definition of done

A week is “done” when:

-   `uv run python -m compileall -q src tests examples` is clean
-   `uv run pytest` is green
-   You can explain, in your own words:

    -   what the week’s primitive is
    -   what problem it solves
    -   what it _does not_ solve

## Next files to write

-   `docs/course/week00.md`
-   `docs/course/week01.md`
-   `docs/course/week02.md`
-   `docs/course/week03.md`
-   `docs/course/week04.md`
-   `docs/course/week05.md`
-   `docs/course/week06.md`

(We’ll do one week at a time.)
