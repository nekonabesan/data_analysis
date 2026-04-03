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

# Python パッケージ定義をコピーして一括インストール
COPY requestment.txt /tmp/requestment.txt

RUN pip install --no-cache-dir -r /tmp/requestment.txt

# コンテナシェルから追加インストールしやすいように明示
ENV PIP_DISABLE_PIP_VERSION_CHECK=1