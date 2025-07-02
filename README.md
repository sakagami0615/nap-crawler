# nap-crawler

Nap Crawlerは、[nap-camp.com](https://www.nap-camp.com)から全キャンプ場情報を収集するためのウェブクローラーです。

## インストール

このプロジェクトはPoetryを使用して管理されています。以下の手順でインストールしてください。

```bash
pip install git+https://github.com/sakagami0615/nap-crawler/nap-crawler.git
```

## 使用方法

`napcrawler`コマンドを実行してクローリングを開始します。

### 実行コマンド

以下のコマンドでクローリングを開始します。

```bash
napcrawler [output_folder_path] -t [output_type] -w [wait_time] --headless [headless] --log_level [log_level]
```

### コマンドライン引数

default 列の記載があるコマンドラインは省略可能です。  
省略した場合は default に記載した値となります。

| name | option | doc | datatype |default |
| --- | :-: | --- | --- | --- |
| output_folder_path | - | クローリングしたデータの保存先 | str | - |
| output_type | -t | クリーリングデータの出力形式(HTML or Text) | str | HTML |
| wait_time | -w | ページへのリクエスト時の待ち時間(秒) | int (positive) | 1 |
| headless | --headless | ブラウザのヘッドレスモード | bool | False |
| log_level | --log_level | ログレベル | str | WARNING |

## 開発者向けの環境準備

本リポジトリをカスタマイズする場合は、下記の手順で環境を用意してください。

1. リポジトリをクローン

   ```bash
   git clone https://github.com/sakagami0615/nap-crawler/nap-crawler.git
   ```

2. poetryで必要な依存関係をインストール

   ```bash
   poetry update
   ```

環境構築後、以下のコマンドで「napcrawler/app.py」を実行できます。

```bash
# windowsの場合
make windows

# macの場合
make mac
```

> 上記のコマンドでは make コマンドを使用しています。  
> windows環境の場合は事前に make コマンドを使用できるようにしておく必要があります。  
> (ex) chocolatey でインストールする場合
> 
> ```powershell
> choco install make
> ```

また、下記コマンドでも「napcrawler/app.py」を実行することができます。  
※ $()の変数は各自用意してください

```bash
# windowsの場合
powershell -Command "$$env:PYTHONPATH = './'; poetry run python ./napcrawler/app.py $(OUTPUT_PATH) -t $(OUTPUT_TYPE) -w $(WAIT_TIME_SEC) --headless $(HEADLESS) --log_level $(LOG_LEVEL)"

# macの場合
PYTHONPATH="./" poetry run python ./napcrawler/app.py $(OUTPUT_PATH) -t $(OUTPUT_TYPE) -w $(WAIT_TIME_SEC) --headless $(HEADLESS) --log_level $(LOG_LEVEL)
```

## ライセンス

MIT License
