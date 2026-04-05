#!/usr/bin/env bash
set -euo pipefail

VENV_DIR="/tmp/prophet-venv"
READY_FILE="$VENV_DIR/.ready"

if [[ ! -f "$READY_FILE" ]]; then
  rm -rf "$VENV_DIR"
  python -m venv "$VENV_DIR"
  source "$VENV_DIR/bin/activate"
  pip install --no-cache-dir --upgrade pip
  pip install --no-cache-dir "numpy<2" pandas matplotlib plotly prophet==1.1.5 ipykernel
  PROPHET_STAN_DIR=$(python -c "from pathlib import Path; import prophet; print(Path(prophet.__file__).resolve().parent / 'stan_model')")
  python -m cmdstanpy.install_cmdstan --version 2.33.1 --dir "$PROPHET_STAN_DIR" --overwrite
  touch "$READY_FILE"
else
  source "$VENV_DIR/bin/activate"
fi

python -m ipykernel install --user --name python3 --display-name "Python 3 (Prophet)"
