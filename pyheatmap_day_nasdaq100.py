import sys
import pandas as pd
import numpy as np
import yfinance as yf
import datetime
from pyti.stochrsi import stochrsi as srsi
import matplotlib.pyplot as plt
import json
import requests
import time
from PIL import Image, ImageDraw, ImageFont
import tweepy

#ファイルアドレス
listfilepath = r"[任意のディレクトリ]\nasdaq100list.txt"
imagefilepath = r"[任意のディレクトリ]\heatmap_day_nasdaq100.png"
#ファイルからリストを作成
with open(listfilepath, "r", encoding="utf-8") as file:
    tickers = file.read().split('\n')

##色の指定
color_white = (255,255,255)
color_black = (0,0,0)
color_lightgray = (211,211,211)
color_dimgray = (105,105,105)
color_0 = (105,105,105)
color_d1 = (100,69,70)
color_d2 = (139,68,67)
color_d3 = (191,64,69)
color_d4 = (246,53,56)
color_d5 = (242,46,14)
color_u1 = (61,90,80)
color_u2 = (53,118,78)
color_u3 = (47,158,79)
color_u4 = (48,204,90)
color_u5 = (10,219,50)
#線の太さ
linewidth1 = 1
linewidth2 = 1
linewidth3 = 2
linewidth4 = 4
#フォント
font0 = ImageFont.truetype(r"C:\Windows\fonts\arialbd.ttf", 10)
font1 = ImageFont.truetype(r"C:\Windows\fonts\arialbd.ttf", 15)
font2 = ImageFont.truetype(r"C:\Windows\fonts\arialbd.ttf", 20)
font3 = ImageFont.truetype(r"C:\Windows\fonts\arialbd.ttf", 25)
font4 = ImageFont.truetype(r"C:\Windows\fonts\arialbd.ttf", 30)
font5 = ImageFont.truetype(r"C:\Windows\fonts\arialbd.ttf", 40)
#白紙画像の作成
im = Image.new("RGB", (2300, 1500), color_white)
draw = ImageDraw.Draw(im)
#日付
today = datetime.date.today()
dt_now = datetime.datetime.now()
strdt_now = dt_now.strftime('%Y/%m/%d %H:%M')
marketcaplist =[0] * 100
#ループ処理1
for i in range(len(tickers)):
    #time.sleep(0.2)
    
    try :
#時価総額を取得
        marketcaplist[i] = yf.Ticker(tickers[i]).info["marketCap"]
        if (tickers[i]== "NVDA") or (tickers[i]== "AAPL") or (tickers[i]== "MSFT") or (tickers[i]== "AMZN") or (tickers[i]== "TSLA") or (tickers[i]== "META") or (tickers[i]== "GOOGL") :
            marketcaplist[i] = (yf.Ticker(tickers[i]).info["marketCap"])*0.5
        if (tickers[i]== "AVGO")  :
            marketcaplist[i] = (yf.Ticker(tickers[i]).info["marketCap"])*0.75
 
        print(str(i)+ "next")
#エラーの時
    except Exception :
        print(str(tickers[i])+ "error")
totalmarketcap = sum(marketcaplist)
print(totalmarketcap)
linl=[]
#ループ処理2
for i in range(len(tickers)):
    #time.sleep(0.1)
    
    try :
        if tickers[i]=="" :
            text1= ""
            DoDcolor = color_white

#ヒストリカルデータのdfを取得
        else :
            df =yf.Ticker(tickers[i]).history(period="5d")
#前日比を計算
            DoD = ((df.iloc[-1,3]/ df.iloc[-2,3])*100)-100
#構成比率を計算
            composition = marketcaplist[i]/totalmarketcap
#寄与度を計算
            con = composition*DoD*100
