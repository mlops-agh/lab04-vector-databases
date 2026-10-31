#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

uv run python -m scripts.create_tables
uv run python -m scripts.seed_images
uv run python -m scripts.load_games