# nap-crawler

Nap Crawlerは、[nap-camp.com](https://www.nap-camp.com)から全キャンプ場情報を収集するためのウェブクローラーです。

## インストール

このプロジェクトはPoetryを使用して管理されています。以下の手順でインストールしてください。

```bash
pip install git+https://github.com/sakagami0615/nap-crawler/nap-crawler.git
```

## 使用方法

環境変数を設定し、`napcrawler`コマンドを実行してクローリングを開始します。

### 環境変数

環境変数は「dotenv」を使用して設定しています。そのため、各自で「.env」ファイルを準備してください。設定が必要な環境変数は下記の通りです。

- `NAP_CRAWLER_OUTPUT_CRAWL_FOLDER_PATH`: クローリング結果を保存するフォルダのパス（デフォルト: `.crawl_data`）
- `NAP_CRAWLER_SLEEP_TIME_SEC`: 各リクエスト間の待機時間（デフォルト: `1`秒）
- `NAP_CRAWLER_HEADLESS`: ヘッドレスモードでブラウザを起動するか（デフォルト: `False`）

### 実行

以下のコマンドでクローリングを開始します。

```bash
napcrawler
```

## 開発者向けの環境準備

本リポジトリをカスタマイズする場合は、下記の手順で環境を用意してください。

1. リポジトリをクローン

   ```bash
   git clone https://github.com/sakagami0615/nap-crawler/nap-crawler.git
   ```

2. poetryで必要な依存関係をインストール

   ```bash
   poetry update --with dev
   ```

環境構築後、以下のコマンドで「napcrawler/app.py」を実行できます。

```bash
# windowsの場合
make windows

# macの場合
make mac
```

> 下記コマンドでも実行可能です。
>
> ```bash
> # windowsの場合
> powershell -Command "$$env:PYTHONPATH = './'; poetry run python ./napcrawler/app.py"
> 
> # macの場合
> PYTHONPATH="./" poetry run python ./napcrawler/app.py
> ```

## ライセンス

MIT License