#変化があったときon offをつける
            concolor = color_white
            if 20<=con :
                concolor =  color_u5
            elif 10<=con :
                concolor =  color_u3
            elif 3<=con :
                concolor =  color_u3
            elif 0.5<=con :
                concolor =  color_u2
            elif 0.1<=con :
                concolor =  color_u1
            elif -0.1<con :
                concolor =  color_0
            elif -0.5<con :
                concolor =  color_d1
            elif -3<con :
                concolor =  color_d2
            elif -10<con :
                concolor =  color_d3
            elif -20<con :
                concolor =  color_d4
            elif -20>=con :
                concolor =  color_d5
#必要な要素を選択してリストを作成
#テキストを作成
            plussign =""
            if con>0 :
                plussign="+"
            text1 = tickers[i]
            text2 = plussign+ str("{:.2f}".format(con ,2)) +"bp"
            text3 = "("+plussign+ str("{:.2f}".format(DoD ,2)) +"%)"
            
            linl.append([con ,text1,text2,text3,concolor])
            
            if  tickers[i] =="NVDA" :
                P= [100, 200, 300 ,600]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font5 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font4 ,anchor='mm' ,align='center')
            elif  tickers[i] =="AVGO" :
                P= [100, 600, 300 ,800]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font4 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font3 ,anchor='mm' ,align='center')
            elif  tickers[i] =="AMD" :
                P= [100, 800, 200 ,1000]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font3 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="HON" :
                P= [100, 1000, 200 ,1200]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font3 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="KLAC" :
                P= [100, 1200, 200 ,1300]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="AXON" :
                P= [100, 1300, 200 ,1400]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="QCOM" :
                P= [200, 800, 300 ,1000]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font3 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="MU" :
                P= [200, 1000, 300 ,1200]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font3 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="NXPI" :
                P= [200, 1200, 300 ,1300]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="MCHP" :
                P= [200, 1300, 300 ,1400]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="AAPL" :
                P= [300, 200, 500 ,600]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font5 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font4 ,anchor='mm' ,align='center')
            elif  tickers[i] =="ASML" :
                P= [300, 600, 400 ,900]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font3 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="ARM" :
                P= [300, 900, 400 ,1100]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font3 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="ADI" :
                P= [300, 1100, 400 ,1300]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font3 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="ON" :
                P= [300, 1300, 400 ,1400]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="CSCO" :
                P= [400, 600, 500 ,900]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font3 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="TXN" :
                P= [400, 900, 500 ,1100]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font3 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="MRVL" :
                P= [400, 1100, 500 ,1300]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font3 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="GFS" :
                P= [400, 1300, 500 ,1400]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
#----------------------------------------------
            elif  tickers[i] =="MSFT" :
                P= [500+5, 200, 700+5 ,600]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font5 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font4 ,anchor='mm' ,align='center')
            elif  tickers[i] =="META" :
                P= [500+5, 600, 700+5 ,1000]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font5 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font4 ,anchor='mm' ,align='center')
            elif  tickers[i] =="CRWD" :
                P= [500+5, 1000, 600+5 ,1100]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="WDAY" :
                P= [500+5, 1100, 600+5 ,1200]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="DDOG" :
                P= [500+5, 1200, 600+5 ,1300]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="ANSS" :
                P= [500+5, 1300, 600+5 ,1400]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="CDNS" :
                P= [600+5, 1000, 700+5 ,1100]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="ADSK" :
                P= [600+5, 1100, 700+5 ,1200]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="VRSK" :
                P= [600+5, 1200, 700+5 ,1300]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="CSGP" :
                P= [600+5, 1300, 700+5 ,1400]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="GOOGL" :
                P= [700+5, 200, 900+5 ,600]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font5 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font4 ,anchor='mm' ,align='center')
            elif  tickers[i] =="ADBE" :
                P= [700+5, 600, 800+5 ,800]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font3 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="ADP" :
                P= [700+5, 800, 800+5 ,1000]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font3 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="SNPS" :
                P= [700+5, 1000, 800+5 ,1100]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="TTD" :
                P= [700+5, 1100, 800+5 ,1200]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="CTSH" :
                P= [700+5, 1200, 800+5 ,1300]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="ZS" :
                P= [700+5, 1300, 800+5 ,1400]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="INTU" :
                P= [800+5, 600, 900+5 ,800]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font3 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="PANW" :
                P= [800+5, 800, 900+5 ,900]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="APP" :
                P= [800+5, 900, 900+5 ,1000]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="FTNT" :
                P= [800+5, 1000, 900+5 ,1100]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="ROP" :
                P= [800+5, 1100, 900+5 ,1200]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="EA" :
                P= [800+5, 1200, 900+5 ,1300]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="CDW" :
                P= [800+5, 1300, 900+5 ,1400]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="NFLX" :
                P= [900+5, 200, 1000+5 ,600]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font3 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="PLTR" :
                P= [900+5, 600, 1000+5 ,800]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font3 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="MSTR" :
                P= [900+5, 800, 1000+5 ,900]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="INTC" :
                P= [900+5, 900, 1000+5 ,1000]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="TEAM" :
                P= [900+5, 1000, 1000+5 ,1100]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="PAYX" :
                P= [900+5, 1100, 1000+5 ,1200]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="TTWO" :
                P= [900+5, 1200, 1000+5 ,1300]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="MDB" :
                P= [900+5, 1300, 1000+5 ,1400]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
