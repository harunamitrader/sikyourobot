# 市況ロボット (Sikyou Robot)

このリポジトリは、金融市場の情報を自動的に収集し、Discordに投稿するためのPythonスクリプト群です。

## スクリプト一覧

### 1. `originalcalendar.py`

#### 機能
このスクリプトは、マネックス証券のウェブサイトから以下の情報をスクレイピングし、1枚の画像にまとめてDiscordに投稿します。
- 経済指標カレンダー
- 米国株の決算発表スケジュール
- 日本株の決算発表スケジュール

生成される画像 (`originalcalendar.png`) には、当日から翌日にかけての主要な予定が時系列で記載されます。


### 2. `pyscreenshot_discord.py`

#### 機能
このスクリプトは、以下の市場サマリーのスクリーンショットを取得し、それぞれDiscordに投稿します。

1.  **Fear & Greed Index (CNN)**
    - CNN MoneyのFear & Greed指数のページからスクリーンショットを取得し、インジケーター部分を切り抜いて投稿します。

2.  **S&P 500セクターヒートマップ (Finviz)**
    - FinvizのS&P 500セクターヒートマップのスクリーンショットを取得し、投稿します。

3.  **ETFヒートマップ (Finviz)**
    - FinvizのETFヒートマップのスクリーンショットを取得し、投稿します。

取得した各画像には、タイムスタンプが付与されます。

## 依存ライブラリ
- `selenium`
- `pandas` (originalcalendar.pyのみ)
- `requests`
- `Pillow`

## セットアップと設定

### 前提条件
- Python 3.x
- Google Chrome
- [ChromeDriver](https://chromedriver.chromium.org/downloads)

### インストール
必要なライブラリをインストールします。
```bash
pip install selenium pandas requests pillow
```

### 設定
各スクリプト内の以下の項目を、ご自身の環境に合わせて変更する必要があります。

- **ファイル保存パス**: 画像を保存するパス (`imagefilepath`など) を、任意のディレクトリに変更してください。
- **Discord Webhook URL**: `WEBHOOK_URL` に、投稿したいDiscordチャンネルのWebhook URLを設定してください。
- **フォントパス**: `ImageFont.truetype()` で指定されているフォントのパスを、ご自身の環境に合わせて変更してください。(存在しない場合、エラーになります)

## 使い方
各スクリプトを直接実行します。
```bash
# 経済・決算カレンダーを生成して投稿
python originalcalendar.py

# 各種市場サマリーのスクリーンショットを取得して投稿
python pyscreenshot_discord.py
```

### 3. `pyheatmap_day_nasdaq100.py`

#### 機能
このスクリプトは、`nasdaq100list.txt` に記載されたNASDAQ 100の構成銘柄の株価データを取得し、各銘柄の前日比騰落率と指数への寄与度を可視化したヒートマップ画像 (`heatmap_day_nasdaq100.png`) を生成します。

生成されたヒートマップは、セクターごとにグループ化されており、指数全体、および寄与度の高かった上位・下位銘柄の情報も表示されます。最終的に、この画像は指定されたDiscordのWebhookに投稿されます。

#### 関連ファイル
- `nasdaq100list.txt`
  - ヒートマップを生成するための、NASDAQ 100構成銘柄のティッカーシンボルが記載されたテキストファイルです。