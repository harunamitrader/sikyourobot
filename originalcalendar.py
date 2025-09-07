from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import datetime
from datetime import datetime as dt
import json
import requests
from PIL import Image, ImageDraw, ImageFont
import re

#ファイルアドレス
imagefilepath = r"C:\Users\harunami\Desktop\python_study\originalcalendar.png"

#設定-----------------------------------------------------
driver = webdriver.Chrome()
driver.set_window_size(800,1080)
# Chromeドライバのオプション設定
chrome_options = webdriver.ChromeOptions()
chrome_options.headless = True 

#色の指定
color_white = (255,255,255)
color_black = (0,0,0)
color_lightgray = (211,211,211)
color_dimgray = (105,105,105)
color_darkgray = (50,50,50)
color_lightpink = (255,240,255)
color_lightcyan = (230,255,255)
color_blue = (10,100,190)
color_red = (180,0,0)
color_green = (0,130,0)
#線の太さ
linewidth1 = 2
linewidth2 = 4
linewidth3 = 7
linewidth4 = 8
#フォント
font1 = ImageFont.truetype(r"C:\Windows\fonts\HGRGE.TTC", 25)
font2 = ImageFont.truetype(r"C:\Windows\fonts\HGRGE.TTC", 30)
font3 = ImageFont.truetype(r"C:\Windows\fonts\HGRGE.TTC", 40)
#列の数
row = 10
#白紙画像の作成
im = Image.new("RGB", (1100, 3000), color_white)
draw = ImageDraw.Draw(im)
#日付
today = datetime.date.today()
strtoday =today.strftime('%Y/%m/%d')
dt_now = datetime.datetime.now()
strdt_now = dt_now.strftime('%Y/%m/%d %H:%M')
strdt_now2 =dt_now.strftime('%m/%d --:--')
list1 = []

#指標カレンダー----------------------------
driver.get("https://mst.monex.co.jp/pc/servlet/ITS/report/EconomyIndexCalendar")
list1.append(["経済指標　予定","",""])
#クリック
click1 = driver.find_element(by=By.XPATH, value="/html/body/div[7]/div/div[3]/div[1]/form/table/tbody/tr[1]/td/ul/li[1]/label/input")
click1.click()
time.sleep(1)

click1 = driver.find_element(by=By.XPATH, value="/html/body/div[7]/div/div[3]/div[1]/form/table/tbody/tr[2]/td/ul/li[3]/label/input")
click1.click()
time.sleep(1)

click1 = driver.find_element(by=By.XPATH, value="/html/body/div[7]/div/div[3]/div[1]/div[3]/a")
click1.click()
time.sleep(1)


table = driver.find_element(by=By.XPATH, value="/html/body/div[7]/div/div[3]/div[1]/div[4]/table")

html = table.get_attribute('outerHTML')
df0 = pd.read_html(html)
df = df0[0]

try :
    for i in range(len(df)):
        if len(df.iloc[i,1]) < 5 :
            df.iloc[i,1]="00:00"  
        text0 = str(dt_now.year)+"/"+df.iloc[i,0][:5]+" "+df.iloc[i,1][:5]
        tdatetime = dt.strptime(text0, '%Y/%m/%d %H:%M')
        text1 = tdatetime.strftime('%m/%d %H:%M')
        list =[text1 ,df.iloc[i,2],df.iloc[i,4][:22]]
        if tdatetime > dt_now + datetime.timedelta(hours=-2) and tdatetime < dt_now + datetime.timedelta(hours=+26):        
            list1.append(list)
except : 
    print("except1")

click1 = driver.find_element(by=By.XPATH, value="/html/body/div[7]/div/div[3]/div[1]/div[4]/div[1]/span[3]")
click1.click()
time.sleep(1)
table = driver.find_element(by=By.XPATH, value="/html/body/div[7]/div/div[3]/div[1]/div[4]/table")

