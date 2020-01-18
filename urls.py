"""
author = "YiRui Wang"

定义了一系列抓取51jobs页面上urls的函数（包）

创建于2020 1 16

getPageNum(num):根据初始url找到并返回网页总页数
webUrlsPool(page_num):根据得到的网页总数，构造并返回所有符合搜索标准的网页url列表
getJobUrls(pageUrl):根据pageUrl,得到该page上的jobUrl

"""

import requests
from bs4 import BeautifulSoup

def getPageNum():
    """
    根据初始url找到并返回网页总页数
    """
    # keyword = quote(keyword, safe='/:?=')
    
    url = 'https://search.51job.com/list/070300%252C020000,000000,0000,00,9,99,\
        %25E6%2595%25B0%25E5%25AD%2597%25E8%2590%25A5%25E9%2594%2580,2,1.html?\
        lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&\
        companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&\
        fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
    html = requests.get(url)
    html.encoding = 'gb18030'
    soup = BeautifulSoup(html.text, "lxml") # 用html.content需要的代码较少，不需要解码编码的调整
    span = soup.find('div', class_='p_in').find('span', class_='td')
    page_num = span.get_text(strip= True).replace('共', '').replace('页，到第', '')
    return page_num


def webUrlsPool(page_num):
    """
    根据得到的网页总数，构造并返回所有符合搜索标准的网页url列表
    params:
        page_num:根据初始url获得的网页页数
    """
    pageUrls = []
    page_num = int(page_num)
    for i in range(1,page_num + 1):
        url = 'https://search.51job.com/list/070300%252C020000,000000,0000,00,9,99,%25E6%2595%25B0%25E5%25AD%2597%25E8%2590%25A5%25E9%2594%2580,2,' + str(i) + \
            '.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
        pageUrls.append(url)
    
    return pageUrls

# webUrlsPool()



# -*- coding: gb2312 -*-


def getJobUrls(pageUrl,):
    """
    根据pageUrl,得到该page上的jobUrl列表
    params:
        pageUrl:搜索结果的一页
    """
    
    # 用requests请求网页url
    r = requests.get(pageUrl)
    r.encoding = 'gb18030'
    htmlContents = r.text
        
    # 用beautifulsoup，找到岗位urls，并添加到pool中
    htmlSoup = BeautifulSoup(htmlContents,'html.parser')
    withTags = htmlSoup.find_all('p',class_='t1')
    # 删掉第0个元素--html文档中表格标头，不含有目标信息（岗位url）
    del withTags[0]
    # 找到岗位url，并返回
    urls0 = [] 
    for a in withTags:
        b = a.find('a')
        urls0.append(b['href'])
    return urls0
