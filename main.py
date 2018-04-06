
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as et
from bs4 import BeautifulSoup as BS
from dateutil import parser
from urllib import request
import os
class getxml():

    def __init__(self,thisusername):
        self.retlist = []
        self.firstmaxnum=-1
        try:
            from urllib.request import urlopen
            openurl=urlopen("https://twitrss.me/twitter_user_to_rss/?user=" + thisusername)
        except:
            print("twitter, failed to get "+thisusername)
            return

        xml = openurl.read().decode('utf-8').replace('<dc:creator>', '<dccreator>').replace('</dc:creator>', '</dccreator>')

        channel = et.fromstring(xml).find('channel')
        self.username = channel.find('title').text.split()[-1]
        self.profile_photo = channel.find('image').find('url').text
        item = channel.findall('item')

        self.newfile=""
        self.lasttime=parser.parse('1970-1-1 00:00:00 +0')
        with open(".timelog.txt","r+") as log:
            for line in log:
                if line.split("#")[0]==self.username:
                    self.lasttime= parser.parse(line.replace("\n", "").split("#")[1])
                else:
                    if line !="\n":
                        self.newfile = self.newfile + line

            log.close()

        if self.lasttime ==parser.parse('1970-1-1 00:00:00 +0'):
            # if parser.parse(item[1].find('pubDate').text) >= parser.parse(item[0].find('pubDate').text) :
            #     self.lasttime = parser.parse(item[2].find('pubDate').text)
            # else:
            #     self.lasttime = parser.parse(item[1].find('pubDate').text)
            for i in item:
                j = parser.parse(i.find('pubDate').text)
                if j>self.lasttime:
                    self.lasttime=j


        self.finaltime = self.lasttime

        self.retlist = []

        newpath = r'./src'
        if not os.path.exists(newpath):
            os.makedirs(newpath)

        for i in item:
            j=parser.parse(i.find('pubDate').text)
            k=BS(i.find('description').text, "html.parser").get_text
            if j > self.lasttime:
                soup = BS(i.find('description').text, "html.parser")
                imgarray=[]

                for eachimg in soup.find_all("img"):
                    if '/emoji/' not in eachimg['src']:
                        if len(imgarray)< 4:
                            imgarray.append(eachimg['src'])

                tweet = newtweet(self.username, soup.get_text().replace('pic.twitter.com', ' https://pic.twitter.com'), parser.parse(i.find('pubDate').text),i.find('dccreator').text.replace('(', '').replace(')', '').replace('@', '').replace(' ',''),imgarray)

                for url in tweet.imglist:
                    request.urlretrieve(url, 'src/' + url.split('/')[-1])

                self.retlist.append(tweet)
                if self.finaltime < tweet.time:
                    self.finaltime=tweet.time

        self.newfile=self.newfile+"\n"+self.username+"#"+str(self.finaltime)

        with open(".timelog.txt","w+") as log:
            log.write(self.newfile)
            log.close()
        print(str(len(self.retlist))+" "+self.username+" has "+ str(len(xml)))
        # self.imgarray = []
        # self.imagename = []

        # self.content = soup.get_text().replace('pic.twitter.com',' https://pic.twitter.com')
        # imgcount=0
        # for eachimg in soup.find_all("img"):
        #     if '/emoji/' not in eachimg['src']:
        #         if imgcount<4:
        #             imgcount+=1
        #             self.imgarray.append(eachimg['src'])





class newtweet():

    def __init__(self,username,content,time,ori,imglist):
        self.username=username
        self.content=content
        self.time=time
        self.ori=ori
        self.imglist=imglist
        self.imgname=[]

        for imgurl in imglist:
            self.imgname.append(imgurl.split('/')[-1])

        if self.ori==self.username:
            self.finalcontent=username+": "+self.content
        else:
            self.finalcontent=self.username+ ' retweets '+self.ori+"'s tweet: "+self.content