html = table.get_attribute('outerHTML')
df0 = pd.read_html(html)
df = df0[0]
try :
    for i in range(len(df)):
        if len(df.iloc[i,1]) < 5 :
            df.iloc[i,1]="00:00"  
        text0 = str(dt_now.year)+"/"+df.iloc[i,0][:5]+" "+df.iloc[i,1][:5]
        tdatetime = dt.strptime(text0, '%Y/%m/%d %H:%M')
        text1 = tdatetime.strftime('%m/%d %H:%M')
        list =[text1 ,df.iloc[i,2],df.iloc[i,4][:22]]
        if tdatetime > dt_now + datetime.timedelta(hours=-2) and tdatetime < dt_now + datetime.timedelta(hours=+26):        
            list1.append(list)
except : 
    print("except2")


#米国株決算カレンダー----------------------------
driver.get("https://mst.monex.co.jp/mst/servlet/ITS/fi/FIClosingCalendarUSGuest")
list1.append(["米国株 決算予定","",""])
#クリック

click1 = driver.find_element(by=By.XPATH, value="/html/body/div[7]/div/div[3]/div[1]/form/div[6]/div/div/div[1]/a[3]")
click1.click()
time.sleep(1)

table = driver.find_element(by=By.XPATH, value="/html/body/div[7]/div/div[3]/div[1]/form/div[6]/table")

html = table.get_attribute('outerHTML')
df0 = pd.read_html(html)
df = df0[0]

UStickerlist = ["AAPL" , "NVDA" , "MSFT" , "GOOG" , "META" , "AMZN" , "NFLX" , "BRK-B" , "TSLA" , "AVGO" , "LLY" , "WMT" , "JPM" , "V" , "UNH" , "XOM" , "ORCL" , "MA" , "HD" , "PG" , "COST" , "JNJ" , "ABBV" , "TMUS" , "BAC" , "CRM" , "KO" , "CVX" , "VZ" , "MRK" , "AMD" , "PEP" , "CSCO" , "LIN" , "ACN" , "WFC" , "TMO" , "ADBE" , "MCD" , "ABT" , "BX" , "PM" , "NOW" , "IBM" , "AXP" , "MS" , "TXN" , "GE" , "QCOM" , "CAT" , "ISRG" , "DHR" , "INTU" , "DIS" , "CMCSA" , "AMGN" , "T" , "GS" , "PFE" , "NEE" , "CHTR" , "RTX" , "BKNG" , "UBER" , "AMAT" , "SPGI" , "LOW" , "BLK" , "PGR" , "UNP" , "SYK" , "HON" , "ETN" , "SCHW" , "LMT" , "TJX" , "COP" , "ANET" , "BSX" , "KKR" , "VRTX" , "C" , "PANW" , "ADP" , "NKE" , "BA" , "MDT" , "FI" , "UPS" , "SBUX" , "ADI" , "CB" , "GILD" , "MU" , "BMY" , "DE" , "PLD" , "MMC" , "INTC" , "AMT" , "SO" , "LRCX" , "ELV" , "DELL" , "PLTR" , "REGN" , "MDLZ" , "MO" , "HCA" , "SHW" , "KLAC" , "ICE" , "CI" , "ABNB"]
for i in range(len(df)):
    if df.iloc[i ,2] in UStickerlist :
        text0 = df.iloc[i,0]+" "+df.iloc[i,1][:5]
        tdatetime = dt.strptime(text0, '%Y/%m/%d %H:%M')+ datetime.timedelta(hours=13)
        text1 = tdatetime.strftime('%m/%d %H:%M')
        list =[text1 ,df.iloc[i,2] ,"("+df.iloc[i,3][:20]+")"]
        if tdatetime > dt_now + datetime.timedelta(hours=-2) :        
            list1.append(list)
if strtoday =="2025/04/16" :
    list=[strdt_now2 ,"ASML" ,"(エーエスエムエル・ホールディングス)"]
if strtoday =="2025/05/07" :
    list=[strdt_now2 ,"ARM" ,"(アーム・ホールディングス)"]
if strtoday =="2025/03/12" :
    list=[strdt_now2 ,"PDD" ,"(ピンドゥオドゥオ)"]
if strtoday =="2025/04/17" :
    list=[strdt_now2 ,"TSMC" ,"(台湾・セミコンダクター)"]
