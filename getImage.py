from bs4 import BeautifulSoup as bs
import os, sys
from requests_html import HTMLSession

saveDir = "./BeautyImage/"
fileNameCount = 0

def dirCreator(src):
    if not os.path.isdir(src):
        print("Dir not exist")
        print(f"Create a new Dir which name is {saveDir} in current path.")
        os.mkdir(src)
    else:
        print("Dir existed.")

def downloadImage(url, imageDir):
    imgPath = f"{saveDir}{imageDir}"

    if not os.path.isdir(imgPath):
        dirCreator(imgPath)
    
    print(url)
    image = HTMLSession().get(url)

    # with open(saveDir+"beauty"+str(fileNameCount)+".jpg", "wb") as f:
    with open(f"{imgPath}/{fileNameCount}.jpg", "wb") as f:
        f.write(image.content)
        f.close()

urlCount = 4001
dirCreator(saveDir)
while urlCount > 3900:
    try:
        session = HTMLSession()
        
        # beautyTitleUrl = "https://www.ptt.cc/bbs/Beauty/index.html"
        beautyTitleUrl = f"https://www.ptt.cc/bbs/Beauty/index{urlCount}.html"
        urlCount -= 1

        r = session.get(beautyTitleUrl, cookies = {'over18': '1'})
        Soup = bs(r.text, 'html.parser')
        # titles = Soup.html.find(class_="title")
        titles = Soup.find_all(class_='r-ent')

        # 最後三則是公告
        for title in titles[:-3]:
            try:
                print(title.a.text)
                # input("Press any key to continue...")

                text = title.find(class_="title").a.text
                if "肉特" in text:
                    continue

                urlFindInHref = title.find(class_="title").a["href"]
                url = f"https://www.ptt.cc{urlFindInHref}"

                rBeautyPage = session.get(url, cookies = {'over18': '1'})
                Soup = bs(rBeautyPage.text, 'html.parser')
    # Get all image urls
                imgUrls = Soup.find_all("a")
                fileExtension = ['jpg', 'jpeg', 'png', 'gif']
    #  前 6 個 url 是 ppt 網站其他連結

                for imgUrl in imgUrls[5:]:
                    urlIsImage = imgUrl.attrs['href'].split('.')[-1] in fileExtension
                    if urlIsImage:
                        downloadImage(imgUrl.attrs['href'], title.a.text)
                        fileNameCount += 1
                        print(fileNameCount)

            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)