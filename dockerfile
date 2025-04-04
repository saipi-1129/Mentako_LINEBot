# Pythonの公式イメージを使う
FROM python:3.9-slim

# 作業ディレクトリを作成
WORKDIR /app

# 必要なパッケージをインストールするためのrequirements.txtをコピー
COPY requirements.txt /app/

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# 残りのコードをコンテナにコピー
COPY . /app/

# main.pyを実行する
CMD ["python", "src/main.py"]
