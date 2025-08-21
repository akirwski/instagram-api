# ベースイメージ
FROM python:3.12-slim

# 作業ディレクトリ
WORKDIR /app

# 依存関係をコピーしてインストール
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリコードをコピー
COPY app/ .

# ポート開放
EXPOSE 8000

# FastAPI 起動
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
