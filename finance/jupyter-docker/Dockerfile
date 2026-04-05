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

# Python パッケージ定義をコピーして一括インストール
COPY requestment.txt /tmp/requestment.txt

RUN pip install --no-cache-dir -r /tmp/requestment.txt

# Prophet は安定して動作した /tmp 配下の分離仮想環境へ導入する
RUN python -m venv /tmp/prophet-venv && \
	. /tmp/prophet-venv/bin/activate && \
	pip install --no-cache-dir --upgrade pip && \
	pip install --no-cache-dir "numpy<2" pandas matplotlib plotly python-dotenv prophet==1.1.5 ipykernel && \
	PROPHET_STAN_DIR=$(python -c "from pathlib import Path; import prophet; print(Path(prophet.__file__).resolve().parent / \"stan_model\")") && \
	python -m cmdstanpy.install_cmdstan --version 2.33.1 --dir "$PROPHET_STAN_DIR" --overwrite && \
	python -m ipykernel install --user --name python3 --display-name "Python 3 (Prophet)" && \
	INSTALL_PY=/tmp/prophet-venv/lib/python3.10/site-packages/cmdstanpy/install_cmdstan.py && \
	sed -i 's/^    import readline/    pass  # import readline disabled (segfault workaround)/' "$INSTALL_PY" && \
	sed -i 's/^    _ = readline\.__doc__/    pass  # readline disabled/' "$INSTALL_PY"

# コンテナシェルから追加インストールしやすいように明示
ENV PIP_DISABLE_PIP_VERSION_CHECK=1