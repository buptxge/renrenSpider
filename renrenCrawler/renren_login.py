#! /usr/lib/python
#-*- coding: utf-8 -*-
import time
import sys
import urllib
import urllib2
import cookielib
import os
import re
import getpass
import socket
from bs4 import BeautifulSoup

import sqlHelper

class renrenSpider:    

    def __init__(self,email,password):
        self.email = email
        self.password = password
        self.domain = 'renren.com'
        self.id = ''
        self.sid = ''
        self.name = ''
        self.level = ''
        self.viewers = ''
        self.friends = ''
        self.journals = ''
        self.albums = ''
        self.shares = ''
        self.boards = ''
        self.sex = '-1'
        self.birthday = ''
        self.constellation = ''
        self.hometownProvince = ''
        self.hometownCity = ''
        self.currentYear = time.strftime("%Y",time.gmtime( time.time()))
        try:
            self.cookie = cookielib.CookieJar()
            self.cookieProc = urllib2.HTTPCookieProcessor(self.cookie)
        except:
            raise
        else:
            opener = urllib2.build_opener(self.cookieProc)
            opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
            urllib2.install_opener(opener)
    
    def Navigate(self,url,data={}):           #定义链接函数，有超时重连功能
        tryTimes = 0
        while True:
            if (tryTimes>20):
                print "多次尝试仍无法链接网络，程序终止"
                break
            try:
                if (data=={}):
                    req = urllib2.Request(url)
                else:
                    req = urllib2.Request(url,urllib.urlencode(data))
                req = urllib2.urlopen(req).read()
                tryTimes = tryTimes +1
            except socket.error:
                print "连接失败，尝试重新连接"
            else:
                break
        return req

    def Login(self):
        url='http://3g.renren.com/login.do' #登陆人人网3g首页
        postdata = {
                    'email':self.email,
                    'password':self.password,
                    }
        index = self.Navigate(url,postdata) 
        indexSoup = BeautifulSoup(index)  #首页soup

        if (len(indexSoup.find_all(".notice"))!=0):  #查找是否有class名字为notice的元素，表示是否需要输入验证码
            print "需要输入验证码："
        else:
            print "不需要验证码"
                    
        #indexFile = open('index.html','w')
        #indexFile.write(indexSoup.prettify())
        #indexFile.close()
       # print indexSoup.prettify()
        print indexSoup.prettify()
        tmp = indexSoup.select('.cur')[0]
        
        idHref =  tmp.parent.contents[2]['href']
        m = re.findall(r"\d{6,}",str(idHref))
        self.id = m[0]
        print "用户ID为：" + self.id
        m = re.findall(r"(?<=sid=).*?(?=&)",str(idHref))
        self.sid = m[0]
        print "用户的sid为:" + self.sid
        
        GetStatus
    def GetProfile(self,url):    
        for i
        #url = 'http://3g.renren.com/profile.do' #登陆到个人主页
        #profileGetData = {
        #                  'id':str(self.id),
        #                  'sid':self.sid  
        #                 }
        #req = urllib2.Request(url,urllib.urlencode(profileGetData))
        profile = self.Navigate(url) #根据url来获取信息
        self.profileSoup = BeautifulSoup(profile)
       # print profileSoup.prettify()

        #获取用户id
        self.id = re.findall(r"(?<=id=)\d+",url)[0]

        #获取用户姓名
        self.name = self.profileSoup.select('.ssec')[0].b.contents[0] 
        print "开始获取"+self.name+"的数据"+",id为"+str(self.id)

        #获取用户等级
        self.level = self.profileSoup.select('.ssec')[0].find_all('b')[1].contents[0] 

        #获取用户好友数
        self.friends = self.profileSoup.select('.gray')[0].contents[0] 
        m = re.findall(r"\d+",self.friends) 
        self.friends = m[0]
        
        #获取用户总来访
        self.viewers = self.profileSoup.select('.gray')[1].contents[0]
        m = re.findall(r"\d+",self.viewers)
        self.viewers = m[0]
      
        #获取用户总日志数
        self.journals = self.profileSoup.select('.gray')[2].contents[0]
        m = re.findall(r"\d+",self.journals)
        self.journals = m[0]

        #获取用户相册数
        self.albums = self.profileSoup.select('.gray')[3].contents[0]
        m = re.findall(r"\d+",self.albums)
        self.albums = m[0]

        #获取用户分享数
        self.shares = self.profileSoup.select('.gray')[4].contents[0]
        m = re.findall(r"\d+",self.shares)
        self.shares = m[0]

        #获取用户留言板数
        self.boards = self.profileSoup.select('.gray')[6].contents[0]
        m = re.findall(r"\d+",self.boards)
        if m:
            self.boards = m[0]
        else:
            self.boards = self.profileSoup.select('.gray')[7].contents[0]
            m = re.findall(r"\d+",self.boards)
            self.boards = m[0]

        #跳转到详细资料页面，开始获取详细用户资料
        url = self.profileSoup.select('.ssec')[0].find_all('div')[0].find_all('td')[1].a['href']
        details = self.Navigate(url)
        detailsSoup = BeautifulSoup(details)
        # try用户详细资料页面，有可能物内容，则跑出异常
        try:
            details = str(detailsSoup.select('.list')[0].find_all('div')[1])
        except IndexError:
            print "无详细资料"
            
        else:
            #print details
            #获取性别 0为男 1为女
            m = re.findall(r"(?<=性别：).*?(?=<)",details)
            if m:
                if (m[0]=="男"):
                    self.sex = 0
                else :
                    self.sex = 1
           # print self.sex
            #获取生日
            m = re.findall(r"生日：(\d+)年(\d+)月(\d+)日",details)
            if m:
                year = str(m[0][0])

                month = str(m[0][1])
                if (len(month)==1): 
                    month = "0"+month

                day = str(m[0][2])
                if (len(day)==1):
                    day = "0"+day
                self.birthday = year+'-'+month+'-'+day
          #  print self.birthday

            #获取星座
            m = re.findall(r"(?<=span>).*?座",details)
            if m:
                self.constellation = m[0]
            #print self.constellation
            #获取家乡
            m = re.findall(r"家乡：(.*?)\s(.*?)市",details)
            if m:
                self.hometownProvince = str(m[0][0])
            if m:
                self.hometownCity = str(m[0][1])

            #print self.hometownCity
            #print self.hometownProvince
            #time.sleep(10)
        
    def GetAllFriendsList(self):

        url = "http://3g.renren.com/friendlist.do"
        friendsListGetData = {
                            'sid':self.sid
                            }
        friendsList = self.Navigate(url,friendsListGetData)
        self.friendsListSoup = BeautifulSoup(friendsList)

        #print self.friendsListSoup.prettify()
        
        totalFriendsPage = self.friendsListSoup.select(".l")[0].span.contents[0]
        totalFriendsPage = int(re.findall(r"(?<=/)\d+",totalFriendsPage)[0])
        nowPage = 1
       # totalFriendsPage = 2
        while (nowPage<=totalFriendsPage) :
            print "当前正在获取"+str(nowPage)+"页的好友地址"
            tmpurl = self.friendsListSoup.select(".p")
            for tmp in tmpurl:
                tmp = re.findall(r"(?<=href=\").*?(?=&amp)",str(tmp))[0]
                allFriendsUrl.append(tmp)

            nextPageUrl = self.friendsListSoup.select(".l")[0].a['href']
            friendsList = self.Navigate(nextPageUrl)
            self.friendsListSoup = BeautifulSoup(friendsList)
            nowPage = nowPage +1
                     
    def GetStatus(self):
        #获取个人状态页面

        statusDate = []
        statusContent = []
        originStatusContent = []  
        comments = []
        #url = self.profileSoup.select(".sec")[3].find_all('a')[3]['href'] #获取链接 好友情况
        url = self.profileSoup.select('.sec')[5].find_all('a')[3]['href']    #获取链接(个人)
        
        statusFile = self.Navigate(url)
        statusSoup = BeautifulSoup(statusFile)
        #statusFile = open("status.html",'w')
        #statusFile.write( statusSoup.prettify())
        #statusFile.close()
        
        totalPageHtml = statusSoup.select(".gray")[0].contents
        totalPage = re.findall(r"(?<=/)\d+(?=[^\d])",str(totalPageHtml))
        totalPage = int(totalPage[0])
        print "总共有:"+str(totalPage)+"页"
        
        nowPage = 1
        #totalPage = int(totalPage /20)
        while (nowPage<=totalPage) :
            print "当前正在获取第"+str(nowPage)+"页状态信息"
            statusList = statusSoup.select(".list")[0].children
            for child in statusList:

                if (child.select(".time")):
                # Step1: 找时间戳，确定为状态信息,并把带有时间的内容存储为xxxx-xx-xx xx:xx的形式
                    tmpTimeStr = child.select(".time")[0].string
                    print tmpTimeStr
                    m = re.findall(r"\d{4}",str(tmpTimeStr))
                    # 找到年的部分，如果没有则说明为当前一年，使用self.currentYear
                    if m:
                       # print "find year"
                        year = m[0]
                    else:
                        year = self.currentYear

                   # m = re.findall(r"(\d+)月(\d+)日\s(\d{2}:\d{2})",tmpTimeStr)
                    #找月和日
                    m = re.findall(r"\d{1,2}",tmpTimeStr)
                
                    if m:
                        month = str(m[0])
                        if (len(month)==1) : month = "0"+month

                        day = str(m[1])
                        if (len(day)==1) : day = "0"+day
                    
                    #找xx:xx样式的时间
                    m = re.findall(r"\d\d:\d\d",tmpTimeStr)
                    if m:                    
                        time = str(m[0])

                    tmpTimeStr = year+"-"+month+"-"+day+" "+time
                    statusDate.append(tmpTimeStr) 

                    #step2:找时间戳之后第一个<a>标记，获取状态回复数
                    tmpCommentStr = child.select(".time")[0].nextSibling.contents[0]
                    m = re.findall(r"\d+",str(tmpCommentStr))
                    if m:
                        comments.append(int(m[0]))
                    else:
                        comments.append(int(0))
                     
                    #step3:找class名为forward的内容，这部分为转的状态
                    if (child.select(".forward")): 
                        tmpStr = child.select(".forward")[0]
                        tmpStr = re.subn(r"<a href=.*?>|</a>|<img alt=.*?>|<p class=\"forward\">|</p>","",str(tmpStr))
                        originStatusContent.append(tmpStr[0])

                        tmpStr = child.select(".forward")[0].parent
                        tmpStr = re.findall(r"((?<=></a>)[\s\S]*(?=<p class=\"forward\"))",str(tmpStr))
                        tmpStr = re.subn(r"<a href=.*?>|</a>|<img alt=.*?>","",tmpStr[0])
                        m = re.findall(r"^.*?(?=转自)",str(tmpStr[0]))
                        if m: 
                                statusContent.append(m[0])
                        else:
                                statusContent.append("无")
                       # originHtml = child.select(".forward")[0].a.next_element.next_element
                       # m = re.findall(r"class=\"time\"",str(originHtml))
                       # if m:
                       #     originStatusContent.append("原始状态已删除")
                       # else :
                       #     originStatusContent.append(originHtml)

                    #step4:这些是原创内容，直接保存
                    else:   
                        tmpStr = child.select(".time")[0].parent
                        tmpStr = re.findall(r"((?<=></a>)[\s\S]*(?=<p class=\"time\"))",str(tmpStr))
                        tmpStr = re.subn(r"<a href=.*?>|</a>|<img alt=.*?>|<p class=.*?>|</p>","",tmpStr[0])

                        statusContent.append(tmpStr[0])
                        #print tmpStr[0]
                        originStatusContent.append("无")                    
            nowPage = nowPage+1
            if (nowPage>totalPage): break
                                    
            #查找下一页URL并跳转
            nextPageUrl =str(statusSoup.select(".l")[0].a['href']) 
            statusFile = self.Navigate(nextPageUrl)
            statusSoup = BeautifulSoup(statusFile)                            
           # for state in statusList:
           #     print state.name     
        
        #获得当前总状态数
        sql = 'SELECT count(*) from Status'# select Total status
        renrenSqlHelper.DoSql(sql)
        totalStatus = int(renrenSqlHelper.GetResult()[0][0]) 

        #获得下一条转发的开始记录位置
        statusStart = totalStatus+1
        statusEnd = statusStart + len(statusDate)-1

        #UserInfo数据表写入，主要是用户基本信息
        sql = "INSERT INTO UserInfo(renrenID,name,friends,level,viewers,sex,birthday,constellation,province,city,journals,albums,shares,boards,statusNum,statusStart,statusEnd) values (%r,%r,%d,%d,%d,%d,%r,%r,%r,%r,%d,%d,%d,%d,%d,%d,%d)"%(str(self.id),str(self.name),int(self.friends),int(self.level),int(self.viewers),int(self.sex),str(self.birthday),str(self.constellation),str(self.hometownProvince),str(self.hometownCity),int(self.journals),int(self.albums),int(self.shares),int(self.boards),len(statusDate),statusStart,statusEnd)
        sql = sql.replace("\\","\\\\")
        renrenSqlHelper.DoSql(sql) 

        #文本输出内容，存储在/UserData/对应用户id 文件内
        finalFile = open("UserData/"+self.id+"-"+self.name,"w")

        finalFile.write("性别用0,1,-1存，0代表男,-1表示未填写个人资料"+"\n")
        finalFile.write("日期统一格式为：xxxx-xx-xx xx:xx,单个数字前面补0"+"\n")
        finalFile.write("----------------------------------------------------\n")
        finalFile.write("名字："+self.name+"\n")
        finalFile.write("性别："+str(self.sex)+"\n")
        finalFile.write("生日："+self.birthday+"\n")
        finalFile.write("星座："+self.constellation+"\n")
        finalFile.write("家乡（省）:"+self.hometownProvince+"\n")
        finalFile.write("家乡（市）:"+self.hometownCity+"\n")
        finalFile.write("人人ID:"+self.id+"\n")
        finalFile.write("等级:"+self.level+"\n")
        finalFile.write("来访数量："+self.viewers+"\n")
        finalFile.write("好友数:"+self.friends+"\n")
        finalFile.write("日志数:"+self.journals+"\n")
        finalFile.write("相册数:"+self.albums+"\n")
        finalFile.write("分享数:"+self.shares+"\n")
        finalFile.write("留言板数:"+self.boards+"\n")
        finalFile.write("----------------------------------------------------\n")
        #循环写入Status数据表，包括用户每一条状态的信息

        for i in range (0,len(statusDate)):
            sql = "INSERT INTO Status(content,originContent,publishDate,comments) values (%r,%r,%r,%d)" % (str(statusContent[i]),str(originStatusContent[i]),str(statusDate[i]),int(comments[i]))
            sql = sql.replace("\\","\\\\")
            renrenSqlHelper.DoSql(sql)
            finalFile.write("第"+str(i+1)+"条:"+"\n")
            finalFile.write("时间:"+str(statusDate[i])+"\n")
            finalFile.write("状态："+str(statusContent[i])+"\n")
            finalFile.write("转发原文："+str(originStatusContent[i])+"\n")
            finalFile.write("回复数："+str(comments[i])+"\n")
            finalFile.write("\n") 
        renrenSqlHelper.Commit() 
        finalFile.close()

if __name__ == '__main__':
    email = raw_input("输入人人网账号")
    password = getpass.getpass("输入人人网密码")
    reload(sys)

    timeout = 5
    socket.setdefaulttimeout(timeout)

    sys.setdefaultencoding('utf-8')
    renrenSqlHelper = sqlHelper.sqlHelper('localhost','mysql用户名','mysql密码','存储的表名','utf8')
    spider = renrenSpider(email,password)
    spider.Login()
    allFriendsUrl = []
    #spider.GetAllFriendsList()  #收集登陆用户的好友信息，对应的链接信息存放到allFriendsUrl
    #friendNum = 1
    #for url in allFriendsUrl:
    #print "开始收集第"+str(friendNum)+"个好友的数据"
    targetID = raw_input("输入想获取数据的用户id:")
    url = 'http://3g.renren.com/profile.do'
    url = url+'?id='+str(targetID)+'&sid='+str(spider.sid)
    print url

    spider.GetProfile(url)
    spider.GetStatus() 
    renrenSqlHelper.CloseSqlHelper()
