"""
author = "YiRui Wang"

定义一系列解析文本的函数

创建于2020 1 14
"""
import re
from bs4 import BeautifulSoup
import bs4

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
    if jobInfo is None:
        return -3,-3,-3
    titleAndSalary = findTitle(html0)
    # ----从职位信息中抓取工作职责（data1）,任职要求(data2)与职位薪资与公司名称（titleAndSalary）
    
    
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

def findJobInfo(bs40):
    """
    从输入的bs4对象中寻找到岗位信息段，并返回其bs4对象,若找不到，则返回0#适用于51job
    params:
        data：（bs4对象）被查找的html
    """
    jobInfo = bs40.find('div',class_='bmsg job_msg inbox')
    if jobInfo == None:
        return 0
    return jobInfo

def findText1(bs41,):
    """
    从岗位信息段的bs4对象中解析出开头处以数字序号串联的一段话，若找不到这段话，则返回-2或0（超范围或找不到任何内容）
    用于jobInfok开头没有keyword1，但是有数字序号出现的情况
    params:
        bs41:由网址获得的bs4对象中，岗位信息段
    """
    #----要返回的aim
    aimString = []
    #构造正则对象
    numPattern = re.compile(r"^[1-9①②③④⑤⑥⑦⑧⑨].*") #"为什么要使用."
    HanZiPattern = re.compile(r"[\u4e00-\u9fa5]+")
    #生成岗位信息段の子对象
    dataChildren = [x for x in bs41.children]
    for x in dataChildren:
        if type(x) != bs4.element.NavigableString:
            y = x.get_text()
        else:
            y = "0"
        #滤除超范围串：即没有KeyWord1也没有数字序号为开头的情况。
        if re.match(HanZiPattern,y) != None:
            #print("超范围")
            return 0
        #匹配开始串
        if re.search(numPattern,y) != None:
            aimString.append("工作职责:")
            aimString.append(y)
            flag = 0
            while flag == 0:
                if x != None:
                    x = x.next_sibling
                else:
                    if len(aimString) == 1:
                        return 0
                    return aimString
                if type(x) == bs4.element.NavigableString or x == None:
                    y = ""
                else:
                    y = x.get_text()
                #匹配中间串
                if re.search(numPattern,y)!= None:
                    aimString.append(y)
                #匹配末尾串
                elif re.match(HanZiPattern,y) != None:
                    flag = 1
                    if len(aimString) == 1:
                        return 0
            return aimString


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
        #print("x是",x)
        #print("type(x)是", type(x))
        if type(x) != bs4.element.NavigableString:
            y = x.get_text()
        else:
            y = ""
        if re.match(aimPattern, y) != None:
            aimString.append(y)
            flag = 0
            while flag == 0:
                if x != None:
                    x = x.next_sibling
                else:
                    if len(aimString) == 1:
                        return 0
                    return aimString
                if type(x) == bs4.element.NavigableString or x == None:
                    #print("NavigatableString x is:", x)
                    y == ""
                else:
                    y = x.get_text()
                if re.match(numPattern,y) != None:
                    #print("数字match")
                    aimString.append(y)                   
                elif re.match(HanZiPattern,y) != None:
                    flag = 1
                    #print("下一个为：",y)
                    if len(aimString) == 1:
                        return 0
                    return aimString  
    return -2
            
def findTextHelp():
    """
    findText的辅助函数,输入bs4目标段的子对象，返回解析后提取的
    """
    pass

def findTitle(bs40):
    """
    输入解析后的bs4对象,返回jobUrl的title、公司、薪水信息的元组,若解析出错，则返回0
    params:
        data:使用bf4 解析好的html文档
    """
    #找到title和Salary
    title = bs40.find('h1')
    if title is None:
        return 0
    else:
        salary = title.next_sibling
        salary = salary.text
        title = title.text
    #找到company
    company = bs40.find('div', class_='com_msg')
    if company == None:
        return 0
    else:
        comName = company.get_text()
        comName = comName[:-1]
        titleAndSalary = (title, salary, comName)
    return titleAndSalary