#----------------------------------------------
            elif  tickers[i] =="AMZN" :
                P= [1000+10, 200, 1200+10 ,600]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font5 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font4 ,anchor='mm' ,align='center')
            elif  tickers[i] =="ORLY" :
                P= [1000+10, 600, 1100+10 ,700]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="CPRT" :
                P= [1100+10, 600, 1200+10 ,700]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="COST" :
                P= [1200+10, 200, 1400+10 ,400]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font4 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font3 ,anchor='mm' ,align='center')
            elif  tickers[i] =="PDD" :
                P= [1200+10, 400, 1300+10 ,600]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font3 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="ROST" :
                P= [1200+10, 600, 1300+10 ,700]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="MELI" :
                P= [1300+10, 400, 1400+10 ,600]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font3 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="LULU" :
                P= [1300+10, 600, 1400+10 ,700]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
#----------------------------------------------
            elif  tickers[i] =="TSLA" :
                P= [1000+10, 800, 1400+10 ,1000]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font5 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font4 ,anchor='mm' ,align='center')
#---------------------------------------------- 
            elif  tickers[i] =="BKNG" :
                P= [1000+10, 1100, 1100+10 ,1300]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font3 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="ABNB" :
                P= [1000+10, 1300, 1100+10 ,1400]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="CMCSA" :
                P= [1100+10, 1100, 1200+10 ,1300]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font3 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="CTAS" :
                P= [1100+10, 1300, 1200+10 ,1400]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="SBUX" :
                P= [1200+10, 1100, 1300+10 ,1300]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font3 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="MAR" :
                P= [1200+10, 1300, 1300+10 ,1400]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="CHTR" :
                P= [1300+10, 1100, 1400+10 ,1300]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font3 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="WBD" :
                P= [1300+10, 1300, 1400+10 ,1400]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
#---------------------------------------------- 
            elif  tickers[i] =="ISRG" :
                P= [1400+15, 200, 1500+15 ,400]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font3 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="GILD" :
                P= [1400+15, 400, 1500+15 ,600]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font3 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="IDXX" :
                P= [1400+15, 600, 1500+15 ,700]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="AZN" :
                P= [1500+15, 200, 1600+15 ,400]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font3 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="VRTX" :
                P= [1500+15, 400, 1600+15 ,600]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font3 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="DXCM" :
                P= [1500+15, 600, 1600+15 ,700]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="AMGN" :
                P= [1600+15, 200, 1700+15 ,400]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font3 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="REGN" :
                P= [1600+15, 400, 1700+15 ,500]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="GEHC" :
                P= [1600+15, 500, 1700+15 ,600]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="BIIB" :
                P= [1600+15, 600, 1700+15 ,700]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
