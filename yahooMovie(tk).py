import tkinter as tk
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
from io import BytesIO
import urllib
import json
import os
import tkinter.messagebox 

#Request+Page
def webrequesT(urL):
    global noMovie,pagE
    rQ=requests.get(urL).text
    souP=BeautifulSoup(rQ,"html5lib")
    souP1=souP.find("ul","release_list")
    
    for mySoup in souP1.find_all("li"):
        lisTsmall=[]
        try:
            cName=mySoup.find("div","release_movie_name").a.text.strip()
            lisTsmall.append(cName)
            
            eName=mySoup.find("div","en").a.text.strip()  
            lisTsmall.append(eName)
            
            datE=mySoup.find("div","release_movie_time").text.strip()
            lisTsmall.append(datE)
            
            piC=mySoup.find("div","release_foto").find('a','gabtn').find('img')['data-src']
            lisTsmall.append(piC)
            
            synopsiS=mySoup.find("div","release_text").text.strip()
            lisTsmall.append(synopsiS)
            
            lisT.append(lisTsmall)
        except:
            continue
        noMovie=0
        changEmoviE(noMovie)
    #多頁
    if pagE <15:
        pagE+=1
        urL=(urL.split('?'))[0]+'?page='+str(pagE)
        webrequesT(urL)
    
#改變畫面資料
def changEmoviE(noMovie):
    texT.configure(state='normal')   #textBox可讀寫
    texT2.configure(state='normal')
    texT.delete(1.0,tk.END)   #清空textBox
    texT2.delete(1.0,tk.END)
    #textBox.Insert
    texT.insert(tk.END, 'Ⅰ.電影中文名稱: '+'\n'+'\t'+lisT[noMovie][0]+'\n')
    texT.insert(tk.END, 'Ⅱ.電影英文名稱: '+'\n'+'\t'+lisT[noMovie][1]+'\n')
    texT.insert(tk.END, 'Ⅲ.'+lisT[noMovie][2]+'\n')
    texT2.insert(tk.END, 'Ⅳ.電影描述: '+'\n'+lisT[noMovie][4]+'\n')
    #Label set Image in online
    webImg=requests.get(lisT[noMovie][3])
    img= Image.open(BytesIO(webImg.content))
    #改變圖片大小
    w, h= img.size
    if w>400:
        h= int(h*400/w)
        w=400
    if h>600:
        w= int(w*600/h)
        h=600
    img= img.resize((w,h))
    tk_img= ImageTk.PhotoImage(img)
    #顯示圖片
    lbPic['image']= tk_img
    lbPic.image= tk_img
    texT.configure(state='disabled')   #textBox唯讀
    texT2.configure(state='disabled')

#本週新片
def _hit1():
    global pagE
    lisT.clear()
    pagE=1
    urL="https://movies.yahoo.com.tw/movie_thisweek.html"
    webrequesT(urL)

#上映中
def _hit4():
    global pagE
    lisT.clear()
    pagE=1
    urL="https://movies.yahoo.com.tw/movie_intheaters.html"
    webrequesT(urL)

#即將上映
def _hit5():
    global pagE
    lisT.clear()
    pagE=1
    urL="https://movies.yahoo.com.tw/movie_comingsoon.html"
    webrequesT(urL)

#backPage
def _hit2():
    global noMovie
    texT.delete(1.0,tk.END)
    noMovie=noMovie-1
    if noMovie>=0:
        noMovie=noMovie
    else:
        noMovie=0
        tk.messagebox.showinfo("提示","已是第一頁")
    changEmoviE(noMovie)

#nextPage
def _hit3():
    global noMovie
    texT.delete(1.0,tk.END)
    noMovie=noMovie+1
    if noMovie<=(len(lisT)-1):
        noMovie=noMovie
    else:
        noMovie=(len(lisT)-1)
        tk.messagebox.showinfo("提示","已是最後一頁")
    changEmoviE(noMovie)
    
#儲存成JSON+圖片
def _savE():
    movieDir=lisT[noMovie][0]+ "/"
    if not os.path.exists(movieDir):
        os.mkdir(movieDir)
        lisTT=[]
        fileNmae=lisT[noMovie][0]
        lisTT.append('Ⅰ.電影中文名稱:'+lisT[noMovie][0])
        lisTT.append('Ⅱ.電影英文名稱:'+lisT[noMovie][1])
        lisTT.append('Ⅲ.'+lisT[noMovie][2])
        lisTT.append('Ⅳ.電影海報網址:'+lisT[noMovie][3])
        lisTT.append('Ⅴ.電影描述:'+lisT[noMovie][4])
        jsoNamE=fileNmae+"\\"+fileNmae+".json"
        with open(jsoNamE,"w",encoding="utf-8") as jsonFile2:
            json.dump(lisTT,jsonFile2,ensure_ascii=False,indent=4)
        picNamE=fileNmae+"\\"+fileNmae+".jpg"
        urllib.request.urlretrieve(lisT[noMovie][3],picNamE)

#關閉
def _hit6():
    qQ=tk.messagebox.askokcancel("離開確定","確定要結束程式嗎???")
    if qQ:
        wiN.destroy()

#main
lisT=[]
pagE=1
noMovie=int()

#視窗設定
wiN = tk.Tk()
wiN.title("yahooMovie(●’ω`●）")
wiN.geometry("1500x1000+100+0")
wiN.resizable(False, False)
wiN.configure(background='black')

#按鈕設定
btN1 = tk.Button(wiN, text="本週新片!!",fg="green", font=("Arial Black", 16), width=10, height=2, command=_hit1)
btN1.place(x=180,y=0)

btN4 = tk.Button(wiN, text="上映中!!",fg="green", font=("Arial Black", 16), width=10, height=2, command=_hit4)
btN4.place(x=360,y=0)

btN5 = tk.Button(wiN, text="即將上映!!",fg="green", font=("Arial Black", 16), width=10, height=2, command=_hit5)
btN5.place(x=540,y=0)

btN2 = tk.Button(wiN, text="上一部(∩_∩)",fg="blue", font=("Arial Black", 16), width=10, height=2, command=_hit2)
btN2.place(x=0,y=0)

btN3 = tk.Button(wiN, text="下一部(´∀`)",fg="blue", font=("Arial Black", 16), width=10, height=2, command=_hit3)
btN3.place(x=720,y=0)

btN6 = tk.Button(wiN, text="儲存成JSON(≧▽≦)",fg="orange", font=("Arial Black", 16), width=13, height=2, command=_savE)
btN6.place(x=900,y=0)

btN7 = tk.Button(wiN, text="離開(╬ Ò ‸ Ó)",fg="red", font=("Arial Black", 16), width=13, height=2, command=_hit6)
btN7.place(x=1250,y=0)

#textBox設定
texT=tk.Text(wiN, font=("Arial Black", 20), fg ="white", bg ="black")
texT.place(x=0,y=83,width=1100,height=300)

texT2=tk.Text(wiN, font=("Arial Black", 20), fg ="white", bg ="black")
texT2.place(x=0,y=383,width=1100,height=550)

#Label設定
lbPic = tk.Label(wiN, width=400, height=600, bg ="black")
lbPic.place(x=1100,y=110,width=400,height=600)

wiN.mainloop()

