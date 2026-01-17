FROM python:3.11-slim

# 作業ディレクトリ
WORKDIR /app

# Pythonライブラリをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリ本体
COPY app.py .

# HTMLテンプレート
COPY templates ./templates

# アプリ起動
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
