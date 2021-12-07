import threading, time
from random import random
from db import DB
from ctypes import *
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

def get_7606():
    try:
        res =  cdll.LoadLibrary("./spi.so")
        #设备初始化
        res.pinInit()
        #设置输入范围  5 = ±5   10 =±10
        res.ad7606_SetRange(10)
        #设置过采样模式（数字滤波，硬件求平均值)
        #*	形    参：_ucMode : 0-6  0表示无过采样，1表示2倍，2表示4倍，3表示8倍，4表示16倍	5表示32倍，6表示64倍
        res.ad7606_SetOS(6)     #设置物理滤波器
        while (1):
            res.ad7606_readChannel()
            channel1=res.getValue(4)/32768*res.getRange()
            channel2=res.getValue(5)/32768*res.getRange()
            channel3=res.getValue(6)/32768*res.getRange()
            channel4=res.getValue(7)/32768*res.getRange()
            channel5=res.getValue(0)/32768*res.getRange()
            channel6=res.getValue(1)/32768*res.getRange()
            channel7=res.getValue(2)/32768*res.getRange()
            channel8=res.getValue(3)/32768*res.getRange()
            print("nadao-----8",channel8)
            return [channel1,channel2,channel3,channel4,channel5,channel6,channel7,channel8]


    except :
        GPIO.cleanup()
        print ("\r\nProgram end     ")
        exit()

# 获取树莓派上的数值
def ReturnADs():
    ADC_Value = get_7606()
    # ad1 = (ADC_Value[0]*5.0/0x7fffff)
    # ad2 = (ADC_Value[1]*5.0/0x7fffff)
    # ad3 = (ADC_Value[2]*5.0/0x7fffff)
    # ad4 = (ADC_Value[3]*5.0/0x7fffff)
    # ad5 = (ADC_Value[4]*5.0/0x7fffff)
    # ad6 = (ADC_Value[5]*5.0/0x7fffff)
    # ad7 = (ADC_Value[6]*5.0/0x7fffff)
    # ad8 = (ADC_Value[7]*5.0/0x7fffff)

    ad1 = (ADC_Value[1]*10) # 单位转为mv
    ad2 = (ADC_Value[1]*10)
    ad3 = (ADC_Value[2]*10)
    ad4 = (ADC_Value[3]*10)
    ad5 = (ADC_Value[4]*10)
    ad6 = (ADC_Value[5]*10)
    ad7 = (ADC_Value[6]*10)
    ad8 = (ADC_Value[7]*10)
#    print([ad1, ad2, ad3, ad4, ad5, ad6, ad7, ad8])
    return (ad1, ad2, ad3, ad4, ad5, ad6, ad7, ad8)


def run_ad(table_name,RF):
    db=DB()
    ad1, ad2, ad3, ad4, ad5, ad6, ad7, ad8 = ReturnADs()
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
