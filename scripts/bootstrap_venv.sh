#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -r requirements.txt
python -c "import requests; print('requests', requests.__version__)"
echo "已就绪。新终端请执行: source .venv/bin/activate （提示符前应显示 (.venv)）"