#---------------------------------------------- 
            elif  tickers[i] =="CEG" :
                P= [1400+15, 800, 1500+15 ,900]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="EXC" :
                P= [1400+15, 900, 1500+15 ,1000]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="AEP" :
                P= [1500+15, 800, 1600+15 ,900]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="XEL" :
                P= [1500+15, 900, 1600+15 ,1000]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
#---------------------------------------------- 
            elif  tickers[i] =="LIN" :
                P= [1600+20, 800, 1700+20 ,1000]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font3 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
#---------------------------------------------- 
            elif  tickers[i] =="TMUS" :
                P= [1400+15, 1100, 1700+15 ,1200]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font3 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
#---------------------------------------------- 
            elif  tickers[i] =="PYPL" :
                P= [1400+15, 1300, 1600+15 ,1400]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font3 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
#---------------------------------------------- 
            elif  tickers[i] =="FANG" :
                P= [1600+20, 1300, 1700+20 ,1400]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
#---------------------------------------------- 
            elif  tickers[i] =="PEP" :
                P= [1700+25, 200, 1800+25 ,500]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font3 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="CCEP" :
                P= [1700+25, 500, 1800+25 ,600]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="MDLZ" :
                P= [1800+25, 200, 1900+25 ,300]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="MNST" :
                P= [1800+25, 300, 1900+25 ,400]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="KDP" :
                P= [1800+25, 400, 1900+25 ,500]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="KHC" :
                P= [1800+25, 500, 1900+25 ,600]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
#---------------------------------------------- 
            elif  tickers[i] =="AMAT" :
                P= [1700+25, 700, 1800+25 ,900]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font3 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="LRCX" :
                P= [1800+25, 700, 1900+25 ,800]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="PCAR" :
                P= [1800+25, 800, 1900+25 ,900]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
#---------------------------------------------- 
            elif  tickers[i] =="DASH" :
                P= [1700+25, 1000, 1900+25 ,1100]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font3 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="CSX" :
                P= [1700+25, 1100, 1800+25 ,1200]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font3 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
            elif  tickers[i] =="ODFL" :
                P= [1800+25, 1100, 1900+25 ,1200]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
#---------------------------------------------- 
            elif  tickers[i] =="BKR" :
                P= [1700+25, 1300, 1800+25 ,1400]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
#---------------------------------------------- 
            elif  tickers[i] =="FAST" :
                P= [1800+30, 1300, 1900+30 ,1400]
                draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
                draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), text1, fill=color_white, font=font2 ,anchor='md' ,align='center')
                draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
#            print(str(i)+ "finish")

    except Exception :
        print(str(tickers[i])+ "error")
    
#QQQ-----------------------------------------------------------
try :
    df =yf.Ticker("QQQ").history(period="5d")
#前日比を計算
    DoD = ((df.iloc[-1,3]/ df.iloc[-2,3])*100)-100
#変化があったときon offをつける
    DoDcolor = color_white
    if 5<=DoD :
        DoDcolor =  color_u5
    elif 3<=DoD :
        DoDcolor =  color_u3
    elif 2<=DoD :
        DoDcolor =  color_u3
    elif 1<=DoD :
        DoDcolor =  color_u2
    elif 0.2<=DoD :
        DoDcolor =  color_u1
    elif -0.2<DoD :
        DoDcolor =  color_0
    elif -1<DoD :
        DoDcolor =  color_d1
    elif -2<DoD :
        DoDcolor =  color_d2
    elif -3<DoD :
        DoDcolor =  color_d3
    elif -5<DoD :
        DoDcolor =  color_d4
    elif -5>=DoD :
        DoDcolor =  color_d5
#必要な要素を選択してリストを作成
#テキストを作成
    plussign =""
    if DoD>0 :
        plussign="+"
    textQQQ1 = "QQQ"
    textQQQ2 = "("+plussign+ str("{:.2f}".format(DoD ,2)) +"%)"

    P= [2000, 200, 2200 ,400]
    draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
    draw.text(((P[0]+P[2])/2, (P[1]+P[3])/2-5), textQQQ1, fill=color_white, font=font4 ,anchor='md' ,align='center')
    draw.text(((P[0]+P[2])/2, (P[1]+P[3]*3)/4), textQQQ2, fill=color_white, font=font3 ,anchor='mm' ,align='center')

