#! /usr/lib/python
#-*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *
import sys

class Render(QWebPage):
	def __init__(self,url):
		self.app = QApplication(sys.argv)
		QWebPage.__init__(self)
		self.loadFinished.connect(self._loadFinished)
		self.mainFrame().load(QUrl(url))
		self.app.exec_()
	
	def _loadFinished(self,result):
		self.frame = self.mainFrame()
		self.app.quit()

if __name__ == "__main__":
    url = 'http://webscraping.com'
    r = Render(url)
    html = r.frame.toHtml()
    print html.toUtf8()    
