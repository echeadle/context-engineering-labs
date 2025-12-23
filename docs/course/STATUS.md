# STATUS — Context Engineering Labs

Last updated: 2025-12-22

## Current health

✅ Build/compile:

```bash
uv run python -m compileall -q src tests examples
```

✅ Tests:

```bash
uv run pytest
```

Current: **15 passed, 1 skipped**

## What’s done

### Code labs (Weeks 0–6)

-   Week 00 — OpenAI smoke demo
-   Week 01 — Context inspector
-   Week 02 — Budgets + packers (priority-first, recency-first)
-   Week 03 — Output contracts (Pydantic validation)
-   Week 04 — Retrieval injection defense (scan/sanitize + bundle)
-   Week 05 — Deterministic digestion (lossy marker)
-   Week 06 — Tool logs as context (bounded transcript + redaction)

All demos are runnable from `examples/` and behavior is locked by tests in `tests/`.

## What’s next

### Course writing (Docs)

Write lessons:

-   `docs/course/week00.md`
-   `docs/course/week01.md`
-   `docs/course/week02.md`
-   `docs/course/week03.md`
-   `docs/course/week04.md`
-   `docs/course/week05.md`
-   `docs/course/week06.md`

Each lesson should include:

-   objective and key terms
-   exact run commands
-   walkthrough tied to the demo and tests
-   exercises
-   “definition of done” checklist

## Backlog (after docs)

-   Add a simple CLI runner (`scripts/run_week.sh` or `python -m ...`) to run week demos consistently.
-   Add a single “capstone” script that composes multiple primitives (pack + inject defense + tool transcript + contract).
-   Optional: add an LLM-based digest variant and contrast it with deterministic digestion.
