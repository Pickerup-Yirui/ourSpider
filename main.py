"""
爬虫运行的主程序
author = ”YiRui Wang"
创建时间 = 2020 1 13
"""

from urlPool import urlPool as uP
import spider
from bs4 import BeautifulSoup  
import time
import random
import urls
import json
#import pandas as pd 
#import numpy as np

#--------定义随机时延程序
def randomDelay():
    """
    产生一个随机的时间延迟
    """
    time1 = random.random()
    time.sleep(time1)

#--------定义爬虫主程序--------
def crawling():
    """
    爬虫的主程序
    """
    #----建立待爬取的url仓库
    toCrawl = uP()
    page_num = urls.getPageNum("0300")
    pageUrls = urls.webUrlsPool(page_num)
    number0 = 0
    for pageUrl in pageUrls[:1]:
        number0 += 1
        pageUrl = urls.getJobUrls(pageUrl)
        for x in pageUrl:
            toCrawl.pressIn(x)
        if number0 % 5 == 0:
            randomDelay()
            print("url输入进度为：",number0)
    print(toCrawl.queue)
    #toCrawl.pressIn(
    #    "https://jobs.51job.com/shanghai-ptq/119005406.html?s=01&t=0")  # 测试用例
    #----建立爬取失败的url的仓库
    CanNotCrawl = uP()
    #----建立爬取结果的储存字典
    result = {}
    #----开始爬取
    spider1 = spider.Spider()
    number1 = 0
    errorCounter = 0
    while True:
        number1 += 1
        if number1 % 100 == 0:
            print("爬了",number1,"个,错误",errorCounter,"个")
        randomDelay()
        url1 = spider1.eatURL(toCrawl,)
        if url1 == -1:
            print("没有待爬的url啦")
            return result, CanNotCrawl
        try:
            data = spider1.fetchHtml() 
            flag, data, titleAndSalary = spider1.parsingContent()
        except AttributeError:
            continue
        if flag == -2:
            #print("爬取出错啦")
            errorCounter += 1
            result[titleAndSalary] = data
            CanNotCrawl.pressIn(url1)
        else:
            titleAndSalary = str(titleAndSalary)
            result[titleAndSalary] = data

if __name__ == "__main__":
    result,CanNotCrawl = crawling()
    #print("爬取结果是：\n",result,"\n")

    # df = pd.DataFrame(result, index = result.key, columns = [value1, value2])

    with open("./Results.json","w",encoding="gb18030") as f:
        json.dump(result,f,indent = 1, ensure_ascii=False)
    #print("爬不出来的是：",CanNotCrawl.queue)
    with open("./CanNotCrawl.json","w") as ff:
        json.dump(CanNotCrawl.queue,ff,indent = 1)
