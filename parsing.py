"""
author = "YiRui Wang"

定义一系列解析文本的函数

创建于2020 1 14
"""
import re
from bs4 import BeautifulSoup

def parsingText(html0,keyWords1,keyWords2):
    """
    输入待解析html，返回解析的结果 （以列表的形式）
    params:
        html0: html
        keyWords1: 待爬取结果的第一个关键字
        keyWords2: 待爬取结果的第二个关键字
    """
    html0 = decoding(html0, 'gb18030')
    jobInfo = findJobInfo(html0)
    titleAndSalary = findTitle(html0)
    # ----从职位信息中抓取工作职责（data1）,任职要求(data2)与职位薪资与公司名称（titleAndSalary）
    data1 = findText(jobInfo, r"[\u4e00-\u9fa5]{0-2}[职责|描述].*")
    data2 = findText(jobInfo, r"[\u4e00-\u9fa5]{0-2}"+keyWords2)
    return data1, data2, titleAndSalary

def decoding(data,form):
    """
    将输入的data解码为form格式的文本，并返回bs4对象
    params：
        data：（requests对象）待解码的data
        form：解码的格式
    """
    data.encoding = form  #'gb18030'
    dataContent = data.text
    dataContent = BeautifulSoup(dataContent,'html.parser')
    return dataContent

def findJobInfo(data):
    """
    从输入的data中寻找到，工作描述段，并返回（bs4对象）#适用于51job
    params:
        data：（bs4对象）被查找的html
    """
    jobInfo = data.find('div',class_='bmsg job_msg inbox')
    # jobInfo = jobInfo.text() #去除标签
    return jobInfo

def findText(data,text):
    """
    从输入的data中解析出到以text开头，并以数字序号串联的一段话,若找不到text开头，则返回-2,若找到不到数字序号，则返回0
    params：
        data：被查找的范围
        text：要找到的目标
    """
    #----要返回的aim
    aimString = []
    #----构造正则对象
    aimPattern = re.compile(text)
    numPattern = re.compile(r"^[1-9①②③④⑤⑥⑦⑧⑨].*")
    HanZiPattern = re.compile(r"[\u4e00-\u9fa5]*")
    # lengthPattern = re.compile(r"^")
    #----迭代data子tag
    dataChildren = [x for x in data.children]
    for x in dataChildren:
        print("x是",x)
        #try:
        for a in range(1):
            y = x.text()
        #except AttributeError:
        #    y = ""
        print("y是",y)
        if re.match(aimPattern, y) != None:
            aimString.append(y)
            flag = 0
            while flag == 0:
                x = x.next_sibling
                #try:
                for a in range(1):
                    y = x.text()
                #except AttributeError:
                #    y = ""
                if re.match(numPattern,y) != None:
                    print("数字match")
                    aimString.append(y)                   
                elif re.match(HanZiPattern,y) != None:
                    flag = 1
                    print("下一个为：",y)
                    if len(aimString) == 1:
                        return 0
                    print("aimString",aimString)
                    return aimString  
    return -2
            
def findTitle(data):
    """
    寻找jobUrl的title、公司、薪水（来作为字典的key）
    params:
        data:使用bf4 解析好的html文档
    """
    title = data.find('h1')
    try:
        salary = title.next_sibling
        salary = salary.text
    except AttributeError:
        salary = ""
    title = title.text
    company = data.find('div', class_='com_msg')
    comName = company.text()
    comName = comName[:-1]
    titleAndSalary = (title, salary, comName)

    return titleAndSalary




