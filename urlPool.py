"""
author = "YiRui Wang"

定义了一个储存url的仓库类

创建于2020 1 13
"""

class urlPool():
    """
    一个储存url的仓库类
    pressIn(self, url)：压入一个url,返回1
    popOut(self,):弹出一个url，返回该url或-1
    howMany(self,):返回当前url的数量
    """
    def __init__(self,):
        """
        建立一个内置队列，储存url,并初始化为空
        """
        self.queue = []
    
    def pressIn(self, url):
        """
        将一个url压入,成功则返回1
        params：
            url：待压入的url
        """
        self.queue.append(url)
        #print(self.queue)
        return 1

    def popOut(self,):
        """
        将一个url弹出，成功则返回url,若队列为空返回-1
        """
        #print(self.queue)
        if len(self.queue) != 0:
            #print(self.queue)
            #print("going to pop")
            return self.queue.pop(0)
            #print(self.queue)
        else:
            return -1
    
    def howMany(self,):
        """
        查询队列中还有多少url，返回url数量
        """
        return len(self.queue)

if __name__ == "__main__":
    testPool = urlPool()
    print(testPool.pressIn(10))
    print(testPool.popOut())
    print(testPool.howMany())
