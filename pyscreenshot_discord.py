from selenium import webdriver
from selenium.webdriver.common.by import By
import time

import datetime
import json
import requests
import time
from PIL import Image, ImageDraw, ImageFont


driver = webdriver.Chrome()
driver.set_window_size(1080,1080)
# Chromeドライバのオプション設定
chrome_options = webdriver.ChromeOptions()
chrome_options.headless = True 

#WEBHOOK
#hana塾サーバー
WEBHOOK_URL = "[WEBHOOKのURL]?wait=true"
#テスト サーバー
#WEBHOOK_URL = "https://discordapp.com/api/webhooks/1303499824108273745/jpQdcsHz0UtnPbyhOcYYuIXDrPbdL9E_ggvgCL2WDKEaJkG6PDJjSqFdoAjsvF7hn5eW?wait=true"

#ファイルパス
imagefilepath1 = r"[任意のディレクトリ]\screenshot_fg.png"
imagefilepath2 = r"[任意のディレクトリ]\screenshot_heatmap.png"
imagefilepath3 = r"[任意のディレクトリ]\screenshot_heatmap2.png"

#共通設定
color_black = (0,0,0)
color_dimgray = (105,105,105)
color_red = (255,0,0)
color_white = (255,255,255)
font1 = ImageFont.truetype(r"C:\Windows\fonts\arialbd.ttf", 16)
dt_now = datetime.datetime.now()
today = dt_now.strftime('%Y/%m/%d %H:%M')

#fear and greed------------------------------------------------------
driver.get("https://edition.cnn.com/markets/fear-and-greed")
driver.execute_script('window.scrollBy(0, 250);')
# スクリーンショットを保存
time.sleep(1)
driver.save_screenshot(imagefilepath1)
#画像編集
im1 = Image.open(imagefilepath1)

#書き込み
draw1 = ImageDraw.Draw(im1)
text1=today + "   from cnn  @hana_bot"
draw1.multiline_text((690, 910), text1, fill=color_dimgray, font=font1 ,anchor='rd' ,align='center')

#切り抜き
im1_crop = im1.crop((0, 240, 700, 920))
im1_crop.save(imagefilepath1)

#投稿-----------------------------------
### テキスト
payload = {
	"content"		: "Fear&Greed screenshot",
}

### 画像添付

with open(imagefilepath1, 'rb') as f:
	file_bin = f.read()
files_qiita = {
	"favicon" : ( imagefilepath1, file_bin),
}
#送信
res = requests.post( WEBHOOK_URL, data={"payload_json": json.dumps(payload)} ,files = files_qiita )

print("finish")

#heat map1------------------------------------------------------
driver.get("https://finviz.com/map.ashx?t=sec")
# スクリーンショットを保存
time.sleep(1)
driver.save_screenshot(imagefilepath2)
#画像編集
im2 = Image.open(imagefilepath2)

#書き込み
draw2 = ImageDraw.Draw(im2)
text2=today + "   from finviz  @hana_bot"
draw2.multiline_text((1030, 640), text2, fill=color_white, font=font1 ,anchor='rd' ,align='center')

#切り抜き
im2_crop = im2.crop((200, 165, 1040, 650))
im2_crop.save(imagefilepath2)

#heat map2------------------------------------------------------
driver.get("https://finviz.com/map.ashx?t=etf")
# スクリーンショットを保存
time.sleep(1)
driver.save_screenshot(imagefilepath3)
#画像編集
im3 = Image.open(imagefilepath3)

#書き込み
draw3 = ImageDraw.Draw(im3)
text3=today + "   from finviz  @hana_bot"
draw3.multiline_text((1030, 640), text3, fill=color_white, font=font1 ,anchor='rd' ,align='center')

#切り抜き
im3_crop = im3.crop((200, 165, 1040, 650))
im3_crop.save(imagefilepath3)

### テキスト
payload = {
	"content"		: "S&P500・ETF heatmap screenshot",
}
### 複数画像

file_list = [imagefilepath2, imagefilepath3]

multiple_files = []
for i, image_file in enumerate(file_list):
    multiple_files.append((
        f"files[{i}]", (f"image{i+1}.png", open(image_file, "rb"), "image/png")
    ))
#送信
res = requests.post( WEBHOOK_URL, data={"payload_json": json.dumps(payload)} ,files = multiple_files )
print("hm finish")