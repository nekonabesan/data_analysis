#!/usr/bin/env bash
set -eu

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
WORK_DIR="${PROJECT_ROOT}/work"
IMAGE_NAME="ferm-finance-jupyter:latest"
CONTAINER_NAME="stock_and_finance"
JUPYTER_TOKEN="vscode-jupyter-token"

mkdir -p "${WORK_DIR}"

# Compose 定義に沿って再構築・起動
cd "${SCRIPT_DIR}"
JUPYTER_TOKEN="${JUPYTER_TOKEN}" docker compose up -d --build

echo "Jupyter URL for VS Code: http://127.0.0.1:8888/?token=${JUPYTER_TOKEN}"
echo "Open container shell: docker exec -it ${CONTAINER_NAME} bash"