except Exception :
    print("QQQ"+ "error")
#BEST-------------------------------------------------------
linl.sort(reverse=True)
#1
P= [2000, 500, 2200 ,600]
list = linl[0]
text1 = list[1]
text2 = list[2]
text3 = list[3]
concolor = list[4]
draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
draw.text((P[0]+50, (P[1]+P[3])/2), text1, fill=color_white, font=font3 ,anchor='mm' ,align='center')
draw.text((P[0]+150, (P[1]+P[3])/2), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
#2
P= [2000, 600, 2200 ,700]
list = linl[1]
text1 = list[1]
text2 = list[2]
text3 = list[3]
concolor = list[4]
draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
draw.text((P[0]+50, (P[1]+P[3])/2), text1, fill=color_white, font=font3 ,anchor='mm' ,align='center')
draw.text((P[0]+150, (P[1]+P[3])/2), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
#3
P= [2000, 700, 2200 ,800]
list = linl[2]
text1 = list[1]
text2 = list[2]
text3 = list[3]
concolor = list[4]
draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
draw.text((P[0]+50, (P[1]+P[3])/2), text1, fill=color_white, font=font3 ,anchor='mm' ,align='center')
draw.text((P[0]+150, (P[1]+P[3])/2), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
#4
P= [2000, 800, 2200 ,900]
list = linl[3]
text1 = list[1]
text2 = list[2]
text3 = list[3]
concolor = list[4]
draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
draw.text((P[0]+50, (P[1]+P[3])/2), text1, fill=color_white, font=font3 ,anchor='mm' ,align='center')
draw.text((P[0]+150, (P[1]+P[3])/2), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
#WORST-------------------------------------------------------
linl.sort()
#1
P= [2000, 1000, 2200 ,1100]
list = linl[3]
text1 = list[1]
text2 = list[2]
text3 = list[3]
concolor = list[4]
draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
draw.text((P[0]+50, (P[1]+P[3])/2), text1, fill=color_white, font=font3 ,anchor='mm' ,align='center')
draw.text((P[0]+150, (P[1]+P[3])/2), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
#2
P= [2000, 1100, 2200 ,1200]
list = linl[2]
text1 = list[1]
text2 = list[2]
text3 = list[3]
concolor = list[4]
draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
draw.text((P[0]+50, (P[1]+P[3])/2), text1, fill=color_white, font=font3 ,anchor='mm' ,align='center')
draw.text((P[0]+150, (P[1]+P[3])/2), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
#3
P= [2000, 1200, 2200 ,1300]
list = linl[1]
text1 = list[1]
text2 = list[2]
text3 = list[3]
concolor = list[4]
draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
draw.text((P[0]+50, (P[1]+P[3])/2), text1, fill=color_white, font=font3 ,anchor='mm' ,align='center')
draw.text((P[0]+150, (P[1]+P[3])/2), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')
#4
P= [2000, 1300, 2200 ,1400]
list = linl[0]
text1 = list[1]
text2 = list[2]
text3 = list[3]
concolor = list[4]
draw.rectangle((P[0],P[1], P[2],P[3]), fill=concolor, outline=color_black ,width=linewidth2)
draw.text((P[0]+50, (P[1]+P[3])/2), text1, fill=color_white, font=font3 ,anchor='mm' ,align='center')
draw.text((P[0]+150, (P[1]+P[3])/2), text2+"\n"+text3, fill=color_white, font=font2 ,anchor='mm' ,align='center')







#グループ名
P= [100, 120, 450 ,200]
draw.rectangle((P[0],P[1], P[2],P[3]), fill=color_dimgray, outline=color_black ,width=linewidth3)
draw.multiline_text((P[0], P[1]+40), " Electronic Technology", fill=color_white, font=font3 ,anchor='lm' ,align='left')
P= [500+5, 120, 950+5, 200]
draw.rectangle((P[0],P[1], P[2],P[3]), fill=color_dimgray, outline=color_black ,width=linewidth3)
draw.multiline_text((P[0], P[1]+40), " Technology Services", fill=color_white, font=font3 ,anchor='lm' ,align='left')
P= [1000+10,120, 1350+10,200]
draw.rectangle((P[0],P[1], P[2],P[3]), fill=color_dimgray, outline=color_black ,width=linewidth3)
draw.multiline_text((P[0], P[1]+40), " Retail Trade", fill=color_white, font=font3 ,anchor='lm' ,align='left')
P= [1000+10,720, 1350+10,800]
draw.rectangle((P[0],P[1], P[2],P[3]), fill=color_dimgray, outline=color_black ,width=linewidth3)
draw.multiline_text((P[0], P[1]+40), " Consumer Durables", fill=color_white, font=font3 ,anchor='lm' ,align='left')
P= [1000+10,1020, 1350+10,1100]
draw.rectangle((P[0],P[1], P[2],P[3]), fill=color_dimgray, outline=color_black ,width=linewidth3)
draw.multiline_text((P[0], P[1]+40), " Consumer Services", fill=color_white, font=font3 ,anchor='lm' ,align='left')
P= [1400+15,120, 1650+15,200]
draw.rectangle((P[0],P[1], P[2],P[3]), fill=color_dimgray, outline=color_black ,width=linewidth3)
draw.multiline_text((P[0], P[1]+40), " Health Technology", fill=color_white, font=font3 ,anchor='lm' ,align='left')
P= [1400+15,720, 1550+15,800]
draw.rectangle((P[0],P[1], P[2],P[3]), fill=color_dimgray, outline=color_black ,width=linewidth3)
draw.multiline_text((P[0], P[1]+40), " Utilities", fill=color_white, font=font3 ,anchor='lm' ,align='left')
P= [1400+15,1020, 1650+15,1100]
draw.rectangle((P[0],P[1], P[2],P[3]), fill=color_dimgray, outline=color_black ,width=linewidth3)
draw.multiline_text((P[0], P[1]+40), " Communications", fill=color_white, font=font3 ,anchor='lm' ,align='left')
P= [1400+15,1220, 1550+15,1300]
draw.rectangle((P[0],P[1], P[2],P[3]), fill=color_dimgray, outline=color_black ,width=linewidth3)
draw.multiline_text((P[0], P[1]+40), " Commercial\n Services", fill=color_white, font=font2 ,anchor='lm' ,align='left')
P= [1600+20,720, 1700+20,800]
draw.rectangle((P[0],P[1], P[2],P[3]), fill=color_dimgray, outline=color_black ,width=linewidth3)
draw.multiline_text((P[0], P[1]+40), " Process\n Industrie", fill=color_white, font=font2 ,anchor='lm' ,align='left')
P= [1600+20,1220, 1700+20,1300]
draw.rectangle((P[0],P[1], P[2],P[3]), fill=color_dimgray, outline=color_black ,width=linewidth3)
draw.multiline_text((P[0], P[1]+40), " Energy\n Minerals", fill=color_white, font=font2 ,anchor='lm' ,align='left')
P= [1700+25,120, 1850+25,200]
draw.rectangle((P[0],P[1], P[2],P[3]), fill=color_dimgray, outline=color_black ,width=linewidth3)
draw.multiline_text((P[0], P[1]+40), " Consumer\n Non-Durables", fill=color_white, font=font2 ,anchor='lm' ,align='left')
P= [1700+25,620, 1850+25,700]
draw.rectangle((P[0],P[1], P[2],P[3]), fill=color_dimgray, outline=color_black ,width=linewidth3)
draw.multiline_text((P[0], P[1]+40), " Producer\n Manufacturing", fill=color_white, font=font2 ,anchor='lm' ,align='left')
P= [1700+25,920, 1850+25,1000]
draw.rectangle((P[0],P[1], P[2],P[3]), fill=color_dimgray, outline=color_black ,width=linewidth3)
draw.multiline_text((P[0], P[1]+40), " Trans\n portation", fill=color_white, font=font3 ,anchor='lm' ,align='left')
P= [1700+25,1220, 1800+25,1300]
draw.rectangle((P[0],P[1], P[2],P[3]), fill=color_dimgray, outline=color_black ,width=linewidth3)
draw.multiline_text((P[0], P[1]+40), " Industrial\n Services", fill=color_white, font=font2 ,anchor='lm' ,align='left')
P= [1800+30,1220, 1900+30,1300]
draw.rectangle((P[0],P[1], P[2],P[3]), fill=color_dimgray, outline=color_black ,width=linewidth3)
draw.multiline_text((P[0], P[1]+40), " Distributi\n Services", fill=color_white, font=font2 ,anchor='lm' ,align='left')

P= [2000,120, 2150,200]
draw.rectangle((P[0],P[1], P[2],P[3]), fill=color_dimgray, outline=color_black ,width=linewidth3)
draw.multiline_text((P[0], P[1]+40), " ETF", fill=color_white, font=font3 ,anchor='lm' ,align='left')
P= [2000,420, 2150,500]
draw.rectangle((P[0],P[1], P[2],P[3]), fill=color_dimgray, outline=color_black ,width=linewidth3)
draw.multiline_text((P[0], P[1]+40), " BEST", fill=color_white, font=font3 ,anchor='lm' ,align='left')
P= [2000,920, 2150,1000]
draw.rectangle((P[0],P[1], P[2],P[3]), fill=color_dimgray, outline=color_black ,width=linewidth3)
draw.multiline_text((P[0], P[1]+40), " WORST", fill=color_white, font=font3 ,anchor='lm' ,align='left')
P= [2000,500, 2030,530]
draw.rectangle((P[0],P[1], P[2],P[3]), fill=color_dimgray, outline=color_black ,width=linewidth1)
draw.multiline_text((P[0], P[1]+15), "  1", fill=color_white, font=font2 ,anchor='lm' ,align='left')
P= [2000,600, 2030,630]
draw.rectangle((P[0],P[1], P[2],P[3]), fill=color_dimgray, outline=color_black ,width=linewidth1)
draw.multiline_text((P[0], P[1]+15), "  2", fill=color_white, font=font2 ,anchor='lm' ,align='left')
P= [2000,700, 2030,730]
draw.rectangle((P[0],P[1], P[2],P[3]), fill=color_dimgray, outline=color_black ,width=linewidth1)
draw.multiline_text((P[0], P[1]+15), "  3", fill=color_white, font=font2 ,anchor='lm' ,align='left')
P= [2000,800, 2030,830]
draw.rectangle((P[0],P[1], P[2],P[3]), fill=color_dimgray, outline=color_black ,width=linewidth1)
draw.multiline_text((P[0], P[1]+15), "  4", fill=color_white, font=font2 ,anchor='lm' ,align='left')
P= [2000,1000, 2030,1030]
draw.rectangle((P[0],P[1], P[2],P[3]), fill=color_dimgray, outline=color_black ,width=linewidth1)
draw.multiline_text((P[0], P[1]+15), "  4", fill=color_white, font=font2 ,anchor='lm' ,align='left')
P= [2000,1100, 2030,1130]
draw.rectangle((P[0],P[1], P[2],P[3]), fill=color_dimgray, outline=color_black ,width=linewidth1)
draw.multiline_text((P[0], P[1]+15), "  3", fill=color_white, font=font2 ,anchor='lm' ,align='left')
P= [2000,1200, 2030,1230]
draw.rectangle((P[0],P[1], P[2],P[3]), fill=color_dimgray, outline=color_black ,width=linewidth1)
draw.multiline_text((P[0], P[1]+15), "  2", fill=color_white, font=font2 ,anchor='lm' ,align='left')
P= [2000,1300, 2030,1330]
draw.rectangle((P[0],P[1], P[2],P[3]), fill=color_dimgray, outline=color_black ,width=linewidth1)
draw.multiline_text((P[0], P[1]+15), "  1", fill=color_white, font=font2 ,anchor='lm' ,align='left')
#表題
#日付
today = datetime.date.today()
textt1=strdt_now + " Daily_heatmap  NASDAQ100_Contribution_Ratio(bp)  (DoD(%))"
draw.multiline_text((1200, 50), textt1, fill=color_black, font=font5 ,anchor='mm' ,align='center')
#外枠
P= [100, 200, 500 ,1400]
draw.rectangle((P[0],P[1],P[2],P[3]), outline=color_black ,width=linewidth4)
P= [500+5, 200, 1000+5 ,1400]
draw.rectangle((P[0],P[1],P[2],P[3]), outline=color_black ,width=linewidth4)
P= [1000+10, 200, 1400+10 ,700]
draw.rectangle((P[0],P[1],P[2],P[3]), outline=color_black ,width=linewidth4)
P= [1000+10, 800, 1400+10 ,1000]
draw.rectangle((P[0],P[1],P[2],P[3]), outline=color_black ,width=linewidth4)
P= [1000+10, 1100, 1400+10 ,1400]
draw.rectangle((P[0],P[1],P[2],P[3]), outline=color_black ,width=linewidth4)
P= [1400+15, 200, 1700+15 ,700]
draw.rectangle((P[0],P[1],P[2],P[3]), outline=color_black ,width=linewidth4)
P= [1400+15, 800, 1600+15 ,1000]
draw.rectangle((P[0],P[1],P[2],P[3]), outline=color_black ,width=linewidth4)
P= [1400+15, 1100, 1700+15 ,1200]
draw.rectangle((P[0],P[1],P[2],P[3]), outline=color_black ,width=linewidth4)
P= [1400+15, 1300, 1600+15 ,1400]
draw.rectangle((P[0],P[1],P[2],P[3]), outline=color_black ,width=linewidth4)
P= [1600+20, 800, 1700+20 ,1000]
draw.rectangle((P[0],P[1],P[2],P[3]), outline=color_black ,width=linewidth4)
P= [1600+20, 1300, 1700+20 ,1400]
draw.rectangle((P[0],P[1],P[2],P[3]), outline=color_black ,width=linewidth4)
P= [1700+25, 200, 1900+25 ,600]
draw.rectangle((P[0],P[1],P[2],P[3]), outline=color_black ,width=linewidth4)
P= [1700+25, 700, 1900+25 ,900]
draw.rectangle((P[0],P[1],P[2],P[3]), outline=color_black ,width=linewidth4)
P= [1700+25, 1000, 1900+25 ,1200]
draw.rectangle((P[0],P[1],P[2],P[3]), outline=color_black ,width=linewidth4)
P= [1700+25, 1300, 1800+25 ,1400]
draw.rectangle((P[0],P[1],P[2],P[3]), outline=color_black ,width=linewidth4)
P= [1800+30, 1300, 1900+30 ,1400]
draw.rectangle((P[0],P[1],P[2],P[3]), outline=color_black ,width=linewidth4)
P= [2000, 200, 2200 ,400]
draw.rectangle((P[0],P[1],P[2],P[3]), outline=color_black ,width=linewidth4)
P= [2000, 500, 2200 ,900]
draw.rectangle((P[0],P[1],P[2],P[3]), outline=color_black ,width=linewidth4)
P= [2000, 1000, 2200 ,1400]
draw.rectangle((P[0],P[1],P[2],P[3]), outline=color_black ,width=linewidth4)

#スタンプ
text5="@hana_bot"
draw.text((2250, 1450), text5, fill=color_dimgray, font=font1 ,anchor='rd' ,align='center')
#画像を保存
im.save(imagefilepath)
print("finish")

#WEBHOOK
#hana塾サーバー
WEBHOOK_URL = "[WEBHOOKのアドレス]?wait=true"
### メッセージ
payload = {
	"content"		: "NASDAQ100 寄与度ヒートマップ配信" ,
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