#!/usr/bin/python
#!-*-coding:utf8-*-
import sqlHelper
import sys
import re

def test(a,b={}):
	if (b=={}):
		print "asdf"
	else:
		print "调用了b"
	print a
	print b

a = 19
bb = {'d':'dd'}
test(a)
test(a,bb)

