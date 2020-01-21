import xlwt
import json


def excelWriter(result):
    """
    输入result,将result里的内容写入excel
    """
    #----检查输入参数类型----
    if type(result) != type({}):
        raise TypeError
    #----创建workbook----
    workbook = xlwt.Workbook(encoding="gb18030")
    worksheet = workbook.add_sheet("worksheet1")
    worksheet.write(0,0,"Job Title")
    worksheet.write(0,1,"Salary/month")
    worksheet.write(0,2,"Company Name")
    worksheet.write(0,3,"Job Descriptions")
    worksheet.write(0,4,"Requirements")

    #----遍历result，清洗和填入
    rawNumber = 1
    columnNumber = 0
    keyList = list(result)
    for key in keyList:
        #填入jobTitleSalary
        jobTitle = tuple(eval(key))
        for text in jobTitle:
            worksheet.write(rawNumber,columnNumber,text)
            columnNumber += 1
        #对工作职责和任职要求清洗
        for list0 in result[key]:
            text1 = ""
            monoSet = set()
            if list0 != []:
                for text in list0[1:]:
                    if not(text in monoSet):
                        text1 += text
                        monoSet.add(text)
                text1 = text1.replace("\ax0","")
            #填入职责或要求
            worksheet.write(rawNumber,columnNumber,text1)
            columnNumber += 1
        rawNumber += 1
        columnNumber = 0
    workbook.save("spider.xls")


if __name__ == "__main__":
    with open("./Results.json", "r", encoding="gb18030") as f:
        result = json.load(f)
    print(result)
    excelWriter(result)
