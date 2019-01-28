# -*- coding: utf-8 -*-
#####爬取project的label种类数目
#####地址：https://api.github.com/repos/rails/rails/labels
import xlrd
import itertools
import json
import os
import scrapy
from scrapy import Request

class pullRequestSpider(scrapy.spiders.Spider):

    name = "commitComments1" #爬虫名称
    allowed_domains = ["github.com"] #制定爬取域名
    num = 1 # 页数，默认从第一页开始
    handle_httpstatus_list = [404, 403, 401,500] #如果返回这个列表中的状态码，爬虫也不会终止
    output_file = open('commitComments2', "w") #输出文件
    crawlResult = []
    allRes = []
    crawlList = []
    index=0
    error=0  
  
    def __init__(self): #初始化
        scrapy.spiders.Spider.__init__(self)
        self.token_list = []
        self.filepath = r'/media/mamile/DATA1/G盘文件夹/beihang_study/scapy_spider/多线程爬取pr的commit/crawlComments1/commitComments'
        with open(self.filepath,"r") as e:
            for line in e:
                data = json.loads(line)
		self.crawlList.append([data['comments_url'],data["pullRequestID"],data["owner"]])

        self.token_list = [
	'f0f1147d70df77018989579552b83e616a9286c0',
	'74d04340a4852d69b7984a4823e2ae864037aa4b',
	'b0deefda65f81ca88228870966dc6ccbeae074bd',]
        self.token_iter = itertools.cycle(self.token_list) #生成循环迭代器，迭代到最后一个token后，会重新开始迭代    

    def __del__(self): #爬虫结束时，关闭文件
        self.output_file.close()

    def start_requests(self):
        start_urls = [] #初始爬取链接列表
        url = self.crawlList[self.index][0]+"?per_page=99&page="+str(self.num) ##第一条爬取url
        #添加一个爬取请求
        start_urls.append(scrapy.FormRequest(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en',
            'Authorization': 'token ' + self.token_iter.next(),#这个字段为添加token字段
            },dont_filter=True, callback=self.parse)) 

        return start_urls

    def yield_request(self): #定义一个生成请求函数
        url = self.crawlList[self.index][0]+"?per_page=99&page="+str(self.num) #第一条爬取url
        #返回请求
        return Request(url,headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en',
                'Authorization': 'token ' + self.token_iter.next(),
                },dont_filter=True,callback=self.parse)

    #解析函数
    def parse(self, response,max=5):
        if self.index == self.crawlList.__len__():
            return

        if response.status in self.handle_httpstatus_list:#如果遇见handle_httpstatus_list中出现的状态码
            print '**************************'
            self.error+=1
            if self.error==max:
                self.index+=1
                self.num=1
                self.error=0
            if self.index == self.crawlList.__len__():
                return
            else:
                yield self.yield_request() #产生新的请求
            return

        json_data = json.loads(response.body_as_unicode()) #获取json
        length = len(response.body_as_unicode()) #获取json长度
        #print (json_data==None)
        if length > 5:
            self.error=0
            self.num = self.num + 1
            for issue in json_data:
                if issue == None:
                    continue
                data = {}
                data['body']=issue.get("body",None)
		if 'user' in issue and issue['user'] != None:
                    data["user"]=issue["user"].get("login",None)
		else:
		    data['user']=None
		data['owner'] = self.crawlList[self.index][-1]
		data['pullRequestID'] = self.crawlList[self.index][1]
		data['created_at'] = issue.get('created_at',None)
            	self.output_file.write(json.dumps(data)+'\n') #输出每一行，格式也为json
            self.output_file.flush()
            yield self.yield_request() #产生新的请求

        else: #意味着爬取到最后一页
            self.error=0
            self.index+=1          
            self.num=1
            if self.index == self.crawlList.__len__():
                self.__del__()
                return
            else:
                yield self.yield_request() #产生新的请求