if strtoday =="2025/03/25" :
    list=[strdt_now2 ,"AZN" ,"(アストラゼネカ)"]
if strtoday =="2025/02/20" :
    list=[strdt_now2 ,"MELI" ,"(メルカドリブレ)"]
"ASML" , "ARM" , "PDD" ,"TSMC", "AZN" , "MELI"
#日本株決算カレンダー----------------------------
driver.get("https://mst.monex.co.jp/mst/servlet/ITS/fi/FIClosingCalendarJPGuest")
list1.append(["日本株 決算予定","",""])
#クリック
#1回目
click1 = driver.find_element(by=By.XPATH, value="/html/body/div[7]/div/div[3]/div[1]/form/div[8]/div/div/div[1]/a[3]")
click1.click()
time.sleep(1)

table = driver.find_element(by=By.XPATH, value="/html/body/div[7]/div/div[3]/div[1]/form/div[8]/table")

html = table.get_attribute('outerHTML')
df0 = pd.read_html(html)
df = df0[0]

JPtickerlist = ["7203" , "8306" , "6501" , "6861" , "6758" , "9983" , "6098" , "9984" , "8316" , "9432" , "4519" , "4063" , "8058" , "8001" , "8766" , "8035" , "9433" , "8031" , "7974" , "4568" , "9434" , "8411" , "2914" , "7267" , "7741" , "7011" , "4502" , "6857" , "6902" , "4661" , "6503" , "3382" , "6367" , "8725" , "4578" , "6702" , "6981" , "6146" , "7751" , "6178" , "4543" , "4901" , "6273" , "8053" , "8002" , "6954" , "5108" , "8591" , "6301" , "8801" , "6723" , "8750" , "6762" , "6594" , "9020" , "6701" , "9613" , "4503" , "8267" , "8630" , "6752" , "6201" , "9022" , "7733" , "4452" , "4689" , "2802" , "5401" , "1925" , "7269" , "8802" , "8113" , "2502" , "8015" , "4612" , "4307" , "1605" , "8309" , "8308" , "1928" , "8604" , "9101" , "6326" , "4684" , "7532" , "9735" , "8830" , "9503" , "5020" , "3659" , "9843" , "6971" , "7832" , "4091" , "7309" , "4755" , "9104" , "4716" , "7936" , "9766" , "4507" , "8697" , "5802" , "2503" , "7270" , "6920" , "6869" , "6988" , "2801" , "2587" , "3407" , "5803" , "7201" , "8593" , "9531" , "4523" , "9107" , "7202" , "3092" , "8601" , "5019" , "9202" , "9435" , "1802" , "4768" , "7911" , "4151" , "9502" , "6586" , "7701" , "3402" , "7272" , "9532" , "9697" , "4911" , "9021" , "8795" , "3064" , "7259" , "1812" , "2897" , "7912" , "4324" , "6504" , "7013" , "7550" , "6645" , "5713" , "5411" , "4188"]
for i in range(len(df)):
    text2 = df.iloc[i,2][-6:]
    text3 = re.sub(r'\D', '', text2)
    if text3 in JPtickerlist :
        text1 = df.iloc[i,0]+" "+df.iloc[i,1][:5]
        text4 = df.iloc[i,2][:-8]
        list =[text1 ,text3 ,"("+text4[:20]+")"]
        if tdatetime > dt_now + datetime.timedelta(hours=-2) :        
            list1.append(list)

try :
    for i in range(7):
        cur_url = driver.current_url
        click2 = driver.find_element(By.CLASS_NAME, "next")
        click2.click()
        time.sleep(1)
        if cur_url == driver.current_url :
            break
        table = driver.find_element(by=By.XPATH, value="/html/body/div[7]/div/div[3]/div[1]/form/div[8]/table")

        html = table.get_attribute('outerHTML')
        df0 = pd.read_html(html)
        df = df0[0]

        for i in range(len(df)):
            text2 = df.iloc[i,2][-6:]
            text3 = re.sub(r'\D', '', text2)
            if text3 in JPtickerlist :
                text1 = df.iloc[i,0]+" "+df.iloc[i,1][:5]
                text4 = df.iloc[i,2][:-8]
                list =[text1 ,text3 ,"("+text4[:20]+")"]
                if tdatetime > dt_now + datetime.timedelta(hours=-2) :        
                    list1.append(list)
