# ベースイメージの指定
FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

# 作業ディレクトリを設定
WORKDIR /app

# requirements.lockファイルをコンテナにコピー
COPY requirements.lock .

# 必要なパッケージをインストール
RUN pip install -r requirements.lock && rm requirements.lock

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]
