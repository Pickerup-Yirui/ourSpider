"""
author = "YiRui Wang"

定义了一个爬取数据的Spider类

创建于2020 1 13
"""

import requests
from bs4 import BeautifulSoup as bf
import parsing
from parsing import parsingText as pt 

class Spider():
    """
    一个根据读取的URL爬取相关数据的da蜘蛛
    eatURL(self, pool):从url库中取得一个url，存入体内，返回该url
    fetchHtml(self,)：根据体内的url爬取数据,存入体内，返回数据
    parsingContent(self,):根据体内爬取的数据，提取出所需要素，返回要素
    """
    def __init__(self,):
        """
        初始化蜘蛛的url、data、info,
        以及haveFetchedHtml、haveParsedContent
        """
        self.url = 0
        self.html = 0
        self.info = 0
        self.haveFetchedHtml = 0
        self.haveParsedContent = 0
    
    def eatURL(self, pool):
        """
        从url库中取得一个url，存入体内，返回该url
        若无url可取则返回-1
        params：
            pool：可用的url库,urlPool的一个实例
        """
        self.url = pool.popOut()
        if self.url == -1:
            print("爬完啦，没得爬啦")
            return -1
        #将haveFetchedHtml和haveParsedContent置零
        self.haveFetchedHtml = 0
        self.haveParsedContent = 0
        return self.url
            
    def fetchHtml(self, ):
        """
        根据体内的url爬取data,存入体内，返回data
        若无未爬url，则报错；
        若连接超时，则返回0
        """
        #判断是否已经取过html
        assert self.haveFetchedHtml != 1
        try:
            self.html = requests.get(self.url, timeout=5)
        except requests.exceptions.RequestException as e:
            print(e)
            return 0 
        self.haveFetchedHtml = 1
        return self.html
        
    def parsingContent(self, keyWords1, keyWords2):
        """
        根据体内爬取的html文件，提取出目标要素,
        返回flag(int), data(list), titleAndSalary(tuple)
        flag =  0：网页无法解析
        flag = -1：找不到关键词1，data中关键词1为空
        flag = -2：找不到关键词2，data中关键词2为空
        flag = -3：两个关键词都找不到
        params:
            keyWords1: 待爬取结果的第一个关键字
            keyWords2: 待爬取结果的第二个关键字
        """
        #判断要素是否已经经过解析
        assert self.haveParsedContent != 1
        #解析html生成bs4对象
        bs40 =parsing.decoding(self.html,"gb18030") #"gb18030"
        #解析html生成titleAndSalary
        titleAndSalary =parsing.findTitle(bs40)
        if titleAndSalary == 0:
            return 0, [], ()
        #解析bs4对象，找到岗位信息段的bs4对象
        bs41 = parsing.findJobInfo(bs40)
        if bs41 == 0:
            return 0, [], ()
        #解析岗位信息段，找出目标信息
        #data1 = parsing.findText(bs41, r"[\u4e00-\u9fa5]{2}"+keyWords1)
        data1 = parsing.findText1(bs41)
        data2 = parsing.findText(bs41, r"[\u4e00-\u9fa5]{2}"+keyWords2)
        errorCounter = 0
        flag = 1
        if data1 == -2 or data1 == 0:
            errorCounter += 1
            flag = -1
            data1 = []
        if data2 == -2 or data2 == 0:
            errorCounter += 1
            flag = -2
            data2 = []
        if errorCounter == 2:
            flag = -3
        data = [data1, data2]
        #print("flag",flag)
        return flag, data, titleAndSalary
        
