import requests
import time
from bs4 import BeautifulSoup as bs
import os
import re
import urllib.request
import json
from requests_html import HTMLSession

def dirCreator(src):
    if not os.path.isdir(saveDir):
        print("Dir not exist")
        print(f"Create a new Dir which name is {saveDir} in current path.")
        os.mkdir(saveDir)
    else:
        print("Dir existed.")
#Create a Dir to save photo.
saveDir="./Beauty2/"
dirCreator(saveDir)

# #Get content in the website.
#1500-2500
#2500-3495
beautyUrlCount=3400
fileNameCount = 0
timeCount=0
while beautyUrlCount<=3495:
    try:
        session = HTMLSession()
        beautyTitleUrl = "https://www.ptt.cc/bbs/Beauty/index"+str(beautyUrlCount)+".html"
        r = session.get(beautyTitleUrl, cookies = {'over18': '1'})
        getTitle = r.html.find(".title")
        # print(temp)
        print(f"Curren Beauty Url Count {beautyUrlCount}")
        for i in getTitle:
            print(i.text)
            if "正妹" in i.text:
                if "肉特" in i.text:
                    break
                for article in i.find('a'):
                    # print(type(list(j.absolute_links)))
                    articleList = list(article.absolute_links)
                    print(articleList[0])

                    #Get image
                    r1 = session.get(articleList[0], cookies = {'over18': '1'})
                    getContent = r1.html.find("#main-content")
                    for i in getContent:
                        getImageUrl= i.find('a')
                        #最後一個網址是該文章的網址，所以要過濾掉
                        imgCount, endCount= 0, len(getImageUrl)-1
                        timeCount=0
                        for image in getImageUrl:
                            # print(imgCount)
                            if imgCount==endCount:
                                break
                            if imgCount%2==0:
                                imageUrlToList = list(image.absolute_links)
                                imageUrl = imageUrlToList[0]
                                if "imgur" not in imageUrl:
                                    continue
                                if "jpg" in imageUrl:
                                    image = HTMLSession().get(imageUrl)
                                    with open(saveDir+"beauty"+str(fileNameCount)+".jpg", "wb") as f:
                                        f.write(image.content)
                                    fileNameCount+=1
                            imgCount+=1
                            time.sleep(timeCount)
        beautyUrlCount+=1
    except Exception as e:
        print(f"Get Error {e}, Current beautyUrlCount {beautyUrlCount}")
        timeCount+=5
        
    