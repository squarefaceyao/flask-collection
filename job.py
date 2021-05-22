import threading, time
from random import random
from db import DB
def ReturnAD():
    # 采集频率RF的含义是1S保存几个点。0.5HZ = 1秒0.5个点。或者说：2秒1个点
    # t秒保存一个次数值

    ad1 = random() * 100
    ad2 = random() * 100
    ad3 = random() * 100
    ad4 = random() * 100
    ad5 = random() * 100
    ad6 = random() * 100
    ad7 = random() * 100
    ad8 = random() * 100
    return (ad1, -ad2, ad3, ad4, ad5, ad6, ad7, ad8)


def run_ad(table_name,RF):
    db=DB()
    ad1, ad2, ad3, ad4, ad5, ad6, ad7, ad8 = ReturnAD()
    t = 1 / RF
    time.sleep(t)  # 暂停的秒数，t秒保存一个次数值
    # i = i + 1  # 时间
    data = [ad1, ad2, ad3, ad4, ad5, ad6, ad7, ad8]
    #print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    #print(data)
    db.write(table_name, ad1, ad2, ad3, ad4, ad5, ad6, ad7, ad8)


class Job(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(Job, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()  # 用于暂停线程的标识
        self.__flag.set()  # 设置为True
        self.__running = threading.Event()  # 用于停止线程的标识
        self.__running.set()  # 将running设置为True


    def run(self,table_name, RF):

        db = DB()
        db.create(table_name)
        while self.__running.isSet():
            self.__flag.wait()  # 为True时立即返回, 为False时阻塞直到self.__flag为True后返回
            #print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            run_ad(table_name, RF)


    def pause(self):
        self.__flag.clear()  # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()  # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.set()  # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()  # 设置为False

    def flag(self):
        return self.__flag
