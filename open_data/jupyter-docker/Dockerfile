FROM jupyter/base-notebook:latest

USER root

# matplotlib の日本語表示用フォントをインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
	fonts-noto-cjk \
	fonts-ipaexfont-gothic \
	fonts-ipaexfont-mincho \
	fontconfig \
	&& rm -rf /var/lib/apt/lists/*

USER ${NB_UID}

# コンテナ初期構築に必要な最小パッケージのみインストール
COPY --chown=${NB_UID}:users requestment.txt /tmp/requestment.txt
COPY --chown=${NB_UID}:users pyproject.toml /tmp/env/pyproject.toml

RUN pip install --no-cache-dir -r /tmp/requestment.txt

# Python依存は uv で管理し、仮想環境へ同期する
RUN python -m venv /tmp/notebook-venv && \
	. /tmp/notebook-venv/bin/activate && \
	UV_PROJECT_ENVIRONMENT=/tmp/notebook-venv uv sync --project /tmp/env --no-dev && \
	python -m ipykernel install --user --name python3 --display-name "Python 3 (open_data)"

# コンテナシェルから追加インストールしやすいように明示
ENV PIP_DISABLE_PIP_VERSION_CHECK=1