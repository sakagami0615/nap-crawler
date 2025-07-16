# nap-crawler

Nap Crawlerは、[nap-camp.com](https://www.nap-camp.com)から全キャンプ場情報を収集するためのウェブクローラーです。

## インストール

virtualenvやpoetryなどを使用し、Pythonの仮想環境を作成することを推奨します。  
仮想環境にアクティベートした状態で下記コマンドを実行してインストールしてください。

```bash
pip install git+https://github.com/sakagami0615/nap-crawler.git
```

また、Nap Crawlerではplaywrightを使用します。  
下記コマンドを実行し、playwrightで使用するブラウザをインストールしてください。

```bash
playwright install
```

## 使用方法

`napcrawler`コマンドを実行してクローリングを開始します。

### 実行コマンド

以下のコマンドでクローリングを開始します。

```bash
napcrawler [output_folder_path] -r [region] -t [output_type] -w [wait_time] --headless [headless] --log_level [log_level]
```

### コマンドライン引数

default 列の記載があるコマンドラインは省略可能です。  
省略した場合は default に記載した値となります。

| name | option | doc | datatype | default |
| --- | :-: | --- | --- | --- |
| output_folder_path | - | クローリングしたデータの保存先 | str | - |
| region | -r | クローリングするキャンプ場の地域 | str | None (何も指定しなければ全てクロールする) |
| output_type | -t | クリーリングデータの出力形式 | str (HTML, Text) | HTML |
| wait_time | -w | ページへのリクエスト時の待ち時間(秒) | int (positive) | 1 |
| headless | --headless | ブラウザのヘッドレスモード | bool | False |
| log_level | --log_level | ログレベル | str (DEBUG, INFO, WARNING, ERROR, CRITICAL) | WARNING |

#### [regionの設定値について]

region ではクローリングするキャンプ場の [地域], [都道府県], [市(エリア)] の設定が可能です。  
なお、設定は [,] 区切りで複数指定することが可能です。

```bash
# [地域], [都道府県], [市(エリア)] によらず、複数指定することが可能
# 下記の場合、
#     [地域]: hokkaido_tohoku
#     [都道府県]: okinawa
#     [市(エリア)]: hokkaido/sapporo
# を指定している。 
napcrawler -r hokkaido_tohoku,okinawa,hokkaido/sapporo
```

- **地域の設定値に関して**  

   下記の地域を引数指定することが可能です。

   | 地域名 | 引数に指定する値 |
   | --- | --- |
   | 北海道・東北 | hokkaido_tohoku |
   | 関東 | kanto |
   | 北陸・甲信越 | hokushinetsu |
   | 東海 | tokai |
   | 関西 | kansai |
   | 中国・四国 | chugoku_shikoku |
   | 九州・沖縄 | kyushu_okinawa |

- **都道府県の設定値に関して**  

   下記の度道府県を引数指定することが可能です。

   | 地域名 | 引数に指定する値 |
   | --- | --- |
   | 北海道・東北 | hokkaido, aomori, iwate, miyagi, akita, yamagata, fukushima |
   | 関東 | tokyo, kanagawa, saitama, chiba, ibaraki, tochigi, gunma |
   | 北陸・甲信越 | yamanashi,  nagano,  niigata,  toyama,  ishikawa,  fukui  |
   | 東海 | gifu, shizuoka, aichi, mie |
   | 関西 | osaka, hyogo, kyoto, shiga, nara, wakayama |
   | 中国・四国 | okayama, hiroshima, tottori, shimane, yamaguchi, kagawa, tokushima, ehime, kochi |
   | 九州・沖縄 | fukuoka, saga, nagasaki, kumamoto, oita, miyazaki, kagoshima, okinawa |

- **市(エリア)の設定値に関して**  
   [都道府県]の文字 + / + [市(エリア)]の文字を引数指定することが可能です。  
   下記図の赤枠は `北海道` の[市(エリア)]となります。

   ![check_area](./img/check_area.drawio.svg)

   この枠内の項目を一つ選択し、「エリアを絞り込む」を押すと以下のURLにジャンプするので、この文字を引数指定するような流れになります。

   ```text
   https://www.nap-camp.com/[都道府県]/[市(エリア)]/list?sortId=21
   ```

   > (ex) 札幌を引数指定する場合は以下のようになります
   > 
   > ```bash
   > napcrawler -r hokkaido/sapporo
   > ```

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

3. playwrightで使用するブラウザをインストールする

   ```bash
   poetry run playwright install
   ```

環境構築後、以下のコマンドで「napcrawler/app.py」を実行できます。

```bash
# poetry で [make run] を実行
poetry run make run
```

> 上記のコマンドでは make コマンドを使用しています。  
> windows環境の場合は事前に make コマンドを使用できるようにしておく必要があります。  
> (ex) chocolatey でインストールする場合
> 
> ```powershell
> choco install make
> ```

> [補足]  
> `make run` コマンド実行時、環境変数を設定してコマンドライン引数を変更することが可能です。  
> 設定方法に関しては、下記コマンドを実行することで表示することができます。
> 
> ```bash
> poetry run make help
> ```

## ライセンス

MIT License
