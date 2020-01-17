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
        * 若无数据，则返回0 *
        """
        if self.url == 0 or self.haveFetchedData == 1:
            return -1
        self.data = requests.get(self.url)
        self.haveFetchedData = 1
        return self.data
        
    def parsingContent(self,):
        """
        根据体内爬取的data(html)，提取出所需要素，返回要素
        若要素已解析，返回-1
        * 若data中目标要素无法获取，返回0 *
        """
        if self.haveParsedCotent == 2:
            return -1
        #----从职位信息中抓取工作职责（data1）,任职要求(data2)与职位薪资与公司名称（titleAndSalary）
        data1, data2, titleAndSalary = pt(self.data)
        #----识别找不到关键词（-2）或数字（0）的情况，返回-2与职位薪资与公司名称
        if data1 == -2 or data1 == 0:
            #print("找不到职责")
            return -2, [data2,], titleAndSalary
        if data2 == -2 or data2 == 0:
            #print("找不到要求/资格")
            return -2, [data1,], titleAndSalary
        # ----print("data",data)
        # ----建立工作职责与任职要求的列表
        data = [data1, data2]
        return 1, data, titleAndSalary
        
