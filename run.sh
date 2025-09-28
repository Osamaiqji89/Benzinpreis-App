#!/usr/bin/env bash
set -euo pipefail
# Simple runner for the Benzinpreis-App
# Usage: ./run.sh

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

# Create virtualenv if missing
if [ ! -d ".venv" ]; then
  echo "Creating virtualenv .venv..."
  python3 -m venv .venv
fi

# Activate
source .venv/bin/activate

# Upgrade pip and install requirements
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Run the app using the venv python
.venv/bin/python main.py
