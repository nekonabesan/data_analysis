#!/usr/bin/env bash
set -eu

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
WORK_DIR="${PROJECT_ROOT}/work"
IMAGE_NAME="ferm-jupyter:latest"
CONTAINER_NAME="jupyter"
JUPYTER_TOKEN="vscode-jupyter-token"

mkdir -p "${WORK_DIR}"

# 既存コンテナがあれば削除して起動し直す
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
  docker rm -f "${CONTAINER_NAME}" >/dev/null
fi

docker build -t "${IMAGE_NAME}" "${SCRIPT_DIR}"

docker run -d \
  --name "${CONTAINER_NAME}" \
  -p 8888:8888 \
  -v "${WORK_DIR}:/home/jovyan/work" \
  "${IMAGE_NAME}" \
  start-notebook.sh \
    --NotebookApp.token="${JUPYTER_TOKEN}" \
    --NotebookApp.password='' \
    --NotebookApp.allow_origin='*'

echo "Jupyter URL for VS Code: http://127.0.0.1:8888/?token=${JUPYTER_TOKEN}"
echo "Open container shell: docker exec -it ${CONTAINER_NAME} bash"