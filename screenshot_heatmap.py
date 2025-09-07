from selenium import webdriver
from selenium.webdriver.common.by import By
import time

import datetime
import json
import requests
from PIL import Image, ImageDraw, ImageFont
driver = webdriver.Chrome()
driver.set_window_size(1080,1080)
# Chromeドライバのオプション設定
chrome_options = webdriver.ChromeOptions()
chrome_options.headless = True 
#ファイルパス
imagefilepath = r"C:\Users\harunami\Desktop\python_study\screenshot_heatmap.png"
imagefilepath2 = r"C:\Users\harunami\Desktop\python_study\screenshot_heatmap2.png"
# 画面サイズの取得
page_rect = driver.execute_cdp_cmd("Page.getLayoutMetrics", {})

driver.get("https://finviz.com/map.ashx?t=sec")
# スクリーンショット1を保存
time.sleep(1)
driver.save_screenshot(imagefilepath)
#画像編集
im = Image.open(imagefilepath)

#書き込み
draw = ImageDraw.Draw(im)
dt_now = datetime.datetime.now()
today = dt_now.strftime('%Y/%m/%d %H:%M')
textt1=today + "   from finviz  @hana_bot"
color_black = (0,0,0)
color_white = (255,255,255)
font1 = ImageFont.truetype(r"C:\Windows\fonts\arialbd.ttf", 16)
draw.multiline_text((210, 640), textt1, fill=color_white, font=font1 ,anchor='rd' ,align='center')

#切り抜き
im_crop = im.crop((200, 165, 1040, 650))
im_crop.save(imagefilepath)


driver.get("https://finviz.com/map.ashx?t=etf")
# スクリーンショットを保存
time.sleep(1)
driver.save_screenshot(imagefilepath2)

#画像編集
im = Image.open(imagefilepath2)

#書き込み
draw = ImageDraw.Draw(im)
dt_now = datetime.datetime.now()
today = dt_now.strftime('%Y/%m/%d %H:%M')
textt1=today + "   from finviz  @hana_bot"
color_black = (0,0,0)
color_white = (255,255,255)
font1 = ImageFont.truetype(r"C:\Windows\fonts\arialbd.ttf", 16)
draw.multiline_text((210, 640), textt1, fill=color_white, font=font1 ,anchor='rd' ,align='center')

#切り抜き
im_crop = im.crop((200, 165, 1040, 650))
im_crop.save(imagefilepath2)

#WEBHOOK
#screenshotサーバー
WEBHOOK_URL = "https://discord.com/api/webhooks/1329382483116036116/y8crWZgmNtmA_zQeDxksVtftSOIwlrFXdOF_umd5wo8mHxRCZ9hXwIReq8FcVtXmV1sl"
#haru bot サーバー
#WEBHOOK_URL = "https://discordapp.com/api/webhooks/1311201721774641152/azWkyQ8Kpf2TfLnLH_2uqeFOmTppKJjZwPQxn_WINKFmfkRMGsHsoEGq2qVgHFYC8ASM?wait=true"

### テキスト
payload = {
	"content"		: "heatmap screenshot 配信テスト",
}
### 複数画像
filepath = r"C:\Users\harunami\Desktop\python_study\screenshot_heatmap.png"
filepath2 = r"C:\Users\harunami\Desktop\python_study\screenshot_heatmap2.png"

file_list = [imagefilepath, imagefilepath2]

multiple_files = []
for i, image_file in enumerate(file_list):
    multiple_files.append((
        f"files[{i}]", (f"image{i+1}.png", open(image_file, "rb"), "image/png")
    ))
#送信
res = requests.post( WEBHOOK_URL, data={"payload_json": json.dumps(payload)} ,files = multiple_files )
print("finish")