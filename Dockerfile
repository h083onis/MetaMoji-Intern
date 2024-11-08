# ベースイメージの指定
FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

# 作業ディレクトリを設定
WORKDIR /app

# requirements.lockファイルをコンテナにコピー
COPY requirements.lock .

# 必要なパッケージをインストール
RUN pip install -r requirements.lock && rm requirements.lock

# 必要なポートを公開（例としてポート8000を指定）
EXPOSE 8000
