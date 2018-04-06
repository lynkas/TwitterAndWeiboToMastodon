# -*- coding: utf-8 -*-

from urllib.request import urlopen
import xml.etree.ElementTree as et
from bs4 import BeautifulSoup as BS
from dateutil import parser
from urllib import request
import os
class getxml():

    def __init__(self,thisuserid):
        self.retlist = []
        self.isNotForward = True
        self.userid=thisuserid
        try:
            openurl=urlopen("https://api.izgq.net/weibo/rss/" + self.userid)
        except:
            print("Weibo, Failed to get "+thisuserid)
            return

        xml = openurl.read().decode('utf-8').replace('<br><br>转发', '江泽民QsCfTDlawka3')
        channel = et.fromstring(xml).find('channel')
        self.username = channel.find('title').text[:-3]
        item = channel.findall('item')

        self.newfile=""
        self.lasttime=parser.parse('1970-1-1 00:00:00 +0')
        with open(".wtimelog.txt","r+") as log:
            for line in log:
                if line.split("#")[0]==self.userid:
                    self.lasttime= parser.parse(line.replace("\n", "").split("#")[1])
                else:
                    if line !="\n":
                        self.newfile = self.newfile + line

            log.close()

        if self.lasttime ==parser.parse('1970-1-1 00:00:00 +0'):
            if parser.parse(item[1].find('pubDate').text) >= parser.parse(item[0].find('pubDate').text) :
            #     self.lasttime = parser.parse(item[2].find('pubDate').text)
            # else:
            #     self.lasttime = parser.parse(item[1].find('pubDate').text)
                for i in item:
                    j = parser.parse(i.find('pubDate').text)
                    if j > self.lasttime:
                        self.lasttime = j

        self.finaltime = self.lasttime

        self.retlist = []

        newpath = r'./src'
        if not os.path.exists(newpath):
            os.makedirs(newpath)

        for i in item:
            isNotForward = True
            if parser.parse(i.find('pubDate').text) > self.lasttime:
                soup = BS(i.find('description').text, "html.parser")
                imgarray=[]

                for eachimg in soup.find_all("img"):
                    if len(imgarray)< 4:
                        imgarray.append(eachimg['src'])

                if '江泽民QsCfTDlawka3' in soup.get_text():
                    isNotForward = False

                content = soup.get_text()
                cont =[]
                if not isNotForward:
                    cont.append(content.split("江泽民QsCfTDlawka3")[0])
                    cont.append(content.split("江泽民QsCfTDlawka3")[1])
                else:
                    cont.append(content)
                aarray = []

                for eacha in soup.find_all("a"):
                    if ('weibo.cn/n/' not in eacha['href']) and ('weibo.cn/k/' not in eacha['href']):
                        aarray.append(eacha['href'])

                newpath = r'./src'
                if not os.path.exists(newpath):
                    os.makedirs(newpath)

                for url in imgarray:
                    request.urlretrieve(url, 'src/' + url.split('/')[-1])

                weibo = newweibo(self.username, cont, parser.parse(i.find('pubDate').text),imgarray,aarray)

                for url in weibo.imglist:
                    request.urlretrieve(url, 'src/' + url.split('/')[-1])

                self.retlist.append(weibo)
                if self.finaltime < weibo.time:
                    self.finaltime=weibo.time

        self.newfile=self.newfile+"\n"+self.userid+"#"+str(self.finaltime)

        with open(".wtimelog.txt","w+") as log:
            log.write(self.newfile)
            log.close()
        print(str(len(self.retlist))+" "+self.username+" has "+str(len(xml)))

class newweibo():

    def __init__(self,username,content,time,imglist,aarray):
        self.username=username
        self.time=time
        self.imglist=imglist
        self.imgname=[]

        if len(content)==2:
            self.comment=content[0]
            self.orig=content[1]
            self.isForward=True
        else:
            self.orig=content[0]
            self.isForward=False

        for imgurl in imglist:
            self.imgname.append(imgurl.split('/')[-1])

        if self.isForward:
            self.finalcontent=self.username+": "+self.comment+" 原微博："+self.orig
        else:
            self.finalcontent=self.username+"："+self.orig

        for a in aarray:
            self.finalcontent+=(" "+a)