"""
author = "YiRui Wang"

定义了一个爬取数据的Spider类

创建于2020 1 13
"""

import requests
from bs4 import BeautifulSoup as bf
import parsing as p
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
        初始化蜘蛛的url、data、info。
        将haveFetchedData、haveParsedContent置否
        """
        self.url = 0
        self.data = 0
        self.info = 0
        self.haveFetchedData = 0
        self.haveParsedCotent = 0
    
    def eatURL(self, pool):
        """
        从url库中取得一个url，存入体内，返回该url
        若无url可取则返回-1
        params：
            pool：可用的url库,urlPool的一个实例
        """
        if self.url == -1:
            print("爬完啦，没得爬啦")
            return -1
        self.url = pool.popOut()
        self.haveFetchedData = 0
        self.haveParsedCotent = 0
        return self.url
            
    def fetchHtml(self, ):
        """
        根据体内的url爬取data,存入体内，返回data
        若无未爬url，则返回-1；
        若连接超时，则返回0
        """
        if self.url == 0 or self.haveFetchedData == 1:
            return -1
        try:
            self.data = requests.get(self.url, timeout=5)
        except requests.exceptions.RequestException as e:
            print(e)
            return 0 
        self.haveFetchedData = 1
        return self.data
        
    def parsingContent(self, keyWords1, keyWords2):
        """
        根据体内爬取的data(html)，提取出所需要素，返回要素
        若要素已解析，返回0
        params:
            keyWords1: 待爬取结果的第一个关键字
            keyWords2: 待爬取结果的第二个关键字
        """
        if self.haveParsedCotent == 2:
            return 0
        #----从职位信息中抓取工作职责（data1）,任职要求(data2)与职位薪资与公司名称（titleAndSalary）
        data1, data2, titleAndSalary = pt(self.data, keyWords1, keyWords2)
        #----识别找不到关键词，返回-1或-2与职位薪资与公司名称
        if data1 == -2:
            #print("找不到职责")
            return -1, [data2,], titleAndSalary
        if data2 == -2:
            #print("找不到要求/资格")
            return -2, [data1,], titleAndSalary
        # ----print("data",data)
        # ----建立工作职责与任职要求的列表
        data = [data1, data2]
        return 1, data, titleAndSalary
        
