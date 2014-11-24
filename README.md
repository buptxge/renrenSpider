RenrenSpider
============

关于人人网的爬虫，需要验证自己账户。

###相关包
BeautifulSoup4
地址：[http://www.crummy.com/software/BeautifulSoup/](http://www.crummy.com/software/BeautifulSoup/ "Title")

###v1.0
    用户首先输入账号密码，运行程序，程序自动爬取数据，结果存放在相对路径/UserData/人人网id文件中。
    可以抓取用户状态信息，分为状态发布时间，状态内容，转发状态原文等，以文本方式存储。

###v2.0
	添加数据库存储功能，存储为两个表，分别为UserInfo和Status。
	修复部分状态爬取bug，包括带链接状态显示错误等。
	添加更多详细人人数据，包括用户个人资料、日志数、相册数等，并提供爬取所有好友列表的功能。
	优化代码结构。

	
