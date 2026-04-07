FROM jupyter/base-notebook:python-3.10

USER root

# matplotlib の日本語表示用フォントをインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
	fonts-noto-cjk \
	fonts-ipaexfont-gothic \
	fonts-ipaexfont-mincho \
	fontconfig \
	&& rm -rf /var/lib/apt/lists/*

# TA-Lib C ライブラリのビルド・インストール
RUN apt-get update && apt-get install -y --no-install-recommends \
	build-essential \
	wget \
	&& rm -rf /var/lib/apt/lists/* \
	&& wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz \
	&& tar -xzf ta-lib-0.4.0-src.tar.gz \
	&& cd ta-lib/ \
	&& ./configure --prefix=/usr \
	&& make && make install \
	&& cd .. \
	&& rm -rf ta-lib ta-lib-0.4.0-src.tar.gz

USER ${NB_UID}

# コンテナ初期構築に必要な最小パッケージのみインストール
COPY --chown=${NB_UID}:users requestment.txt /tmp/requestment.txt
COPY --chown=${NB_UID}:users pyproject.toml /tmp/env/pyproject.toml

RUN pip install --no-cache-dir -r /tmp/requestment.txt

# Python依存は uv で管理し、Prophet 用の分離仮想環境へ同期する
RUN python -m venv /tmp/prophet-venv && \
	. /tmp/prophet-venv/bin/activate && \
	UV_PROJECT_ENVIRONMENT=/tmp/prophet-venv uv sync --project /tmp/env --no-dev && \
	PROPHET_STAN_DIR=$(python -c "from pathlib import Path; import prophet; print(Path(prophet.__file__).resolve().parent / \"stan_model\")") && \
	python -m cmdstanpy.install_cmdstan --version 2.33.1 --dir "$PROPHET_STAN_DIR" --overwrite && \
	python -m ipykernel install --user --name python3 --display-name "Python 3 (Prophet)" && \
	INSTALL_PY=/tmp/prophet-venv/lib/python3.10/site-packages/cmdstanpy/install_cmdstan.py && \
	sed -i 's/^    import readline/    pass  # import readline disabled (segfault workaround)/' "$INSTALL_PY" && \
	sed -i 's/^    _ = readline\.__doc__/    pass  # readline disabled/' "$INSTALL_PY"

# コンテナシェルから追加インストールしやすいように明示
ENV PIP_DISABLE_PIP_VERSION_CHECK=1