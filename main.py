"""
爬虫运行的主程序
author = ”YiRui Wang"
创建时间 = 2020 1 13
"""


#--------用户设定参数---------


#生成URL集合的模式
URL_BUILD_MODE = 2  #--生成新的URL集合：  0
                    #--读取已有的URL仓库：1
                    #--使用单独URL测试：  2

CUT = 50

#生成URL集合的根URL
ROOT_URL = "https://search.51job.com/list/070300%252C020000,000000,0000,00,9,99,\
        %25E6%2595%25B0%25E5%25AD%2597%25E8%2590%25A5%25E9%2594%2580,2,1.html?\
        lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&\
        companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&\
        fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="

#用于测试的单独URL
TEST_URL = "https://jobs.51job.com/shanghai-ptq/119005406.html?s=01&t=0"


#用于定位目标语句的关键词(正则表达式)
KEY_WORDS1 = r"[职责|描述]"
KEY_WORDS2 = r"[要求|资格]"


#------------------------------


from urlPool import urlPool as uP
import spider
from bs4 import BeautifulSoup
import time
import random
import urls
import json


#--------定义爬虫主程序--------


def crawling():
    """
    爬虫的主程序
    """
    #----判断建立url仓库的方式
    if URL_BUILD_MODE == 1:
        #从CanNotCrawl.json文件中直接读取
        with open("./CanNotCrawl.json","r",encoding="ascii") as f:
            jobUrls = json.load(f)
    elif URL_BUILD_MODE == 2:
        #读取单独的测试url
        jobUrls = [TEST_URL]
    elif URL_BUILD_MODE == 0:
        #调用urls模块生成
        page_num = urls.getPageNum()
        pageUrls = urls.webUrlsPool(page_num)
        number0 = 0
        for pageUrl in pageUrls:
            number0 += 1
            jobUrls = urls.getJobUrls(pageUrl)
            if number0 % 5 == 0:
                randomDelay()
                print("url输入进度为：", number0)

    #----建立待爬取的url仓库
    toCrawl = uP()
    for x in jobUrls[:CUT]:
        toCrawl.pressIn(x)
    #print(toCrawl.queue)
    #----建立爬取失败的url的仓库
    CanNotCrawl = uP()
    #----建立爬取结果的储存字典
    if URL_BUILD_MODE == 1:
        # 从Results.json中读取已爬取的结果
        with open("./Results.json","r",encoding="gb18030") as f:
            result = json.load(f)
    elif URL_BUILD_MODE == 0 or URL_BUILD_MODE == 2:
        result = {}
        
    #----开始爬取--------
    #实现spider对象
    spider1 = spider.Spider()
    #建立计数器与计错器
    number1 = 0
    errorCounter = 0 # 总出错数
    errorCounter1 = 0 #keyWord1出错数
    errorCounter2 = 0 #keyWord2出错数
    errorOfparsing = 0 #解析错误AttributeError
    #开始爬取循环 
    while True:
        if number1 % 1 == 0:
            print("爬了",number1,"个,错误",errorCounter,"个,关键词1错误",errorCounter1,"个，关键词2错误",errorCounter2,"个","解析错误了",errorOfparsing,"个")
        randomDelay()
        number1 += 1
        #爬虫获取待爬url
        url1 = spider1.eatURL(toCrawl,)
        if url1 == -1:
            print("没有待爬的url啦")
            return result, CanNotCrawl
        #爬虫获取html，并解析
        #try:
        for a in range(1):#无用，调缩进
            data = spider1.fetchHtml() 
            flag, data, titleAndSalary = spider1.parsingContent(KEY_WORDS1,KEY_WORDS2)
            titleAndSalary = str(titleAndSalary)
        #except AttributeError:
        #    errorCounter += 1
        #    errorOfparsing += 1
            #continue
        #判断
        if flag == -1 or flag == -2:
            errorCounter += 1
            if flag == -2:
                errorCounter2 += 1
            if flag == -1:
                errorCounter1 += 1
            CanNotCrawl.pressIn(url1)
        result[titleAndSalary] = data


#--------定义随机时延程序--------


def randomDelay():
    """
    产生一个随机的时间延迟
    """
    time1 = random.random()
    time.sleep(time1)


#--------定义命令行运行程序---------


if __name__ == "__main__":
    #----运行爬虫主函数
    result,CanNotCrawl = crawling()
    #----将爬取结果存入文件或打印出来
    if URL_BUILD_MODE == 0 or URL_BUILD_MODE == 1:
        with open("./Results.json","w",encoding="gb18030") as f:
            json.dump(result,f,indent = 1, ensure_ascii=False)
        with open("./CanNotCrawl.json", "w") as ff:
            json.dump(CanNotCrawl.queue, ff, indent=1)
    elif URL_BUILD_MODE == 2:
        print(result)
    
