# -*- coding: utf-8 -*-
import urllib2
import urllib
import os


class GetHtml:
	title = "http://class.sise.com.cn:7001"
	
	def get_html(self,url):
		return urllib2.urlopen(url).read()
	
	def get_html_suffix(self,url):
		return urllib2.urlopen(self.title+url).read()