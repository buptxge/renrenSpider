#! /usr/lib/python
#-*- coding: utf-8 -*-
import time
import sys
import urllib
import urllib2
import cookielib
import os
import re
from bs4 import BeautifulSoup

#import js2html
class renrenSpider:    

    def __init__(self,email,password):
        self.email = email
        self.password = password
        self.domain = 'renren.com'
        self.id = ''
        self.sid = ''
        try:
            self.cookie = cookielib.CookieJar()
            self.cookieProc = urllib2.HTTPCookieProcessor(self.cookie)
        except:
            raise
        else:
            opener = urllib2.build_opener(self.cookieProc)
            opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
            urllib2.install_opener(opener)
    
    def login(self):
        url='http://3g.renren.com/login.do' #登陆人人网3g首页
        postdata = {
                    'email':self.email,
                    'password':self.password,
                    }
        
        req = urllib2.Request(url,urllib.urlencode(postdata))
        index = urllib2.urlopen(req).read()
        indexSoup = BeautifulSoup(index)  #首页soup

        if (len(indexSoup.find_all(".notice"))!=0):  #查找是否有class名字为notice的元素，表示是否需要输入验证码
            print "需要输入验证码："
        else:
            print "不需要验证码"
                    
        indexFile = open('index.html','w')
        indexFile.write(indexSoup.prettify())
        indexFile.close()
        tmp = indexSoup.select('.cur')[0]
        idHref =  tmp.parent.contents[2]['href']
        m = re.findall(r"\d{6,}",str(idHref))
        self.id = m[0]
        print "用户ID为：" + self.id

        m = re.findall(r"(?<=sid=).*?(?=&)",str(idHref))
        self.sid = m[0]
        print "用户的sid为:" + self.sid

       # for item in self.cookie:
       #     self.cookieDict[item.name] = item.value
       # print self.cookieDict

    def getStatus(self):
        #获取个人状态页面

        statusDate = []
        statusContent = []
        originStatusContent = []  
        url = 'http://3g.renren.com/profile.do' #登陆到个人主页
        profileGetData = {
                          'id':str(self.id),
                          'sid':self.sid  
                         }
        req = urllib2.Request(url,urllib.urlencode(profileGetData))
        profile = urllib2.urlopen(req).read()
        profileSoup = BeautifulSoup(profile)
       # print profileSoup.prettify()
        url = profileSoup.select('.sec')[5].find_all('a')[3]['href']    #获得链接

        req = urllib2.Request(url)
        statusFile = urllib2.urlopen(req).read()
        statusSoup = BeautifulSoup(statusFile)
        statusFile = open("status.html",'w')
        statusFile.write( statusSoup.prettify())
        statusFile.close()
        
        totalPageHtml = statusSoup.select(".gray")[0].contents
        totalPage = re.findall(r"(?<=/)\d+(?=[^\d])",str(totalPageHtml))
        totalPage = int(totalPage[0])
        print "总共有:"+str(totalPage)+"页"
        
        nowPage = 1
       # totalPage = 15
        while (nowPage<=totalPage) :
            print "当前正在获取第"+str(nowPage)+"页状态信息"
            statusList = statusSoup.select(".list")[0].children
            for child in statusList:
                #statusNum = statusNum+1
                if (child.select(".time")):# Step1: 找时间戳，确定为状态信息
                    statusDate.append(child.select(".time")[0].string) 
                    if (child.select(".forward")): #step2:找class名为forward的内容，这部分为转的状态
                        tempStr = str(child.a.next_element)
                        m = re.findall(r"^.*?(?=转自)",tempStr)                            
                        if m: 
                            statusContent.append(m[0])
                        else :
                            statusContent.append("无")

                        originStatusContent.append(child.select(".forward")[0].a.next_element.next_element) 
                    else:   #step3:这些是原创内容，直接保存
                       statusContent.append(child.a.next_element)
                       originStatusContent.append("无")                    
            nowPage = nowPage+1
            if (nowPage>totalPage): break
            nextPageUrl =str(statusSoup.select(".l")[0].a['href']) #查找下一页URL并跳转
            req = urllib2.Request(nextPageUrl)
            statusFile = urllib2.urlopen(req).read() 
            statusSoup = BeautifulSoup(statusFile)                            
           # for state in statusList:
           #     print state.name     
        
        finalFile = open("UserData/"+self.id,"w")
        for i in range (0,len(statusDate)):
            finalFile.write("第"+str(i+1)+"条:"+"\n")
            finalFile.write("时间:"+str(statusDate[i])+"\n")
            finalFile.write("状态："+str(statusContent[i])+"\n")
            finalFile.write("转发原文："+str(originStatusContent[i])+"\n")
            finalFile.write("\n") 

if __name__ == '__main__':
    email = raw_input("输入人人网账号")
    password = raw_input("输入人人网密码")
    reload(sys)
    sys.setdefaultencoding('utf-8')  
    renrenLogin = renrenSpider(email,password)
    renrenLogin.login()
    renrenLogin.getStatus() 
    