except :
    print("exceptj")

l= len(list1)
#外枠
P= [100, 100, 1000 ,100+l*50]
draw.line(((P[0]+200,P[1]-15), (P[2]-200,P[1]-15)),fill=color_darkgray, width=linewidth2)
draw.text((550, 80), strtoday+ "  本日の予定", fill=color_darkgray, font=font3 ,anchor='md' ,align='center')
for i in range(l) :
    list2=list1[i]
    P= [100, 100+i*50, 1000 ,100+i*50]
    if list2 ==["経済指標　予定","",""] or list2 ==["米国株 決算予定","",""] or list2 ==["日本株 決算予定","",""] :
        if list2 ==["経済指標　予定","",""] :
            color1 =color_green
        elif list2 ==["米国株 決算予定","",""] :
            color1 =color_blue
        elif list2 ==["日本株 決算予定","",""] :
            color1 =color_red
        draw.rectangle(((P[0],P[1]), (P[2],P[3]+50)), fill=color1, outline=color_white ,width=linewidth1)
        draw.text((P[0]+20, P[1]+25), list2[0], fill=color_white, font=font2 ,anchor='lm' ,align='center')
    else : 
        if i % 2 == 0:
            color1 =color_lightcyan
        else :
            color1 = color_lightpink
        draw.rectangle(((P[0],P[1]), (P[2],P[3]+50)), fill=color1 ,width=linewidth1)

        if (not i==0) and list1[i][0][:5] ==list1[i-1][0][:5] :
            draw.text((P[0]+20, P[1]+25), "     "+list2[0][5:], fill=color_black, font=font2 ,anchor='lm' ,align='center')
        else :
            draw.text((P[0]+20, P[1]+25),list2[0], fill=color_black, font=font2 ,anchor='lm' ,align='center')
        if list2[1] =="★★" or list2[1] =="★★★" :
            fontx= font1
        else :
            fontx=font2
        draw.text((P[0]+250, P[1]+25), list2[1], fill=color_black, font=fontx ,anchor='lm' ,align='center')
        draw.text((P[0]+350, P[1]+25), list2[2], fill=color_black, font=font1 ,anchor='lm' ,align='center')

#スタンプ
text5="@hana_bot"
draw.text((1000, 150+l*50), text5, fill=color_dimgray, font=font1 ,anchor='rd' ,align='center')
#切り抜き
imcrop = im.crop((0, 0, 1100, 200+l*50))
#画像を保存
imcrop.save(imagefilepath)


#WEBHOOK
#hana塾サーバー
WEBHOOK_URL = "https://discord.com/api/webhooks/1412952583030444064/f_6CPlPODN-2gPqMEkioYgAWraxxE0_kDV49owkeWoiWQmqxkMtvFIGnAOwK_NRV8uJ1?wait=true"
#hana塾サーバー(指標部屋)
#WEBHOOK_URL2 = "https://discord.com/api/webhooks/1339135865829457952/zTJEkbXassYmgLpNTQ7_9TwoI9IYEC-HpFDfQ9opi_Sl-zdWEnji0TB2xmZXSu-DYFij?wait=true"
#テストサーバー
#WEBHOOK_URL = "https://discordapp.com/api/webhooks/1303499824108273745/jpQdcsHz0UtnPbyhOcYYuIXDrPbdL9E_ggvgCL2WDKEaJkG6PDJjSqFdoAjsvF7hn5eW?wait=true"

### メッセージ
payload = {
	"content"		: "本日の主な予定" ,
}

### 画像添付
with open(imagefilepath, 'rb') as f:
	file_bin = f.read()
files_qiita = {
	"favicon" : ( imagefilepath, file_bin),
}
###送信
res = requests.post( WEBHOOK_URL, data={"payload_json": json.dumps(payload)} ,files = files_qiita )

print("finish")