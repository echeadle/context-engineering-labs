#!/usr/bin/env bash
set -euo pipefail
EXAMPLE=${1:-examples/week01_context_inspector.py}
uv run python "$EXAMPLE"
