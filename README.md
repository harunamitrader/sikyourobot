# 市況ロボット (Sikyou Robot)

このリポジトリは、金融市場の情報を自動的に収集し、共有するためのPythonスクリプト群です。

## スクリプト一覧

### 1. `originalcalendar.py`

#### 機能
このスクリプトは、マネックス証券のウェブサイトから以下の情報をスクレイピングし、1枚の画像にまとめてDiscordに投稿します。
- 経済指標カレンダー
- 米国株の決算発表スケジュール
- 日本株の決算発表スケジュール

生成される画像 (`originalcalendar.png`) には、当日から翌日にかけての主要な予定が時系列で記載されます。

#### 依存ライブラリ
- `selenium`
- `pandas`
- `requests`
- `Pillow`

---

### 2. `screenshot_heatmap.py`

#### 機能
このスクリプトは、Finvizのウェブサイトから以下の2種類のヒートマップのスクリーンショットを取得し、Discordに投稿します。
- S&P 500 セクターヒートマップ
- ETFヒートマップ

取得したスクリーンショットは、ヒートマップ部分のみが切り抜かれ、タイムスタンプが追加されます。

#### 依存ライブラリ
- `selenium`
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

- **ChromeDriverのパス**: `webdriver.Chrome()` の引数に、ダウンロードしたChromeDriverのパスを指定してください。
- **ファイル保存パス**: 画像を保存するパス (`imagefilepath`など) を変更してください。
- **フォントパス**: `ImageFont.truetype()` で指定されているフォントのパスを、ご自身の環境に合わせて変更してください。
- **Discord Webhook URL**: `WEBHOOK_URL` に、投稿したいDiscordチャンネルのWebhook URLを設定してください。

## 使い方
各スクリプトを直接実行します。
```bash
# 経済・決算カレンダーを生成して投稿
python originalcalendar.py

# ヒートマップのスクリーンショットを取得して投稿
python screenshot_heatmap.py
```
